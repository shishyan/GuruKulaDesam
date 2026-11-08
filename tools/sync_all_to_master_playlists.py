#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/sync_all_to_master_playlists.py

Automated utility to sync all Videos and Shorts across Guru Kula Desam's
3 channels into their canonical master playlists:
  - PLW7qBZp_Q8Ro: திருக்குறள் | Thirukkural — Master Collection
  - PLeqSbdtlRtmc: Lord Shiva Songs
  - PLcpX3K7ZFYjM: Lord Murugar Songs
  - PLY1-K1NUPDWg: Lord Vishnu Songs
  - PLHmbyO4GR_2k: Lord Krishnar Songs
  - PLC84A3gANh-s: Lord Vinayagar Songs
  - PLKng43jJe18o: Goddess Amman Songs
  - PLI7Waf6Z6I48: Other Songs
  - PLAjtBRKl_IlI: Discography (Grand Master Playlist)

Usage:
  python tools/sync_all_to_master_playlists.py --dry-run
  python tools/sync_all_to_master_playlists.py --live
  python tools/sync_all_to_master_playlists.py --export-plan
"""

import os
import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parent.parent

PLAYLIST_MAPPING = {
    "thirukkural": {"id": "PLW7qBZp_Q8Ro", "title": "திருக்குறள் | Thirukkural — Master Collection"},
    "shiva": {"id": "PLeqSbdtlRtmc", "title": "Lord Shiva Songs"},
    "murugan": {"id": "PLcpX3K7ZFYjM", "title": "Lord Murugar Songs"},
    "vishnu": {"id": "PLY1-K1NUPDWg", "title": "Lord Vishnu Songs"},
    "krishna": {"id": "PLHmbyO4GR_2k", "title": "Lord Krishnar Songs"},
    "vinayagar": {"id": "PLC84A3gANh-s", "title": "Lord Vinayagar Songs"},
    "amman": {"id": "PLKng43jJe18o", "title": "Goddess Amman Songs"},
    "other": {"id": "PLI7Waf6Z6I48", "title": "Other Songs"},
    "discography": {"id": "PLAjtBRKl_IlI", "title": "Discography (Grand Master)"},
}

DISCOGRAPHY_ID = "PLAjtBRKl_IlI"

def load_data():
    playlists_backup_file = ROOT / "production" / "youtube_backup" / "playlists.json"
    catalog_file = ROOT / "assets" / "data" / "catalog.json"
    shorts_reg_file = ROOT / "production" / "shorts_metadata" / "gurukuladesam2_published_registry.json"
    live_meta_file = ROOT / "live_youtube_metadata.json"

    playlists_data = {}
    if playlists_backup_file.exists():
        with open(playlists_backup_file, "r", encoding="utf-8") as f:
            playlists_data = json.load(f)

    catalog_data = {}
    if catalog_file.exists():
        with open(catalog_file, "r", encoding="utf-8") as f:
            catalog_data = json.load(f)

    shorts_data = {}
    if shorts_reg_file.exists():
        with open(shorts_reg_file, "r", encoding="utf-8") as f:
            shorts_data = json.load(f).get("published_shorts", {})

    live_meta = {}
    if live_meta_file.exists():
        with open(live_meta_file, "r", encoding="utf-8") as f:
            live_meta = json.load(f)

    return playlists_data, catalog_data, shorts_data, live_meta


def build_playlist_sync_plan():
    playlists_data, catalog_data, shorts_data, live_meta = load_data()
    
    current_items_by_pl = {pid: set(vids) for pid, vids in playlists_data.get("items", {}).items()}

    plan = []

    # 1. Map Shorts from registry
    for track_key, short_item in shorts_data.items():
        sid = short_item.get("youtube_short_id")
        if not sid:
            continue
        title = short_item.get("title", "")
        deity = short_item.get("deity", "other").lower()

        if deity in PLAYLIST_MAPPING:
            target_pl_key = deity
        elif "kural" in deity or "thirukkural" in deity:
            target_pl_key = "thirukkural"
        elif "krishn" in deity:
            target_pl_key = "krishna"
        elif "vishnu" in deity:
            target_pl_key = "vishnu"
        elif "shiva" in deity:
            target_pl_key = "shiva"
        elif "murug" in deity:
            target_pl_key = "murugan"
        elif "vinayag" in deity or "ganesh" in deity:
            target_pl_key = "vinayagar"
        elif "amman" in deity:
            target_pl_key = "amman"
        else:
            target_pl_key = "other"

        target_pl_id = PLAYLIST_MAPPING[target_pl_key]["id"]
        target_pl_title = PLAYLIST_MAPPING[target_pl_key]["title"]

        # Category Playlist
        if sid not in current_items_by_pl.get(target_pl_id, set()):
            plan.append({
                "video_id": sid,
                "title": title,
                "type": "Short",
                "channel": short_item.get("channel_handle", "@GuruKulaDesam2"),
                "playlist_id": target_pl_id,
                "playlist_title": target_pl_title,
                "category": target_pl_key
            })

        # Discography
        if sid not in current_items_by_pl.get(DISCOGRAPHY_ID, set()):
            plan.append({
                "video_id": sid,
                "title": title,
                "type": "Short",
                "channel": short_item.get("channel_handle", "@GuruKulaDesam2"),
                "playlist_id": DISCOGRAPHY_ID,
                "playlist_title": PLAYLIST_MAPPING["discography"]["title"],
                "category": "discography"
            })

    # 2. Map Catalog Videos
    for cat_name, items in catalog_data.items():
        if not isinstance(items, list):
            continue
        
        if "thirukkural" in cat_name:
            c_key = "thirukkural"
        elif "shiva" in cat_name:
            c_key = "shiva"
        elif "murugan" in cat_name:
            c_key = "murugan"
        elif "vishnu" in cat_name:
            c_key = "vishnu"
        elif "vinayagar" in cat_name:
            c_key = "vinayagar"
        elif "amman" in cat_name:
            c_key = "amman"
        else:
            c_key = "other"

        target_pl_id = PLAYLIST_MAPPING[c_key]["id"]
        target_pl_title = PLAYLIST_MAPPING[c_key]["title"]

        for item in items:
            vid = item.get("id")
            if not vid:
                continue
            title = item.get("title", "")
            
            # Category Playlist
            if vid not in current_items_by_pl.get(target_pl_id, set()):
                plan.append({
                    "video_id": vid,
                    "title": title,
                    "type": "Video",
                    "channel": "@guru-kula-desam",
                    "playlist_id": target_pl_id,
                    "playlist_title": target_pl_title,
                    "category": c_key
                })

            # Discography
            if vid not in current_items_by_pl.get(DISCOGRAPHY_ID, set()):
                plan.append({
                    "video_id": vid,
                    "title": title,
                    "type": "Video",
                    "channel": "@guru-kula-desam",
                    "playlist_id": DISCOGRAPHY_ID,
                    "playlist_title": PLAYLIST_MAPPING["discography"]["title"],
                    "category": "discography"
                })

    # Deduplicate plan items
    deduped = []
    seen = set()
    for item in plan:
        k = (item["video_id"], item["playlist_id"])
        if k not in seen:
            seen.add(k)
            deduped.append(item)

    return deduped, current_items_by_pl


def export_plan_report(plan):
    out_file = ROOT / "production" / "master_playlist_sync_plan.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    print(f"✅ Full sync plan exported to: {out_file}")


def get_authenticated_service(token_env_var="GURU_KULA_DESAM_FLAGSHIP_OAUTH_TOKEN"):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    token_json_str = os.environ.get(token_env_var)
    local_token_path = ROOT / "data" / "credentials" / "token.json"

    creds = None
    if token_json_str:
        token_data = json.loads(token_json_str)
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    elif local_token_path.exists():
        creds = Credentials.from_authorized_user_file(str(local_token_path), SCOPES)

    if not creds:
        raise ValueError(f"No valid credentials found in {token_env_var} or {local_token_path}")

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("youtube", "v3", credentials=creds)


def execute_live_sync(plan):
    print("🔑 Authenticating with YouTube Data API...")
    youtube = get_authenticated_service()
    print("✅ Authenticated successfully!\n")

    total = len(plan)
    success = 0
    errors = 0

    print(f"Executing insertion of {total} items into master playlists...\n")

    for i, item in enumerate(plan, 1):
        vid = item["video_id"]
        pid = item["playlist_id"]
        title = item["title"][:40]
        pl_title = item["playlist_title"]

        print(f"[{i}/{total}] Adding {item['type']} {vid} ('{title}') -> {pl_title}...", end=" ", flush=True)

        body = {
            "snippet": {
                "playlistId": pid,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": vid
                }
            }
        }

        try:
            youtube.playlistItems().insert(part="snippet", body=body).execute()
            print("DONE ✅")
            success += 1
        except Exception as e:
            err_msg = str(e)
            if "videoAlreadyInPlaylist" in err_msg:
                print("ALREADY PRESENT ⏩")
                success += 1
            elif "quotaExceeded" in err_msg:
                print(f"\n❌ YouTube Quota Exceeded! Exiting at item {i}.")
                break
            else:
                print(f"FAILED ❌ ({err_msg})")
                errors += 1

    print("\n" + "=" * 60)
    print(f"SYNC SUMMARY: {success} succeeded / already present, {errors} errors out of {total} items.")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Sync videos & shorts to master playlists")
    parser.add_argument("--dry-run", action="store_true", help="Print summary of playlist additions without modifying YouTube")
    parser.add_argument("--live", action="store_true", help="Execute live playlist insertions via YouTube Data API")
    parser.add_argument("--export-plan", action="store_true", help="Export full plan to JSON file")
    args = parser.parse_args()

    plan, current_items = build_playlist_sync_plan()

    # Calculate statistics
    by_playlist = {}
    by_type = {}
    for item in plan:
        pid = item["playlist_id"]
        pt = item["playlist_title"]
        by_playlist[pt] = by_playlist.get(pt, 0) + 1
        
        t = item["type"]
        by_type[t] = by_type.get(t, 0) + 1

    print("=" * 80)
    print("GURU KULA DESAM — MASTER PLAYLIST SYNC AUDIT")
    print("=" * 80)
    print(f"Total New Additions Identified: {len(plan)}")
    print(f"  - YouTube Shorts to Add:     {by_type.get('Short', 0)}")
    print(f"  - Long-form Videos to Add:   {by_type.get('Video', 0)}")
    print("\n--- Additions by Target Playlist ---")
    for pl_title, count in sorted(by_playlist.items(), key=lambda x: -x[1]):
        print(f"  • {pl_title:<55} : +{count} items")
    print("=" * 80)

    if args.export_plan or not args.live:
        export_plan_report(plan)

    if args.live:
        execute_live_sync(plan)
    else:
        print("\nRun with '--live' (or trigger the GitHub Actions workflow) to apply these updates live to YouTube.")


if __name__ == "__main__":
    main()
