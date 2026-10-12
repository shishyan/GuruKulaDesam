import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

dots_vids = []
for vid, data in live_meta.items():
    t = data.get('title', '')
    if '...' in t or '…' in t:
        dots_vids.append((vid, t))

print(f"Videos with dots in title: {len(dots_vids)}")
for vid, t in dots_vids:
    print(f"  [{vid}] {t}")
