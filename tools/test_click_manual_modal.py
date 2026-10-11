import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print('Waiting for page to be ready...')
    page.wait_for_load_state('domcontentloaded')
    time.sleep(3)
    print('Current URL:', page.url)
    
    res = page.evaluate("""() => {
        let ytcp = document.querySelector('#upload-default-language-button');
        if (!ytcp) return { found: false };
        let btn = ytcp.querySelector('button') || ytcp;
        btn.click();
        return { found: true, tag: btn.tagName };
    }""")
    print('Click result:', res)
    time.sleep(2)
    
    page.screenshot(path='scratch/modal_open_test.png')
    
    # Check what modal is open
    modal_text = page.evaluate("""() => {
        let modals = Array.from(document.querySelectorAll('ytcp-dialog, ytcp-modal, *[role="dialog"]'));
        return modals.map(m => m.innerText);
    }""")
    print('Open modals:', modal_text)
