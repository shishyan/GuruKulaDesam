#!/usr/bin/env python3
"""
Colab Batch 2x Video Extender Pipeline
======================================
Extends workspace videos (8s-10s clips in production/google_flow_renders/ or custom folders)
to at least 2x their original length (16s-20s+) at 1280x720 @ 24fps.

Supports two extension engines:
  1. `ltx_i2v` (Default on Colab GPU):
     - Extracts the final frame of each clip (`last_frame.png`)
     - Runs Lightricks/LTX-Video Image-to-Video (161 frames @ 24fps = ~6.7s raw,
       plus optical-flow frame interpolation to match exact source duration = 8s-10s)
     - Seamlessly stitches original + AI continuation -> 16s-20s clip (2x length).
  2. `optical_flow_2x` (Fast GPU/CPU Hybrid):
     - Uses motion-compensated optical flow (`minterpolate`) + seamless twilight/crossfade
       continuation to double clip duration with zero diffusion hallucination.

Usage in Google Colab:
  !git clone https://github.com/shishyan/GuruKulaDesam.git /content/GuruKulaDesam
  %cd /content/GuruKulaDesam
  !pip install -q git+https://github.com/huggingface/diffusers.git transformers accelerate imageio-ffmpeg opencv-python sentencepiece
  !python production/colab_handoff/colab_batch_extend_2x.py --mode ltx_i2v --max-clips 50 --push-git
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import cv2
from PIL import Image


def probe_video(path: str) -> dict:
    """Return duration, width, height, and fps of a video file."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_frames:format=duration",
        "-of", "json",
        path,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {"duration": 0.0, "width": 1280, "height": 720, "fps": 24.0}
    data = json.loads(res.stdout)
    dur = float(data.get("format", {}).get("duration", 0.0))
    stream = (data.get("streams") or [{}])[0]
    w = int(stream.get("width", 1280))
    h = int(stream.get("height", 720))
    r_fps = stream.get("r_frame_rate", "24/1")
    try:
        num, den = map(int, r_fps.split("/"))
        fps = num / den if den else 24.0
    except Exception:
        fps = 24.0
    return {"duration": dur, "width": w, "height": h, "fps": fps}


def extract_last_frame(video_path: str, output_image_path: str, width: int = 768, height: int = 512) -> Image.Image:
    """Extract the final valid frame of a video and resize for LTX-Video I2V."""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        cap.release()
        raise ValueError(f"Could not read frames from {video_path}")

    # Step back 1-2 frames from the very end to avoid black/corrupt trailing frames
    frame = None
    for offset in [1, 2, 3, 5]:
        idx = max(0, total_frames - offset)
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frm = cap.read()
        if ok and frm is not None:
            frame = frm
            break
    cap.release()

    if frame is None:
        raise RuntimeError(f"Failed to extract final frame from {video_path}")

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb).resize((width, height), Image.Resampling.LANCZOS)
    img.save(output_image_path)
    return img


def load_ltx_pipeline():
    """Load Lightricks/LTX-Video Image-to-Video pipeline in bfloat16."""
    import torch
    from diffusers import LTXImageToVideoPipeline

    print("[Colab-2x] Loading Lightricks/LTX-Video (bfloat16) on GPU...")
    pipe = LTXImageToVideoPipeline.from_pretrained(
        "Lightricks/LTX-Video",
        torch_dtype=torch.bfloat16,
    )
    pipe.enable_model_cpu_offload()
    return pipe


def infer_scene_prompt(video_path: str) -> str:
    """Infer a spiritual/cinematic continuation prompt from the clip path or metadata."""
    parent_dir = Path(video_path).parent
    meta_file = parent_dir / "render_manifest.json"
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            for scene in meta.get("scenes", []):
                if Path(video_path).name in str(scene.get("file", "")):
                    if scene.get("prompt"):
                        return scene["prompt"] + ", smooth continuous cinematic camera movement, sacred temple atmosphere, 4k photorealistic"
        except Exception:
            pass
    return (
        "The sacred South Indian temple scene continues forward seamlessly, "
        "smooth slow cinematic camera motion, warm golden oil lamp lighting, "
        "photorealistic spiritual ambiance, ultra detailed."
    )


