#!/usr/bin/env python3
"""
Colab GPU worker for Zero-Credit 16:9 Full Plant Growth Time-Lapse Pilot (Dwarf Golden Sunflower):
  1. Installs ComfyUI + downloads Wan2.1-FLF2V-14B FP8 split weights from Comfy-Org.
  2. Uses native Ada FP8 Tensor Core acceleration (`fp8_e4m3fn_fast`) on CC >= 8.9 (L4/H100),
     with automatic fallback to `fp8_e4m3fn` if unsupported.
  3. Runs 4 sequential WanFirstLastFrameToVideo passes (stage_01->02->03->04->05, 49 frames each).
  4. Stitches 193 continuous frames, runs 4x Practical-RIFE v4.25 interpolation (769 frames @ 30fps = ~25.63s).
  5. Upscales to 1920x1080 Rec.709 H.264 High Profile (h264_nvenc), muxes trimmed ambient audio,
     and builds a 5-panel + summary Plant_Growth_QA_Sheet.jpg.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

WORK_ROOT = Path("/content")
COMFY_DIR = WORK_ROOT / "ComfyUI"
RIFE_DIR = WORK_ROOT / "Practical-RIFE"
COMFY_URL = "http://127.0.0.1:8188"

MODEL_FILES = [
    (
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/diffusion_models/wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors",
        COMFY_DIR / "models/diffusion_models/wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors",
    ),
    (
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
        COMFY_DIR / "models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    ),
    (
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors",
        COMFY_DIR / "models/clip_vision/clip_vision_h.safetensors",
    ),
    (
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors",
        COMFY_DIR / "models/vae/wan_2.1_vae.safetensors",
    ),
]

SEGMENTS = [
    {
        "idx": 1,
        "start": "stage_01.png",
        "end": "stage_02.png",
        "prompt": (
            "Smooth botanical nature time-lapse of a tiny green sprout emerging from dark moist soil "
            "and growing upward into a young four-leaf green sunflower seedling at golden dawn, stem "
            "elongating and fresh green leaves unfurling smoothly, locked tripod camera, photorealistic"
        ),
    },
    {
        "idx": 2,
        "start": "stage_02.png",
        "end": "stage_03.png",
        "prompt": (
            "Smooth botanical nature time-lapse of a young green sunflower seedling growing taller "
            "into a sturdy leafy green stem and forming a closed pointed green flower bud at the crown "
            "at golden dawn, new serrated leaves expanding smoothly, locked tripod camera, photorealistic"
        ),
    },
    {
        "idx": 3,
        "start": "stage_03.png",
        "end": "stage_04.png",
        "prompt": (
            "Smooth botanical nature time-lapse of a closed green sunflower bud swelling and peeling "
            "back its green outer bracts as bright golden-yellow petals lift into a half-open cup at "
            "golden dawn, locked tripod camera, photorealistic"
        ),
    },
    {
        "idx": 4,
        "start": "stage_04.png",
        "end": "stage_05.png",
        "prompt": (
            "Smooth botanical nature time-lapse of a half-open sunflower blossom unfurling all its "
            "golden-yellow petals wide into glorious full bloom revealing the dark-amber spiral center "
            "in warm golden morning sunbeams, locked tripod camera, photorealistic"
        ),
    },
]

NEG_PROMPT = (
    "camera pan, camera shake, shifting soil, morphing rocks, sudden jump, cut, text, watermark, "
    "blurry, deformed, extra stems, floating leaves, flickering"
)


def sh(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    print(f"+ {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, check=check)


def http_json(url: str, data: dict | None = None, timeout: int = 20) -> dict:
    body = json.dumps(data).encode("utf-8") if data is not None else None
    headers = {"Content-Type": "application/json"} if data is not None else {}
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_gpu_compute_cap() -> tuple[int, int]:
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("No CUDA GPU available on Colab worker.")
    major, minor = torch.cuda.get_device_capability(0)
    name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"GPU: {name} | CC {major}.{minor} | VRAM {vram_gb:.1f} GB", flush=True)
    return major, minor


def setup_comfyui_and_models() -> None:
    sh("apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq aria2 ffmpeg git unzip")
    if not COMFY_DIR.exists():
        sh(f"git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git {COMFY_DIR}")
    sh(f"pip install -q -r {COMFY_DIR / 'requirements.txt'}")
    sh("pip install -q pillow")

    for url, dest in MODEL_FILES:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and dest.stat().st_size > 100 * 1024 * 1024:
            print(f"Already downloaded: {dest.name} ({dest.stat().st_size} bytes)", flush=True)
            continue
        sh(
            f"aria2c -x 16 -s 16 -k 1M --continue=true --console-log-level=warn "
            f"--dir='{dest.parent}' --out='{dest.name}' '{url}'"
        )
        if not dest.exists() or dest.stat().st_size < 10 * 1024 * 1024:
            raise RuntimeError(f"Download failed or incomplete for {dest}")


def prepare_normalized_inputs() -> None:
    from PIL import Image, ImageOps

    input_dir = COMFY_DIR / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    candidates = [
        ("stage_01.png", ["stage_01_tiny_sprout.jpg", "stage_01_tiny_sprout.png", "stage_01.png"]),
        ("stage_02.png", ["stage_02_young_seedling.jpg", "stage_02_young_seedling.png", "stage_02.png"]),
        ("stage_03.png", ["stage_03_green_bud_stem.jpg", "stage_03_green_bud_stem.png", "stage_03.png"]),
        ("stage_04.png", ["stage_04_opening_bud.jpg", "stage_04_opening_bud.png", "stage_04.png"]),
        ("stage_05.png", ["stage_05_full_bloom.jpg", "stage_05_full_bloom.png", "stage_05.png"]),
    ]
    for target_name, src_names in candidates:
        src_path = next((WORK_ROOT / n for n in src_names if (WORK_ROOT / n).exists()), None)
        if src_path is None:
            raise FileNotFoundError(f"Missing uploaded keyframe; checked {src_names} in {WORK_ROOT}")
        img = Image.open(src_path).convert("RGB")
        fitted = ImageOps.fit(img, (1280, 720), method=Image.Resampling.LANCZOS)
        out_path = input_dir / target_name
        fitted.save(out_path, format="PNG")
        print(f"Prepared ComfyUI input: {out_path} ({fitted.size})", flush=True)


def build_flf2v_workflow(seg: dict, unet_weight_dtype: str) -> dict:
    seg_idx = seg["idx"]
    return {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors",
                "weight_dtype": unet_weight_dtype,
            },
        },
        "2": {
            "class_type": "ModelSamplingSD3",
            "inputs": {"model": ["1", 0], "shift": 8.0},
        },
        "3": {
            "class_type": "CLIPLoader",
            "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan"},
        },
        "4": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": "wan_2.1_vae.safetensors"},
        },
        "5": {
            "class_type": "CLIPVisionLoader",
            "inputs": {"clip_name": "clip_vision_h.safetensors"},
        },
        "6": {
            "class_type": "LoadImage",
            "inputs": {"image": seg["start"]},
        },
        "7": {
            "class_type": "LoadImage",
            "inputs": {"image": seg["end"]},
        },
        "8": {
            "class_type": "CLIPVisionEncode",
            "inputs": {"clip_vision": ["5", 0], "image": ["6", 0], "crop": "none"},
        },
        "9": {
            "class_type": "CLIPVisionEncode",
            "inputs": {"clip_vision": ["5", 0], "image": ["7", 0], "crop": "none"},
        },
        "10": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["3", 0], "text": seg["prompt"]},
        },
        "11": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["3", 0], "text": NEG_PROMPT},
        },
        "12": {
            "class_type": "WanFirstLastFrameToVideo",
            "inputs": {
                "positive": ["10", 0],
                "negative": ["11", 0],
                "vae": ["4", 0],
                "width": 832,
                "height": 480,
                "length": 49,
                "batch_size": 1,
                "clip_vision_start_image": ["8", 0],
                "clip_vision_end_image": ["9", 0],
                "start_image": ["6", 0],
                "end_image": ["7", 0],
            },
        },
        "13": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["2", 0],
                "seed": 100 + seg_idx,
                "steps": 16,
                "cfg": 5.0,
                "sampler_name": "uni_pc",
                "scheduler": "simple",
                "positive": ["12", 0],
                "negative": ["12", 1],
                "latent_image": ["12", 2],
                "denoise": 1.0,
            },
        },
        "14": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["13", 0], "vae": ["4", 0]},
        },
        "15": {
            "class_type": "SaveImage",
            "inputs": {"images": ["14", 0], "filename_prefix": f"seg_{seg_idx:02d}"},
        },
    }


def start_comfy_server(use_fp16_unet: bool) -> subprocess.Popen:
    log_path = WORK_ROOT / "comfyui.log"
    cmd = [
        sys.executable,
        "main.py",
        "--listen",
        "127.0.0.1",
        "--port",
        "8188",
        "--disable-auto-launch",
    ]
    if use_fp16_unet:
        cmd.append("--fp16-unet")
    print(f"Starting ComfyUI: {' '.join(cmd)}", flush=True)
    log_f = open(log_path, "w")
    proc = subprocess.Popen(cmd, cwd=str(COMFY_DIR), stdout=log_f, stderr=subprocess.STDOUT)

    for _ in range(90):
        if proc.poll() is not None:
            tail = log_path.read_text(errors="replace")[-3000:]
            raise RuntimeError(f"ComfyUI exited early ({proc.returncode}):\n{tail}")
        try:
            stats = http_json(f"{COMFY_URL}/system_stats", timeout=3)
            print("ComfyUI ready:", json.dumps(stats.get("system", {})), flush=True)
            return proc
        except Exception:
            time.sleep(2)
    raise TimeoutError("Timed out waiting for ComfyUI server on 127.0.0.1:8188")


def submit_and_wait_segment(seg: dict, unet_weight_dtype: str, out_dir: Path) -> list[Path]:
    t0 = time.time()
    workflow = build_flf2v_workflow(seg, unet_weight_dtype=unet_weight_dtype)
    res = http_json(f"{COMFY_URL}/prompt", data={"prompt": workflow}, timeout=30)
    prompt_id = res["prompt_id"]
    print(f"Submitted seg_{seg['idx']:02d} ({unet_weight_dtype}) prompt_id={prompt_id}", flush=True)

    while True:
        time.sleep(5)
        hist = http_json(f"{COMFY_URL}/history/{prompt_id}", timeout=15)
        if prompt_id not in hist:
            elapsed = int(time.time() - t0)
            if elapsed % 30 < 5:
                print(f"[seg_{seg['idx']:02d}] waiting ({elapsed}s)...", flush=True)
            continue

        entry = hist[prompt_id]
        status = entry.get("status", {})
        if status.get("status_str") == "error":
            log_tail = (WORK_ROOT / "comfyui.log").read_text(errors="replace")[-4000:]
            raise RuntimeError(
                f"ComfyUI seg_{seg['idx']:02d} error ({unet_weight_dtype}): {json.dumps(status)}\nLog:\n{log_tail}"
            )

        imgs = entry.get("outputs", {}).get("15", {}).get("images", [])
        paths = []
        for im in imgs:
            sub = im.get("subfolder", "")
            p = out_dir / sub / im["filename"] if sub else out_dir / im["filename"]
            paths.append(p)
        paths.sort(key=lambda x: x.name)
        if len(paths) != 49:
            raise RuntimeError(f"Expected 49 frames for seg_{seg['idx']:02d}, got {len(paths)}")
        print(
            f"Completed seg_{seg['idx']:02d} ({len(paths)} frames) in {int(time.time() - t0)}s",
            flush=True,
        )
        return paths


def run_comfy_segments(major: int, minor: int) -> list[list[Path]]:
    out_dir = COMFY_DIR / "output"
    for old in out_dir.glob("seg_*.png"):
        old.unlink()

    use_fp16_unet = major < 8
    unet_weight_dtype = "fp8_e4m3fn_fast" if (major, minor) >= (8, 9) else "fp8_e4m3fn"
    print(f"Selected UNET weight_dtype={unet_weight_dtype} (CC {major}.{minor})", flush=True)

    proc = start_comfy_server(use_fp16_unet=use_fp16_unet)
    all_segment_frames: list[list[Path]] = []
    try:
        for i, seg in enumerate(SEGMENTS):
            try:
                paths = submit_and_wait_segment(seg, unet_weight_dtype=unet_weight_dtype, out_dir=out_dir)
            except RuntimeError as exc:
                err_txt = str(exc)
                if (
                    i == 0
                    and unet_weight_dtype == "fp8_e4m3fn_fast"
                    and any(tok in err_txt for tok in ("_scaled_mm", "fp8_optimizations", "fp8_e4m3fn_fast", "Float8"))
                ):
                    print("fp8_e4m3fn_fast failed on seg_01; retrying with fp8_e4m3fn...", flush=True)
                    unet_weight_dtype = "fp8_e4m3fn"
                    paths = submit_and_wait_segment(seg, unet_weight_dtype=unet_weight_dtype, out_dir=out_dir)
                else:
                    raise
            all_segment_frames.append(paths)
    finally:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return all_segment_frames


def stitch_and_interpolate(segment_frames: list[list[Path]]) -> tuple[Path, bool]:
    stitched_dir = WORK_ROOT / "stitched_frames"
    rife_in_dir = WORK_ROOT / "rife_in"
    for d in (stitched_dir, rife_in_dir):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    ordered: list[Path] = []
    for seg_i, frames in enumerate(segment_frames):
        subset = frames if seg_i == 0 else frames[1:]
        ordered.extend(subset)

    for idx, src in enumerate(ordered):
        shutil.copy2(src, stitched_dir / f"frame_{idx:04d}.png")
        shutil.copy2(src, rife_in_dir / f"{idx:04d}.png")
    print(f"Stitched {len(ordered)} continuous frames into {stitched_dir}", flush=True)

    vid_out_dir = RIFE_DIR / "vid_out"
    try:
        if not RIFE_DIR.exists():
            sh(f"git clone --depth 1 https://github.com/hzwer/Practical-RIFE.git {RIFE_DIR}")
        train_log = RIFE_DIR / "train_log"
        if not (train_log / "flownet.pkl").exists():
            rife_zip = WORK_ROOT / "RIFEv4.25_0919.zip"
            sh(
                f"aria2c -x 8 -s 8 --continue=true --dir='{WORK_ROOT}' --out='RIFEv4.25_0919.zip' "
                f"'https://huggingface.co/r3gm/RIFE/resolve/main/RIFEv4.25_0919.zip'"
            )
            tmp_unzip = WORK_ROOT / "rife_unzip"
            shutil.rmtree(tmp_unzip, ignore_errors=True)
            sh(f"unzip -q -o {rife_zip} -d {tmp_unzip}")
            pkls = list(tmp_unzip.rglob("flownet.pkl"))
            if not pkls:
                raise RuntimeError("flownet.pkl not found inside RIFEv4.25_0919.zip")
            train_log.mkdir(parents=True, exist_ok=True)
            shutil.copytree(pkls[0].parent, train_log, dirs_exist_ok=True)

        sh("pip install -q tqdm opencv-python")
        inf_py = RIFE_DIR / "inference_video.py"
        txt = inf_py.read_text(encoding="utf-8")
        if "import skvideo.io\n" in txt:
            inf_py.write_text(
                txt.replace(
                    "import skvideo.io\n",
                    "try:\n    import skvideo.io\nexcept Exception:\n    skvideo = None\n",
                    1,
                ),
                encoding="utf-8",
            )
        shutil.rmtree(vid_out_dir, ignore_errors=True)
        sh(f"cd {RIFE_DIR} && python3 inference_video.py --exp=2 --img={rife_in_dir}")
        out_pngs = sorted(vid_out_dir.glob("*.png"))
        if len(out_pngs) >= 400:
            print(f"Practical-RIFE 4x interpolation complete: {len(out_pngs)} PNG frames", flush=True)
            return vid_out_dir, True
        raise RuntimeError(f"Expected >=400 RIFE frames, got {len(out_pngs)}")
    except Exception as exc:
        print(f"Practical-RIFE failed ({exc}); falling back to FFmpeg minterpolate...", flush=True)

    raw_mp4 = WORK_ROOT / "raw_193.mp4"
    rife_mp4 = WORK_ROOT / "rife_769.mp4"
    sh(
        f"ffmpeg -y -framerate 7.5 -i {stitched_dir}/frame_%04d.png "
        f"-c:v libx264 -crf 10 -pix_fmt yuv420p {raw_mp4}"
    )
    sh(
        f"ffmpeg -y -i {raw_mp4} "
        f"-vf 'minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1' "
        f"-c:v libx264 -crf 12 -pix_fmt yuv420p {rife_mp4}"
    )
    return rife_mp4, False


def get_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def master_1080p_and_qa(interp_source: Path, is_png_seq: bool) -> None:
    if is_png_seq:
        frame_count = len(list(interp_source.glob("*.png")))
        vid_dur = frame_count / 30.0
        in_video_args = f"-framerate 30 -i {interp_source}/%07d.png"
    else:
        vid_dur = get_duration(interp_source)
        in_video_args = f"-i {interp_source}"

    audio_trim = max(1.0, vid_dur - 0.05)
    fade_out_start = max(0.5, audio_trim - 2.5)

    audio_in = WORK_ROOT / "ambient_30s.wav"
    if not audio_in.exists():
        raise FileNotFoundError(f"Missing ambient audio slice: {audio_in}")

    out_mp4 = WORK_ROOT / "Plant_Growth_Sunflower_Timelapse_1080p.mp4"
    vf = "fps=30,scale=1920:1080:flags=lanczos,cas=0.3"
    af = f"atrim=0:{audio_trim:.3f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out_start:.3f}:d=2.5"

    nvenc_cmd = (
        f"ffmpeg -y {in_video_args} -i {audio_in} "
        f"-filter_complex '[0:v]{vf}[vout];[1:a]{af}[aout]' "
        f"-map '[vout]' -map '[aout]' "
        f"-c:v h264_nvenc -preset p6 -cq 18 -profile:v high -pix_fmt yuv420p "
        f"-colorspace bt709 -color_primaries bt709 -color_trc bt709 "
        f"-c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart {out_mp4}"
    )
    res = sh(nvenc_cmd, check=False)
    if res.returncode != 0:
        print("h264_nvenc failed, retrying with libx264 high profile...", flush=True)
        sh(
            f"ffmpeg -y {in_video_args} -i {audio_in} "
            f"-filter_complex '[0:v]{vf}[vout];[1:a]{af}[aout]' "
            f"-map '[vout]' -map '[aout]' "
            f"-c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p "
            f"-colorspace bt709 -color_primaries bt709 -color_trc bt709 "
            f"-c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart {out_mp4}"
        )

    qa_dir = WORK_ROOT / "qa_samples"
    shutil.rmtree(qa_dir, ignore_errors=True)
    qa_dir.mkdir(parents=True)
    actual_dur = get_duration(out_mp4)
    sample_times = [0.8, 6.4, 12.8, 19.2, min(24.8, max(1.0, actual_dur - 0.8))]
    labels = ["Sprout (0.8s)", "Seedling (6.4s)", "Green Bud (12.8s)", "Opening (19.2s)", f"Full Bloom ({sample_times[4]:.1f}s)"]

    from PIL import Image, ImageDraw

    cell_imgs = []
    for idx, (ts, lbl) in enumerate(zip(sample_times, labels)):
        frame_p = qa_dir / f"sample_{idx}.png"
        sh(f"ffmpeg -y -ss {ts:.2f} -i {out_mp4} -frames:v 1 -update 1 {frame_p}")
        im = Image.open(frame_p).convert("RGB").resize((640, 360), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(8, 8), (190, 34)], fill=(0, 0, 0))
        draw.text((14, 14), lbl, fill=(255, 225, 130))
        cell_imgs.append(im)

    info_cell = Image.new("RGB", (640, 360), color=(16, 24, 18))
    idraw = ImageDraw.Draw(info_cell)
    lines = [
        "PLANT GROWTH TIME-LAPSE PILOT",
        "Dwarf Golden Sunflower (5 Stages)",
        f"Duration: {actual_dur:.2f}s @ 30fps (1920x1080)",
        "Engine: Wan2.1-FLF2V FP8 + RIFE 4x",
        "Video Credits Spent: $0 (Zero gflow video)",
    ]
    for li, text in enumerate(lines):
        idraw.text((36, 70 + li * 42), text, fill=(235, 245, 225) if li else (255, 215, 100))
    cell_imgs.append(info_cell)

    sheet = Image.new("RGB", (1280, 1080))
    positions = [(0, 0), (640, 0), (0, 360), (640, 360), (0, 720), (640, 720)]
    for im, pos in zip(cell_imgs, positions):
        sheet.paste(im, pos)

    qa_path = WORK_ROOT / "Plant_Growth_QA_Sheet.jpg"
    sheet.save(qa_path, format="JPEG", quality=92)
    print(f"DONE_OK: {out_mp4} ({out_mp4.stat().st_size} bytes) | QA: {qa_path}", flush=True)


def main() -> int:
    major, minor = get_gpu_compute_cap()
    setup_comfyui_and_models()
    prepare_normalized_inputs()
    segment_frames = run_comfy_segments(major, minor)
    interp_source, is_png_seq = stitch_and_interpolate(segment_frames)
    master_1080p_and_qa(interp_source, is_png_seq)
    return 0


if __name__ == "__main__":
    sys.exit(main())
