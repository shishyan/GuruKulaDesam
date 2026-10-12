from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    btn = flow_page.locator("button[aria-label*='Start generation' i], button.generate-icon-button").last
    print("Btn visible:", btn.is_visible())
    box = btn.bounding_box()
    print("Btn box:", box)
    
    if box:
        flow_page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
        print("Clicked mouse at center of button!")
    
    flow_page.wait_for_timeout(3000)
    flow_page.screenshot(path="tools/after_click_test.png")
    print("Saved tools/after_click_test.png")
    browser.close()
