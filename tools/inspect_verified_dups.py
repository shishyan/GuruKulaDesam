import json, sys
sys.stdout.reconfigure(encoding='utf-8')

dups = json.load(open('production/verified_exact_duplicates.json', encoding='utf-8'))
for d in dups:
    print(f"[{d['topic']} | {d['duration']}]")
    print(f"   KEEP: [{d['keep_id']}] ({d['keep_views']} views) - {d['keep_title'][:40]}")
    print(f"   REDUNDANT: [{d['redundant_id']}] ({d['redundant_views']} views) - {d['redundant_title'][:40]}")
