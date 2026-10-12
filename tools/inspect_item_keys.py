import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('master_all_598_songs_catalog.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

for item in master:
    if "jZFTlpJwn6A" in str(item):
        print("Item with jZFTlpJwn6A:", json.dumps(item, indent=2, ensure_ascii=False))
        break
