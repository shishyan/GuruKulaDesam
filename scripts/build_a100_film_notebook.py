# -*- coding: utf-8 -*-
"""
Builder for dedicated A100 Master Films Notebook:
colab_generate_master_films_a100.ipynb
"""

import json
from pathlib import Path
from build_full_colab import CH54_PROMPTS, CH57_PROMPTS, CH61_PROMPTS

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "colab_generate_master_films_a100.ipynb"

def build():
    total_images = len(CH54_PROMPTS) + len(CH57_PROMPTS) + len(CH61_PROMPTS)
    cells = []

    # Cell 0: Badge pointing to dedicated file
    cells.append({
        "cell_type": "markdown",
        "metadata": {"id": "view-in-github"},
        "source": [
            '<a href="https://colab.research.google.com/github/shishyan/GuruKulaDesam/blob/main/colab_generate_master_films_a100.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>\n'
        ]
    })

    # Cell 1: Intro Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {"id": "intro_md"},
        "source": [
            "# 🎬 குரு குல தேசம் — Thirukkural Master Film Visual Suite Generator\n",
            "### Dedicated GPU Studio for A100 GPU (40GB / 80GB VRAM)\n",
            "\n",
            "This notebook is solely dedicated to generating the **136 verse-specific cinematic artworks** for the master Thirukkural films:\n",
            "- **Chapter 54 (*பொச்சாவாமை - Pochchaavaamai*)**: 46 shots (Kurals 531–540)\n",
            "- **Chapter 57 (*வெருவந்த செய்யாமை - Veruvantha Seyyaamai*)**: 50 shots (Kurals 561–570)\n",
            "- **Chapter 61 (*மடியின்மை - Madiyinmai*)**: 40 shots (Kurals 601–610)\n",
            "\n",
            "### Engine: **FLUX.1-schnell** (Black Forest Labs) in native `bfloat16`\n",
            "- **SOTA Quality**: 12-billion parameter flow-matching transformer for photorealistic historical accuracy.\n",
            "- **Widescreen 16:9**: Native `1280x720` resolution.\n",
            "- **Blazing Fast**: ~1.5–2.5s per image on A100 (~5.5 minutes for all 136 shots).\n",
            "\n",
            "👉 **To run**: Click **Runtime → Run all** (or press `Ctrl + F9`)."
        ]
    })

    # Cell 2: Step 1: Install packages
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step1_install"},
        "outputs": [],
        "source": [
            "# Step 1: Install high-performance libraries\n",
            "!pip install -q diffusers transformers accelerate safetensors sentencepiece protobuf torch torchvision\n",
            "\n",
            "import torch\n",
            "print('PyTorch Version:', torch.__version__)\n",
            "if torch.cuda.is_available():\n",
            "    device_name = torch.cuda.get_device_name(0)\n",
            "    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9\n",
            "    print(f'✅ GPU Detected: {device_name} ({vram_gb:.2f} GB VRAM)')\n",
            "else:\n",
            "    print('⚠️ WARNING: No GPU detected! Please go to Runtime -> Change runtime type -> Select A100 or T4 GPU.')\n"
        ]
    })

    # Cell 3: Step 2: Initialize FLUX.1-schnell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step2_load_pipeline"},
        "outputs": [],
        "source": [
            "# Step 2: Initialize FLUX.1-schnell Pipeline\n",
            "ENGINE = 'FLUX-schnell'  # Default for A100; change to 'SDXL-Lightning' if desired\n",
            "\n",
            "import torch\n",
            "pipe = None\n",
            "\n",
            "if ENGINE == 'FLUX-schnell':\n",
            "    print('⏳ Loading FLUX.1-schnell (12B Flow Transformer in bfloat16)...')\n",
            "    from diffusers import FluxPipeline\n",
            "    pipe = FluxPipeline.from_pretrained(\n",
            "        'black-forest-labs/FLUX.1-schnell',\n",
            "        torch_dtype=torch.bfloat16\n",
            "    )\n",
            "    pipe.to('cuda')\n",
            "    print('✅ FLUX.1-schnell ready on A100 GPU!')\n",
            "else:\n",
            "    print('⏳ Loading SDXL-Lightning 4-step Pipeline...')\n",
            "    from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler\n",
            "    from huggingface_hub import hf_hub_download\n",
            "    from safetensors.torch import load_file\n",
            "\n",
            "    base = 'stabilityai/stable-diffusion-xl-base-1.0'\n",
            "    repo = 'ByteDance/SDXL-Lightning'\n",
            "    ckpt = 'sdxl_lightning_4step_unet.safetensors'\n",
            "    unet = UNet2DConditionModel.from_config(base, subfolder='unet').to('cuda', torch.float16)\n",
            "    unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device='cuda'))\n",
            "    pipe = StableDiffusionXLPipeline.from_pretrained(base, unet=unet, torch_dtype=torch.float16, variant='fp16').to('cuda')\n",
            "    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing='trailing')\n",
            "    print('✅ SDXL-Lightning ready!')\n"
        ]
    })

    # Cell 4: Step 3: Run Generation
    tasks_json = json.dumps(CH54_PROMPTS + CH57_PROMPTS + CH61_PROMPTS, indent=4, ensure_ascii=False)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step3_generate_all"},
        "outputs": [],
        "source": [
            f"# Step 3: Generate All 136 Master Film Visuals\n",
            "import os, time\n",
            "from PIL import Image\n",
            "\n",
            f"tasks = {tasks_json}\n",
            "\n",
            "base_out_dir = 'production/visuals/thirukkural'\n",
            "print(f'🚀 Starting batch generation of {len(tasks)} master film artworks...')\n",
            "start_time = time.time()\n",
            "\n",
            "for idx, task in enumerate(tasks, 1):\n",
            "    out_path = os.path.join(base_out_dir, task['filename'])\n",
            "    os.makedirs(os.path.dirname(out_path), exist_ok=True)\n",
            "\n",
            "    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:\n",
            "        print(f'[{idx}/{len(tasks)}] Already exists, skipping: {task[\"filename\"]}')\n",
            "        continue\n",
            "\n",
            "    t0 = time.time()\n",
            "    prompt = task['prompt']\n",
            "    print(f'\\n[{idx}/{len(tasks)}] Generating: {task[\"title\"]} -> {task[\"filename\"]}')\n",
            "\n",
            "    if ENGINE == 'FLUX-schnell':\n",
            "        image = pipe(\n",
            "            prompt=prompt,\n",
            "            width=1280,\n",
            "            height=720,\n",
            "            num_inference_steps=4,\n",
            "            max_sequence_length=256\n",
            "        ).images[0]\n",
            "    else:\n",
            "        image = pipe(\n",
            "            prompt=prompt,\n",
            "            negative_prompt='modern elements, distorted limbs, blurry, text, watermark, bad anatomy, pink tint',\n",
            "            num_inference_steps=4,\n",
            "            guidance_scale=0.0,\n",
            "            width=1280,\n",
            "            height=720\n",
            "        ).images[0]\n",
            "\n",
            "    image.save(out_path, 'JPEG', quality=95)\n",
            "    elapsed = time.time() - t0\n",
            "    print(f'  ✅ Saved ({elapsed:.2f}s): {out_path}')\n",
            "\n",
            "total_elapsed = time.time() - start_time\n",
            "print(f'\\n🎉 All {len(tasks)} master film artworks generated successfully in {total_elapsed/60:.2f} minutes!')\n"
        ]
    })

    # Cell 5: Step 4: Zip & Download
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step4_zip_download"},
        "outputs": [],
        "source": [
            "# Step 4: Package Master Artworks and Trigger Automatic Download\n",
            "import os, zipfile\n",
            "from google.colab import files\n",
            "\n",
            "zip_filename = 'gurukuladesam_film_artworks_a100.zip'\n",
            "print(f'📦 Packaging production visuals into {zip_filename}...')\n",
            "\n",
            "with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:\n",
            "    for root, dirs, filenames in os.walk('production/visuals/thirukkural'):\n",
            "        for fn in filenames:\n",
            "            if fn.endswith(('.jpg', '.png')):\n",
            "                full_path = os.path.join(root, fn)\n",
            "                arcname = os.path.relpath(full_path, '.')\n",
            "                zipf.write(full_path, arcname)\n",
            "\n",
            "size_mb = os.path.getsize(zip_filename) / (1024 * 1024)\n",
            "print(f'✅ Archive created: {zip_filename} ({size_mb:.2f} MB)')\n",
            "print('⬇ Triggering automatic browser download...')\n",
            "files.download(zip_filename)\n"
        ]
    })

    nb = {
        "cells": cells,
        "metadata": {
            "colab": {
                "provenance": [],
                "toc_visible": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            },
            "accelerator": "GPU"
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"Created dedicated notebook: {NOTEBOOK_PATH} with {total_images} shot prompts!")

if __name__ == "__main__":
    build()
