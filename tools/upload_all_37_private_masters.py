#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/upload_all_37_private_masters.py
Sequentially uploads the 37 existing high-quality cinematic master films from renders/releases
to YouTube as PRIVATE drafts on Guru Kula Desam (@guru-kula-desam), inserting them into
Master Playlist PLW7qBZp_Q8Ro and rotating through the quota pool automatically.
"""

import os
import sys
import re
import json
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.quota_rotator import get_next_available_youtube_service, mark_project_exhausted
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

RENDERS_DIR = ROOT / "renders" / "releases"
MANIFEST_FILE = ROOT / "production" / "metadata" / "thirukkural_133_youtube_manifest.json"
REGISTRY_FILE = ROOT / "production" / "youtube_uploaded_private_masters.json"
PLAYLIST_ID = "PLW7qBZp_Q8Ro"

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
    if REGISTRY_FILE.exists():
        try:
            return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_registry(reg):
    REGISTRY_FILE.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")

def upload_single_video(ch_num, video_path, manifest_item):
    title = manifest_item.get("title", f"திருக்குறள்: அதிகாரம் {ch_num} | Cinematic Devotional Film")
    description = manifest_item.get("description", f"திருக்குறள் — அதிகாரம் {ch_num}\nவள்ளுவர் வாய்மொழி\nGuru Kula Desam")
    tags = manifest_item.get("tags", ["திருக்குறள்", "Thirukkural", f"அதிகாரம் {ch_num}", "Guru Kula Desam"])

    body = {
        "snippet": {
            "title": title[:95],
            "description": description,
            "tags": tags[:15],
            "categoryId": "27"  # Education
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False
        }
    }

    max_rotations = 10
    rotations = 0

    while rotations < max_rotations:
        try:
            youtube, project_id = get_next_available_youtube_service()
        except Exception as e:
            print(f"  [ERROR] No available YouTube projects in quota pool: {e}")
            return None

        print(f"\n[{project_id}] Uploading Chapter {ch_num}: {title[:60]}... (PRIVATE)")
        print(f"  Video: {video_path.name} ({video_path.stat().st_size / 1e6:.1f} MB)")

        media = MediaFileUpload(str(video_path), chunksize=10 * 1024 * 1024, resumable=True)
        req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        retries = 0
        quota_hit = False

        while response is None:
            try:
                status, response = req.next_chunk()
                if status:
                    pct = int(status.progress() * 100)
                    print(f"  > [{project_id}] Chapter {ch_num} Upload: {pct}%", flush=True)
                retries = 0
            except HttpError as e:
                if "quotaExceeded" in str(e):
                    print(f"  [QUOTA LIMIT] Project {project_id} hit quota. Rotating to next project...")
                    mark_project_exhausted(project_id)
                    quota_hit = True
                    break
                elif e.resp.status in [500, 502, 503, 504]:
                    retries += 1
                    if retries > 5:
                        print(f"  [RETRY FAIL] Server error {e.resp.status}")
                        break
                    time.sleep(2 ** retries)
                else:
                    print(f"  [HTTP ERROR] {e}")
                    raise

            except Exception as e:
                print(f"  [EXCEPTION] {e}")
                time.sleep(5)
                break

        if quota_hit:
            rotations += 1
            continue

        if response and "id" in response:
            video_id = response["id"]
            print(f"✔ [UPLOAD SUCCESS] Chapter {ch_num} Video ID: {video_id} (https://youtu.be/{video_id})")

            # Add to Master Playlist
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
                print(f"✔ [PLAYLIST] Added {video_id} to playlist {PLAYLIST_ID}")
            except Exception as pe:
                print(f"  [PLAYLIST NOTE] {pe}")

            # Record in registry
            reg = load_registry()
            reg[str(ch_num)] = {
                "chapter": ch_num,
                "video_id": video_id,
                "title": title,
                "file_name": video_path.name,
                "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "privacy": "private"
            }
            save_registry(reg)
            return video_id
        else:
            print(f"  [RETRYING] Upload failed for Chapter {ch_num}, trying next project...")
            rotations += 1

    print(f"❌ Failed to upload Chapter {ch_num} after {max_rotations} rotations.")
    return None

def main():
    chapters_map = get_37_chapters_map()
    manifest_map = load_manifest()
    registry = load_registry()

    print(f"=== GURU KULA DESAM: 37 CURATED MASTER FILMS UPLOADER ===")
    print(f"Total Available Masters: {len(chapters_map)}")
    print(f"Already Uploaded: {len(registry)} ({list(registry.keys())})")

    remaining_chapters = [ch for ch in sorted(chapters_map.keys()) if str(ch) not in registry]
    print(f"Chapters To Upload ({len(remaining_chapters)}): {remaining_chapters}\n")

    success_count = 0
    for ch in remaining_chapters:
        vpath = chapters_map[ch]
        mitem = manifest_map.get(ch, {})
        vid = upload_single_video(ch, vpath, mitem)
        if vid:
            success_count += 1
            print(f"--- Sleeping 3s before next upload ---\n")
            time.sleep(3)
        else:
            print(f"Halting sequence due to upload failure on Chapter {ch}.")
            break

    print(f"\n=== UPLOAD SUMMARY ===")
    print(f"Successfully uploaded: {success_count} chapters")
    print(f"Total recorded in registry: {len(load_registry())}")

if __name__ == "__main__":
    main()
