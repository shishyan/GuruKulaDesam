import sys
import os
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(".")
cat = json.load(open("assets/data/catalog.json", encoding='utf-8'))
ovr = json.load(open("production/youtube_lyrics_overrides.json", encoding='utf-8'))
works = ovr.get('_works', {})
vids_file = "production/youtube_backup/videos.json"
channel_vids = json.load(open(vids_file, encoding='utf-8')) if os.path.exists(vids_file) else []
progress = json.load(open("production/channel_sync_progress.json", encoding='utf-8'))

remaining = [v for v in channel_vids if v['id'] not in progress]

cat_by_id = {}
cat_by_clean_title = {}
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        sid = s.get('id')
        if sid:
            cat_by_id[sid] = (vault, s)
        t = re.sub(r'\[.*?\]', '', s.get('title', '')).strip()
        if t:
            cat_by_clean_title[t] = (vault, s)

print(f"Total remaining: {len(remaining)}")

resolved_count = 0
unresolved = []

for v in remaining:
    vid = v['id']
    title = v['snippet']['title']
    
    lyrics = None
    meaning = None
    source = None
    
    if vid in ovr:
        ref = ovr[vid].get('ref')
        if ref and ref in works:
            lyrics = works[ref].get('lyrics')
            meaning = works[ref].get('meaning')
            source = f"OVERRIDE_WORK ({ref})"
        elif ovr[vid].get('lyrics'):
            lyrics = ovr[vid].get('lyrics')
            source = "OVERRIDE_DIRECT"

    if not lyrics and vid in cat_by_id:
        s = cat_by_id[vid][1]
        l = (s.get('lyrics') or '').strip()
        if len(l) > 15:
            lyrics = l
            meaning = s.get('meaning')
            source = f"CAT_ID ({s.get('title')[:30]})"

    if not lyrics:
        clean_t = re.sub(r'\[.*?\]', '', title).strip()
        for ct, (cvault, cs) in cat_by_clean_title.items():
            if ct in clean_t or clean_t in ct:
                l = (cs.get('lyrics') or '').strip()
                if len(l) > 15:
                    lyrics = l
                    meaning = cs.get('meaning')
                    source = f"CAT_TITLE ({ct[:30]})"
                    break

    if lyrics:
        resolved_count += 1
        lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        first_line = lines[0] if lines else ""
        print(f"OK   [{vid}] [{source[:20]}] lines:{len(lines)} | {title[:40]} -> {first_line[:40]}")
    else:
        unresolved.append((vid, title))
        print(f"FAIL [{vid}] [NO_LYRICS] | {title}")

print(f"\nSummary:")
print(f"Resolved: {resolved_count}/{len(remaining)}")
print(f"Unresolved: {len(unresolved)}")
