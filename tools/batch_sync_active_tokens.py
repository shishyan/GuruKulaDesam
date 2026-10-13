import sys, os, glob, json, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

# Active tokens pool (5 tokens currently verified with quota)
ACTIVE_TOKENS = [
    'data/credentials/tokens/token_440375337189.json',
    'data/credentials/tokens/token_472322435541.json',
    'data/credentials/tokens/token_801831475660.json',
    'data/credentials/tokens/token_839236964216.json',
    'data/credentials/tokens/token_942198183044.json'
]
token_idx = 0

def get_yt_client():
    global token_idx
    attempts = 0
    while attempts < len(ACTIVE_TOKENS):
        t_file = ACTIVE_TOKENS[token_idx]
        try:
            creds = Credentials.from_authorized_user_file(t_file)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
            return yt, t_file
        except Exception as e:
            print(f"Token {t_file} error: {e}")
            token_idx = (token_idx + 1) % len(ACTIVE_TOKENS)
            attempts += 1
    return None, None

def rotate_token():
    global token_idx
    token_idx = (token_idx + 1) % len(ACTIVE_TOKENS)
    print(f"--> Rotated to token index {token_idx}: {ACTIVE_TOKENS[token_idx]}")

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

with open('production/next_batch_500_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

log_file = 'production/batch_token_sync_log.jsonl'
done_ids = set()
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as lf:
        for line in lf:
            if line.strip():
                try:
                    d = json.loads(line)
                    done_ids.add(d['id'])
                except:
                    pass

pending = [item for item in queue if item['id'] not in done_ids]
print(f"Total in queue: {len(queue)} | Already processed: {len(done_ids)} | Pending this run: {len(pending)}")

yt, cur_token = get_yt_client()
if not yt:
    print("No active tokens available!")
    sys.exit(1)

success_desc = 0
success_srt = 0
all_exhausted = False

for item in pending:
    vid = item['id']
    title = item['title']
    meta = live_meta.get(vid, {})
    new_desc = meta.get('description', '')
    srt_path = f"production/subtitles/{vid}.srt"
    
    print(f"\nProcessing {vid} ({title[:35]})...")
    desc_ok = False
    srt_ok = False
    
    # 1. Update Description
    retries = len(ACTIVE_TOKENS)
    while retries > 0:
        try:
            r = yt.videos().list(part='snippet', id=vid).execute()
            if r.get('items'):
                snip = r['items'][0]['snippet']
                snip['description'] = new_desc
                yt.videos().update(part='snippet', body={'id': vid, 'snippet': snip}).execute()
                print(f"  [DESC] Updated description for {vid}")
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

    if retries == 0:
        print("ALL ACTIVE TOKENS EXHAUSTED FOR DESCRIPTIONS!")
        all_exhausted = True
        break

    # 2. Upload Authentic SRT Subtitles
    if os.path.exists(srt_path):
        retries = len(ACTIVE_TOKENS)
        while retries > 0:
            try:
                # Remove old user standard caption if present
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

        if retries == 0:
            print("ALL ACTIVE TOKENS EXHAUSTED FOR CAPTIONS!")
            all_exhausted = True
            break

    # Record progress log
    with open(log_file, 'a', encoding='utf-8') as lf:
        lf.write(json.dumps({'id': vid, 'title': title, 'desc_ok': desc_ok, 'srt_ok': srt_ok, 'timestamp': time.time()}) + '\n')
    
    time.sleep(1)

print("\n" + "="*50)
print(f"RUN TERMINATED:")
print(f"  Descriptions updated: {success_desc}")
print(f"  SRTs uploaded: {success_srt}")
print(f"  All tokens exhausted: {all_exhausted}")
print("="*50)
