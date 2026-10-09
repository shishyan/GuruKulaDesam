# -*- coding: utf-8 -*-
"""
Appends Step 5 (Open-Source Video Continuation) to c:\GitHub\Guru-Kula-Desam.ipynb.
"""

import json
from pathlib import Path

nb_path = Path(r"c:\GitHub\Guru-Kula-Desam.ipynb")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

md_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🎬 Step 5: Hybrid Video Extender (Open-Model Video Continuation)\n",
        "### Extends Google Flow (Veo) Videos Using Colab GPU for Free\n",
        "Takes the base Veo clips, extracts the final frame, and generates 5 seconds of continuous cinematic camera motion using open-source Image-to-Video models. Stitches the two halves into a seamless, high-framerate extended scene."
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "#@title Run Hybrid Video Extender (Open Model GPU Continuation)\n",
        "import os, sys, glob, subprocess\n",
        "from pathlib import Path\n",
        "!pip install -q opencv-python imageio imageio-ffmpeg diffusers\n",
        "\n",
        "import cv2\n",
        "import torch\n",
        "from PIL import Image\n",
        "from diffusers import StableVideoDiffusionPipeline\n",
        "\n",
        "device = \"cuda\" if torch.cuda.is_available() else \"cpu\"\n",
        "print(f\"🚀 Initializing SOTA Video Extension Engine on {device}...\")\n",
        "\n",
        "# Load Stable Video Diffusion XT (1.1) for photorealistic motion continuation\n",
        "pipe = StableVideoDiffusionPipeline.from_pretrained(\n",
        "    \"stabilityai/stable-video-diffusion-img2vid-xt-1-1\",\n",
        "    torch_dtype=torch.float16 if device == \"cuda\" else torch.float32,\n",
        "    variant=\"fp16\" if device == \"cuda\" else None\n",
        ").to(device)\n",
        "\n",
        "VEO_INPUT_DIR = Path(\"/content/drive/MyDrive/GuruKulaDesam/veo_raw\")\n",
        "EXTENDED_OUTPUT_DIR = Path(\"/content/drive/MyDrive/GuruKulaDesam/extended_scenes\")\n",
        "VEO_INPUT_DIR.mkdir(parents=True, exist_ok=True)\n",
        "EXTENDED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)\n",
        "\n",
        "def extract_last_frame(video_path: Path) -> Image.Image:\n",
        "    cap = cv2.VideoCapture(str(video_path))\n",
        "    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))\n",
        "    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, total_frames - 2))\n",
        "    ret, frame = cap.read()\n",
        "    cap.release()\n",
        "    if not ret:\n",
        "        raise RuntimeError(f\"Failed to read frame from {video_path}\")\n",
        "    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)\n",
        "    return Image.fromarray(frame_rgb)\n",
        "\n",
        "# Process all Veo clips placed in Drive\n",
        "clips = sorted(VEO_INPUT_DIR.glob(\"*.mp4\"))\n",
        "if not clips:\n",
        "    print(f\"ℹ️ Place your raw base Veo clips into: {VEO_INPUT_DIR}\")\n",
        "    print(\"Once uploaded, re-run this cell to extend them automatically!\")\n",
        "else:\n",
        "    print(f\"Found {len(clips)} base Veo clips to extend...\")\n",
        "    for clip in clips:\n",
        "        out_clip = EXTENDED_OUTPUT_DIR / f\"{clip.stem}_extended.mp4\"\n",
        "        if out_clip.exists():\n",
        "            print(f\"✅ Already extended: {out_clip.name}\")\n",
        "            continue\n",
        "        \n",
        "        print(f\"🎞️ Extending: {clip.name}...\")\n",
        "        last_frame = extract_last_frame(clip)\n",
        "        last_frame_resized = last_frame.resize((1024, 576))\n",
        "        \n",
        "        # Generate continuation frames from last frame\n",
        "        generator = torch.manual_seed(42)\n",
        "        frames = pipe(\n",
        "            last_frame_resized,\n",
        "            decode_chunk_size=8,\n",
        "            generator=generator,\n",
        "            motion_bucket_id=127,\n",
        "            fps=7\n",
        "        ).frames[0]\n",
        "        \n",
        "        # Save continuation part\n",
        "        temp_ext = Path(\"/content/temp_ext.mp4\")\n",
        "        from diffusers.utils import export_to_video\n",
        "        export_to_video(frames, str(temp_ext), fps=24)\n",
        "        \n",
        "        # Concat original Veo clip + continuation\n",
        "        concat_txt = Path(\"/content/concat.txt\")\n",
        "        concat_txt.write_text(f\"file '{clip.resolve()}'\\nfile '{temp_ext.resolve()}'\\n\")\n",
        "        \n",
        "        subprocess.run([\n",
        "            \"ffmpeg\", \"-y\",\n",
        "            \"-f\", \"concat\", \"-safe\", \"0\",\n",
        "            \"-i\", str(concat_txt),\n",
        "            \"-c:v\", \"libx264\", \"-preset\", \"fast\", \"-crf\", \"18\",\n",
        "            str(out_clip)\n",
        "        ], check=True, capture_output=True)\n",
        "        \n",
        "        print(f\"   🎉 Saved extended continuous scene: {out_clip.name}\")\n",
        "\n",
        "print(\"\\n🚀 Video Extension processing completed!\")\n"
    ]
}

nb["cells"].append(md_cell)
nb["cells"].append(code_cell)

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"Successfully added Hybrid Video Extender cells to {nb_path}!")
