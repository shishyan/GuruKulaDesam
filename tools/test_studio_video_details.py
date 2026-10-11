import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    print("Connecting to Chrome on port 9225...", flush=True)
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    vid = "ssOkftpUcLE"
    url = f"https://studio.youtube.com/video/{vid}/edit"
    print(f"Navigating to {url}...", flush=True)
    page.goto(url, wait_until="domcontentloaded")
    time.sleep(5)
    
    print(f"Current page URL: {page.url}", flush=True)
    print(f"Page title: {page.title()}", flush=True)
    
    info = page.evaluate('''() => {
        const titleBox = document.querySelector('#textbox[aria-label*="Title"], ytcp-social-suggestions-textbox[aria-label*="Title"] #textbox, #input[aria-label*="Title"]');
        const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
        const saveBtn = document.querySelector('#save-button, ytcp-button#save-button, [aria-label*="Save"]');
        
        return {
            titleBoxFound: !!titleBox,
            titleText: titleBox ? titleBox.innerText : null,
            descBoxFound: !!descBox,
            descTextSnippet: descBox ? descBox.innerText.slice(0, 150) : null,
            saveBtnFound: !!saveBtn,
            saveBtnDisabled: saveBtn ? saveBtn.getAttribute('disabled') : null
        };
    }''')
    
    print("Form elements info:", info, flush=True)
    
    screenshot_path = "C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/studio_video_details_test.png"
    page.screenshot(path=screenshot_path)
    print(f"Saved screenshot to {screenshot_path}", flush=True)
