import json, sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('production/remaining_bad_public_srts.json', encoding='utf-8'))
truncated = [d for d in data if 'truncated' in d['reason']]
print(f"Total severely truncated public SRTs: {len(truncated)}")
for d in truncated:
    print(f"[{d['id']}] {d['blocks']} blocks | {d['title']}")
