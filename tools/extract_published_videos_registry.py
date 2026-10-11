#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_published_videos_registry.py
Scans:
1. live_youtube_metadata.json (channel's live catalog)
2. All task logs in .system_generated/tasks
3. Manifests (autonomous_master_production_manifest.json, vinayagar_published_manifest.json)
to build an authoritative, permanent, ironclad registry of all YouTube video IDs,
track IDs, and titles that exist on YouTube to guarantee ZERO DUPLICATE UPLOADS.
"""

import os
import sys
import re
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "production" / "youtube_published_registry.json"
MANIFEST_FILE = ROOT / "production" / "autonomous_master_production_manifest.json"
LIVE_METADATA_FILE = ROOT / "live_youtube_metadata.json"
VINAYAGAR_MANIFEST = ROOT / "production" / "vinayagar_published_manifest.json"

LOG_DIR = Path("C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/.system_generated/tasks")

def main():
    registry = {}
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception:
            registry = {}

    print(f"Existing registry entries: {len(registry)}")

    # 1. Ingest live_youtube_metadata.json (Authoritative live YouTube channel inventory)
    live_added = 0
    if LIVE_METADATA_FILE.exists():
        try:
            with open(LIVE_METADATA_FILE, "r", encoding="utf-8") as f:
                live_meta = json.load(f)
            for vid_id, data in live_meta.items():
                title = data.get("title", "")
                # Key by video_id as well as track_id
                if vid_id not in registry:
                    registry[vid_id] = {
                        "track_id": vid_id,
                        "youtube_id": vid_id,
                        "youtube_url": f"https://youtu.be/{vid_id}",
                        "title": title,
                        "source": "live_youtube_metadata.json"
                    }
                    live_added += 1
            print(f"Ingested {live_added} videos from live_youtube_metadata.json")
        except Exception as e:
            print(f"Error reading live metadata: {e}")

    # 2. Ingest vinayagar_published_manifest.json if exists
    vin_added = 0
    if VINAYAGAR_MANIFEST.exists():
        try:
            with open(VINAYAGAR_MANIFEST, "r", encoding="utf-8") as f:
                vin_data = json.load(f)
            for item in vin_data:
                tid = item.get("track_id")
                yid = item.get("youtube_id") or tid
                if tid and tid not in registry:
                    registry[tid] = {
                        "track_id": tid,
                        "youtube_id": yid,
                        "youtube_url": f"https://youtu.be/{yid}",
                        "title": item.get("title", ""),
                        "source": "vinayagar_published_manifest.json"
                    }
                    vin_added += 1
            print(f"Ingested {vin_added} videos from vinayagar_published_manifest.json")
        except Exception as e:
            print(f"Error reading vinayagar manifest: {e}")

    # 3. Scan all logs in task directory for [UPLOAD SUCCESS]
    pattern_pub = re.compile(r"PUBLISHING MASTER FILM TO YOUTUBE:\s*(.*?)\s*\((.*?)\)")
    pattern_success = re.compile(r"\[UPLOAD SUCCESS\] New YouTube Video ID:\s*([a-zA-Z0-9_-]{11})")

    found_in_logs = 0
    if LOG_DIR.exists():
        log_files = list(LOG_DIR.glob("*.log"))
        print(f"Scanning {len(log_files)} task log files for upload successes...")
        for log_path in log_files:
            try:
                # Fast check if file contains marker before parsing
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                if "[UPLOAD SUCCESS]" not in content:
                    continue

                current_title = None
                current_tid = None

                for line in content.splitlines():
                    m_pub = pattern_pub.search(line)
                    if m_pub:
                        current_title = m_pub.group(1).strip()
                        current_tid = m_pub.group(2).strip()

                    m_succ = pattern_success.search(line)
                    if m_succ:
                        yid = m_succ.group(1).strip()
                        tid = current_tid or yid
                        if tid not in registry:
                            registry[tid] = {
                                "track_id": tid,
                                "youtube_id": yid,
                                "youtube_url": f"https://youtu.be/{yid}",
                                "title": current_title or "",
                                "source": f"task_log:{log_path.name}"
                            }
                            found_in_logs += 1
                            safe_title = (current_title or "").encode("ascii", errors="replace").decode("ascii")
                            print(f"  [Found in Log] {tid} -> https://youtu.be/{yid} ({safe_title})")
            except Exception as e:
                print(f"Error reading {log_path.name}: {e}")

    print(f"\nTotal authoritative entries in registry: {len(registry)} (New from logs: {found_in_logs})")

    # 4. Sync status into autonomous_master_production_manifest.json
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            synced_count = 0
            for track in manifest.get("completed_tracks", []):
                tid = track.get("track_id")
                if tid in registry:
                    track["status"] = "PUBLISHED"
                    track["youtube_id"] = registry[tid]["youtube_id"]
                    track["published_url"] = registry[tid]["youtube_url"]
                    synced_count += 1

            with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            print(f"Synced {synced_count} published states into {MANIFEST_FILE}")
        except Exception as e:
            print(f"Error syncing manifest: {e}")

    # 5. Save registry
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"Saved authoritative registry to {REGISTRY_FILE}")

if __name__ == "__main__":
    main()
