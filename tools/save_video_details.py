import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

print("Starting Playwright...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print(f"Page URL: {page.url}", flush=True)
    
    # Click Save button
    print("Clicking Save button in header...", flush=True)
    res = page.evaluate("""() => {
        let btn = document.querySelector('#save, [id="save"], ytcp-button#save');
        if (btn) {
            let r = btn.getBoundingClientRect();
            btn.click();
            return { clicked: true, x: r.x + r.width/2, y: r.y + r.height/2, disabled: btn.hasAttribute('disabled') };
        }
        return { clicked: false };
    }""")
    print(f"Save click result: {res}", flush=True)
    
    if not res.get('clicked'):
        print("Fallback click coordinate (662, 104)...", flush=True)
        page.mouse.click(662, 104)
        
    print("Waiting 5s for save response...", flush=True)
    time.sleep(5)
    
    ss_path = "scratch/studio_save_confirmed.png"
    page.screenshot(path=ss_path)
    print(f"Saved confirmation to {ss_path}", flush=True)
    
    # Check if Save button is now disabled (means saved!)
    btn_status = page.evaluate("""() => {
        let btn = document.querySelector('#save, [id="save"], ytcp-button#save');
        return btn ? { disabled: btn.hasAttribute('disabled') || btn.getAttribute('aria-disabled') === 'true' } : null;
    }""")
    print(f"Post-save button status: {btn_status}", flush=True)
    browser.close()

print("Done!", flush=True)
