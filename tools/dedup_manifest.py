import json

with open('production/autonomous_master_production_manifest.json', 'r', encoding='utf-8') as f:
    man = json.load(f)

seen_tids = set()
deduped_tracks = []
for t in man.get('completed_tracks', []):
    tid = t.get('track_id')
    if tid not in seen_tids:
        seen_tids.add(tid)
        deduped_tracks.append(t)

print(f"Before dedup: {len(man['completed_tracks'])} tracks")
print(f"After dedup: {len(deduped_tracks)} unique tracks")

man['completed_tracks'] = deduped_tracks
with open('production/autonomous_master_production_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(man, f, indent=2, ensure_ascii=False)
