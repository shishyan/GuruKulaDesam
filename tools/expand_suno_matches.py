import json, os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Gather all suno IDs and titles
suno_files = [f.replace('.txt', '') for f in os.listdir('production/suno_lyrics') if f.endswith('.txt')]
meta_map = {}

# Sources of titles
for mf_id in suno_files:
    mf = f'production/suno_meta/{mf_id}.json'
    if os.path.exists(mf):
        try:
            m = json.load(open(mf, encoding='utf-8'))
            meta_map[mf_id] = m.get('title', '')
        except Exception:
            pass

if os.path.exists('production/metadata/all_browser_history_suno.json'):
    for item in json.load(open('production/metadata/all_browser_history_suno.json', encoding='utf-8')):
        cid = item['url'].split('/song/')[-1].split('?')[0]
        if cid not in meta_map or not meta_map[cid]:
            meta_map[cid] = item.get('title', '')

if os.path.exists('production/metadata/all_extracted_suno_urls.json'):
    for item in json.load(open('production/metadata/all_extracted_suno_urls.json', encoding='utf-8')):
        cid = item['id']
        if cid not in meta_map or not meta_map[cid]:
            meta_map[cid] = item.get('title', '')

catalog = json.load(open('site/assets/data/master_all_598_songs_catalog.json', encoding='utf-8'))

def clean_tamil_string(t):
    if not t:
        return ""
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'\[.*?\]', '', t)
    t = t.split(' by ')[0]
    for w in ['Golden', 'Pop', 'Intro', '2026', 'Cover', 'Female', 'Male', 'Remix', 'Film', 'Audio', 
               'திருக்குறள்', 'அதிகாரம்', 'Part 1', 'Part 2', 'பகுதி 1', 'பகுதி 2', 'Cinematic', 'Song']:
        t = t.replace(w, '')
    t = re.sub(r'[0-9A-Za-z]', '', t)
    t = re.sub(r'[-—–:!|.,?]', ' ', t)
    return ''.join(t.split())

matches = []
seen_pairs = set()

for sid in suno_files:
    title = meta_map.get(sid, '')
    clean_s = clean_tamil_string(title)
    if len(clean_s) < 3:
        continue
        
    for cat in catalog:
        c_title = cat.get('canonical_title', '')
        c_clean = clean_tamil_string(c_title)
        
        # Check bidirectional substring match
        if (clean_s in c_clean or c_clean in clean_s) and len(c_clean) >= 3:
            pair = (sid, cat.get('video_id'))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                matches.append({
                    "suno_id": sid,
                    "youtube_id": cat.get('video_id'),
                    "suno_title": title,
                    "youtube_title": c_title
                })
                break

print(f"Total matched pairs: {len(matches)} out of {len(suno_files)} Suno files!")

with open('production/metadata/suno_to_youtube_matches_expanded.json', 'w', encoding='utf-8') as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)

# Update the lyrics_update_plan.json
targets = []
seen_vids = set()
for m in matches:
    vid = m['youtube_id']
    if vid not in seen_vids:
        seen_vids.add(vid)
        targets.append({
            'video_id': vid,
            'suno_id': m['suno_id'],
            'title': m.get('youtube_title', '')
        })

with open('production/lyrics_update_plan.json', 'w', encoding='utf-8') as f:
    json.dump(targets, f, ensure_ascii=False, indent=2)

print(f"Updated production/lyrics_update_plan.json with {len(targets)} unique YouTube targets!")
