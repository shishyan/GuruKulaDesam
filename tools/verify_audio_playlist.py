import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    page.goto('https://www.youtube.com/playlist?list=PLP-GdNkY_qyo', wait_until='domcontentloaded')
    time.sleep(5)

    info = page.evaluate('''() => {
        const title = document.querySelector('h1')?.innerText;
        const statsEl = document.querySelector('ytd-playlist-byline-renderer, #stats, .metadata-stats');
        const statsText = statsEl ? statsEl.innerText.replace(/\\n+/g, ' ') : '';
        
        // Also sample first 5 and last 5 videos in DOM
        const vids = Array.from(document.querySelectorAll('ytd-playlist-video-renderer')).map(v => {
            const t = v.querySelector('#video-title')?.innerText;
            const a = v.querySelector('a')?.href;
            return { title: t, href: a };
        });

        return {
            title,
            statsText,
            renderedVideosCount: vids.length,
            first5: vids.slice(0, 5),
            bodySnippet: document.body.innerText.slice(0, 500)
        };
    }''')

    print("Title:", info.get('title'))
    print("Stats:", info.get('statsText'))
    print("Rendered Videos:", info.get('renderedVideosCount'))
    print("\nFirst 5 tracks:")
    for v in info.get('first5', []):
        print(f"  {v['title']}")

    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\new_audio_playlist_verified.png')
    page.close()
