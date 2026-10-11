import sys
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
print("Step 1: Importing Playwright...", flush=True)
from playwright.sync_api import sync_playwright

print("Step 2: Entering sync_playwright...", flush=True)
with sync_playwright() as p:
    print("Step 3: Connecting over CDP...", flush=True)
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225', timeout=5000)
    print("Step 4: Connected! Contexts:", len(browser.contexts), flush=True)
    pages = browser.contexts[0].pages
    print(f"Step 5: Pages found: {len(pages)}", flush=True)
    for idx, pg in enumerate(pages):
        print(f"   [{idx}] {pg.url}", flush=True)
print("Done!", flush=True)
