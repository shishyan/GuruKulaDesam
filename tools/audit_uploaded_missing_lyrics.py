import sys, json, re, collections
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = {v['id']: v for v in json.load(f)}

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

# Find all videos uploaded to YouTube that lack lyrics
pending_on_yt = []
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        sid = s.get('id')
        if sid in vids:
            desc = vids[sid]['snippet'].get('description', '')
            if 'பாடல் வரிகள்' not in desc and 'Lyrics' not in desc:
                pending_on_yt.append((vault, sid, s.get('title', '')))

print(f"Total uploaded videos currently missing lyrics on YouTube: {len(pending_on_yt)}")
by_vault = collections.Counter(x[0] for x in pending_on_yt)
for v, count in by_vault.items():
    print(f"  - {v:18}: {count} videos")

print("\n--- Shiva Videos on YouTube Missing Lyrics ---")
for v, sid, t in pending_on_yt:
    if v == 'shiva':
        print(f"  {sid}: {t}")
