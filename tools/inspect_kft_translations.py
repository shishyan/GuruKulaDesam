import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "KFtS403RfbY"
target_url = f"https://studio.youtube.com/video/{vid}/translations"
print(f"Target URL: {target_url}", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print(f"Navigating to {target_url}...", flush=True)
    page.goto(target_url, wait_until='domcontentloaded')
    time.sleep(5)
    
    screenshot_path = "scratch/kft_translations_page.png"
    page.screenshot(path=screenshot_path)
    print(f"Saved screenshot to {screenshot_path}", flush=True)
    
    # Inspect buttons on page
    btns = page.evaluate("""() => {
        function collect(root) {
            let res = [];
            let elms = Array.from(root.querySelectorAll('*'));
            for (let el of elms) {
                if (el.shadowRoot) res = res.concat(collect(el.shadowRoot));
                let txt = (el.innerText || '').trim();
                let aria = (el.getAttribute('aria-label') || '').trim();
                if ((el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON') && (txt || aria)) {
                    let r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) {
                        res.push({
                            tag: el.tagName,
                            id: el.id,
                            text: txt.slice(0, 50),
                            disabled: el.hasAttribute('disabled') || el.getAttribute('aria-disabled') === 'true',
                            x: Math.round(r.x + r.width/2),
                            y: Math.round(r.y + r.height/2)
                        });
                    }
                }
            }
            return res;
        }
        return collect(document.body);
    }""")
    print("Actionable buttons on page:")
    for b in btns:
        if any(w in b['text'].lower() or w in (b['id'] or '').lower() for w in ['upload', 'edit', 'subtitle', 'manual', 'add']):
            print(" ", b)
