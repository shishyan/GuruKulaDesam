import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PLAYLIST_ID = 'PLP-GdNkY_qyo'
TRACKS_FILE = 'production/thirukkural_audio_master_tracks.json'

with open(TRACKS_FILE, encoding='utf-8') as f:
    master_data = json.load(f)

sequential_tracks = master_data['sequential_tracklist']
target_order = {t['videoId']: idx for idx, t in enumerate(sequential_tracks)}
print(f"Total target sequential tracks: {len(target_order)}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Use tab with playlist
    pl_page = None
    for page in ctx.pages:
        if 'PLP-GdNkY_qyo' in page.url:
            pl_page = page
            break
    if not pl_page:
        pl_page = ctx.pages[0]
        pl_page.goto(f'https://www.youtube.com/playlist?list={PLAYLIST_ID}', wait_until='domcontentloaded')

    # Scroll down to load all 155 items in DOM
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
    print(f"Beginning Reverse-Stack Move-To-Top execution ({len(reverse_plan)} actions)...", flush=True)

    # Define JS move helper
    pl_page.evaluate('''() => {
        window.__moveVideoToTop = async function(plId, svid) {
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
            async function sha1(str) {
                const buffer = new TextEncoder().encode(str);
                const digest = await crypto.subtle.digest('SHA-1', buffer);
                return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
            }
            const timestamp = Math.floor(Date.now() / 1000);
            const origin = window.location.origin;
            const hash = await sha1(`${timestamp} ${sapisid} ${origin}`);
            const authHeader = `SAPISIDHASH ${timestamp}_${hash}`;

            const payload = {
                context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                playlistId: plId,
                actions: [
                    {
                        action: 'ACTION_MOVE_VIDEO_AFTER',
                        setVideoId: svid
                    }
                ]
            };

            const resp = await fetch('/youtubei/v1/browse/edit_playlist?prettyPrint=false', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': authHeader,
                    'X-Origin': origin
                },
                body: JSON.stringify(payload)
            });
            return await resp.json();
        };
    }''')

    success = 0
    total = len(reverse_plan)
    for i, item in enumerate(reverse_plan, 1):
        svid = item['setVideoId']
        target_p = item['target_pos']
        meta = sequential_tracks[target_p]
        ch_str = f"Ch {meta['chapter_num']}: {meta['chapter_name']}"

        res = pl_page.evaluate('([plId, svid]) => window.__moveVideoToTop(plId, svid)', [PLAYLIST_ID, svid])
        status = res.get('status')
        if status == 'STATUS_SUCCEEDED':
            success += 1
            if i % 15 == 0 or i == total:
                print(f"[{i}/{total}] (Pos {target_p:3d}) {ch_str} | Moved to top -> STATUS_SUCCEEDED", flush=True)
        else:
            print(f"[{i}/{total}] (Pos {target_p:3d}) Failed: {status}", flush=True)
        time.sleep(0.12)

    print(f"\n=== Reordering Complete! ===")
    print(f"Successfully ordered {success}/{total} tracks strictly from Chapter 1 to Chapter 110!")
