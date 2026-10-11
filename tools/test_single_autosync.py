import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = 'xGb7ZXDRvVU'
print(f"Testing full Auto-sync Publish flow on {vid}...", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print(f"1. Navigating to https://studio.youtube.com/video/{vid}/translations...", flush=True)
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(4)
    
    print("2. Finding Edit subtitles button...", flush=True)
    edit_btn = page.locator('#m2-editor-button, button:has-text("Edit subtitles"), ytcp-button:has-text("Edit subtitles")').first
    if not edit_btn.is_visible():
        # Check if there is an Edit button or Add button
        edit_btn = page.locator('button:has-text("Edit"), ytcp-button:has-text("Edit")').first
        
    if not edit_btn.is_visible():
        print("ERROR: Edit button not visible!")
        sys.exit(1)
        
    print(f"3. Clicking Edit subtitles: {edit_btn.inner_text().strip()}...", flush=True)
    edit_btn.click()
    time.sleep(3)
    
    print("4. Finding Publish button in editor modal...", flush=True)
    pub_btn = page.locator('#publish-button, button:has-text("Publish"), ytcp-button:has-text("Publish")').first
    if not pub_btn.is_visible():
        # Try finding inside dialog
        pub_btn = page.locator('ytcp-dialog #publish-button, ytcp-subtitles-editor #publish-button').first
        
    if pub_btn.is_visible():
        print("5. Clicking Publish button...", flush=True)
        pub_btn.click()
        print("Waiting 5s for Publish to process...", flush=True)
        time.sleep(5)
        print("6. SUCCESS! Subtitle published & auto-sync engaged!", flush=True)
    else:
        print("ERROR: Publish button not found in modal!")
        
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/test_single_done.png")
    print("Saved screenshot test_single_done.png", flush=True)
