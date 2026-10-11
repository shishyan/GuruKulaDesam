import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('production/remaining_bad_public_srts.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f'Total bad public SRTs: {len(items)}')

# Check categories and videos
for i, it in enumerate(items[:20], 1):
    vid = it.get('video_id', '')
    title = it.get('title', '')
    dur = it.get('duration', '')
    print(f"[{i:02d}] {vid} | {dur} | {title}")
