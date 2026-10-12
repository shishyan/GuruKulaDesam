import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

for v in videos:
    if v['id'] == 'udRsA-oWxS0':
        print(v['snippet']['description'])
