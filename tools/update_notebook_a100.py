import json
from pathlib import Path

p = Path(r"c:\GitHub\Guru-Kula-Desam.ipynb")
with open(p, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Set A100 GPU in metadata
nb["metadata"]["accelerator"] = "GPU"
if "colab" not in nb["metadata"]:
    nb["metadata"]["colab"] = {}
nb["metadata"]["colab"]["gpuType"] = "A100"

cell_code = """#@title Run Hybrid Video Extender (A100 / High-VRAM GPU Continuation)
import os, sys, glob, subprocess
from pathlib import Path
!pip install -q opencv-python imageio imageio-ffmpeg diffusers transformers accelerate

import cv2
import torch
from PIL import Image
from diffusers import StableVideoDiffusionPipeline

device = "cuda" if torch.cuda.is_available() else "cpu"
gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3) if torch.cuda.is_available() else 0

print(f"🚀 Initializing Video Extension Engine on {gpu_name} ({vram_gb:.1f} GB VRAM)...")

# Load SOTA video diffusion pipeline with fp16/bf16 precision
dtype = torch.bfloat16 if ("A100" in gpu_name or "H100" in gpu_name) else torch.float16
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt-1-1",
    torch_dtype=dtype if device == "cuda" else torch.float32,
    variant="fp16" if device == "cuda" else None
).to(device)

if vram_gb >= 30:
    print("⚡ High-VRAM Mode (A100/H100) Active: Full batch decoding enabled without CPU offload.")
else:
    pipe.enable_model_cpu_offload()

VEO_INPUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/veo_raw")
EXTENDED_OUTPUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/extended_scenes")
VEO_INPUT_DIR.mkdir(parents=True, exist_ok=True)
EXTENDED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_last_frame(video_path: Path) -> Image.Image:
    cap = cv2.VideoCapture(str(video_path))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, total_frames - 2))
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError(f"Failed to read frame from {video_path}")
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame_rgb)

clips = sorted(VEO_INPUT_DIR.glob("*.mp4"))
if not clips:
    print(f"ℹ️ Place your raw base Veo clips into: {VEO_INPUT_DIR}")
    print("Once uploaded, re-run this cell to extend them automatically!")
else:
    print(f"Found {len(clips)} base Veo clips to extend...")
    for i, clip in enumerate(clips, 1):
        out_clip = EXTENDED_OUTPUT_DIR / f"{clip.stem}_extended.mp4"
        if out_clip.exists():
            print(f"[{i}/{len(clips)}] ✅ Already extended: {out_clip.name}")
            continue
        
        print(f"[{i}/{len(clips)}] 🎞️ Extending: {clip.name} on {gpu_name}...")
        last_frame = extract_last_frame(clip)
        last_frame_resized = last_frame.resize((1024, 576), Image.Resampling.LANCZOS)
        
        generator = torch.manual_seed(42)
        frames = pipe(
            last_frame_resized,
            decode_chunk_size=14 if vram_gb >= 30 else 8,
            generator=generator,
            motion_bucket_id=127,
            fps=7
        ).frames[0]
        
        temp_ext_raw = Path("/content/temp_ext_raw.mp4")
        temp_ext_1080p = Path("/content/temp_ext_1080p.mp4")
        from diffusers.utils import export_to_video
        export_to_video(frames, str(temp_ext_raw), fps=24)
        
        # High quality Lanczos upscale continuation part to 1080p
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(temp_ext_raw),
            "-vf", "scale=1920:1080:flags=lanczos",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(temp_ext_1080p)
        ], check=True, capture_output=True)
        
        # Concat original Veo clip + 1080p continuation
        concat_txt = Path("/content/concat.txt")
        concat_txt.write_text(f"file '{clip.resolve()}'\\nfile '{temp_ext_1080p.resolve()}'\\n")
        
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(out_clip)
        ], check=True, capture_output=True)
        
        print(f"   🎉 Saved 1080p extended scene: {out_clip.name}")

print("\\n🚀 Video Extension processing completed!")
"""

nb["cells"][6]["source"] = [line + "\n" for line in cell_code.split("\n")]

with open(p, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Guru-Kula-Desam.ipynb successfully upgraded for A100 GPU!")

