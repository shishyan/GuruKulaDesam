from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]
    
    # 1. Close popup by clicking canvas at x=200, y=200
    page.mouse.click(200, 200)
    page.wait_for_timeout(500)
    
    # 2. Click the sliders/tune button inside the prompt box (to the right of the paper-pencil icon)
    # Let's inspect all buttons inside the bottom prompt bar
    prompt_bar = page.locator('div:has-text("What do you want to create?")').last
    buttons = page.locator('button').all()
    
    # Click the tune/sliders button (typically has SVG with sliders)
    for b in buttons:
        html = b.inner_html()
        if 'tune' in html or 'slider' in html or 'settings' in html or 'M3 17v2h6v-2H3' in html or 'filter' in html:
            if b.is_visible() and b.bounding_box() and b.bounding_box()['y'] > 800:
                print("Clicking prompt box settings button...")
                b.click()
                break
                
    page.wait_for_timeout(1000)
    page.screenshot(path='production/flow_prompt_model_panel.png')
    print("Screenshot saved to production/flow_prompt_model_panel.png")
    browser.close()
