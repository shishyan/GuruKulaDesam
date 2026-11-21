#!/usr/bin/env python3
"""
Cloud/Local Verified v2 Movie-Poster Thumbnail Sync Tool.
Pulls verified <VIDEO_ID>.jpg thumbnails from Google Drive (`GuruKulaDesam/Assets/Thumbnails/`
via rclone if not already local) and applies them live to `@guru-kula-desam` via the multi-project
OAuth pool while respecting YouTube's rolling 24h custom-thumbnail cap (~100/day).
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

EXPECTED_CHANNEL_ID = "UCPqB1A_WzpLJec6q69BOO3Q"
REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_FILE = REPO_ROOT / "production" / "verified_v2_upload_queue.json"
LOCAL_THUMB_CACHE = Path("/home/shishyan/GuruKulaDesam_Local/thumbnails/@guru-kula-desam")
TMP_THUMB_DIR = Path("/tmp/gkd_verified_thumbnails")


def get_valid_yt_clients() -> list[tuple[str, object]]:
    creds_dir = REPO_ROOT / "data" / "credentials"
    candidates = [
        creds_dir / "token_gkd_942198183044.json",
        creds_dir / "token_472322435541.json",
        creds_dir / "token_gkd_839236964216.json",
        creds_dir / "token.json",
        *sorted((creds_dir / "tokens").glob("token_*.json")),
    ]
    seen = set()
    clients = []
    for p in candidates:
        if not p.exists() or p.resolve() in seen:
            continue
        seen.add(p.resolve())
        try:
            creds = Credentials.from_authorized_user_file(str(p))
            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            ch = yt.channels().list(part="id", mine=True).execute().get("items", [])
            if ch and ch[0]["id"] == EXPECTED_CHANNEL_ID:
                clients.append((p.name, yt))
        except Exception as e:
            if "quotaExceeded" not in str(e):
                print(f"Skipping token {p.name}: {e}")
    return clients


def resolve_thumbnail_file(vid: str, gdrive_remote: str) -> Path | None:
    loc = LOCAL_THUMB_CACHE / f"{vid}.jpg"
    if loc.exists():
        return loc
    TMP_THUMB_DIR.mkdir(parents=True, exist_ok=True)
    dst = TMP_THUMB_DIR / f"{vid}.jpg"
    if dst.exists():
        return dst
    res = subprocess.run(
        ["rclone", "copyto", f"{gdrive_remote}/{vid}.jpg", str(dst)],
        capture_output=True,
        text=True,
    )
    return dst if (res.returncode == 0 and dst.exists()) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-uploads", type=int, default=100)
    ap.add_argument("--gdrive-remote", default="gdrive:GuruKulaDesam/Assets/Thumbnails")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not QUEUE_FILE.exists():
        print(f"No queue manifest found at {QUEUE_FILE}; nothing to sync.")
        return

    data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    pending = data.get("pending_verified_v2_queue", [])
    live_ids = set(data.get("live_verified_v2_ids", []))
    if not pending:
        print("All 304/304 verified v2 Movie-Poster thumbnails are already LIVE on YouTube!")
        return

    if args.dry_run:
        print(f"[DRY RUN] {len(pending)} verified posters pending (top 5: {[x['id'] for x in pending[:5]]})")
        return

    clients = get_valid_yt_clients()
    if not clients:
        raise SystemExit("No valid @guru-kula-desam OAuth token with Cloud quota available.")

    client_idx = 0
    uploaded = 0
    still_pending = []

    for i, item in enumerate(pending):
        if uploaded >= args.max_uploads:
            still_pending.extend(pending[i:])
            break
        vid = item["id"]
        jpg = resolve_thumbnail_file(vid, args.gdrive_remote)
        if not jpg:
            print(f"Could not locate {vid}.jpg locally or on {args.gdrive_remote}; keeping queued.")
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
                print(f"[{uploaded}] LIVE ({tname}) -> {vid} ({item.get('views', 0)} views)", flush=True)
                ok = True
                break
            except HttpError as e:
                s = str(e)
                if "quotaExceeded" in s:
                    print(f"Cloud quota reached on {tname}, rotating...", flush=True)
                    client_idx += 1
                elif "uploadRateLimitExceeded" in s:
                    print(f"YouTube rolling 24h channel thumbnail limit active at {vid}; pausing cleanly.", flush=True)
                    rate_limited = True
                    break
                else:
                    print(f"HTTP error on {vid}: {e}", flush=True)
                    break

        if not ok:
            still_pending.append(item)
            if rate_limited or client_idx >= len(clients):
                still_pending.extend(pending[i + 1 :])
                break

    data["updated_at"] = datetime.now().isoformat()
    data["live_verified_v2_ids"] = sorted(list(live_ids))
    data["pending_verified_v2_queue"] = still_pending
    QUEUE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Summary: uploaded={uploaded} | live={len(live_ids)} | pending={len(still_pending)}")


if __name__ == "__main__":
    main()
