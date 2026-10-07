import json
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Load updates mapping
with open('all_channel_title_updates.json', 'r', encoding='utf-8') as f:
    updates = json.load(f)

title_map = {u['video_id']: u['new_title'] for u in updates}
print(f"Loaded {len(title_map)} title updates.")

# 2. Update live_youtube_metadata.json
with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

live_updated = 0
for vid, new_title in title_map.items():
    if vid in live_meta:
        if live_meta[vid].get('title') != new_title:
            live_meta[vid]['title'] = new_title
            live_updated += 1

with open('live_youtube_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(live_meta, f, ensure_ascii=False, indent=2)

print(f"Updated {live_updated} titles in live_youtube_metadata.json (Total records: {len(live_meta)}).")

# 3. Update assets/data/catalog.json
with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

cat_updated = 0
for cat_name, items in catalog.items():
    for item in items:
        vid = item.get('id')
        if vid in title_map:
            if item.get('title') != title_map[vid]:
                item['title'] = title_map[vid]
                cat_updated += 1

with open('assets/data/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=4)

print(f"Updated {cat_updated} titles across categories in assets/data/catalog.json.")

# 4. Generate assets/data/catalog.js
js_content = f"""/**
 * Guru Kula Desam - Complete Devotional & Scripture Catalog
 * 580 video & audio items enriched with Tamil lyrics, spiritual meanings, authors, and sources.
 */
window.GURUKULA_CATALOG = {json.dumps(catalog, ensure_ascii=False)};
"""

with open('assets/data/catalog.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Generated assets/data/catalog.js successfully.")

# 5. Mirror to site/ and docs/
for target_dir in ['site/assets/data', 'docs/assets/data']:
    shutil.copy2('assets/data/catalog.json', f'{target_dir}/catalog.json')
    shutil.copy2('assets/data/catalog.js', f'{target_dir}/catalog.js')
    print(f"Mirrored catalog.json and catalog.js to {target_dir}/")

print("\n--- Verification: checking mirror file hashes / contents ---")
import hashlib

def get_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

files = ['catalog.json', 'catalog.js']
dirs = ['assets/data', 'site/assets/data', 'docs/assets/data']

for f in files:
    hashes = [get_hash(f"{d}/{f}") for d in dirs]
    match = all(h == hashes[0] for h in hashes)
    print(f"{f}: {'100% PARITY' if match else 'MISMATCH'} (Hash: {hashes[0][:10]}...)")

