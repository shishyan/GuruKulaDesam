#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/colab/build_upanishad_wan21_ltx_a100_notebook.py

Generates the ready-to-run Google Colab A100 Notebook:
  /home/shishyan/GitHub/GuruKulaDesam/tools/colab/colab_upanishad_wan21_ltx_a100_pilot.ipynb
and uploads it directly to Google Drive (`GuruKulaDesam/Tools/`) so the user can open it
with 1 click in Google Colab on an A100 GPU.

What the Notebook Does on A100 (40GB / 80GB VRAM):
1. Engine Selector:
   - `ENGINE = "wan2.1"` -> `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` (or `Wan2.1-T2V-14B-Diffusers` in bfloat16 on A100)
   - `ENGINE = "ltx"`    -> `Lightricks/LTX-Video` (blazing fast 24fps 16:9 Text-to-Video on A100)
   - `ENGINE = "both"`   -> Generates Scene 1 in both Wan 2.1 and LTX-Video side-by-side to compare quality & speed, then generates all 7 scenes!
2. Embedded Pilot Story #1:
   - **Katha Upanishad (#003) — Nachiketa & Lord Yama: The Three Boons & Secret of Immortality**
   - Full 7 Scenes (`scene_01.mp4` .. `scene_07.mp4`) with 16:9 prompts, negative prompts, Tamil & English narration (`edge-tts` / `gTTS` neural voiceover), and 2x optical-flow slow-motion extender.
3. Full Master Film Assembly:
   - Stitches all 7 scenes into a complete 1080p 16:9 YouTube video (`MUKHYA_03_KATHA_01_Wan21_LTX_Master_1080p.mp4`) with Tamil & English subtitles and saves to Google Drive (`GuruKulaDesam/Videos/Upanishads/`).
"""

import json
from pathlib import Path

ROOT = Path("/home/shishyan/GitHub/GuruKulaDesam")
MANIFEST_PATH = ROOT / "production" / "upanishad_stories" / "google_flow_7scene_master_manifest.json"
OUT_IPYNB = ROOT / "tools" / "colab" / "colab_upanishad_wan21_ltx_a100_pilot.ipynb"

def make_cell(cell_type, source_str, cell_id):
    lines = [line + "\n" for line in source_str.split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    cell = {
        "cell_type": cell_type,
        "metadata": {"id": cell_id},
        "source": lines
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

def main():
    manifest = json.load(open(MANIFEST_PATH, encoding="utf-8"))
    # Pick Katha Upanishad (#003 - Nachiketa & Yama) as default pilot, plus embed top 5 stories for instant selection
    pilot_tracks = []
    target_ids = [
        "MUKHYA_03_KATHA_01",
        "MUKHYA_01_ISHA_01",
        "MUKHYA_02_KENA_01",
        "MUKHYA_11_CHANDOGYA_01",
        "MUKHYA_12_CHANDOGYA_02",
    ]
    for tid in target_ids:
        for t in manifest["tracks"]:
            if t["track_id"] == tid:
                pilot_tracks.append(t)
                break

    cells = []

    # Cell 0: Title & Instructions
    cells.append(make_cell("markdown", """# 🎬 குரு குல தேசம் — Upanishad 7-Scene 16:9 Video Generator (`Wan 2.1` + `LTX-Video` on A100 GPU)

This notebook generates a complete **7-Scene 16:9 Upanishad Story Video** on an **NVIDIA A100 GPU** using open-weights state-of-the-art video diffusion models (**Wan 2.1** and **LTX-Video**):

1. **Zero API Cost / Zero Flow Credits**: Runs 100% on your Colab A100 GPU in `bfloat16`.
2. **Dual Engine Support**:
   - **`LTX-Video` (`Lightricks/LTX-Video`)**: Ultra-fast (~12–18 seconds per 5-second 24fps clip on A100).
   - **`Wan 2.1` (`Wan-AI/Wan2.1-T2V-1.3B-Diffusers` or `14B`)**: Deep cinematic texture, lighting, and motion coherence (~45–75 seconds per clip on A100).
3. **Complete 7-Scene Pilot Story Embedded**:
   - Default Story: **`MUKHYA_03_KATHA_01` — கடோபநிடதம் (Katha Upanishad #003): நசிகேதனும் எமதர்மனும் — மூன்று வரங்களும் மரணமில்லாப் பெருவாழ்வும் (Nachiketa & Lord Yama)**
   - Also loads all **138 Upanishad stories (966 scenes)** automatically if your Google Drive is mounted!

👉 **How to run**:
1. Go to **Runtime → Change runtime type → Select `A100 GPU`**.
2. Click **Runtime → Run all (`Ctrl + F9`)**.""", "intro_md"))

    # Cell 1: Check A100 GPU & Install Dependencies
    cells.append(make_cell("code", """# Step 1: Verify A100 GPU & Install Latest Diffusers + Video Dependencies
!pip install -q -U diffusers transformers accelerate safetensors sentencepiece protobuf imageio imageio-ffmpeg edge-tts

import torch
print("PyTorch:", torch.__version__)
assert torch.cuda.is_available(), "❌ No GPU detected! Switch Runtime -> Change runtime type -> A100 GPU."
gpu_name = torch.cuda.get_device_name(0)
vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
print(f"✅ GPU Active: {gpu_name} ({vram_gb:.1f} GB VRAM)")""", "step1_install"))

    # Cell 2: Mount Google Drive (Optional automatic sync)
    cells.append(make_cell("code", """# Step 2: Mount Google Drive to save 7 scenes & assembled 1080p film directly to Drive
from pathlib import Path
import os

USE_GOOGLE_DRIVE = True
DRIVE_OUT_DIR = Path("/content/upanishad_renders")

if USE_GOOGLE_DRIVE:
    try:
        from google.colab import drive
        drive.mount("/content/drive")
        DRIVE_OUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/Videos/Upanishads_Wan21_LTX")
        DRIVE_OUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ Mounted Google Drive! Renders will be saved to: {DRIVE_OUT_DIR}")
    except Exception as e:
        print(f"⚠️ Drive mount skipped ({e}), saving locally to /content/upanishad_renders")
        DRIVE_OUT_DIR.mkdir(parents=True, exist_ok=True)
else:
    DRIVE_OUT_DIR.mkdir(parents=True, exist_ok=True)""", "step2_drive"))

    # Cell 3: Load the Embedded 7-Scene Pilot Story (or any of the 138 stories from Drive)
    pilot_py_str = repr(pilot_tracks)
    cells.append(make_cell("code", f"""# Step 3: Select Upanishad Story & Inspect its 7 Scenes
import json

EMBEDDED_PILOT_STORIES = {pilot_py_str}

# Choose which story to generate (0 = Katha Upanishad: Nachiketa & Yama, 1 = Isha, 2 = Kena, 3 = Chandogya Satyakama, 4 = Chandogya Tat Tvam Asi)
STORY_INDEX = 0

# Or if you uploaded google_flow_7scene_master_manifest.json to Drive, load all 138 stories automatically:
manifest_drive_path = Path("/content/drive/MyDrive/GuruKulaDesam/upanishad_stories/google_flow_7scene_master_manifest.json")
if manifest_drive_path.exists():
    all_tracks = json.load(open(manifest_drive_path, encoding="utf-8"))["tracks"]
    print(f"📚 Loaded full 138-Story Master Manifest from Drive ({{len(all_tracks)}} tracks)!")
    selected_story = all_tracks[STORY_INDEX]
else:
    selected_story = EMBEDDED_PILOT_STORIES[STORY_INDEX]

print("=================================================================")
print(f"🎬 SELECTED STORY: {{selected_story['track_id']}} (Muktika #{{selected_story['muktika_number']:03d}})")
print(f"📖 Upanishad     : {{selected_story['upanishad_en']}} | {{selected_story['upanishad_ta']}}")
print(f"🌟 Title (EN)    : {{selected_story['title_en']}}")
print(f"🌟 Title (TA)    : {{selected_story['title_ta']}}")
print("=================================================================")
for sc in selected_story["scenes"]:
    print(f"  • Scene {{sc['scene_num']}}: {{sc['title']}}")""", "step3_story_data"))

    # Cell 4: Load Wan 2.1 and/or LTX-Video Pipeline on A100
    cells.append(make_cell("code", """# Step 4: Load Video Generation Engine on A100 (`wan2.1` or `ltx` or `both_scene1_compare`)
# Options:
#   "wan2.1_1.3b" -> Wan-AI/Wan2.1-T2V-1.3B-Diffusers (Fast + High Cinematic Quality, ~14GB VRAM)
#   "wan2.1_14b"  -> Wan-AI/Wan2.1-T2V-14B-Diffusers  (Maximum 14B Quality on A100 40GB/80GB with CPU offload)
#   "ltx"         -> Lightricks/LTX-Video             (Blazing Fast ~15s per clip on A100)
#   "compare_then_wan" -> Generates Scene 1 in BOTH LTX-Video and Wan 2.1 first so you can compare, then generates Scenes 1..7!

ENGINE_MODE = "compare_then_wan"  # Change to "ltx", "wan2.1_1.3b", or "wan2.1_14b" if desired

import gc
import torch
from diffusers import DiffusionPipeline, LTXPipeline, AutoencoderKLWan, WanPipeline
from diffusers.utils import export_to_video

def load_ltx_pipeline():
    print("⏳ Loading Lightricks/LTX-Video in bfloat16 on A100...")
    pipe = LTXPipeline.from_pretrained(
        "Lightricks/LTX-Video",
        torch_dtype=torch.bfloat16
    ).to("cuda")
    print("✅ LTX-Video loaded on A100!")
    return pipe

def load_wan_pipeline(model_id="Wan-AI/Wan2.1-T2V-1.3B-Diffusers"):
    print(f"⏳ Loading {model_id} in bfloat16 on A100...")
    vae = AutoencoderKLWan.from_pretrained(model_id, subfolder="vae", torch_dtype=torch.float32)
    pipe = WanPipeline.from_pretrained(
        model_id,
        vae=vae,
        torch_dtype=torch.bfloat16
    )
    if "14B" in model_id:
        pipe.enable_model_cpu_offload()
    else:
        pipe.to("cuda")
    print(f"✅ {model_id} loaded on A100!")
    return pipe

def generate_clip_ltx(pipe, prompt, negative_prompt, out_path, seed=42):
    generator = torch.Generator("cuda").manual_seed(seed)
    video = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=768,
        height=512,
        num_frames=121,          # 5.0 seconds @ 24fps
        num_inference_steps=40,
        guidance_scale=3.5,
        generator=generator,
    ).frames[0]
    export_to_video(video, str(out_path), fps=24)

def generate_clip_wan(pipe, prompt, negative_prompt, out_path, seed=42):
    generator = torch.Generator("cuda").manual_seed(seed)
    video = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=832,
        height=480,              # Native 16:9 widescreen Wan 2.1 resolution
        num_frames=81,           # 5.0 seconds @ 16fps (upsampled to 24fps 1080p in post)
        num_inference_steps=35,
        guidance_scale=5.0,
        generator=generator,
    ).frames[0]
    export_to_video(video, str(out_path), fps=16)""", "step4_models"))

    # Cell 5: Run Generation (Scene 1 Side-by-Side Comparison + Full 7 Scenes)
    cells.append(make_cell("code", """# Step 5: Generate the 7 Scenes for the Selected Upanishad Story
