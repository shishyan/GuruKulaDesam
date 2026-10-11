import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

vid = "31xVgvxoiUA"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print(f"Navigating to {vid} translations...")
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(3)
    
    edit_btn = page.get_by_text("Edit subtitles")
    print(f"Edit subtitles count: {edit_btn.count()}")
    if edit_btn.count() > 0:
        edit_btn.first.click()
        time.sleep(3)
        
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/shot_editor_open.png")
    
    # Now look for "Edit as text" button
    toggle_btn = page.locator("#toggle-button, text='Edit as text'")
    print(f"Toggle button count: {toggle_btn.count()}")
    if toggle_btn.count() > 0:
        for i in range(toggle_btn.count()):
            b = toggle_btn.nth(i)
            print(f"  b {i}: visible={b.is_visible()}, text='{b.inner_text().strip()}'")
            if b.is_visible():
                print("Clicking Edit as text...")
                b.click()
                time.sleep(2)
                break
                
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/shot_after_edit_as_text.png")
    print("Screenshot saved to shot_after_edit_as_text.png")
