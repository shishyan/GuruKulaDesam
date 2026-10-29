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

GKD1_TOKENS_DIR = ROOT / "data" / "credentials" / "tokens_gurukuladesam"
PRIMARY_GKD1_TOKEN = ROOT / "data" / "credentials" / "token_gurukuladesam.json"
GKD1_EXHAUSTED_FILE = ROOT / "data" / "credentials" / "quota_exhausted_gurukuladesam.json"

INFLUENZIAN_TOKENS_DIR = ROOT / "data" / "credentials" / "tokens_influenzian"
PRIMARY_INFLUENZIAN_TOKEN = ROOT / "data" / "credentials" / "token_influenzian.json"
INFLUENZIAN_EXHAUSTED_FILE = ROOT / "data" / "credentials" / "quota_exhausted_influenzian.json"

GKD2_TOKENS_DIR.mkdir(parents=True, exist_ok=True)
GKD1_TOKENS_DIR.mkdir(parents=True, exist_ok=True)
INFLUENZIAN_TOKENS_DIR.mkdir(parents=True, exist_ok=True)

TARGET_CHANNEL_ID = "UCGUmNzaV_OUFbsNdHJQtaNQ"
TARGET_HANDLE = "@GuruKulaDesam2"

ORIGINAL_CHANNEL_ID = "UCz4dzcjahGaIb5dZCv32AmA"
ORIGINAL_HANDLE = "@GuruKulaDesam"

INFLUENZIAN_CHANNEL_ID = "UCmixCKV4uTv3wIp634IRLXg"
INFLUENZIAN_HANDLE = "@influenzian"

CHANNELS_CONFIG = {
    "@gurukuladesam": {
        "channel_id": ORIGINAL_CHANNEL_ID,
        "handle": ORIGINAL_HANDLE,
        "channel_title": "குரு குல தேசம் | நெறி தவறாமை",
        "category_ta": "நற்செய்கை",
        "pillar": "virtuous",
        "role_desc": "குரு குல தேசம் | நெறி தவறாமை >> @GuruKulaDesam (நற்செய்கை — Virtuous Shorts: Thirukkural, Vallalar & Universal Aram)",
        "channel_description": (
            "குரு குல தேசம் | நெறி தவறாமை — 📖 நற்செய்கை (Narseigai)\n\n"
            "திருக்குறள், வள்ளலார் அருட்பெருஞ்ஜோதி மற்றும் அறநெறிச் சிந்தனைகள் அடங்கிய நற்செய்கை Shorts அலைவரிசை.\n"
            "Sacred Tamil Virtuous Shorts Channel dedicated to Narseigai (நற்செய்கை — Righteous Action, Thirukkural, Vallalar Thiruvarutpa & Universal Dharma)."
        ),
        "tokens_dir": GKD1_TOKENS_DIR,
        "primary_token": PRIMARY_GKD1_TOKEN,
        "exhausted_file": GKD1_EXHAUSTED_FILE,
    },
    "@gurukuladesam2": {
        "channel_id": TARGET_CHANNEL_ID,
        "handle": TARGET_HANDLE,
        "channel_title": "குரு குல தேசம் | நன்றி மறவாமை",
        "category_ta": "நற்பண்பு",
        "pillar": "devotional",
        "role_desc": "குரு குல தேசம் | நன்றி மறவாமை >> @GuruKulaDesam2 (நற்பண்பு — Devotional Shorts: Murugan, Shiva, Amman, Vinayagar, Vishnu)",
        "channel_description": (
            "குரு குல தேசம் | நன்றி மறவாமை — 📖 நற்பண்பு (Narpanbu)\n\n"
            "தமிழ் பஞ்சாங்கம், திதி, நட்சத்திரம் மற்றும் நல்ல நேரத்திற்கு ஏற்ப அமைந்த தெய்வீக வழிபாட்டுப் பாடல்கள் (நற்பண்பு Shorts அலைவரிசை).\n"
            "Sacred Tamil Devotional Shorts Channel dedicated to Narpanbu (நற்பண்பு — Divine Gratitude, Panchangam-Aligned Bhakti Hymns for Murugan, Shiva, Amman, Vinayagar & Perumal)."
        ),
        "tokens_dir": GKD2_TOKENS_DIR,
        "primary_token": PRIMARY_GKD2_TOKEN,
        "exhausted_file": GKD2_EXHAUSTED_FILE,
    },
    "@guru-kula-desam": {
        "channel_id": "UCPqB1A_WzpLJec6q69BOO3Q",
        "handle": "@Guru-Kula-Desam",
        "channel_title": "குரு குல தேசம் | ஒழுக்கம் பிழையாமை",
        "category_ta": "நற்குணம்",
        "pillar": "master_video",
        "role_desc": "குரு குல தேசம் | ஒழுக்கம் பிழையாமை >> @Guru-Kula-Desam (நற்குணம் — Master Long-Form Video Channel)",
        "channel_description": (
            "குரு குல தேசம் | ஒழுக்கம் பிழையாமை — 📖 நற்குணம் (Narkunam)\n\n"
            "உலகப் பொதுமறை திருக்குறள், திருமுறைகள், திருப்புகழ், திருவருட்பா மற்றும் தெய்வீகத் தமிழ் இசைப் படைப்புகளின் முதன்மை முழுநீள அலைவரிசை.\n"
            "Master Sacred Tamil Long-Form Video Channel dedicated to Narkunam (நற்குணம் — Flawless Discipline, Pure Virtue & Eternal Tamil Wisdom)."
        ),
        "tokens_dir": ROOT / "data" / "credentials" / "tokens",
        "primary_token": ROOT / "data" / "credentials" / "token.json",
        "exhausted_file": ROOT / "data" / "credentials" / "quota_exhausted.json",
    },
    "@influenzian": {
        "channel_id": INFLUENZIAN_CHANNEL_ID,
        "handle": INFLUENZIAN_HANDLE,
        "channel_title": "Influenzian | காலமே உயிர்",
        "category_ta": "நற்சிந்தனை",
        "pillar": "spiritual",
        "role_desc": "Spiritual Shorts (Future — Asking the right questions, doing the right thing at the right time; Time as the ultimate limited credit to be wisely used)",
        "channel_description": (
            "Spiritual Shorts — Asking the right questions, doing the right thing at the right time. "
            "Understanding Time as the ultimate credit that is limited and to be wisely used."
        ),
        "tokens_dir": INFLUENZIAN_TOKENS_DIR,
        "primary_token": PRIMARY_INFLUENZIAN_TOKEN,
        "exhausted_file": INFLUENZIAN_EXHAUSTED_FILE,
    },
}

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtubepartner",
    "https://www.googleapis.com/auth/youtube.upload",
]

