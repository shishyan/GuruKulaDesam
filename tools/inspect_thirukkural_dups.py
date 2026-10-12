import json, sys
sys.stdout.reconfigure(encoding='utf-8')

dups = json.load(open('production/verified_exact_duplicates.json', encoding='utf-8'))
thiru_dups = [d for d in dups if 'thirukkural' in d['topic']]

print(f"Total Thirukkural duplicate pairs: {len(thiru_dups)}")
for d in thiru_dups:
    print(f"[{d['topic']} | {d['duration']}]")
    print(f"   KEEP: [{d['keep_id']}] ({d['keep_views']} views) - {d['keep_title']}")
    print(f"   REDUNDANT: [{d['redundant_id']}] ({d['redundant_views']} views) - {d['redundant_title']}")
    print()
