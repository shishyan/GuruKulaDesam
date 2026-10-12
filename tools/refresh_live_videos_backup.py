import json, sys, pathlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_FILE = ROOT / 'data' / 'credentials' / 'token_backup_guru-kula-desam.json'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(CRED_FILE))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# Fetch all upload video IDs
uploads_playlist_id = 'UUPqB1A_WzpLJec6q69BOO3Q'
video_ids = []
page_token = None

print("Fetching all upload IDs from channel...")
while True:
    res = yt.playlistItems().list(
        part='contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=page_token
    ).execute()
    for item in res.get('items', []):
        video_ids.append(item['contentDetails']['videoId'])
    page_token = res.get('nextPageToken')
    if not page_token:
        break

print(f"Total uploaded videos: {len(video_ids)}")

live_videos = []
for i in range(0, len(video_ids), 50):
    chunk = video_ids[i:i+50]
    res = yt.videos().list(
        part='snippet,status,contentDetails,statistics',
        id=",".join(chunk)
    ).execute()
    live_videos.extend(res.get('items', []))

print(f"Fetched live records for {len(live_videos)} videos.")

with open(ROOT / 'production' / 'youtube_backup' / 'videos.json', 'w', encoding='utf-8') as f:
    json.dump(live_videos, f, indent=2, ensure_ascii=False)

print(f"Successfully refreshed production/youtube_backup/videos.json with {len(live_videos)} fresh live records!")
