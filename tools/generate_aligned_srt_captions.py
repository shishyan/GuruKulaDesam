#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_aligned_srt_captions.py
Generates line-synchronized Tamil SRT captions from audio and uploads them
as Closed Caption (CC) subtitle tracks to YouTube videos.

Workflow:
1. Takes the canonical lyrics from all_songs_lyrics_and_meanings.json and youtube_lyrics_overrides.json.
2. Uses Gemini Multimodal Audio analysis (gemini-2.5-flash / gemini-1.5-flash) to detect exact vocal entry
   and timestamp boundaries for each verse/couplet in the audio track.
3. Formats the aligned lyrics into standard .srt format.
4. Uploads the .srt file directly to the corresponding YouTube video as a native subtitle track.
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

ROOT = Path(__file__).resolve().parents[1]
SUBTITLES_DIR = ROOT / "subtitles"
SUBTITLES_DIR.mkdir(parents=True, exist_ok=True)

LYRICS_DB_FILE = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
OVERRIDES_FILE = ROOT / "production" / "youtube_lyrics_overrides.json"
REGISTRY_FILE = ROOT / "production" / "youtube_published_registry.json"
TOKEN_FILE = ROOT / "data" / "credentials" / "token.json"
SOURCE_AUDIO_DIR = ROOT / "source" / "youtube"
ENV_FILE = ROOT / ".env"

def load_gemini_client():
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key and ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env file.")
    return genai.Client(api_key=api_key)

def sec_to_srt_time(seconds: float) -> str:
    millis = int(round((seconds - int(seconds)) * 1000))
    total_sec = int(seconds)
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    sec = total_sec % 60
    return f"{hours:02d}:{minutes:02d}:{sec:02d},{millis:03d}"

def get_track_lyrics(track_id: str) -> str:
    if OVERRIDES_FILE.exists():
        try:
            with open(OVERRIDES_FILE, "r", encoding="utf-8") as f:
                overrides = json.load(f)
            if track_id in overrides:
                ref = overrides[track_id].get("ref")
                if ref and ref in overrides.get("_works", {}):
                    return overrides["_works"][ref].get("lyrics", "")
        except Exception:
            pass

    if LYRICS_DB_FILE.exists():
        try:
            with open(LYRICS_DB_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
            if track_id in db:
                return db[track_id].get("tamil_lyrics", "")
        except Exception:
            pass

    return ""

def align_lyrics_with_gemini(client, audio_path: Path, raw_lyrics: str) -> list:
    print(f"  Uploading audio {audio_path.name} to Gemini...")
    audio_upload = client.files.upload(file=str(audio_path))
    time.sleep(2)

    prompt = f"""Listen to this Tamil audio recording carefully.
The lyrics for this song are:
{raw_lyrics}

Your task is to transcribe and provide EXACT start and end timestamps (in seconds) for each sung stanza or couplet from the very first vocal entry to the end.
Only include timestamps when vocals are actually being sung (do not include instrumental pauses or prelude/interludes).

Return ONLY a valid JSON list of objects matching this exact schema:
[
  {{
    "start_sec": 33.2,
    "end_sec": 42.5,
    "tamil_text": "First line\\nSecond line"
  }}
]
"""

    print("  Aligning lyrics to audio vocal boundaries...")
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[audio_upload, prompt]
    )

    resp_text = response.text or ""
    m = re.search(r"\[.*\]", resp_text, re.DOTALL)
    if not m:
        raise ValueError(f"Could not parse JSON timestamp array from Gemini response:\n{resp_text[:300]}")

    return json.loads(m.group(0))

def build_srt_file(timed_segments: list, output_path: Path) -> Path:
    lines = []
    for idx, seg in enumerate(timed_segments, 1):
        start_str = sec_to_srt_time(float(seg["start_sec"]))
        end_str = sec_to_srt_time(float(seg["end_sec"]))
        text = seg.get("tamil_text", "").strip()
        lines.append(f"{idx}\n{start_str} --> {end_str}\n{text}\n")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path