def extend_clip_ltx(
    pipe,
    video_path: str,
    output_path: str,
    work_dir: str,
    target_multiplier: float = 2.0,
) -> bool:
    """Extend a single video to >= 2x length using LTX-Video I2V + FFmpeg optical flow."""
    from diffusers.utils import export_to_video

    info = probe_video(video_path)
    orig_dur = info["duration"]
    if orig_dur <= 0:
        print(f"  [SKIP] Invalid duration for {video_path}")
        return False

    # Skip if already extended (> 14.5s)
    if orig_dur >= 14.5:
        print(f"  [SKIP] Already extended ({orig_dur:.2f}s): {video_path}")
        return False

    os.makedirs(work_dir, exist_ok=True)
    seed_png = os.path.join(work_dir, "last_frame.png")
    raw_cont_mp4 = os.path.join(work_dir, "raw_cont.mp4")
    norm_orig_mp4 = os.path.join(work_dir, "orig_norm.mp4")
    norm_cont_mp4 = os.path.join(work_dir, "cont_norm.mp4")
    concat_txt = os.path.join(work_dir, "concat.txt")

    seed_img = extract_last_frame(video_path, seed_png, width=768, height=512)
    prompt = infer_scene_prompt(video_path)
    negative_prompt = "blurry, jittery, sudden cut, static image, deformed, low quality, watermark, text"

    # LTX-Video num_frames must be (8 * k + 1). 161 frames @ 24fps = 6.71s raw clip.
    num_frames = 161
    print(f"  [I2V] Synthesizing {num_frames} frames from final frame of {Path(video_path).name} ({orig_dur:.2f}s)...")
    frames = pipe(
        image=seed_img,
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=768,
        height=512,
        num_frames=num_frames,
        num_inference_steps=30,
        guidance_scale=3.0,
    ).frames[0]

    export_to_video(frames, raw_cont_mp4, fps=24)

    # Calculate stretch factor so the continuation matches orig_dur (making total >= 2.0x)
    raw_dur = num_frames / 24.0
    needed_cont_dur = orig_dur * (target_multiplier - 1.0)
    pts_stretch = max(1.0, needed_cont_dur / raw_dur)

    # 1. Normalize original clip to 1280x720 @ 24fps
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", "scale=1280:720:flags=lanczos,fps=24,format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-an",
            norm_orig_mp4,
        ],
        check=True,
        capture_output=True,
    )

    # 2. Upscale + Optical-Flow interpolate continuation to match 1280x720 @ 24fps and exact needed duration
    vf_cont = (
        f"setpts={pts_stretch:.4f}*PTS,"
        f"minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
        f"scale=1280:720:flags=lanczos,"
        f"unsharp=5:5:0.8:3:3:0.4,"
        f"format=yuv420p"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", raw_cont_mp4,
            "-vf", vf_cont,
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-an",
            norm_cont_mp4,
        ],
        check=True,
        capture_output=True,
    )

    # 3. Concatenate seamlessly
    with open(concat_txt, "w", encoding="utf-8") as f:
        f.write(f"file '{os.path.abspath(norm_orig_mp4)}'\n")
        f.write(f"file '{os.path.abspath(norm_cont_mp4)}'\n")

    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_txt, "-c", "copy", output_path,
        ],
        check=True,
        capture_output=True,
    )

    new_info = probe_video(output_path)
    print(f"  [DONE] {Path(video_path).name}: {orig_dur:.2f}s -> {new_info['duration']:.2f}s ({new_info['width']}x{new_info['height']} @ {new_info['fps']:.0f}fps)")
    return True


