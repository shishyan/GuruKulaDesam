import sys, json

sys.stdout.reconfigure(encoding='utf-8')
edge = json.load(open('scratch/edge_suno.json', encoding='utf-8'))
chrome = json.load(open('scratch/chrome_suno.json', encoding='utf-8'))

all_urls = edge + chrome
seen = set()
unique_songs = []
for s in all_urls:
    u = s['url'].split('?')[0]
    if '/song/' in u and u not in seen:
        seen.add(u)
        unique_songs.append((u, s.get('title', '')))

print(f"Total Unique Suno Songs found: {len(unique_songs)}")
for u, t in unique_songs[:40]:
    print(f"  {u} | {t}")
