import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        print(f"Connected. Title: {page.title()}, URL: {page.url}")
        
        info = page.evaluate('''() => {
            function findButtons(root) {
                let results = [];
                const all = root.querySelectorAll('*');
                for (const el of all) {
                    const text = (el.innerText || '').trim();
                    const aria = (el.getAttribute('aria-label') || '').trim();
                    const id = el.id || '';
                    if (text === 'Save' || aria.toLowerCase().includes('save') || id.toLowerCase().includes('save')) {
                        results.push({
                            tag: el.tagName,
                            id: el.id,
                            className: el.className,
                            text: text.slice(0, 30),
                            ariaLabel: aria,
                            hasShadow: !!el.shadowRoot,
                            disabled: el.hasAttribute('disabled') || el.getAttribute('aria-disabled') === 'true'
                        });
                    }
                    if (el.shadowRoot) {
                        results = results.concat(findButtons(el.shadowRoot));
                    }
                }
                return results;
            }
            return findButtons(document);
        }''')
        print(f"Found {len(info)} elements matching 'save':")
        for x in info:
            print(" ", x)
    finally:
        browser.close()
