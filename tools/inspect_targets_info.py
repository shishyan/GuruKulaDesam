import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('production/public_videos_lyrics_srt_audit.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

vids = ['TUwlsvN7v1w', 'klSi7r6YhCU', 'PO4U3nRv6o0', '255aVCj3t0w', 'KjQZFlnCluU', 'JzGTK1V3dkM', 'HPP3IG7DWRc', 'cKyT1Cv7zEA', 'ETELjf0OTi4']
items = audit.get('all', [])
found = {item['id']: item for item in items if item.get('id') in vids}

for vid in vids:
    item = found.get(vid, {})
    print(f"{vid}: title='{item.get('title')}', duration='{item.get('duration')}', descLen={len(item.get('description',''))}")
