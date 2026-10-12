import json
import re
import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

with open('all_playlist_items.json', 'r', encoding='utf-8') as f:
    pl_items = json.load(f)

# Group playlists per video
vid_to_pls = defaultdict(list)
for it in pl_items:
    vid = it.get('video_id')
    pname = it.get('playlist_title')
    if pname not in vid_to_pls[vid]:
        vid_to_pls[vid].append(pname)

print(f"Total videos in live_youtube_metadata: {len(live_meta)}")

# Let's inspect non-Thirukkural tracks
non_kural_vids = []
for vid, data in live_meta.items():
    t = data.get('title', '')
    pls = vid_to_pls[vid]
    is_kural = any('Thirukkural' in p or 'திருக்குறள்' in p for p in pls) or 'அதிகாரம்' in t or 'Thirukkural' in t
    if not is_kural:
        non_kural_vids.append((vid, t, pls))

print(f"Non-kural videos: {len(non_kural_vids)}")

# Check formatting of non-kural videos
unformatted = []
for vid, t, pls in non_kural_vids:
    if '|' not in t or t.endswith('!') or t.endswith('.m') or 'QC HOLD' in t or re.search(r'^[A-Za-z0-9\s|—\-_()]+$', t):
        unformatted.append((vid, t, pls))

print(f"Unformatted / needs standardization non-kural videos: {len(unformatted)}")
for vid, t, pls in unformatted:
    print(f"  [{vid}] '{t}' | Playlists: {pls}")
