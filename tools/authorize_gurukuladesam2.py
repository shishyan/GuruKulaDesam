#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/authorize_gurukuladesam2.py
Dedicated Google OAuth 2.0 Authorization & Multi-Project Token Manager
for @gurukuladesam2 (Channel ID: UCGUmNzaV_OUFbsNdHJQtaNQ).

Supports:
- Authorizing a single project or rotating pool of Google Cloud projects for @gurukuladesam2
- Verifying that the selected account/brand channel matches UCGUmNzaV_OUFbsNdHJQtaNQ
- Saving isolated tokens to data/credentials/tokens_gurukuladesam2/ so @guru-kula-desam tokens are never overwritten
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

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "data" / "credentials" / "projects"
GKD2_TOKENS_DIR = ROOT / "data" / "credentials" / "tokens_gurukuladesam2"
PRIMARY_GKD2_TOKEN = ROOT / "data" / "credentials" / "token_gurukuladesam2.json"
GKD2_EXHAUSTED_FILE = ROOT / "data" / "credentials" / "quota_exhausted_gurukuladesam2.json"

GKD2_TOKENS_DIR.mkdir(parents=True, exist_ok=True)

TARGET_CHANNEL_ID = "UCGUmNzaV_OUFbsNdHJQtaNQ"
TARGET_HANDLE = "@gurukuladesam2"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtubepartner",
    "https://www.googleapis.com/auth/youtube.upload",
]

# Known active OAuth projects first
ACTIVE_PROJECT_IDS = ["440375337189", "472322435541"]


def extract_project_id(filename: str) -> str:
    m = re.search(r"client_secret_(\d+)-", filename)
    if m:
        return m.group(1)
    m = re.search(r"(\d+)", filename)
    return m.group(1) if m else Path(filename).stem


def get_candidate_secret_files() -> list[tuple[str, Path]]:
    candidates = []
    seen = set()

    # Check active project IDs first
    for pid in ACTIVE_PROJECT_IDS:
        for p in list(PROJECTS_DIR.glob(f"client_secret_{pid}*.json")) + list(ROOT.glob(f"client_secret_{pid}*.json")):
            if pid not in seen and p.exists():
                candidates.append((pid, p))
                seen.add(pid)

    # Check root client_secrets.json
    default_secret = ROOT / "data" / "credentials" / "client_secrets.json"
    if default_secret.exists():
        try:
            data = json.loads(default_secret.read_text(encoding="utf-8"))
            cid = data.get("installed", data.get("web", {})).get("client_id", "")
            pid = cid.split("-")[0] if "-" in cid else "default"
            if pid not in seen:
                candidates.append((pid, default_secret))
                seen.add(pid)
        except Exception:
            pass

    return candidates


def verify_token_channel(creds) -> tuple[str | None, str | None, str | None]:
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
    res = yt.channels().list(part="snippet,statistics", mine=True).execute()
    items = res.get("items", [])
    if not items:
        return None, None, None
    ch = items[0]
    cid = ch.get("id")
    title = ch.get("snippet", {}).get("title")
    handle = ch.get("snippet", {}).get("customUrl")
    return cid, title, handle


def authorize_gurukuladesam2(project_id: str = None, port: int = 8089) -> bool:
    from google_auth_oauthlib.flow import InstalledAppFlow

    candidates = get_candidate_secret_files()
    if project_id:
        candidates = [(pid, p) for pid, p in candidates if pid == project_id]

    if not candidates:
        print("[ERROR] No valid OAuth client_secret JSON files found.")
        return False

    pid, secret_path = candidates[0]
    print("=" * 75)
    print(f"🔐 AUTHORIZING YOUTUBE CHANNEL: {TARGET_HANDLE} ({TARGET_CHANNEL_ID})")
    print(f"📁 Using OAuth Project: {pid} ({secret_path.name})")
    print("=" * 75)
    print("\n👉 IMPORTANT: When your browser opens:")
    print("   1. Pick your Google Account.")
    print(f"   2. When asked to choose a channel/brand account, select 'GuruKulaDesam' ({TARGET_HANDLE}).")
    print("   3. Click 'Continue' / 'Allow' on all permissions.\n")

    flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
    creds = flow.run_local_server(
        port=port,
        prompt="consent select_account",
        open_browser=True,
        authorization_prompt_message="\n🌐 Please open this URL in your browser if it did not open automatically:\n{url}\n"
    )

    cid, title, handle = verify_token_channel(creds)
    print(f"\n✅ OAuth Flow Complete! Connected to Channel:")
    print(f"   • Title  : {title}")
    print(f"   • Handle : {handle}")
    print(f"   • ID     : {cid}")

    token_json = creds.to_json()
    project_token_path = GKD2_TOKENS_DIR / f"token_{pid}.json"
    project_token_path.write_text(token_json, encoding="utf-8")
    PRIMARY_GKD2_TOKEN.write_text(token_json, encoding="utf-8")

    print(f"💾 Saved token to: {PRIMARY_GKD2_TOKEN}")
    print(f"💾 Saved pool token to: {project_token_path}")

    if cid != TARGET_CHANNEL_ID:
        print(f"\n⚠️ WARNING: The authorized channel ID is {cid} ({handle}), not {TARGET_CHANNEL_ID} ({TARGET_HANDLE}).")
        print("   If you accidentally picked @guru-kula-desam, re-run this script and select @gurukuladesam2!")
        return False

    print(f"\n🎉 SUCCESS! {TARGET_HANDLE} ({TARGET_CHANNEL_ID}) is now authorized for autonomous Shorts publishing!")
    return True


