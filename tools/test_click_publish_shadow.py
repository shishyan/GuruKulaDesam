import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Check with get_by_role and get_by_text
    btn_role = page.get_by_role("button", name="Publish")
    print(f"get_by_role count: {btn_role.count()}")
    if btn_role.count() > 0:
        print(f"Role button visible: {btn_role.first.is_visible()}")
        print("Clicking via get_by_role...")
        btn_role.first.click()
        time.sleep(5)
    else:
        btn_text = page.get_by_text("Publish")
        print(f"get_by_text count: {btn_text.count()}")
        if btn_text.count() > 0:
            print("Clicking via get_by_text...")
            btn_text.first.click()
            time.sleep(5)
            
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/publish_click_result.png")
    print("Screenshot saved to publish_click_result.png")