def upload_srt_to_youtube(video_id: str, srt_path: Path):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    yt = build("youtube", "v3", credentials=creds)

    print(f"  Uploading SRT caption track to YouTube video {video_id}...")
    media = MediaFileUpload(str(srt_path), mimetype="application/x-subrip", resumable=True)
    body = {
        "snippet": {
            "videoId": video_id,
            "language": "ta",
            "name": "தமிழ் (Tamil)",
            "isDraft": False
        }
    }

    resp = yt.captions().insert(
        part="snippet",
        body=body,
        media_body=media
    ).execute()

    print(f"  [CAPTION SUCCESS] Uploaded caption ID: {resp.get('id')} for video {video_id}")
    return resp

def process_track(track_id: str, youtube_id: str = None, upload: bool = False):
    print("\n" + "=" * 70)
    print(f"GENERATING ALIGNED SRT SUBTITLES FOR: {track_id}")
    print("=" * 70)

    lyrics = get_track_lyrics(track_id)
    if not lyrics:
        print(f"  [Error] No lyrics found for track {track_id}")
        return None

    audio_path = SOURCE_AUDIO_DIR / f"{track_id}.m4a"
    if not audio_path.exists():
        print(f"  [Error] Audio file missing: {audio_path}")
        return None

    srt_path = SUBTITLES_DIR / f"{track_id}.srt"
    client = load_gemini_client()
    timed_segments = align_lyrics_with_gemini(client, audio_path, lyrics)
    build_srt_file(timed_segments, srt_path)
    print(f"  >>> Generated SRT: {srt_path} ({len(timed_segments)} segments)")

    if upload and youtube_id:
        try:
            upload_srt_to_youtube(youtube_id, srt_path)
        except Exception as e:
            print(f"  [Caption Upload Error] {e}")

def process_all_clean_tracks(upload: bool = False, limit: int = None):
    manifest_file = ROOT / "production" / "autonomous_master_production_manifest.json"
    if not manifest_file.exists():
        print(f"Manifest missing: {manifest_file}")
        return

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    tracks = [t for t in manifest.get("completed_tracks", []) if t.get("clean_cinematic")]
    print(f"Found {len(tracks)} clean cinematic tracks to process for subtitles.")

    count = 0
    for idx, track in enumerate(tracks, 1):
        if limit and count >= limit:
            break
        tid = track.get("track_id")
        srt_file = SUBTITLES_DIR / f"{tid}.srt"
        if srt_file.exists() and srt_file.stat().st_size > 50:
            print(f"[{idx}/{len(tracks)}] Already exists: {srt_file.name}")
            continue

        yid = track.get("youtube_id")
        print(f"\n[{idx}/{len(tracks)}] Generating SRT for: {track.get('title')} ({tid})")
        try:
            res = process_track(tid, youtube_id=yid, upload=upload)
            if res:
                count += 1
            time.sleep(3)
        except Exception as e:
            print(f"  [Error] Skipping {tid}: {e}")

    print(f"\nBatch SRT generation complete. Generated {count} new subtitle files.")

def main():
    parser = argparse.ArgumentParser(description="Generate and upload aligned SRT subtitles to YouTube")
    parser.add_argument("--track-id", help="Single track ID to process")
    parser.add_argument("--youtube-id", help="YouTube video ID to upload to")
    parser.add_argument("--batch", action="store_true", help="Process all clean tracks from manifest")
    parser.add_argument("--limit", type=int, default=None, help="Maximum tracks to process in batch")
    parser.add_argument("--upload", action="store_true", help="Upload generated SRT to YouTube via API")
    args = parser.parse_args()

    if args.track_id:
        process_track(args.track_id, youtube_id=args.youtube_id, upload=args.upload)
    elif args.batch:
        process_all_clean_tracks(upload=args.upload, limit=args.limit)
    else:
        print("Please specify --track-id or --batch to process subtitles.")

if __name__ == "__main__":
    main()
