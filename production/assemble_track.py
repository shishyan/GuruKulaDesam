#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assembles master film for any track using available cached scenes."""

import sys
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import parse_blueprint, ensure_audio, build_master_film, RENDERS_DIR, FLOW_RENDERS_DIR, PROMPTS_DIR

def assemble(track_id: str):
    matches = list(PROMPTS_DIR.glob(f"**/{track_id}*.md"))
    if not matches:
        print(f"Error: No blueprint found for track {track_id}", flush=True)
        return False
    
    bp = parse_blueprint(matches[0])
    track_dir = FLOW_RENDERS_DIR / bp["track_id"]
    existing_clips = sorted(track_dir.glob("scene_*.mp4"))
    if not existing_clips:
        print(f"Error: No scenes found in {track_dir}", flush=True)
        return False

    print(f"\n[Assembly] Found {len(existing_clips)} scenes for {bp['track_id']} ({bp['title']})", flush=True)
    audio_path = ensure_audio(bp["track_id"])
    out_film = RENDERS_DIR / f"{bp['category'].lower()}_{bp['track_id']}_master.mp4"
    build_master_film(bp, existing_clips, audio_path, out_film)
    print(f"\n[Master Film Complete] Output: {out_film} ({out_film.stat().st_size} bytes)", flush=True)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("track_id", help="Track ID to assemble")
    args = parser.parse_args()
    assemble(args.track_id)
