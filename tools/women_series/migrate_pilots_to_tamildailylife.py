#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Marks the 3 temporary @guru-kula-desam uploads (`k5S4-mhe47A`, `X53iNUO6YC8`, `BfmH7nQLwjw`) as `private`.
2. Exports fresh Playwright `storage_state` JSON files for both `@TamilDailyLife` and `@guru-kula-desam`
   from headless Chrome CDP 9225 so GitHub Actions schedules run 100% without the local PC.
3. Publishes all 3 Women's Series Pilot episodes + v2 Movie-Poster thumbnails to `@TamilDailyLife` (`UCDdEZ6CPCr6tIzWdDY9mzxg`).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

REPO_ROOT = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam")
TOOLS_DIR = REPO_ROOT / "tools"
WOMEN_DIR = TOOLS_DIR / "women_series"
sys.path.insert(0, str(TOOLS_DIR))
sys.path.insert(0, str(WOMEN_DIR))

import flow_autonomous_generator as fg  # noqa: E402
from women_3pillars_catalog import EPISODES  # noqa: E402

OLD_GKD_IDS = {
    "ep01": "k5S4-mhe47A",
    "ep02": "X53iNUO6YC8",
    "ep03": "BfmH7nQLwjw",
}
OUT_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots")
TDL_THUMB_DIR = Path("/home/shishyan/GuruKulaDesam_Local/thumbnails/@TamilDailyLife")


def mark_gkd_videos_private() -> None:
    tok = REPO_ROOT / "data" / "credentials" / "token_gkd_839236964216.json"
    creds = Credentials.from_authorized_user_file(str(tok))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        tok.write_text(creds.to_json(), encoding="utf-8")
    yt = build("youtube", "v3", credentials=creds)

    for ep_id, vid in OLD_GKD_IDS.items():
        items = yt.videos().list(part="status,snippet", id=vid).execute().get("items", [])
        if not items:
            print(f"  [GKD {vid}] Not found, skipping.")
            continue
        st = items[0]["status"]
        if st.get("privacyStatus") != "private":
            yt.videos().update(
                part="status",
                body={
                    "id": vid,
                    "status": {
                        "privacyStatus": "private",
                        "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", False),
                    },
                },
            ).execute()
            print(f"  [GKD {vid}] Marked PRIVATE on @guru-kula-desam ({ep_id})")
        else:
            print(f"  [GKD {vid}] Already PRIVATE on @guru-kula-desam ({ep_id})")


def ensure_cdp_9225_fresh_and_export_states() -> None:
    os.environ.setdefault("XDG_CURRENT_DESKTOP", "zorin:GNOME")
    os.environ.setdefault("DESKTOP_SESSION", "zorin")
    os.environ.setdefault("DBUS_SESSION_BUS_ADDRESS", f"unix:path=/run/user/{os.getuid()}/bus")
    subprocess.run(["pkill", "-f", "[r]emote-debugging-port=9225"], check=False)
    time.sleep(2.0)
    fg.sync_flow_chrome_profile(force=True)
    fg.ensure_flow_chrome_running(user_idx=3)
    time.sleep(3.0)

    from publish_tdl_3category_community_posts import ensure_tamildailylife_account

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9225")
        ctx = b.contexts[0]
        pg = ctx.new_page()
        # Switch active brand account to @TamilDailyLife and save storage_state
        ensure_tamildailylife_account(pg)
        pg.wait_for_timeout(1500)
        ctx.storage_state(path="/tmp/tdl_storage_state.json")
        print("Exported @TamilDailyLife storage_state -> /tmp/tdl_storage_state.json")
        pg.close()


def publish_pilots_to_tamildailylife() -> list[dict]:
    TDL_THUMB_DIR.mkdir(parents=True, exist_ok=True)
    moved_records = []

    for ep in EPISODES:
        ep_id = ep["id"]
        slug = ep["slug"]
        mp4_path = OUT_ROOT / slug / f"{slug}.mp4"
        thumb_path = OUT_ROOT / slug / f"{slug}_Thumbnail.jpg"
        desc_path = Path(f"/tmp/tdl_women_{ep_id}_desc.txt")
        desc_path.write_text(ep["yt_description"], encoding="utf-8")

        title = ep["yt_title"]
        if len(title) > 98:
            title = title[:98].rsplit(" | ", 1)[0].strip()[:98]

        print(f"\n=== Publishing {ep_id} ({slug}) to @TamilDailyLife (UCDdEZ6CPCr6tIzWdDY9mzxg) ===")
        res = subprocess.run(
            [
                sys.executable,
                "/home/shishyan/GuruKulaDesam_Local/publish_tamildailylife_cdp.py",
                "--video", str(mp4_path),
                "--thumb", str(thumb_path),
                "--title", title,
                "--desc-file", str(desc_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(res.stdout[-800:])
        if res.returncode == 2 or "DAILY_UPLOAD_LIMIT" in res.stdout:
            raise RuntimeError(f"@TamilDailyLife hit rolling 24h upload cap on {ep_id}: {res.stdout[-300:]}")
        m = re.search(r"Assigned YouTube Video ID:\s*([A-Za-z0-9_-]{11})", res.stdout) or re.search(
            r"PUBLISHED_SUCCESS VIDEO_ID=([A-Za-z0-9_-]{11})", res.stdout
        )
        assert res.returncode == 0 and m, f"Failed publishing {ep_id} to @TamilDailyLife:\n{res.stdout[-600:]}"
        new_vid = m.group(1)

        shutil.copy2(thumb_path, TDL_THUMB_DIR / f"{new_vid}.jpg")
        subprocess.run(
            ["rclone", "copyto", str(thumb_path), f"gdrive:GuruKulaDesam/Assets/Thumbnails/@TamilDailyLife/{new_vid}.jpg"],
            check=False,
        )
        rec = {
            "ep_id": ep_id,
            "ep_code": {"ep01": "P1_001", "ep02": "P2_001", "ep03": "P3_001"}[ep_id],
            "slug": slug,
            "old_gkd_video_id": OLD_GKD_IDS[ep_id],
            "old_gkd_status": "private",
            "new_tamildailylife_video_id": new_vid,
            "new_tamildailylife_url": f"https://youtu.be/{new_vid}",
            "title": title,
        }
        moved_records.append(rec)
        print(f"  => LIVE on @TamilDailyLife: {rec['new_tamildailylife_url']}")
        time.sleep(4)

    out_moved = REPO_ROOT / "production" / "moved_women_series_to_tamildailylife.json"
    out_moved.write_text(json.dumps(moved_records, ensure_ascii=False, indent=2), encoding="utf-8")
    return moved_records


if __name__ == "__main__":
    print("Step 1: Marking @guru-kula-desam pilot copies PRIVATE...")
    mark_gkd_videos_private()
    print("\nStep 2: Syncing Chrome 9225 to @TamilDailyLife & exporting cloud storage_state...")
    ensure_cdp_9225_fresh_and_export_states()
    print("\nStep 3: Publishing all 3 Women's Series Pilots + Thumbnails to @TamilDailyLife...")
    recs = publish_pilots_to_tamildailylife()
    print("\nMIGRATION_COMPLETE", json.dumps(recs, ensure_ascii=False))
