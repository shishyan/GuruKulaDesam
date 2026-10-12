from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]
    print("Attached to:", page.title(), page.url)
    
    # Take screenshot of active Flow tab
    page.screenshot(path='production/flow_live_9222.png')
    print("Screenshot saved to production/flow_live_9222.png")
    browser.close()
