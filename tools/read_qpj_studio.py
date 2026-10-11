import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        page.goto("https://studio.youtube.com/video/qPjurMK6xpI/edit", wait_until="domcontentloaded")
        import time; time.sleep(4)
        desc_elem = page.locator('#description-textarea #textbox').first
        desc = desc_elem.inner_text()
        print("Length:", len(desc))
        print("Has முதாகராத்த:", "முதாகராத்த" in desc)
        print("Has நிதாந்த:", "நிதாந்த" in desc)
        print("Desc:\n", desc)
    finally:
        browser.close()
