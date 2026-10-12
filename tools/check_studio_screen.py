import sys
import base64
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    cdp = ctx.new_cdp_session(page)
    
    shot = cdp.send('Page.captureScreenshot', {'format': 'png', 'fromSurface': False})
    out_file = 'C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/shot_current_surface.png'
    with open(out_file, 'wb') as f:
        f.write(base64.b64decode(shot['data']))
    print(f"Screenshot saved to {out_file}")
    
    # Check what is currently visible on page
    txt = page.evaluate("() => document.body.innerText")
    print(f"Page body text:\n{txt[:400]}")
