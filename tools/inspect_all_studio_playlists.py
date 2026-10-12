import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    print("Navigating to https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists ...")
    page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists')
    time.sleep(5)

    # Let's inspect ALL playlists in the Studio table
    pls = page.evaluate('''() => {
        const results = [];
        document.querySelectorAll('ytcp-playlist-row, tr, [id="row-container"]').forEach(r => {
            const titleEl = r.querySelector('#title, .title, a');
            const linkEl = r.querySelector('a[href*="/playlist/"]');
            const countEl = r.querySelector('.video-count, [id*="video-count"], [id*="count"]');
            const visEl = r.querySelector('.visibility-cell, [id*="visibility"]');
            if (titleEl) {
                results.push({
                    title: titleEl.innerText.trim(),
                    href: linkEl ? linkEl.href : '',
                    count: countEl ? countEl.innerText.trim() : '',
                    visibility: visEl ? visEl.innerText.trim() : '',
                    fullRow: (r.innerText || '').replace(/\\n+/g, ' | ')
                });
            }
        });
        return results;
    }''')

    print(f"Total playlists found in Studio: {len(pls)}")
    for p_info in pls:
        print(f"  {p_info['title']} (count: {p_info['count']}, vis: {p_info['visibility']}) -> {p_info['href']}")

    page.close()
