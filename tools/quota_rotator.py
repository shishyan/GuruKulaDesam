#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/quota_rotator.py
Multi-Project YouTube Data API Quota Pool & Rotator for Guru Kula Desam.

Manages 8+ Google Cloud Projects (each offering 10,000 quota units / day),
enabling automatic failover when a project hits its daily quota limit.
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

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "data" / "credentials" / "projects"
TOKENS_DIR = ROOT / "data" / "credentials" / "tokens"
EXHAUSTED_FILE = ROOT / "data" / "credentials" / "quota_exhausted.json"

PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
TOKENS_DIR.mkdir(parents=True, exist_ok=True)

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtubepartner"
]

GURUKULA_CHANNEL_ID = "UCPqB1A_WzpLJec6q69BOO3Q"

def extract_project_id(filename: str) -> str:
    m = re.search(r"client_secret_(\d+)-", filename)
    if m:
        return m.group(1)
    m = re.search(r"(\d+)", filename)
    return m.group(1) if m else Path(filename).stem

def load_exhausted_registry() -> dict:
    if EXHAUSTED_FILE.exists():
        try:
            with open(EXHAUSTED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_exhausted_registry(reg: dict):
    with open(EXHAUSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2)

def mark_project_exhausted(project_id: str):
    reg = load_exhausted_registry()
    reg[project_id] = {
        "exhausted_at": time.time(),
        "date_str": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    save_exhausted_registry(reg)
    print(f"  [QUOTA POOL] Project {project_id} marked as quota-exhausted for current window.")

def is_project_exhausted(project_id: str) -> bool:
    reg = load_exhausted_registry()
    if project_id in reg:
        exhausted_at = reg[project_id].get("exhausted_at", 0)
        # Quota resets at 07:00 UTC (12:30 PM IST). If marked more than 12 hours ago, allow retry.
        if time.time() - exhausted_at < 12 * 3600:
            return True
    return False

def list_all_projects():
    projects = []
    for f in sorted(PROJECTS_DIR.glob("client_secret_*.json")):
        pid = extract_project_id(f.name)
        token_path = TOKENS_DIR / f"token_{pid}.json"
        
        # Check if legacy token.json matches this pid
        if not token_path.exists() and (ROOT / "data" / "credentials" / "token.json").exists():
            try:
                with open(ROOT / "data" / "credentials" / "token.json") as tf:
                    tdata = json.load(tf)
                if pid in tdata.get("client_id", ""):
                    # Sync to tokens dir
                    token_path.write_text(json.dumps(tdata, indent=2), encoding="utf-8")
            except Exception:
                pass

        has_token = token_path.exists()
        is_ex = is_project_exhausted(pid)
        projects.append({
            "project_id": pid,
            "secret_file": f,
            "token_file": token_path if has_token else None,
            "has_token": has_token,
            "is_exhausted": is_ex
        })
    return projects

def get_channel_info(creds):
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=creds)
    ch = yt.channels().list(part="snippet,id", mine=True).execute()
    for item in ch.get("items", []):
        return item.get("id"), item.get("snippet", {}).get("title")
    return None, None

def authorize_project(project_id: str = None):
    from google_auth_oauthlib.flow import InstalledAppFlow
    projects = list_all_projects()
    
    targets = [p for p in projects if not p["has_token"]]
    if project_id:
        targets = [p for p in projects if p["project_id"] == project_id]

    if not targets:
        print("[Quota Rotator] All configured projects already have authorized tokens!")
        return

    print(f"\n[Quota Rotator] Found {len(targets)} project(s) ready for authorization.")
    print("IMPORTANT: When your browser opens, select the account owning Guru Kula Desam (@guru-kula-desam).\n")

    for p in targets:
        pid = p["project_id"]
        secret_path = p["secret_file"]
        token_path = TOKENS_DIR / f"token_{pid}.json"

        print("=" * 70)
        print(f"AUTHORIZING PROJECT: {pid} ({secret_path.name})")
        print("=" * 70)
        try:
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Save token
            token_path.write_text(creds.to_json(), encoding="utf-8")
            
            # Check authorized channel
            cid, ctitle = get_channel_info(creds)
            print(f"  [SUCCESS] Token saved to: {token_path.name}")
            print(f"  [CHANNEL] Authorized for: {ctitle} (ID: {cid})")
            if cid != GURUKULA_CHANNEL_ID:
                print(f"  [NOTE] Channel is '{ctitle}'. Ensure this channel has access to upload to Guru Kula Desam.")
        except Exception as e:
            print(f"  [ERROR] Authorization failed for project {pid}: {e}")

def get_next_available_youtube_service():
    """
    Returns an authenticated YouTube API service client from the next
    available (non-exhausted) project in the pool.
    """
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    projects = list_all_projects()
    ready = [p for p in projects if p["has_token"] and not p["is_exhausted"]]

    if not ready:
        # If all tokens are marked exhausted, reset the pool and retry first
        print("[Quota Pool Alert] All available tokens marked exhausted; resetting pool.")
        save_exhausted_registry({})
        ready = [p for p in projects if p["has_token"]]

    if not ready:
        raise RuntimeError("No authorized tokens available in data/credentials/tokens/. Run 'python tools/quota_rotator.py --authorize' first.")

    for p in ready:
        pid = p["project_id"]
        token_path = p["token_file"]
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                token_path.write_text(creds.to_json(), encoding="utf-8")

            yt = build("youtube", "v3", credentials=creds)
            print(f"[Quota Pool] Active Project: {pid} (Token: {token_path.name})")
            return yt, pid
        except Exception as e:
            print(f"[Quota Pool] Failed initializing project {pid}: {e}. Trying next...")
            mark_project_exhausted(pid)

    raise RuntimeError("Failed to obtain a working YouTube client from any project in the pool.")

def status_report():
    projects = list_all_projects()
    print("=" * 80)
    print("GURU KULA DESAM — YOUTUBE API MULTI-PROJECT QUOTA POOL")
    print("=" * 80)
    print(f"Total Configured Google Cloud Projects: {len(projects)}")
    
    ready_count = 0
    for idx, p in enumerate(projects, 1):
        pid = p["project_id"]
        status = "READY" if p["has_token"] else "NEEDS_AUTH"
        if p["is_exhausted"]:
            status = "EXHAUSTED"
        if status == "READY":
            ready_count += 1
        print(f"  {idx}. Project {pid} | Status: {status:<10} | Secret: {p['secret_file'].name}")
    
    print("-" * 80)
    print(f"Active Ready Projects: {ready_count} / {len(projects)}")
    print(f"Total Combined Quota Pool: {ready_count * 10000:,} units/day (Potential: {len(projects) * 10000:,} units/day)")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Project YouTube Quota Rotator")
    parser.add_argument("--status", action="store_true", help="Print quota pool status")
    parser.add_argument("--authorize", action="store_true", help="Authorize projects needing OAuth tokens")
    parser.add_argument("--project", help="Specific project ID to authorize")
    args = parser.parse_args()

    if args.authorize:
        authorize_project(args.project)
    else:
        status_report()
