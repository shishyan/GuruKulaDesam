import json
from pathlib import Path

p = Path(r"c:\GitHub\Guru-Kula-Desam.ipynb")
with open(p, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Update Step 5 markdown
nb["cells"][5]["source"] = [
    "# 💎 Step 5: 4K Devotional Video Super-Resolution & Upscaler (Real-ESRGAN)\n",
    "### Ultra-HD 4K / 1080p Enhancement for Google Flow & Veo Master Films\n",
    "Utilizes RealESRGAN_x4plus with CUDA acceleration to restore micro-textures, sharpen temple architecture, enhance facial features and jewelry, and upscale videos up to 4K without gated tokens or login restrictions.\n"
]

# Update Step 6 code cell
cell_code = '''#@title 🚀 Run 4K Video Upscaler Studio (Real-ESRGAN)
import os, sys, glob, subprocess
from pathlib import Path

# Mount Drive if not already mounted
if not Path("/content/drive/MyDrive").exists():
    from google.colab import drive
    drive.mount("/content/drive")

# Install Real-ESRGAN
if not Path("/content/Real-ESRGAN").exists():
    print("📦 Setting up Real-ESRGAN 4K Engine...")
    !git clone https://github.com/xinntao/Real-ESRGAN.git /content/Real-ESRGAN
    %cd /content/Real-ESRGAN
    !pip install -q basicsr facexlib gfpgan ffmpeg ffmpeg-python
    !pip install -q -r requirements.txt
    !python setup.py develop
    !pip install -q "numpy<2"
    %cd /content

import torch
gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
print(f"⚡ Super-Resolution Engine Active on: {gpu_name}")

INPUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/input_videos")
OUTPUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/upscaled_4k")
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Select target resolution: 1080p or 4K
TARGET_RES = "4K"  # Options: 1080p or 4K
MODEL = "RealESRGAN_x4plus"

videos = sorted(INPUT_DIR.glob("*.mp4"))
if not videos:
    print(f"ℹ️ Place video files to upscale in: {INPUT_DIR}")
    print("Then re-run this cell to upscale all videos to 4K!")
else:
    print(f"Found {len(videos)} videos to upscale to {TARGET_RES}...")
    for i, vid in enumerate(videos, 1):
        out_vid = OUTPUT_DIR / f"{vid.stem}_4k.mp4"
        if out_vid.exists():
            print(f"[{i}/{len(videos)}] ✅ Already upscaled: {out_vid.name}")
            continue
        
        print(f"[{i}/{len(videos)}] 🎬 Upscaling: {vid.name} to {TARGET_RES} on {gpu_name}...")
        outscale = 4 if TARGET_RES == "4K" else 2
        
        cmd = [
            "python", "/content/Real-ESRGAN/inference_realesrgan_video.py",
            "-n", MODEL,
            "-i", str(vid),
            "-o", str(OUTPUT_DIR),
            "--outscale", str(outscale)
        ]
        subprocess.run(cmd, check=True)
        print(f"   🎉 Finished: {vid.stem}_out.mp4 saved to {OUTPUT_DIR}")

print("\\n💎 All video upscaling completed!")
'''

nb["cells"][6]["source"] = [line + "\n" for line in cell_code.split("\n")]

with open(p, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Guru-Kula-Desam.ipynb successfully upgraded with Real-ESRGAN 4K Studio!")
