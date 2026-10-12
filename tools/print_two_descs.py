import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    for vid in ['qPjurMK6xpI', 'fq0nJxj5aU4']:
        page.goto(f"https://www.youtube.com/watch?v={vid}", wait_until="domcontentloaded")
        time.sleep(2)
        desc = page.evaluate('''() => {
            const exp = document.querySelector('#expand, ytd-text-inline-expander #expand');
            if (exp) exp.click();
            const el = document.querySelector('#description-inline-expander, ytd-text-inline-expander #description');
            return el ? el.innerText : '';
        }''')
        print(f"=== {vid} ({page.title()}) ===", flush=True)
        print(desc[:300], flush=True)
        print("="*60, flush=True)
