import sys, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('data/credentials/tokens/token_472322435541.json')
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# Check existing captions for dpx7C3wuyio
caps = yt.captions().list(part='snippet', videoId='dpx7C3wuyio').execute()
print(f"Existing captions for dpx7C3wuyio: {len(caps.get('items', []))}")
for c in caps.get('items', []):
    cid = c['id']
    lang = c['snippet']['language']
    name = c['snippet']['name']
    track_kind = c['snippet']['trackKind']
    print(f"  - id={cid}, lang={lang}, name={name}, kind={track_kind}")
    # If standard user caption exists, delete or replace it
    if track_kind == 'standard':
        try:
            yt.captions().delete(id=cid).execute()
            print(f"    Deleted old caption {cid}")
        except Exception as e:
            print(f"    Could not delete {cid}: {e}")

# Upload fresh authentic SRT
srt_path = 'production/subtitles/dpx7C3wuyio.srt'
if os.path.exists(srt_path):
    media = MediaFileUpload(srt_path, mimetype='application/x-subrip')
    body = {
        'snippet': {
            'videoId': 'dpx7C3wuyio',
            'language': 'ta',
            'name': 'தமிழ் பாடல் வரிகள் (Lyrics)',
            'isDraft': False
        }
    }
    inserted = yt.captions().insert(part='snippet', body=body, media_body=media).execute()
    print("SUCCESS! Uploaded authentic SRT caption to dpx7C3wuyio:", inserted['id'])
else:
    print("SRT file not found:", srt_path)
