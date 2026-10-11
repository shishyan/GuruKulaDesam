import sys
import json
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/all_flawed_descriptions_audit.json', encoding='utf-8') as f:
    audit = json.load(f)

no_lyrics = audit['no_lyrics_at_all']
mismatched = audit['mismatched_wrong_lyrics']
truncated = audit['truncated_incomplete_lyrics']

print(f"Total videos with NO lyrics at all: {len(no_lyrics)}")

# Categorize by title pattern
categories = []
for item in no_lyrics:
    t = item['title'].lower()
    if 'திருக்குறள்' in t or 'thirukkural' in t or 'அதிகாரம்' in t:
        categories.append('Thirukkural')
    elif 'திருவருட்பா' in t or 'thiruvarutpa' in t or 'வள்ளலார்' in t:
        categories.append('Vallalar / Thiruvarutpa')
    elif 'சிவ' in t or 'shiva' in t or 'தேவாரம்' in t or 'திருவாசகம்' in t or 'நடராஜர்' in t:
        categories.append('Shiva / Thevaram / Thiruvasagam')
    elif 'முருக' in t or 'muruga' in t or 'கந்த' in t or 'திருப்புகழ்' in t:
        categories.append('Murugan / Thiruppugazh')
    elif 'விநாயக' in t or 'vinayagar' in t or 'கணேச' in t or 'பிள்ளையார்' in t:
        categories.append('Vinayagar')
    elif 'அம்மன்' in t or 'மாரியம்மன்' in t or 'துர்க்கை' in t or 'அபிராமி' in t:
        categories.append('Amman / Devi')
    elif 'விஷ்ணு' in t or 'பெருமாள்' in t or 'ராமர்' in t or 'கிருஷ்ண' in t or 'நாராயண' in t:
        categories.append('Vishnu / Rama / Krishna')
    else:
        categories.append('Other / General Devotional')

counts = Counter(categories)
print("\n--- Breakdown of Videos with NO Lyrics ---")
for cat, count in counts.most_common():
    print(f"  {cat}: {count} videos")

print("\n--- Sample of Non-Thirukkural videos with NO Lyrics ---")
non_tk = [item for item in no_lyrics if not any(x in item['title'].lower() for x in ['திருக்குறள்', 'thirukkural', 'அதிகாரம்'])]
print(f"Total Non-Thirukkural videos with NO Lyrics: {len(non_tk)}")
for item in non_tk[:25]:
    print(f"  [{item['id']}] {item['title']} (Desc len: {item['desc_len']})")

print("\n--- Mismatched / Wrong Lyrics Videos ---")
for item in mismatched:
    print(f"  [{item['id']}] {item['title']}")
    print(f"      Work: {item['work']} | Issue: {item['issue']}")
    if item.get('found_sample'):
        print(f"      Found text: {item['found_sample']}")

print("\n--- Truncated / Incomplete Lyrics Videos ---")
for item in truncated:
    print(f"  [{item['id']}] {item['title']}")
    print(f"      Work: {item['work']} | Issue: {item['issue']}")
