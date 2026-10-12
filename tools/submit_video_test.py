from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    # 1. Close settings popup if open by pressing Escape or clicking outside
    flow_page.keyboard.press("Escape")
    flow_page.wait_for_timeout(500)
    
    # 2. Click generate button
    gen_btn = flow_page.locator("button.generate-icon-button, button[aria-label*='Start generation' i]").last
    print("Generate button visible:", gen_btn.is_visible())
    gen_btn.click(force=True)
    print("Clicked Start generation!")
    flow_page.wait_for_timeout(3000)
    
    body_text = flow_page.locator("body").inner_text()
    print("Has Stop now:", "Stop" in body_text)
    flow_page.screenshot(path="tools/after_submit_video.png")
    browser.close()
