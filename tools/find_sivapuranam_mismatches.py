import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

# Find all videos with non-Sivapuranam titles that might have Sivapuranam lyrics
candidates = []
for v in videos:
    vid = v['id']
    title = v['snippet']['title']
    desc = v['snippet']['description']
    
    if "provided to youtube by distrokid" in desc.lower():
        continue
        
    t_lower = title.lower()
    # If title is NOT Sivapuranam, but mentions Shiva / Thevaram / Thiruvasagam
    if not any(k in t_lower for k in ['சிவபுராணம்', 'sivapuranam']):
        if any(k in t_lower for k in ['திருப்புலம்பல்', 'வேதஸார', 'வேதசார்', 'திருவையாறு', 'குழைத்த பத்து', 'நடராஜர் பத்து', 'அபிராத', 'அன்பு மாலை', 'அருளியல்', 'தியாக வண்ண']):
            candidates.append((vid, title))

print(f"Total candidate Shiva videos to check for Sivapuranam mismatch: {len(candidates)}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    sivapuranam_mismatches = []
    for idx, (vid, title) in enumerate(candidates):
        try:
            info = page.evaluate('''async (v) => {
                const resp = await fetch('/youtubei/v1/player?prettyPrint=false', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                        videoId: v
                    })
                });
                const data = await resp.json();
                const d = data.videoDetails || {};
                return {
                    videoId: v,
                    title: d.title || '',
                    desc: d.shortDescription || ''
                };
            }''', vid)
            
            d_text = info.get('desc', '')
            if 'நமச்சிவாய வாழ்க' in d_text:
                sivapuranam_mismatches.append({
                    'id': vid,
                    'title': title,
                    'desc_len': len(d_text)
                })
                print(f"  [MISMATCH] {vid}: {title} has Sivapuranam lyrics!", flush=True)
            elif 'பாடல் வரிகள்' not in d_text and len(d_text) < 500:
                print(f"  [NO LYRICS] {vid}: {title} (len {len(d_text)})", flush=True)
            else:
                print(f"  [OK / OTHER] {vid}: {title}", flush=True)
        except Exception as e:
            print(f"  [ERROR] {vid}: {e}", flush=True)
        time.sleep(0.2)

    print(f"\n=======================================================")
    print(f"Total Videos with Wrong Sivapuranam Lyrics: {len(sivapuranam_mismatches)}")
    print(f"=======================================================")
    with open('production/sivapuranam_mismatches.json', 'w', encoding='utf-8') as f:
        json.dump(sivapuranam_mismatches, f, indent=2, ensure_ascii=False)
