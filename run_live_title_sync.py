import os
import sys
import json
import time
import httplib2
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

TOKEN_FILE = "data/credentials/token_839236964216.json"
PENDING_FILE = "channel_direct_uploads_pending.json"
PROGRESS_FILE = "production/title_updates_progress.json"

def get_yt_client():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    http = httplib2.Http(disable_ssl_certificate_validation=True)
    auth_http = AuthorizedHttp(creds, http=http)
    return build("youtube", "v3", http=auth_http)

def main():
    print("=" * 70)
    print("STARTING LIVE YOUTUBE TITLE UPDATES WITH PROJECT 839236964216")
    print("=" * 70)

    yt = get_yt_client()
    ch_resp = yt.channels().list(part="snippet", mine=True).execute()
    for ch in ch_resp.get("items", []):
        print(f"Authenticated as Channel: {ch['snippet']['title']} (ID: {ch['id']})")

    with open(PENDING_FILE, "r", encoding="utf-8") as f:
        pending_items = json.load(f)

    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    progress = {}
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                progress = json.load(f)
        except Exception:
            progress = {}

    target_map = {item["video_id"]: item["new_title"] for item in pending_items}
    # Filter items not yet successfully done in progress
    items_to_process = [
        item for item in pending_items 
        if not progress.get(item["video_id"], {}).get("done")
    ]
    print(f"Total pending tracks in queue: {len(pending_items)}")
    print(f"Remaining to process: {len(items_to_process)}")

    batch_size = 50
    success_count = 0
    skip_count = 0
    fail_count = 0
    quota_exhausted = False

    for chunk_start in range(0, len(items_to_process), batch_size):
        if quota_exhausted:
            break
        chunk = items_to_process[chunk_start : chunk_start + batch_size]
        chunk_vids = [item["video_id"] for item in chunk]
        ids_str = ",".join(chunk_vids)

        try:
            res = yt.videos().list(part="snippet", id=ids_str).execute()
            items_by_id = {it["id"]: it for it in res.get("items", [])}
        except HttpError as he:
            if "quotaExceeded" in str(he):
                print("\n[QUOTA REACHED] YouTube API daily quota limit reached during batch fetch.")
                quota_exhausted = True
                break
            else:
                print(f"[ERROR] Error listing batch: {he}")
                continue

        for item in chunk:
            vid = item["video_id"]
            target_title = target_map[vid]
            video_obj = items_by_id.get(vid)

            if not video_obj:
                # Video not found or topic track
                progress[vid] = {"done": True, "status": "not_found_or_topic"}
                continue

            snippet = video_obj["snippet"]
            current_title = snippet.get("title", "")

            if current_title == target_title:
                skip_count += 1
                progress[vid] = {"done": True, "status": "already_up_to_date", "title": current_title}
                continue

            # Title needs update
            print(f"\n[{success_count + fail_count + 1}] Updating video [{vid}]")
            print(f"   OLD: {current_title}")
            print(f"   NEW: {target_title}")

            snippet["title"] = target_title

            try:
                yt.videos().update(
                    part="snippet",
                    body={"id": vid, "snippet": snippet}
                ).execute()
                print(f"   -> SUCCESS!")
                success_count += 1
                progress[vid] = {"done": True, "status": "updated", "title": target_title, "old_title": current_title}
                time.sleep(0.3)
            except HttpError as ex:
                if "quotaExceeded" in str(ex):
                    print(f"\n[ALERT] YouTube API quota exceeded after {success_count} updates.")
                    quota_exhausted = True
                    break
                else:
                    print(f"   -> FAILED: {ex}")
                    progress[vid] = {"done": False, "status": "failed", "error": str(ex)}
                    fail_count += 1

            # Save progress periodically
            with open(PROGRESS_FILE, "w", encoding="utf-8") as pf:
                json.dump(progress, pf, ensure_ascii=False, indent=2)

    with open(PROGRESS_FILE, "w", encoding="utf-8") as pf:
        json.dump(progress, pf, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print("SYNC EXECUTION SUMMARY:")
    print(f"  Successfully Updated: {success_count}")
    print(f"  Already Up to Date:   {skip_count}")
    print(f"  Failed / Skipped:     {fail_count}")
    print(f"  Quota Exhausted:      {quota_exhausted}")
    print("=" * 70)

if __name__ == "__main__":
    main()
