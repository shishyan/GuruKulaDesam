import json

with open('production/youtube_published_registry.json', 'r', encoding='utf-8') as f:
    reg = json.load(f)

with open('production/autonomous_master_production_manifest.json', 'r', encoding='utf-8') as f:
    man = json.load(f)

unpub = 0
for t in man['completed_tracks']:
    tid = t.get('track_id')
    if tid not in reg:
        t['status'] = 'READY_CLEAN'
        unpub += 1
    else:
        t['status'] = 'PUBLISHED'
        t['youtube_id'] = reg[tid]['youtube_id']

with open('production/autonomous_master_production_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(man, f, indent=2, ensure_ascii=False)

print(f"Updated manifest: {unpub} tracks set to READY_CLEAN, {len(man['completed_tracks']) - unpub} kept as PUBLISHED.")
