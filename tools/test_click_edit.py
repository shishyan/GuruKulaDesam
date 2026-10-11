import sys, time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print('Clicking Edit subtitles (#m2-editor-button)...')
    btn = page.locator('#m2-editor-button').first
    btn.click()
    time.sleep(3)
    
    # Take screenshot of what opened
    page.screenshot(path='C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/test_editor_click.png')
    print('Screenshot saved!')
    
    # List visible buttons in modal
    btns = page.locator('button, ytcp-button').all()
    print('Total buttons:', len(btns))
    for b in btns:
        try:
            if b.is_visible():
                txt = b.inner_text().strip()
                bid = b.get_attribute('id') or ''
                if any(k in txt for k in ['Edit', 'Publish', 'Save', 'Done', 'timing', 'text', 'Auto']):
                    print(f'  Button: txt="{txt}" | id="{bid}"')
        except:
            pass
