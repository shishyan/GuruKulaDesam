import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

for v in vids:
    t = v['snippet']['title']
    if 'பிரார்த்தனை' in t:
        print(f"ID: {v['id']}")
        print(f"TITLE: {t}")
        print("DESCRIPTION:")
        print(v['snippet'].get('description'))
        print("="*60)
