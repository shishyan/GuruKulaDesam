from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]
    
    # 1. Click Save button in Agent settings panel
    save_btn = page.locator('button:has-text("Save"), [role="button"]:has-text("Save")').first
    if save_btn.is_visible():
        save_btn.click()
        print("Clicked Save on Agent Settings.")
        page.wait_for_timeout(1000)
    else:
        page.keyboard.press("Escape")
        
    page.screenshot(path='production/flow_ready_to_prompt.png')
    print("Screenshot saved to production/flow_ready_to_prompt.png")
    browser.close()
