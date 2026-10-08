#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam (@guru-kula-desam)
YouTube Live Description Sync Utility
====================================
Synchronizes enriched video descriptions (with authentic Tamil lyrics, English meanings,
scripture attributions, and production credits) live to YouTube via the YouTube Data API v3.

Uses credentials from:
- data/credentials/token.json
- data/credentials/client_secrets.json

Features:
- Dry-run mode by default (safe preview)
- Batch update with quota limits and graceful quota error handling
- Single video targeting via --video-id
- Automatic token refresh
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_DIR = ROOT_DIR / "data" / "credentials"
TOKEN_PATH = CREDENTIALS_DIR / "token.json"
CLIENT_SECRETS_PATH = CREDENTIALS_DIR / "client_secrets.json"
ENRICHED_DB_PATH = ROOT_DIR / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    """Authenticates and returns the YouTube Data API v3 client."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Token file not found at {TOKEN_PATH}")

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[Auth] Refreshing expired YouTube OAuth token...")
            creds.refresh(Request())
            with open(TOKEN_PATH, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
            print("[Auth] Token refreshed and saved.")
        else:
            if not CLIENT_SECRETS_PATH.exists():
                raise FileNotFoundError(f"OAuth client secrets file not found at {CLIENT_SECRETS_PATH}")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, "w", encoding="utf-8") as f:
                f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def sync_descriptions(dry_run=True, limit=None, target_video_id=None, force=False):
    if not ENRICHED_DB_PATH.exists():
        print(f"[Error] Enriched database not found at {ENRICHED_DB_PATH}")
        print("Please run tools/enrich_lyrics_and_descriptions.py first.")
        sys.exit(1)

    with open(ENRICHED_DB_PATH, "r", encoding="utf-8") as f:
        enriched_db = json.load(f)

    with open(ROOT_DIR / "live_youtube_metadata.json", "r", encoding="utf-8") as f:
        live_yt = json.load(f)

    # Filter items
    items_to_sync = []
    if target_video_id:
        if target_video_id in enriched_db:
            items_to_sync.append((target_video_id, enriched_db[target_video_id]))
        else:
            print(f"[Error] Video ID {target_video_id} not found in enriched database.")
            sys.exit(1)
    else:
        for vid_id, data in enriched_db.items():
            items_to_sync.append((vid_id, data))

    if limit and limit > 0:
        items_to_sync = items_to_sync[:limit]

    print("=" * 80)
    print(f"YOUTUBE DESCRIPTION SYNC — {'DRY RUN (Preview)' if dry_run else 'LIVE EXECUTION'}")
    print("=" * 80)
    print(f"Total videos identified for sync: {len(items_to_sync)}")

    if dry_run:
        for i, (vid_id, data) in enumerate(items_to_sync[:5], 1):
            title = data.get("title", "")
            print(f"\n[{i}/{len(items_to_sync)}] DRY RUN PREVIEW: {vid_id} — {title}")
            print(f"Scripture: {data.get('scripture')} | Author: {data.get('author')}")
            print(f"Hashtags: {data.get('hashtags')}")
            print("Description Snippet (first 400 chars):")
            print("-" * 50)
            print(data.get("description", "")[:400] + "...")
            print("-" * 50)
        if len(items_to_sync) > 5:
            print(f"\n... and {len(items_to_sync) - 5} more videos queued for update.")
        print("\nDry run completed successfully. Run with --live to push updates to YouTube.")
        return

    # Live update mode
    print("\nConnecting to YouTube Data API...")
    youtube = get_authenticated_service()
    print("Authentication established successfully.\n")

    updated_count = 0
    skipped_count = 0
    failed_count = 0

    for i, (vid_id, data) in enumerate(items_to_sync, 1):
        title = data.get("title", "")
        new_desc = data.get("description", "")
        print(f"[{i}/{len(items_to_sync)}] Processing {vid_id}: '{title[:45]}...'")

        try:
            # 1. Fetch live snippet
            resp = youtube.videos().list(part="snippet", id=vid_id).execute()
            items = resp.get("items", [])
            if not items:
                print(f"  [Warning] Video {vid_id} not found on YouTube. Skipping.")
                skipped_count += 1
                continue

            snippet = items[0]["snippet"]
            cur_desc = snippet.get("description", "")

            # Avoid redundant updates if description is already enriched
            if cur_desc.strip() == new_desc.strip():
                print(f"  [Info] Description already up-to-date. Skipping.")
                skipped_count += 1
                continue

            # 2. Update snippet description
            snippet["description"] = new_desc

            # Keep categoryId, tags, title intact
            update_body = {
                "id": vid_id,
                "snippet": snippet
            }
            youtube.videos().update(part="snippet", body=update_body).execute()
            print(f"  [Success] Description updated live on YouTube!")
            updated_count += 1

            # Brief pause to respect API rate limits
            time.sleep(1.0)

        except Exception as e:
            err_str = str(e)
            if "quotaExceeded" in err_str:
                print(f"\n[QUOTA REACHED] YouTube Data API daily quota limit reached.")
                print(f"Successfully updated {updated_count} videos before quota exhaustion.")
                print(f"Quota resets at midnight Pacific Time. Resume with --limit or scheduled sync.")
                break
            else:
                print(f"  [Error] Failed to update {vid_id}: {e}")
                failed_count += 1

    print("\n" + "=" * 80)
    print("SYNC SUMMARY")
    print(f"Updated live : {updated_count}")
    print(f"Skipped      : {skipped_count}")
    print(f"Failed       : {failed_count}")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Sync enriched descriptions to live YouTube videos.")
    parser.add_argument("--live", action="store_true", help="Execute live updates to YouTube (default is dry-run)")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of videos to update")
    parser.add_argument("--video-id", type=str, default=None, help="Update a specific video ID")
    parser.add_argument("--force", action="store_true", help="Force update even if description looks already enriched")

    args = parser.parse_args()
    sync_descriptions(
        dry_run=not args.live,
        limit=args.limit,
        target_video_id=args.video_id,
        force=args.force
    )

if __name__ == "__main__":
    main()
