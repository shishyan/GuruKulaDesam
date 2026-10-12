import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    captured = {}
    def on_req(req):
        if 'edit_playlist' in req.url:
            captured['url'] = req.url
            captured['headers'] = req.headers
            try:
                captured['data'] = req.post_data_json
            except Exception:
                captured['data'] = req.post_data
            print('Captured request!')
            
    page.on('request', on_req)
    
    # Click 3-dot menu on row 2
    row = page.locator('ytd-playlist-video-renderer').nth(2)
    menu_btn = row.locator('ytd-menu-renderer yt-icon-button#button')
    menu_btn.click()
    time.sleep(1)
    
    page.locator('ytd-menu-service-item-renderer:has-text("Move to top")').click()
    time.sleep(3)
    
    print('POST DATA JSON:')
    print(json.dumps(captured.get('data'), indent=2))
    
    with open('production/captured_edit_playlist_payload.json', 'w', encoding='utf-8') as f:
        json.dump(captured, f, indent=2)