# Known active OAuth projects first (3 live verified projects: guru-kula-desam, home-manager-2026, lotusnaga)
ACTIVE_PROJECT_IDS = ["839236964216", "472322435541", "942198183044"]


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


def authorize_gurukuladesam2(project_id: str = None, port: int = 8089, channel_key: str = "@gurukuladesam") -> bool:
    from google_auth_oauthlib.flow import InstalledAppFlow

    cfg = CHANNELS_CONFIG.get(channel_key.lower(), CHANNELS_CONFIG["@gurukuladesam"])
    target_cid = cfg["channel_id"]
    target_hnd = cfg["handle"]

    candidates = get_candidate_secret_files()
    if project_id:
        candidates = [(pid, p) for pid, p in candidates if pid == project_id]

    if not candidates:
        print("[ERROR] No valid OAuth client_secret JSON files found.")
        return False

    pid, secret_path = candidates[0]
    print("=" * 75)
    print(f"🔐 AUTHORIZING YOUTUBE CHANNEL: {target_hnd} ({target_cid})")
    print(f"📁 Using OAuth Project: {pid} ({secret_path.name})")
    print("=" * 75)
    print("\n👉 IMPORTANT: When your browser opens:")
    print("   1. Pick your Google Account.")
    print(f"   2. When asked to choose a channel/brand account, select '{target_hnd}' ({target_cid}).")
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

    if cid != target_cid:
        print(f"\n⚠️ WARNING: The authorized channel ID is {cid} ({handle}), not {target_cid} ({target_hnd}).")
        print(f"   Please re-run and select {target_hnd}!")
        return False

    token_json = creds.to_json()
    project_token_path = cfg["tokens_dir"] / f"token_{pid}.json"
    project_token_path.write_text(token_json, encoding="utf-8")
    cfg["primary_token"].write_text(token_json, encoding="utf-8")

    print(f"💾 Saved token to: {cfg['primary_token']}")
    print(f"💾 Saved pool token to: {project_token_path}")

    print(f"\n🎉 SUCCESS! {target_hnd} ({target_cid}) is now authorized for autonomous Shorts publishing!")
    return True


