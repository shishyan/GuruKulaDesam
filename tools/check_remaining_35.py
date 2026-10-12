import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

catalog = json.load(open('master_all_598_songs_catalog.json', encoding='utf-8'))
missing = [s for s in catalog if 'Discography' not in s.get('playlists', [])]

print(f"Total remaining missing from Discography in catalog: {len(missing)}")
for idx, s in enumerate(missing, 1):
    vid = s['video_id']
    title = s.get('canonical_title', '')[:55]
    genre = s.get('genre', '')
    tt = s.get('track_type', '')
    print(f"{idx:2d}. [{vid}] {title} | {genre} | {tt}")
