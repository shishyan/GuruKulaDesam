#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/authorize_karmicgenie.py
Dedicated OAuth2 authorizer for @KarmicGenie (nagaraj957@gmail.com).
"""
import os, sys, json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
CLIENT_SECRETS_FILE = ROOT / "data" / "credentials" / "client_secrets.json"
OUT_TOKEN = ROOT / "data" / "credentials" / "token_karmicgenie.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]

def main():
    if not CLIENT_SECRETS_FILE.exists():
        print(f"❌ Missing client_secrets.json at {CLIENT_SECRETS_FILE}")
        return
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), scopes=SCOPES)
    print("\n" + "="*80)
    print("🔑 AUTHORIZING @KarmicGenie (nagaraj957@gmail.com)")
    print("Please select 'Karmic Genie' / 'nagaraj957@gmail.com' in the Google sign-in prompt!")
    print("="*80 + "\n")
    creds = flow.run_local_server(port=8089, prompt="consent", access_type="offline")
    OUT_TOKEN.parent.mkdir(parents=True, exist_ok=True)
    OUT_TOKEN.write_text(creds.to_json(), encoding="utf-8")
    
    youtube = build("youtube", "v3", credentials=creds)
    ch = youtube.channels().list(part="snippet", mine=True).execute()
    for item in ch.get("items", []):
        print(f"✅ Successfully Authorized: {item['snippet']['title']} ({item['snippet'].get('customUrl')}) [ID: {item['id']}]")
    print(f"💾 Token saved to: {OUT_TOKEN}")

if __name__ == "__main__":
    main()
