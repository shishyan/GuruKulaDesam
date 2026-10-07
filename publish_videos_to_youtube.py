# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Official YouTube Channel Publisher
Publishes rendered Thirukkural cinematic releases to @guru-kula-desam:
1. Resumable video upload (1280x720 24fps MP4 with Faststart)
2. Sets official custom high-resolution 16:9 thumbnail artwork
3. Inserts into Master Playlist: 'திருக்குறள் | Thirukkural — Master Collection' (PLW7qBZp_Q8Ro)
4. Updates catalog and stages publishing manifest
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
TOKEN_FILE = ROOT / "token.json"
CLIENT_SECRETS_FILE = ROOT / "client_secrets.json"
METADATA_FILE = ROOT / "production" / "metadata" / "thirukkural_releases_metadata.json"
PLAYLIST_ID = "PLW7qBZp_Q8Ro"  # திருக்குறள் | Thirukkural — Master Collection

VIDEO_FILES = {
    26: ROOT / "renders" / "releases" / "adhikaram_26_pulaal_unnaamai_cinematic.mp4",
    27: ROOT / "renders" / "releases" / "adhikaram_27_thavam_cinematic.mp4",
    52: ROOT / "renders" / "releases" / "adhikaram_52_therinthu_vinaiyaadal_cinematic.mp4",
    54: ROOT / "renders" / "releases" / "adhikaram_54_pochchaavaamai_cinematic.mp4",
    57: ROOT / "renders" / "releases" / "adhikaram_57_veruvantha_seyyaamai_cinematic.mp4",
    61: ROOT / "renders" / "releases" / "adhikaram_61_madiyinmai_cinematic.mp4",
}

THUMBNAIL_FILES = {
    26: ROOT / "production" / "visuals" / "thirukkural" / "26-pulaal-unnaamai" / "04-saint-turning-away-meat.jpg",
    27: ROOT / "production" / "visuals" / "thirukkural" / "27-thavam" / "01-ascetic-dawn-boulder.jpg",
    52: ROOT / "production" / "visuals" / "thirukkural" / "52-therinthu-vinaiyaadal" / "01-n01_king_weighs_good_and_evil.jpg",
    54: ROOT / "production" / "visuals" / "thirukkural" / "54-pochchaavaamai" / "01-n01_king_neglecting_affairs.jpg",
    57: ROOT / "production" / "visuals" / "thirukkural" / "57-veruvantha-seyyaamai" / "01-n01_king_patient_hearing.jpg",
    61: ROOT / "production" / "visuals" / "thirukkural" / "61-madiyinmai" / "01-n01_flickering_lamp_neglected_house.jpg",
}

def get_authenticated_service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRETS_FILE.exists():
                raise FileNotFoundError(f"Missing {CLIENT_SECRETS_FILE}")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def format_description(item):
    desc = item["description"]
    lines = [
        item["canonical_youtube_title"],
        "",
        desc["tamil_summary"],
        "",
        "Key Kurals:"
    ]
    for k in item["key_kurals"]:
        lines.append(f"குறள் {k['number']}:")
        lines.append(k["tamil"])
        lines.append(f"English: \"{k['english']}\"")
        lines.append("")
        
    lines.append(desc["english_summary"])
    lines.append("")
    lines.append("⏱️ Timestamps / Chapters:")
    for t in desc["timestamps"]:
        lines.append(f"{t['time']} - {t['label']}")
        
    lines.append("")
    lines.append("🎵 Credits & Release Info:")
    lines.append(f"• Track: {desc['audio_credits']['track']}")
    lines.append(f"• Channel: {desc['audio_credits']['artist']} (@guru-kula-desam)")
    if "vocals_engineering" in desc['audio_credits']:
        lines.append(f"• Production & Vocals: {desc['audio_credits']['vocals_engineering']}")
    if "banjo_engineering" in desc['audio_credits']:
        lines.append(f"• Production & Instrumentation: {desc['audio_credits']['banjo_engineering']}")
    lines.append(f"• Audio Master: {desc['audio_credits']['audio_source_url']}")
    lines.append(f"• Thirukkural Master Collection: {desc['audio_credits']['playlist_url']}")
    lines.append("")
    lines.append(desc["call_to_action"])
    lines.append("")
    lines.append(" ".join(item["hashtags"]))
    return "\n".join(lines)

