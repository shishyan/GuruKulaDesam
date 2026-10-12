from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    flow_page = next((page for page in ctx.pages if 'flow.google.com/project' in page.url), None)
    
    # 1. Click Video button in settings popup
    video_btn = flow_page.locator("button:has-text('Video')").first
    if video_btn.is_visible():
        video_btn.click()
        print("Clicked Video toggle!")
        flow_page.wait_for_timeout(1000)
    else:
        # Open settings first if not visible
        settings_btn = flow_page.locator("button.settings-trigger-button").first
        settings_btn.click()
        flow_page.wait_for_timeout(500)
        video_btn = flow_page.locator("button:has-text('Video')").first
        video_btn.click()
        print("Opened settings and clicked Video toggle!")
        flow_page.wait_for_timeout(1000)
        
    flow_page.screenshot(path="tools/after_video_toggle.png")
    browser.close()
