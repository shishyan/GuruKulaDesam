import json
from pathlib import Path

p = Path(r"c:\GitHub\Guru-Kula-Desam.ipynb")
with open(p, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Ensure metadata defaults to A100 GPU
nb["metadata"]["accelerator"] = "GPU"
if "colab" not in nb["metadata"]:
    nb["metadata"]["colab"] = {}
nb["metadata"]["colab"]["gpuType"] = "A100"

# Retain cells 0 to 4 (Thumbnails)
base_cells = nb["cells"][:5]

# Step 5: CogVideoX-5B Generative Continuation
cogvideox_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🎬 Step 5: Generative Video Continuation (CogVideoX-5B — A100 GPU)\n",
        "### 100% Open-Source & Ungated (Apache 2.0 — No HuggingFace Token Needed)\n",
        "Takes the final frame of your Google Veo clip and generates 6 seconds of brand new continuous action using **THUDM/CogVideoX-5b-I2V**. Stitches the original clip and continuation into a seamless extended scene at 1080p."
    ]
}

cogvideox_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\n" for line in """#@title 🚀 Run CogVideoX-5B Generative Video Extender
import os, sys, glob, subprocess
from pathlib import Path

# Mount Drive
if not Path("/content/drive/MyDrive").exists():
    from google.colab import drive
    drive.mount("/content/drive")

# Install diffusion and transformer libraries
!pip install -q diffusers transformers accelerate sentencepiece imageio-ffmpeg opencv-python

import cv2
import torch
from PIL import Image
from diffusers import CogVideoXImageToVideoPipeline
from diffusers.utils import export_to_video

device = "cuda" if torch.cuda.is_available() else "cpu"
gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3) if torch.cuda.is_available() else 0

print(f"🚀 Initializing CogVideoX-5B Extension Studio on {gpu_name} ({vram_gb:.1f} GB VRAM)...")
assert torch.cuda.is_available(), "GPU required! Please connect to an A100 GPU runtime."

# Load CogVideoX-5B Image-to-Video (100% UNGATED Apache 2.0 model)
pipe = CogVideoXImageToVideoPipeline.from_pretrained(
    "THUDM/CogVideoX-5b-I2V",
    torch_dtype=torch.bfloat16
).to(device)

if vram_gb < 35:
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
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

clips = sorted(VEO_INPUT_DIR.glob("*.mp4"))
if not clips:
    print(f"ℹ️ Place base Veo clips into: {VEO_INPUT_DIR}")
    print("Then re-run this cell to generate 6-second extensions for each clip!")
else:
    print(f"Found {len(clips)} base clips to extend...")
    for i, clip in enumerate(clips, 1):
        out_clip = EXTENDED_OUTPUT_DIR / f"{clip.stem}_extended.mp4"
        if out_clip.exists():
            print(f"[{i}/{len(clips)}] ✅ Already extended: {out_clip.name}")
            continue
        
        print(f"[{i}/{len(clips)}] 🎞️ Generating continuous motion for: {clip.name}...")
        last_frame = extract_last_frame(clip)
        last_frame_resized = last_frame.resize((720, 480))
        
        prompt = "Continuous smooth cinematic camera motion, glowing divine temple lamps, sacred spiritual atmosphere, high detail 24fps"
        
        generator = torch.Generator(device=device).manual_seed(42)
        video_frames = pipe(
            prompt=prompt,
            image=last_frame_resized,
            num_videos_per_prompt=1,
            num_inference_steps=50,
            guidance_scale=6.0,
            generator=generator
        ).frames[0]
        
        temp_ext_raw = Path("/content/temp_ext_raw.mp4")
        temp_ext_1080p = Path("/content/temp_ext_1080p.mp4")
        export_to_video(video_frames, str(temp_ext_raw), fps=8)
        
        # Lanczos upscale continuation part to 1080p Full HD
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(temp_ext_raw),
            "-vf", "scale=1920:1080:flags=lanczos,setpts=0.333*PTS",
            "-r", "24",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(temp_ext_1080p)
        ], check=True, capture_output=True)
        
        # Concat original Veo clip + continuation
        concat_txt = Path("/content/concat.txt")
        concat_txt.write_text(f"file '{clip.resolve()}'\\nfile '{temp_ext_1080p.resolve()}'\\n")
        
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(out_clip)
        ], check=True, capture_output=True)
        
        print(f"   🎉 Saved extended continuous scene: {out_clip.name}")

print("\\n🚀 CogVideoX-5B Video Continuation completed!")""".split("\n")]
}

# Step 6: RIFE Temporal Motion Extension Studio
rife_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# ⏳ Step 6: Temporal Motion Extension (RIFE 2× / 4× Duration Expansion)\n",
        "### Ultra-Smooth 60fps Slow-Motion Extension with Zero Hallucination or Morphing\n",
        "Uses Real-Time Intermediate Flow Estimation (RIFE) to double or quadruple the duration of your clips (5s $\\rightarrow$ 10s or 20s). Mathematically interpolates motion vectors for pristine, authentic devotional realism."
    ]
}

rife_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\n" for line in """#@title ⏳ Run RIFE Temporal Motion Extender (2x / 4x Duration)
import os, sys, glob, subprocess
from pathlib import Path

