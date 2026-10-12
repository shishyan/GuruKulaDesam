import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print(f"Current page URL: {page.url}", flush=True)
    
    # Find all buttons that have 'Save' or similar
    btn_info = page.evaluate('''() => {
        const elements = Array.from(document.querySelectorAll('button, ytcp-button, [role="button"]'));
        return elements.map(el => ({
            tag: el.tagName,
            id: el.id,
            className: el.className,
            text: (el.innerText || '').trim(),
            ariaLabel: el.getAttribute('aria-label'),
            disabled: el.hasAttribute('disabled') || el.getAttribute('aria-disabled') === 'true'
        })).filter(x => x.text.toLowerCase().includes('save') || (x.ariaLabel && x.ariaLabel.toLowerCase().includes('save')) || (x.id && x.id.toLowerCase().includes('save')));
    }''')
    
    print("Found potential save buttons:", btn_info, flush=True)
    
    # Click using Playwright's locator for text 'Save'
    save_btn = page.locator('button:has-text("Save"), ytcp-button:has-text("Save"), [role="button"]:has-text("Save")').first
    if save_btn.count() > 0:
        print("Clicking save button via locator...", flush=True)
        save_btn.click()
        time.sleep(4)
        print("Clicked save button!", flush=True)
    else:
        print("Locator did not find Save button, trying get_by_role...", flush=True)
        page.get_by_role("button", name="Save").click()
        time.sleep(4)
        print("Clicked via get_by_role!", flush=True)
        
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/after_save_click.png")
    print("Screenshot saved to after_save_click.png", flush=True)
