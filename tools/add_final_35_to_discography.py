import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PLAYLIST_ID = 'PLAjtBRKl_IlI'

with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    catalog = json.load(f)

missing = [s for s in catalog if 'Discography' not in s.get('playlists', [])]
print(f"Adding remaining {len(missing)} songs to Grand Master ({PLAYLIST_ID})...")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Inject batch adder helper
    page.evaluate('''() => {
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
    
    batch_size = 10
    total_batches = (len(missing) + batch_size - 1) // batch_size
    successful = 0
    failed = []
    
    for b_idx in range(total_batches):
        batch = missing[b_idx * batch_size : (b_idx + 1) * batch_size]
        vids = [s['video_id'] for s in batch]
        print(f"[{b_idx+1}/{total_batches}] Adding {len(vids)} songs...", flush=True)
        for s in batch:
            print(f"   + [{s['video_id']}] {s['canonical_title'][:50]}", flush=True)
            
        try:
            res = page.evaluate('([plId, vids]) => window.__addVideosBatch(plId, vids)', [PLAYLIST_ID, vids])
            status = res.get('status')
            if status == 'STATUS_SUCCEEDED':
                successful += len(vids)
                print(f"   ==> Batch {b_idx+1} SUCCEEDED! ({successful}/{len(missing)})", flush=True)
            else:
                print(f"   ==> Batch {b_idx+1} status: {status}", flush=True)
                failed.extend(batch)
        except Exception as e:
            print(f"   ==> Error: {e}", flush=True)
            failed.extend(batch)
        time.sleep(1.5)
        
    print(f"\nCompleted: {successful} added, {len(failed)} failed.")
    
    if successful > 0:
        added_vids = set(s['video_id'] for s in missing if s not in failed)
        for s in catalog:
            if s['video_id'] in added_vids:
                if 'Discography' not in s.get('playlists', []):
                    s['playlists'].append('Discography')
                    
        with open('master_all_598_songs_catalog.json', 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
            
        print("Updated master_all_598_songs_catalog.json! All songs now tagged in Discography.")
