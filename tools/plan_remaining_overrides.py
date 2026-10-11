import sys
import os
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(".")
ovr = json.load(open("production/youtube_lyrics_overrides.json", encoding='utf-8'))
works = ovr.get('_works', {})
channel_vids = json.load(open("production/youtube_backup/videos.json", encoding='utf-8'))
progress = json.load(open("production/channel_sync_progress.json", encoding='utf-8'))
remaining = [v for v in channel_vids if v['id'] not in progress]

print(f"Total remaining videos: {len(remaining)}")

# Mapping rules based on video title analysis
# Let's see what each video title contains
for i, v in enumerate(remaining):
    vid = v['id']
    title = v['snippet']['title']
    existing_ref = ovr.get(vid, {}).get('ref')
    print(f"{i+1:2d}. [{vid}] ref:{str(existing_ref):<15} | {title}")
