"""
Thirukkural Channel & Playlist Sync Utility for @guru-kula-desam
This script:
1. Applies canonical Adhigaram prefixes (அதிகாரம் <எண்> - <அதிகாரப் பெயர்>) to all 84 Thirukkural song titles.
2. Reconciles 'திருக்குறள் | Thirukkural — Master Collection' (PLW7qBZp_Q8Ro):
   - Adds 5 missing Thirukkural videos
   - Removes 9 non-Thirukkural videos
Supports both dry-run simulation and live YouTube Data API execution.
"""

import os
import sys
import json
import csv
import argparse

# Setup UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PLAYLIST_ID = "PLW7qBZp_Q8Ro"  # திருக்குறள் | Thirukkural — Master Collection
CHANNEL_HANDLE = "@guru-kula-desam"

MISSING_VIDEOS_TO_ADD = [
    {"id": "JDqbpISJjIA", "chapter": 125, "adhigaram": "நெஞ்சறிவுறுத்தல்", "title": "அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் (பகுதி 1)"},
    {"id": "7wJJCQrYo04", "chapter": 125, "adhigaram": "நெஞ்சறிவுறுத்தல்", "title": "அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் (பகுதி 2)"},
    {"id": "KFtS403RfbY", "chapter": 125, "adhigaram": "நெஞ்சறிவுறுத்தல்", "title": "அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் (பகுதி 1) | Nenjari Vuruthal Part 1 Cinematic Film"},
    {"id": "lpOcAVJIax0", "chapter": 125, "adhigaram": "நெஞ்சறிவுறுத்தல்", "title": "அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் (பகுதி 2) | Compassion Journey Cinematic Film"},
    {"id": "R8OyFbqJJEw", "chapter": 125, "adhigaram": "நெஞ்சறிவுறுத்தல்", "title": "அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் (பகுதி 2) | Nenjari Vuruthal Part 2 Cinematic Film"}
]

NON_KURAL_TO_REMOVE = [
    {"id": "5gO0xpY_Y3E", "reason": "Hans Zimmer - Interstellar (Non-devotional / Non-kural)"},
    {"id": "-zVzQ1XnY8Q", "reason": "தில்லை வாழ் அந்தணர்! (Lord Shiva Song)"},
    {"id": "FGeahfpAbiw", "reason": "திருவருட்பா - அன்பு மாலை (Thiruvarutpa Song)"},
    {"id": "-yEq62Bu_d8", "reason": "வேண்டுமே இத்தனையும் (Thiruvempavai / Shiva Song)"},
    {"id": "2Gbhx6SwH-M", "reason": "திருவோத்தூர் பதிகம் (Thiruvothur Pathigam / Shiva Song)"},
    {"id": "umo1jodWzXY", "reason": "திருவோத்தூர் பதிகம் (V) (Thiruvothur Pathigam / Shiva Song)"},
    {"id": "4RUk7FPJ3TU", "reason": "குழைத்த பத்து (II) (Thiruvasagam / Shiva Song)"},
    {"id": "ZAjf5Ewzu_c", "reason": "மாசில் வீணையும் (Tevaram / Shiva Song)"},
    {"id": "jZFTlpJwn6A", "reason": "தியாக வண்ணப் பதிகம் (Thiyaga Vanna Pathigam / Shiva Song)"}
]

def load_updates():
    json_path = os.path.join(os.path.dirname(__file__), "thirukkural_title_updates.json")
    with open(json_path, "r", encoding="utf-8") as f:
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
                raise FileNotFoundError(
                    f"OAuth client secret file '{client_secret_file}' not found.\n"
                    f"Please download OAuth Client ID JSON from Google Cloud Console as '{client_secret_file}'."
                )
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def run_dry_run(updates):
    print("=" * 80)
    print(f"DRY RUN AUDIT REPORT — @guru-kula-desam")
    print(f"Playlist: திருக்குறள் | Thirukkural — Master Collection ({PLAYLIST_ID})")
    print("=" * 80)
    print(f"\n1. TITLE PREFIX UPDATES: {len(updates)} Thirukkural songs")
    for u in updates:
        print(f"  [{u['chapter']}] {u['id']}: '{u['current_title']}' -> '{u['new_title']}'")

    print(f"\n2. PLAYLIST ADDITIONS: {len(MISSING_VIDEOS_TO_ADD)} missing songs to add")
    for m in MISSING_VIDEOS_TO_ADD:
        print(f"  + Add {m['id']} (Chapter {m['chapter']}: {m['adhigaram']}) -> {m['title']}")

    print(f"\n3. PLAYLIST REMOVALS: {len(NON_KURAL_TO_REMOVE)} non-Thirukkural songs to remove")
    for r in NON_KURAL_TO_REMOVE:
        print(f"  - Remove {r['id']} ({r['reason']})")
    print("\nDry run completed successfully. No remote mutations performed.")

