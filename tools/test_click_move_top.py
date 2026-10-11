import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    def on_req(req):
        if 'edit_playlist' in req.url:
            print('CAPTURED EDIT_PLAYLIST REQ:', req.url, flush=True)
            print('POST DATA:', req.post_data, flush=True)
            
    def on_resp(resp):
        if 'edit_playlist' in resp.url:
            print(f'EDIT_PLAYLIST RESP {resp.status}', flush=True)
            print('RESP TEXT:', resp.text()[:200], flush=True)
            
    page.on('request', on_req)
    page.on('response', on_resp)
    
    # Click 3-dot menu on row 1 (the second video)
    rows = page.locator('ytd-playlist-video-renderer')
    row = rows.nth(1)
    title = row.locator('#video-title').inner_text().strip()
    print(f'Opening menu on row 1: {title[:35]}...', flush=True)
    
    menu_btn = row.locator('ytd-menu-renderer yt-icon-button#button')
    menu_btn.click()
    time.sleep(1)
    
    # Click "Move to top"
    move_top = page.locator('ytd-menu-service-item-renderer:has-text("Move to top")')
    print('Move to top button visible:', move_top.is_visible(), flush=True)
    move_top.click()
    
    time.sleep(4)
    print('Finished click test!', flush=True)
