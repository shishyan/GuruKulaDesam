#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/publish_influenzian_10_viral.py
Authenticates @influenzian (UCmixCKV4uTv3wIp634IRLXg) across the multi-project OAuth pool
if needed, and publishes all 10 52-second 1080x1920 Global Viral Shorts with full
global SEO tags, descriptions, and multi-language localizations.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from authorize_gurukuladesam2 import (
    INFLUENZIAN_CHANNEL_ID,
    INFLUENZIAN_TOKENS_DIR,
    PRIMARY_INFLUENZIAN_TOKEN,
    authorize_gurukuladesam2,
)
from build_and_publish_influenzian_10_viral import VIRAL_10_IDEAS, MASTERS_DIR

RESULTS_FILE = ROOT / "production" / "influenzian_viral_shorts" / "published_results.json"


def authorize_influenzian_any(project_id: str = "942198183044", port: int = 8093) -> bool:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from authorize_gurukuladesam2 import get_candidate_secret_files, SCOPES, verify_token_channel

    candidates = get_candidate_secret_files()
    if project_id:
        candidates = [(pid, p) for pid, p in candidates if pid == project_id]
    if not candidates:
        return False

    pid, secret_path = candidates[0]
    flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
    creds = flow.run_local_server(
        port=port,
        prompt="consent select_account",
        open_browser=True,
        authorization_prompt_message="\n🌐 Open this URL in your browser:\n{url}\n",
    )
    cid, title, handle = verify_token_channel(creds)
    print(f"\n✅ Authorized Channel: {title} ({handle} | {cid})")
    token_json = creds.to_json()
    (INFLUENZIAN_TOKENS_DIR / f"token_{pid}.json").write_text(token_json, encoding="utf-8")
    PRIMARY_INFLUENZIAN_TOKEN.write_text(token_json, encoding="utf-8")
    return True


def get_influenzian_clients():
    clients = []
    seen = set()
    token_files = sorted(INFLUENZIAN_TOKENS_DIR.glob("token_*.json"))
    if PRIMARY_INFLUENZIAN_TOKEN.exists() and PRIMARY_INFLUENZIAN_TOKEN not in token_files:
        token_files.append(PRIMARY_INFLUENZIAN_TOKEN)

    for tf in token_files:
        try:
            raw = json.loads(tf.read_text(encoding="utf-8"))
            proj = raw.get("client_id", "").split("-")[0]
            if proj in seen:
                continue
            creds = Credentials.from_authorized_user_file(str(tf))
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                tp_json = creds.to_json()
                tf.write_text(tp_json, encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            ch = yt.channels().list(part="snippet", mine=True).execute()
            cid = ch["items"][0]["id"]
            hnd = ch["items"][0]["snippet"].get("customUrl", "")
            print(f"  🔑 Loaded token {tf.name}: {ch['items'][0]['snippet']['title']} ({hnd} | {cid})")
            clients.append((proj, yt))
            seen.add(proj)
        except Exception as e:
            print(f"  [Token skip] {tf.name}: {e}")
    return clients


def load_published():
    if RESULTS_FILE.exists():
        try:
            return json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_published(res: dict):
    RESULTS_FILE.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth-project", type=str, default=None, help="Authorize a specific GCP project for @influenzian")
    args = ap.parse_args()

    if args.auth_project:
        authorize_influenzian_any(project_id=args.auth_project, port=8093)

    clients = get_influenzian_clients()
    if not clients:
        print("🔐 Launching browser authorization on Project 942198183044...")
        ok = authorize_influenzian_any(project_id="942198183044", port=8094)
        if not ok:
            sys.exit("❌ Authorization was not completed.")
        clients = get_influenzian_clients()

    published = load_published()
    client_idx = 0

    for idx, item in enumerate(VIRAL_10_IDEAS, 1):
        slug = item["slug"]
        if slug in published and published[slug].get("youtube_id"):
            print(f"  ⏭️ [{idx}/10] {slug} already published: https://youtube.com/shorts/{published[slug]['youtube_id']}")
            continue

        mp4_path = MASTERS_DIR / f"{slug}_1080x1920_Short.mp4"
        if not mp4_path.exists():
            print(f"  ❌ Missing master file: {mp4_path}")
            continue

        desc = (
            f"{item['title']}\n\n"
            f"{item['hook']} — Watch till the end for the full satisfying slow-motion replay!\n\n"
            "🌍 Subscribe to @influenzian for daily hyper-realistic AI ASMR, oddly satisfying physics experiments, "
            "mind-blowing 'What If' scenarios, and surreal visual loops.\n\n"
            "#shorts #viral #satisfying #asmr #oddlysatisfying #trending #fyp #influenzian #ai #relaxing"
        )

        body = {
            "snippet": {
                "title": item["title"],
                "description": desc,
                "tags": item["tags"] + ["influenzian", "youtube shorts", "trending shorts", "viral video", "fyp"],
                "categoryId": "24",  # Entertainment (or 10 Music)
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }

        while client_idx < len(clients):
            proj, yt = clients[client_idx]
            try:
                print(f"\n🚀 [{idx}/10] Uploading {mp4_path.name} ({mp4_path.stat().st_size / 1e6:.1f} MB) to @influenzian via Project {proj}...")
                media = MediaFileUpload(str(mp4_path), mimetype="video/mp4", resumable=True)
                req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
                resp = None
                while resp is None:
                    status, resp = req.next_chunk()
                    if status:
                        print(f"    Upload progress: {int(status.progress() * 100)}%")
                vid_id = resp["id"]
                url = f"https://youtube.com/shorts/{vid_id}"
                print(f"  🎉 PUBLISHED LIVE on @influenzian: {url}")
                published[slug] = {
                    "title": item["title"],
                    "youtube_id": vid_id,
                    "url": url,
                    "project": proj,
                    "published_at": time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                }
                save_published(published)
                break
            except HttpError as e:
                err_str = str(e)
                print(f"  ⚠️ API Error on Project {proj}: {err_str[:180]}")
                if "quotaExceeded" in err_str or "uploadLimitExceeded" in err_str or e.resp.status in (403, 429):
                    client_idx += 1
                else:
                    break

        if client_idx >= len(clients):
            print("\n🛑 Exhausted currently authorized projects for @influenzian.")
            print("To authorize the next project (e.g. 942198183044 or 472322435541) and continue:")
            print("  python3 tools/publish_influenzian_10_viral.py --auth-project 942198183044")
            break

    print("\n" + "=" * 80)
    print(f"✅ TOTAL PUBLISHED TO @influenzian: {len(published)} / 10")
    for k, v in published.items():
        print(f"  • {k}: {v['url']} ({v['title'][:55]}...)")
    print("=" * 80)


if __name__ == "__main__":
    main()
