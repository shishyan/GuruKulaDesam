#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_all_masters_clean.py
Re-assembles all available master films with clean cinematic visuals (NO burned lyrics).
Utilizes pre-existing downloaded Veo scene clips and source audio,
applying 75% devotional speed retiming, sacred temple border overlay, and divine drizzle.
"""

import os
import sys
import json
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import build_master_film

MANIFEST_FILE = ROOT / "production" / "autonomous_master_production_manifest.json"
FLOW_RENDERS_DIR = ROOT / "production" / "google_flow_renders"
SOURCE_AUDIO_DIR = ROOT / "source" / "youtube"
RELEASES_DIR = ROOT / "renders" / "releases"

def main():
    if not MANIFEST_FILE.exists():
        print(f"Manifest not found at {MANIFEST_FILE}")
        return

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    tracks = manifest.get("completed_tracks", [])
    print(f"Found {len(tracks)} tracks in manifest.")

    rebuilt_count = 0
    skipped_count = 0
    already_clean_count = 0
    failed_count = 0

    for idx, track in enumerate(tracks, 1):
        tid = track.get("track_id")
        title = track.get("title", tid)
        cat = track.get("category", "devotional")
        master_rel = track.get("master_film")

        if not master_rel:
            skipped_count += 1
            continue

        master_path = ROOT / master_rel
        scene_dir = FLOW_RENDERS_DIR / tid
        scene_clips = sorted(list(scene_dir.glob("scene_*.mp4")))
        audio_path = SOURCE_AUDIO_DIR / f"{tid}.m4a"

        # Check if already rebuilt clean
        if track.get("clean_cinematic") and master_path.exists() and master_path.stat().st_size > 1000000:
            already_clean_count += 1
            print(f"[{idx}/{len(tracks)}] Already Clean: {title} ({tid})")
            continue

        if not scene_clips:
            skipped_count += 1
            continue

        if not audio_path.exists():
            skipped_count += 1
            continue

        print(f"\n[{idx}/{len(tracks)}] Rebuilding Clean Master for: {title} ({tid})")
        print(f"  Category: {cat} | Scenes: {len(scene_clips)} | Audio: {audio_path.name}")

        try:
            if master_path.exists():
                master_path.unlink()

            track_info = {
                "track_id": tid,
                "title": title,
                "category": cat
            }

            t0 = time.time()
            clean_film = build_master_film(track_info, scene_clips, audio_path, master_path)
            dur = time.time() - t0
            size_mb = clean_film.stat().st_size / 1024 / 1024

            track["file_size_mb"] = round(size_mb, 2)
            track["clean_cinematic"] = True
            rebuilt_count += 1
            print(f"  >>> SUCCESS: Clean film built in {dur:.1f}s ({size_mb:.2f} MB)")

            # Save manifest progress after each track
            with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"  >>> ERROR rebuilding {tid}: {e}")
            failed_count += 1

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"REBUILD COMPLETE:")
    print(f"  Newly Rebuilt: {rebuilt_count}")
    print(f"  Already Clean: {already_clean_count}")
    print(f"  Skipped (No local clips): {skipped_count}")
    print(f"  Failed: {failed_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
