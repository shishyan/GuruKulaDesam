import os
import time
from playwright.sync_api import sync_playwright

vid = "31xVgvxoiUA"
srt_path = os.path.abspath(f"production/subtitles/{vid}.srt")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    requests_made = []
    responses_received = []
    
    page.on('request', lambda r: requests_made.append(f"{r.method} {r.url}"))
    page.on('response', lambda r: responses_received.append(f"{r.status} {r.url}"))
    page.on('console', lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    page.on('pageerror', lambda err: print(f"PAGE ERROR: {err}"))
    
    print(f"Navigating to video {vid} translations...")
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(3)
    
    upload_btn = page.get_by_text("Upload manual").first
    print(f"Clicking Upload manual...")
    upload_btn.click()
    time.sleep(2)
    
    continue_btn = page.get_by_role("button", name="Continue")
    print(f"Clicking Continue with file chooser...")
    with page.expect_file_chooser() as fc_info:
        continue_btn.click()
        
    fc = fc_info.value
    print(f"File chooser opened: is_multiple={fc.is_multiple()}")
    fc.set_files(srt_path)
    print("Set files called! Waiting 8 seconds...")
    time.sleep(8)
    
    print(f"Total requests during upload: {len(requests_made)}")
    for r in requests_made[-10:]:
        print("  Req:", r)
    for r in responses_received[-10:]:
        print("  Res:", r)
        
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/trace_screenshot.png")
