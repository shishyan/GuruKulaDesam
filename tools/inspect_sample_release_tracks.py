import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    # Let's inspect the release on YouTube Music
    print("Navigating to https://music.youtube.com/browse/MPREb_zOXoDZxwePN ...")
    page.goto('https://music.youtube.com/browse/MPREb_zOXoDZxwePN')
    time.sleep(5)

    music_tracks = page.evaluate('''() => {
        const title = document.querySelector('h1, yt-formatted-string[class*="title"]')?.innerText;
        const tracks = [];
        document.querySelectorAll('ytmusic-responsive-list-item-renderer').forEach(el => {
            const trackTitle = el.querySelector('.title-column, [class*="title"] a, a')?.innerText;
            const playLink = el.querySelector('a[href*="watch?v="]')?.href;
            const duration = el.querySelector('.fixed-columns, [class*="duration"]')?.innerText;
            tracks.push({
                title: trackTitle,
                link: playLink,
                duration: duration
            });
        });
        return { title, tracks };
    }''')
    print("Music Tracks Info:", music_tracks)

    # Let's also inspect Studio release page
    print("\nNavigating to https://studio.youtube.com/release/b_zOXoDZxwePN/overview ...")
    page.goto('https://studio.youtube.com/release/b_zOXoDZxwePN/overview')
    time.sleep(5)

    studio_tracks = page.evaluate('''() => {
        const title = document.querySelector('h1, #title')?.innerText;
        const rows = [];
        document.querySelectorAll('tr, [id*="row"], ytcp-entity-table-row').forEach(r => {
            const a = r.querySelector('a');
            rows.push({
                text: r.innerText.replace(/\\n+/g, ' | '),
                href: a ? a.href : ''
            });
        });
        return {
            title,
            body: document.body.innerText.slice(0, 800),
            rows: rows.slice(0, 10)
        };
    }''')
    print("\nStudio Tracks Info:")
    print("Title:", studio_tracks.get('title'))
    print("Body snippet:", repr(studio_tracks.get('body')[:300]))
    print("Rows:", studio_tracks.get('rows'))

    page.close()
