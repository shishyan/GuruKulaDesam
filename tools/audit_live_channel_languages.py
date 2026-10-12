import json, sys, pathlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_FILE = ROOT / 'data' / 'credentials' / 'token.json'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(CRED_FILE))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# Fetch all upload video IDs from uploads playlist (UUPqB1A_WzpLJec6q69BOO3Q)
uploads_playlist_id = 'UUPqB1A_WzpLJec6q69BOO3Q'

video_ids = []
page_token = None

print("Fetching all uploaded video IDs via playlistItems...")
while True:
    res = yt.playlistItems().list(
        part='contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=page_token
    ).execute()
    for item in res.get('items', []):
        video_ids.append(item['contentDetails']['videoId'])
    page_token = res.get('nextPageToken')
    if not page_token:
        break

print(f"Total uploaded videos found: {len(video_ids)}")

# Batch fetch snippets in chunks of 50
live_catalog = []
for i in range(0, len(video_ids), 50):
    chunk = video_ids[i:i+50]
    res = yt.videos().list(
        part='snippet',
        id=",".join(chunk)
    ).execute()
    for item in res.get('items', []):
        snip = item['snippet']
        live_catalog.append({
            'id': item['id'],
            'title': snip.get('title'),
            'defaultLanguage': snip.get('defaultLanguage'),
            'defaultAudioLanguage': snip.get('defaultAudioLanguage'),
            'tags': snip.get('tags', [])
        })

print(f"Successfully fetched live snippets for {len(live_catalog)} videos.")

with open(ROOT / 'production' / 'live_videos_language_audit.json', 'w', encoding='utf-8') as f:
    json.dump(live_catalog, f, indent=2, ensure_ascii=False)

# Analyze language stats
dl_stats = {}
dal_stats = {}
needs_language_fix = []

for v in live_catalog:
    dl = v['defaultLanguage']
    dal = v['defaultAudioLanguage']
    dl_stats[dl] = dl_stats.get(dl, 0) + 1
    dal_stats[dal] = dal_stats.get(dal, 0) + 1
    
    if dl != 'ta' or dal != 'ta':
        needs_language_fix.append(v)

print("\n" + "=" * 60)
print("LIVE LANGUAGE AUDIT RESULTS:")
print(f"Total Videos: {len(live_catalog)}")
print(f"defaultLanguage distribution: {dl_stats}")
print(f"defaultAudioLanguage distribution: {dal_stats}")
print(f"Videos needing language fix to Tamil ('ta'): {len(needs_language_fix)}")
print("=" * 60)

if needs_language_fix:
    print("\nSample 10 videos needing language fix:")
    for v in needs_language_fix[:10]:
        print(f"  {v['id']} | dl={v['defaultLanguage']} dal={v['defaultAudioLanguage']} | {v['title'][:40]}")
