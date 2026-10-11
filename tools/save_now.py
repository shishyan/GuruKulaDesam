import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    res = page.evaluate("""() => {
        let s = document.querySelector('#save, [id="save"], ytcp-button#save');
        if (s) {
            let r = s.getBoundingClientRect();
            s.click();
            return { found: true, id: s.id, x: r.x + r.width/2, y: r.y + r.height/2 };
        }
        return { found: false };
    }""")
    print("Click #save:", res)
    time.sleep(5)
    page.screenshot(path="scratch/studio_saved_verified.png")
    print("Saved scratch/studio_saved_verified.png")
