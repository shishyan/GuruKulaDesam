import time, sys, pathlib, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
srt_file = os.path.abspath("production/subtitles/Mata6vtnrjQ.srt")
print(f"Target SRT file: {srt_file}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print("Finding 'Upload manual' button...", flush=True)
    # Search for button with text "Upload manual"
    btn = page.locator("text='Upload manual'").first
    if not btn.is_visible():
        btn = page.locator("button:has-text('Upload manual')").first
        
    print(f"Button visible: {btn.is_visible()}", flush=True)
    btn.click()
    time.sleep(2)
    
    screenshot_1 = "scratch/studio_after_upload_click.png"
    page.screenshot(path=screenshot_1)
    print(f"Saved screenshot: {screenshot_1}", flush=True)
    
    # Inspect modal buttons
    modal_texts = page.evaluate("""() => {
        let elms = Array.from(document.querySelectorAll('ytcp-button, button, paper-radio-button, [role="radio"]'));
        return elms.map(e => ({
            tag: e.tagName,
            text: (e.innerText || '').trim(),
            visible: e.offsetParent !== null
        })).filter(x => x.text.length > 0);
    }""")
    print("Modal options found:")
    for m in modal_texts:
        print(" ", m)
