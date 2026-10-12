import sys
import time
import json
import gzip
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    captured = {}
    def on_req(req):
        if 'edit_playlist' in req.url and req.method == 'POST':
            captured['url'] = req.url
            buf = req.post_data_buffer
            if buf:
                try:
                    decompressed = gzip.decompress(buf)
                    data = json.loads(decompressed.decode('utf-8'))
                except Exception:
                    data = json.loads(buf.decode('utf-8'))
                captured['data'] = data
                print('Successfully captured & decompressed edit_playlist payload!', flush=True)
            
    page.on('request', on_req)
    
    # Click 3-dot menu on row 3
    row = page.locator('ytd-playlist-video-renderer').nth(3)
    menu_btn = row.locator('ytd-menu-renderer yt-icon-button#button')
    menu_btn.click()
    time.sleep(1)
    
    page.locator('ytd-menu-service-item-renderer:has-text("Move to top")').click()
    time.sleep(3)
    
    if 'data' in captured:
        print('DECOMPRESSED PAYLOAD:')
        print(json.dumps(captured['data'], indent=2))
        with open('production/captured_edit_playlist_payload.json', 'w', encoding='utf-8') as f:
            json.dump(captured, f, indent=2)
