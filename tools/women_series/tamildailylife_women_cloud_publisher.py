#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloud-Native GitHub Actions Publisher for @TamilDailyLife Women's 3-Pillar Series (324 Episodes)
(`UCDdEZ6CPCr6tIzWdDY9mzxg` — தமிழர் பண்பாடு / வாழ்வியல் நெறி #TamilVirtues).

Runs autonomously on GitHub Actions (`tamildailylife-women-3pillars-cloud.yml`) with ZERO local PC dependency:
  1. Reads `data/women_3pillars_324/MASTER_324_WOMEN_SERIES_MANIFEST.json` & `production/tamildailylife_women_324_registry.json`.
  2. Checks Google Drive (`gdrive:GuruKulaDesam/Assets/women_3pillars_324/<pillar_folder>/<ep_folder>/`
     and `gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/`) for pre-rendered `.mp4` + `_Thumbnail.jpg`.
  3. Publishes up to `--max-uploads` due episodes in round-robin pillar order (`P1 -> P2 -> P3`) to `@TamilDailyLife`
     via YouTube Data API v3 (`TAMILDAILYLIFE_OAUTH_TOKEN` / `TAMILDAILYLIFE_OAUTH_TOKEN_2`).
  4. Persists published YouTube IDs in `production/tamildailylife_women_324_registry.json` & syncs back to Google Drive.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, ResumableUploadError
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

CHANNEL_ID = "UCDdEZ6CPCr6tIzWdDY9mzxg"
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "data" / "women_3pillars_324"
MANIFEST_PATH = DATA_ROOT / "MASTER_324_WOMEN_SERIES_MANIFEST.json"
REGISTRY_PATH = REPO_ROOT / "production" / "tamildailylife_women_324_registry.json"
CREDS_DIR = REPO_ROOT / "data" / "credentials"
TMP_DIR = Path("/tmp/tdl_women_cloud_pub")

PILLAR_FOLDERS = {
    "P1": "pillar1_108_amman_varalaru",
    "P2": "pillar2_108_patti_vaithiyam",
    "P3": "pillar3_108_pooja_deepa_shastram",
}

PILOT_GDRIVE_PATHS = {
    "P1_001": (
        "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep01_amman_garbarakshambigai/ep01_amman_garbarakshambigai.mp4",
        "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep01_amman_garbarakshambigai/ep01_amman_garbarakshambigai_Thumbnail.jpg",
    ),
    "P2_001": (
        "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep02_patti_vaithiyam_ulundhukali/ep02_patti_vaithiyam_ulundhukali.mp4",
        "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep02_patti_vaithiyam_ulundhukali/ep02_patti_vaithiyam_ulundhukali_Thumbnail.jpg",
    ),
    "P3_001": (
        "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep03_pooja_deepa_shastram/ep03_pooja_deepa_shastram.mp4",
        "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep03_pooja_deepa_shastram/ep03_pooja_deepa_shastram_Thumbnail.jpg",
    ),
}

BANNED_CTA = (
    r"\bsubscribe\b", r"\blike\b", r"\bcomment\b", r"\bshare\b",
    r"சப்ஸ்கிரைப்", r"(?:^|\s)லைக்(?:\s|$|[,.!?])", r"கமெண்ட்", r"(?:^|\s)ஷேர்(?:\s|$|[,.!?])",
)


def get_yt_clients() -> list[tuple[str, object]]:
    candidates = [CREDS_DIR / "token_tamildailylife.json"]
    if (CREDS_DIR / "tokens_tamildailylife").is_dir():
        candidates.extend(sorted((CREDS_DIR / "tokens_tamildailylife").glob("*.json")))
    local_drive_tok = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Tools/Credentials/token_tamildailylife.json")
    if local_drive_tok.exists():
        candidates.append(local_drive_tok)

    clients = []
    seen = set()
    for p in candidates:
        if not p.exists():
            continue
        raw = p.read_text(encoding="utf-8").strip()
        if not raw or raw in seen:
            continue
        seen.add(raw)
        try:
            creds = Credentials.from_authorized_user_file(str(p))
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                p.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds)
            ch = yt.channels().list(part="id", mine=True).execute().get("items", [])
            if ch and ch[0]["id"] == CHANNEL_ID:
                clients.append((p.name, yt))
        except Exception as exc:
            print(f"  [Token warn {p.name}]: {exc}")
    return clients


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {"channel": "@TamilDailyLife", "channel_id": CHANNEL_ID, "published": {}}


