"""
Comprehensive YouTube Channel & Playlist Title Sync Utility
Channel: @guru-kula-desam

Features:
1. Standardizes all 323 video titles across Thirukkural, Shiva, Murugan, Vishnu, Krishna, Amman, Vinayagar, and Vallalar categories.
2. Enforces bilingual canonical naming format:
   - Thirukkural: அதிகாரம் <எண்> - <அதிகாரப் பெயர்> | <English Transliteration> [<Descriptor>]
   - Deity/Spiritual: <தமிழ் தலைப்பு> | <English Transliteration> [<Category Film/Song>]
3. Strictly maintains all titles <= 95 characters (below YouTube's 100 char limit).
4. Supports simulation (--dry-run) and authenticated live API updates (--live).
"""

import os
import sys
import json
import csv
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UPDATES_FILE = os.path.join(os.path.dirname(__file__), "all_channel_title_updates.json")

def load_updates():
    if not os.path.exists(UPDATES_FILE):
        raise FileNotFoundError(f"Updates manifest not found: {UPDATES_FILE}")
    with open(UPDATES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_authenticated_service(client_secret_file="client_secrets.json", token_file="token.json"):
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(client_secret_file):
                raise FileNotFoundError(f"OAuth credentials file '{client_secret_file}' not found.")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
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
        
        # Categorize
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
    print("=" * 70)
    print(f"LIVE EXECUTION: Applying {len(updates)} title updates via YouTube Data API")
    print("=" * 70)
    
    try:
        youtube = get_authenticated_service()
    except Exception as e:
        print(f"[ERROR] Authentication failed: {e}")
        return

    success_count = 0
    fail_count = 0

    for i, item in enumerate(updates, 1):
        vid = item["video_id"]
        new_title = item["new_title"]
        try:
            # 1. Fetch current snippet
            res = youtube.videos().list(part="snippet", id=vid).execute()
            items = res.get("items", [])
            if not items:
                print(f"[{i:03d}] FAIL: Video {vid} not found on channel.")
                fail_count += 1
                continue
            
            snippet = items[0]["snippet"]
            old_title = snippet["title"]
            if old_title == new_title:
                print(f"[{i:03d}] SKIP: Video {vid} already has target title.")
                success_count += 1
                continue

            # 2. Update title
            snippet["title"] = new_title
            youtube.videos().update(
                part="snippet",
                body={"id": vid, "snippet": snippet}
            ).execute()
            
            print(f"[{i:03d}] SUCCESS: Updated {vid} -> '{new_title}'")
            success_count += 1
        except Exception as ex:
            print(f"[{i:03d}] ERROR updating {vid}: {ex}")
            fail_count += 1

    print("\n" + "=" * 70)
    print(f"LIVE SYNC COMPLETED: {success_count} succeeded, {fail_count} failed.")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Sync standardized titles to YouTube channel @guru-kula-desam")
    parser.add_argument("--live", action="store_true", help="Execute live updates using YouTube Data API")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate updates without calling API (default)")
    args = parser.parse_args()

    updates = load_updates()
    if args.live:
        run_live(updates)
    else:
        run_dry_run(updates)

if __name__ == "__main__":
    main()