def get_channel_youtube_service(channel_key: str = "@gurukuladesam"):
    """
    Returns an authenticated (youtube_service, project_id, channel_config) for
    @GuruKulaDesam (UCz4dzcjahGaIb5dZCv32AmA).
    """
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    cfg = CHANNELS_CONFIG.get(channel_key.lower(), CHANNELS_CONFIG["@gurukuladesam"])
    exhausted = {}
    if cfg["exhausted_file"].exists():
        try:
            exhausted = json.loads(cfg["exhausted_file"].read_text(encoding="utf-8"))
        except Exception:
            exhausted = {}

    token_files = sorted(cfg["tokens_dir"].glob("token_*.json"))
    if not token_files and cfg["primary_token"].exists():
        token_files = [cfg["primary_token"]]

    if not token_files:
        raise RuntimeError(
            f"No OAuth token found for {cfg['handle']}. "
            f"Run: python tools/authorize_gurukuladesam2.py --authorize --channel {channel_key}"
        )

    for tf in token_files:
        pid = tf.stem.replace("token_", "")
        try:
            raw_tok = json.loads(tf.read_text(encoding="utf-8"))
            cid_prefix = raw_tok.get("client_id", "").split("-")[0]
            if cid_prefix.isdigit():
                pid = cid_prefix
        except Exception:
            pass
        if pid in exhausted:
            if time.time() - exhausted[pid].get("exhausted_at", 0) < 12 * 3600:
                continue

        try:
            creds = Credentials.from_authorized_user_file(str(tf), SCOPES)
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                tf.write_text(creds.to_json(), encoding="utf-8")

            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            return yt, pid, cfg
        except Exception as e:
            print(f"[{cfg['handle']} Quota Pool] Token {tf.name} failed ({e}), trying next...")

    raise RuntimeError(f"All tokens for {cfg['handle']} are exhausted or invalid.")


def get_gurukuladesam2_youtube_service():
    yt, pid, _ = get_channel_youtube_service("@gurukuladesam")
    return yt, pid


def mark_gkd2_project_exhausted(pid: str, channel_key: str = "@gurukuladesam"):
    cfg = CHANNELS_CONFIG.get(channel_key.lower(), CHANNELS_CONFIG["@gurukuladesam"])
    exhausted = {}
    if cfg["exhausted_file"].exists():
        try:
            exhausted = json.loads(cfg["exhausted_file"].read_text(encoding="utf-8"))
        except Exception:
            pass
    exhausted[pid] = {
        "exhausted_at": time.time(),
        "date_str": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    cfg["exhausted_file"].write_text(json.dumps(exhausted, indent=2), encoding="utf-8")
    print(f"  [{cfg['handle']} Quota Pool] Project {pid} marked quota-exhausted.")


def check_status():
    from google.oauth2.credentials import Credentials

    for ch_key, cfg in CHANNELS_CONFIG.items():
        print("=" * 75)
        print(f"📊 CHANNEL STATUS: {cfg['handle']} ({cfg['channel_id']})")
        print("=" * 75)

        token_files = sorted(cfg["tokens_dir"].glob("token_*.json"))
        if cfg["primary_token"].exists() and cfg["primary_token"] not in token_files:
            token_files.insert(0, cfg["primary_token"])

        if not token_files:
            print(f"❌ No dedicated token found for {cfg['handle']} yet.")
            print(f"   Run: python tools/authorize_gurukuladesam2.py --authorize --channel {cfg['handle']}")
            continue

        for tf in token_files:
            try:
                creds = Credentials.from_authorized_user_file(str(tf), SCOPES)
                cid, title, handle = verify_token_channel(creds)
                match_str = f"✅ MATCHES {cfg['handle']}" if cid == cfg["channel_id"] else f"⚠️ MISMATCH ({handle})"
                print(f"  • {tf.name}: {title} ({handle} | {cid}) -> {match_str}")
            except Exception as e:
                print(f"  • {tf.name}: ❌ Error ({e})")
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Authorize and manage OAuth tokens for @GuruKulaDesam")
    ap.add_argument("--authorize", action="store_true", help="Launch browser OAuth login")
    ap.add_argument("--channel", type=str, default="@GuruKulaDesam", help="Channel handle (@GuruKulaDesam)")
    ap.add_argument("--project", type=str, default=None, help="Specific Google Cloud Project ID to authorize")
    ap.add_argument("--port", type=int, default=8089, help="Local OAuth callback port")
    ap.add_argument("--status", action="store_true", help="Check current token status")
    args = ap.parse_args()

    if args.authorize:
        authorize_gurukuladesam2(project_id=args.project, port=args.port, channel_key=args.channel)
    else:
        check_status()
