import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    for ci, ctx in enumerate(browser.contexts):
        print(f"Context {ci}: {len(ctx.pages)} pages")
        for pi, pg in enumerate(ctx.pages):
            print(f"  Page {pi}: {pg.url} - {pg.title()}")
