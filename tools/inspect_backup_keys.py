import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

for v in vids:
    if "jZFTlpJwn6A" in str(v):
        print(json.dumps(v, indent=2, ensure_ascii=False))
        break
