import sys
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load Master Catalog
with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    master_songs = json.load(f)

print(f"Total songs in master catalog: {len(master_songs)}")

# Analyze master songs
in_discography = []
missing_from_discography = []

for s in master_songs:
    pls = s.get('playlists', [])
    if 'Discography' in pls:
        in_discography.append(s)
    else:
        missing_from_discography.append(s)

print(f"Tagged with 'Discography' in catalog: {len(in_discography)}")
print(f"NOT tagged with 'Discography' in catalog: {len(missing_from_discography)}")

missing_by_genre = {}
for s in missing_from_discography:
    g = s.get('genre', 'Unknown')
    missing_by_genre[g] = missing_by_genre.get(g, 0) + 1

print("\nMissing from Discography by Genre:")
for g, count in sorted(missing_by_genre.items(), key=lambda x: -x[1]):
    print(f"  {g}: {count} songs")

print("\nFirst 15 songs NOT in Discography:")
for s in missing_from_discography[:15]:
    vid = s.get('video_id')
    title = s.get('canonical_title', '')[:55]
    genre = s.get('genre', '')
    print(f"  [{vid}] {title} | {genre}")

# 2. Check Playlists Backup
try:
    with open('production/youtube_backup/playlists.json', encoding='utf-8') as f:
        backup = json.load(f)
    print("\n" + "="*60)
    print("BACKUP PLAYLISTS STATUS (production/youtube_backup/playlists.json):")
    for pl in backup.get('playlists', []):
        sn = pl.get('snippet', {})
        cd = pl.get('contentDetails', {})
        print(f"  {pl['id']} | {sn.get('title')} -> {cd.get('itemCount')} items")
except Exception as e:
    print("Could not read backup playlists:", e)
