import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]

    # Let's see what cookies and tokens we have
    test_create = page.evaluate('''async () => {
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
        const origin = 'https://studio.youtube.com';
        const hash = await sha1(`${timestamp} ${sapisid} ${origin}`);
        const authHeader = `SAPISIDHASH ${timestamp}_${hash}`;
        
        const context = window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {};
        
        const resp = await fetch('/youtubei/v1/playlist/create?prettyPrint=false', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authHeader,
                'X-Origin': origin
            },
            body: JSON.stringify({
                context: context,
                title: 'திருக்குறள் | Thirukkural — Audio Master Collection',
                privacyStatus: 'PUBLIC',
                description: 'Official Thirukkural Audio Master Collection by Guru Kula Desam (@gurukuladesam). All released chapters in sequential order.'
            })
        });
        
        const resText = await resp.text();
        return { status: resp.status, body: resText };
    }''')

    print("Playlist create response:", test_create)
