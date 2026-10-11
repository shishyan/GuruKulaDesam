import sys, os, json, time, pathlib

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_FILE = ROOT / 'data' / 'credentials' / 'token.json'
PROGRESS_FILE = ROOT / 'production' / 'delete_asr_progress.json'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(CRED_FILE))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

channel_vids = json.load(open(ROOT / 'production/youtube_backup/videos.json', encoding='utf-8'))

if PROGRESS_FILE.exists():
    try:
        progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
    except Exception:
        progress = {}
else:
    progress = {}

def save_progress():
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

deleted_count = 0
checked_count = 0
total = len(channel_vids)

print(f"Starting Clean Sweep: Deleting all auto-generated English (ASR) caption tracks across {total} videos...", flush=True)

for i, v in enumerate(channel_vids, 1):
    vid = v['id']
    title = v['snippet']['title']
    
    if progress.get(vid, {}).get('checked'):
        continue
        
    try:
        r = yt.captions().list(part='snippet', videoId=vid).execute()
        items = r.get('items', [])
        found_asr = []
        for c in items:
            snip = c.get('snippet', {})
            lang = snip.get('language')
            tk = snip.get('trackKind')
            if lang == 'en' and tk == 'asr':
                found_asr.append(c['id'])
                
        if found_asr:
            for cid in found_asr:
                yt.captions().delete(id=cid).execute()
                deleted_count += 1
                print(f"[{i}/{total}] DELETED English ASR on {vid} ({title[:35]})", flush=True)
        else:
            # No English ASR
            pass
            
        progress[vid] = {'checked': True, 'had_asr': len(found_asr) > 0, 'deleted': len(found_asr)}
        checked_count += 1
        
        if checked_count % 15 == 0:
            save_progress()
            print(f"Progress: {checked_count} videos checked, {deleted_count} English ASR tracks deleted.", flush=True)
            
    except Exception as e:
        err = str(e)
        if 'quotaExceeded' in err:
            print(f"\nQuota ceiling reached at video {i}/{total}. Halting cleanly.", flush=True)
            save_progress()
            break
        else:
            print(f"[{i}/{total}] Error on {vid}: {e}", flush=True)
            progress[vid] = {'checked': True, 'error': str(e)}

save_progress()
print(f"\nClean Sweep Complete for this pass! Total checked: {checked_count}, Total English ASR tracks deleted: {deleted_count}", flush=True)
