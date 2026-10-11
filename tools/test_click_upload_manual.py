import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print("Page URL:", page.url)
    
    # Click 'Upload manual'
    btn = page.locator('text="Upload manual"')
    print("Upload manual button count:", btn.count())
    if btn.count() > 0:
        btn.first.click()
        print("Clicked 'Upload manual'!")
        time.sleep(2)
        
        # Screenshot modal
        shot1 = "scratch/after_upload_manual_click.png"
        page.screenshot(path=shot1)
        print("Saved screenshot:", shot1)
