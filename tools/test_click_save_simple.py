import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        print(f"Page title: {page.title()}, URL: {page.url}", flush=True)
        
        save_res = page.evaluate('''() => {
            const candidates = Array.from(document.querySelectorAll('ytcp-button, button, div[role="button"], [role="button"]'));
            const saveBtn = candidates.find(el => el.innerText && el.innerText.trim() === 'Save');
            if (saveBtn) {
                saveBtn.click();
                return { clicked: true, tag: saveBtn.tagName, id: saveBtn.id, class: saveBtn.className };
            }
            return { clicked: false, candidates: candidates.map(c => c.innerText.trim()).filter(Boolean) };
        }''')
        print("Save click result:", save_res, flush=True)
        time.sleep(3)
        page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/after_save_click_simple.png")
        print("Screenshot saved to after_save_click_simple.png", flush=True)
    finally:
        browser.close()
