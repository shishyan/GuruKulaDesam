import sys, json, collections
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

lyrics_map = collections.defaultdict(list)
empty_lyrics = []
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        sid = s.get('id', '')
        title = s.get('title', '')
        lyr = (s.get('lyrics') or '').strip()
        first_line = lyr.split('\n')[0].strip() if lyr else ''
        if not lyr:
            empty_lyrics.append((vault, sid, title))
        else:
            lyrics_map[first_line].append((vault, sid, title))

print(f"Total songs with empty lyrics in catalog: {len(empty_lyrics)}")
print(f"Unique lyric beginnings: {len(lyrics_map)}")

sorted_clusters = sorted(lyrics_map.items(), key=lambda x: len(x[1]), reverse=True)
print("\nTop 15 largest lyric clusters:")
for line, items in sorted_clusters[:15]:
    print(f"Count: {len(items):2d} | Vaults: {set(x[0] for x in items)} | Starts: '{line[:50]}'")
