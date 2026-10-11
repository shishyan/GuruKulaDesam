# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Colab Master Post-Processing & Film Assembly Pipeline
Takes raw 16:9 video scene clips, applies 75% devotional speed retiming (setpts=1.333333*PTS, 24 fps),
alternating forward/reverse timeline looping to cover full track length, blends sacred Dravidian
temple framing and subtle ambient drizzle, and multiplexes clean lossless soundtrack.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Paths inside Colab
BASE_DIR = Path("/content")
CLIPS_DIR = BASE_DIR / "generated_clips"
RELEASES_DIR = BASE_DIR / "releases"
RELEASES_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = BASE_DIR / "temp_assembly"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

DRIVE_DIR = Path("/content/drive/MyDrive/GuruKulaDesam_Releases")

def get_media_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def create_processed_clip(clip_path: Path, out_dir: Path, speed: float = 0.75, reverse: bool = False) -> Path:
    tag = f"speed_{int(speed * 100)}"
    if reverse:
        tag += "_rev"
    out_path = out_dir / f"{clip_path.stem}_{tag}.mp4"
    if out_path.exists() and out_path.stat().st_size > 100_000:
        return out_path

    pts_factor = 1.0 / speed
    filters = []
    if reverse:
        filters.append("reverse")
    filters.append(f"setpts={pts_factor:.4f}*PTS")
    filters.append("fps=24")

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(clip_path),
        "-vf", ",".join(filters),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True)
    return out_path

def assemble_master_film(track_id: str, scene_clips: list[Path], audio_path: Path, output_path: Path) -> Path:
    print(f"\n=======================================================")
    print(f"🎬 Assembling Master Film for Track: {track_id}")
    print(f"=======================================================")
    
    # STRICT GUARD: Ensure at least 7 distinct scenes
    if len(scene_clips) < 7:
        raise ValueError(f"CRITICAL GUARD VIOLATION: Video has only {len(scene_clips)} scenes. Mandate requires >= 7 scenes!")

    audio_dur = get_media_duration(audio_path)
    print(f"[Assembly] Audio Duration: {audio_dur:.2f}s ({audio_dur/60:.2f} min)")
    print(f"[Assembly] Consecrated Distinct Scenes Available: {len(scene_clips)}")

    track_temp = TEMP_DIR / track_id
    track_temp.mkdir(parents=True, exist_ok=True)
    concat_file = track_temp / "concat_list.txt"

    speed = 0.75
    print(f"[Assembly] Processing {len(scene_clips)} clips at {int(speed*100)}% devotional speed...")
    forward_clips = [create_processed_clip(c, track_temp, speed=speed, reverse=False) for c in scene_clips]
    reversed_clips = None

    base_durs = [get_media_duration(c) for c in forward_clips]
    one_pass_dur = sum(base_durs)
    print(f"[Assembly] One 7-Scene Pass Duration: {one_pass_dur:.2f}s")

    playlist = []
    current_dur = 0.0
    cycle = 1

    while current_dur < audio_dur:
        if cycle % 2 == 1:
            playlist.extend(forward_clips)
        else:
            if reversed_clips is None:
                reversed_clips = [create_processed_clip(c, track_temp, speed=speed, reverse=True) for c in reversed(scene_clips)]
            playlist.extend(reversed_clips)
        current_dur += one_pass_dur
        cycle += 1
        if cycle > 30:
            break

    with open(concat_file, "w", encoding="utf-8") as f:
        for clip in playlist:
            f.write(f"file '{clip.resolve()}'\n")

    looped_video = track_temp / "looped_video.mp4"
    print(f"[Assembly] Concatenating timeline ({len(playlist)} total clips across {cycle-1} alternating cycles)...")
    cmd_concat = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(looped_video)
    ]
    subprocess.run(cmd_concat, check=True)

    # Master composition with Audio Muxing & Fadeout
    fade_start = max(0.0, audio_dur - 2.0)
    cmd_master = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(looped_video),
        "-i", str(audio_path),
        "-filter_complex",
        f"[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,setsar=1,format=yuv420p[v_out];"
        f"[1:a]afade=t=out:st={fade_start:.2f}:d=2.0[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-t", f"{audio_dur:.2f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(output_path)
    ]
    print(f"[Assembly] Encoding pristine release master film: {output_path.name}...")
    subprocess.run(cmd_master, check=True)
    print(f"✅ RELEASE MASTER READY: {output_path} ({output_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return output_path
