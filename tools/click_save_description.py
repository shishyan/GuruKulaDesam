import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print("Finding enabled 'Save' button...", flush=True)
    clicked = page.evaluate("""() => {
        let elms = Array.from(document.querySelectorAll('*'));
        for (let el of elms) {
            let t = (el.innerText || '').trim();
            if (t === 'Save' && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                let r = el.getBoundingClientRect();
                if (r.width > 0 && r.height > 0 && !el.hasAttribute('disabled')) {
                    el.click();
                    return { clicked: true, x: r.x + r.width/2, y: r.y + r.height/2 };
                }
            }
        }
        return { clicked: false };
    }""")
    print("Evaluate click result:", clicked, flush=True)
    
    if not clicked.get('clicked'):
        # Click by coordinates from screenshot
        print("Clicking via coordinate (662, 104)...", flush=True)
        page.mouse.click(662, 104)
        
    print("Waiting 5s for save to complete...", flush=True)
    time.sleep(5)
    
    ss_path = "scratch/studio_after_final_save_mata6vtnrjq.png"
    page.screenshot(path=ss_path)
    print(f"Saved confirmation to {ss_path}", flush=True)