def upload_video(youtube, item, privacy_status="public", dry_run=False):
    ch = item["chapter_number"]
    video_path = VIDEO_FILES.get(ch)
    thumb_path = THUMBNAIL_FILES.get(ch)
    
    if not video_path or not video_path.exists():
        raise FileNotFoundError(f"Video file not found for Chapter {ch}: {video_path}")
    if not thumb_path or not thumb_path.exists():
        raise FileNotFoundError(f"Thumbnail not found for Chapter {ch}: {thumb_path}")
        
    title = item["canonical_youtube_title"]
    description = format_description(item)
    tags = item.get("search_tags", [])
    
    print("\n" + "=" * 80)
    print(f"PREPARING PUBLICATION: Chapter {ch} - {item['tamil_title']}")
    print("=" * 80)
    print(f"Title ({len(title)} chars): {title}")
    print(f"Video File: {video_path} ({video_path.stat().st_size / (1024*1024):.2f} MB)")
    print(f"Thumbnail: {thumb_path} ({thumb_path.stat().st_size / 1024:.1f} KB)")
    print(f"Privacy: {privacy_status}")
    print(f"Tags ({len(tags)}): {', '.join(tags[:6])}...")
    
    if dry_run:
        print("[DRY RUN] Skipping actual network upload to YouTube API.")
        return {
            "chapter": ch,
            "title": title,
            "status": "DRY_RUN_OK",
            "video_id": f"DRY_RUN_ID_CH_{ch}",
            "privacy": privacy_status
        }
        
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27"  # Education
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    print("Initiating resumable upload to YouTube Data API v3...", flush=True)
    media = MediaFileUpload(str(video_path), chunksize=10 * 1024 * 1024, resumable=True)
    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    retry_count = 0
    max_retries = 5
    while response is None:
        try:
            status, response = insert_request.next_chunk()
            if status:
                print(f"  > Upload progress: {int(status.progress() * 100)}%", flush=True)
            retry_count = 0
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                retry_count += 1
                if retry_count > max_retries:
                    raise
                wait_time = 2 ** retry_count
                print(f"Server error {e.resp.status}, retrying in {wait_time}s...", flush=True)
                time.sleep(wait_time)
            elif "quotaExceeded" in str(e):
                print(f"ERROR: YouTube API quota exceeded! {e}", flush=True)
                raise
            else:
                raise
        except Exception as e:
            retry_count += 1
            if retry_count > max_retries:
                raise
            wait_time = 2 ** retry_count
            print(f"Connection glitch: {e}, retrying chunk in {wait_time}s...", flush=True)
            time.sleep(wait_time)
            
    video_id = response["id"]
    print(f"SUCCESS: Video published! ID: {video_id} (https://www.youtube.com/watch?v={video_id})", flush=True)
    
    # Set custom thumbnail
    try:
        print("Uploading official 16:9 thumbnail...", flush=True)
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(str(thumb_path))
        ).execute()
        print("SUCCESS: Custom thumbnail uploaded.", flush=True)
    except Exception as e:
        print(f"WARNING: Could not set thumbnail: {e}", flush=True)
        
    # Add to Playlist
    try:
        print(f"Adding video to Master Playlist ({PLAYLIST_ID})...", flush=True)
        pl_body = {
            "snippet": {
                "playlistId": PLAYLIST_ID,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        youtube.playlistItems().insert(
            part="snippet",
            body=pl_body
        ).execute()
        print("SUCCESS: Added to Master Playlist.", flush=True)
    except Exception as e:
        print(f"WARNING: Could not add to playlist: {e}", flush=True)
        
    return {
        "chapter": ch,
        "title": title,
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "status": "PUBLISHED",
        "privacy": privacy_status
    }

def update_catalogs_with_new_ids(published_map):
    """
    Updates assets/data/catalog.json, docs/assets/data/catalog.json, site/assets/data/catalog.json
    and site_catalog.json with the newly published YouTube IDs.
    """
    patch_path = ROOT / "production" / "catalog_patch_new_videos.json"
    if not patch_path.exists():
        print(f"Notice: {patch_path} not found for patching.")
        return
        
    with open(patch_path, "r", encoding="utf-8") as f:
        patch_data = json.load(f)
        
    new_films = []
    for rel in patch_data.get("releases", []):
        ch = rel["chapter_number"]
        if ch in published_map:
            film_entry = rel["catalog_film_entry"].copy()
            film_entry["id"] = published_map[ch]["video_id"]
            new_films.append(film_entry)
            
    if not new_films:
        return
        
    target_files = [
        ROOT / "assets" / "data" / "catalog.json",
        ROOT / "docs" / "assets" / "data" / "catalog.json",
        ROOT / "site" / "assets" / "data" / "catalog.json",
        ROOT / "site_catalog.json"
    ]
    
    for tf in target_files:
        if not tf.exists():
            continue
        with open(tf, "r", encoding="utf-8") as f:
            cat = json.load(f)
            
        existing_ids = set(x["id"] for x in cat.get("thirukkural", []))
        updated_count = 0
        added_count = 0
        for nf in new_films:
            # First look for existing entry to update in place
            matched = False
            for item in cat.get("thirukkural", []):
                if item.get("original_audio_id") == nf.get("original_audio_id") or (
                    item.get("title") and nf.get("title") and item.get("title")[:20] == nf.get("title")[:20]
                ):
                    item["id"] = nf["id"]
                    item["playlists"] = nf.get("playlists", item.get("playlists"))
                    matched = True
                    updated_count += 1
                    break
            if not matched and nf["id"] not in existing_ids:
                cat["thirukkural"].append(nf)
                existing_ids.add(nf["id"])
                added_count += 1
                
        with open(tf, "w", encoding="utf-8") as f:
            json.dump(cat, f, indent=4, ensure_ascii=False)
        print(f"Updated {tf.name}: {updated_count} updated, {added_count} added.", flush=True)

def load_existing_published():
    manifest_path = ROOT / "production" / "published_videos_manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                published = {}
                for item in data:
                    if item.get("status") == "PUBLISHED" and not str(item.get("video_id", "")).startswith("DRY_RUN"):
                        published[item["chapter"]] = item
                return published
        except Exception:
            return {}
    return {}

def save_manifest(published_results):
    manifest_path = ROOT / "production" / "published_videos_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(published_results, f, indent=2, ensure_ascii=False)
    print(f"Manifest saved to {manifest_path}", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Publish Thirukkural videos to YouTube channel")
    parser.add_argument("--dry-run", action="store_true", help="Simulate upload without actual API mutations")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"], help="Privacy status")
    parser.add_argument("--chapter", type=int, help="Single chapter to upload (e.g. 26)")
    parser.add_argument("--republish", action="store_true", help="Republish new multi-scene films and mark previous uploads as private")
    args = parser.parse_args()
    
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata_list = json.load(f)
        
    if args.chapter:
        metadata_list = [item for item in metadata_list if item["chapter_number"] == args.chapter]
        if not metadata_list:
            print(f"Error: Chapter {args.chapter} not found in metadata.")
            return
            
    print(f"Found {len(metadata_list)} chapters to process.")
    youtube = None
    if not args.dry_run:
        print("Authenticating with YouTube API...")
        youtube = get_authenticated_service()
        print("Authenticated successfully!")
        
    existing_published = load_existing_published()
    published_results = list(existing_published.values())
    published_map = dict(existing_published)
    
    for item in metadata_list:
        ch = item["chapter_number"]
        if not args.dry_run and ch in existing_published and not args.republish:
            print(f"\n[SKIP] Chapter {ch} is already PUBLISHED with video ID {existing_published[ch]['video_id']}! Preventing duplicate upload.", flush=True)
            continue
            
        old_id = existing_published[ch]["video_id"] if ch in existing_published else None
        
        try:
            res = upload_video(youtube, item, privacy_status=args.privacy, dry_run=args.dry_run)
            
            # If republishing, mark previous video as private
            if not args.dry_run and args.republish and old_id and old_id != res.get("video_id"):
                try:
                    print(f"Deprecating previous placeholder upload ({old_id}) to private...", flush=True)
                    youtube.videos().update(
                        part="status",
                        body={"id": old_id, "status": {"privacyStatus": "private"}}
                    ).execute()
                    print(f"Successfully deprecated {old_id}.", flush=True)
                except Exception as e:
                    print(f"Notice: Could not deprecate old video {old_id}: {e}", flush=True)
                    
            # Update results list
            published_results = [p for p in published_results if p["chapter"] != ch]
            published_results.append(res)
            
            if res.get("status") == "PUBLISHED":
                published_map[res["chapter"]] = res
                save_manifest(published_results)
                update_catalogs_with_new_ids(published_map)
        except Exception as e:
            print(f"\n[ERROR] Failed publishing Chapter {ch}: {e}", flush=True)
            save_manifest(published_results)
            if "quotaExceeded" in str(e):
                print("Aborting remaining uploads due to YouTube daily quota exhaustion.")
                break
            
    # Final manifest save
    save_manifest(published_results)
    
    if published_map:
        print("\nUpdating site catalogs with newly published YouTube video IDs...", flush=True)
        update_catalogs_with_new_ids(published_map)
        
    print("\nAll publishing operations completed!")
    print(json.dumps(published_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
