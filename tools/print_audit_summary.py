import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/all_flawed_descriptions_audit.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

for cat, items in audit.items():
    print(f"\n=================== {cat.upper()} ({len(items)} items) ===================")
    for x in items:
        if isinstance(x, dict):
            print(f"- {x.get('id')}: {x.get('title')}")
            if 'reason' in x: print(f"  Reason: {x['reason']}")
            if 'issue' in x: print(f"  Issue: {x['issue']}")
        else:
            print(f"- {x}")
