import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()
    page.goto('https://www.youtube.com/@gurukuladesam/playlists', wait_until='domcontentloaded')
    time.sleep(4)
    for _ in range(4):
        page.evaluate('() => window.scrollBy(0, 3000)')
        time.sleep(1)
        
    playlists = page.evaluate('''() => {
        const items = [];
        const seen = new Set();
        document.querySelectorAll('ytd-lockup-view-model, ytd-grid-playlist-renderer, ytd-playlist-renderer').forEach(el => {
            const titleEl = el.querySelector('h3, #video-title, .yt-core-attributed-string');
            const linkEl = el.querySelector('a[href*="list="]');
            const countEl = el.querySelector('.badge-shape-wiz__text, .badge, [aria-label*="video"], [aria-label*="track"]');
            if (titleEl && linkEl) {
                const title = titleEl.innerText.trim();
                const url = linkEl.href;
                if (!seen.has(url)) {
                    seen.add(url);
                    items.push({
                        title: title,
                        url: url,
                        count: countEl ? countEl.innerText.trim() : ''
                    });
                }
            }
        });
        return items;
    }''')
    print(f'Total public playlists found: {len(playlists)}')
    for pl in playlists:
        print(f"  {pl['title']} | count: {pl['count']} | {pl['url']}")
    page.close()
