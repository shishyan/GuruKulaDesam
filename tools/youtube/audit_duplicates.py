import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('channel_all_uploads.json', 'r', encoding='utf-8') as f:
    channel = json.load(f)

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

audio_ids = ['h2q-ADrbBc4', 'IEk-wwY3rC8', '5uRYFxhT32k', 'O0hASl4BS2c', 'hjcH8zbEleE', 'GfGlO3RQuik']
chapters = [26, 27, 52, 54, 57, 61]
keywords = [
    (26, ['புலால்', 'உண்ணாமை', 'pulaal', 'unnaamai']),
    (27, ['தவம்', 'thavam']),
    (52, ['தெரிந்து வினையாடல்', 'vinaiyaadal']),
    (54, ['பொச்சாவாமை', 'pochchaavaamai']),
    (57, ['வெருவந்த', 'செய்யாமை', 'veruvantha']),
    (61, ['மடியின்மை', 'madiyinmai'])
]

print('=== 1. AUDIT CHANNEL UPLOADS (294 videos) FOR AUDIO IDs ===')
found_aids = 0
for v in channel:
    vid = v['id']
    if vid in audio_ids:
        print(f'Match found in channel uploads! {vid}: {v["title"]}')
        found_aids += 1
if found_aids == 0:
    print('PASS: Zero audio IDs exist as channel uploads.')

print('\n=== 2. AUDIT CHANNEL UPLOADS FOR CHAPTER NUMBERS AND KEYWORDS ===')
matches = []
for v in channel:
    t = v.get('title', '')
    tl = t.lower()
    for chap, kws in keywords:
        for kw in kws:
            if kw.lower() in tl:
                matches.append((chap, kw, v['id'], t))
        for p in [f'அதிகாரம் {chap}', f'அதிகாரம்: {chap}', f'adhikaram {chap}', f'chapter {chap}', f'ch {chap}', f'ch.{chap}']:
            if p in tl:
                print(f'CRITICAL: Channel upload mentions chapter {chap}! ID={v["id"]} Title={t}')

if matches:
    print(f'Keyword occurrences in titles ({len(matches)} total):')
    for chap, kw, vid, t in matches:
        print(f'  Ch {chap} (keyword "{kw}"): [{vid}] {t}')
else:
    print('PASS: No chapter keywords found in channel uploads.')

print('\n=== 3. AUDIT CATALOG FILMS FOR REFERENCES TO AUDIO IDs OR CHAPTERS ===')
film_matches = 0
for c, items in cat.items():
    for item in items:
        if item.get('type') == 'film':
            desc = item.get('description', '')
            t = item.get('title', '')
            tl = t.lower()
            for aid in audio_ids:
                if aid in desc or aid in t:
                    print(f'CRITICAL: Catalog film references audio {aid}! ID={item["id"]} Title={t}')
                    film_matches += 1
            for chap in chapters:
                for p in [f'அதிகாரம் {chap}', f'adhikaram {chap}', f'chapter {chap}']:
                    if p in tl:
                        print(f'CRITICAL: Catalog film mentions chapter {chap}! ID={item["id"]} Title={t}')
                        film_matches += 1
if film_matches == 0:
    print('PASS: Zero catalog films reference these 6 chapters or audio IDs.')
