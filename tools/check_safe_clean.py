import json

with open('production/youtube_published_registry.json', 'r', encoding='utf-8') as f:
    reg = json.load(f)

with open('production/autonomous_master_production_manifest.json', 'r', encoding='utf-8') as f:
    man = json.load(f)

clean = [t for t in man['completed_tracks'] if t.get('clean_cinematic')]
safe = [t for t in clean if t['track_id'] not in reg]

print(f"Total clean films: {len(clean)}")
print(f"Already in registry (published): {len(clean) - len(safe)}")
print(f"Safe to publish (clean + never published): {len(safe)}")
for t in safe:
    print(f"  SAFE: {t['track_id']} | {t.get('title')}")
