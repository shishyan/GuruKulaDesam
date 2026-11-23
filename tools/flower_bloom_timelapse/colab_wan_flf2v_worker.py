#!/usr/bin/env python3
"""
Colab GPU worker for Zero-Credit 16:9 Lotus Blooming Time-Lapse Pilot:
  1. Installs ComfyUI + downloads Wan2.1-FLF2V-14B FP8 split weights from Comfy-Org.
  2. Runs 3 sequential WanFirstLastFrameToVideo passes (stage_01->02->03->04, 65 frames each).
  3. Stitches 193 continuous frames, runs 4x Practical-RIFE v4.25 interpolation (769 frames @ 30fps = ~25.6s).
  4. Upscales to 1920x1080 Rec.709 H.264 High Profile (h264_nvenc), muxes trimmed ambient audio,
     and builds a 2x2 Lotus_Bloom_QA_Sheet.jpg at 1280px width.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
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
            "Smooth botanical macro time-lapse of a closed green-and-rose lotus bud slowly awakening "
            "at golden dawn, outer sepals gently loosening and tip beginning to part, locked tripod "
            "camera, mirror-still pond water, photorealistic natural petal motion"
        ),
    },
    {
        "idx": 2,
        "start": "stage_02.png",
        "end": "stage_03.png",
        "prompt": (
            "Smooth botanical macro time-lapse of a pointed rose-pink lotus bud gracefully unfurling "
            "outward into a cupped half-open lotus blossom at golden dawn, velvety pink petals peeling "
            "open layer by layer, locked tripod camera, photorealistic"
        ),
    },
    {
        "idx": 3,
        "start": "stage_03.png",
        "end": "stage_04.png",
        "prompt": (
            "Smooth botanical macro time-lapse of a half-open pink lotus flower blossoming wide into "
            "majestic full bloom at golden dawn, outer and inner petals opening smoothly to reveal the "
            "glowing golden stamen crown, locked tripod camera, photorealistic"
        ),
    },
]

NEG_PROMPT = (
    "camera shake, sudden jump, morphing stem, text, watermark, blurry, deformed, low quality, "
    "flickering, static freeze, extra stems"
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
        ("stage_01.png", ["stage_01_tight_bud.png", "stage_01_tight_bud.jpg", "stage_01.png", "stage_01.jpg"]),
        ("stage_02.png", ["stage_02_cracking_bud.png", "stage_02_cracking_bud.jpg", "stage_02.png", "stage_02.jpg"]),
        ("stage_03.png", ["stage_03_half_open.png", "stage_03_half_open.jpg", "stage_03.png", "stage_03.jpg"]),
        ("stage_04.png", ["stage_04_full_bloom.png", "stage_04_full_bloom.jpg", "stage_04.png", "stage_04.jpg"]),
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


def build_flf2v_workflow(seg: dict) -> dict:
    seg_idx = seg["idx"]
    return {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors",
                "weight_dtype": "fp8_e4m3fn",
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
                "length": 65,
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
                "seed": 42 + seg_idx,
                "steps": 20,
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


def run_comfy_segments(use_fp16_unet: bool) -> list[list[Path]]:
    out_dir = COMFY_DIR / "output"
    for old in out_dir.glob("seg_*.png"):
        old.unlink()

    proc = start_comfy_server(use_fp16_unet=use_fp16_unet)
    all_segment_frames: list[list[Path]] = []
    try:
        for seg in SEGMENTS:
            t0 = time.time()
            workflow = build_flf2v_workflow(seg)
            res = http_json(f"{COMFY_URL}/prompt", data={"prompt": workflow}, timeout=30)
            prompt_id = res["prompt_id"]
            print(f"Submitted seg_{seg['idx']:02d} prompt_id={prompt_id}", flush=True)

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
                        f"ComfyUI seg_{seg['idx']:02d} error: {json.dumps(status)}\nLog:\n{log_tail}"
                    )

                imgs = entry.get("outputs", {}).get("15", {}).get("images", [])
                paths = []
                for im in imgs:
                    sub = im.get("subfolder", "")
                    p = out_dir / sub / im["filename"] if sub else out_dir / im["filename"]
                    paths.append(p)
                paths.sort(key=lambda x: x.name)
                if len(paths) != 65:
                    raise RuntimeError(f"Expected 65 frames for seg_{seg['idx']:02d}, got {len(paths)}")
                print(
                    f"Completed seg_{seg['idx']:02d} ({len(paths)} frames) in {int(time.time() - t0)}s",
                    flush=True,
                )
                all_segment_frames.append(paths)
                break
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
        # Guard unused skvideo.io import in --img mode so numpy 2.x never blocks RIFE
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

    out_mp4 = WORK_ROOT / "Lotus_Bloom_Timelapse_Pilot_1080p.mp4"
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
    sample_times = [1.0, min(9.0, actual_dur * 0.35), min(17.0, actual_dur * 0.68), max(1.0, actual_dur - 1.2)]
    cell_imgs = []
    from PIL import Image, ImageDraw

    for idx, ts in enumerate(sample_times):
        frame_p = qa_dir / f"sample_{idx}.png"
        sh(f"ffmpeg -y -ss {ts:.2f} -i {out_mp4} -frames:v 1 -q:v 2 {frame_p}")
        im = Image.open(frame_p).convert("RGB").resize((640, 360), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(8, 8), (92, 34)], fill=(0, 0, 0))
        draw.text((14, 14), f"t = {ts:.1f}s", fill=(255, 225, 130))
        cell_imgs.append(im)

    sheet = Image.new("RGB", (1280, 720))
    sheet.paste(cell_imgs[0], (0, 0))
    sheet.paste(cell_imgs[1], (640, 0))
    sheet.paste(cell_imgs[2], (0, 360))
    sheet.paste(cell_imgs[3], (640, 360))
    qa_path = WORK_ROOT / "Lotus_Bloom_QA_Sheet.jpg"
    sheet.save(qa_path, format="JPEG", quality=92)
    print(f"DONE_OK: {out_mp4} ({out_mp4.stat().st_size} bytes) | QA: {qa_path}", flush=True)


def main() -> int:
    major, _ = get_gpu_compute_cap()
    setup_comfyui_and_models()
    prepare_normalized_inputs()
    segment_frames = run_comfy_segments(use_fp16_unet=(major < 8))
    interp_source, is_png_seq = stitch_and_interpolate(segment_frames)
    master_1080p_and_qa(interp_source, is_png_seq)
    return 0


if __name__ == "__main__":
    sys.exit(main())
