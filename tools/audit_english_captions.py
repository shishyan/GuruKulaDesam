import json, sys, re, concurrent.futures, urllib.request

sys.stdout.reconfigure(encoding='utf-8')

vids = json.load(open('production/youtube_backup/videos.json', encoding='utf-8'))
print(f"Total videos to scan: {len(vids)}")

def scan_video(v):
    vid = v['id']
    title = v['snippet']['title']
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
    except Exception as e:
        return {'vid': vid, 'title': title, 'error': str(e)}
        
    tracks = []
    m = re.search(r'"captionTracks":(\[.*?\])', html)
    if m:
        try:
            tracks = json.loads(m.group(1))
        except:
            pass
            
    english_tracks = []
    for t in tracks:
        lang = t.get('languageCode', '')
        if lang.startswith('en'):
            english_tracks.append(t)
            
    return {
        'vid': vid,
        'title': title,
        'total_tracks': len(tracks),
        'english_tracks': english_tracks,
        'all_tracks': tracks
    }

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scan_video, v) for v in vids]
    for i, f in enumerate(concurrent.futures.as_completed(futures), 1):
        r = f.result()
        if r.get('english_tracks'):
            print(f"FOUND ENGLISH CC: {r['vid']} | {r['title']} | {len(r['english_tracks'])} English track(s)")
        results.append(r)
        if i % 50 == 0:
            print(f"Scanned {i}/{len(vids)}...")

with open('production/caption_tracks_audit.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

en_found = [r for r in results if r.get('english_tracks')]
print("=" * 60)
print(f"SCAN COMPLETED:")
print(f"Total videos scanned: {len(results)}")
print(f"Videos with English CC tracks: {len(en_found)}")
print("=" * 60)