# Mount Drive
if not Path("/content/drive/MyDrive").exists():
    from google.colab import drive
    drive.mount("/content/drive")

# Install RIFE dependencies
if not Path("/content/Practical-RIFE").exists():
    print("📦 Setting up RIFE Motion Interpolation Engine...")
    !git clone https://github.com/hzwer/Practical-RIFE.git /content/Practical-RIFE
    !gdown --id 1wsQIrtL39wEevEsMWgfymeBWAmDlg0Wu -O /content/Practical-RIFE/train_log.zip
    !unzip -q /content/Practical-RIFE/train_log.zip -d /content/Practical-RIFE/
    !pip install -q sk-video moviepy

VEO_INPUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/veo_raw")
RIFE_OUTPUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/extended_rife")
VEO_INPUT_DIR.mkdir(parents=True, exist_ok=True)
RIFE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Select slow-motion multiplier: 2x (double duration) or 4x (quadruple duration)
EXP_MULTIPLIER = 2 #@param [2, 4] {type:"integer"}

clips = sorted(VEO_INPUT_DIR.glob("*.mp4"))
if not clips:
    print(f"ℹ️ Place base Veo clips into: {VEO_INPUT_DIR}")
    print("Then re-run this cell to extend their duration 2x or 4x smoothly!")
else:
    print(f"Found {len(clips)} clips to expand {EXP_MULTIPLIER}x with RIFE...")
    %cd /content/Practical-RIFE
    for i, clip in enumerate(clips, 1):
        out_clip = RIFE_OUTPUT_DIR / f"{clip.stem}_{EXP_MULTIPLIER}x_smooth.mp4"
        if out_clip.exists():
            print(f"[{i}/{len(clips)}] ✅ Already extended: {out_clip.name}")
            continue
        
        print(f"[{i}/{len(clips)}] ⏳ Expanding motion {EXP_MULTIPLIER}x: {clip.name}...")
        cmd = [
            "python", "inference_video.py",
            "--video", str(clip),
            "--output", str(out_clip),
            "--exp", str(EXP_MULTIPLIER)
        ]
        subprocess.run(cmd, check=True)
        print(f"   🎉 Saved {EXP_MULTIPLIER}x extended clip: {out_clip.name}")
    %cd /content

print("\\n⏳ RIFE Motion Extension completed!")""".split("\n")]
}

# Step 7: Real-ESRGAN 4K Super-Resolution Upscaler
realesrgan_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 💎 Step 7: 4K Devotional Video Super-Resolution (Real-ESRGAN)\n",
        "### Ultra-HD 4K / 1080p Enhancement for Master Films & Extended Scenes\n",
        "Deep convolutional super-resolution via RealESRGAN_x4plus to sharpen temple carvings, facial features, eyes, jewelry, and textures to pristine 4K Ultra HD."
    ]
}

realesrgan_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + "\n" for line in """#@title 💎 Run Real-ESRGAN 4K Super-Resolution Upscaler
import os, sys, glob, subprocess
from pathlib import Path

# Mount Drive
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

TARGET_RES = "4K" #@param ["1080p", "4K"]
MODEL = "RealESRGAN_x4plus"

videos = sorted(INPUT_DIR.glob("*.mp4"))
if not videos:
    print(f"ℹ️ Place videos to upscale into: {INPUT_DIR}")
    print("Then re-run this cell to upscale them to true 4K!")
else:
    print(f"Found {len(videos)} videos to upscale to {TARGET_RES}...")
    outscale = 4 if TARGET_RES == "4K" else 2
    for i, vid in enumerate(videos, 1):
        out_vid = OUTPUT_DIR / f"{vid.stem}_4k.mp4"
        if out_vid.exists():
            print(f"[{i}/{len(videos)}] ✅ Already upscaled: {out_vid.name}")
            continue
        
        print(f"[{i}/{len(videos)}] 🎬 Upscaling {vid.name} to {TARGET_RES} on {gpu_name}...")
        cmd = [
            "python", "/content/Real-ESRGAN/inference_realesrgan_video.py",
            "-n", MODEL,
            "-i", str(vid),
            "-o", str(OUTPUT_DIR),
            "--outscale", str(outscale)
        ]
        subprocess.run(cmd, check=True)
        print(f"   🎉 Finished: {vid.stem}_out.mp4 saved to {OUTPUT_DIR}")

print("\\n💎 All 4K video upscaling completed!")""".split("\n")]
}

# Assemble full notebook
nb["cells"] = base_cells + [
    cogvideox_md, cogvideox_code,
    rife_md, rife_code,
    realesrgan_md, realesrgan_code
]

with open(p, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Guru-Kula-Desam.ipynb successfully updated with CogVideoX-5B, RIFE, and Real-ESRGAN!")
