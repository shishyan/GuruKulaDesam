import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
cat = json.load(open('assets/data/catalog.json', encoding='utf-8'))
ovr = json.load(open('production/youtube_lyrics_overrides.json', encoding='utf-8'))
works = ovr.get('_works', {})
channel_vids = json.load(open('production/youtube_backup/videos.json', encoding='utf-8'))
progress = json.load(open('production/channel_sync_progress.json', encoding='utf-8'))
remaining = [v for v in channel_vids if v['id'] not in progress]

cat_by_id = {}
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        if s.get('id'): cat_by_id[s['id']] = s

print(f"Total remaining: {len(remaining)}")

for i, v in enumerate(remaining):
    vid = v['id']
    title = v['snippet']['title']
    target = '?'
    first_line = ''
    if vid in ovr and ovr[vid].get('ref'):
        ref = ovr[vid]['ref']
        target = f"OVR_WORK: {ref}"
        if ref in works:
            lyr = works[ref].get('lyrics', '')
            first_line = lyr.split('\n')[0] if lyr else ''
    elif vid in cat_by_id:
        c_title = cat_by_id[vid].get('title', '')
        target = f"CAT_ID: {c_title[:30]}"
        lyr = cat_by_id[vid].get('lyrics', '')
        first_line = lyr.split('\n')[0] if lyr else ''
    print(f"{i+1:2d}. [{vid}] {title[:40]:<40} ===> {target:<30} | {first_line[:40]}")
