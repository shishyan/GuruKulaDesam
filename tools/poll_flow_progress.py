import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9225')
    page = browser.contexts[0].pages[0]
    
    for i in range(12): # check for 1 minute
        time.sleep(5)
        # Check text in chat
        chat_text = page.locator('body').inner_text()
        stop_btn = page.locator('button:has-text("Stop"), [role="button"]:has-text("Stop")').first
        is_generating = stop_btn.is_visible()
        
        # Check if video appeared
        videos = page.locator('video').all()
        print(f"[{i*5}s] Generating: {is_generating} | Videos rendered: {len(videos)}")
        
        if not is_generating and len(videos) > 0:
            print("Video generation completed!")
            break
            
    page.screenshot(path='production/flow_generation_check.png')
    browser.close()
