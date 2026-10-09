#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam (@guru-kula-desam)
Official Publisher: Lord Murugar Master Cinematic Films
Uploads the rendered 720p master films to YouTube and adds them to playlist 'PLcpX3K7ZFYjM' (Lord Murugar Songs).
"""

import sys
import json
import time
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = ROOT / "production" / "murugan_published_manifest.json"
TOKEN_FILE = ROOT / "data" / "credentials" / "token.json"
CLIENT_SECRETS_FILE = ROOT / "data" / "credentials" / "client_secrets.json"
PLAYLIST_ID = "PLcpX3K7ZFYjM"

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Missing {TOKEN_FILE}")
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def main():
    parser = argparse.ArgumentParser(description="Publish Lord Murugar Master Films to YouTube")
    parser.add_argument("--dry-run", action="store_true", help="Preview publication without uploading")
    parser.add_argument("--limit", type=int, default=15, help="Max films to upload")
    args = parser.parse_args()

    if not MANIFEST_FILE.exists():
        print(f"Error: Manifest {MANIFEST_FILE} not found.")
        sys.exit(1)

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    with open(ROOT / "live_youtube_metadata.json", "r", encoding="utf-8") as f:
        live_yt = json.load(f)

    releases = manifest.get("releases", [])
    print("=" * 80)
    print(f"GURU KULA DESAM — LORD MURUGAR MASTER FILMS PUBLISHING")
    print(f"Target Playlist: {PLAYLIST_ID} ({manifest.get('playlist_name')})")
    print(f"Total Master Films: {len(releases)} | Mode: {'DRY RUN' if args.dry_run else 'LIVE UPLOAD'}")
    print("=" * 80)

    for i, rel in enumerate(releases[:args.limit], 1):
        tid = rel["track_id"]
        meta = live_yt.get(tid, {})
        title = meta.get("title", f"{rel['hymn']} | Guru Kula Desam")
        desc = meta.get("description", f"{rel['hymn']} | Guru Kula Desam\n\nஅருணகிரிநாதர் அருளிய கந்தர் அநுபூதி")
        film_path = ROOT / rel["master_film"]
        
        print(f"\n[{i}/{len(releases)}] {rel['hymn']} ({tid})")
        print(f"  Title: {title}")
        print(f"  Film:  {film_path.name} ({rel['file_size_mb']:.2f} MB, {rel['duration_sec']}s)")

        if rel.get("status") == "PUBLISHED" and rel.get("youtube_id"):
            print(f"  Already published: https://youtu.be/{rel['youtube_id']} - Skipping.")
            continue

        if args.dry_run:
            print("  Status: [DRY RUN OK]")
            continue

        try:
            yt = get_authenticated_service()
            from googleapiclient.http import MediaFileUpload
            from googleapiclient.errors import HttpError
            body = {
                "snippet": {
                    "title": title,
                    "description": desc,
                    "tags": meta.get("tags", ["GuruKulaDesam", "Murugan", "Karthikeya", "KandharAnubhuti", "TamilDevotional", "Arunagirinathar"]),
                    "categoryId": "27"
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            }
            media = MediaFileUpload(str(film_path), chunksize=10*1024*1024, resumable=True)
            print("  Initiating upload to YouTube...")
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                status, resp = req.next_chunk()
                if status:
                    print(f"    Progress: {int(status.progress() * 100)}%")
            new_id = resp.get("id")
            print(f"  Upload Complete! New Video ID: {new_id} -> https://youtu.be/{new_id}")
            
            # Add to playlist
            try:
                yt.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": PLAYLIST_ID,
                            "resourceId": {"kind": "youtube#video", "videoId": new_id}
                        }
                    }
                ).execute()
                print(f"  Added to playlist {PLAYLIST_ID}")
            except Exception as pe:
                print(f"  Note: Playlist insertion note: {pe}")

            rel["status"] = "PUBLISHED"
            rel["youtube_id"] = new_id
            rel["published_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            time.sleep(3)
        except HttpError as he:
            if "quotaExceeded" in str(he):
                print(f"\n[QUOTA REACHED] YouTube Data API daily upload quota reached.")
                print(f"Uploaded tracks are saved. Remaining tracks will upload on the next daily quota window.")
                break
            else:
                print(f"  HTTP error for {tid}: {he}")
                break
        except Exception as e:
            print(f"  Upload error for {tid}: {e}")
            break

if __name__ == "__main__":
    main()
