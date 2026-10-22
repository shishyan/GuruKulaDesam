import os
import json

puranas_dir = r"C:\GitHub\Gurukuladesam\data\puranas"
for f in sorted(os.listdir(puranas_dir)):
    if f.endswith('.json') and f != 'puranas_index.json':
        fp = os.path.join(puranas_dir, f)
        with open(fp, 'r', encoding='utf-8') as jf:
            d = json.load(jf)
        ch0 = d['chapters'][0]
        exp = ch0.get('exposition', '')
        # Check if verses or story
        has_verse_pattern = '..' in exp[:200] or '<br><br>' in exp[:200] or 'பாடல்' in exp[:200]
        print(f"{f:32} | Chs: {len(d['chapters']):3} | Verse-like: {has_verse_pattern} | Sample: {exp[:60].strip().encode('ascii', 'replace').decode('ascii')}")
