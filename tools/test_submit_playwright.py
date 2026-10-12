from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    # 1. Click directly on ProseMirror to focus
    pm = flow_page.locator("div.ProseMirror").first
    pm.click()
    flow_page.wait_for_timeout(300)
    
    # 2. Press Enter
    flow_page.keyboard.press("Enter")
    print("Pressed Enter in ProseMirror")
    flow_page.wait_for_timeout(3000)
    
    body_text = flow_page.locator("body").inner_text()
    print("Has Stop:", "Stop" in body_text)
    
    # If not started, try locating the exact generate button and click via Playwright
    if "Stop" not in body_text:
        gen_btn = flow_page.locator("button.generate-icon-button").last
        if gen_btn.is_visible():
            print("Clicking generate-icon-button via Playwright...")
            gen_btn.click()
            flow_page.wait_for_timeout(3000)
            body_text = flow_page.locator("body").inner_text()
            print("After btn click, has Stop:", "Stop" in body_text)
            
    browser.close()
