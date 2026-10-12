import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

catalog = json.load(open('master_all_598_songs_catalog.json', encoding='utf-8'))
backup = json.load(open('production/youtube_backup/playlists.json', encoding='utf-8'))

amman_items = set(backup['items'].get('PLKng43jJe18o', []))

all_amman_candidates = []
for s in catalog:
    title = s.get('canonical_title', '').lower()
    genre = s.get('genre', '')
    if 'அம்மன்' in genre or 'amman' in title or 'அபிராமி' in title or 'சரஸ்வதி' in title or 'துர்க்கை' in title or 'காளி' in title or 'மாரியம்மன்' in title:
        all_amman_candidates.append(s)

print(f"Total Amman candidates in catalog: {len(all_amman_candidates)}")
missing_amman = [s for s in all_amman_candidates if s['video_id'] not in amman_items]
print(f"Missing from Amman playlist (PLKng43jJe18o): {len(missing_amman)}")
for s in missing_amman:
    print(f"  [{s['video_id']}] {s['canonical_title'][:65]} | {s['genre']}")
