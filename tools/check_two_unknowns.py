import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    for vid in ['qPjurMK6xpI', 'fq0nJxj5aU4']:
        print(f"Navigating to https://www.youtube.com/watch?v={vid} ...", flush=True)
        page.goto(f"https://www.youtube.com/watch?v={vid}", wait_until="domcontentloaded")
        time.sleep(2)
        print("Page title:", page.title(), flush=True)
        print("URL:", page.url, flush=True)
