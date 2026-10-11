import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print('Testing clicking Edit subtitles or Upload manual...')
    # Let's find any element containing 'Edit subtitles' or 'Upload manual'
    for phrase in ['Edit subtitles', 'Upload manual', 'Add language']:
        el = page.locator(f':text("{phrase}")').first
        if el.count() > 0 and el.is_visible():
            print(f'Clicking: {phrase}...')
            el.click()
            time.sleep(3)
            print('New URL:', page.url)
            page.screenshot(path=f'C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/after_click_{phrase.replace(" ", "_")}.png')
            break
        else:
            print(f'{phrase}: not visible directly')
