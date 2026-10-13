import sys, os, glob, json, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

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
            print(f"Token {t_file} init error: {e}")
            token_idx = (token_idx + 1) % len(TOKENS)
    raise RuntimeError("All tokens failed!")

def rotate_token():
    global token_idx
    token_idx = (token_idx + 1) % len(TOKENS)
    print(f"--> Rotated to token index {token_idx}: {TOKENS[token_idx]}")

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

with open('production/pending_live_siva_sync.json', 'r', encoding='utf-8') as f:
    targets = json.load(f)

log_file = 'production/siva_live_sync_log.jsonl'
completed_vids = set()
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as lf:
        for line in lf:
            if line.strip():
                try:
                    entry = json.loads(line)
                    completed_vids.add(entry['id'])
                except:
                    pass

pending = [v for v in targets if v not in completed_vids]
print(f"Total targets: {len(targets)} | Already synced: {len(completed_vids)} | Pending now: {len(pending)}")

yt, cur_token = get_yt_client()
success_desc = 0
success_srt = 0

for vid in pending:
    if vid not in live_meta:
        continue
    
    item = live_meta[vid]
    new_desc = item.get('description', '')
    title = item.get('title', '')
    srt_path = f"production/subtitles/{vid}.srt"
    
    print(f"\nProcessing {vid} ({title[:35]})...")
    desc_ok = False
    srt_ok = False
    
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
                desc_ok = True
                success_desc += 1
            break
        except Exception as e:
            err = str(e)
            if 'quotaExceeded' in err:
                print(f"  [DESC] Quota exceeded on {cur_token}. Rotating...")
                rotate_token()
                yt, cur_token = get_yt_client()
                retries -= 1
            elif 'forbidden' in err.lower():
                print(f"  [DESC] Forbidden (private/unowned): {vid}")
                break
            else:
                print(f"  [DESC] Error: {err[:60]}")
                break

    # 2. Upload Authentic SRT Subtitles
    if os.path.exists(srt_path):
        retries = 3
        while retries > 0:
            try:
                # Check existing captions
                caps = yt.captions().list(part='snippet', videoId=vid).execute()
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
                print(f"  [SRT] Uploaded authentic caption {res['id'][:20]}... for {vid}")
                srt_ok = True
                success_srt += 1
                break
            except Exception as e:
                err = str(e)
                if 'quotaExceeded' in err:
                    print(f"  [SRT] Quota exceeded on {cur_token}. Rotating...")
                    rotate_token()
                    yt, cur_token = get_yt_client()
                    retries -= 1
                elif 'forbidden' in err.lower():
                    print(f"  [SRT] Forbidden (private/unowned): {vid}")
                    break
                else:
                    print(f"  [SRT] Error: {err[:60]}")
                    break

    # Log completion
    with open(log_file, 'a', encoding='utf-8') as lf:
        lf.write(json.dumps({'id': vid, 'title': title, 'desc_ok': desc_ok, 'srt_ok': srt_ok, 'timestamp': time.time()}) + '\n')
    
    time.sleep(1)

print("\n" + "="*50)
print(f"BATCH RUN COMPLETE:")
print(f"  Descriptions updated: {success_desc}")
print(f"  SRTs uploaded: {success_srt}")
print("="*50)
