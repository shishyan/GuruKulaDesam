import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('all_uploads.json', 'r', encoding='utf-8') as f:
    uploads = json.load(f)

print(f'Total uploads: {len(uploads)}')

kural_count = 0
non_kural_count = 0

for i, v in enumerate(uploads):
    vid = v['video_id']
    t = v['title']
    print(f'{i+1:3d}. [{vid}] {t}')
