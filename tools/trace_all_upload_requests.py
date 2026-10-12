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
    
    events = []
    
    def log_req(r):
        events.append(f"REQ: {r.method} {r.url}")
    def log_resp(r):
        events.append(f"RESP: {r.status} {r.url}")
    def log_fail(r):
        events.append(f"FAIL: {r.method} {r.url} -> {r.failure}")
        
    page.on('request', log_req)
    page.on('response', log_resp)
    page.on('requestfailed', log_fail)
    
    print("Navigating to translations...")
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(3)
    
    events.clear() # clear navigation events
    print("Clicking upload manual...")
    ub = page.get_by_text("Upload manual").first
    ub.click()
    time.sleep(2)
    
    cb = page.get_by_role("button", name="Continue")
    with page.expect_file_chooser() as fc_info:
        cb.click()
    fc = fc_info.value
    print(f"Setting file {srt_path}...")
    fc.set_files(srt_path)
    time.sleep(5)
    
    print(f"\n--- Total events during file upload: {len(events)} ---")
    for e in events:
        print(" ", e)
