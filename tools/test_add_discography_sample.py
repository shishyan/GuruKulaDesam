import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PLAYLIST_ID = 'PLAjtBRKl_IlI'
TEST_VID = '02C8glMmetw'  # Ch 1 கடவுள் வாழ்த்து

print(f"Connecting to CDP on 9225 to test adding {TEST_VID} to {PLAYLIST_ID}...")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Pick YouTube page without navigating
    page = None
    for pg in ctx.pages:
        if 'youtube.com' in pg.url and 'studio' not in pg.url:
            page = pg
            break
            
    if not page:
        print("No youtube.com tab found!")
        sys.exit(1)
        
    print(f"Found YouTube page: {page.url}")
    
    res = page.evaluate('''async ([plId, vid]) => {
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
        const origin = window.location.origin;
        const msg = `${now} ${sapisid} ${origin}`;
        
        const enc = new TextEncoder().encode(msg);
        const hashBuf = await crypto.subtle.digest('SHA-1', enc);
        const hashArr = Array.from(new Uint8Array(hashBuf));
        const hashHex = hashArr.map(b => b.toString(16).padStart(2, '0')).join('');
        const authHeader = `SAPISIDHASH ${now}_${hashHex}`;

        const payload = {
            context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
            actions: [
                {
                    action: "ACTION_ADD_VIDEO",
                    addedVideoId: vid
                }
            ],
            playlistId: plId
        };

        const resp = await fetch('/youtubei/v1/browse/edit_playlist?prettyPrint=false', {
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

        const data = await resp.json();
        return {
            status: resp.status,
            innertubeStatus: data.status,
            data: data
        };
    }''', [PLAYLIST_ID, TEST_VID])
    
    print("Add Test Result:", res.get('status'), res.get('innertubeStatus'))
    print("Response details:", json.dumps(res)[:300])
