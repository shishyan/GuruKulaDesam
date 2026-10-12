import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('master_all_598_songs_catalog.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

vids = ["_eG3rWRIvJo", "udRsA-oWxS0", "iXHNzqOrxzw", "qPjurMK6xpI", "mPypwIgdo-E", "g42Pg2sg_gg", "rRoJfeRQiaM", "jZFTlpJwn6A", "FGeahfpAbiw", "nGBmGzsD-kM"]

print("Searching master catalog for defective videos:")
for item in master:
    yurl = item.get('youtube_url', '') or item.get('youtube_id', '')
    for v in vids:
        if v in str(yurl):
            print(f"\nFound {v}:")
            print(f"  Title: {item.get('title')}")
            print(f"  Deity: {item.get('deity')}")
            print(f"  Category: {item.get('category')}")
            print(f"  Lyrics: {repr(item.get('lyrics', '')[:120])}")
            print(f"  Meaning: {repr(item.get('meaning', '')[:100])}")
