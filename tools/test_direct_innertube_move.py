import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Test moving setVideoId: F3D73C336952E57D (Thirukkural Agara Muthala - Item 0) to top
    print('Testing direct fetch to /youtubei/v1/browse/edit_playlist...', flush=True)
    res = page.evaluate('''async () => {
        const payload = {
            context: ytcfg.get('INNERTUBE_CONTEXT'),
            actions: [
                {
                    setVideoId: "F3D73C336952E57D",
                    action: "ACTION_MOVE_VIDEO_AFTER"
                }
            ],
            params: "CAFAAQ%3D%3D",
            playlistId: "PLW7qBZp_Q8Ro"
        };
        const response = await fetch('/youtubei/v1/browse/edit_playlist?prettyPrint=false', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-YouTube-Client-Name': '1',
                'X-YouTube-Client-Version': ytcfg.get('INNERTUBE_CLIENT_VERSION')
            },
            body: JSON.stringify(payload)
        });
        const json = await response.json();
        return {
            status: response.status,
            statusText: response.statusText,
            data: json
        };
    }''')
    
    print('Result status:', res.get('status'))
    print('Result data:', json.dumps(res.get('data'), indent=2)[:500])
