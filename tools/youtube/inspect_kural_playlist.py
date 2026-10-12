import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('all_playlist_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

kural_items = [it for it in items if it.get('playlist_id') == 'PLW7qBZp_Q8Ro']
print(f"Total items in PLW7qBZp_Q8Ro: {len(kural_items)}")

with_adhigaram = []
without_adhigaram = []

for it in kural_items:
    t = it.get('title', '')
    vid = it.get('video_id', '')
    if re.search(r'அதிகாரம்\s+\d+\s*[-–]', t):
        with_adhigaram.append((vid, t))
    else:
        without_adhigaram.append((vid, t))

print(f"Items with canonical 'அதிகாரம் <num> - ': {len(with_adhigaram)}")
print(f"Items WITHOUT 'அதிகாரம் <num> - ': {len(without_adhigaram)}")

print("\nAll items WITHOUT 'அதிகாரம் <num> - ':")
for i, (vid, t) in enumerate(without_adhigaram):
    print(f"{i+1:3d}. [{vid}] {t}")
