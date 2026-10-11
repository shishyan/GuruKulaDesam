import sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
SUB_DIR = ROOT / 'production' / 'subtitles'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = Credentials.from_authorized_user_file(str(ROOT / 'data/credentials/token.json'))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

def upload_caption(video_id: str, srt_file: pathlib.Path):
    if not srt_file.exists():
        print(f"SRT file not found: {srt_file}")
        return False
        
    body = {
        'snippet': {
            'videoId': video_id,
            'language': 'ta',
            'name': 'தமிழ் பாடல் வரிகள் (Tamil Lyrics)',
            'isDraft': False
        }
    }
    media = MediaFileUpload(str(srt_file), mimetype='application/x-subrip', resumable=True)
    try:
        req = yt.captions().insert(part='snippet', body=body, media_body=media)
        res = req.execute()
        print(f"SUCCESS: Uploaded caption track {res.get('id')} for video {video_id}")
        return True
    except Exception as e:
        print(f"FAILED to upload caption for {video_id}: {e}")
        return False

# Also enable yt:cc=on tag so YouTube shows captions automatically by default
def enable_default_captions_tag(video_id: str):
    try:
        r = yt.videos().list(part='snippet', id=video_id).execute()
        if not r.get('items'): return False
        snippet = r['items'][0]['snippet']
        tags = snippet.get('tags', [])
        if 'yt:cc=on' not in tags:
            tags.append('yt:cc=on')
            body = {
                'id': video_id,
                'snippet': {k: snippet[k] for k in ('title', 'categoryId', 'description', 'defaultLanguage', 'defaultAudioLanguage') if k in snippet}
            }
            body['snippet']['tags'] = tags
            yt.videos().update(part='snippet', body=body).execute()
            print(f"SUCCESS: Enabled default auto-captions tag (yt:cc=on) for {video_id}")
            return True
        else:
            print(f"yt:cc=on tag already present on {video_id}")
            return True
    except Exception as e:
        print(f"FAILED to update tags for {video_id}: {e}")
        return False

if __name__ == '__main__':
    # Test on Muthai Tharu (4s48KQnjSyQ)
    test_id = '4s48KQnjSyQ'
    srt = SUB_DIR / f"{test_id}.srt"
    if not srt.exists():
        # Fallback to muthaitharu.srt
        srt = SUB_DIR / "muthaitharu.srt"
    print(f"Testing caption sync on {test_id} using {srt}...")
    upload_caption(test_id, srt)
    enable_default_captions_tag(test_id)
