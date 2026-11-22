#!/usr/bin/env python3
"""
Cloud-Native Daily Publisher & Queue Drip Engine for @TamilDailyLife (`UCDdEZ6CPCr6tIzWdDY9mzxg`).

Runs daily at 06:00 AM IST (`cron: '30 0 * * *'`) via GitHub Actions (`.github/workflows/tamildailylife-daily.yml`)
completely independent of the local Linux workstation:

1. Pulls pre-rendered 1080p episodes (`TamilDailyLife_YYYY-MM-DD.mp4`), custom 16:9 v2 Movie-Poster
   thumbnails (`@TamilDailyLife/YYYY-MM-DD.jpg`), and `STORY_METADATA.json` / `tdl_publish_meta/`
   directly from Google Drive via `rclone` (`GURUKULADESAM_RCLONE_CONF`).
2. Publishes unpaid/pending episodes up to `today_ist` to `@TamilDailyLife` (`UCDdEZ6CPCr6tIzWdDY9mzxg`)
   via YouTube Data API v3 (`TAMILDAILYLIFE_OAUTH_TOKEN` / `TAMILDAILYLIFE_OAUTH_TOKEN_2`).
3. Tracks live YouTube Video IDs in `production/tamildailylife_published_registry.json` (and syncs back
   to Google Drive) so episodes never duplicate and any rolling-24h or quota pause resumes automatically
   on the next scheduled GitHub Actions run.
"""
import argparse
import datetime
import json
import subprocess
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

CHANNEL_ID = "UCDdEZ6CPCr6tIzWdDY9mzxg"
REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "production" / "tamildailylife_published_registry.json"
CREDS_DIR = REPO_ROOT / "data" / "credentials"
TMP_DIR = Path("/tmp/tdl_cloud_publish")

KNOWN_LIVE_EPISODES = {
    "2026-11-08": {"youtubeVideoId": "2C1bAaGDJKE", "url": "https://youtu.be/2C1bAaGDJKE"},
    "2026-11-09": {"youtubeVideoId": "pJUUK0lXylg", "url": "https://youtu.be/pJUUK0lXylg"},
    "2026-11-10": {"youtubeVideoId": "AXShW9izVt8", "url": "https://youtu.be/AXShW9izVt8"},
    "2026-11-11": {"youtubeVideoId": "djOaBcVurRk", "url": "https://youtu.be/djOaBcVurRk"},
    "2026-11-13": {"youtubeVideoId": "it2EEgkjHfQ", "url": "https://youtu.be/it2EEgkjHfQ"},
    "2026-11-14": {"youtubeVideoId": "Ia7D4RJ94KM", "url": "https://youtu.be/Ia7D4RJ94KM"},
    "2026-11-15": {"youtubeVideoId": "A9SDGW7fb6c", "url": "https://youtu.be/A9SDGW7fb6c"},
    "2026-11-16": {"youtubeVideoId": "ENnzXg9vuxg", "url": "https://youtu.be/ENnzXg9vuxg"},
    "2026-11-17": {"youtubeVideoId": "Izedww_NgWc", "url": "https://youtu.be/Izedww_NgWc"},
    "2026-11-18": {"youtubeVideoId": "O2kJx_Wqw-o", "url": "https://youtu.be/O2kJx_Wqw-o"},
    "2026-11-19": {"youtubeVideoId": "iYcqEcECAZ4", "url": "https://youtu.be/iYcqEcECAZ4"},
    "2026-11-20": {"youtubeVideoId": "49Td9yK78Po", "url": "https://youtu.be/49Td9yK78Po"},
}


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    else:
        reg = {"channel_id": CHANNEL_ID, "published": {}}
    for ds, info in KNOWN_LIVE_EPISODES.items():
        reg["published"].setdefault(ds, info)
    return reg


