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

# Print only clusters with count > 2 or with different title patterns
print("\n=== HIGH COUNT CLUSTERS (Count > 2) ===")
for line, items in sorted(lyrics_map.items(), key=lambda x: len(x[1]), reverse=True):
    if len(items) > 2:
        print(f"\n--- Count: {len(items)} | Lyric starts: '{line[:60]}'")
        for vault, sid, title in items:
            print(f"   [{vault}] {sid}: {title}")
