import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

targets = ["udRsA-oWxS0", "qPjurMK6xpI", "mPypwIgdo-E", "g42Pg2sg_gg", "rRoJfeRQiaM", "FGeahfpAbiw"]

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        for vid in targets:
            url = f"https://studio.youtube.com/video/{vid}/edit"
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(4)
            desc_elem = page.locator('#description-textarea #textbox').first
            desc = desc_elem.inner_text()
            print(f"\n=================== {vid} (len={len(desc)}) ===================")
            # Find the lyrics section in desc
            if "பாடல் வரிகள்" in desc:
                idx = desc.find("பாடல் வரிகள்")
                print(desc[idx:idx+350])
            else:
                print(desc[:350])
    finally:
        browser.close()
