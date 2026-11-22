#!/usr/bin/env python3
"""
Cloud/Local Multi-Channel Verified v2 Movie-Poster Thumbnail Sync Tool.
Pulls verified <VIDEO_ID>.jpg thumbnails from Google Drive (`GuruKulaDesam/Assets/Thumbnails/...`
via rclone if not already local) and applies them live across:
  1. @guru-kula-desam  (`production/verified_v2_upload_queue.json`)
  2. @GuruKulaDesam    (`production/verified_v2_queue_gurukuladesam.json`)
  3. @GuruKulaDesam2   (`production/verified_v2_queue_gurukuladesam2.json`)

Rotates automatically across all available Google Cloud OAuth 2.0 projects while respecting
YouTube's rolling 24h custom-thumbnail cap (~100/day per channel). Runs 100% cloud-natively
in GitHub Actions (`sync-verified-thumbnails.yml`) even when the local Linux PC is powered off.
"""
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

REPO_ROOT = Path(__file__).resolve().parent.parent
CREDS_DIR = REPO_ROOT / "data" / "credentials"
LOCAL_THUMB_BASE = Path("/home/shishyan/GuruKulaDesam_Local/thumbnails")
TMP_THUMB_BASE = Path("/tmp/gkd_verified_thumbnails")

CHANNELS = [
    {
        "name": "@guru-kula-desam",
        "channel_id": "UCPqB1A_WzpLJec6q69BOO3Q",
        "queue_file": REPO_ROOT / "production" / "verified_v2_upload_queue.json",
        "local_cache": LOCAL_THUMB_BASE / "@guru-kula-desam",
        "gdrive_subdir": "",
        "token_candidates": [
            CREDS_DIR / "token_472322435541.json",
            CREDS_DIR / "token_gkd_942198183044.json",
            CREDS_DIR / "token_gkd_839236964216.json",
            CREDS_DIR / "token.json",
            CREDS_DIR / "tokens" / "token_472322435541.json",
            CREDS_DIR / "tokens" / "token_942198183044.json",
        ],
    },
    {
        "name": "@GuruKulaDesam",
        "channel_id": "UCz4dzcjahGaIb5dZCv32AmA",
        "queue_file": REPO_ROOT / "production" / "verified_v2_queue_gurukuladesam.json",
        "local_cache": LOCAL_THUMB_BASE / "@GuruKulaDesam_v2",
        "gdrive_subdir": "@GuruKulaDesam_v2",
        "token_candidates": [
            CREDS_DIR / "token_gurukuladesam_472322435541.json",
            CREDS_DIR / "token_gurukuladesam_942198183044.json",
            CREDS_DIR / "token_gurukuladesam.json",
            CREDS_DIR / "tokens_gurukuladesam" / "token_472322435541.json",
            CREDS_DIR / "tokens_gurukuladesam" / "token_942198183044.json",
        ],
    },
    {
        "name": "@GuruKulaDesam2",
        "channel_id": "UCGUmNzaV_OUFbsNdHJQtaNQ",
        "queue_file": REPO_ROOT / "production" / "verified_v2_queue_gurukuladesam2.json",
        "local_cache": LOCAL_THUMB_BASE / "@GuruKulaDesam2_v2",
        "gdrive_subdir": "@GuruKulaDesam2_v2",
        "token_candidates": [
            CREDS_DIR / "token_942198183044.json",
            CREDS_DIR / "token_gurukuladesam2.json",
            CREDS_DIR / "tokens_gurukuladesam2" / "token_942198183044.json",
            CREDS_DIR / "tokens_gurukuladesam2" / "token_472322435541.json",
        ],
    },
]


def get_valid_yt_clients(cfg: dict) -> list[tuple[str, object]]:
    seen_refresh = set()
    clients = []
    for p in cfg["token_candidates"]:
        if not p.exists():
            continue
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            rt = raw.get("refresh_token", str(p.resolve()))
            if rt in seen_refresh:
                continue
            creds = Credentials.from_authorized_user_file(str(p))
            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            ch = yt.channels().list(part="id", mine=True).execute().get("items", [])
            if ch and ch[0]["id"] == cfg["channel_id"]:
                seen_refresh.add(rt)
                clients.append((p.name, yt))
        except Exception as e:
            if "quotaExceeded" not in str(e):
                print(f"[{cfg['name']}] Skipping token {p.name}: {str(e)[:120]}")
    return clients


