import sys, json, re, collections
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

TAMIL = re.compile(r'[\u0B80-\u0BFF]')

print("=== CATALOG TITLES AUDIT (706 songs) ===")
cat_no_tamil = []
cat_short = []
cat_no_pipe = []
cat_patterns = collections.Counter()

for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        t = (s.get('title') or '').strip()
        sid = s.get('id', '')
        if not TAMIL.search(t):
            cat_no_tamil.append((vault, sid, t))
        if len(t) < 10:
            cat_short.append((vault, sid, t))
        if '|' not in t:
            cat_no_pipe.append((vault, sid, t))
        # Check formatting pattern: Work: SongName | English Translation [Format]
        if ':' in t and '|' in t:
            cat_patterns['Canonical (Work: Song | Eng [Format])'] += 1
        elif '|' in t:
            cat_patterns['Pipe only (Tamil | English)'] += 1
        else:
            cat_patterns['Other / Single string'] += 1

print(f"Total songs: {sum(len(v) for v in cat.values() if isinstance(v, list))}")
print(f"No Tamil: {len(cat_no_tamil)}")
print(f"Very short: {len(cat_short)}")
print(f"No pipe '|': {len(cat_no_pipe)}")
print("\nPatterns breakdown:")
for pat, count in cat_patterns.items():
    print(f"  {pat}: {count}")

if cat_no_pipe:
    print(f"\nSample of {len(cat_no_pipe)} titles without pipe '|':")
    for v, sid, t in cat_no_pipe[:15]:
        print(f"   [{v}] {sid}: {t}")
