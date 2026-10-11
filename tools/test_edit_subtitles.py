import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print("Clicking Edit subtitles...")
    edit_btn = page.get_by_text("Edit subtitles").first
    edit_btn.click()
    time.sleep(5)
    
    print("Current URL:", page.url)
    print("Page title:", page.title())
    
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/edit_subtitles_shot.png")
    print("Screenshot saved to edit_subtitles_shot.png")
