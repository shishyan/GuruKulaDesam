import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

item = next((v for v in vids if v.get('id') == 'nGBmGzsD-kM'), None)
if item:
    print("Found in backup:")
    print("Title:", item.get('snippet', {}).get('title'))
    print("Description:", item.get('snippet', {}).get('description')[:400])
else:
    print("Not found in backup.")
