#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam (@guru-kula-desam)
Autonomous Multi-Deity Master Films Publisher

Enforces STRICT User Directives:
1. ZERO DUPLICATES: Checks production/youtube_published_registry.json and live YouTube metadata.
   If a track or title already exists on YouTube, it is NEVER uploaded again.
2. NO BURNED LYRICS: Requires track["clean_cinematic"] == True. Master films must have
   unobstructed, clean devotional visuals with sacred framing and drizzle.
3. SEPARATE CAPTIONS: Lyrics are provided in video description and via closed caption (CC) tracks.
"""

import os
import sys
import re
import json
import time
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
MANIFEST_FILE = ROOT / "production" / "autonomous_master_production_manifest.json"
REGISTRY_FILE = ROOT / "production" / "youtube_published_registry.json"
METADATA_FILE = ROOT / "live_youtube_metadata.json"
TOKEN_FILE = ROOT / "data" / "credentials" / "token.json"
CLIENT_SECRETS_FILE = ROOT / "data" / "credentials" / "client_secrets.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtubepartner"
]

PLAYLIST_MAP = {
    "shiva": "PLeqSbdtlRtmc",          # Lord Shiva Songs
    "murugan": "PLcpX3K7ZFYjM",        # Lord Murugar Songs
    "vinayagar": "PLC84A3gANh-s",      # Lord Vinayagar Songs
    "amman": "PLKng43jJe18o",          # Goddess Amman Songs
    "vishnu_krishna": "PLHmbyO4GR_2k", # Lord Krishnar Songs
    "thirukkural": "PLW7qBZp_Q8Ro",    # Thirukkural Master Collection
    "vallalar_cultural": "PLI7Waf6Z6I48" # Other Songs
}

DEFAULT_TAGS = {
    "shiva": ["GuruKulaDesam", "LordShiva", "ShivaSongs", "Thevaram", "Thiruvasagam", "TamilDevotional", "Nataraja"],
    "murugan": ["GuruKulaDesam", "LordMurugan", "MuruganSongs", "KandharAnubhuti", "Thiruppugazh", "TamilDevotional"],
    "vinayagar": ["GuruKulaDesam", "LordVinayagar", "Ganesha", "VinayagarSongs", "Avvaiyar", "TamilDevotional"],
    "amman": ["GuruKulaDesam", "GoddessAmman", "AmmanSongs", "AbiramiAnthathi", "TamilDevotional", "Shakti"],
    "vishnu_krishna": ["GuruKulaDesam", "LordKrishna", "LordVishnu", "DivyaPrabandham", "HareKrishna", "TamilDevotional"],
    "thirukkural": ["GuruKulaDesam", "Thirukkural", "Thiruvalluvar", "TamilLiterature", "TamilWisdom", "TamilDevotional"],
    "vallalar_cultural": ["GuruKulaDesam", "Vallalar", "Thiruvarutpa", "Arutperunjothi", "Bharathiyar", "TamilSongs"]
}

def get_authenticated_service():
    try:
        from tools.quota_rotator import get_next_available_youtube_service
        return get_next_available_youtube_service()
    except Exception as e:
        print(f"[Rotator Warning] {e}. Falling back to default token.json.")
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        if not TOKEN_FILE.exists():
            raise FileNotFoundError(f"Missing OAuth token at {TOKEN_FILE}")

        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                    f.write(creds.to_json())
            else:
                raise RuntimeError("OAuth token expired and cannot refresh without user interaction.")
        return build("youtube", "v3", credentials=creds), "default"


def load_published_registry():
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def record_published_video(track_id, youtube_id, title, category):
    registry = load_published_registry()
    entry = {
        "track_id": track_id,
        "youtube_id": youtube_id,
        "youtube_url": f"https://youtu.be/{youtube_id}",
        "title": title,
        "category": category,
        "published_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")
    }
    registry[track_id] = entry
    if youtube_id not in registry:
        registry[youtube_id] = entry
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"  [REGISTRY LOCKED] Recorded {track_id} -> https://youtu.be/{youtube_id} in {REGISTRY_FILE.name}")

def load_manifest():
    if not MANIFEST_FILE.exists():
        return {"completed_tracks": []}
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            return {"completed_tracks": data}
        return data

def save_manifest(manifest):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def is_track_safe_to_publish(track, registry, metadata_db):
    tid = track.get("track_id")
    title = track.get("title", "").strip()

    # 1. Authoritative Duplicate Check via Registry
    if tid in registry:
        reg_info = registry[tid]
        return False, f"DUPLICATE GUARD: Already published on YouTube ({reg_info.get('youtube_url', tid)})"

    # Normalize title for match (Tamil + ASCII alphanumeric)
    norm_title = re.sub(r"[^\w\u0B80-\u0BFF]", "", title.lower())
    if len(norm_title) >= 8:
        for reg_id, reg_info in registry.items():
            reg_t = re.sub(r"[^\w\u0B80-\u0BFF]", "", reg_info.get("title", "").strip().lower())
            if reg_t and reg_t == norm_title:
                return False, f"DUPLICATE GUARD: Title matches published video {reg_id} ({reg_info.get('youtube_url')})"

    # Check downloads deduplication audit
    audit_file = ROOT / "production" / "downloads_vs_youtube_audit.json"
    if audit_file.exists():
        try:
            with open(audit_file, "r", encoding="utf-8") as af:
                audit_data = json.load(af)
            source_audio = Path(track.get("source_audio", "")).name
            for match in audit_data.get("exact_matches_must_skip", []):
                if match.get("file_name") == source_audio:
                    return False, f"DUPLICATE GUARD: Source audio matches existing YouTube video {match.get('matched_youtube_id')} ({match.get('matched_youtube_title')})"
        except Exception:
            pass

    # 2. Status Check
    if track.get("status") == "PUBLISHED":
        return False, f"STATUS GUARD: Manifest marks track as already PUBLISHED"

    # 3. Clean Visuals Check (User Directive: REMOVE ALL BURNED LYRICS)
    if not track.get("clean_cinematic"):
        return False, f"CLEAN VISUAL GUARD: Video does not have clean_cinematic=True (must be rebuilt clean)"

    # 4. Master Film File Check
    film_rel = track.get("master_film")
    if not film_rel:
        return False, f"FILE GUARD: No master_film specified"

    film_path = ROOT / film_rel
    if not film_path.exists() or film_path.stat().st_size < 1000000:
        return False, f"FILE GUARD: Master film missing or invalid ({film_rel})"

    return True, "SAFE"

def publish_track(yt, track, metadata_db):
    tid = track.get("track_id")
    title = track.get("title", "Guru Kula Desam Master Film")
    cat = track.get("category", "vallalar_cultural").lower()
    film_rel = track.get("master_film")
    film_path = ROOT / film_rel

    # Retrieve live metadata if available
    meta = metadata_db.get(tid, {})
    meta_title = meta.get("title") or title
    if "Guru Kula Desam" not in meta_title and "@guru-kula-desam" not in meta_title:
        meta_title = f"{meta_title} | Guru Kula Desam"

    meta_desc = meta.get("description")
    if not meta_desc or len(meta_desc.strip()) < 20:
        meta_desc = (
            f"{meta_title}\n\n"
            f"Official 720p HD Master Film with Clean Devotional Visuals.\n"
            f"Presented by Guru Kula Desam (@guru-kula-desam).\n"
            f"Devotional and Philosophical Heritage of Tamil Nadu.\n\n"
            f"#GuruKulaDesam #TamilDevotional #SanatanaDharma"
        )
    else:
        # Sanitize any legacy "burned lyrics" mention
        meta_desc = meta_desc.replace("burned on screen", "with clean cinematic presentation")
        meta_desc = meta_desc.replace("burned-in lower-third lyrics", "clean devotional visuals")

    tags = meta.get("tags") or DEFAULT_TAGS.get(cat, ["GuruKulaDesam", "TamilDevotional"])

    print("\n" + "=" * 80)
    print(f"PUBLISHING MASTER FILM TO YOUTUBE: {title} ({tid})")
    print(f"Category: {cat.upper()} | Clean Master: {film_path.name} ({track.get('file_size_mb', 0)} MB)")
    print(f"Title: {meta_title}")
    print("=" * 80)

    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    body = {
        "snippet": {
            "title": meta_title[:100],  # YouTube title limit 100 chars
            "description": meta_desc[:5000], # YouTube description limit 5000 chars
            "tags": tags[:30],
            "categoryId": "27"  # Education / Devotional
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(str(film_path), chunksize=10 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    
    resp = None
    last_pct = 0
    print("  Uploading clean video chunks to YouTube...")
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            if pct - last_pct >= 20 or pct == 100:
                print(f"    Progress: {pct}%")
                last_pct = pct

    new_video_id = resp.get("id")
    print(f"  [UPLOAD SUCCESS] New YouTube Video ID: {new_video_id} -> https://youtu.be/{new_video_id}")

    # Immediately lock into persistent registry
    record_published_video(tid, new_video_id, meta_title, cat)

    # Add to Deity Playlist
    playlist_id = PLAYLIST_MAP.get(cat)
    if playlist_id:
        try:
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": new_video_id}
                    }
                }
            ).execute()
            print(f"  [PLAYLIST] Added to playlist {playlist_id} ({cat.upper()})")
        except Exception as pe:
            print(f"  [PLAYLIST NOTE] Could not insert to playlist {playlist_id}: {pe}")

    # Attach synchronized Tamil SRT captions if available
    srt_path = ROOT / "subtitles" / f"{tid}.srt"
    if srt_path.exists() and srt_path.stat().st_size > 50:
        try:
            print(f"  Uploading aligned SRT caption track ({srt_path.name}) to YouTube video {new_video_id}...")
            cap_media = MediaFileUpload(str(srt_path), mimetype="application/x-subrip", resumable=True)
            cap_body = {
                "snippet": {
                    "videoId": new_video_id,
                    "language": "ta",
                    "name": "தமிழ் (Tamil)",
                    "isDraft": False
                }
            }
            cap_resp = yt.captions().insert(
                part="snippet",
                body=cap_body,
                media_body=cap_media
            ).execute()
            print(f"  [CAPTION SUCCESS] Uploaded caption ID: {cap_resp.get('id')} for video {new_video_id}")
        except Exception as ce:
            print(f"  [CAPTION NOTE] Could not upload caption: {ce}")

    return new_video_id

def run_publisher_loop(limit=None, continuous=True, poll_interval=30):
    metadata_db = {}
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            metadata_db = json.load(f)

    published_count = 0
    print("=" * 80)
    print("GURU KULA DESAM — AUTONOMOUS MASTER FILMS PUBLISHER LAUNCHED")
    print("Guards Active: ZERO DUPLICATES | CLEAN CINEMATIC ONLY (NO BURNED LYRICS)")
    print(f"Mode: {'CONTINUOUS MONITOR' if continuous else 'SINGLE PASS'}")
    print("=" * 80)

    while True:
        try:
            registry = load_published_registry()
            manifest = load_manifest()
            tracks = manifest.get("completed_tracks", [])

            safe_candidates = []
            for t in tracks:
                safe, reason = is_track_safe_to_publish(t, registry, metadata_db)
                if safe:
                    safe_candidates.append(t)

            if safe_candidates:
                print(f"\n[Publisher] Found {len(safe_candidates)} verified CLEAN master films ready to publish.")
                try:
                    yt, cur_project = get_authenticated_service()
                except Exception as ce:
                    print(f"[Publisher Auth Error] {ce}")
                    time.sleep(poll_interval)
                    continue

                for track in safe_candidates:
                    if limit and published_count >= limit:
                        print(f"[Publisher] Limit of {limit} uploads reached.")
                        return

                    tid = track.get("track_id")
                    # Double-check registry in case an earlier iteration registered it
                    cur_registry = load_published_registry()
                    safe, reason = is_track_safe_to_publish(track, cur_registry, metadata_db)
                    if not safe:
                        print(f"  [Skipping] {tid}: {reason}")
                        continue

                    try:
                        new_id = publish_track(yt, track, metadata_db)
                        if new_id:
                            # Update manifest
                            cur_manifest = load_manifest()
                            for m in cur_manifest.get("completed_tracks", []):
                                if m.get("track_id") == tid:
                                    m["status"] = "PUBLISHED"
                                    m["youtube_id"] = new_id
                                    m["published_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                                    break
                            save_manifest(cur_manifest)
                            published_count += 1
                            print(f"[Publisher] Published count this session: {published_count}")
                            time.sleep(5)
                    except Exception as e:
                        err_str = str(e)
                        from tools.quota_rotator import mark_project_exhausted, get_next_available_youtube_service
                        if any(k in err_str for k in ["quotaExceeded", "rateLimitExceeded", "429"]):
                            print(f"\n[PROJECT QUOTA EXHAUSTED] Project {cur_project} hit daily API quota limit.")
                            mark_project_exhausted(cur_project)
                            try:
                                yt, cur_project = get_next_available_youtube_service()
                                print(f"[Quota Rotator] Successfully rotated to next project in pool: {cur_project}!")
                                continue
                            except Exception as re:
                                print(f"[Quota Rotator] All projects exhausted in pool: {re}")
                                if not continuous:
                                    return
                                wait_secs = 1800
                                print(f"Standing by for 30 minutes before re-checking pool...")
                                time.sleep(wait_secs)
                                break
                        elif any(k in err_str for k in ["uploadLimitExceeded", "Video Uploads per day"]):
                            print(f"\n[CHANNEL VELOCITY LIMIT] YouTube channel upload velocity limit reached.")
                            print(f"Uploaded {published_count} videos this run. YouTube applies a rolling 24-hour limit.")
                            if not continuous:
                                return
                            # Cooldown for 30 minutes before re-checking for rolling window slot availability
                            wait_secs = 1800
                            print(f"Standing by for rolling upload slot window (~{wait_secs//60} mins)...")
                            while wait_secs > 0:
                                chunk = min(60, wait_secs)
                                time.sleep(chunk)
                                wait_secs -= chunk
                                if wait_secs % 300 == 0 or wait_secs <= 60:
                                    print(f"  [Velocity Standby] ~{wait_secs//60} mins remaining...", flush=True)
                            print("[Velocity Standby] Cooldown elapsed. Testing upload slots...", flush=True)
                            break
                        else:
                            print(f"  [Publish Error] Failed uploading {tid}: {e}")
                            time.sleep(10)

            if not continuous:
                break

            print(f"[Publisher] Standing by... Checking for newly rendered clean master films in {poll_interval}s.", flush=True)
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("\n[Publisher] Terminating on user request.")
            break
        except Exception as ge:
            print(f"[Publisher Loop Error] {ge}")
            time.sleep(poll_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Master Films YouTube Publisher")
    parser.add_argument("--limit", type=int, default=None, help="Maximum videos to upload in this run")
    parser.add_argument("--once", action="store_true", help="Run a single pass and exit instead of continuous loop")
    parser.add_argument("--interval", type=int, default=30, help="Polling interval in seconds")
    args = parser.parse_args()

    run_publisher_loop(limit=args.limit, continuous=not args.once, poll_interval=args.interval)
