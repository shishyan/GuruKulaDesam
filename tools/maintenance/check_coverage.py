import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('all_uploads.json', 'r', encoding='utf-8') as f:
    uploads = json.load(f)

with open('all_playlist_items.json', 'r', encoding='utf-8') as f:
    pl_items = json.load(f)

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

upload_vids = {v['video_id'] for v in uploads}
pl_vids = {it['video_id'] for it in pl_items}
all_unique_vids = upload_vids.union(pl_vids)

print(f"Total uploads in all_uploads.json: {len(uploads)} ({len(upload_vids)} unique)")
print(f"Total items in all_playlist_items.json: {len(pl_items)} ({len(pl_vids)} unique)")
print(f"Union of video IDs in channel uploads & playlists: {len(all_unique_vids)}")
print(f"Total tracks in catalog.json: {len(catalog)}")
print(f"Total tracks in live_youtube_metadata.json: {len(live_meta)}")

# Check overlap
cat_vids = {c.get('youtube_id') for c in catalog if c.get('youtube_id')}
print(f"Catalog tracks with youtube_id: {len(cat_vids)}")
print(f"Overlap between catalog and unique videos: {len(cat_vids.intersection(all_unique_vids))}")
