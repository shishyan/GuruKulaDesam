import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
target_url = f"https://studio.youtube.com/video/{vid}/translations"
print(f"Target URL: {target_url}", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print(f"Current page URL: {page.url}", flush=True)
    
    print(f"Navigating to {target_url}...", flush=True)
    page.goto(target_url, wait_until='networkidle')
    time.sleep(3)
    
    print("Taking screenshot...", flush=True)
    os.makedirs("scratch", exist_ok=True)
    page.screenshot(path="scratch/mata_translations_page.png")
    print("Screenshot saved to scratch/mata_translations_page.png")
    
    # Inspect all actionable buttons/links on the page
    elements = page.evaluate("""() => {
        function collect(root) {
            let res = [];
            let elms = Array.from(root.querySelectorAll('*'));
            for (let el of elms) {
                if (el.shadowRoot) res = res.concat(collect(el.shadowRoot));
                let txt = (el.innerText || '').trim();
                let aria = (el.getAttribute('aria-label') || '').trim();
                if ((el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON' || el.tagName === 'A' || el.tagName === 'YTCP-ICON-BUTTON') && (txt || aria)) {
                    let r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) {
                        res.push({
                            tag: el.tagName,
                            id: el.id,
                            text: txt.slice(0, 50),
                            aria: aria.slice(0, 50),
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
    print("Found actionable elements:")
    for el in elements:
        print(f"  [{el['tag']}] id={el['id']} text='{el['text']}' aria='{el['aria']}' at ({el['x']}, {el['y']})")

print("Navigation & inspection complete!")
