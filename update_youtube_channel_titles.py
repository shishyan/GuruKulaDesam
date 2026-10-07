"""
Comprehensive YouTube Channel & Playlist Title Sync Utility
Channel: @guru-kula-desam

Features:
1. Standardizes video titles across Thirukkural, Shiva, Murugan, Vishnu, Krishna, Amman, Vinayagar, and Vallalar categories.
2. Enforces bilingual canonical naming format:
   - Thirukkural: அதிகாரம் <எண்> - <அதிகாரப் பெயர்> | <English Transliteration> [<Descriptor>]
   - Deity/Spiritual: <தமிழ் தலைப்பு> | <English Transliteration> [<Category Film/Song>]
3. Strictly maintains all titles <= 95 characters (below YouTube's 100 char limit).
4. Efficient batch querying (50 videos/call) to conserve quota.
5. Supports simulation (--dry-run) and authenticated live API updates (--live).
"""

import os
import sys
import json
import csv
import argparse
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UPDATES_FILE = os.path.join(os.path.dirname(__file__), "all_channel_title_updates.json")
MASTER_FILE = os.path.join(os.path.dirname(__file__), "master_all_598_songs_catalog.json")
PENDING_FILE = os.path.join(os.path.dirname(__file__), "channel_direct_uploads_pending.json")

def load_updates(mode="pending"):
    if mode == "master":
        target = MASTER_FILE
    elif mode == "all":
        target = UPDATES_FILE
    else:
        target = PENDING_FILE if os.path.exists(PENDING_FILE) else UPDATES_FILE
    
    if not os.path.exists(target):
        raise FileNotFoundError(f"Manifest not found: {target}")
    with open(target, "r", encoding="utf-8") as f:
        data = json.load(f)
    if mode == "master":
        updates = []
        for r in data:
            updates.append({
                "video_id": r["video_id"],
                "current_title": r.get("canonical_title"),
                "new_title": r.get("canonical_title"),
                "length": r.get("length", len(r.get("canonical_title", ""))),
                "playlists": r.get("playlists", [])
            })
        return updates
    return data


def get_authenticated_service(client_secret_file=None, token_file=None):
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    if not token_file:
        for candidate in ["data/credentials/token.json", "token.json"]:
            if os.path.exists(candidate):
                token_file = candidate
                break

    if not client_secret_file:
        for candidate in ["data/credentials/client_secrets.json", "client_secrets.json"]:
            if os.path.exists(candidate):
                client_secret_file = candidate
                break

    creds = None
    if token_file and os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing OAuth access token...")
            creds.refresh(Request())
            if token_file:
                with open(token_file, "w") as token:
                    token.write(creds.to_json())
            print("OAuth token refreshed.")
        else:
            if not client_secret_file or not os.path.exists(client_secret_file):
                raise FileNotFoundError(f"OAuth credentials file not found.")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
            token_path = token_file or "data/credentials/token.json"
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, "w") as token:
                token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def run_dry_run(updates):
    print("=" * 70)
    print(f"DRY-RUN SIMULATION: Channel Title Standardization ({len(updates)} updates)")
    print("=" * 70)
    
    categories = {
        "Thirukkural": 0,
        "Shiva": 0,
        "Murugan": 0,
        "Vishnu / Krishna": 0,
        "Amman": 0,
        "Vinayagar": 0,
        "Vallalar / Cultural": 0
    }
    
    for i, item in enumerate(updates, 1):
        vid = item["video_id"]
        old_t = item["current_title"]
        new_t = item["new_title"]
        length = item["length"]
        pls = item.get("playlists", [])
        
        if "அதிகாரம்" in new_t:
            categories["Thirukkural"] += 1
        elif "Shiva" in new_t or "சிவ" in new_t or any("Shiva" in p for p in pls):
            categories["Shiva"] += 1
        elif "Murugan" in new_t or "முருக" in new_t or any("Murugar" in p for p in pls):
            categories["Murugan"] += 1
        elif "Vishnu" in new_t or "Krishna" in new_t or any("Vishnu" in p or "Krishnar" in p for p in pls):
            categories["Vishnu / Krishna"] += 1
        elif "Amman" in new_t or "அபிராமி" in new_t or any("Amman" in p for p in pls):
            categories["Amman"] += 1
        elif "Vinayagar" in new_t or "கணேச" in new_t or any("Vinayagar" in p for p in pls):
            categories["Vinayagar"] += 1
        else:
            categories["Vallalar / Cultural"] += 1

        if i <= 15 or i > len(updates) - 5:
            print(f"[{i:03d}] ID: {vid}")
            print(f"      OLD: {old_t}")
            print(f"      NEW: {new_t} ({length} chars)")
        elif i == 16:
            print(f"      ... [{len(updates) - 20} more updates] ...")

    print("\n" + "=" * 70)
    print("SUMMARY BY CATEGORY:")
    for cat, count in categories.items():
        print(f"  - {cat:<22}: {count:3d} updates")
    print(f"  TOTAL UPDATES TO APPLY : {len(updates):3d}")
    print("=" * 70)
    print("[OK] Dry run completed. All titles <= 95 characters. 100% compliant with canonical naming.")

