# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Continuous Google Flow Batch Production Supervisor
Iterates through all pending tracks across categories, generating native
Veo 3.1 AI scenes and assembling master release films.
"""

import sys
import json
import time
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import process_blueprint, RENDERS_DIR, FLOW_RENDERS_DIR
MANIFEST_PATH = ROOT / "production" / "pending_google_flow_manifest.json"

CATEGORIES_ORDER = [
    "vinayagar",
    "murugan",
    "amman",
    "shiva",
    "vallalar_cultural",
    "vishnu_krishna",
    "thirukkural"
]

def main():
    print("=" * 80)
    print("STARTING CONTINUOUS GOOGLE FLOW BATCH PRODUCTION")
    print("=" * 80)
    
    if not MANIFEST_PATH.exists():
        print(f"Error: Manifest {MANIFEST_PATH} not found.")
        return
        
    manifest = json.load(open(MANIFEST_PATH, encoding="utf-8"))
    ready_tracks = manifest.get("ready_to_generate", [])
    
    # Sort by priority order
    def get_sort_key(t):
        cat = t.get("category", "").lower()
        if cat in CATEGORIES_ORDER:
            return (CATEGORIES_ORDER.index(cat), t.get("video_id", ""))
        return (len(CATEGORIES_ORDER), t.get("video_id", ""))

    sorted_tracks = sorted(ready_tracks, key=get_sort_key)
    print(f"Total tracks queued for Google Flow generation: {len(sorted_tracks)}\n")

    completed = 0
    skipped = 0

    for i, t in enumerate(sorted_tracks, 1):
        tid = t["video_id"]
        title = t["title"]
        cat = t["category"]
        bp_path = ROOT / t["blueprint_file"]

        if not bp_path.exists():
            print(f"[{i}/{len(sorted_tracks)}] Skipping {tid} - Blueprint not found: {bp_path.name}")
            continue

        # Check if already rendered
        existing_masters = list(RENDERS_DIR.glob(f"*{tid}*.mp4"))
        if existing_masters and existing_masters[0].stat().st_size > 5_000_000:
            print(f"[{i}/{len(sorted_tracks)}] [Already Done] {cat.upper()} | {tid}: {existing_masters[0].name} ({existing_masters[0].stat().st_size / 1024 / 1024:.2f} MB)")
            skipped += 1
            continue

        print(f"\n[{i}/{len(sorted_tracks)}] >>> PROCESSING {cat.upper()} | {tid} — {title[:40]} <<<")
        try:
            out_film = process_blueprint(bp_path, model="veo-3.1-fast-generate-preview", duration=6)
            print(f"[{i}/{len(sorted_tracks)}] SUCCESS: {out_film.name}\n")
            completed += 1
        except Exception as e:
            err_str = str(e)
            if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                print(f"\n[QUOTA REACHED] Veo video generation quota limit reached at track {tid}: {title}")
                print("Halting production queue cleanly. All completed clips and master films are safely preserved.")
                print("Resume batch production at any time by re-running: python production/run_continuous_flow.py\n")
                break
            print(f"[{i}/{len(sorted_tracks)}] ERROR generating {tid}: {e}\n")
            time.sleep(5)

    print("=" * 80)
    print(f"BATCH PRODUCTION COMPLETE! Completed: {completed} | Skipped: {skipped}")
    print("=" * 80)

if __name__ == "__main__":
    main()

