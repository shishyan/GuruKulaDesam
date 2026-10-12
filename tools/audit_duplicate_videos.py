import json, sys, pathlib, re

sys.stdout.reconfigure(encoding='utf-8')

def parse_duration_sec(dur_str):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', dur_str)
    if not m:
        return 0
    h, m_, s = m.groups()
    return int(h or 0) * 3600 + int(m_ or 0) * 60 + int(s or 0)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_FILE = ROOT / 'data' / 'credentials' / 'token_backup_guru-kula-desam.json'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(CRED_FILE))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# Fetch all upload video IDs
uploads_playlist_id = 'UUPqB1A_WzpLJec6q69BOO3Q'
video_ids = []
page_token = None

print("Fetching all uploaded video IDs...")
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

print(f"Total videos to fetch: {len(video_ids)}")

full_videos = []
for i in range(0, len(video_ids), 50):
    chunk = video_ids[i:i+50]
    res = yt.videos().list(
        part='snippet,contentDetails,statistics,status',
        id=",".join(chunk)
    ).execute()
    for item in res.get('items', []):
        dur_str = item['contentDetails']['duration']
        dur_sec = parse_duration_sec(dur_str)
            
        full_videos.append({
            'id': item['id'],
            'title': item['snippet']['title'],
            'publishedAt': item['snippet']['publishedAt'],
            'duration_str': dur_str,
            'duration_sec': dur_sec,
            'viewCount': int(item['statistics'].get('viewCount', 0)),
            'likeCount': int(item['statistics'].get('likeCount', 0)),
            'privacyStatus': item['status'].get('privacyStatus'),
            'tags': item['snippet'].get('tags', [])
        })

print(f"Fetched full metadata for {len(full_videos)} videos.")

with open(ROOT / 'production' / 'channel_all_videos_full_audit.json', 'w', encoding='utf-8') as f:
    json.dump(full_videos, f, indent=2, ensure_ascii=False)

# Find duplicates by normalized title and duration
# Let's inspect exact matches (same clean title + same duration)
def normalize_title(t):
    clean = re.sub(r'\[.*?\]', '', t) # remove [Film], [Audio], etc
    clean = re.sub(r'\(.*?\)', '', clean) # remove (Original), (Remix)
    clean = re.sub(r'\s+', ' ', clean).strip().lower()
    return clean

# 1. Exact duplicates: identical raw title AND exact same duration (+- 2 sec)
exact_dupes = {}
for v in full_videos:
    # Key by (title, duration_sec)
    key = (v['title'].strip().lower(), v['duration_sec'])
    exact_dupes.setdefault(key, []).append(v)

exact_duplicate_groups = {k: v for k, v in exact_dupes.items() if len(v) > 1}

# 2. Same title but different durations or tags
same_title_dupes = {}
for v in full_videos:
    key = v['title'].strip().lower()
    same_title_dupes.setdefault(key, []).append(v)

same_title_groups = {k: v for k, v in same_title_dupes.items() if len(v) > 1}

# 3. Normalized title and same duration
norm_dupes = {}
for v in full_videos:
    key = (normalize_title(v['title']), v['duration_sec'])
    norm_dupes.setdefault(key, []).append(v)

norm_groups = {k: v for k, v in norm_dupes.items() if len(v) > 1}

report = {
    'total_videos': len(full_videos),
    'exact_raw_title_and_duration_duplicates': [
        {
            'title': k[0],
            'duration_sec': k[1],
            'count': len(group),
            'videos': group
        }
        for k, group in exact_duplicate_groups.items()
    ],
    'identical_title_different_metadata': [
        {
            'title': k,
            'count': len(group),
            'videos': group
        }
        for k, group in same_title_groups.items()
        if k not in [eg[0] for eg in exact_duplicate_groups.keys()]
    ],
    'normalized_title_and_duration_matches': [
        {
            'norm_title': k[0],
            'duration_sec': k[1],
            'count': len(group),
            'videos': group
        }
        for k, group in norm_groups.items()
        if (k[0], k[1]) not in exact_duplicate_groups
    ]
}

with open(ROOT / 'production' / 'duplicates_audit_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print(f"DUPLICATE AUDIT REPORT SUMMARY:")
print(f"Total Videos Analyzed: {len(full_videos)}")
print(f"Exact Duplicate Groups (Same Title & Same Duration): {len(exact_duplicate_groups)}")
total_exact_vids = sum(len(g) for g in exact_duplicate_groups.values())
print(f"  Total videos in Exact Duplicate Groups: {total_exact_vids}")
print(f"Same Raw Title Groups (Different Duration): {len(report['identical_title_different_metadata'])}")
print(f"Normalized Title + Same Duration (e.g. Film vs Audio): {len(report['normalized_title_and_duration_matches'])}")
print("=" * 60)

print("\n--- SAMPLE EXACT DUPLICATE GROUPS ---")
for eg in report['exact_raw_title_and_duration_duplicates'][:5]:
    print(f"\nTitle: '{eg['title']}' | Duration: {eg['duration_sec']}s | Count: {eg['count']}")
    for v in eg['videos']:
        print(f"  {v['id']} | Published: {v['publishedAt']} | Views: {v['viewCount']} | Privacy: {v['privacyStatus']}")