def get_gurukuladesam2_youtube_service():
    """
    Returns an authenticated (youtube_service, project_id) specifically for @gurukuladesam2.
    Automatically rotates across authorized tokens in tokens_gurukuladesam2/.
    """
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    exhausted = {}
    if GKD2_EXHAUSTED_FILE.exists():
        try:
            exhausted = json.loads(GKD2_EXHAUSTED_FILE.read_text(encoding="utf-8"))
        except Exception:
            exhausted = {}

    token_files = sorted(GKD2_TOKENS_DIR.glob("token_*.json"))
    if PRIMARY_GKD2_TOKEN.exists() and PRIMARY_GKD2_TOKEN not in token_files:
        token_files.insert(0, PRIMARY_GKD2_TOKEN)

    if not token_files:
        raise RuntimeError(
            f"No OAuth token found for {TARGET_HANDLE}. "
            f"Run: python tools/authorize_gurukuladesam2.py --authorize"
        )

    for tf in token_files:
        pid = tf.stem.replace("token_", "")
        if pid in exhausted:
            if time.time() - exhausted[pid].get("exhausted_at", 0) < 12 * 3600:
                continue

        try:
            creds = Credentials.from_authorized_user_file(str(tf), SCOPES)
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                tf.write_text(creds.to_json(), encoding="utf-8")

            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            return yt, pid
        except Exception as e:
            print(f"[GKD2 Quota Pool] Token {tf.name} failed ({e}), trying next...")

    raise RuntimeError(f"All tokens for {TARGET_HANDLE} are exhausted or invalid.")


def mark_gkd2_project_exhausted(pid: str):
    exhausted = {}
    if GKD2_EXHAUSTED_FILE.exists():
        try:
            exhausted = json.loads(GKD2_EXHAUSTED_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    exhausted[pid] = {
        "exhausted_at": time.time(),
        "date_str": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    GKD2_EXHAUSTED_FILE.write_text(json.dumps(exhausted, indent=2), encoding="utf-8")
    print(f"  [GKD2 Quota Pool] Project {pid} marked quota-exhausted.")


def check_status():
    from google.oauth2.credentials import Credentials

    print("=" * 75)
    print(f"📊 CHANNEL STATUS: {TARGET_HANDLE} ({TARGET_CHANNEL_ID})")
    print("=" * 75)

    token_files = sorted(GKD2_TOKENS_DIR.glob("token_*.json"))
    if PRIMARY_GKD2_TOKEN.exists() and PRIMARY_GKD2_TOKEN not in token_files:
        token_files.insert(0, PRIMARY_GKD2_TOKEN)

    if not token_files:
        print(f"❌ No dedicated token found for {TARGET_HANDLE} yet.")
        print("   Run: python tools/authorize_gurukuladesam2.py --authorize")
        return False

    for tf in token_files:
        try:
            creds = Credentials.from_authorized_user_file(str(tf), SCOPES)
            cid, title, handle = verify_token_channel(creds)
            match_str = "✅ MATCHES @gurukuladesam2" if cid == TARGET_CHANNEL_ID else f"⚠️ MISMATCH ({handle})"
            print(f"  • {tf.name}: {title} ({handle} | {cid}) -> {match_str}")
        except Exception as e:
            print(f"  • {tf.name}: ❌ Error ({e})")
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Authorize and manage OAuth tokens for @gurukuladesam2")
    ap.add_argument("--authorize", action="store_true", help="Launch browser OAuth login for @gurukuladesam2")
    ap.add_argument("--project", type=str, default=None, help="Specific Google Cloud Project ID to authorize")
    ap.add_argument("--port", type=int, default=8089, help="Local OAuth callback port")
    ap.add_argument("--status", action="store_true", help="Check current @gurukuladesam2 token status")
    args = ap.parse_args()

    if args.authorize:
        authorize_gurukuladesam2(project_id=args.project, port=args.port)
    else:
        check_status()
