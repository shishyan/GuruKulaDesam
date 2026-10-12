from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    settings_btn = flow_page.locator("button.settings-trigger-button").first
    print("Settings btn text:", settings_btn.inner_text().encode('ascii', 'ignore').decode())
    settings_btn.click()
    flow_page.wait_for_timeout(1000)
    flow_page.screenshot(path="tools/settings_menu.png")
    print("Screenshot saved to tools/settings_menu.png")
    browser.close()
