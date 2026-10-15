import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🎬 Gurukuladesam Batch Video Render Pipeline (NVIDIA L4 GPU NVENC)\n",
                "\n",
                "High-speed parallel batch rendering powered by **NVIDIA Ada Lovelace L4 (24GB VRAM)** with:\n",
                "- Dedicated **8th Gen NVENC (AV1 / H.264)** hardware video encoding units.\n",
                "- Multi-stream parallel encoding (< 25s per 4-minute master video).\n",
                "- 5–7s dynamic image transitions with 1.0s `xfade` (cross-dissolve).\n",
                "- 4-way cinematic pans + 3D parabolic curved arc camera moves.\n",
                "- 100% upward divine drizzle / vibhuti flakes atmospheric composite.\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 1: Verify NVIDIA L4 GPU & Hardware NVENC Support\n",
                "!nvidia-smi\n",
                "!ffmpeg -f lavfi -i testsrc=duration=2:size=1280x720:rate=24 -c:v h264_nvenc -preset p4 -y /tmp/test_nvenc.mp4 2>&1 | tail -n 6\n",
                "!ls -lh /tmp/test_nvenc.mp4\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 2: Clone repository & install dependencies\n",
                "import os\n",
                "if not os.path.exists('/content/Gurukuladesam'):\n",
                "    !git clone -b main https://github.com/shishyan/GuruKulaDesam.git /content/Gurukuladesam\n",
                "\n",
                "%cd /content/Gurukuladesam\n",
                "!pip install -q Pillow numpy tqdm requests mutagen\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 3: Fast GPU Batch Render with L4 NVENC (Starting from Chapter 4 in parallel)\n",
                "# Pass --gpu nvenc and --start-chapter 4\n",
                "!python tools/batch_render_all_cinematic.py --gpu nvenc --start-chapter 4\n"
            ]
        }
    ],
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "L4",
            "machineShape": "hm",
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open("colab_batch_render_l4.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("Created colab_batch_render_l4.ipynb successfully with NVIDIA L4 GPU default.")
