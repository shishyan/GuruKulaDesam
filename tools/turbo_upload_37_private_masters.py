#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/turbo_upload_37_private_masters.py
High-throughput multi-threaded parallel YouTube uploader for Guru Kula Desam.
- Uses 3 concurrent worker threads across 5 independent Google Cloud projects
- 64MB chunk streaming for maximum socket throughput (3-5x faster)
- Auto-rotates exhausted projects seamlessly
- Strictly private drafts added to playlist PLW7qBZp_Q8Ro
"""

import os
import sys
import re
import json
import time
import queue
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.quota_rotator import get_next_available_youtube_service, mark_project_exhausted, is_project_exhausted
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

RENDERS_DIR = ROOT / "renders" / "releases"
MANIFEST_FILE = ROOT / "production" / "metadata" / "thirukkural_133_youtube_manifest.json"
REGISTRY_FILE = ROOT / "production" / "youtube_uploaded_private_masters.json"
PLAYLIST_ID = "PLW7qBZp_Q8Ro"

registry_lock = threading.Lock()
rotator_lock = threading.Lock()

def get_37_chapters_map():
    cinematic_37 = {}
    for f in RENDERS_DIR.glob("thirukkural_adhikaram_*_master.mp4"):
        m = re.search(r"adhikaram_(\d+)", f.name)
        if m:
            cinematic_37[int(m.group(1))] = f

    for f in RENDERS_DIR.glob("adhikaram_*_cinematic.mp4"):
        m = re.search(r"adhikaram_(\d+)", f.name)
        if m:
            cinematic_37[int(m.group(1))] = f

    ch3 = RENDERS_DIR / "thirukkural_ch003_cinematic_720p_master.mp4"
    if ch3.exists():
        cinematic_37[3] = ch3

    return cinematic_37

def load_manifest():
    if MANIFEST_FILE.exists():
        data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        return {item["chapter"]: item for item in data}
    return {}

def load_registry():
    with registry_lock:
        if REGISTRY_FILE.exists():
            try:
                return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

def save_registry_entry(ch_num, video_id, title, filename):
    with registry_lock:
        reg = {}
        if REGISTRY_FILE.exists():
            try:
                reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        reg[str(ch_num)] = {
            "chapter": ch_num,
            "video_id": video_id,
            "title": title,
            "file_name": filename,
            "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "privacy": "private"
        }
        REGISTRY_FILE.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")

def upload_worker(ch_num, video_path, manifest_item, thread_name):
    title = manifest_item.get("title", f"திருக்குறள்: அதிகாரம் {ch_num} | Cinematic Devotional Film")
    description = manifest_item.get("description", f"திருக்குறள் — அதிகாரம் {ch_num}\nவள்ளுவர் வாய்மொழி\nGuru Kula Desam")
    tags = manifest_item.get("tags", ["திருக்குறள்", "Thirukkural", f"அதிகாரம் {ch_num}", "Guru Kula Desam"])

    body = {
        "snippet": {
            "title": title[:95],
            "description": description,
            "tags": tags[:15],
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False
        }
    }

    rotations = 0
    while rotations < 8:
        with rotator_lock:
            try:
                youtube, project_id = get_next_available_youtube_service()
            except Exception as e:
                print(f"[{thread_name}] ❌ Quota pool exhausted: {e}")
                return None

        file_size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"[{thread_name} | {project_id}] 🚀 Starting Ch {ch_num:3d} ({file_size_mb:.1f} MB)...")

        # 64 MB chunk size for high-speed socket throughput
        media = MediaFileUpload(str(video_path), chunksize=64 * 1024 * 1024, resumable=True)
        req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        quota_hit = False

        while response is None:
            try:
                status, response = req.next_chunk()
                if status:
                    pct = int(status.progress() * 100)
                    print(f"  > [{thread_name}] Ch {ch_num:3d} Upload: {pct}%", flush=True)
            except HttpError as e:
                if "quotaExceeded" in str(e):
                    print(f"[{thread_name}] ⚠️ Project {project_id} quota exceeded. Rotating...")
                    with rotator_lock:
                        mark_project_exhausted(project_id)
                    quota_hit = True
                    break
                elif e.resp.status in [500, 502, 503, 504]:
                    time.sleep(3)
                else:
                    print(f"[{thread_name}] HTTP Error {e}")
                    raise
            except Exception as e:
                print(f"[{thread_name}] Exception during upload: {e}")
                time.sleep(3)
                break

        if quota_hit:
            rotations += 1
            continue

        if response and "id" in response:
            video_id = response["id"]
            print(f"[{thread_name}] ✔ Ch {ch_num:3d} Uploaded! ID: {video_id} (https://youtu.be/{video_id})")

            # Add to playlist
            try:
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": PLAYLIST_ID,
                            "resourceId": {"kind": "youtube#video", "videoId": video_id}
                        }
                    }
                ).execute()
                print(f"[{thread_name}] ✔ Ch {ch_num:3d} Added to playlist {PLAYLIST_ID}")
            except Exception as pe:
                print(f"[{thread_name}] Playlist note: {pe}")

            save_registry_entry(ch_num, video_id, title, video_path.name)
            return video_id
        else:
            rotations += 1

    print(f"[{thread_name}] ❌ Failed to upload Chapter {ch_num} after retries.")
    return None

def main():
    chapters_map = get_37_chapters_map()
    manifest_map = load_manifest()
    registry = load_registry()

    print("================================================================")
    print("      GURU KULA DESAM — TURBO MULTI-PROJECT YOUTUBE UPLOADER   ")
    print("================================================================")
    print(f"Total Available Masters: {len(chapters_map)}")
    print(f"Already Uploaded: {len(registry)} chapters")

    remaining_chapters = [ch for ch in sorted(chapters_map.keys()) if str(ch) not in registry]
    print(f"Remaining To Upload ({len(remaining_chapters)}): {remaining_chapters}")
    print(f"Launching with 3 Parallel Worker Threads & 64MB Turbo Chunks...\n")

    if not remaining_chapters:
        print("All chapters are already uploaded!")
        return

    # Use ThreadPoolExecutor with 3 workers
    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="Uploader") as executor:
        futures = []
        for idx, ch in enumerate(remaining_chapters):
            vpath = chapters_map[ch]
            mitem = manifest_map.get(ch, {})
            tname = f"Worker-{(idx % 3) + 1}"
            fut = executor.submit(upload_worker, ch, vpath, mitem, tname)
            futures.append((ch, fut))

        for ch, fut in futures:
            try:
                res = fut.result()
                if not res:
                    print(f"Warning: Chapter {ch} returned no video ID.")
            except Exception as e:
                print(f"Error on Chapter {ch}: {e}")

    print("\n================================================================")
    print("                  TURBO UPLOAD BATCH COMPLETE                   ")
    print("================================================================")
    final_reg = load_registry()
    print(f"Total Uploaded Chapters Recorded: {len(final_reg)} / 37")

if __name__ == "__main__":
    main()
