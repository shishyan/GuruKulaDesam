import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    def safe_eval(expr, retries=5):
        for i in range(retries):
            try:
                time.sleep(2)
                return page.evaluate(expr)
            except Exception as e:
                print(f"Eval attempt {i+1} failed: {e}. Retrying...")
                time.sleep(2)
        return None

    # First, let's look at public channel playlists directly
    print("Navigating to https://www.youtube.com/@gurukuladesam/playlists ...")
    page.goto('https://www.youtube.com/@gurukuladesam/playlists')
    time.sleep(4)

    channel_pls = safe_eval('''() => {
        const items = [];
        // Scroll a bit
        window.scrollBy(0, 1000);
        document.querySelectorAll('ytd-rich-item-renderer, ytd-grid-playlist-renderer').forEach(el => {
            const titleEl = el.querySelector('#video-title, h3, a');
            const linkEl = el.querySelector('a[href*="list="]');
            if (titleEl && linkEl) {
                items.push({
                    title: titleEl.innerText.trim(),
                    href: linkEl.href
                });
            }
        });
        return items;
    }''')
    print(f"Public Playlists found ({len(channel_pls) if channel_pls else 0}):")
    if channel_pls:
        for it in channel_pls:
            print("  ", it['title'], "-->", it['href'])

    # Next, let's look at public channel releases directly
    print("\nNavigating to https://www.youtube.com/@gurukuladesam/releases ...")
    page.goto('https://www.youtube.com/@gurukuladesam/releases')
    time.sleep(4)

    channel_rel = safe_eval('''() => {
        const items = [];
        window.scrollBy(0, 1000);
        document.querySelectorAll('ytd-rich-item-renderer, ytd-grid-playlist-renderer, ytd-playlist-renderer, ytd-compact-station-renderer').forEach(el => {
            const titleEl = el.querySelector('#video-title, #title, h3, a');
            const linkEl = el.querySelector('a[href*="list="], a[href*="watch?v="]');
            if (titleEl && linkEl) {
                items.push({
                    title: titleEl.innerText.trim(),
                    href: linkEl.href
                });
            }
        });
        return {
            items: items,
            url: window.location.href,
            body: document.body.innerText.slice(0, 500)
        };
    }''')
    print("Public Releases page:")
    if channel_rel:
        print("  Current URL:", channel_rel.get('url'))
        print("  Body snippet:", repr(channel_rel.get('body', '')[:200]))
        for it in channel_rel.get('items', []):
            print("  Release item:", it)

    # Next, let's look at YouTube Studio Playlists
    print("\nNavigating to https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists ...")
    page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists')
    time.sleep(6)

    studio_pls = safe_eval('''() => {
        const links = [];
        document.querySelectorAll('a[href*="playlist?list="], a[href*="/playlist/"]').forEach(a => {
            links.push({
                text: a.innerText.trim(),
                href: a.href
            });
        });
        const rows = [];
        document.querySelectorAll('ytcp-playlist-row, tr, [id="row-container"]').forEach(r => {
            const title = r.querySelector('#title, .title, a');
            const count = r.querySelector('.video-count, [id*="count"]');
            if (title) {
                rows.push({
                    title: title.innerText.trim(),
                    count: count ? count.innerText.trim() : ''
                });
            }
        });
        return {
            links: links,
            rows: rows,
            body: document.body.innerText.slice(0, 1000)
        };
    }''')
    print("Studio Playlists:")
    if studio_pls:
        print("  Snippet:", repr(studio_pls.get('body', '')[:300]))
        print("  Rows:", studio_pls.get('rows'))
        print("  Links:", studio_pls.get('links'))

    page.close()
