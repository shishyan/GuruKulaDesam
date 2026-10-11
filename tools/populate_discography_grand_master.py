import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PLAYLIST_ID = 'PLAjtBRKl_IlI'

# Load the audit results
with open('production/grand_master_audit_results.json', encoding='utf-8') as f:
    audit_data = json.load(f)

missing_songs = audit_data['missing_songs_list']
print(f"Total missing songs to add to Grand Master ({PLAYLIST_ID}): {len(missing_songs)}")

with sync_playwright() as p:
    print("Connecting to Chrome on port 9225...")
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Pick a suitable page
    pl_page = None
    for page in ctx.pages:
        if 'youtube.com' in page.url and 'studio' not in page.url:
            pl_page = page
            break
    if not pl_page:
        pl_page = ctx.pages[0]
        pl_page.goto(f'https://www.youtube.com/playlist?list={PLAYLIST_ID}', wait_until='domcontentloaded')
        
    print(f"Using tab: {pl_page.url}")
    
    # Inject batch adder helper into page
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
    
    # Batch add in chunks of 10
    batch_size = 10
    total_batches = (len(missing_songs) + batch_size - 1) // batch_size
    successful_adds = 0
    failed_adds = []
    
    for b_idx in range(total_batches):
        batch = missing_songs[b_idx * batch_size : (b_idx + 1) * batch_size]
        vids = [s['videoId'] for s in batch]
        print(f"[{b_idx+1}/{total_batches}] Adding {len(vids)} songs to Discography...", flush=True)
        for s in batch:
            print(f"   + [{s['videoId']}] {s['title'][:50]} ({s['genre']})", flush=True)
            
        try:
            res = pl_page.evaluate('([plId, vids]) => window.__addVideosBatch(plId, vids)', [PLAYLIST_ID, vids])
            status = res.get('status')
            if status == 'STATUS_SUCCEEDED':
                successful_adds += len(vids)
                print(f"   ==> Batch {b_idx+1} SUCCEEDED! ({successful_adds}/{len(missing_songs)})", flush=True)
            else:
                print(f"   ==> Batch {b_idx+1} returned status: {status} | details: {json.dumps(res)[:180]}", flush=True)
                failed_adds.extend(batch)
        except Exception as e:
            print(f"   ==> Error in Batch {b_idx+1}: {e}", flush=True)
            failed_adds.extend(batch)
            
        time.sleep(1.5)
        
    print(f"\n========================================================")
    print(f"Population finished: {successful_adds} added, {len(failed_adds)} failed.")
    print(f"========================================================")
    
    # Update master_all_598_songs_catalog.json
    if successful_adds > 0:
        added_vids = set(s['videoId'] for s in missing_songs if s not in failed_adds)
        with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
            catalog = json.load(f)
            
        for item in catalog:
            if item['video_id'] in added_vids:
                if 'Discography' not in item.get('playlists', []):
                    item['playlists'].append('Discography')
                    
        with open('master_all_598_songs_catalog.json', 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
            
        print("Updated master_all_598_songs_catalog.json with Discography tags.")
