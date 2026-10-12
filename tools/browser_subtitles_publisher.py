"""
Reusable YouTube Studio Subtitle Publisher via Chrome Port 9225.
Navigates to https://studio.youtube.com/video/{vid}/translations,
uploads the verified acoustic SRT, and publishes it live.
"""

import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

def publish_subtitles_for_video(vid):
    srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
    print(f"\n==========================================", flush=True)
    print(f"Publishing subtitles for {vid}", flush=True)
    print(f"SRT file: {srt_file}", flush=True)
    assert os.path.exists(srt_file), f"SRT file not found: {srt_file}"
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
        context = browser.contexts[0]
        # Find studio page or open new
        pages = context.pages
        page = pages[0] if pages else context.new_page()
        
        target_url = f"https://studio.youtube.com/video/{vid}/translations"
        print(f"Navigating to {target_url}...", flush=True)
        page.goto(target_url, wait_until='networkidle')
        time.sleep(5)
        print("Page URL:", page.url, flush=True)
        print("Page Title:", page.title(), flush=True)
        
        os.makedirs("scratch", exist_ok=True)
        screenshot1 = f"scratch/{vid}_translations_page.png"
        page.screenshot(path=screenshot1)
        print(f"Saved {screenshot1}", flush=True)
        
        # Check if there is already an Edit button or Upload manual button
        # Look for 'Upload manual' button first
        upload_btn = page.locator("#upload-default-language-button, ytcp-button:has-text('Upload manual')").first
        if upload_btn.is_visible(timeout=5000):
            print("Found 'Upload manual' button! Clicking...", flush=True)
            upload_btn.click()
            time.sleep(2)
            
            print("Intercepting file chooser on Continue...", flush=True)
            with page.expect_file_chooser(timeout=10000) as fc_info:
                continue_btn = page.locator("ytcp-button:has-text('Continue'), button:has-text('Continue')").first
                continue_btn.click()
            fc = fc_info.value
            print(f"File chooser active! Setting SRT: {srt_file}", flush=True)
            fc.set_files(srt_file)
            print("SRT file set! Waiting 8s for Subtitle Editor...", flush=True)
            time.sleep(8)
        else:
            print("'Upload manual' not visible directly. Checking for existing draft/published track Edit button...", flush=True)
            edit_btn = page.locator("#m2-editor-button, ytcp-button:has-text('Edit'), button:has-text('Edit')").first
            if edit_btn.is_visible(timeout=5000):
                print("Found Edit button! Clicking to open editor...", flush=True)
                edit_btn.click()
                time.sleep(5)
                # In editor, click Options menu -> Upload file
                print("Looking for Options (3 dots) in Subtitle Editor...", flush=True)
                options_btn = page.locator("#overflow-menu-button, ytcp-icon-button[aria-label*='Options'], button[aria-label*='Options']").first
                if options_btn.is_visible(timeout=5000):
                    options_btn.click()
                    time.sleep(2)
                    upload_menu = page.locator("ytcp-text-menu-item:has-text('Upload file'), tp-yt-paper-item:has-text('Upload file')").first
                    upload_menu.click()
                    time.sleep(2)
                    with page.expect_file_chooser(timeout=10000) as fc_info:
                        cont_btn = page.locator("ytcp-button:has-text('Continue'), button:has-text('Continue')").first
                        cont_btn.click()
                    fc = fc_info.value
                    fc.set_files(srt_file)
                    time.sleep(6)
            else:
                print("Warning: Neither Upload manual nor Edit button immediately found. Taking screenshot...", flush=True)
                page.screenshot(path=f"scratch/{vid}_debug_state.png")
        
        screenshot2 = f"scratch/{vid}_in_editor.png"
        page.screenshot(path=screenshot2)
        print(f"Saved {screenshot2}", flush=True)
        
        # Click Publish button
        print("Looking for Publish button...", flush=True)
        publish_btn = page.locator("#publish-button, ytcp-button:has-text('Publish'), button:has-text('Publish')").first
        if publish_btn.is_visible(timeout=7000):
            print("Publish button visible! Clicking...", flush=True)
            publish_btn.click()
            time.sleep(6)
            screenshot3 = f"scratch/{vid}_published.png"
            page.screenshot(path=screenshot3)
            print(f"Saved {screenshot3}", flush=True)
            print(f"SUCCESS: Subtitles uploaded and published for {vid}!", flush=True)
            return True
        else:
            print("Publish button not visible. Trying direct CDP click at (1497, 80)...", flush=True)
            page.mouse.click(1497, 80)
            time.sleep(6)
            screenshot3 = f"scratch/{vid}_published.png"
            page.screenshot(path=screenshot3)
            print(f"Saved {screenshot3}", flush=True)
            return True

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "mQpQEuXiEZ4"
    publish_subtitles_for_video(vid)
