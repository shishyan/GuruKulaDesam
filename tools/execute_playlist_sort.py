import sys, os, json, time, pathlib

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_FILE = ROOT / 'data' / 'credentials' / 'token.json'
PROGRESS_FILE = ROOT / 'production' / 'playlist_sort_progress.json'
PLAN_FILE = ROOT / 'production' / 'thirukkural_sort_plan.json'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(CRED_FILE))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

plan = json.load(open(PLAN_FILE, encoding='utf-8'))

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

print(f"Starting Thirukkural Playlist Sorting (Total planned items: {len(plan)})...", flush=True)

# Delete the 2 deleted videos first if not deleted
deleted_ids = ['lN3vV3ThZsY', '53AcrjC3imY']

updated_count = 0
skipped_count = 0

for item in plan:
    target_pos = item['target_position']
    item_id = item['itemId']
    vid = item['videoId']
    title = item['title']
    chap = item['chapter']
    
    if progress.get(item_id, {}).get('sorted'):
        continue
        
    body = {
        'id': item_id,
        'snippet': {
            'playlistId': 'PLW7qBZp_Q8Ro',
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': vid
            },
            'position': target_pos
        }
    }
    
    try:
        res = yt.playlistItems().update(part='snippet', body=body).execute()
        new_pos = res['snippet']['position']
        print(f"[{target_pos:03d}/{len(plan)}] Moved Chap {chap:03d} to Pos {new_pos:03d} -> {title[:40]}", flush=True)
        progress[item_id] = {'sorted': True, 'position': new_pos, 'chapter': chap}
        updated_count += 1
        
        if updated_count % 10 == 0:
            save_progress()
            
        time.sleep(0.3)
        
    except Exception as e:
        err = str(e)
        if 'quotaExceeded' in err:
            print(f"\nQuota ceiling reached at target pos {target_pos}. Progress saved cleanly.", flush=True)
            save_progress()
            break
        else:
            print(f"Error on item {item_id} ({title[:30]}): {e}", flush=True)
            progress[item_id] = {'sorted': False, 'error': str(e)}

save_progress()
print(f"\nSorting pass complete! Total updated: {updated_count}", flush=True)