def resolve_thumbnail_file(vid: str, cfg: dict, gdrive_base: str) -> Path | None:
    loc = cfg["local_cache"] / f"{vid}.jpg"
    if loc.exists():
        return loc
    tmp_dir = TMP_THUMB_BASE / cfg["name"].lstrip("@")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    dst = tmp_dir / f"{vid}.jpg"
    if dst.exists():
        return dst
    remote_dir = f"{gdrive_base}/{cfg['gdrive_subdir']}".rstrip("/")
    res = subprocess.run(
        ["rclone", "copyto", f"{remote_dir}/{vid}.jpg", str(dst)],
        capture_output=True,
        text=True,
    )
    return dst if (res.returncode == 0 and dst.exists()) else None


def sync_one_channel(cfg: dict, max_uploads: int, gdrive_base: str, dry_run: bool) -> None:
    qfile: Path = cfg["queue_file"]
    if not qfile.exists():
        return

    data = json.loads(qfile.read_text(encoding="utf-8"))
    pending = data.get("pending_verified_v2_queue", [])
    live_ids = set(data.get("live_verified_v2_ids", []))
    if not pending:
        print(f"[{cfg['name']}] All {len(live_ids)} verified v2 Movie-Poster thumbnails are already LIVE!")
        return

    if dry_run:
        print(f"[DRY RUN] [{cfg['name']}] {len(pending)} verified posters pending (top 5: {[x['id'] for x in pending[:5]]})")
        return

    clients = get_valid_yt_clients(cfg)
    if not clients:
        print(f"[{cfg['name']}] No active OAuth token with Cloud quota available right now ({len(pending)} pending).")
        return

    client_idx = 0
    uploaded = 0
    still_pending = []

    for i, item in enumerate(pending):
        if uploaded >= max_uploads:
            still_pending.extend(pending[i:])
            break
        vid = item["id"]
        jpg = resolve_thumbnail_file(vid, cfg, gdrive_base)
        if not jpg:
            print(f"[{cfg['name']}] Could not locate {vid}.jpg locally or on Google Drive; keeping queued.")
            still_pending.append(item)
            continue

        rate_limited = False
        ok = False
        while client_idx < len(clients):
            tname, yt = clients[client_idx]
            try:
                yt.thumbnails().set(
                    videoId=vid,
                    media_body=MediaFileUpload(str(jpg), mimetype="image/jpeg"),
                ).execute()
                uploaded += 1
                live_ids.add(vid)
                print(f"[{cfg['name']} #{uploaded}] LIVE ({tname}) -> {vid} ({item.get('views', 0)} views)", flush=True)
                ok = True
                break
            except HttpError as e:
                s = str(e)
                if "quotaExceeded" in s:
                    print(f"[{cfg['name']}] Cloud quota reached on {tname}, rotating...", flush=True)
                    client_idx += 1
                elif "uploadRateLimitExceeded" in s:
                    print(f"[{cfg['name']}] YouTube rolling 24h channel thumbnail limit active at {vid}; pausing cleanly.", flush=True)
                    rate_limited = True
                    break
                elif "doesn't have permissions to upload and set custom video thumbnails" in s:
                    print(f"[{cfg['name']}] Channel Intermediate Features not yet enabled on YouTube Studio; keeping queued.", flush=True)
                    rate_limited = True
                    break
                else:
                    print(f"[{cfg['name']}] HTTP error on {vid}: {e}", flush=True)
                    break

        if not ok:
            still_pending.append(item)
            if rate_limited or client_idx >= len(clients):
                still_pending.extend(pending[i + 1 :])
                break

    data["updated_at"] = datetime.now().isoformat()
    data["live_verified_v2_ids"] = sorted(list(live_ids))
    data["pending_verified_v2_queue"] = still_pending
    qfile.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{cfg['name']}] Summary: uploaded={uploaded} | live={len(live_ids)} | pending={len(still_pending)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-uploads", type=int, default=100)
    ap.add_argument("--gdrive-remote", default="gdrive:GuruKulaDesam/Assets/Thumbnails")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for cfg in CHANNELS:
        sync_one_channel(cfg, args.max_uploads, args.gdrive_remote, args.dry_run)


if __name__ == "__main__":
    main()
