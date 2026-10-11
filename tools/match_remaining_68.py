import sys
import os
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    all_vids = json.load(f)

with open('production/channel_sync_progress.json', 'r', encoding='utf-8') as f:
    synced = json.load(f)

synced_ids = set(synced.keys())
remaining = [v for v in all_vids if v['id'] not in synced_ids]

# Load master catalogs
master_cat = []
if os.path.exists('master_all_598_songs_catalog.json'):
    with open('master_all_598_songs_catalog.json', 'r', encoding='utf-8') as f:
        master_cat = json.load(f)

assets_cat = []
if os.path.exists('assets/data/catalog.json'):
    with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            assets_cat = data
        elif isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, list):
                    assets_cat.extend(v)

overrides = {}
if os.path.exists('production/youtube_lyrics_overrides.json'):
    with open('production/youtube_lyrics_overrides.json', 'r', encoding='utf-8') as f:
        overrides = json.load(f)

print(f"Total remaining: {len(remaining)}")
print(f"Master catalog items: {len(master_cat)}")
print(f"Assets catalog items: {len(assets_cat)}")
print(f"Overrides: {len(overrides)}")

results = []
for i, v in enumerate(remaining):
    vid = v['id']
    title = v['snippet']['title']
    duration_str = v.get('contentDetails', {}).get('duration', '')
    
    # check overrides
    match_source = None
    lyrics_text = None
    
    if vid in overrides:
        match_source = "OVERRIDE"
        lyrics_text = overrides[vid].get('lyrics', '')
    
    # check srt existing text
    srt_path = f"production/subtitles/{vid}.srt"
    srt_content = ""
    if os.path.exists(srt_path):
        with open(srt_path, 'r', encoding='utf-8', errors='ignore') as f:
            srt_content = f.read()

    results.append({
        'index': i+1,
        'id': vid,
        'title': title,
        'duration': duration_str,
        'has_srt': bool(srt_content),
        'srt_length': len(srt_content),
        'has_override': vid in overrides
    })

print(f"\nListing remaining videos:")
for r in results:
    ov = "YES" if r['has_override'] else "NO"
    print(f"{r['index']:2d}. [{r['id']}] (ov:{ov}, srt_len:{r['srt_length']}) {r['title'][:55]}")
