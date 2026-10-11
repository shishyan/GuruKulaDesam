import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

vid = "31xVgvxoiUA"
srt_path = os.path.abspath(f"production/subtitles/{vid}.srt")

print(f"Connecting to port 9225...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print(f"Navigating to video {vid} translations...", flush=True)
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(4)
    
    # Check upload button
    upload_btn = page.get_by_text("Upload manual").first
    print(f"Upload manual visible: {upload_btn.is_visible()}", flush=True)
    upload_btn.click()
    time.sleep(2)
    
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/step1_dialog.png")
    print("Step 1 dialog captured.", flush=True)
    
    # Check "With timing" radio
    radio_timing = page.locator("tp-yt-paper-radio-button, [role='radio']").first
    print(f"Radio timing: visible={radio_timing.is_visible()}", flush=True)
    
    continue_btn = page.get_by_role("button", name="Continue")
    print(f"Continue button visible: {continue_btn.is_visible()}", flush=True)
    
    with page.expect_file_chooser() as fc_info:
        continue_btn.click()
        
    fc = fc_info.value
    print(f"File chooser intercepted: setting {srt_path}", flush=True)
    fc.set_files(srt_path)
    
    # Now monitor the screen every 2 seconds
    for s in range(1, 6):
        time.sleep(2)
        shot_path = f"C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/step2_after_upload_{s*2}s.png"
        page.screenshot(path=shot_path)
        print(f"Captured {shot_path}", flush=True)
        # Check if Publish button exists
        pub = page.locator("#publish-button, [aria-label='Publish'], button:has-text('Publish')")
        print(f"  [{s*2}s] Publish button count: {pub.count()}", flush=True)
        for i in range(pub.count()):
            try:
                print(f"    pub {i}: visible={pub.nth(i).is_visible()}, text='{pub.nth(i).inner_text().strip()}'", flush=True)
            except Exception: pass
