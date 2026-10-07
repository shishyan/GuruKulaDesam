# -*- coding: utf-8 -*-
"""
Builds Colab Notebook for Batch 2 (Chapters 5, 8, 16, 25, 30, 31)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from production.generate_batch2_prompts import ALL_CHAPTERS

tasks = []
for ch_num, ch_data in sorted(ALL_CHAPTERS.items()):
    for path, title, prompt in ch_data['prompts']:
        tasks.append({
            'filename': f'production/visuals/thirukkural/{path}',
            'title': title,
            'prompt': prompt
        })

print(f"Total tasks constructed: {len(tasks)}")

intro_md = (
    "# 🎬 குரு குல தேசம் — Thirukkural Master Film Visual Suite Generator (Batch 2)\n"
    "### Dedicated GPU Studio for A100 / T4 GPU\n\n"
    "This notebook generates the **269 verse-specific cinematic artworks** for Batch 2:\n"
    "- **Chapter 5 (*இல்வாழ்க்கை - Ilvaazhkkai*)**: 42 shots (Kurals 41–50)\n"
    "- **Chapter 8 (*அன்புடைமை - Anbudaimai*)**: 35 shots (Kurals 71–80)\n"
    "- **Chapter 16 (*பொறையுடைமை - Poraiyudaimai*)**: 62 shots (Kurals 151–160)\n"
    "- **Chapter 25 (*அருளுடைமை - Aruludaimai*)**: 37 shots (Kurals 241–250)\n"
    "- **Chapter 30 (*வாய்மை - Vaaimai*)**: 41 shots (Kurals 291–300)\n"
    "- **Chapter 31 (*வெகுளாமை - Vegulaamai*)**: 52 shots (Kurals 301–310)\n\n"
    "### Engine: **SDXL-Lightning (ByteDance / Stability AI)**\n"
    "- ⚡ **Zero-Auth Instant Start**: No Hugging Face tokens or gated permissions required.\n"
    "- ⚡ **Blazing Fast**: 4-step distilled diffusion (~1.2s per image on T4, ~0.4s on A100).\n"
    "- ⚡ **16:9 Widescreen**: Native 1280x720 cinematic framing.\n"
    "- ⚡ **Automatic Packaging**: Zips all 269 artworks into `gurukuladesam_film_artworks_batch2.zip` and triggers browser download.\n\n"
    "👉 **To run**: Click **Runtime → Run all** (or press `Ctrl + F9`)."
)

step1_code = (
    "# Step 1: Install high-performance libraries\n"
    "!pip install -q diffusers transformers accelerate safetensors sentencepiece protobuf torch torchvision\n\n"
    "import torch\n"
    "print('PyTorch Version:', torch.__version__)\n"
    "if torch.cuda.is_available():\n"
    "    device_name = torch.cuda.get_device_name(0)\n"
    "    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9\n"
    "    print(f'✅ GPU Detected: {device_name} ({vram_gb:.2f} GB VRAM)')\n"
    "else:\n"
    "    print('⚠️ WARNING: No GPU detected! Please go to Runtime -> Change runtime type -> Select A100 or T4 GPU.')\n"
)

step2_code = (
    "# Step 2: Initialize SDXL-Lightning 4-step Pipeline (Zero-Auth, High-Speed)\n"
    "import torch\n"
    "from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler\n"
    "from huggingface_hub import hf_hub_download\n"
    "from safetensors.torch import load_file\n\n"
    "print('⏳ Loading SDXL-Lightning 4-step Pipeline in float16...')\n"
    "base = 'stabilityai/stable-diffusion-xl-base-1.0'\n"
    "repo = 'ByteDance/SDXL-Lightning'\n"
    "ckpt = 'sdxl_lightning_4step_unet.safetensors'\n\n"
    "unet = UNet2DConditionModel.from_config(base, subfolder='unet').to('cuda', torch.float16)\n"
    "unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device='cuda'))\n"
    "pipe = StableDiffusionXLPipeline.from_pretrained(\n"
    "    base,\n"
    "    unet=unet,\n"
    "    torch_dtype=torch.float16,\n"
    "    variant='fp16'\n"
    ").to('cuda')\n"
    "pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing='trailing')\n"
    "print('✅ SDXL-Lightning ready on GPU!')\n"
)

tasks_json = json.dumps(tasks, indent=4, ensure_ascii=False)

step3_code = (
    "# Step 3: Generate All 269 Master Film Visuals\n"
    "import os, time\n"
    "from PIL import Image\n\n"
    f"tasks = {tasks_json}\n\n"
    "print(f'🚀 Starting generation of {len(tasks)} cinematic master film visuals...')\n"
    "start_time = time.time()\n\n"
    "for i, task in enumerate(tasks, 1):\n"
    "    out_path = task['filename']\n"
    "    os.makedirs(os.path.dirname(out_path), exist_ok=True)\n"
    "    \n"
    "    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:\n"
    "        print(f'[{i}/{len(tasks)}] ⏩ Skipping (already exists): {out_path}')\n"
    "        continue\n"
    "        \n"
    "    print(f'[{i}/{len(tasks)}] 🎨 Generating: {task[\"title\"]}')\n"
    "    t0 = time.time()\n"
    "    \n"
    "    with torch.inference_mode():\n"
    "        image = pipe(\n"
    "            prompt=task['prompt'],\n"
    "            negative_prompt='text, watermark, logo, cartoon, anime, blurry, low quality, modern clothes, wrist watch, glasses, plastic, distorted anatomy, extra limbs',\n"
    "            num_inference_steps=4,\n"
    "            guidance_scale=0.0,\n"
    "            width=1280,\n"
    "            height=720\n"
    "        ).images[0]\n\n"
    "    image.save(out_path, 'JPEG', quality=95)\n"
    "    elapsed = time.time() - t0\n"
    "    print(f'  ✅ Saved ({elapsed:.2f}s): {out_path}')\n\n"
    "total_elapsed = time.time() - start_time\n"
    "print(f'\\n🎉 All {len(tasks)} master film artworks generated successfully in {total_elapsed/60:.2f} minutes!')\n"
)

step4_code = (
    "# Step 4: Package Master Artworks and Trigger Automatic Download\n"
    "import os, zipfile\n"
    "from google.colab import files\n\n"
    "zip_filename = 'gurukuladesam_film_artworks_batch2.zip'\n"
    "print(f'📦 Packaging production visuals into {zip_filename}...')\n\n"
    "with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:\n"
    "    for root, dirs, filenames in os.walk('production/visuals/thirukkural'):\n"
    "        for fn in filenames:\n"
    "            if fn.endswith(('.jpg', '.png')):\n"
    "                full_path = os.path.join(root, fn)\n"
    "                arcname = os.path.relpath(full_path, '.')\n"
    "                zipf.write(full_path, arcname)\n\n"
    "size_mb = os.path.getsize(zip_filename) / (1024 * 1024)\n"
    "print(f'✅ Archive created: {zip_filename} ({size_mb:.2f} MB)')\n"
    "print('⬇ Triggering automatic browser download...')\n"
    "files.download(zip_filename)\n"
)

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {"id": "view-in-github", "colab_type": "text"},
            "source": [
                '<a href="https://colab.research.google.com/github/shishyan/GuruKulaDesam/blob/main/colab_generate_master_films_batch2.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>'
            ]
        },
        {"cell_type": "markdown", "metadata": {"id": "intro_md"}, "source": [intro_md]},
        {"cell_type": "code", "execution_count": None, "metadata": {"id": "step1_install"}, "outputs": [], "source": [step1_code]},
        {"cell_type": "code", "execution_count": None, "metadata": {"id": "step2_pipeline"}, "outputs": [], "source": [step2_code]},
        {"cell_type": "code", "execution_count": None, "metadata": {"id": "step3_generate"}, "outputs": [], "source": [step3_code]},
        {"cell_type": "code", "execution_count": None, "metadata": {"id": "step4_zip"}, "outputs": [], "source": [step4_code]},
    ],
    "metadata": {
        "colab": {"provenance": [], "toc_visible": True, "gpuType": "T4", "include_colab_link": True},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
        "accelerator": "GPU"
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open('colab_generate_master_films_batch2.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

with open('colab_generate_master_films_a100.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("Generated both colab_generate_master_films_batch2.ipynb and colab_generate_master_films_a100.ipynb successfully!")
