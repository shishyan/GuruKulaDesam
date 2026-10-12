import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

targets = ["jZFTlpJwn6A", "FGeahfpAbiw", "mPypwIgdo-E", "g42Pg2sg_gg", "rRoJfeRQiaM", "_eG3rWRIvJo", "udRsA-oWxS0", "iXHNzqOrxzw", "qPjurMK6xpI", "nGBmGzsD-kM"]

for t in targets:
    item = next((v for v in vids if v.get('id') == t), None)
    if item:
        print(f"\n=== {t} : {item.get('title')} ===")
        print(item.get('description', '')[:300])
        print("...")
