import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

for v in videos:
    if v['id'] in ['Yg_IgGStRvY', 'udRsA-oWxS0', 'iXHNzqOrxzw', 'qPjurMK6xpI']:
        print(f"\nID: {v['id']}")
        print(f"Title: {v['snippet']['title']}")
        print(f"Description:\n{v['snippet']['description'][:600]}")
        print("="*60)
