import json, sys, pathlib, re
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

token_path = ROOT / 'data/credentials/token_backup_guru-kula-desam.json'
creds = Credentials.from_authorized_user_file(str(token_path))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# Fetch all videos from channel live
print("Fetching all live channel videos...")
all_channel_vids = []
req = yt.search().list(part='snippet', channelId='UCPqB1A_WzpLJec6q69BOO3Q', maxResults=50, type='video')
# But search().list is costly in quota. We have videos.json and can list by ID in batches of 50.
vids = json.load(open(ROOT / 'production/youtube_backup/videos.json', encoding='utf-8'))
vid_ids = [v['id'] for v in vids]

live_vids = []
for i in range(0, len(vid_ids), 50):
    chunk = vid_ids[i:i+50]
    res = yt.videos().list(part='status,snippet,contentDetails,statistics', id=','.join(chunk)).execute()
    live_vids.extend(res.get('items', []))

print(f"Retrieved {len(live_vids)} live videos from channel.")

# Only consider public videos for duplicate deduplication
public_vids = [v for v in live_vids if v.get('status', {}).get('privacyStatus') == 'public']
print(f"Total public videos: {len(public_vids)}")

# Group by exact duration
by_duration = {}
for v in public_vids:
    dur = v['contentDetails']['duration']
    by_duration.setdefault(dur, []).append(v)

duplicates_to_privatize = []

for dur, v_list in by_duration.items():
    if len(v_list) < 2:
        continue
    
    # Within this duration bucket, find clusters of matching videos
    clusters = []
    for v in v_list:
        v_title = v['snippet']['title'].lower()
        # Clean title for comparison
        clean_title = re.sub(r'[\W_]+', ' ', v_title).strip()
        matched_cluster = None
        for c in clusters:
            lead = c[0]
            lead_title = re.sub(r'[\W_]+', ' ', lead['snippet']['title'].lower()).strip()
            # check string similarity or significant word overlap
            ratio = SequenceMatcher(None, clean_title, lead_title).ratio()
            # or check if main keywords match
            words_v = set(clean_title.split())
            words_l = set(lead_title.split())
            common = words_v.intersection(words_l)
            overlap = len(common) / max(len(words_v), len(words_l)) if words_v and words_l else 0
            
            if ratio > 0.45 or overlap > 0.35:
                # Special check: for thirukkural, chapter number must match
                m_v = re.search(r'(\d+)', clean_title)
                m_l = re.search(r'(\d+)', lead_title)
                if 'திருக்குறள்' in lead_title or 'thirukkural' in lead_title:
                    if m_v and m_l and m_v.group(1) == m_l.group(1):
                        matched_cluster = c
                        break
                else:
                    matched_cluster = c
                    break
        if matched_cluster is not None:
            matched_cluster.append(v)
        else:
            clusters.append([v])
            
    for c in clusters:
        if len(c) >= 2:
            # Sort by viewCount descending, then description length descending
            def sort_key(item):
                views = int(item.get('statistics', {}).get('viewCount', 0))
                desc_len = len(item.get('snippet', {}).get('description', ''))
                return (views, desc_len)
            c.sort(key=sort_key, reverse=True)
            
            keeper = c[0]
            redundant = c[1:]
            for r in redundant:
                duplicates_to_privatize.append({
                    'keep_id': keeper['id'],
                    'keep_title': keeper['snippet']['title'],
                    'keep_views': keeper.get('statistics', {}).get('viewCount', 0),
                    'redundant_id': r['id'],
                    'redundant_title': r['snippet']['title'],
                    'redundant_views': r.get('statistics', {}).get('viewCount', 0),
                    'duration': dur
                })

print(f"\nFound {len(duplicates_to_privatize)} redundant duplicate public videos to privatize:")
for d in duplicates_to_privatize:
    print(f"KEEP [{d['keep_id']}] ({d['keep_views']} views) : {d['keep_title'][:40]}")
    print(f"  -> PRIVATIZE [{d['redundant_id']}] ({d['redundant_views']} views) : {d['redundant_title'][:40]} (Duration: {d['duration']})")
    print()

out_file = ROOT / 'production' / 'candidates_exact_duplicates_to_privatize.json'
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(duplicates_to_privatize, f, indent=2, ensure_ascii=False)
print(f"Saved candidates to {out_file}")
