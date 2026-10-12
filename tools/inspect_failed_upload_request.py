import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

vid = "31xVgvxoiUA"
srt_path = os.path.abspath(f"production/subtitles/{vid}.srt")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    failed_requests = []
    all_responses = []
    
    def on_response(response):
        if response.status >= 400 or 'caption' in response.url.lower() or 'upload' in response.url.lower() or 'timedtext' in response.url.lower():
            try:
                body = response.text()[:500]
            except Exception:
                body = "<binary or inaccessible>"
            all_responses.append({
                'url': response.url,
                'status': response.status,
                'body': body
            })
            
    page.on('response', on_response)
    
    print(f"Navigating to video {vid} translations...")
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(3)
    
    upload_btn = page.get_by_text("Upload manual").first
    upload_btn.click()
    time.sleep(2)
    
    continue_btn = page.get_by_role("button", name="Continue")
    with page.expect_file_chooser() as fc_info:
        continue_btn.click()
        
    fc = fc_info.value
    fc.set_files(srt_path)
    time.sleep(5)
    
    print(f"\n--- Captured {len(all_responses)} relevant responses ---")
    for r in all_responses:
        print(f"Status {r['status']}: {r['url']}")
        print(f"  Body: {r['body']}\n")
