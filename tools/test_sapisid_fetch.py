import sys, time, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    res = page.evaluate('''async () => {
        // Find SAPISID
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
        
        const now = Math.floor(Date.now() / 1000);
        const origin = 'https://www.youtube.com';
        const msg = `${now} ${sapisid} ${origin}`;
        
        const enc = new TextEncoder().encode(msg);
        const hashBuf = await crypto.subtle.digest('SHA-1', enc);
        const hashArr = Array.from(new Uint8Array(hashBuf));
        const hashHex = hashArr.map(b => b.toString(16).padStart(2, '0')).join('');
        const authHeader = `SAPISIDHASH ${now}_${hashHex}`;
        
        // Now test fetch with this exact Authorization header
        const payload = {
            context: ytcfg.get('INNERTUBE_CONTEXT'),
            actions: [
                {
                    setVideoId: "208A2CA64C241A85",
                    action: "ACTION_MOVE_VIDEO_AFTER"
                }
            ],
            params: "CAFAAQ%3D%3D",
            playlistId: "PLW7qBZp_Q8Ro"
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
            status: response.status,
            authHeader: authHeader.substring(0, 30),
            data: data
        };
    }''')
    
    print('Response status:', res.get('status'))
    data = res.get('data', {})
    print('Status field:', data.get('status'))
    print('Action count in response:', len(data.get('actions', [])))
    print('Logged in service tracking:', json.dumps(data.get('responseContext', {}).get('serviceTrackingParams', []), indent=2)[:300])
