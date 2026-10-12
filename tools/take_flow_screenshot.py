from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    flow_page.screenshot(path="tools/flow_debug.png", full_page=False)
    print("Screenshot saved to tools/flow_debug.png")
    browser.close()
