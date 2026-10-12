import os, glob, json
import sys
sys.path.insert(0, '.')
from production.google_flow_engine import get_media_duration

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

# Also check 598 catalog if available
catalog_598 = {}
if os.path.exists('master_all_598_songs_catalog.json'):
    with open('master_all_598_songs_catalog.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            for item in data:
                if 'id' in item:
                    catalog_598[item['id']] = item
                elif 'track_id' in item:
                    catalog_598[item['track_id']] = item
        elif isinstance(data, dict):
            catalog_598 = data

murugan_pub = set()
if os.path.exists('production/murugan_published_manifest.json'):
    with open('production/murugan_published_manifest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for r in data.get('releases', []):
            if r.get('status') == 'PUBLISHED':
                murugan_pub.add(r.get('track_id'))

vinayagar_pub = set()
if os.path.exists('production/vinayagar_published_manifest.json'):
    with open('production/vinayagar_published_manifest.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for r in data.get('releases', []):
            if r.get('status') == 'PUBLISHED':
                vinayagar_pub.add(r.get('track_id'))

cached = glob.glob('source/youtube/*.m4a')

results = []
for p in cached:
    tid = os.path.splitext(os.path.basename(p))[0]
    meta = live_meta.get(tid, {})
    meta598 = catalog_598.get(tid, {})
    title = meta.get('title') or meta598.get('title') or 'Unknown'
    playlist = meta.get('playlist_title') or meta598.get('playlist') or meta598.get('category') or 'Unknown'
    
    dur = 0
    try:
        dur = get_media_duration(p)
    except Exception as e:
        pass
    
    is_pub_m = tid in murugan_pub
    is_pub_v = tid in vinayagar_pub
    
    results.append({
        'tid': tid,
        'title': title,
        'playlist': playlist,
        'duration': dur,
        'dur_m': dur / 60,
        'pub_m': is_pub_m,
        'pub_v': is_pub_v,
    })

print(f"Total cached audio files: {len(cached)}")
print(f"Published Murugan: {len(murugan_pub)}")
print(f"Published Vinayagar: {len(vinayagar_pub)}")

print('\n=== CACHED UNPUBLISHED TRACKS (<= 480s / 8 min) ===')
unpub = [r for r in results if not r['pub_m'] and not r['pub_v'] and r['duration'] <= 480]
unpub.sort(key=lambda x: (x['playlist'], x['duration']))
for r in unpub:
    print(f"{r['tid']} | {r['duration']:.1f}s ({r['dur_m']:.1f}m) | [{r['playlist']}] {r['title']}")

print(f'\nTotal eligible unpublished cached <= 8m: {len(unpub)}')
