import sys, time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print('Clicking Publish button (#publish-button)...')
    pub = page.locator('#publish-button').first
    if pub.is_visible():
        pub.click()
        print('Clicked Publish! Waiting 4s...')
        time.sleep(4)
    else:
        print('Publish button not visible!')
        
    page.screenshot(path='C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/test_after_publish.png')
    print('Screenshot saved!')