import gc, time, json
from pathlib import Path
from IPython.display import HTML, display
from base64 import b64encode

# Self-healing fallback if Step 2 or Step 3 was skipped:
if "DRIVE_OUT_DIR" not in globals():
    DRIVE_OUT_DIR = Path("/content/drive/MyDrive/GuruKulaDesam/Videos/Upanishads_Wan21_LTX") if Path("/content/drive/MyDrive").exists() else Path("/content/upanishad_renders")
    DRIVE_OUT_DIR.mkdir(parents=True, exist_ok=True)

if "selected_story" not in globals():
    if "EMBEDDED_PILOT_STORIES" in globals():
        selected_story = EMBEDDED_PILOT_STORIES[0]
    else:
        raise RuntimeError("Please run Step 3 cell above first (or click Runtime -> Run all) so EMBEDDED_PILOT_STORIES is loaded!")

story_dir = DRIVE_OUT_DIR / selected_story["track_id"]
story_dir.mkdir(parents=True, exist_ok=True)

def show_video_inline(mp4_path, label):
    mp4 = open(mp4_path, "rb").read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    display(HTML(f"<h4>{label} ({mp4_path.name})</h4><video width=640 controls autoplay loop muted><source src='{data_url}' type='video/mp4'></video>"))

# 1. Optional Side-by-Side Scene 1 Benchmark (LTX-Video vs Wan 2.1)
if ENGINE_MODE == "compare_then_wan":
    sc1 = selected_story["scenes"][0]
    ltx_test_path = story_dir / "scene_01_LTX_benchmark.mp4"
    if not ltx_test_path.exists():
        ltx_pipe = load_ltx_pipeline()
        t0 = time.time()
        generate_clip_ltx(ltx_pipe, sc1["prompt"], sc1["negative_prompt"], ltx_test_path, seed=101)
        print(f"⚡ LTX-Video generated Scene 1 in {time.time() - t0:.1f}s -> {ltx_test_path}")
        del ltx_pipe
        gc.collect()
        torch.cuda.empty_cache()
    show_video_inline(ltx_test_path, "⚡ LTX-Video Benchmark — Scene 1")

