import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_lyrics_overrides.json', encoding='utf-8') as f:
    overrides = json.load(f)

works = overrides.get('_works', {})
print(f"Total defined works in overrides: {len(works)}")
for name, data in works.items():
    status = data.get('status')
    source = data.get('source', '')
    print(f"  * {name:<16} | status: {status:<18} | source: {source[:60]}")

# Check video mappings
vids = {k: v for k, v in overrides.items() if not k.startswith('_')}
print(f"\nTotal video IDs mapped to overrides: {len(vids)}")
for vid, data in vids.items():
    ref = data.get('ref')
    print(f"  [{vid}] -> ref: {ref}")
