import sys
import json
import re
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]

    # Let's test fetch for MPREb_zOXoDZxwePN
    res = page.evaluate('''async () => {
        const resp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                browseId: 'MPREb_zOXoDZxwePN'
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
        return {
            uniqueVideoIds: [...new Set(matches)],
            totalFound: matches.length
        };
    }''')
    print("Test MPREb_zOXoDZxwePN Video IDs:", res)
