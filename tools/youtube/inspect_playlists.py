import json
import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

with open('all_playlist_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total playlist item rows: {len(items)}")

playlists = defaultdict(list)
pl_titles = {}
for it in items:
    pid = it.get('playlist_id')
    playlists[pid].append(it)
    pl_titles[pid] = it.get('playlist_title')

print(f"Unique playlists: {len(playlists)}\n")
for pid, it_list in sorted(playlists.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"Playlist [{pid}]: {pl_titles[pid]} ({len(it_list)} items)")

