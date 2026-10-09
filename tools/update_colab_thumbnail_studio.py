# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Colab Thumbnail Studio Updater
Adds a dedicated GPU-accelerated Devotional Thumbnail Studio to Guru-Kula-Desam.ipynb.
"""

import json
from pathlib import Path

nb_path = Path(r"c:\GitHub\Guru-Kula-Desam.ipynb")
if not nb_path.exists():
    print(f"Error: {nb_path} does not exist")
    exit(1)

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

md_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🎨 Step 12: Dedicated 4K Devotional Thumbnail Studio (GPU Accelerated)\n",
        "Generates cinematic 16:9 thumbnails (1920x1080) for Lord Murugar rapid-queue releases with divine temple lighting, golden Vel aura, and saves directly to `/content/drive/MyDrive/GuruKulaDesam/thumbnails/`."
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "#@title Run Devotional Thumbnail Studio (GPU Accelerated)\n",
        "import os, sys, json\n",
        "from pathlib import Path\n",
        "\n",
        "# Install diffusers & torch\n",
        "!pip install -q diffusers transformers accelerate safetensors sentencepiece protobuf torch torchvision pillow\n",
        "\n",
        "import torch\n",
        "from diffusers import AutoPipelineForText2Image\n",
        "\n",
        "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n",
        "print(f'🚀 Initializing Devotional Thumbnail Studio on {device}...')\n",
        "\n",
        "# High-speed photorealistic SDXL-Turbo\n",
        "pipe = AutoPipelineForText2Image.from_pretrained(\n",
        "    'stabilityai/sdxl-turbo',\n",
        "    torch_dtype=torch.float16 if device == 'cuda' else torch.float32,\n",
        "    variant='fp16' if device == 'cuda' else None\n",
        ").to(device)\n",
        "\n",
        "output_dir = Path('/content/drive/MyDrive/GuruKulaDesam/thumbnails')\n",
        "output_dir.mkdir(parents=True, exist_ok=True)\n",
        "\n",
        "# Murugan rapid-queue releases\n",
        "queue_tracks = [\n",
        "    {\n",
        "        'id': '3oJ2OPG-WCs',\n",
        "        'title': 'Muthai Tharu (Thiruppugazh)',\n",
        "        'prompt': 'Cinematic 16:9 devotional masterpiece, 8k. Lord Murugan standing majestically atop Thiruchendur seashore cliffs, holding glowing golden divine Vel. Iridescent emerald peacock beside Him. Golden twilight sky, glowing incense, sacred Tripundra Vibhuti, hyperrealistic temple lighting, no modern clothing.'\n",
        "    },\n",
        "    {\n",
        "        'id': 'On2xoZqBsss',\n",
        "        'title': 'Muthai Tharu II',\n",
        "        'prompt': 'Cinematic 16:9 devotional masterpiece, 8k. Young Lord Balasubramanya adorned with sacred rudraksha garland and radiant golden crown, holding sharp luminous Vel. Sacred temple mandapam in background, burning brass deepams, glowing aura, divine serenity.'\n",
        "    },\n",
        "    {\n",
        "        'id': 'SN7FIkL-o1k',\n",
        "        'title': 'Muthai Tharu III',\n",
        "        'prompt': 'Cinematic 16:9 devotional masterpiece, 8k. Lord Swaminatha Swami whispering the cosmic Pranava mantra OM into Lord Shiva\\'s ear on Mount Kailash. Golden divine radiance, snow-capped Himalayas, ancient rishis in reverence, photorealistic.'\n",
        "    },\n",
        "    {\n",
        "        'id': '5RTBMEIozEg',\n",
        "        'title': 'Naal En Seyyum',\n",
        "        'prompt': 'Cinematic 16:9 devotional masterpiece, 8k. Lord Murugan triumphantly wielding the divine golden Vel, subduing nine planetary afflictions. Radiant aura of absolute protection, ancient Dravidian temple pillars, mystical divine grace.'\n",
        "    }\n",
        "]\n",
        "\n",
        "print(f'🎨 Generating {len(queue_tracks)} high-definition devotional thumbnails...')\n",
        "for item in queue_tracks:\n",
        "    out_file = output_dir / f\"{item['id']}_thumbnail.png\"\n",
        "    if out_file.exists():\n",
        "        print(f'✅ Already exists: {out_file.name}')\n",
        "        continue\n",
        "    print(f\"🎨 Generating thumbnail for: {item['title']}...\")\n",
        "    img = pipe(prompt=item['prompt'], num_inference_steps=2, guidance_scale=0.0).images[0]\n",
        "    img = img.resize((1920, 1080))\n",
        "    img.save(str(out_file))\n",
        "    print(f'   Saved: {out_file} (1920x1080)')\n",
        "\n",
        "print('\\n🎉 All thumbnails generated and saved to Google Drive!')\n"
    ]
}

if len(nb["cells"]) > 12:
    nb["cells"][12] = md_cell
    if len(nb["cells"]) > 13:
        nb["cells"][13] = code_cell
    else:
        nb["cells"].append(code_cell)
else:
    nb["cells"].append(md_cell)
    nb["cells"].append(code_cell)

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"Successfully updated {nb_path} with Thumbnail Studio cells!")