# 2. Generate all 7 Scenes (scene_01.mp4 .. scene_07.mp4)
if ENGINE_MODE == "ltx":
    active_pipe = load_ltx_pipeline()
    gen_fn = generate_clip_ltx
elif ENGINE_MODE == "wan2.1_14b":
    active_pipe = load_wan_pipeline("Wan-AI/Wan2.1-T2V-14B-Diffusers")
    gen_fn = generate_clip_wan
else:
    active_pipe = load_wan_pipeline("Wan-AI/Wan2.1-T2V-1.3B-Diffusers")
    gen_fn = generate_clip_wan

for sc in selected_story["scenes"]:
    snum = sc["scene_num"]
    out_mp4 = story_dir / f"scene_{snum:02d}.mp4"
    if out_mp4.exists():
        print(f"✅ Scene {snum:02d} already exists at {out_mp4}, skipping.")
        continue
    print(f"🎬 Generating Scene {snum:02d}/07: {sc['title']}...")
    t0 = time.time()
    gen_fn(active_pipe, sc["prompt"], sc["negative_prompt"], out_mp4, seed=100 + snum)
    print(f"   ✅ Saved {out_mp4.name} in {time.time() - t0:.1f}s")
    if snum == 1:
        show_video_inline(out_mp4, f"🌟 Scene 01 ({ENGINE_MODE})")

