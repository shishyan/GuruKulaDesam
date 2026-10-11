import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]

    # Navigate page to playlist edit or www.youtube.com first so origin is https://www.youtube.com
    page.goto('https://www.youtube.com/playlist?list=PLP-GdNkY_qyo')
    time.sleep(3)

    res = page.evaluate('''async () => {
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

    print("Add video response:", res.get('status'), list(res.keys()))
    print("Full response:", json.dumps(res, indent=2)[:500])