def run_live_update(updates, client_secret_file, token_file):
    print("Authenticating with YouTube API...")
    youtube = get_authenticated_service(client_secret_file, token_file)
    print("Authentication successful!\n")

    # 1. Update Video Titles
    print("--- 1. Updating Video Titles ---")
    for i, u in enumerate(updates, start=1):
        vid_id = u["id"]
        new_title = u["new_title"]
        try:
            # Fetch existing video snippet
            vid_resp = youtube.videos().list(part="snippet", id=vid_id).execute()
            if not vid_resp.get("items"):
                print(f"[{i}/{len(updates)}] Video {vid_id} not found on YouTube. Skipping.")
                continue
            item = vid_resp["items"][0]
            snippet = item["snippet"]
            cur_title = snippet["title"]

            if cur_title == new_title:
                print(f"[{i}/{len(updates)}] {vid_id}: Title already up-to-date.")
                continue

            snippet["title"] = new_title
            # Update video
            youtube.videos().update(
                part="snippet",
                body={"id": vid_id, "snippet": snippet}
            ).execute()
            print(f"[{i}/{len(updates)}] Updated {vid_id} -> {new_title}")
        except Exception as e:
            print(f"[{i}/{len(updates)}] ERROR updating {vid_id}: {e}")

    # 2. Fetch Playlist Items to get playlistItemIds
    print("\n--- 2. Fetching Playlist Items for PLW7qBZp_Q8Ro ---")
    pl_items = []
    next_page_token = None
    while True:
        resp = youtube.playlistItems().list(
            part="snippet",
            playlistId=PLAYLIST_ID,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        pl_items.extend(resp.get("items", []))
        next_page_token = resp.get("nextPageToken")
        if not next_page_token:
            break

    existing_vids = {it["snippet"]["resourceId"]["videoId"]: it["id"] for it in pl_items}
    print(f"Current items in playlist: {len(existing_vids)}")

    # 3. Add Missing Videos
    print("\n--- 3. Adding Missing Thirukkural Songs to Playlist ---")
    for m in MISSING_VIDEOS_TO_ADD:
        vid_id = m["id"]
        if vid_id in existing_vids:
            print(f"Video {vid_id} already in playlist.")
            continue
        try:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": PLAYLIST_ID,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": vid_id
                        }
                    }
                }
            ).execute()
            print(f"Added {vid_id} ({m['title']}) to playlist {PLAYLIST_ID}")
        except Exception as e:
            print(f"ERROR adding {vid_id}: {e}")

    # 4. Remove Non-Thirukkural Videos
    print("\n--- 4. Removing Non-Thirukkural Songs from Playlist ---")
    remove_ids = {r["id"] for r in NON_KURAL_TO_REMOVE}
    for vid_id in remove_ids:
        if vid_id in existing_vids:
            pl_item_id = existing_vids[vid_id]
            try:
                youtube.playlistItems().delete(id=pl_item_id).execute()
                print(f"Removed non-kural video {vid_id} (item: {pl_item_id})")
            except Exception as e:
                print(f"ERROR removing {vid_id}: {e}")
        else:
            print(f"Non-kural video {vid_id} not found in playlist.")

    print("\nAll updates completed successfully!")

def main():
    parser = argparse.ArgumentParser(description="Update Thirukkural titles and playlist on @guru-kula-desam")
    parser.add_argument("--live", action="store_true", help="Execute live updates using YouTube Data API")
    parser.add_argument("--client-secrets", default="client_secrets.json", help="Path to OAuth client secrets JSON")
    parser.add_argument("--token", default="token.json", help="Path to token cache file")
    args = parser.parse_args()

    updates = load_updates()

    if args.live:
        run_live_update(updates, args.client_secrets, args.token)
    else:
        run_dry_run(updates)
        print("\nNote: To run live updates with OAuth, run:")
        print("  python update_youtube_metadata.py --live --client-secrets <path-to-client-secret.json>")

if __name__ == "__main__":
    main()
