import sys
import json
import time
import base64
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PLAYLIST_ID = 'PLP-GdNkY_qyo'
TRACKS_FILE = 'production/thirukkural_audio_master_tracks.json'

with open(TRACKS_FILE, encoding='utf-8') as f:
    master_data = json.load(f)

sequential_tracks = master_data['sequential_tracklist']
target_order = {t['videoId']: idx for idx, t in enumerate(sequential_tracks)}
print(f"Total target sequential audio tracks: {len(target_order)}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Use tab with playlist or navigate
    pl_page = None
    for page in ctx.pages:
        if 'PLP-GdNkY_qyo' in page.url:
            pl_page = page
            break
    if not pl_page:
        pl_page = ctx.pages[0]
        pl_page.goto(f'https://www.youtube.com/playlist?list={PLAYLIST_ID}', wait_until='domcontentloaded')

    # Scroll to load all 155 items in DOM
    print("Scrolling to load all items into DOM...")
    for _ in range(5):
        pl_page.evaluate('() => window.scrollBy(0, 8000)')
        time.sleep(1.5)

    dom_items = pl_page.evaluate('''() => {
        const els = Array.from(document.querySelectorAll('ytd-playlist-video-renderer'));
        return els.map(el => ({
            videoId: el.data ? el.data.videoId : null,
            setVideoId: el.data ? el.data.setVideoId : null,
            title: el.data && el.data.title && el.data.title.runs ? el.data.title.runs[0].text : ''
        })).filter(x => x.videoId && x.setVideoId);
    }''')

    print(f"DOM items loaded with setVideoId: {len(dom_items)}")

    # Map to target position
    plan = []
    seen_vids = set()
    for it in dom_items:
        vid = it['videoId']
        if vid in target_order and vid not in seen_vids:
            seen_vids.add(vid)
            plan.append({
                'target_pos': target_order[vid],
                'videoId': vid,
                'setVideoId': it['setVideoId'],
                'title': it['title']
            })

    print(f"Matched items in plan: {len(plan)} / {len(dom_items)}")
    plan.sort(key=lambda x: x['target_pos'])

    # Reverse: move from bottom (154) up to top (0)
    reverse_plan = list(reversed(plan))
    total = len(reverse_plan)
    print(f"Beginning Reverse-Stack Move-To-Top execution ({total} actions)...", flush=True)

    # Define JS helper with exact tested headers & params
    pl_page.evaluate('''() => {
        window.__moveAudioVideoToTop = async function(svid) {
            const cookies = document.cookie.split('; ');
            let sapisid = '';
            for (const c of cookies) {
                if (c.startsWith('SAPISID=')) { sapisid = c.split('=')[1]; break; }
            }
            if (!sapisid) {
                for (const c of cookies) {
                    if (c.startsWith('__Secure-3PAPISID=')) { sapisid = c.split('=')[1]; break; }
                }
            }
            const now = Math.floor(Date.now() / 1000);
            const origin = 'https://www.youtube.com';
            const msg = `${now} ${sapisid} ${origin}`;
            
            const enc = new TextEncoder().encode(msg);
            const hashBuf = await crypto.subtle.digest('SHA-1', enc);
            const hashArr = Array.from(new Uint8Array(hashBuf));
            const hashHex = hashArr.map(b => b.toString(16).padStart(2, '0')).join('');
            const authHeader = `SAPISIDHASH ${now}_${hashHex}`;

            const payload = {
                context: ytcfg.get('INNERTUBE_CONTEXT'),
                actions: [
                    {
                        setVideoId: svid,
                        action: "ACTION_MOVE_VIDEO_AFTER"
                    }
                ],
                params: "CAFAAQ%3D%3D",
                playlistId: "PLP-GdNkY_qyo"
            };

            const response = await fetch('/youtubei/v1/browse/edit_playlist?prettyPrint=false', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': authHeader,
                    'X-Origin': origin,
                    'X-YouTube-Client-Name': '1',
                    'X-YouTube-Client-Version': ytcfg.get('INNERTUBE_CLIENT_VERSION')
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            return {
                httpStatus: response.status,
                status: data.status
            };
        };
    }''')

    success_count = 0
    for i, item in enumerate(reverse_plan):
        svid = item['setVideoId']
        target_pos = item['target_pos']
        vid = item['videoId']
        title = item['title']
        meta = sequential_tracks[target_pos]
        chap = meta['chapter_num']
        cname = meta['chapter_name']

        # Retry up to 3 times
        success = False
        res = None
        for attempt in range(3):
            try:
                res = pl_page.evaluate('svid => window.__moveAudioVideoToTop(svid)', svid)
                if res.get('status') == 'STATUS_SUCCEEDED':
                    success = True
                    break
            except Exception as e:
                res = {'error': str(e)}
            time.sleep(0.3)

        if success:
            success_count += 1
            print(f"[{i+1:03d}/{total:03d}] Moved to top: Pos {target_pos:03d} (Ch {chap:03d}: {cname}) -> {title[:40]}", flush=True)
        else:
            print(f"[{i+1:03d}/{total:03d}] FAILED Pos {target_pos:03d} (Ch {chap:03d}): {res}", flush=True)

        time.sleep(0.2)

    print(f"\nInnertube sorting pass finished: {success_count}/{total} succeeded!", flush=True)
    time.sleep(3)
    pl_page.reload(wait_until='domcontentloaded')
    time.sleep(4)
    pl_page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\audio_master_sorted_final.png')
    print("Verification screenshot saved to audio_master_sorted_final.png", flush=True)
