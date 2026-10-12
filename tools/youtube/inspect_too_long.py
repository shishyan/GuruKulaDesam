import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('all_channel_title_updates.json', 'r', encoding='utf-8') as f:
    updates = json.load(f)

too_long = [u for u in updates if u['length'] > 95]
print(f"Total too long: {len(too_long)}")

for u in too_long:
    vid = u['video_id']
    curr = u['current_title']
    print(f"\n[{vid}] Current: '{curr}'")
