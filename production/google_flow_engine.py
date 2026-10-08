# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Google Flow (Veo 3.1) Universal Direct Video Engine
Directly generates cinematic AI videos using Google DeepMind's Veo 3.1 video family
via the google-genai SDK, assembles master films with authentic audio,
consecrated corner framing, and scene-aware atmospheric effects.

Usage:
  python production/google_flow_engine.py --list
  python production/google_flow_engine.py --track GydxHEmyDPc
  python production/google_flow_engine.py --file production/google_flow_prompts/vinayagar/GydxHEmyDPc_track.md
  python production/google_flow_engine.py --category vinayagar
"""

import os
import sys
import re
import glob
import time
import json
import argparse
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe"
RENDERS_DIR = ROOT / "renders" / "releases"
RENDERS_DIR.mkdir(parents=True, exist_ok=True)
FLOW_RENDERS_DIR = ROOT / "production" / "google_flow_renders"
FLOW_RENDERS_DIR.mkdir(parents=True, exist_ok=True)
PROMPTS_DIR = ROOT / "production" / "google_flow_prompts"
SOURCE_AUDIO_DIR = ROOT / "source" / "youtube"
SOURCE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
OVERLAY_FILE = ROOT / "production" / "sacred_lamp_dhoopa_overlay_1280x720.png"
DRIZZLE_LOOP = ROOT / "production" / "drizzle_composite_loop.mp4"

def get_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

def get_genai_client():
    from google import genai
    return genai.Client(api_key=get_gemini_api_key())

def parse_blueprint(file_path: Path) -> dict:
    """Parses a Google Flow prompt markdown blueprint."""
    text = file_path.read_text(encoding="utf-8")
    
    # Extract Title
    title_match = re.search(r"^#\s*Google Flow Cinematic Video Plan\s*—\s*(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else file_path.stem
    
    # Extract Track ID
    track_id_match = re.search(r"\*\*Track ID:\*\*\s*`?([A-Za-z0-9_\-]+)`?", text)
    track_id = track_id_match.group(1).strip() if track_id_match else None
    if not track_id:
        # Fallback to filename prefix
        prefix = file_path.stem.split("_")[0]
        if len(prefix) == 11:
            track_id = prefix
            
    # Extract Category
    cat_match = re.search(r"\*\*Category:\*\*\s*([A-Za-z0-9_]+)", text)
    category = cat_match.group(1).strip().upper() if cat_match else file_path.parent.name.upper()

    # Extract Continuity Bible
    continuity = {}
    for field in ["Atmosphere", "Architecture", "Lighting", "Hard Exclusions"]:
        f_match = re.search(rf"-\s*\*\*{field}:\*\*\s*(.+)$", text, re.MULTILINE)
        if f_match:
            continuity[field] = f_match.group(1).strip()

    # Extract Scenes
    scenes = []
    scene_blocks = re.findall(r"###\s*Scene\s*(\d+)[^\n]*\n([\s\S]*?)(?=###\s*Scene|\Z)", text)
    for num, block in scene_blocks:
        prompt_m = re.search(r"\*\*Prompt:\*\*\s*\n*(.*?)(?=\n\*[A-Za-z]|\Z)", block, re.DOTALL)
        excl_m = re.search(r"\*Exclusions:\*\s*(.*?)(?=\n\n|\Z)", block, re.DOTALL)
        
        prompt_text = prompt_m.group(1).strip() if prompt_m else ""
        excl_text = excl_m.group(1).strip() if excl_m else ""
        
        if prompt_text:
            scenes.append({
                "scene_num": int(num),
                "prompt": prompt_text,
                "exclusions": excl_text,
            })

    return {
        "file_path": file_path,
        "title": title,
        "track_id": track_id,
        "category": category,
        "continuity": continuity,
        "scenes": scenes,
    }

def ensure_audio(track_id: str) -> Path:
    """Ensures the track audio file is present, downloading via yt-dlp if needed."""
    audio_path = SOURCE_AUDIO_DIR / f"{track_id}.m4a"
    if audio_path.exists() and audio_path.stat().st_size > 100_000:
        return audio_path

    print(f"[Audio] Fetching master audio for track {track_id} via yt-dlp...", flush=True)
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "m4a",
        "-o", str(SOURCE_AUDIO_DIR / "%(id)s.%(ext)s"),
        f"https://www.youtube.com/watch?v={track_id}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Audio Warning] yt-dlp failed: {res.stderr}", flush=True)
        # Search for any existing file
        existing = list(SOURCE_AUDIO_DIR.glob(f"{track_id}.*"))
        if existing:
            return existing[0]
        raise RuntimeError(f"Could not resolve audio for track {track_id}")
    return audio_path

def get_media_duration(file_path: Path) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return float(res.stdout.strip())

def generate_veo_clip(client, prompt: str, out_path: Path, model: str = "veo-3.1-fast-generate-preview", duration: int = 6, max_retries: int = 5) -> Path:
    """Invokes Google Flow (Veo 3.1) video generation, polls operation, and downloads MP4 with high-demand retry handling."""
    from google.genai import types

    if out_path.exists() and out_path.stat().st_size > 500_000:
        print(f"  [Cached] Scene clip already exists: {out_path.name} ({out_path.stat().st_size / 1024 / 1024:.2f} MB)", flush=True)
        return out_path

    for attempt in range(1, max_retries + 1):
        try:
            print(f"  [Veo 3.1] Submitting generation to model '{model}' ({duration}s, attempt {attempt}/{max_retries})...", flush=True)
            print(f"  [Prompt] {prompt[:120]}...", flush=True)

            op = client.models.generate_videos(
                model=model,
                source=types.GenerateVideosSource(prompt=prompt),
                config=types.GenerateVideosConfig(
                    aspect_ratio="16:9",
                    duration_seconds=duration,
                )
            )

            op_name = op.name
            print(f"  [Operation] {op_name} launched. Polling status...", flush=True)

            poll_interval = 8
            max_wait = 600
            elapsed = 0

            while elapsed < max_wait:
                time.sleep(poll_interval)
                elapsed += poll_interval
                status_op = client.operations.get(operation=op)
                if status_op.done:
                    if status_op.error:
                        err_msg = str(status_op.error)
                        if "high demand" in err_msg.lower() or "'code': 14" in err_msg or "temporarily unavailable" in err_msg.lower():
                            backoff = attempt * 30
                            print(f"  [Veo High Demand Detected] {err_msg} -> Backing off {backoff}s before retry...", flush=True)
                            time.sleep(backoff)
                            break # breaks poll loop to trigger outer attempt retry
                        raise RuntimeError(f"Veo generation failed: {status_op.error}")
                    
                    if not status_op.response or not status_op.response.generated_videos:
                        raise RuntimeError("Veo generation completed without video in response.")
                    
                    video_obj = status_op.response.generated_videos[0].video
                    print(f"  [Complete in {elapsed}s] Downloading video artifact...", flush=True)
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    client.files.download(file=video_obj, destination=str(out_path))
                    print(f"  [Downloaded] Saved to {out_path} ({out_path.stat().st_size / 1024 / 1024:.2f} MB)", flush=True)
                    return out_path

                print(f"  [Polling] Waiting for Veo... ({elapsed}s elapsed)", flush=True)

        except Exception as e:
            err_str = str(e)
            if "high demand" in err_str.lower() or "'code': 14" in err_str or "temporarily unavailable" in err_str.lower():
                backoff = attempt * 30
                print(f"  [High Demand Error] Backing off {backoff}s before retry (Attempt {attempt}/{max_retries})...", flush=True)
                time.sleep(backoff)
                continue
            raise e

    raise TimeoutError(f"Veo generation failed after {max_retries} attempts due to persistent high demand.")

def build_master_film(track_info: dict, scene_clips: list[Path], audio_path: Path, output_path: Path) -> Path:
    """Assembles scene clips to match audio duration, overlays sacred kuthuvilakku/dhoopam frame and subtle drizzle."""
    audio_dur = get_media_duration(audio_path)
    print(f"\n[Assembly] Audio Duration: {audio_dur:.2f}s | Available Veo Clips: {len(scene_clips)}", flush=True)
    
    # Calculate how many repetitions or sequences of clips we need
    clip_durs = [get_media_duration(c) for c in scene_clips]
    total_scenes_dur = sum(clip_durs)
    print(f"[Assembly] 1 Pass Duration: {total_scenes_dur:.2f}s", flush=True)
    
    # Create temp concat list
    temp_dir = ROOT / "renders" / f"temp_flow_{track_info['track_id']}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    concat_file = temp_dir / "concat_list.txt"
    
    # Repeat the scene sequence until it exceeds audio_dur + 5s
    needed_passes = max(1, int(audio_dur / total_scenes_dur) + 1)
    with open(concat_file, "w", encoding="utf-8") as f:
        for _ in range(needed_passes):
            for clip in scene_clips:
                clip_str = str(clip.resolve()).replace("\\", "/")
                f.write(f"file '{clip_str}'\n")

    looped_video = temp_dir / "looped_video.mp4"
    print(f"[Assembly] Concatenating {needed_passes} passes of scene clips...", flush=True)
    cmd_concat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(looped_video)
    ]
    subprocess.run(cmd_concat, check=True, capture_output=True)

    # Master composition with Sacred Overlay & Divine Drizzle
    print("[Assembly] Composing master film with sacred framing & audio sync...", flush=True)
    
    has_drizzle = DRIZZLE_LOOP.exists()
    has_overlay = OVERLAY_FILE.exists()

    inputs = [
        "-i", str(looped_video),
        "-i", str(audio_path),
    ]
    
    filter_complex = []
    curr_v = "[0:v]"
    
    # Scale base video to 1280x720 24fps
    filter_complex.append(f"{curr_v}scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,setsar=1,format=rgba[v_base]")
    curr_v = "[v_base]"

    input_idx = 2
    if has_drizzle:
        inputs.extend(["-stream_loop", "-1", "-i", str(DRIZZLE_LOOP)])
        drizzle_idx = input_idx
        input_idx += 1
        # Screen blend drizzle layer over base video
        filter_complex.append(f"[{drizzle_idx}:v]scale=1280:720,fps=24,setsar=1,format=rgba[drizzle_rgba]")
        filter_complex.append(f"{curr_v}format=gbrp[v_gbrp];[drizzle_rgba]format=gbrp[d_gbrp];[v_gbrp][d_gbrp]blend=all_mode=screen:all_opacity=0.25,format=rgba[v_drizzled]")
        curr_v = "[v_drizzled]"

    if has_overlay:
        inputs.extend(["-loop", "1", "-i", str(OVERLAY_FILE)])
        overlay_idx = input_idx
        input_idx += 1
        filter_complex.append(f"[{overlay_idx}:v]format=rgba[fg_overlay]")
        filter_complex.append(f"{curr_v}[fg_overlay]overlay=0:0:format=auto,format=yuv420p[v_framed]")
        curr_v = "[v_framed]"

    # Audio fade out over last 2 seconds
    fade_start = max(0.0, audio_dur - 2.0)
    filter_complex.append(f"[1:a]afade=t=out:st={fade_start:.2f}:d=2.0[a_out]")

    cmd_master = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", ";".join(filter_complex),
        "-map", curr_v,
        "-map", "[a_out]",
        "-t", f"{audio_dur:.2f}",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-movflags", "+faststart",
        str(output_path)
    ]

    res = subprocess.run(cmd_master, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg master assembly failed:\n{res.stderr}")

    print(f"\n[Master Film Complete] Output: {output_path} ({output_path.stat().st_size / 1024 / 1024:.2f} MB)", flush=True)
    return output_path

def process_blueprint(file_path: Path, model: str = "veo-3.1-fast-generate-preview", duration: int = 6, generate_only: bool = False, assemble_only: bool = False) -> Path:
    """Executes the complete Google Flow generation pipeline for a single blueprint."""
    bp = parse_blueprint(file_path)
    print("=" * 80, flush=True)
    print(f"GOOGLE FLOW VIDEO GENERATION: {bp['title']}", flush=True)
    print(f"Track ID: {bp['track_id']} | Category: {bp['category']} | Scenes: {len(bp['scenes'])}", flush=True)
    print("=" * 80, flush=True)

    track_dir = FLOW_RENDERS_DIR / (bp['track_id'] or file_path.stem)
    track_dir.mkdir(parents=True, exist_ok=True)

    scene_clips = []
    
    if not assemble_only:
        client = get_genai_client()
        continuity_context = " ".join([f"{k}: {v}." for k, v in bp['continuity'].items() if k != "Hard Exclusions"])
        exclusions = bp['continuity'].get("Hard Exclusions", "No text, no watermarks, no modern vehicles, no plastic.")

        for sc in bp['scenes']:
            sc_num = sc['scene_num']
            clip_path = track_dir / f"scene_{sc_num:02d}.mp4"
            
            # Combine scene prompt with continuity guidelines
            full_prompt = (
                f"{sc['prompt']} "
                f"Setting continuity: {continuity_context} "
                f"Negative constraints: {sc.get('exclusions', '')} {exclusions}"
            )
            
            clip = generate_veo_clip(
                client=client,
                prompt=full_prompt,
                out_path=clip_path,
                model=model,
                duration=duration,
            )
            scene_clips.append(clip)
    else:
        scene_clips = sorted(track_dir.glob("scene_*.mp4"))
        if not scene_clips:
            raise FileNotFoundError(f"No rendered scene clips found in {track_dir} for assemble-only mode.")

    if generate_only:
        print("\n[Done] --generate-only flag set. Skipping final master assembly.", flush=True)
        return track_dir

    # Master audio and film assembly
    if not bp['track_id']:
        raise ValueError(f"No Track ID found in blueprint {file_path.name}")

    audio_path = ensure_audio(bp['track_id'])
    out_film_path = RENDERS_DIR / f"{bp['category'].lower()}_{bp['track_id']}_master.mp4"
    master_film = build_master_film(bp, scene_clips, audio_path, out_film_path)
    return master_film

def list_blueprints():
    """Lists all available Google Flow blueprints categorized."""
    md_files = sorted(PROMPTS_DIR.glob("*/*.md"))
    print(f"\nFound {len(md_files)} Google Flow prompt blueprints:\n", flush=True)
    print(f"{'Category':<18} | {'Track ID':<13} | {'Scenes':<7} | {'Audio':<6} | Title", flush=True)
    print("-" * 80, flush=True)
    for f in md_files:
        try:
            bp = parse_blueprint(f)
            has_audio = (SOURCE_AUDIO_DIR / f"{bp['track_id']}.m4a").exists() if bp['track_id'] else False
            audio_flag = "✓ Yes" if has_audio else "- No "
            print(f"{bp['category']:<18} | {str(bp['track_id']):<13} | {len(bp['scenes']):<7} | {audio_flag:<6} | {bp['title'][:35]}", flush=True)
        except Exception as e:
            print(f"Error parsing {f.name}: {e}", flush=True)
    print("-" * 80, flush=True)

def main():
    parser = argparse.ArgumentParser(description="Guru Kula Desam - Google Flow (Veo 3.1) Universal Direct Video Engine")
    parser.add_argument("--list", action="store_true", help="List all available prompt blueprints")
    parser.add_argument("--track", type=str, help="Process a specific track by Track ID")
    parser.add_argument("--file", type=str, help="Process a specific prompt blueprint file")
    parser.add_argument("--category", type=str, help="Process all blueprints in a category (e.g. vinayagar, shiva)")
    parser.add_argument("--model", type=str, default="veo-3.1-fast-generate-preview", help="Veo model to use (default: veo-3.1-fast-generate-preview)")
    parser.add_argument("--duration", type=int, default=6, help="Clip duration in seconds (4-8, default: 6)")
    parser.add_argument("--generate-only", action="store_true", help="Generate video clips only, skip master assembly")
    parser.add_argument("--assemble-only", action="store_true", help="Assemble existing video clips, skip generation")
    
    args = parser.parse_args()

    if args.list:
        list_blueprints()
        return

    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = ROOT / p
        process_blueprint(p, model=args.model, duration=args.duration, generate_only=args.generate_only, assemble_only=args.assemble_only)
        return

    if args.track:
        matches = [f for f in PROMPTS_DIR.glob(f"*/{args.track}*.md")]
        if not matches:
            print(f"Error: No blueprint found for track ID '{args.track}'", flush=True)
            return
        process_blueprint(matches[0], model=args.model, duration=args.duration, generate_only=args.generate_only, assemble_only=args.assemble_only)
        return

    if args.category:
        cat_dir = PROMPTS_DIR / args.category.lower()
        if not cat_dir.exists():
            print(f"Error: Category directory '{args.category}' not found in {PROMPTS_DIR}", flush=True)
            return
        files = sorted(cat_dir.glob("*.md"))
        print(f"Found {len(files)} blueprints in category '{args.category}'", flush=True)
        for f in files:
            process_blueprint(f, model=args.model, duration=args.duration, generate_only=args.generate_only, assemble_only=args.assemble_only)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
