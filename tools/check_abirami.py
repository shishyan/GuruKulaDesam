import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

catalog = json.load(open('master_all_598_songs_catalog.json', encoding='utf-8'))
backup = json.load(open('production/youtube_backup/playlists.json', encoding='utf-8'))

amman_items = set(backup['items'].get('PLKng43jJe18o', []))
print(f"Items in backup for Amman playlist (PLKng43jJe18o): {len(amman_items)}")

abirami_songs = []
for s in catalog:
    title = s.get('canonical_title', '')
    lyrics = s.get('source', '')
    if 'அபிராமி' in title or 'abirami' in title.lower() or 'abhirami' in title.lower() or 'அபிராமி' in lyrics:
        abirami_songs.append(s)

print(f"\nTotal Abirami songs found in master catalog: {len(abirami_songs)}")
missing_from_amman = []
for s in abirami_songs:
    vid = s['video_id']
    in_amman = vid in amman_items
    if not in_amman:
        missing_from_amman.append(s)
    print(f"  [{vid}] in_amman={in_amman} | {s['canonical_title'][:65]}")

print(f"\nAbirami songs missing from Amman playlist: {len(missing_from_amman)}")
