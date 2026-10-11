import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "3t5U9ABVeOc"
srt_path = os.path.abspath(f"production/subtitles/{vid}.srt")

print(f"Testing video {vid}...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print(f"Navigating to https://studio.youtube.com/video/{vid}/translations...", flush=True)
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(3)
    
    # Take screenshot of translations page
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/v2_translations.png")
    
    ub = page.get_by_text("Upload manual").first
    print(f"Upload manual visible: {ub.is_visible()}", flush=True)
    if ub.is_visible():
        ub.click()
        time.sleep(2)
        
        cb = page.get_by_role("button", name="Continue")
        print(f"Continue button visible: {cb.is_visible()}", flush=True)
        with page.expect_file_chooser() as fc_info:
            cb.click()
            
        fc = fc_info.value
        print(f"Setting {srt_path}...", flush=True)
        fc.set_files(srt_path)
        time.sleep(4)
        
        page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/v2_after_set_file.png")
        print("Screenshot v2_after_set_file.png saved.", flush=True)
