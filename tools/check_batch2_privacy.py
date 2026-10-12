import glob, json, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.quota_rotator import get_next_available_youtube_service

sys.stdout.reconfigure(encoding='utf-8')
yt, pid = get_next_available_youtube_service()

batch = json.load(open('production/metadata/bad_srts_matched_batch2.json', encoding='utf-8'))
video_ids = [b['video_id'] for b in batch]

res = yt.videos().list(part='status,snippet', id=','.join(video_ids)).execute()
items = res.get('items', [])
print(f"Retrieved {len(items)} items from YouTube API:")

privacy_map = {}
public_count = 0
for item in items:
    vid = item['id']
    priv = item['status']['privacyStatus']
    title = item['snippet']['title']
    privacy_map[vid] = {"status": priv, "title": title}
    if priv == 'public':
        public_count += 1
    print(f"{vid} | {priv:10s} | {title[:35]}")

print(f"\nSummary: {public_count} public out of {len(items)} queried.")

with open('production/metadata/batch2_privacy_status.json', 'w', encoding='utf-8') as f:
    json.dump(privacy_map, f, ensure_ascii=False, indent=2)
