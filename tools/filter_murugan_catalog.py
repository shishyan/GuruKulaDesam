#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filters Lord Murugar catalog into:
1. Active Queue: Duration <= 8 minutes (480 seconds)
2. Backlog: Duration > 8 minutes (put on hold for future)
"""

import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "production" / "google_flow_prompts" / "murugan"
AUDIO_DIR = ROOT / "source" / "youtube"
BACKLOG_FILE = ROOT / "production" / "murugan_long_songs_backlog.json"
ACTIVE_QUEUE_FILE = ROOT / "production" / "murugan_active_queue_under_8min.json"
PUBLISHED_MANIFEST = ROOT / "production" / "murugan_published_manifest.json"

published_tids = set()
if PUBLISHED_MANIFEST.exists():
    with open(PUBLISHED_MANIFEST, "r", encoding="utf-8") as f:
        pub = json.load(f)
        for r in pub.get("releases", []):
            if r.get("status") == "PUBLISHED":
                published_tids.add(r.get("track_id"))

live_yt = {}
if (ROOT / "live_youtube_metadata.json").exists():
    with open(ROOT / "live_youtube_metadata.json", "r", encoding="utf-8") as f:
        live_yt = json.load(f)

active_queue = []
backlog = []

for md in sorted(PROMPTS_DIR.glob("*.md")):
    tid = md.stem.split("_")[0]
    audio = AUDIO_DIR / f"{tid}.m4a"
    dur = 0.0
    if audio.exists():
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
            capture_output=True, text=True
        )
        try:
            dur = float(res.stdout.strip())
        except Exception:
            dur = 0.0

    meta = live_yt.get(tid, {})
    title = meta.get("title", md.stem)
    is_published = tid in published_tids

    item = {
        "track_id": tid,
        "title": title,
        "duration_sec": round(dur, 2),
        "duration_min": round(dur / 60, 2),
        "blueprint": str(md.relative_to(ROOT)),
        "published": is_published
    }

    if dur > 480:
        backlog.append(item)
    else:
        active_queue.append(item)

# Save backlog
with open(BACKLOG_FILE, "w", encoding="utf-8") as f:
    json.dump({"total": len(backlog), "max_duration_cutoff_sec": 480, "tracks": backlog}, f, indent=2, ensure_ascii=False)

# Save active queue
with open(ACTIVE_QUEUE_FILE, "w", encoding="utf-8") as f:
    json.dump({"total": len(active_queue), "max_duration_cutoff_sec": 480, "tracks": active_queue}, f, indent=2, ensure_ascii=False)

print(f"=== LORD MURUGAR CATALOG DURATION AUDIT (8-MINUTE CUTOFF) ===")
print(f"Active Queue (<= 8 minutes): {len(active_queue)} tracks (saved to {ACTIVE_QUEUE_FILE.name})")
print(f"Backlog (> 8 minutes):       {len(backlog)} tracks (saved to {BACKLOG_FILE.name})")
print("\n--- ACTIVE QUEUE (READY FOR FAST PRODUCTION) ---")
for x in active_queue:
    pub_flag = "✓ Published" if x["published"] else "○ PENDING"
    print(f"  [{x['duration_min']:>5.2f}m / {x['duration_sec']:>6.1f}s] [{pub_flag}] {x['track_id']} : {x['title'][:55]}")

print("\n--- BACKLOG (LONG CHANTS POSTPONED FOR FUTURE) ---")
for x in backlog:
    pub_flag = "✓ Published" if x["published"] else "○ ON HOLD"
    print(f"  [{x['duration_min']:>5.2f}m / {x['duration_sec']:>6.1f}s] [{pub_flag}] {x['track_id']} : {x['title'][:55]}")