def save_registry(reg: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    reg["updated_at_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    REGISTRY_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run(
        ["rclone", "copyto", str(REGISTRY_PATH), "gdrive:GuruKulaDesam/Assets/women_3pillars_324/tamildailylife_women_324_registry.json"],
        check=False,
    )


def build_interleaved_order() -> list[str]:
    order = []
    for i in range(1, 109):
        for p in ("P1", "P2", "P3"):
            order.append(f"{p}_{i:03d}")
    return order


def rclone_exists(remote_path: str) -> bool:
    r = subprocess.run(["rclone", "lsf", remote_path], capture_output=True, text=True)
    return r.returncode == 0 and bool(r.stdout.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-uploads", type=int, default=1)
    ap.add_argument("--skip-pilots", action="store_true", help="Skip P1_001/P2_001/P3_001 if handled separately")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    reg = load_registry()
    # Pull latest cloud registry from GDrive if newer
    tmp_reg = Path("/tmp/gdrive_women_reg.json")
    if subprocess.run(["rclone", "copyto", "gdrive:GuruKulaDesam/Assets/women_3pillars_324/tamildailylife_women_324_registry.json", str(tmp_reg)], capture_output=True).returncode == 0 and tmp_reg.exists():
        remote_reg = json.loads(tmp_reg.read_text(encoding="utf-8"))
        reg["published"].update(remote_reg.get("published", {}))

    clients = [] if args.dry_run else get_yt_clients()
    if not args.dry_run and not clients:
        print("NOTICE: No valid TAMILDAILYLIFE_OAUTH_TOKEN configured yet; exiting cleanly.")
        return

    # Also detect already-live titles on @TamilDailyLife so we never duplicate an episode uploaded by another runner!
    live_titles = {}
    if clients:
        try:
            _, yt0 = clients[0]
            ch_info = yt0.channels().list(part="contentDetails", id=CHANNEL_ID).execute()["items"][0]
            uploads_pl = ch_info["contentDetails"]["relatedPlaylists"]["uploads"]
            pl_items = yt0.playlistItems().list(part="snippet", playlistId=uploads_pl, maxResults=50).execute().get("items", [])
            for it in pl_items:
                vid = it["snippet"]["resourceId"]["videoId"]
                live_titles[it["snippet"]["title"].strip()] = vid
        except Exception as e:
            print(f"  [Playlist pre-check warn]: {e}")

    uploaded = 0
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # First heal any already-published episode whose custom thumbnail hit quotaExceeded previously
    if clients and not args.dry_run:
        for ep_code, pub_info in list(reg["published"].items()):
            if pub_info.get("thumb_set") is False and pub_info.get("video_id"):
                vid_h = pub_info["video_id"]
                p_code = ep_code.split("_")[0]
                if ep_code in PILOT_GDRIVE_PATHS:
                    _, r_thumb = PILOT_GDRIVE_PATHS[ep_code]
                else:
                    sm = list((DATA_ROOT / PILLAR_FOLDERS[p_code]).glob(f"{ep_code}_*/episode_spec.json"))
                    if not sm:
                        continue
                    sp = json.loads(sm[0].read_text(encoding="utf-8"))
                    r_thumb = f"gdrive:GuruKulaDesam/Assets/women_3pillars_324/{PILLAR_FOLDERS[p_code]}/{sm[0].parent.name}/{sp['slug']}_Thumbnail.jpg"
                if rclone_exists(r_thumb):
                    lt = TMP_DIR / f"heal_{ep_code}.jpg"
                    subprocess.run(["rclone", "copyto", r_thumb, str(lt)], check=True)
                    for tok_name, yt in clients:
                        try:
                            yt.thumbnails().set(videoId=vid_h, media_body=MediaFileUpload(str(lt), mimetype="image/jpeg")).execute()
                            pub_info["thumb_set"] = True
                            save_registry(reg)
                            print(f"[Heal Thumbnail] Set verified v2 thumbnail on {ep_code} ({vid_h}) via {tok_name}!")
                            break
                        except HttpError as e:
                            print(f"  [Heal warn {ep_code} on {tok_name}]: {e.resp.status}")
                    lt.unlink(missing_ok=True)

    for ep_code in build_interleaved_order():
        if uploaded >= args.max_uploads:
            break
        if ep_code in reg["published"]:
            continue
        if args.skip_pilots and ep_code in PILOT_GDRIVE_PATHS:
            continue

        p_code = ep_code.split("_")[0]
        spec_matches = list((DATA_ROOT / PILLAR_FOLDERS[p_code]).glob(f"{ep_code}_*/episode_spec.json"))
        if not spec_matches:
            continue
        spec_path = spec_matches[0]
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        ep_folder_name = spec_path.parent.name
        slug = spec["slug"]

        title = spec["yt_title"].strip()
        if len(title) > 98:
            title = title[:95].rstrip() + "..."
        if title in live_titles:
            vid = live_titles[title]
            print(f"[{ep_code}] Already live on @TamilDailyLife ({vid}) — recording in registry.")
            reg["published"][ep_code] = {"video_id": vid, "url": f"https://youtu.be/{vid}", "title": title}
            save_registry(reg)
            continue

        if ep_code in PILOT_GDRIVE_PATHS:
            remote_mp4, remote_thumb = PILOT_GDRIVE_PATHS[ep_code]
        else:
            base_r = f"gdrive:GuruKulaDesam/Assets/women_3pillars_324/{PILLAR_FOLDERS[p_code]}/{ep_folder_name}"
            remote_mp4 = f"{base_r}/{slug}.mp4"
            remote_thumb = f"{base_r}/{slug}_Thumbnail.jpg"

        if not rclone_exists(remote_mp4):
            continue

        if args.dry_run:
            print(f"[DRY-RUN] Would publish {ep_code}: {title} from {remote_mp4}")
            uploaded += 1
            continue

        local_mp4 = TMP_DIR / f"{slug}.mp4"
        local_thumb = TMP_DIR / f"{slug}_Thumbnail.jpg"
        subprocess.run(["rclone", "copyto", remote_mp4, str(local_mp4)], check=True)
        has_thumb = rclone_exists(remote_thumb)
        if has_thumb:
            subprocess.run(["rclone", "copyto", remote_thumb, str(local_thumb)], check=True)

        desc = spec["yt_description"].strip()
        for pat in BANNED_CTA:
            assert not re.search(pat, f"{title}\n{desc}", re.IGNORECASE), f"CTA violation in {ep_code}"

        vid_id = None
        thumb_ok = False
        for tok_name, yt in clients:
            try:
                body = {
                    "snippet": {
                        "title": title,
                        "description": desc,
                        "tags": ["TamilDailyLife", "TamilVirtues", spec["thumb_badge_ta"], spec["thumb_main_ta"], "GuruKulaDesam"],
                        "categoryId": "27",
                        "defaultLanguage": "ta",
                        "defaultAudioLanguage": "ta",
                    },
                    "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
                }
                media = MediaFileUpload(str(local_mp4), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
                req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
                resp = None
                while resp is None:
                    _, resp = req.next_chunk()
                vid_id = resp["id"]
                print(f"[{ep_code}] PUBLISHED on @TamilDailyLife -> https://youtu.be/{vid_id} (via {tok_name})")
                if has_thumb and local_thumb.exists():
                    try:
                        yt.thumbnails().set(videoId=vid_id, media_body=MediaFileUpload(str(local_thumb), mimetype="image/jpeg")).execute()
                        thumb_ok = True
                        print(f"[{ep_code}] Custom thumbnail SET on {vid_id}")
                    except Exception as te:
                        print(f"[{ep_code}] Thumbnail warn: {te}")
                break
            except (HttpError, ResumableUploadError) as e:
                err_str = str(e)
                if "uploadLimitExceeded" in err_str:
                    print(f"  [{tok_name}] Channel rolling-24h uploadLimitExceeded (HTTP 400) — channel cap reached; yielding cleanly.")
                    local_mp4.unlink(missing_ok=True)
                    local_thumb.unlink(missing_ok=True)
                    return
                if "quotaExceeded" in err_str or getattr(getattr(e, "resp", None), "status", 0) in (403, 429):
                    print(f"  [{tok_name}] API quota/rate limit hit; rotating token...")
                    continue
                raise

        local_mp4.unlink(missing_ok=True)
        local_thumb.unlink(missing_ok=True)
        if vid_id:
            reg["published"][ep_code] = {"video_id": vid_id, "url": f"https://youtu.be/{vid_id}", "title": title, "thumb_set": thumb_ok}
            save_registry(reg)
            uploaded += 1
        else:
            print("Quota/rate-limit reached across tokens; yielding until next scheduled GitHub Actions run.")
            break


if __name__ == "__main__":
    main()
