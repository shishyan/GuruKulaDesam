import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_FILE = Path('data/credentials/token.json')
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl', 'https://www.googleapis.com/auth/youtubepartner']

try:
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            print("Refreshing token...", flush=True)
            creds.refresh(Request())
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                f.write(creds.to_json())
            print("Token refreshed successfully!", flush=True)
        else:
            print("Credentials expired and cannot refresh!", flush=True)
            sys.exit(1)

    yt = build('youtube', 'v3', credentials=creds)
    ch_resp = yt.channels().list(part='snippet', mine=True).execute()
    for ch in ch_resp.get('items', []):
        print(f"Channel: {ch['snippet']['title']} (ID: {ch['id']})", flush=True)

    pl_resp = yt.playlists().list(part='snippet', mine=True, maxResults=50).execute()
    playlists = {}
    for pl in pl_resp.get('items', []):
        pid = pl['id']
        title = pl['snippet']['title']
        playlists[pid] = title
        print(f"Playlist: {pid} -> {title}", flush=True)

    with open('production/youtube_playlists.json', 'w', encoding='utf-8') as f:
        json.dump(playlists, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(playlists)} playlists to production/youtube_playlists.json", flush=True)

except Exception as e:
    print(f"Error: {e}", flush=True)
