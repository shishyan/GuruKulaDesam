import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    all_vids = json.load(f)

with open('production/channel_sync_progress.json', 'r', encoding='utf-8') as f:
    synced = json.load(f)

remaining = [v for v in all_vids if v['id'] not in synced]

thirukkural_vids = []
devotional_vids = []
instrumental_vids = []

for v in remaining:
    vid = v['id']
    title = v['snippet']['title']
    if 'அதிகாரம்' in title or 'Thirukkural' in title or 'குறள்' in title:
        thirukkural_vids.append((vid, title))
    elif 'ஆலய நாதம்' in title or 'Harmonica' in title or 'Meditation' in title:
        instrumental_vids.append((vid, title))
    else:
        devotional_vids.append((vid, title))

print(f"Total remaining: {len(remaining)}")
print(f"Thirukkural videos ({len(thirukkural_vids)}):")
for vid, t in thirukkural_vids:
    print(f"  [{vid}] {t}")

print(f"\nInstrumental/Meditation videos ({len(instrumental_vids)}):")
for vid, t in instrumental_vids:
    print(f"  [{vid}] {t}")

print(f"\nDevotional songs ({len(devotional_vids)}):")
for vid, t in devotional_vids:
    print(f"  [{vid}] {t}")
