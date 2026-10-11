import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print("Finding publish button...")
    publish_btn = page.locator("#publish-button button, ytcp-button#publish-button, button:has-text('Publish')")
    
    print(f"Publish button count: {publish_btn.count()}")
    for i in range(publish_btn.count()):
        b = publish_btn.nth(i)
        print(f"  btn {i}: visible={b.is_visible()}, text='{b.inner_text().strip()}'")
        if b.is_visible():
            print(f"Clicking Publish button {i}...")
            b.click()
            time.sleep(5)
            break
            
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/after_publish_shot.png")
    print("Screenshot saved to after_publish_shot.png")
