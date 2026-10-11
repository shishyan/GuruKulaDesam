import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    yt_vids = {v['id']: v for v in json.load(f)}

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

# Analyze catalog vs YouTube
cat_ids = set()
for vault, songs in cat.items():
    if isinstance(songs, list):
        for s in songs:
            cat_ids.add(s.get('id'))

meta_ids = set(meta.keys())
yt_ids = set(yt_vids.keys())

print(f"Total Unique Song IDs in Catalog (Local Master): {len(cat_ids)}")
print(f"Total Unique Song IDs in Live Metadata DB: {len(meta_ids)}")
print(f"Total Videos Uploaded to YouTube Channel: {len(yt_ids)}")

print(f"\n1. Catalog songs NOT on YouTube channel yet: {len(cat_ids - yt_ids)}")
print(f"2. Catalog songs that ARE on YouTube channel: {len(cat_ids & yt_ids)}")
print(f"3. YouTube channel videos NOT in Catalog: {len(yt_ids - cat_ids)}")

# Breakdown of catalog songs not yet uploaded to YouTube
missing_by_vault = {}
for vault, songs in cat.items():
    if isinstance(songs, list):
        not_on_yt = sum(1 for s in songs if s.get('id') not in yt_ids)
        missing_by_vault[vault] = (not_on_yt, len(songs))

print("\nBreakdown of Catalog tracks uploaded vs pending by vault:")
for vault, (pending, total) in missing_by_vault.items():
    uploaded = total - pending
    print(f"  - {vault:18}: {uploaded:3d} uploaded | {pending:3d} pending upload (Total in vault: {total})")
