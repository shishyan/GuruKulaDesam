from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9225')
    page = [pg for pg in browser.contexts[0].pages if 'flow.google' in pg.url][0]
    print('Flow Page URL:', page.url)
    
    # Check text around user avatar
    avatar = page.locator('button[aria-label*="Google Account" i], button[aria-label*="Account details" i]').first
    if avatar.is_visible():
        print('Avatar label:\n', avatar.get_attribute('aria-label'))
    
    # Check model / tune options
    tune = page.locator('button:has-text("tune"), button[aria-label*="tune" i]').first
    if tune.is_visible():
        print('Clicking tune button...')
        tune.click()
        page.wait_for_timeout(1000)
        # Capture dialog content
        dialog = page.locator('[role="dialog"], [role="menu"], mat-dialog-container, .cdk-overlay-pane').all()
        print('Found dialogs:', len(dialog))
        for d in dialog:
            if d.is_visible():
                print('Dialog text:\n', d.inner_text())

    browser.close()
