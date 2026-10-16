#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/upload_private_master_to_youtube.py
Uploads a rendered Thirukkural Master Film to YouTube as PRIVATE draft:
- Resumable video upload (1280x720 24fps)
- Sets official 16:9 thumbnail
- Adds to Master Playlist: PLW7qBZp_Q8Ro
- Records YouTube Video ID in published registry
"""
import os, sys, json, time, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = ROOT / "data" / "credentials" / "token.json"
MANIFEST_FILE = ROOT / "production" / "metadata" / "curated_37_youtube_manifest.json"
PLAYLIST_ID = "PLW7qBZp_Q8Ro"  # திருக்குறள் Master Collection

def get_youtube_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtubepartner"]
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Missing OAuth token at {TOKEN_FILE}")

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)

def upload_chapter_as_private(ch_num, video_path, thumb_path=None):
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Load title and metadata
    title = f"திருக்குறள்: அதிகாரம் {ch_num} | Cinematic Devotional Film"
    description = f"திருக்குறள் — அதிகாரம் {ch_num}\nவள்ளுவர் வாய்மொழி | தெய்வீக பக்தி இசை மற்றும் சங்க கால கலைக்காட்சிகள்\n\nMaster Cinematic Release by Guru Kula Desam (@guru-kula-desam)\nResumable 720p 24fps master film.\n\n#Thirukkural #திருக்குறள் #அதிகாரம்{ch_num} #GuruKulaDesam"
    tags = ["திருக்குறள்", "Thirukkural", f"அதிகாரம் {ch_num}", "Guru Kula Desam", "Tamil", "Devotional"]

    if MANIFEST_FILE.exists():
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        for item in manifest:
            if item.get("chapter") == ch_num:
                title = item.get("title", title)
                description = item.get("description", description)
                tags = item.get("tags", tags)
                break

    youtube = get_youtube_service()

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

    print(f"\n[YouTube Upload] Chapter {ch_num}: {title} (PRIVATE)")
    print(f"  File: {video_path.name} ({video_path.stat().st_size / 1e6:.1f} MB)")

    media = MediaFileUpload(str(video_path), chunksize=10 * 1024 * 1024, resumable=True)
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    retries = 0
    while response is None:
        try:
            status, response = req.next_chunk()
            if status:
                print(f"  > Progress: {int(status.progress() * 100)}%", flush=True)
            retries = 0
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                retries += 1
                if retries > 5: raise
                time.sleep(2 ** retries)
            elif "quotaExceeded" in str(e):
                print(f"  [ERROR] YouTube API quota exceeded: {e}")
                return None
            else:
                raise

    video_id = response.get("id")
    print(f"✔ [UPLOADED PRIVATE] Video ID: {video_id} (https://youtu.be/{video_id})")

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
        print(f"✔ [PLAYLIST] Added to {PLAYLIST_ID}")
    except Exception as e:
        print(f"  [PLAYLIST NOTE] {e}")

    # Set custom thumbnail if available
    if thumb_path and Path(thumb_path).exists():
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumb_path))
            ).execute()
            print("✔ [THUMBNAIL] Uploaded custom thumbnail.")
        except Exception as e:
            print(f"  [THUMBNAIL NOTE] {e}")

    # Save to upload registry
    registry_file = ROOT / "production" / "youtube_uploaded_private_masters.json"
    registry = {}
    if registry_file.exists():
        try: registry = json.loads(registry_file.read_text(encoding="utf-8"))
        except: pass
    registry[str(ch_num)] = {
        "chapter": ch_num,
        "video_id": video_id,
        "title": title,
        "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "privacy": "private"
    }
    registry_file.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    return video_id

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--chapter", type=int, required=True)
    p.add_argument("--video-file", type=str, required=True)
    p.add_argument("--thumb-file", type=str, default=None)
    args = p.parse_args()
    upload_chapter_as_private(args.chapter, args.video_file, args.thumb_file)
