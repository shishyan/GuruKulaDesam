import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "KFtS403RfbY"
srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
print(f"Target SRT: {srt_file}", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print("Navigating to translations page...", flush=True)
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until='networkidle')
    time.sleep(4)
    print("Page URL:", page.url, flush=True)
    print("Page Title:", page.title(), flush=True)
    
    screenshot1 = f"scratch/{vid}_translations_ready.png"
    page.screenshot(path=screenshot1)
    print(f"Saved {screenshot1}", flush=True)
    
    # 1. Click Upload manual
    print("Looking for Upload manual button...", flush=True)
    upload_btn = page.locator("#upload-default-language-button, ytcp-button:has-text('Upload manual')").first
    print("Upload button found, clicking...", flush=True)
    upload_btn.click()
    time.sleep(2)
    
    # 2. Intercept file chooser on Continue click
    print("Setting up file chooser expectation...", flush=True)
    with page.expect_file_chooser(timeout=10000) as fc_info:
        continue_btn = page.locator("ytcp-button:has-text('Continue'), button:has-text('Continue')").first
        continue_btn.click()
        
    fc = fc_info.value
    print("File chooser caught! Uploading SRT file...", flush=True)
    fc.set_files(srt_file)
    print("SRT file set! Waiting 8s for editor to load...", flush=True)
    time.sleep(8)
    
    screenshot2 = f"scratch/{vid}_in_editor.png"
    page.screenshot(path=screenshot2)
    print(f"Saved {screenshot2}", flush=True)
    
    # 3. Click Publish
    print("Looking for Publish button in editor...", flush=True)
    publish_btn = page.locator("#publish-button, ytcp-button:has-text('Publish'), button:has-text('Publish')").first
    publish_btn.click()
    print("Clicked Publish! Waiting 6s...", flush=True)
    time.sleep(6)
    
    screenshot3 = f"scratch/{vid}_published.png"
    page.screenshot(path=screenshot3)
    print(f"Saved {screenshot3}", flush=True)
    print("SUCCESS: Subtitles uploaded and published live!", flush=True)
