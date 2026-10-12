import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Scroll down to ensure bottom items are loaded
    for _ in range(4):
        rows = page.locator('ytd-playlist-video-renderer')
        rows.last.scroll_into_view_if_needed()
        time.sleep(1.5)
        
    rows = page.locator('ytd-playlist-video-renderer')
    total = rows.count()
    print(f'Total loaded rows: {total}', flush=True)
    
    last_row = rows.last
    title = last_row.locator('#video-title').inner_text().strip()
    href = last_row.locator('#video-title').get_attribute('href')
    idx = last_row.locator('#index').inner_text().strip()
    print(f'Last item ({idx}): {title[:40]} | href={href}', flush=True)
