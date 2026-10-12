import sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds_file = pathlib.Path('data/credentials/token_alt.json')
creds = Credentials.from_authorized_user_file(str(creds_file))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

plan = json.load(open('production/thirukkural_sort_plan.json', encoding='utf-8'))
progress = json.load(open('production/playlist_sort_progress.json', encoding='utf-8'))

for item in plan:
    if not progress.get(item['itemId'], {}).get('sorted'):
        target_pos = item['target_position']
        body = {
            'id': item['itemId'],
            'snippet': {
                'playlistId': 'PLW7qBZp_Q8Ro',
                'resourceId': {'kind': 'youtube#video', 'videoId': item['videoId']},
                'position': target_pos
            }
        }
        print(f"Attempting update on item {item['itemId']} to pos {target_pos} ({item['title'][:30]})...")
        try:
            res = yt.playlistItems().update(part='snippet', body=body).execute()
            print('SUCCESS on token.json! Updated pos:', res['snippet']['position'])
            progress[item['itemId']] = {'sorted': True, 'position': target_pos, 'chapter': item['chapter']}
            json.dump(progress, open('production/playlist_sort_progress.json', 'w', encoding='utf-8'), indent=2)
        except Exception as e:
            print('FAILED on token.json:', e)
        break
