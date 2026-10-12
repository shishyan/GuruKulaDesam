import sys, time, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Test with credentials: 'include'
    res = page.evaluate('''async () => {
        const payload = {
            context: ytcfg.get('INNERTUBE_CONTEXT'),
            actions: [
                {
                    setVideoId: "56B44F6D10557CC6",
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
                'X-YouTube-Client-Name': '1',
                'X-YouTube-Client-Version': ytcfg.get('INNERTUBE_CLIENT_VERSION')
            },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        return {
            status: response.status,
            data: data
        };
    }''')
    
    print('Response status:', res.get('status'))
    data = res.get('data', {})
    print('Status field:', data.get('status'))
    print('Full Response JSON:')
    print(json.dumps(data, indent=2)[:500])
