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
print(f"Total sequential audio tracks to populate: {len(sequential_tracks)}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Use the tab that is already open to YouTube
    pl_page = None
    for page in ctx.pages:
        if 'youtube.com' in page.url:
            pl_page = page
            break
    if not pl_page:
        pl_page = ctx.pages[0]
        pl_page.goto(f'https://www.youtube.com/playlist?list={PLAYLIST_ID}', wait_until='domcontentloaded')

    # Step 1: Check existing videos in playlist
    print("Checking current videos in playlist...")
    existing_vids = pl_page.evaluate('''async (plId) => {
        const resp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                browseId: 'VL' + plId
            })
        });
        const data = await resp.json();
        const str = JSON.stringify(data);
        const matches = [];
        const regex = /"videoId":"([a-zA-Z0-9_-]{11})"/g;
        let m;
        while ((m = regex.exec(str)) !== null) {
            matches.push(m[1]);
        }
        return [...new Set(matches)];
    }''', PLAYLIST_ID)

    print(f"Already in playlist ({len(existing_vids)}): {existing_vids}")

    # Step 2: Determine tracks to add in sequential order
    tracks_to_add = [t for t in sequential_tracks if t['videoId'] not in existing_vids]
    print(f"Remaining tracks to add: {len(tracks_to_add)}")

    if not tracks_to_add:
        print("All tracks already added!")
    else:
        # Define the batch adder function
        pl_page.evaluate('''() => {
            window.__addVideosBatch = async function(plId, vids) {
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

                const actions = vids.map(vid => ({
                    action: 'ACTION_ADD_VIDEO',
                    addedVideoId: vid
                }));

                const payload = {
                    context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                    playlistId: plId,
                    actions: actions
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

        # Add in batches of 10
        batch_size = 10
        total_batches = (len(tracks_to_add) + batch_size - 1) // batch_size

        for b_idx in range(total_batches):
            batch = tracks_to_add[b_idx * batch_size : (b_idx + 1) * batch_size]
            vids = [t['videoId'] for t in batch]
            ch_summary = f"Ch {batch[0]['chapter_num']} to {batch[-1]['chapter_num']}"
            print(f"[{b_idx+1}/{total_batches}] Adding {len(vids)} tracks ({ch_summary}) ...", flush=True)

            res = pl_page.evaluate('([plId, vids]) => window.__addVideosBatch(plId, vids)', [PLAYLIST_ID, vids])
            status = res.get('status')
            if status == 'STATUS_SUCCEEDED':
                print(f"    Batch {b_idx+1} SUCCESS! Added {len(vids)} videos.", flush=True)
            else:
                print(f"    Batch {b_idx+1} result: {status} | {json.dumps(res)[:200]}", flush=True)
            time.sleep(1)

    # Step 3: Final verification of total count
    print("\nVerifying final playlist item count...")
    time.sleep(3)
    final_vids = pl_page.evaluate('''async (plId) => {
        const resp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                browseId: 'VL' + plId
            })
        });
        const data = await resp.json();
        const str = JSON.stringify(data);
        const matches = [];
        const regex = /"videoId":"([a-zA-Z0-9_-]{11})"/g;
        let m;
        while ((m = regex.exec(str)) !== null) {
            matches.push(m[1]);
        }
        return [...new Set(matches)];
    }''', PLAYLIST_ID)

    print(f"=== Population Complete! ===")
    print(f"Playlist ID: {PLAYLIST_ID}")
    print(f"Playlist URL: https://www.youtube.com/playlist?list={PLAYLIST_ID}")
    print(f"Total Unique Audio Tracks in Playlist: {len(final_vids)} / {len(sequential_tracks)}")

    with open('production/audio_master_playlist_summary.json', 'w', encoding='utf-8') as f:
        json.dump({
            'playlist_id': PLAYLIST_ID,
            'url': f'https://www.youtube.com/playlist?list={PLAYLIST_ID}',
            'total_tracks': len(final_vids),
            'expected_tracks': len(sequential_tracks),
            'video_ids': final_vids
        }, f, indent=2, ensure_ascii=False)
