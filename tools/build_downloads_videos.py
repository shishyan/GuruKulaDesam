#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_downloads_videos.py
Autonomous Master Film Builder for Downloads Audio Library.

Processes uncompressed master audio files from C:\\Users\\Shishyan\\Downloads,
pairs them with authentic Veo 3.1 devotional scene clips, applies sacred framing,
divine drizzle, 75% devotional flow, and outputs pristine clean 720p HD masters
into renders/releases/ with zero burned lyrics.
"""

import os
import sys
import re
import glob
import json
import time
import shutil
import hashlib
import argparse
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS_DIR = Path(r"C:\Users\Shishyan\Downloads")
RENDERS_DIR = ROOT / "renders" / "releases"
RENDERS_DIR.mkdir(parents=True, exist_ok=True)
FLOW_RENDERS_DIR = ROOT / "production" / "google_flow_renders"
OVERLAY_FILE = ROOT / "production" / "sacred_lamp_dhoopa_overlay_1280x720.png"
DRIZZLE_LOOP = ROOT / "production" / "drizzle_composite_loop.mp4"
MANIFEST_FILE = ROOT / "production" / "autonomous_master_production_manifest.json"
REGISTRY_FILE = ROOT / "production" / "youtube_published_registry.json"

FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe"

def get_audio_duration(path: Path) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def sanitize_id(name: str) -> str:
    # Produce clean ASCII ID + Tamil prefix
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    clean_name = re.sub(r"[^\w\u0B80-\u0BFF]", "_", name)
    clean_name = re.sub(r"_+", "_", clean_name).strip("_")
    return f"kural_{h}"

def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {"completed_tracks": data}
                return data
        except Exception:
            pass
    return {"completed_tracks": []}

def save_manifest(manifest: dict):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def get_veo_clips_pool() -> list:
    clips = []
    for p in FLOW_RENDERS_DIR.glob("*/*.mp4"):
        try:
            if p.stat().st_size > 500000:
                clips.append(p)
        except Exception:
            pass
    return sorted(clips, key=lambda x: str(x))

def select_clips_for_song(song_name: str, pool: list, audio_dur: float = 180.0) -> list:
    if not pool:
        return []
    # Dynamic scene count: minimum 12 scenes, up to 20 scenes for a 5-minute song
    count = min(len(pool), max(12, int(audio_dur / 15.0)))
    
    # Deterministic hash selection with wide stride for maximum visual variety
    h = int(hashlib.md5(song_name.encode("utf-8")).hexdigest(), 16)
    selected = []
    n = len(pool)
    stride = 23  # prime stride to jump across different deities/chapters
    for i in range(count):
        idx = (h + i * stride) % n
        selected.append(pool[idx])
    return selected

def build_master_film(audio_path: Path, output_path: Path, clips: list) -> bool:
    audio_dur = get_audio_duration(audio_path)
    if audio_dur < 10:
        print(f"  [Error] Audio file too short or unreadable: {audio_path.name}")
        return False

    temp_id = hashlib.md5(audio_path.name.encode("utf-8")).hexdigest()[:12]
    temp_dir = ROOT / "production" / "temp_build" / f"track_{temp_id}"
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    temp_audio = temp_dir / f"audio{audio_path.suffix}"
    shutil.copy2(audio_path, temp_audio)

    print(f"  [1/3] Preparing {len(clips)} scenes at 75% devotional speed...", flush=True)
    retime_clips = []
    for idx, clip in enumerate(clips):
        # 75% speed
        out_clip = temp_dir / f"retime_{idx:02d}.mp4"
        cmd = [
            FFMPEG, "-y", "-nostdin", "-loglevel", "error",
            "-i", str(clip),
            "-filter:v", "setpts=1.333333*PTS,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,setsar=1",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
            "-an", str(out_clip)
        ]
        subprocess.run(cmd, check=True)
        retime_clips.append(out_clip)

    # Calculate single pass duration
    single_pass_dur = sum(get_audio_duration(c) for c in retime_clips)
    if single_pass_dur <= 0:
        single_pass_dur = len(retime_clips) * 8.0

    print(f"  [2/3] Building alternating forward/reverse timeline...", flush=True)
    playlist = []
    accum_dur = 0.0
    cycle = 1
    while accum_dur < audio_dur + 5.0:
        if cycle % 2 != 0:
            for c in retime_clips:
                playlist.append(c)
                accum_dur += get_audio_duration(c)
        else:
            for idx in reversed(range(len(retime_clips))):
                fwd = retime_clips[idx]
                rev = temp_dir / f"rev_{cycle}_{idx:02d}.mp4"
                if not rev.exists():
                    cmd_rev = [
                        FFMPEG, "-y", "-nostdin", "-loglevel", "error",
                        "-i", str(fwd),
                        "-vf", "reverse",
                        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                        "-an", str(rev)
                    ]
                    subprocess.run(cmd_rev, check=True)
                playlist.append(rev)
                accum_dur += get_audio_duration(fwd)
        cycle += 1

    concat_file = temp_dir / "concat_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for p in playlist:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    looped_video = temp_dir / "looped.mp4"
    cmd_concat = [
        FFMPEG, "-y", "-nostdin", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(looped_video)
    ]
    subprocess.run(cmd_concat, check=True)

    print(f"  [3/3] Compositing sacred frame, drizzle layer, and audio sync...", flush=True)
    has_drizzle = DRIZZLE_LOOP.exists()
    has_overlay = OVERLAY_FILE.exists()

    inputs = [
        "-i", str(looped_video),
        "-i", str(temp_audio)
    ]

    filter_complex = []
    curr_v = "[0:v]"
    filter_complex.append(f"{curr_v}scale=1280:720,fps=24,setsar=1,format=rgba[v_base]")
    curr_v = "[v_base]"

    input_idx = 2
    if has_drizzle:
        inputs.extend(["-stream_loop", "-1", "-t", f"{audio_dur:.2f}", "-i", str(DRIZZLE_LOOP)])
        d_idx = input_idx
        input_idx += 1
        filter_complex.append(f"[{d_idx}:v]scale=1280:720,fps=24,setsar=1,format=rgba[drizzle_rgba]")
        filter_complex.append(f"{curr_v}format=gbrp[v_gbrp];[drizzle_rgba]format=gbrp[d_gbrp];[v_gbrp][d_gbrp]blend=all_mode=screen:all_opacity=0.25:shortest=1,format=rgba[v_drizzled]")
        curr_v = "[v_drizzled]"

    if has_overlay:
        inputs.extend(["-loop", "1", "-t", f"{audio_dur:.2f}", "-i", str(OVERLAY_FILE)])
        o_idx = input_idx
        input_idx += 1
        filter_complex.append(f"[{o_idx}:v]scale=1280:720,format=rgba[fg_overlay]")
        filter_complex.append(f"{curr_v}[fg_overlay]overlay=0:0:shortest=1:format=auto,format=yuv420p[v_framed]")
        curr_v = "[v_framed]"

    fade_start = max(0.0, audio_dur - 2.0)
    filter_complex.append(f"[1:a]afade=t=out:st={fade_start:.2f}:d=2.0[a_out]")

    cmd_master = [
        FFMPEG, "-y", "-nostdin", "-loglevel", "error",
        *inputs,
        "-filter_complex", ";".join(filter_complex),
        "-map", curr_v,
        "-map", "[a_out]",
        "-t", f"{audio_dur:.2f}",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        str(output_path)
    ]

    stderr_log = temp_dir / "ffmpeg_master_assembly.log"
    with open(stderr_log, "w", encoding="utf-8") as err_f:
        res = subprocess.run(
            cmd_master,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=err_f,
            timeout=max(1800, int(audio_dur * 8))
        )
    if res.returncode != 0:
        err_msg = stderr_log.read_text(encoding="utf-8", errors="replace") if stderr_log.exists() else "Unknown error"
        print(f"  [Master Assembly Failed]: {err_msg}", flush=True)
        return False

    # Verify integrity with ffprobe
    verify_cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(output_path)]
    try:
        vres = subprocess.run(verify_cmd, capture_output=True, text=True, check=True)
        dur = float(vres.stdout.strip())
        if dur < audio_dur - 2.0:
            print(f"  [Integrity Warning] Duration {dur}s < expected {audio_dur}s", flush=True)
            return False
    except Exception as e:
        print(f"  [Integrity Error] ffprobe failed: {e}", flush=True)
        return False

    shutil.rmtree(temp_dir, ignore_errors=True)
    return True

def process_downloads(limit: int = None):
    print("=" * 80)
    print("GURU KULA DESAM — AUTONOMOUS DOWNLOADS VIDEO BUILDER")
    print("Zero Burned Lyrics | Consecrated Visuals | Clean 720p HD Masters")
    print("=" * 80)

    audio_files = sorted(list(DOWNLOADS_DIR.glob("*.wav")) + list(DOWNLOADS_DIR.glob("*.mp3")) + list(DOWNLOADS_DIR.glob("*.m4a")))
    print(f"Found {len(audio_files)} audio files in {DOWNLOADS_DIR}")

    existing_renders = {f.stem.lower() for f in RENDERS_DIR.glob("*.mp4")}
    veo_pool = get_veo_clips_pool()
    print(f"Loaded Veo devotional scene pool: {len(veo_pool)} clips")

    manifest = load_manifest()
    completed_tids = {t.get("track_id") for t in manifest.get("completed_tracks", [])}

    # Load deduplication audit to strictly avoid duplicating existing YouTube songs
    audit_file = ROOT / "production" / "downloads_vs_youtube_audit.json"
    skip_files = {}
    if audit_file.exists():
        with open(audit_file, "r", encoding="utf-8") as af:
            audit_data = json.load(af)
            for item in audit_data.get("exact_matches_must_skip", []):
                skip_files[item["file_name"]] = item
    print(f"[Deduplication Guard] Loaded {len(skip_files)} tracks that already exist on YouTube (will be skipped).")

    built_count = 0
    for idx, audio in enumerate(audio_files, 1):
        if limit and built_count >= limit:
            print(f"[Builder] Target limit of {limit} videos reached.")
            break

        # Check deduplication guard
        if audio.name in skip_files:
            continue

        # Skip non-final / WIP / intro scratch versions
        if any(w in audio.name.lower() for w in ["intro", "draft", "test", "rough", "wip"]):
            continue

        stem = audio.stem
        # Generate sanitized track_id
        track_id = sanitize_id(stem)
        master_film_name = f"thirukkural_{track_id}_master.mp4"
        master_film_path = RENDERS_DIR / master_film_name

        # Check if already rendered and valid
        if master_film_path.exists() and master_film_path.stat().st_size > 1000000:
            verify_cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_film_path)]
            try:
                vres = subprocess.run(verify_cmd, capture_output=True, text=True, check=True)
                if float(vres.stdout.strip()) > 10.0:
                    continue
            except Exception:
                pass

        print(f"\n[{idx}/{len(audio_files)}] BUILDING CLEAN MASTER FILM:")
        print(f"  Song: {stem}")
        print(f"  Track ID: {track_id} | Audio: {audio.name} ({audio.stat().st_size / (1024*1024):.1f} MB)")

        audio_dur = get_audio_duration(audio)
        selected_clips = select_clips_for_song(stem, veo_pool, audio_dur=audio_dur)
        print(f"  Visual Diversity: Selected {len(selected_clips)} distinct Veo scenes for {audio_dur:.1f}s soundtrack.")
        success = build_master_film(audio, master_film_path, selected_clips)

        if success and master_film_path.exists():
            built_count += 1
            file_mb = round(master_film_path.stat().st_size / (1024 * 1024), 2)
            print(f"  [SUCCESS] Built Master Film: {master_film_name} ({file_mb} MB)")

            # Record in manifest
            manifest["completed_tracks"].append({
                "track_id": track_id,
                "title": f"திருக்குறள்: {stem}",
                "category": "thirukkural",
                "clean_cinematic": True,
                "master_film": f"renders/releases/{master_film_name}",
                "file_size_mb": file_mb,
                "status": "READY_CLEAN",
                "source_audio": str(audio)
            })
            save_manifest(manifest)
            print(f"  [MANIFEST] Recorded {track_id} into autonomous_master_production_manifest.json")

    print("\n" + "=" * 80)
    print(f"PRODUCTION COMPLETE. Built {built_count} new clean master films.")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build clean master films for Downloads audio")
    parser.add_argument("--limit", type=int, default=None, help="Maximum videos to build")
    args = parser.parse_args()

    process_downloads(limit=args.limit)