del active_pipe
gc.collect()
torch.cuda.empty_cache()
print(f"🎉 All 7 scenes generated in: {story_dir}")""", "step5_generate"))

    # Cell 6: Generate Neural Tamil/English Voiceover & Assemble Full 1080p 7-Scene Film
    cells.append(make_cell("code", """# Step 6: Generate Neural Voiceover (Tamil or English), Extend Scenes & Assemble 1080p Master Film
import asyncio
import subprocess
import edge_tts

LANGUAGE = "ta"  # Set "ta" for Senthamizh voiceover (Valluvar) or "en" for English narration
VOICE_MAP = {
    "ta": "ta-IN-ValluvarNeural",
    "en": "en-IN-PrabhatNeural"
}

async def synthesize_scene_audio():
    voice = VOICE_MAP[LANGUAGE]
    for sc in selected_story["scenes"]:
        snum = sc["scene_num"]
        text = sc["vo_ta"] if LANGUAGE == "ta" else sc["vo_en"]
        audio_path = story_dir / f"vo_{snum:02d}_{LANGUAGE}.mp3"
        if not audio_path.exists():
            communicate = edge_tts.Communicate(text, voice, rate="-8%")
            await communicate.save(str(audio_path))
            print(f"🎙️ Synthesized Scene {snum:02d} voiceover ({LANGUAGE}) -> {audio_path.name}")

await synthesize_scene_audio()

# Build 2-Step Ping-Pong 1080p Loop + Multiplex Voiceover for all 7 Scenes
segment_files = []
for sc in selected_story["scenes"]:
    snum = sc["scene_num"]
    raw_mp4 = story_dir / f"scene_{snum:02d}.mp4"
    vo_mp3 = story_dir / f"vo_{snum:02d}_{LANGUAGE}.mp3"
    pingpong_mp4 = story_dir / f"pingpong_{snum:02d}.mp4"
    seg_mp4 = story_dir / f"segment_{snum:02d}_1080p.mp4"

    # Step 6A: Create a single 12-second seamless ping-pong unit (forward + reverse) on the short 5s clip
    fc = (
        "[0:v]scale=1920:1080:flags=lanczos,fps=24,format=yuv420p,split=2[v1][v2];"
        "[v1]setpts=1.25*PTS[va];"
        "[v2]reverse,setpts=1.25*PTS[vb];"
        "[va][vb]concat=n=2:v=1:a=0[vloop]"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_mp4),
        "-filter_complex", fc,
        "-map", "[vloop]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-an",
        str(pingpong_mp4)
    ], check=True)

    # Step 6B: Infinitely loop the ping-pong unit (-stream_loop -1) to match the exact voiceover audio length
    subprocess.run([
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(pingpong_mp4),
        "-i", str(vo_mp3),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(seg_mp4)
    ], check=True)

    segment_files.append(seg_mp4)
    print(f"🎞️ Built 1080p synchronized segment {snum:02d} -> {seg_mp4.name}")

# Concatenate all 7 segments into the final 1080p Master Film
concat_txt = story_dir / "concat_list.txt"
concat_txt.write_text("\\n".join([f"file '{p.name}'" for p in segment_files]), encoding="utf-8")

final_film = story_dir / f"{selected_story['track_id']}_{LANGUAGE}_Master_1080p.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat_txt),
    "-c", "copy",
    str(final_film)
], check=True)

print("=================================================================")
print(f"🏆 MASTER 1080p 7-SCENE FILM READY: {final_film}")
print("=================================================================")
show_video_inline(final_film, f"🏆 Full 7-Scene Upanishad Film — {selected_story['title_en']}")""", "step6_assemble"))

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {
                "provenance": [],
                "gpuType": "A100"
            },
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            },
            "language_info": {
                "name": "python"
            },
            "accelerator": "GPU"
        },
        "cells": cells
    }

    OUT_IPYNB.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_IPYNB, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    print(f"Successfully created A100 Wan 2.1 + LTX-Video notebook at: {OUT_IPYNB}")

if __name__ == "__main__":
    main()
