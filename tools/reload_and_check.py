import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print('Navigating page...')
    page.goto('https://studio.youtube.com/video/Mata6vtnrjQ/translations')
    time.sleep(5)
    page.screenshot(path='scratch/after_reload.png')
    btn_info = page.evaluate("""() => {
        let b = document.querySelector('#upload-default-language-button');
        if (!b) return null;
        return {
            disabled: b.hasAttribute('disabled'),
            aria_disabled: b.getAttribute('aria-disabled'),
            text: b.innerText,
            classes: b.className
        };
    }""")
    print('Button info after reload:', btn_info)
