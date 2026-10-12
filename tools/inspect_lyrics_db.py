import sys, json

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('production/metadata/all_songs_lyrics_and_meanings.json', encoding='utf-8'))
print(f"Total songs in database: {len(data)}")

# Let's search for Thirukkural or Avaa / Kelvi / Aran
matches = []
for item in data:
    title = item.get('title', '')
    lyrics = item.get('lyrics', '')
    meaning = item.get('meaning', '')
    if any(k in title for k in ['அவா', 'கேள்வி', 'அரண்', 'தெரிந்து', 'பொறை', 'குறள்', 'இன்னா']):
        matches.append((title, item.get('youtube_id', ''), len(lyrics)))

print(f"Matching songs: {len(matches)}")
for m in matches[:25]:
    print(f"  {m[0]} | YT: {m[1]} | lyrics len: {m[2]}")
