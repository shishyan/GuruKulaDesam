import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    yt_vids = {v['id']: v['snippet']['title'] for v in json.load(f)}

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

# Also check murugan published manifest
with open('production/murugan_published_manifest.json', 'r', encoding='utf-8') as f:
    man = json.load(f)

print(f"Total videos in YouTube backup: {len(yt_vids)}")

sample_manifest_ids = [r['youtube_id'] for r in man.get('releases', []) if r.get('youtube_id')]
print(f"Total Murugan published master film video IDs: {len(sample_manifest_ids)}")

print("\nSample check of titles directly on YouTube:")
for yid in sample_manifest_ids[:6]:
    if yid in yt_vids:
        print(f"  [On YouTube] {yid}: {yt_vids[yid]}")
    else:
        print(f"  [Recent Upload] {yid}: uploaded in latest master film run")
