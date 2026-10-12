import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('production/metadata/thirukkural_releases_metadata.json', 'r', encoding='utf-8') as f:
    rels = json.load(f)

print(f"Chapters in releases metadata: {len(rels)}")
for r in rels:
    print(f"Chapter {r.get('chapter_number')}: {r.get('tamil_title')} -> track_id: {r.get('track_id')}")

