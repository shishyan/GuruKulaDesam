import json, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print('Current URL:', page.url)
    info = page.evaluate("""() => {
        let elms = Array.from(document.querySelectorAll('*'));
        let res = [];
        for (let el of elms) {
            let t = (el.innerText || '').trim();
            if (t.includes('Upload a file') || t.includes('With timing') || t.includes('Continue') || t.includes('Select subtitle file')) {
                res.push({ tag: el.tagName, id: el.id, text: t.slice(0, 100) });
            }
        }
        return res;
    }""")
    print('Matching modal elements:', len(info))
    for item in info[:10]:
        print(" ", item)
