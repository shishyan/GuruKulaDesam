import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

with open('production/channel_all_videos_full_audit.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

meta_ids = set(meta.keys())
audit_ids = set(item['id'] for item in audit)

print(f"Meta IDs: {len(meta_ids)}")
print(f"Audit IDs: {len(audit_ids)}")
print(f"In Meta but not in Audit: {len(meta_ids - audit_ids)}")
print(f"In Audit but not in Meta: {len(audit_ids - meta_ids)}")

diff = list(meta_ids - audit_ids)
print("\nSample IDs in Meta but not in Audit:")
for vid in diff[:10]:
    item = meta[vid]
    print(f" - {vid}: {item.get('title')[:60]} (dur: {item.get('duration')})")
