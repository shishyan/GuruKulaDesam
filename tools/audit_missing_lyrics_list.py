import sys, json, re, collections
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

TAMIL = re.compile(r'[\u0B80-\u0BFF]')

blurb_only_videos = []
for v in vids:
    d = v['snippet'].get('description', '')
    title = v['snippet'].get('title', '')
    vid = v['id']
    if 'பாடல் வரிகள்' not in d and 'Lyrics' not in d:
        blurb_only_videos.append((vid, title, len(d)))

print(f"Total videos with only short blurb/description: {len(blurb_only_videos)}")
print("\nSample 30 videos missing lyrics on YouTube:")
for vid, t, l in blurb_only_videos[:30]:
    print(f"  [{vid}] ({l} chars): {t}")
