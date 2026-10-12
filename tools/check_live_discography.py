import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Find existing tab or use first
    page = None
    for pg in ctx.pages:
        if 'youtube.com' in pg.url and 'studio' not in pg.url:
            page = pg
            break
    if not page:
        page = ctx.pages[0]
        
    print(f"Using tab with URL: {page.url}")
    print("Navigating to Discography playlist: https://www.youtube.com/playlist?list=PLAjtBRKl_IlI ...")
    page.goto('https://www.youtube.com/playlist?list=PLAjtBRKl_IlI', wait_until='domcontentloaded')
    time.sleep(5)
    
    # Get stats
    meta = page.evaluate('''() => {
        const title = document.querySelector('h1')?.innerText;
        const statsEl = document.querySelector('ytd-playlist-byline-renderer, #stats, .metadata-stats');
        const stats = statsEl ? statsEl.innerText.replace(/\\n+/g, ' ') : '';
        return { title, stats };
    }''')
    print("Discography Live Metadata:", meta)
    
    # Save a screenshot
    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\discography_live_check.png')
    print("Screenshot saved to discography_live_check.png")
