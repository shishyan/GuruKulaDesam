import json
import re
import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

with open('all_playlist_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

playlists = defaultdict(list)
pl_titles = {}
for it in items:
    pid = it.get('playlist_id')
    playlists[pid].append(it)
    pl_titles[pid] = it.get('playlist_title')

for pid, it_list in playlists.items():
    print(f"\n==========================================")
    print(f"PLAYLIST: {pid} - {pl_titles[pid]} ({len(it_list)} items)")
    print(f"==========================================")
    
    # Check naming issues in this playlist
    issues = 0
    for it in it_list:
        t = it.get('title', '')
        vid = it.get('video_id', '')
        reasons = []
        if 'QC HOLD' in t or 'draft' in t.lower():
            reasons.append("Draft marker")
        if t.endswith('!') or t.endswith('.m'):
            reasons.append("Improper trailing punctuation")
        if '|' not in t:
            reasons.append("Missing '|'")
        if pid == 'PLW7qBZp_Q8Ro' and not re.search(r'அதிகாரம்\s+\d+\s*[-–]', t):
            reasons.append("Thirukkural missing 'அதிகாரம் <num> - '")
        if reasons:
            issues += 1
            if issues <= 10:
                print(f"  [{vid}] {t} -> {', '.join(reasons)}")
    if issues > 10:
        print(f"  ... and {issues - 10} more items with issues (total {issues} issues in {pl_titles[pid]})")
    elif issues == 0:
        print("  All items follow canonical formatting!")
