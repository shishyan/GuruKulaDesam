import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

cat = json.load(open("assets/data/catalog.json", encoding='utf-8'))
tk = cat.get('thirukkural', [])

chapters_needed = [2, 8, 16, 32, 40, 125]

found_tk = {}
for item in tk:
    t = item.get('title', '')
    for ch in chapters_needed:
        if f"அதிகாரம் {ch} " in t or f"அதிகாரம் {ch}-" in t or f"அதிகாரம் {ch}:" in t:
            found_tk[ch] = item
            break

print(f"Found {len(found_tk)} chapters:")
for ch, item in sorted(found_tk.items()):
    print(f"\n--- Chapter {ch}: {item.get('title')} ---")
    print(f"ID: {item.get('id')}")
    lyr = item.get('lyrics', '')
    lines = lyr.split('\n')
    print(f"Lines count: {len(lines)}")
    print("First 6 lines:")
    for l in lines[:6]:
        print("  ", l)
