#!/usr/bin/env python3
"""
Batch-migrate all videos/Shorts from @GuruKulaDesam2 (UCGUmNzaV_OUFbsNdHJQtaNQ)
to @GuruKulaDesam using yt-dlp + YouTube Data API v3 multi-token quota rotation.

Tracks migrated IDs in production/shorts_metadata/gkd2_to_gkd_migration_state.json
so it can run safely in scheduled GitHub Actions batches without duplicates.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.authorize_gurukuladesam2 import get_channel_youtube_service

SOURCE_CHANNEL_ID = "UCGUmNzaV_OUFbsNdHJQtaNQ"
SOURCE_SHORTS_URL = f"https://www.youtube.com/channel/{SOURCE_CHANNEL_ID}/shorts"
STATE_FILE = ROOT / "production" / "shorts_metadata" / "gkd2_to_gkd_migration_state.json"


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"migrated": {}, "skipped": {}, "total_discovered": 0, "updated_at": ""}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def discover_source_videos() -> list[dict]:
    cmd = ["yt-dlp", "--flat-playlist", "-J", SOURCE_SHORTS_URL]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    entries = data.get("entries") or []
    # Reverse so oldest videos migrate first
    entries = list(reversed(entries))
    out = []
    seen = set()
    for e in entries:
        vid = e.get("id")
        if not vid or vid in seen:
            continue
        seen.add(vid)
        out.append({"id": vid, "title": (e.get("title") or "").strip()})
    return out


def fetch_target_existing_titles(yt) -> set[str]:
    titles: set[str] = set()
    try:
        ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
        uploads_pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
        page_token = None
        while True:
            res = yt.playlistItems().list(
                part="snippet",
                playlistId=uploads_pl,
                maxResults=50,
                pageToken=page_token,
            ).execute()
            for it in res.get("items", []):
                t = (it.get("snippet", {}).get("title") or "").strip().lower()
                if t:
                    titles.add(t)
            page_token = res.get("nextPageToken")
            if not page_token:
                break
    except Exception as e:
        print(f"[WARN] Could not list existing target titles: {e}", flush=True)
    return titles


def download_video_and_meta(vid: str, tmp_dir: Path) -> tuple[Path, dict]:
    url = f"https://www.youtube.com/watch?v={vid}"
    out_tmpl = str(tmp_dir / f"{vid}.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--write-info-json",
        "--no-playlist",
        "-o", out_tmpl,
        url,
    ]
    subprocess.run(cmd, check=True)
    mp4_path = tmp_dir / f"{vid}.mp4"
    if not mp4_path.exists():
        cands = list(tmp_dir.glob(f"{vid}.*"))
        mp4s = [p for p in cands if p.suffix.lower() in {".mp4", ".mkv", ".webm"}]
        if not mp4s:
            raise FileNotFoundError(f"Downloaded media not found for {vid}")
        mp4_path = mp4s[0]
    info_path = tmp_dir / f"{vid}.info.json"
    info = json.loads(info_path.read_text(encoding="utf-8")) if info_path.exists() else {}
    return mp4_path, info


def upload_to_target(yt, mp4_path: Path, info: dict, fallback_title: str) -> str:
    title = (info.get("title") or fallback_title or "Guru Kula Desam Short").strip()[:100]
    description = (info.get("description") or "").strip()[:4900]
    tags = [t for t in (info.get("tags") or []) if isinstance(t, str)][:30]
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(mp4_path), mimetype="video/mp4", resumable=True, chunksize=8 * 1024 * 1024)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    return resp["id"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--delay-sec", type=float, default=15.0)
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

    state = load_state()
    source_videos = discover_source_videos()
    state["total_discovered"] = len(source_videos)
    save_state(state)

    pending = [
        v for v in source_videos
        if v["id"] not in state["migrated"] and v["id"] not in state["skipped"]
    ]
    print(
        f"[@GuruKulaDesam2 -> @GuruKulaDesam] Discovered: {len(source_videos)} | "
        f"Migrated: {len(state['migrated'])} | Skipped: {len(state['skipped'])} | Pending: {len(pending)}",
        flush=True,
    )

    if not pending:
        print("MIGRATION COMPLETE: All videos from @GuruKulaDesam2 have been migrated to @GuruKulaDesam! Safe to delete @GuruKulaDesam2.", flush=True)
        return

    yt, cid, handle = get_channel_youtube_service("@gurukuladesam")
    print(f"Target authenticated: {handle} ({cid})", flush=True)
    existing_titles = fetch_target_existing_titles(yt)
    print(f"Existing videos on {handle}: {len(existing_titles)}", flush=True)

    uploaded_count = 0
    for item in pending:
        if uploaded_count >= args.batch_size:
            break
        vid = item["id"]
        title = item["title"]
        if title and title.lower() in existing_titles:
            print(f"[SKIP duplicate title] {vid} | {title[:70]}", flush=True)
            state["skipped"][vid] = {"title": title, "reason": "duplicate_title_on_target"}
            save_state(state)
            continue

        print(f"[{uploaded_count + 1}/{args.batch_size}] Migrating {vid} | {title[:70]}", flush=True)
        with tempfile.TemporaryDirectory(prefix="gkd2_mig_") as td:
            try:
                mp4_path, info = download_video_and_meta(vid, Path(td))
                new_id = upload_to_target(yt, mp4_path, info, title)
                state["migrated"][vid] = {
                    "target_id": new_id,
                    "target_url": f"https://www.youtube.com/shorts/{new_id}",
                    "title": info.get("title") or title,
                    "migrated_at": datetime.now(timezone.utc).isoformat(),
                }
                existing_titles.add((info.get("title") or title).strip().lower())
                save_state(state)
                uploaded_count += 1
                print(f"  OK -> https://www.youtube.com/shorts/{new_id} ({len(state['migrated'])}/{len(source_videos)})", flush=True)
                if uploaded_count < args.batch_size:
                    time.sleep(args.delay_sec)
            except HttpError as e:
                err_str = str(e)
                if "quotaExceeded" in err_str or "uploadLimitExceeded" in err_str:
                    print(f"  [QUOTA/LIMIT HIT] Stopping batch cleanly for next scheduled window: {err_str[:220]}", flush=True)
                    break
                print(f"  [ERROR] Failed on {vid}: {err_str[:250]}", flush=True)
            except Exception as e:
                print(f"  [ERROR] Failed on {vid}: {e}", flush=True)

    remaining = len([
        v for v in source_videos
        if v["id"] not in state["migrated"] and v["id"] not in state["skipped"]
    ])
    print(f"Batch complete: uploaded {uploaded_count} video(s). Remaining: {remaining}/{len(source_videos)}.", flush=True)


if __name__ == "__main__":
    main()
