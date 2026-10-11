#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/retire_3scene_videos.py
Retires legacy 3-scene master films on YouTube to 'unlisted' (or 'private')
and enqueues them for complete cinematic reconstruction with 18–20 diverse scenes.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REGISTRY_FILE = ROOT / "production" / "youtube_published_registry.json"
MANIFEST_FILE = ROOT / "production" / "autonomous_master_production_manifest.json"
REBUILD_QUEUE_FILE = ROOT / "production" / "rebuild_queue.json"
FLOW_RENDERS_DIR = ROOT / "production" / "google_flow_renders"

def get_3scene_published_videos() -> list:
    if not REGISTRY_FILE.exists():
        return []

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Compile all published videos
    candidates = {}
    for t in manifest.get("completed_tracks", []):
        yid = t.get("youtube_id")
        tid = t.get("track_id")
        if yid and tid:
            candidates[yid] = {
                "youtube_id": yid,
                "track_id": tid,
                "title": t.get("title", ""),
                "category": t.get("category", "thirukkural")
            }

    for k, v in registry.items():
        yid = v.get("youtube_id")
        tid = v.get("track_id")
        if yid and tid:
            if yid not in candidates:
                candidates[yid] = {
                    "youtube_id": yid,
                    "track_id": tid,
                    "title": v.get("title", ""),
                    "category": v.get("category", "thirukkural")
                }

    # Filter for <= 4 clips (the 3-scene loop)
    three_scene_list = []
    for yid, info in candidates.items():
        tid = info["track_id"]
        clip_dir = FLOW_RENDERS_DIR / tid
        clip_count = len(list(clip_dir.glob("*.mp4"))) if clip_dir.exists() else 0
        # If <= 4 clips in flow renders, it was built using the 3-scene loop
        if clip_count <= 4:
            info["clip_count"] = clip_count
            three_scene_list.append(info)

    return three_scene_list

def retire_videos(privacy: str = "unlisted", limit: int = None):
    from tools.quota_rotator import get_next_available_youtube_service

    targets = get_3scene_published_videos()
    print("=" * 80)
    print("GURU KULA DESAM — RETIRING 3-SCENE VIDEOS ON YOUTUBE")
    print(f"Target Privacy: {privacy.upper()} | Found {len(targets)} candidates to retire")
    print("=" * 80)

    rebuild_queue = []
    if REBUILD_QUEUE_FILE.exists():
        try:
            with open(REBUILD_QUEUE_FILE, "r", encoding="utf-8") as f:
                rebuild_queue = json.load(f)
        except Exception:
            pass

    rebuild_ids = {item.get("track_id") for item in rebuild_queue}

    retired_count = 0
    yt, cur_project = get_next_available_youtube_service()

    for idx, t in enumerate(targets, 1):
        if limit and retired_count >= limit:
            print(f"[Retire] Target limit of {limit} reached.")
            break

        yid = t["youtube_id"]
        tid = t["track_id"]
        title = t.get("title", "")

        try:
            # Check current status
            res = yt.videos().list(id=yid, part="status,snippet").execute()
            items = res.get("items", [])
            if not items:
                print(f"[{idx}/{len(targets)}] {yid} ({tid}): Not found on channel. Skipping.")
                continue

            cur = items[0]
            cur_privacy = cur["status"]["privacyStatus"]
            if cur_privacy == privacy:
                print(f"[{idx}/{len(targets)}] {yid} ({tid}): Already {privacy}. Enqueueing rebuild.")
            else:
                print(f"[{idx}/{len(targets)}] Updating {yid} ({title[:35]}...) from {cur_privacy} -> {privacy}...")
                yt.videos().update(
                    part="status,snippet",
                    body={
                        "id": yid,
                        "status": {
                            "privacyStatus": privacy,
                            "selfDeclaredMadeForKids": cur["status"].get("selfDeclaredMadeForKids", False)
                        },
                        "snippet": {
                            "title": cur["snippet"]["title"],
                            "categoryId": cur["snippet"].get("categoryId", "27")
                        }
                    }
                ).execute()
                retired_count += 1
                print(f"  [SUCCESS] Set https://youtu.be/{yid} to {privacy.upper()}")

            # Add to rebuild queue
            if tid not in rebuild_ids:
                rebuild_queue.append({
                    "track_id": tid,
                    "old_youtube_id": yid,
                    "title": title,
                    "category": t.get("category", "thirukkural"),
                    "status": "QUEUED_FOR_18SCENE_REBUILD",
                    "retired_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")
                })
                rebuild_ids.add(tid)

            time.sleep(1)

        except Exception as e:
            err_str = str(e)
            from tools.quota_rotator import mark_project_exhausted, get_next_available_youtube_service
            if any(k in err_str for k in ["quotaExceeded", "rateLimitExceeded", "429"]):
                print(f"  [Project {cur_project} Quota Exhausted]. Rotating to next project...")
                mark_project_exhausted(cur_project)
                yt, cur_project = get_next_available_youtube_service()
            else:
                print(f"  [Error updating {yid}]: {e}")

    # Save rebuild queue
    with open(REBUILD_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(rebuild_queue, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"COMPLETED. Set {retired_count} videos to {privacy.upper()}.")
    print(f"Enqueued {len(rebuild_queue)} tracks for 18–20 scene rebuild in {REBUILD_QUEUE_FILE.name}")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retire 3-scene videos on YouTube and queue for rebuild")
    parser.add_argument("--privacy", choices=["unlisted", "private"], default="unlisted", help="Target privacy status")
    parser.add_argument("--limit", type=int, default=None, help="Maximum videos to update")
    args = parser.parse_args()

    retire_videos(privacy=args.privacy, limit=args.limit)
