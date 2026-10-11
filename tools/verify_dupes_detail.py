import json, sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('production/exact_duplicates_to_privatize.json', encoding='utf-8'))
unique_dupes = [d for d in data if d['id'] != d['keep_id']]

full_vids = {v['id']: v for v in json.load(open('production/channel_all_videos_full_audit.json', encoding='utf-8'))}

print("=== VERIFICATION OF ALL 18 EXACT DUPLICATE PAIRS ===")
for i, d in enumerate(unique_dupes, 1):
    h = full_vids.get(d['id'])
    k = full_vids.get(d['keep_id'])
    print(f"\nPair {i:02d}:")
    print(f"   KEEP -> ID: {k['id']} | Dur: {k['duration_sec']}s | Views: {k['viewCount']} | Privacy: {k['privacyStatus']}")
    print(f"           Title: {k['title']}")
    print(f"   HIDE -> ID: {h['id']} | Dur: {h['duration_sec']}s | Views: {h['viewCount']} | Privacy: {h['privacyStatus']}")
    print(f"           Title: {h['title']}")
