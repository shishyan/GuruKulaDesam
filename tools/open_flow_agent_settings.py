from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]
    
    # 1. Close the View mode popup by clicking somewhere neutral or Escape
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    
    # 2. Click the gear/settings icon next to help in top header (button with 'settings')
    # Or click the sliders icon inside the prompt box
    prompt_settings = page.locator('button:has-text("tune"), [aria-label*="tune" i], button:has-text("tune_2")').first
    if not prompt_settings.is_visible():
        # Look for the sliders button in the prompt box
        prompt_settings = page.locator('.prompt-box button, [role="region"] button').filter(has_text="tune").first
        
    # The top header settings icon:
    header_settings = page.locator('button[aria-label="Settings"], button:has-text("settings")').first
    if header_settings.is_visible():
        header_settings.click()
        print("Clicked header Settings icon.")
        page.wait_for_timeout(1000)
        
    page.screenshot(path='production/flow_agent_settings_panel.png')
    print("Screenshot saved to production/flow_agent_settings_panel.png")
    browser.close()
