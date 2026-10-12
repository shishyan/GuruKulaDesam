from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9225')
    page = browser.contexts[0].pages[0]
    
    # 1. Click 'Never' radio button (Agent will generate media and spend credits automatically)
    never_radio = page.locator('text="Never"').first
    if never_radio.is_visible():
        never_radio.click()
        print("Selected 'Never' confirmation.")
        
    # 2. Click 'Save' button
    save_btn = page.locator('button:has-text("Save"), [role="button"]:has-text("Save")').first
    if save_btn.is_visible():
        save_btn.click()
        print("Clicked Save on Agent Settings.")
        page.wait_for_timeout(1000)

    # 3. Take screenshot
    page.screenshot(path='production/flow_settings_saved.png')
    print("Screenshot saved to production/flow_settings_saved.png")
    browser.close()
