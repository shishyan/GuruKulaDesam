import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    vid = "ssOkftpUcLE"
    url = f"https://www.youtube.com/watch?v={vid}"
    print(f"Navigating to {url}...", flush=True)
    page.goto(url, wait_until="domcontentloaded")
    time.sleep(3)
    
    # Click expand description
    desc_info = page.evaluate('''() => {
        const exp = document.querySelector('#expand, ytd-text-inline-expander #expand');
        if (exp) exp.click();
        const descEl = document.querySelector('#description-inline-expander, ytd-text-inline-expander #description');
        return {
            title: document.title,
            desc: descEl ? descEl.innerText : document.body.innerText.slice(0, 1000)
        };
    }''')
    
    print("Page Title:", desc_info['title'], flush=True)
    print("Live YouTube Description Snippet:\n", desc_info['desc'][:500], flush=True)