def get_yt_clients() -> list[tuple[str, object]]:
    candidates = [CREDS_DIR / "token_tamildailylife.json"]
    if (CREDS_DIR / "tokens_tamildailylife").is_dir():
        candidates.extend(sorted((CREDS_DIR / "tokens_tamildailylife").glob("*.json")))
    clients = []
    seen = set()
    for p in candidates:
        if not p.exists():
            continue
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            rt = raw.get("refresh_token", str(p))
            if rt in seen:
                continue
            creds = Credentials.from_authorized_user_file(str(p))
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                p.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            ch = yt.channels().list(part="id,snippet", mine=True).execute().get("items", [])
            if ch and ch[0]["id"] == CHANNEL_ID:
                seen.add(rt)
                clients.append((p.name, yt))
                print(f"[OAuth Active] Connected to {ch[0]['snippet']['title']} ({CHANNEL_ID}) via {p.name}")
        except Exception as e:
            print(f"[OAuth Skip] {p.name}: {str(e)[:120]}")
    return clients


def build_title_and_description(ds: str, meta_dir: Path, day_dir: Path) -> tuple[str, str]:
    manifest_file = meta_dir / "manifest.json"
    desc_file = meta_dir / f"desc_{ds}.txt"
    story_meta_file = day_dir / "STORY_METADATA.json"

    title = ""
    desc = ""
    if manifest_file.exists():
        mf = json.loads(manifest_file.read_text(encoding="utf-8"))
        if ds in mf:
            title = mf[ds].get("title", "")
    if desc_file.exists():
        desc = desc_file.read_text(encoding="utf-8").strip()

    if (not title or not desc) and story_meta_file.exists():
        sm = json.loads(story_meta_file.read_text(encoding="utf-8"))
        t_ta = sm.get("title_ta", "புராணக் கதை")
        p_ta = sm.get("purana_source", "புராணம்")
        if not title:
            title = f"{t_ta} | {p_ta} | @TamilDailyLife"
        if not desc:
            desc = (
                f"{t_ta} ({p_ta})\n\n"
                f"{sm.get('story_summary_ta', '')}\n\n"
                f"{sm.get('moral_and_action_ta', '')}\n\n"
                f"ஆலய தரிசனம்: {sm.get('temple_where_to_go_ta', '')}\n\n"
                f"சிவாயநம!\n\n"
                f"#TamilDailyLife #புராணக்கதைகள் #TamilDevotional #GuruKulaDesam #TamilStories"
            )

    safe_title = (title or f"புராண வரலாறு — {ds} | @TamilDailyLife").replace("<", "").replace(">", "").strip()
    if len(safe_title) > 98:
        safe_title = safe_title[:98].rsplit(" | ", 1)[0].strip()[:98]
    safe_desc = (desc or safe_title).replace("<", "").replace(">", "")[:4900]
    return safe_title, safe_desc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="", help="Target YYYY-MM-DD (defaults to draining up to today IST)")
    ap.add_argument("--max-uploads", type=int, default=2, help="Max episodes to upload per cloud run")
    ap.add_argument("--privacy", choices=["public", "unlisted"], default="public")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ist_now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)
    cutoff_date = args.date if args.date else ist_now.strftime("%Y-%m-%d")

    reg = load_registry()
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    meta_dir = TMP_DIR / "tdl_publish_meta"
    meta_dir.mkdir(parents=True, exist_ok=True)

    # Pull publish metadata manifest from Google Drive
    subprocess.run(
        ["rclone", "copy", "gdrive:GuruKulaDesam/Assets/tamil-daily-life/tdl_publish_meta/", str(meta_dir)],
        check=False,
    )

    # List available YYYY-MM-DD folders on Google Drive
    lsf = subprocess.run(
        ["rclone", "lsf", "gdrive:GuruKulaDesam/Assets/tamil-daily-life", "--dirs-only"],
        capture_output=True,
        text=True,
    )
    all_dates = sorted(
        d.strip().rstrip("/")
        for d in lsf.stdout.splitlines()
        if len(d.strip().rstrip("/")) == 10 and d.strip()[:4] in ("2026", "2027")
    )

    pending_dates = [
        ds for ds in all_dates
        if ds <= cutoff_date and ds not in reg["published"]
    ]
    if args.date and args.date not in reg["published"]:
        pending_dates = [args.date]

    if not pending_dates:
        print(f"All @TamilDailyLife episodes up through {cutoff_date} are already published ({len(reg['published'])} live).")
        REGISTRY_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    print(f"Pending @TamilDailyLife episodes <= {cutoff_date}: {pending_dates}")
    if args.dry_run:
        return

    clients = get_yt_clients()
    if not clients:
        print(
            "NOTICE: No active TAMILDAILYLIFE_OAUTH_TOKEN configured yet in GitHub Secrets. "
            "Episodes and thumbnails remain safely staged on Google Drive (`gdrive:GuruKulaDesam/Assets/tamil-daily-life/`) "
            "ready for automatic cloud publishing as soon as TAMILDAILYLIFE_OAUTH_TOKEN is added."
        )
        REGISTRY_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    uploaded = 0
    client_idx = 0
    for ds in pending_dates:
        if uploaded >= args.max_uploads:
            break
        day_tmp = TMP_DIR / ds
        day_tmp.mkdir(parents=True, exist_ok=True)
        mp4_dst = day_tmp / f"TamilDailyLife_{ds}.mp4"
        thumb_dst = day_tmp / f"{ds}.jpg"

        # Check if MP4 exists on Drive before downloading
        chk = subprocess.run(
            ["rclone", "lsf", f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{ds}/TamilDailyLife_{ds}.mp4"],
            capture_output=True,
            text=True,
        )
        if not chk.stdout.strip():
            print(f"[{ds}] Master MP4 not yet rendered on Google Drive — skipping.")
            continue

        print(f"[{ds}] Downloading master MP4 & thumbnail from Google Drive...")
        subprocess.run(
            ["rclone", "copyto", f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{ds}/TamilDailyLife_{ds}.mp4", str(mp4_dst)],
            check=True,
        )
        subprocess.run(
            ["rclone", "copyto", f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{ds}/STORY_METADATA.json", str(day_tmp / "STORY_METADATA.json")],
            check=False,
        )
        subprocess.run(
            ["rclone", "copyto", f"gdrive:GuruKulaDesam/Assets/Thumbnails/@TamilDailyLife/{ds}.jpg", str(thumb_dst)],
            check=False,
        )

        title, desc = build_title_and_description(ds, meta_dir, day_tmp)
        body = {
            "snippet": {
                "title": title,
                "description": desc,
                "tags": ["TamilDailyLife", "புராணக்கதைகள்", "TamilDevotional", "GuruKulaDesam", "TamilStories"],
                "categoryId": "27",
                "defaultLanguage": "ta",
                "defaultAudioLanguage": "ta",
            },
            "status": {
                "privacyStatus": args.privacy,
                "selfDeclaredMadeForKids": False,
            },
        }

        while client_idx < len(clients):
            tname, yt = clients[client_idx]
            try:
                req = yt.videos().insert(
                    part="snippet,status",
                    body=body,
                    media_body=MediaFileUpload(str(mp4_dst), chunksize=8 * 1024 * 1024, resumable=True),
                )
                resp = None
                while resp is None:
                    _, resp = req.next_chunk()
                vid = resp["id"]
                print(f"[{ds}] PUBLISHED -> https://youtu.be/{vid} (via {tname})")
                if thumb_dst.exists() and thumb_dst.stat().st_size < 2 * 1024 * 1024:
                    try:
                        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb_dst), mimetype="image/jpeg")).execute()
                        print(f"[{ds}] Applied v2 Movie-Poster thumbnail.")
                    except Exception as te:
                        print(f"[{ds}] Thumbnail note: {te}")
                reg["published"][ds] = {
                    "youtubeVideoId": vid,
                    "url": f"https://youtu.be/{vid}",
                    "title": title,
                    "publishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
                uploaded += 1
                break
            except HttpError as e:
                s = str(e)
                if "quotaExceeded" in s:
                    print(f"[{ds}] Quota reached on {tname}, rotating...")
                    client_idx += 1
                elif "uploadLimitExceeded" in s:
                    print(f"[{ds}] YouTube rolling 24h channel upload limit reached; will resume on next scheduled run.")
                    client_idx = len(clients)
                    break
                else:
                    print(f"[{ds}] HTTP error: {e}")
                    break
        mp4_dst.unlink(missing_ok=True)
        if client_idx >= len(clients):
            break

    reg["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    REGISTRY_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
