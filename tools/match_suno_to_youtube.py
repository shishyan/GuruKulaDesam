import json, os, sys, re

sys.stdout.reconfigure(encoding='utf-8')
suno_songs = json.load(open('production/metadata/all_extracted_suno_urls.json', encoding='utf-8'))
catalog = json.load(open('site/assets/data/master_all_598_songs_catalog.json', encoding='utf-8'))

def clean_name(t):
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'\[.*?\]', '', t)
    t = t.split(' by ')[0]
    for w in ['Golden', 'Pop', 'Intro', '2026', 'Cover', 'Female', 'Male', 'Remix', 'Film', 'Audio', 'திருக்குறள்', 'அதிகாரம்', 'Part 1', 'Part 2']:
        t = t.replace(w, '')
    t = re.sub(r'[0-9A-Z]', '', t)
    t = re.sub(r'[-—–:!]', ' ', t)
    return ''.join(t.split())

matched = []
for s in suno_songs:
    s_raw = s['title']
    s_clean = clean_name(s_raw)
    if len(s_clean) < 3:
        continue
    best_cat = None
    for cat in catalog:
        c_title = cat.get('canonical_title', '')
        c_clean = clean_name(c_title)
        if s_clean in c_clean or c_clean in s_clean:
            best_cat = cat
            break
    if best_cat:
        matched.append({
            "suno_id": s['id'],
            "youtube_id": best_cat.get('video_id'),
            "suno_title": s['title'],
            "youtube_title": best_cat.get('canonical_title')
        })

print(f"Matched {len(matched)} / {len(suno_songs)} tracks via Tamil root normalizer!")
with open('production/metadata/suno_to_youtube_matches.json', 'w', encoding='utf-8') as f:
    json.dump(matched, f, ensure_ascii=False, indent=2)

for m in matched[:15]:
    print(f"  {m['suno_id']} -> {m['youtube_id']} | {m['suno_title'][:30]}")
