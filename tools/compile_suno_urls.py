import sys, json

sys.stdout.reconfigure(encoding='utf-8')
edge = json.load(open('scratch/edge_suno.json', encoding='utf-8'))
chrome = json.load(open('scratch/chrome_suno.json', encoding='utf-8'))
all_urls = edge + chrome

seen = set()
suno_songs = []
for item in all_urls:
    t = item.get('title', '')
    u = item.get('url', '').split('?')[0]
    if '/song/' in u and u not in seen:
        seen.add(u)
        song_id = u.split('/song/')[-1]
        suno_songs.append({"id": song_id, "title": t, "url": u})

print(f"Total Unique Suno Songs in browser histories: {len(suno_songs)}")
with open('production/metadata/all_extracted_suno_urls.json', 'w', encoding='utf-8') as f:
    json.dump(suno_songs, f, ensure_ascii=False, indent=2)

print("Saved production/metadata/all_extracted_suno_urls.json!")
