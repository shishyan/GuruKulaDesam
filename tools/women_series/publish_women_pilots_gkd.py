#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publish the 3 Women's Series Pilot Episodes (`ep01`, `ep02`, `ep03`) to `@guru-kula-desam`
(`UCPqB1A_WzpLJec6q69BOO3Q`) with multi-project OAuth quota rotation, Zero-CTA check,
custom v2 Movie-Poster thumbnail upload, and local + Drive thumbnail backup.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from women_3pillars_catalog import EPISODES, BANNED_CTA_PATTERNS  # noqa: E402

EXPECTED_CHANNEL_ID = "UCPqB1A_WzpLJec6q69BOO3Q"  # @guru-kula-desam
TOKEN_CANDIDATES = [
    Path("/home/shishyan/GitHub/GuruKulaDesam/data/credentials/token_gkd_839236964216.json"),
    Path("/home/shishyan/GitHub/GuruKulaDesam/data/credentials/token_472322435541.json"),
    Path("/home/shishyan/GitHub/GuruKulaDesam/data/credentials/token_gkd_942198183044.json"),
]
OUT_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots")
LOCAL_THUMB_BACKUP_DIR = Path("/home/shishyan/GuruKulaDesam_Local/thumbnails/@guru-kula-desam")
GDRIVE_THUMB_BACKUP_DIR = "gdrive:GuruKulaDesam/Assets/Thumbnails/@guru-kula-desam"

TAGS_MAP = {
    "ep01": [
        "Garbarakshambigai", "Thirukarukavur", "திருக்கருகாவூர்", "கர்ப்பரட்சாம்பிகை",
        "Amman Varalaru", "அம்மன் தல வரலாறு", "Tamil Devotional", "Guru Kula Desam",
        "குரு குல தேசம்", "Women Devotional Tamil",
    ],
    "ep02": [
        "Patti Vaithiyam", "பாட்டி வைத்தியம்", "Ulundhukali", "கருப்பு உளுந்தங்களி",
        "Ellurundai", "எள்ளுருண்டை", "Pirandai Thuvaiyal", "பிரண்டை துவையல்",
        "Women Health Tamil", "Guru Kula Desam",
    ],
    "ep03": [
        "Deepa Shastram", "தீப சாஸ்திரம்", "Kuthuvilakku", "குத்துவிளக்கு",
        "Mahalakshmi Poojai", "மகாலட்சுமி பூஜை", "Pooja Room Tips Tamil",
        "Pancha Deepam Oil", "Guru Kula Desam",
    ],
}


def get_youtube_client(token_path: Path):
    creds = Credentials.from_authorized_user_file(str(token_path))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
    yt = build("youtube", "v3", credentials=creds)
    ch = yt.channels().list(part="snippet", mine=True).execute()
    items = ch.get("items", [])
    assert items and items[0]["id"] == EXPECTED_CHANNEL_ID, f"Channel mismatch on {token_path.name}: {items}"
    return yt


def upload_one(ep: dict) -> dict:
    ep_id = ep["id"]
    slug = ep["slug"]
    mp4_path = OUT_ROOT / slug / f"{slug}.mp4"
    thumb_path = OUT_ROOT / slug / f"{slug}_Thumbnail.jpg"
    assert mp4_path.exists(), f"Missing {mp4_path}"
    assert thumb_path.exists(), f"Missing {thumb_path}"

    title = ep["yt_title"].replace("| @TamilDailyLife", "| Guru Kula Desam").strip()
    if len(title) > 100:
        title = title[:97].rstrip() + "..."
    desc = ep["yt_description"].replace("#TamilDailyLife", "#GuruKulaDesam").strip()

    for pat in BANNED_CTA_PATTERNS:
        assert not re.search(pat, f"{title}\n{desc}", re.IGNORECASE), f"CTA violation: {pat}"

    video_id = None
    used_token = None
    for tok in TOKEN_CANDIDATES:
        if not tok.exists():
            continue
        try:
            yt = get_youtube_client(tok)
            body = {
                "snippet": {
                    "title": title,
                    "description": desc,
                    "tags": TAGS_MAP[ep_id],
                    "categoryId": "27",
                    "defaultLanguage": "ta",
                    "defaultAudioLanguage": "ta",
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False,
                },
            }
            media = MediaFileUpload(str(mp4_path), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            print(f"[{ep_id}] Uploading {mp4_path.name} ({mp4_path.stat().st_size / 1e6:.1f} MB) via {tok.name}...", flush=True)
            resp = None
            while resp is None:
                status, resp = req.next_chunk()
                if status:
                    print(f"  [{ep_id}] {int(status.progress() * 100)}%", flush=True)
            video_id = resp["id"]
            used_token = tok
            print(f"[{ep_id}] PUBLISHED -> https://youtu.be/{video_id}", flush=True)
            break
        except HttpError as e:
            if e.resp.status in (403, 429) and "quotaExceeded" in str(e):
                print(f"  [{ep_id}] Quota exceeded on {tok.name}, rotating...", flush=True)
                continue
            raise

    assert video_id, f"Failed to upload {ep_id} across all tokens"

    # Backup thumbnail locally + Drive
    LOCAL_THUMB_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_jpg = LOCAL_THUMB_BACKUP_DIR / f"{video_id}.jpg"
    shutil.copy2(thumb_path, backup_jpg)
    subprocess.run(["rclone", "copyto", str(backup_jpg), f"{GDRIVE_THUMB_BACKUP_DIR}/{video_id}.jpg"], check=False)

    # Set custom thumbnail (isolated try/except so 403/429 never triggers duplicate video upload)
    thumb_status = "PENDING"
    for tok in [used_token] + [t for t in TOKEN_CANDIDATES if t != used_token]:
        if not tok or not tok.exists():
            continue
        try:
            yt = get_youtube_client(tok)
            yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")).execute()
            thumb_status = "SET"
            print(f"[{ep_id}] Custom thumbnail SET on {video_id}!", flush=True)
            break
        except HttpError as e:
            print(f"  [{ep_id}] Thumbnail set warn ({tok.name}): {e.resp.status}", flush=True)
            if e.resp.status in (403, 429):
                continue
            break

    return {
        "ep_id": ep_id,
        "slug": slug,
        "video_id": video_id,
        "url": f"https://youtu.be/{video_id}",
        "title": title,
        "thumb_status": thumb_status,
    }


def main():
    results = []
    for ep in EPISODES:
        results.append(upload_one(ep))
        time.sleep(3)
    Path("/tmp/women_series_gkd_published.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nALL_3_PUBLISHED_TO_GKD", flush=True)


if __name__ == "__main__":
    main()
