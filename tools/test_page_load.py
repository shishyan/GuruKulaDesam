import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "3t5U9ABVeOc"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print(f"Navigating to video {vid} translations...")
    page.goto(f"https://studio.youtube.com/video/{vid}/translations")
    
    print("Waiting for selector #upload-default-language-button or #m2-editor-button...")
    try:
        page.wait_for_selector("#upload-default-language-button, #m2-editor-button, text='Languages'", timeout=15000)
        print("Page loaded successfully!")
    except Exception as e:
        print("Timeout waiting for selector:", e)
        
    time.sleep(2)
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/v2_loaded.png")
    print("Screenshot saved to v2_loaded.png")
