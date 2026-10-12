import sys, json, re, collections
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

print("=== YOUTUBE CHANNEL TITLES ANALYSIS (370 videos) ===")
# Check for common title quality criteria:
# 1. Has Tamil characters
# 2. Has English transliteration / meaning
# 3. Clean spacing (no double spaces, no leading/trailing junk)
# 4. Length fits YouTube standard (< 100 chars)

issues = []
too_long = []
double_spaces = []
no_pipe = []

for v in vids:
    vid = v['id']
    t = v['snippet']['title']
    if len(t) > 100:
        too_long.append((vid, len(t), t))
    if '  ' in t:
        double_spaces.append((vid, t))
    if '|' not in t and '—' not in t:
        no_pipe.append((vid, t))

print(f"Titles exceeding 100 chars (YouTube max is 100): {len(too_long)}")
for vid, l, t in too_long:
    print(f"   {vid} ({l} chars): {t}")

print(f"\nTitles with accidental double-spaces: {len(double_spaces)}")
for vid, t in double_spaces[:10]:
    print(f"   {vid}: {t}")

print(f"\nTitles without standard separator ('|' or '—'): {len(no_pipe)}")
for vid, t in no_pipe:
    print(f"   {vid}: {t}")

print("\nSample 25 titles across different categories on the channel:")
for v in vids[::15]:
    print(f" - {v['snippet']['title']}")
