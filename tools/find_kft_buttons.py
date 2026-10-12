import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    info = page.evaluate("""() => {
        let elms = Array.from(document.querySelectorAll('*'));
        let res = [];
        for (let el of elms) {
            let t = (el.innerText || '').trim();
            if (t === 'Edit subtitles' || t === 'Upload manual' || t === 'Add language') {
                let r = el.getBoundingClientRect();
                res.push({ tag: el.tagName, id: el.id, text: t, x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height });
            }
        }
        return res;
    }""")
    print("Found buttons:")
    for b in info:
        print(" ", b)
