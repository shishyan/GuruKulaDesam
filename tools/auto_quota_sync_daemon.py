import sys, os, glob, json, time
from datetime import datetime, timezone, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

ACTIVE_TOKENS = sorted(glob.glob('data/credentials/tokens/*.json'))
token_idx = 0

def get_client():
    global token_idx
    for _ in range(len(ACTIVE_TOKENS)):
        t_file = ACTIVE_TOKENS[token_idx]
        try:
            creds = Credentials.from_authorized_user_file(t_file)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
            return yt, t_file
        except:
            token_idx = (token_idx + 1) % len(ACTIVE_TOKENS)
    return None, None

def rotate():
    global token_idx
    token_idx = (token_idx + 1) % len(ACTIVE_TOKENS)

def run_sync_cycle():
    with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
        meta = json.load(f)
    with open('production/next_batch_500_queue.json', 'r', encoding='utf-8') as f:
        queue = json.load(f)
        
    log_file = 'production/batch_token_sync_log.jsonl'
    done_ids = set()
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as lf:
            for l in lf:
                if l.strip():
                    try:
                        d = json.loads(l)
                        if d.get('srt_ok'):
                            done_ids.add(d['id'])
                    except:
                        pass
                        
    pending = [item for item in queue if item['id'] not in done_ids]
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pending upload targets: {len(pending)}")
    if not pending:
        print("All targets fully synchronized!")
        return True

    yt, cur_token = get_client()
    uploaded = 0
    for item in pending:
        vid = item['id']
        srt_path = f"production/subtitles/{vid}.srt"
        if not os.path.exists(srt_path):
            continue
            
        retries = len(ACTIVE_TOKENS)
        while retries > 0:
            try:
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
                print(f"  [SUCCESS] Uploaded {vid} caption: {res['id'][:20]}")
                uploaded += 1
                with open(log_file, 'a', encoding='utf-8') as lf:
                    lf.write(json.dumps({'id': vid, 'title': item['title'], 'srt_ok': True, 'timestamp': time.time()}) + '\n')
                break
            except Exception as e:
                err = str(e)
                if 'quotaExceeded' in err:
                    rotate()
                    yt, cur_token = get_client()
                    retries -= 1
                elif 'forbidden' in err.lower():
                    # skip unlisted / private copies
                    with open(log_file, 'a', encoding='utf-8') as lf:
                        lf.write(json.dumps({'id': vid, 'title': item['title'], 'srt_ok': False, 'skip_reason': 'forbidden', 'timestamp': time.time()}) + '\n')
                    break
                else:
                    break
        if retries == 0:
            print(f"Daily quota limit reached across all projects after uploading {uploaded} tracks.")
            break
        time.sleep(1)
        
    return False

if __name__ == '__main__':
    print("Auto-Resume Quota Daemon initialized.")
    run_sync_cycle()
