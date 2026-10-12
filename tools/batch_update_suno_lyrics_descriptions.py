#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/batch_update_suno_lyrics_descriptions.py

Updates YouTube video descriptions by appending exact sung lyrics from Suno
as a dedicated section at the bottom, strictly preserving existing descriptions,
commentary, and chapters.
Uses quota_rotator to rotate across authorized Google Cloud projects.
"""

import os
import sys
import json
import time
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from quota_rotator import get_next_available_youtube_service, mark_project_exhausted
from googleapiclient.errors import HttpError

LOG_FILE = ROOT / "production" / "youtube_backup" / "lyrics_update_log.jsonl"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

HEADER = "\n\n🎵 முழுமையான பாடல் வரிகள் (Full Song Lyrics):\n-------------------------------------------------\n"
MARKER = "🎵 முழுமையான பாடல் வரிகள் (Full Song Lyrics):"

def clean_suno_lyrics(raw_text: str) -> str:
    lines = raw_text.splitlines()
    cleaned = []
    for line in lines:
        l = line.strip()
        if not l:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        # Stop at emoji bar or suno metadata
        if any(emoji in l for emoji in ["🔥", "😍", "😱", "🙌", "👍", "😎", "🥵"]) or "0/500" in l:
            break
        if any(stop in l for stop in ["No comments yet", "Be the first one", "Comments", "More like this"]):
            break
        cleaned.append(l)
    return "\n".join(cleaned).strip()

def append_lyrics(existing_desc: str, lyrics: str) -> str:
    # If already present, don't re-append
    if MARKER in existing_desc:
        return existing_desc

    desc_stripped = existing_desc.strip()
    target_block = HEADER + lyrics.strip()
    
    combined = desc_stripped + target_block
    if len(combined) <= 4950:
        return combined
        
    # If exceeds 4950, compress consecutive blank lines
    compressed_desc = re.sub(r'\n{3,}', '\n\n', desc_stripped)
    compressed_lyrics = re.sub(r'\n{3,}', '\n\n', lyrics.strip())
    combined = compressed_desc + HEADER + compressed_lyrics
    if len(combined) <= 4950:
        return combined

    # If still exceeds 4950, trim lyrics from bottom gracefully
    available = 4950 - len(compressed_desc) - len(HEADER) - 5
    if available > 200:
        trimmed_lyrics = compressed_lyrics[:available].rsplit('\n', 1)[0]
        return compressed_desc + HEADER + trimmed_lyrics
    else:
        # Cannot fit lyrics safely
        return existing_desc

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Preview only without API writes")
    parser.add_argument("--limit", type=int, default=0, help="Max videos to process")
    args = parser.parse_args()

    # Load plan
    plan_file = ROOT / "production" / "owned_lyrics_update_plan.json"
    if not plan_file.exists():
        print(f"Error: {plan_file} not found!")
        sys.exit(1)

    plan = json.load(open(plan_file, encoding="utf-8"))
    print(f"Loaded {len(plan)} targets from plan.")

    # Deduplicate targets by video_id
    seen_vids = set()
    targets = []
    for p in plan:
        vid = p["video_id"]
        if vid not in seen_vids:
            seen_vids.add(vid)
            targets.append(p)

    print(f"Unique target videos: {len(targets)}")
    if args.limit > 0:
        targets = targets[:args.limit]
        print(f"Limiting to first {len(targets)} videos.")

    yt = None
    active_pid = None

    if not args.dry_run:
        yt, active_pid = get_next_available_youtube_service()

    success_count = 0
    skip_count = 0
    fail_count = 0

    for idx, item in enumerate(targets, 1):
        vid = item["video_id"]
        suno_id = item["suno_id"]
        suno_file = ROOT / "production" / "suno_lyrics" / f"{suno_id}.txt"
        
        if not suno_file.exists():
            print(f"[{idx}/{len(targets)}] ⏩ {vid}: Suno file missing ({suno_id})")
            skip_count += 1
            continue

        raw_lyrics = suno_file.read_text(encoding="utf-8").strip()
        cleaned_lyrics = clean_suno_lyrics(raw_lyrics)
        if len(cleaned_lyrics) < 40:
            print(f"[{idx}/{len(targets)}] ⏩ {vid}: Lyrics too short ({len(cleaned_lyrics)} chars)")
            skip_count += 1
            continue

        print(f"\n[{idx}/{len(targets)}] Processing {vid} ({item['title'][:40]})...", flush=True)

        if args.dry_run:
            print(f"  [DRY RUN] Would append {len(cleaned_lyrics)} chars of Suno lyrics to {vid}")
            success_count += 1
            continue

        # Fetch live video details with retry across quota rotation
        updated = False
        attempts = 0
        while not updated and attempts < 6:
            attempts += 1
            try:
                r = yt.videos().list(part="snippet", id=vid).execute()
                items = r.get("items", [])
                if not items:
                    print(f"  ❌ Video {vid} not found on YouTube!")
                    fail_count += 1
                    break

                v_obj = items[0]
                snippet = v_obj["snippet"]
                current_desc = snippet.get("description", "")

                if MARKER in current_desc:
                    print(f"  ⏩ Lyrics section already present! Skipping.")
                    skip_count += 1
                    break

                new_desc = append_lyrics(current_desc, cleaned_lyrics)
                if new_desc == current_desc:
                    print(f"  ⏩ Description could not be updated safely (length limit). Skipping.")
                    skip_count += 1
                    break

                # Prepare snippet update
                update_snippet = {
                    "title": snippet["title"],
                    "categoryId": snippet.get("categoryId", "27"),
                    "description": new_desc
                }
                for opt in ["tags", "defaultLanguage", "defaultAudioLanguage"]:
                    if opt in snippet:
                        update_snippet[opt] = snippet[opt]

                body = {
                    "id": vid,
                    "snippet": update_snippet
                }

                yt.videos().update(part="snippet", body=body).execute()
                print(f"  ✅ SUCCESS: {vid} updated ({len(current_desc)} -> {len(new_desc)} chars)")
                
                # Log success
                log_entry = {
                    "video_id": vid,
                    "title": snippet["title"],
                    "suno_id": suno_id,
                    "old_length": len(current_desc),
                    "new_length": len(new_desc),
                    "project_id": active_pid,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

                success_count += 1
                updated = True
                time.sleep(1) # Gentle throttling

            except HttpError as he:
                status_code = he.resp.status
                error_str = str(he)
                if "quotaExceeded" in error_str or status_code == 403:
                    print(f"  [QUOTA LIMIT] Project {active_pid} exceeded quota. Rotating...")
                    mark_project_exhausted(active_pid)
                    try:
                        yt, active_pid = get_next_available_youtube_service()
                    except Exception as e:
                        print(f"  [ERROR] All projects in quota pool exhausted: {e}")
                        break
                else:
                    print(f"  ❌ HttpError {status_code} on {vid}: {he}")
                    fail_count += 1
                    break
            except Exception as ex:
                print(f"  ❌ Error on {vid}: {ex}")
                fail_count += 1
                break

    print("\n" + "=" * 60)
    print(f"RUN COMPLETE: {success_count} updated, {skip_count} skipped, {fail_count} failed.")
    print("=" * 60)

if __name__ == "__main__":
    main()
