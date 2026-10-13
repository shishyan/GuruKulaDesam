import sys, os, glob, json, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

# List of 8 GCP tokens for quota rotation
TOKENS = sorted(glob.glob('data/credentials/tokens/*.json'))
token_idx = 0

def get_yt_client():
    global token_idx
    for _ in range(len(TOKENS)):
        t_file = TOKENS[token_idx]
        try:
            creds = Credentials.from_authorized_user_file(t_file)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
            return yt, t_file
        except Exception as e:
            print(f"Token {t_file} failed init: {e}")
            token_idx = (token_idx + 1) % len(TOKENS)
    raise RuntimeError("All tokens failed!")

def rotate_token():
    global token_idx
    token_idx = (token_idx + 1) % len(TOKENS)
    print(f"--> Rotated to token index {token_idx}: {TOKENS[token_idx]}")

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

with open('production/canonical_descriptions_repaired.json', 'r', encoding='utf-8') as f:
    repaired_21 = json.load(f)

# Combine high-priority targets needing live description & SRT update
targets = list(repaired_21.keys())
print(f"Total priority targets to sync live: {len(targets)}")

success_desc = 0
success_srt = 0

yt, cur_token = get_yt_client()

for vid in targets:
    if vid not in live_meta:
        continue
    
    item = live_meta[vid]
    new_desc = item.get('description', '')
    title = item.get('title', '')
    srt_path = f"production/subtitles/{vid}.srt"
    
    print(f"\nProcessing {vid} ({title[:40]})...")
    
    # 1. Update Description
    retries = 3
    while retries > 0:
        try:
            r = yt.videos().list(part='snippet', id=vid).execute()
            if r.get('items'):
                snip = r['items'][0]['snippet']
                snip['description'] = new_desc
                yt.videos().update(part='snippet', body={'id': vid, 'snippet': snip}).execute()
                print(f"  [DESC] Updated live description for {vid}")
                success_desc += 1
            break
        except Exception as e:
            if 'quotaExceeded' in str(e):
                print(f"  [DESC] Quota exceeded on {cur_token}. Rotating...")
                rotate_token()
                yt, cur_token = get_yt_client()
                retries -= 1
            else:
                print(f"  [DESC] Error updating {vid}: {e}")
                break
                
    # 2. Upload Authentic SRT Subtitles
    if os.path.exists(srt_path):
        retries = 3
        while retries > 0:
            try:
                # Check existing captions
                caps = yt.captions().list(part='snippet', videoId=vid).execute()
                has_clean_std = False
                for c in caps.get('items', []):
                    if c['snippet']['trackKind'] == 'standard':
                        try:
                            yt.captions().delete(id=c['id']).execute()
                        except:
                            pass
                
                media = MediaFileUpload(srt_path, mimetype='application/x-subrip')
                body = {
                    'snippet': {
                        'videoId': vid,
                        'language': 'ta',
                        'name': 'தமிழ் பாடல் வரிகள் (Lyrics)',
                        'isDraft': False
                    }
                }
                res = yt.captions().insert(part='snippet', body=body, media_body=media).execute()
                print(f"  [SRT] Uploaded authentic caption {res['id'][:25]}... for {vid}")
                success_srt += 1
                break
            except Exception as e:
                if 'quotaExceeded' in str(e):
                    print(f"  [SRT] Quota exceeded on {cur_token}. Rotating...")
                    rotate_token()
                    yt, cur_token = get_yt_client()
                    retries -= 1
                else:
                    print(f"  [SRT] Caption upload error for {vid}: {e}")
                    break
    
    time.sleep(1)

print(f"\n==========================================")
print(f"LIVE SYNC COMPLETED:")
print(f"  Descriptions updated: {success_desc}/{len(targets)}")
print(f"  SRT captions uploaded: {success_srt}/{len(targets)}")
print(f"==========================================")
