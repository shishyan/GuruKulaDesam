import json, sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('production/srt_timing_issues_report.json', encoding='utf-8'))
thiru = [p for p in d['problems'] if p['is_thirukkural']]
print(f"Total Thirukkural issues: {len(thiru)}")
for p in thiru:
    print(f"[{p['vid']}] blocks={p['blocks']} max_dur={p['max_block_dur']}s | {p['title']}")
    for iss in p['issues']:
        print(f"   - {iss}")