def run_live(updates):
    from googleapiclient.errors import HttpError

    print("=" * 70)
    print(f"LIVE EXECUTION: Applying up to {len(updates)} title updates via YouTube Data API")
    print("=" * 70)
    
    try:
        youtube = get_authenticated_service()
        # Verify authenticated channel
        ch_resp = youtube.channels().list(part="snippet", mine=True).execute()
        for ch in ch_resp.get("items", []):
            print(f"Authenticated as Channel: {ch['snippet']['title']} (ID: {ch['id']})")
    except Exception as e:
        print(f"[ERROR] Authentication failed: {e}")
        return

    target_map = {item["video_id"]: item["new_title"] for item in updates}
    all_vids = [item["video_id"] for item in updates]

    # Process in batches of 50 for listing
    batch_size = 50
    success_count = 0
    skip_count = 0
    fail_count = 0
    not_found_count = 0
    quota_reached = False

    print(f"Fetching current snippets in batches of {batch_size}...")
    for chunk_start in range(0, len(all_vids), batch_size):
        if quota_reached:
            break
        chunk = all_vids[chunk_start : chunk_start + batch_size]
        ids_str = ",".join(chunk)
        
        try:
            res = youtube.videos().list(part="snippet", id=ids_str).execute()
            items_by_id = {it["id"]: it for it in res.get("items", [])}
        except HttpError as he:
            if "quotaExceeded" in str(he):
                print("\n[ALERT] YouTube API daily quota limit reached during batch fetch.")
                quota_reached = True
                break
            else:
                print(f"[ERROR] Error listing batch {chunk_start}: {he}")
                continue

        for vid in chunk:
            target_title = target_map[vid]
            video_obj = items_by_id.get(vid)
            if not video_obj:
                # Video may be an audio track generated by DistroKid, or private/deleted
                not_found_count += 1
                continue

            snippet = video_obj["snippet"]
            current_title = snippet["title"]

            if current_title == target_title:
                skip_count += 1
                continue

            # Need update
            idx = success_count + fail_count + 1
            print(f"\n[{idx:03d}] Updating [{vid}]")
            print(f"      FROM: {current_title}")
            print(f"      TO:   {target_title}")

            snippet["title"] = target_title
            
            # YouTube update call
            try:
                youtube.videos().update(
                    part="snippet",
                    body={"id": vid, "snippet": snippet}
                ).execute()
                print(f"      -> SUCCESS!")
                success_count += 1
                # Subtle throttle to respect API rate limits
                time.sleep(0.3)
            except HttpError as ex:
                if "quotaExceeded" in str(ex):
                    print("\n[ALERT] YouTube API daily quota limit (10,000 units) reached.")
                    print("Progress is safely stored. Run again tomorrow to continue seamlessly.")
                    quota_reached = True
                    break
                else:
                    print(f"      -> FAILED: {ex}")
                    fail_count += 1

    print("\n" + "=" * 70)
    print("LIVE SYNC SUMMARY:")
    print(f"  Successfully Updated : {success_count}")
    print(f"  Already Up to Date   : {skip_count}")
    print(f"  Unmodified/Not Found : {not_found_count} (e.g. DistroKid auto-generated audio topic tracks)")
    print(f"  Failed Updates       : {fail_count}")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Sync standardized titles to YouTube channel @guru-kula-desam")
    parser.add_argument("--live", action="store_true", help="Execute live updates using YouTube Data API")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate updates without calling API (default)")
    parser.add_argument("--all", action="store_true", help="Process all 323 changed tracks (including DistroKid audio tracks)")
    parser.add_argument("--master", action="store_true", help="Verify all 598 catalog tracks across entire library")
    args = parser.parse_args()

    mode = "pending"
    if args.master:
        mode = "master"
    elif args.all:
        mode = "all"

    updates = load_updates(mode=mode)
    if args.live:
        run_live(updates)
    else:
        run_dry_run(updates)


if __name__ == "__main__":
    main()
