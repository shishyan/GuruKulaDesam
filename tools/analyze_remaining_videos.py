import json
import os

with open('production/channel_sync_progress.json', 'r', encoding='utf-8') as f:
    prog = json.load(f)
with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

remaining = [v for v in videos if v['id'] not in prog]
print(f'Total remaining videos: {len(remaining)}')

has_srt_on_disk = 0
missing_srt = 0

for v in remaining:
    vid = v['id']
    srt_file = os.path.join('production', 'subtitles', f'{vid}.srt')
    if os.path.exists(srt_file):
        has_srt_on_disk += 1
    else:
        missing_srt += 1

print(f'Has .srt on disk: {has_srt_on_disk}')
print(f'Missing .srt on disk: {missing_srt}')
