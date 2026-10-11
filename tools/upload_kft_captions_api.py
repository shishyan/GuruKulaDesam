import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

vid = 'KFtS403RfbY'
srt_path = 'production/subtitles/KFtS403RfbY.srt'

token_path = 'data/credentials/token_backup_guru-kula-desam.json'
creds = Credentials.from_authorized_user_file(token_path)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds)

try:
    print(f"Uploading caption track for {vid} via YouTube API...")
    media = MediaFileUpload(srt_path, mimetype='text/plain')
    body = {
        'snippet': {
            'videoId': vid,
            'language': 'ta',
            'name': 'தமிழ் (Tamil Verified Acoustic)',
            'isDraft': False
        }
    }
    res = yt.captions().insert(part='snippet', body=body, media_body=media).execute()
    print("SUCCESS! Caption track uploaded via API:", res)
except Exception as e:
    print("API caption upload failed or quotaExceeded:", e)
