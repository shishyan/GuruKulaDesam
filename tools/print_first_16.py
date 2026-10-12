import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    all_vids = json.load(f)

with open('production/channel_sync_progress.json', 'r', encoding='utf-8') as f:
    synced = json.load(f)

remaining = [v for v in all_vids if v['id'] not in synced]

print(f"Total remaining: {len(remaining)}")
for i, v in enumerate(remaining[:16]):
    vid = v['id']
    title = v['snippet']['title']
    print(f"{i+1:2d}. [{vid}] {title}")
