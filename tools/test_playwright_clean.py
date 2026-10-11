import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        print(f"Page title: {page.title()}, URL: {page.url}", flush=True)
        
        # Let's inspect the exact DOM of that Save button
        save_btn_html = page.evaluate('''() => {
            // Find any element containing text 'Save'
            const allElements = Array.from(document.querySelectorAll('*'));
            const matches = allElements.filter(el => {
                const text = el.innerText ? el.innerText.trim() : '';
                return text === 'Save' && el.children.length === 0;
            });
            return matches.map(m => {
                let current = m;
                const hierarchy = [];
                for (let i = 0; i < 4 && current; i++) {
                    hierarchy.push({
                        tag: current.tagName,
                        id: current.id,
                        classes: current.className,
                        role: current.getAttribute('role'),
                        disabled: current.hasAttribute('disabled') || current.getAttribute('aria-disabled') === 'true'
                    });
                    current = current.parentElement;
                }
                return hierarchy;
            });
        }''')
        print("Save button hierarchy:", save_btn_html, flush=True)
    finally:
        browser.close()
