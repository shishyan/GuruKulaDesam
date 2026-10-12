import sys, json, re, collections
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

TAMIL = re.compile(r'[\u0B80-\u0BFF]')

# Sample check on YouTube backup video titles
print("=== YOUTUBE BACKUP TITLES AUDIT (370 videos) ===")
yt_no_tamil = []
yt_short = []
yt_ugly = []
for v in vids:
    t = v['snippet']['title'].strip()
    vid = v['id']
    if not TAMIL.search(t):
        yt_no_tamil.append((vid, t))
    if len(t) < 10:
        yt_short.append((vid, t))
    if '|' not in t and '-' not in t and ':' not in t:
        yt_ugly.append((vid, t))

print(f"Videos with NO Tamil characters in title: {len(yt_no_tamil)}")
for vid, t in yt_no_tamil[:15]:
    print(f"   {vid}: {t}")

print(f"\nVideos with very short title (<10 chars): {len(yt_short)}")
for vid, t in yt_short[:10]:
    print(f"   {vid}: {t}")

print(f"\nVideos with unformatted/plain title (no separators): {len(yt_ugly)}")
for vid, t in yt_ugly[:15]:
    print(f"   {vid}: {t}")
