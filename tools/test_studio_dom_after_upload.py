import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

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
    
    print("Page URL:", page.url, flush=True)
    
    # Check if 'Edit subtitles' or 'Upload manual' exists
    edit_btn = page.get_by_text("Edit subtitles")
    upload_btn = page.get_by_text("Upload manual")
    print(f"Edit subtitles visible: {edit_btn.is_visible() if edit_btn.count() > 0 else False}", flush=True)
    print(f"Upload manual visible: {upload_btn.is_visible() if upload_btn.count() > 0 else False}", flush=True)
    
    if upload_btn.is_visible():
        print("Clicking Upload manual...", flush=True)
        upload_btn.first.click()
        time.sleep(2)
        
        continue_btn = page.get_by_role("button", name="Continue")
        print(f"Continue button visible: {continue_btn.is_visible()}", flush=True)
        
        with page.expect_file_chooser() as fc_info:
            continue_btn.click()
            
        fc = fc_info.value
        print(f"File chooser opened: setting {srt_path}", flush=True)
        fc.set_files(srt_path)
        print("File set! Waiting 8 seconds for Editor to load...", flush=True)
        time.sleep(8)
        
    print("Current URL after upload:", page.url, flush=True)
    
    # Check for Publish button or any action buttons
    publish_btn = page.get_by_role("button", name="Publish")
    print(f"Publish button visible: {publish_btn.is_visible() if publish_btn.count() > 0 else False}", flush=True)
    
    save_btn = page.get_by_role("button", name="Save")
    print(f"Save button visible: {save_btn.is_visible() if save_btn.count() > 0 else False}", flush=True)
    
    buttons = page.locator("button, ytcp-button").all()
    print(f"Total buttons found: {len(buttons)}", flush=True)
    for b in buttons:
        try:
            txt = b.inner_text().strip()
            if txt and len(txt) < 30 and b.is_visible():
                print(f"  Visible Button: '{txt}'", flush=True)
        except Exception:
            pass
            
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/studio_dom_test.png")
    print("Screenshot saved to studio_dom_test.png", flush=True)
