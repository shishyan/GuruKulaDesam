#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_natha_vinthugal_master.py
Re-assembles the master film for Natha Vinthugal (nuSx1NgiCuo)
with the authentic 'Naadha Vindhu Kalaadhi Namo Nama' lyrics burned into the lower third.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import build_master_film

def main():
    track_id = "nuSx1NgiCuo"
    track_info = {
        "track_id": track_id,
        "title": "திருப்புகழ்: நாத விந்துகள் (பழனி) | Thiruppugazh: Naatha Vindhugal [Film]",
        "category": "murugan"
    }

    render_dir = ROOT / "production" / "google_flow_renders" / track_id
    scene_clips = sorted(list(render_dir.glob("scene_*.mp4")))
    audio_path = ROOT / "source" / "youtube" / f"{track_id}.m4a"
    out_path = ROOT / "renders" / "releases" / f"murugan_{track_id}_master.mp4"

    print(f"Re-assembling {track_info['title']}...")
    print(f"Scene clips found: {len(scene_clips)}")
    print(f"Audio path: {audio_path}")
    print(f"Target output: {out_path}")

    # Remove old master if exists so build_master_film creates a fresh one
    if out_path.exists():
        out_path.unlink()
        print(f"Removed previous outdated master film: {out_path}")

    result = build_master_film(track_info, scene_clips, audio_path, out_path)
    print(f"\nSUCCESS! Master film re-assembled: {result} ({result.stat().st_size / 1024 / 1024:.2f} MB)")

if __name__ == "__main__":
    main()