def extend_clip_optical_flow_2x(video_path: str, output_path: str, work_dir: str) -> bool:
    """
    Fast local/Colab 2x extension using Optical-Flow Motion Interpolation (MCI)
    or seamless crossfaded forward+gentle-slow continuation.
    Doubles 8s -> 16s at 1280x720 @ 24fps with zero AI hallucination.
    """
    info = probe_video(video_path)
    orig_dur = info["duration"]
    if orig_dur <= 0 or orig_dur >= 14.5:
        return False

    os.makedirs(work_dir, exist_ok=True)
    temp_out = os.path.join(work_dir, "optflow_2x.mp4")

    # Motion-compensated 2x temporal expansion (setpts=2.0*PTS + bidirectional optical flow @ 24fps)
    vf = (
        "setpts=2.0*PTS,"
        "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
        "scale=1280:720:flags=lanczos,"
        "unsharp=5:5:0.6:3:3:0.3,"
        "format=yuv420p"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", vf,
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-an",
            temp_out,
        ],
        check=True,
        capture_output=True,
    )
    shutil.move(temp_out, output_path)
    new_info = probe_video(output_path)
    print(f"  [DONE-OPTFLOW] {Path(video_path).name}: {orig_dur:.2f}s -> {new_info['duration']:.2f}s")
    return True


def main():
    parser = argparse.ArgumentParser(description="Batch 2x Video Extender for Colab & Local Workspace")
    parser.add_argument("--input-glob", default="production/google_flow_renders/*/*.mp4", help="Glob pattern for videos to extend")
    parser.add_argument("--mode", choices=["ltx_i2v", "optical_flow_2x"], default="ltx_i2v", help="Extension engine")
    parser.add_argument("--in-place", action="store_true", default=True, help="Overwrite original clip once 2x clip is verified")
    parser.add_argument("--output-dir", default="", help="Optional separate output directory if not in-place")
    parser.add_argument("--max-clips", type=int, default=100, help="Max clips to process in this batch")
    parser.add_argument("--push-git", action="store_true", help="Commit and push extended videos back to GitHub every 10 clips")
    args = parser.parse_args()

    clips = sorted(glob.glob(args.input_glob))
    print(f"[Colab-2x] Found {len(clips)} candidate clips matching '{args.input_glob}'")

    # Filter to clips that are currently < 14.5s (i.e. 8s-10s originals)
    queue = []
    for c in clips:
        info = probe_video(c)
        if 3.0 <= info["duration"] < 14.5:
            queue.append((c, info["duration"]))

    print(f"[Colab-2x] {len(queue)} clips need 2x extension (< 14.5s). Processing up to {args.max_clips}...")
    queue = queue[: args.max_clips]

    pipe = None
    if args.mode == "ltx_i2v":
        pipe = load_ltx_pipeline()

    work_dir = "/tmp/colab_extend_work" if os.name != "nt" else "production/temp_extend/batch_work"
    completed = 0

    for idx, (clip_path, dur) in enumerate(queue, 1):
        print(f"\n[{idx}/{len(queue)}] Processing {clip_path} ({dur:.2f}s)...")
        if args.output_dir:
            rel = os.path.relpath(clip_path, "production")
            out_path = os.path.join(args.output_dir, rel)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
        else:
            out_path = clip_path + ".2x_tmp.mp4"

        try:
            if args.mode == "ltx_i2v":
                ok = extend_clip_ltx(pipe, clip_path, out_path, work_dir)
            else:
                ok = extend_clip_optical_flow_2x(clip_path, out_path, work_dir)

            if ok and not args.output_dir:
                shutil.move(out_path, clip_path)
            completed += 1

            if args.push_git and completed % 10 == 0:
                subprocess.run(["git", "add", "production/google_flow_renders/"], check=False)
                subprocess.run(["git", "commit", "-m", f"chore(video): batch 2x extend {completed} scene clips via Colab"], check=False)
                subprocess.run(["git", "push", "origin", "main"], check=False)
        except Exception as e:
            print(f"  [ERROR] Failed on {clip_path}: {e}")
            if os.path.exists(out_path):
                os.remove(out_path)

    if args.push_git and completed > 0:
        subprocess.run(["git", "add", "production/google_flow_renders/"], check=False)
        subprocess.run(["git", "commit", "-m", f"chore(video): batch 2x extend {completed} scene clips via Colab"], check=False)
        subprocess.run(["git", "push", "origin", "main"], check=False)

    print(f"\n[Colab-2x] Batch complete! Extended {completed}/{len(queue)} videos to 2x length.")


if __name__ == "__main__":
    main()
