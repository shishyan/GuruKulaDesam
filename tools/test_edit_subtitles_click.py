import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print('Current page:', page.url)
    
    # Locate Edit subtitles
    edit_btn = page.locator("#m2-editor-button, ytcp-button:has-text('Edit subtitles'), button:has-text('Edit subtitles')").first
    print("Edit button count:", edit_btn.count())
    if edit_btn.count() > 0:
        print("Clicking 'Edit subtitles'...")
        edit_btn.click()
        time.sleep(4)
        
        page.screenshot(path='scratch/after_edit_subtitles_click.png')
        print("Saved scratch/after_edit_subtitles_click.png")
        print("New URL:", page.url)
