import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Find the page with playlist URL
    pl_page = None
    for page in ctx.pages:
        if 'PLP-GdNkY_qyo' in page.url:
            pl_page = page
            break

    if not pl_page:
        pl_page = ctx.pages[0]
        pl_page.goto('https://www.youtube.com/playlist?list=PLP-GdNkY_qyo', wait_until='domcontentloaded')

    print("Found playlist page:", pl_page.url)

    res = pl_page.evaluate('''async () => {
        const cookies = document.cookie.split('; ');
        let sapisid = '';
        for (const c of cookies) {
            if (c.startsWith('SAPISID=')) {
                sapisid = c.split('=')[1];
                break;
            }
        }
        if (!sapisid) {
            for (const c of cookies) {
                if (c.startsWith('__Secure-3PAPISID=')) {
                    sapisid = c.split('=')[1];
                    break;
                }
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
            playlistId: 'PLP-GdNkY_qyo',
            actions: [
                {
                    action: 'ACTION_ADD_VIDEO',
                    addedVideoId: 'SWAjAbur-TQ'
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
    }''')

    print("Innertube ACTION_ADD_VIDEO result:")
    print("Status:", res.get('status'))
    print("Keys:", list(res.keys()))
    if 'actions' in res:
        print("Actions in response:", res['actions'])
    else:
        print("Full response snippet:", json.dumps(res, indent=2)[:400])
