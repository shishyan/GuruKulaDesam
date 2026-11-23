#!/usr/bin/env python3
"""Publish verified 1080p botanical time-lapse masters as public to @influenzian (UCcJFqC7z0f-ARNcJadKiKpQ)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

TARGET_CHANNEL_ID = "UCcJFqC7z0f-ARNcJadKiKpQ"
TOKEN_PATH = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/token_influenzian.json")
RECEIPT_PATH = Path("/home/shishyan/GuruKulaDesam_Local/work/plant_growth_pilot/published_timelapses.json")

BANNED_CTA_PHRASES = (
    "subscribe",
    "hit the bell",
    "notification bell",
    "like and",
    "smash that like",
    "leave a comment",
    "comment below",
    "share this",
    "follow us",
    "follow for",
)

VIDEOS = [
    {
        "key": "lotus_bloom",
        "mp4": Path("/home/shishyan/GuruKulaDesam_Local/work/lotus_bloom_pilot/Lotus_Bloom_Timelapse_Pilot_1080p.mp4"),
        "thumbnail": Path("/home/shishyan/GuruKulaDesam_Local/work/lotus_bloom_pilot/keyframes/stage_04_full_bloom.jpg"),
        "title": "Sacred Pink Lotus Blooming Time-Lapse — Closed Dew Bud to Full Golden Dawn Blossom",
        "description": (
            "A continuous botanical macro time-lapse of a Sacred Pink Lotus (Nelumbo nucifera) "
            "awakening above mirror-still emerald pond water at golden dawn.\n\n"
            "00:00 Dew-Covered Closed Lotus Bud\n"
            "00:08 Outer Sepals Loosening at Dawn\n"
            "00:16 Cupped Half-Open Velvet Petals\n"
            "00:22 Full Blossom & Golden Stamen Crown\n\n"
            "#TimeLapse #LotusFlower #Botanical #MacroNature #PlantGrowth"
        ),
        "tags": [
            "lotus flower time lapse",
            "flower blooming time lapse",
            "Nelumbo nucifera",
            "sacred pink lotus",
            "macro botanical time lapse",
            "plant time lapse",
        ],
    },
    {
        "key": "sunflower_plant_growth",
        "mp4": Path("/home/shishyan/GuruKulaDesam_Local/work/plant_growth_pilot/Plant_Growth_Sunflower_Timelapse_1080p.mp4"),
        "thumbnail": Path("/home/shishyan/GuruKulaDesam_Local/work/plant_growth_pilot/keyframes/stage_05_full_bloom.jpg"),
        "title": "Sunflower Full Plant Growth Time-Lapse — Tiny Soil Sprout to Radiant Golden Bloom",
        "description": (
            "A continuous full-lifecycle botanical time-lapse of a compact Golden Sunflower "
            "(Helianthus annuus) emerging from moist forest soil and growing into full bloom "
            "under morning sunbeams.\n\n"
            "00:00 Tiny Dew-Covered Sprout & Cotyledons\n"
            "00:06 Young Four-Leaf Green Seedling\n"
            "00:12 Rising Stem & Spiky Green Star-Bud\n"
            "00:19 Bracts Peeling Back & Opening Petals\n"
            "00:24 Full Golden Sunflower Blossom\n\n"
            "#PlantGrowth #TimeLapse #Sunflower #Botany #NatureMacro"
        ),
        "tags": [
            "plant growth time lapse",
            "sunflower time lapse",
            "seed to flower time lapse",
            "sprout to bloom",
            "Helianthus annuus",
            "botanical macro time lapse",
        ],
    },
]


def assert_zero_cta(text: str, field: str) -> None:
    low = text.lower()
    for phrase in BANNED_CTA_PHRASES:
        if phrase in low:
            raise ValueError(f"ZERO-CTA invariant violated in {field}: matched '{phrase}'")


def get_youtube_client():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"OAuth token not found: {TOKEN_PATH}")

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    yt = build("youtube", "v3", credentials=creds)
    ch_resp = yt.channels().list(part="id,snippet", mine=True).execute()
    items = ch_resp.get("items", [])
    if not items:
        raise RuntimeError("No authenticated YouTube channel returned for token.")
    actual_id = items[0]["id"]
    actual_title = items[0]["snippet"].get("title", "")
    if actual_id != TARGET_CHANNEL_ID:
        raise RuntimeError(
            f"Channel mismatch: expected {TARGET_CHANNEL_ID}, got {actual_id} ({actual_title})"
        )
    print(f"Authenticated channel verified: {actual_id} ({actual_title})", flush=True)
    return yt


def upload_all() -> int:
    from googleapiclient.http import MediaFileUpload

    for item in VIDEOS:
        assert_zero_cta(item["title"], f"{item['key']}.title")
        assert_zero_cta(item["description"], f"{item['key']}.description")
        if not item["mp4"].exists():
            raise FileNotFoundError(f"Missing video MP4: {item['mp4']}")
        if not item["thumbnail"].exists():
            raise FileNotFoundError(f"Missing thumbnail JPG: {item['thumbnail']}")

    yt = get_youtube_client()
    results = []

    for item in VIDEOS:
        print(f"\n=== Uploading {item['key']} ({item['mp4'].stat().st_size} bytes) ===", flush=True)
        body = {
            "snippet": {
                "title": item["title"][:100],
                "description": item["description"],
                "tags": item["tags"],
                "categoryId": "28",
                "defaultLanguage": "en",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
            },
        }
        media = MediaFileUpload(
            str(item["mp4"]),
            chunksize=8 * 1024 * 1024,
            resumable=True,
            mimetype="video/mp4",
        )
        req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
        resp = None
        while resp is None:
            status, resp = req.next_chunk()
            if status:
                print(f"  upload progress: {int(status.progress() * 100)}%", flush=True)

        vid = resp["id"]
        watch_url = f"https://www.youtube.com/watch?v={vid}"
        print(f"  Uploaded video ID={vid} -> {watch_url}", flush=True)

        thumb_status = "skipped"
        try:
            yt.thumbnails().set(
                videoId=vid,
                media_body=MediaFileUpload(str(item["thumbnail"]), mimetype="image/jpeg"),
            ).execute()
            thumb_status = "set"
            print(f"  Thumbnail set cleanly for {vid}", flush=True)
        except Exception as exc:
            thumb_status = f"error: {exc}"
            print(f"  [Thumbnail Notice] {vid}: {exc}", flush=True)

        results.append(
            {
                "key": item["key"],
                "video_id": vid,
                "url": watch_url,
                "title": item["title"],
                "mp4": str(item["mp4"]),
                "thumbnail": str(item["thumbnail"]),
                "thumbnail_status": thumb_status,
            }
        )

    ids_csv = ",".join(r["video_id"] for r in results)
    verify_resp = yt.videos().list(part="snippet,status", id=ids_csv).execute()
    verified_by_id = {it["id"]: it for it in verify_resp.get("items", [])}
    print("\n=== POST-UPLOAD VERIFICATION ===", flush=True)
    for r in results:
        it = verified_by_id.get(r["video_id"])
        if not it:
            raise RuntimeError(f"Verification failed: video {r['video_id']} not returned by videos().list")
        ch_id = it["snippet"]["channelId"]
        priv = it["status"]["privacyStatus"]
        r["verified_channel_id"] = ch_id
        r["verified_privacy_status"] = priv
        print(f"  {r['video_id']} | channel={ch_id} | privacy={priv} | title={it['snippet']['title']}", flush=True)
        if ch_id != TARGET_CHANNEL_ID or priv != "public":
            raise RuntimeError(f"Unexpected verified state for {r['video_id']}: channel={ch_id}, privacy={priv}")

    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved receipt: {RECEIPT_PATH}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(upload_all())
