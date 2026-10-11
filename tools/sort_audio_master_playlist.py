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
# Map videoId -> target position
target_order = {}
for idx, t in enumerate(sequential_tracks):
    target_order[t['videoId']] = idx

print(f"Target sequential tracks: {len(target_order)}")

def get_set_video_id(item_id):
    pad = len(item_id) % 4
    if pad:
        item_id += '=' * (4 - pad)
    decoded = base64.urlsafe_b64decode(item_id).decode('utf-8', errors='ignore')
    return decoded.split('.')[-1]

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    pl_page = None
    for page in ctx.pages:
        if 'youtube.com' in page.url:
            pl_page = page
            break
    if not pl_page:
        pl_page = ctx.pages[0]
        pl_page.goto(f'https://www.youtube.com/playlist?list={PLAYLIST_ID}', wait_until='domcontentloaded')

    # Step 1: Fetch all items in playlist with itemId & videoId
    print("Fetching all items from playlist with continuation...")
    all_items = pl_page.evaluate('''async (plId) => {
        let items = [];
        let resp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                browseId: 'VL' + plId
            })
        });
        let data = await resp.json();
        
        function extractFromContents(obj) {
            const str = JSON.stringify(obj);
            // Search playlistVideoRenderer items
            const found = [];
            function traverse(node) {
                if (!node || typeof node !== 'object') return;
                if (node.playlistVideoRenderer) {
                    const r = node.playlistVideoRenderer;
                    found.push({
                        videoId: r.videoId,
                        itemId: r.navigationEndpoint?.watchEndpoint?.playlistItemId || '',
                        setVideoId: r.setVideoId || '',
                        title: r.title?.runs?.[0]?.text || ''
                    });
                }
                for (const k in node) {
                    traverse(node[k]);
                }
            }
            traverse(obj);
            return found;
        }

        items = items.concat(extractFromContents(data));

        // Follow continuation tokens if any
        function findContinuationToken(node) {
            if (!node || typeof node !== 'object') return null;
            if (node.continuationItemRenderer?.continuationEndpoint?.continuationCommand?.token) {
                return node.continuationItemRenderer.continuationEndpoint.continuationCommand.token;
            }
            for (const k in node) {
                const t = findContinuationToken(node[k]);
                if (t) return t;
            }
            return null;
        }

        let token = findContinuationToken(data);
        while (token && items.length < 200) {
            let cResp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                    continuation: token
                })
            });
            let cData = await cResp.json();
            const cFound = extractFromContents(cData);
            if (cFound.length === 0) break;
            items = items.concat(cFound);
            token = findContinuationToken(cData);
        }

        return items;
    }''', PLAYLIST_ID)

    print(f"Total items fetched from playlist: {len(all_items)}")

    # Map items to target order
    matched_plan = []
    unmatched_items = []
    for it in all_items:
        vid = it['videoId']
        svid = it.get('setVideoId')
        if not svid and it.get('itemId'):
            svid = get_set_video_id(it['itemId'])
        
        target_pos = target_order.get(vid)
        if target_pos is not None:
            matched_plan.append({
                'target_pos': target_pos,
                'videoId': vid,
                'setVideoId': svid,
                'title': it.get('title', '')
            })
        else:
            unmatched_items.append(it)

    print(f"Matched items to sort: {len(matched_plan)} / {len(all_items)}")

    # Sort plan by target_pos ascending (0, 1, 2, ..., N)
    matched_plan.sort(key=lambda x: x['target_pos'])

    # Reverse plan: move each from bottom (N) up to top (0)
    reverse_plan = list(reversed(matched_plan))
    print(f"Beginning Innertube Move-To-Top execution ({len(reverse_plan)} actions)...", flush=True)

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

    success_count = 0
    total = len(reverse_plan)
    for i, item in enumerate(reverse_plan, 1):
        svid = item['setVideoId']
        target_p = item['target_pos']
        meta = sequential_tracks[target_p]
        ch_str = f"Ch {meta['chapter_num']}: {meta['chapter_name']}"

        res = pl_page.evaluate('([plId, svid]) => window.__moveVideoToTop(plId, svid)', [PLAYLIST_ID, svid])
        status = res.get('status')
        if status == 'STATUS_SUCCEEDED':
            success_count += 1
            if i % 15 == 0 or i == total:
                print(f"[{i}/{total}] (Pos {target_p}) {ch_str} | Moved to top -> STATUS_SUCCEEDED", flush=True)
        else:
            print(f"[{i}/{total}] (Pos {target_p}) Failed: {status} | {json.dumps(res)[:150]}", flush=True)
        time.sleep(0.1)

    print(f"\nSorting Complete: {success_count}/{total} operations succeeded!")

    # Verify final sorted order
    time.sleep(3)
    pl_page.goto(f'https://www.youtube.com/playlist?list={PLAYLIST_ID}', wait_until='domcontentloaded')
    time.sleep(4)
    pl_page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\audio_playlist_sorted_final.png')
    print("Screenshot saved to audio_playlist_sorted_final.png")
