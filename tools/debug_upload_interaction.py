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
    
    page.on('console', lambda msg: print(f"CONSOLE: [{msg.type}] {msg.text}"))
    page.on('requestfailed', lambda r: print(f"REQ_FAILED: {r.method} {r.url} -> {r.failure}"))
    page.on('response', lambda r: print(f"RESP: {r.status} {r.url[:80]}") if (r.status >= 400 or 'upload' in r.url or 'timedtext' in r.url or 'channel' in r.url) else None)
    
    print("1. Navigating...")
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(3)
    
    print("2. Checking upload button...")
    ub = page.get_by_text("Upload manual")
    print(f"ub count: {ub.count()}")
    if ub.count() > 0:
        ub.first.click()
        print("Clicked upload manual!")
    else:
        print("Upload manual not found!")
    time.sleep(2)
    
    print("3. Checking continue button...")
    cb = page.get_by_role("button", name="Continue")
    print(f"cb count: {cb.count()}")
    if cb.count() > 0:
        with page.expect_file_chooser() as fc_info:
            cb.click()
        fc = fc_info.value
        print(f"4. Setting file: {srt_path}")
        fc.set_files(srt_path)
        print("File set! Waiting 6s...")
        time.sleep(6)
    else:
        print("Continue not found!")
