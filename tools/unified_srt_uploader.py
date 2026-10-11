import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

def upload_and_publish_video_srt(vid):
    srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
    print(f"\n==========================================", flush=True)
    print(f"Starting unified SRT upload for {vid}", flush=True)
    print(f"SRT file: {srt_file}", flush=True)
    assert os.path.exists(srt_file), f"SRT file not found: {srt_file}"
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
        page = browser.contexts[0].pages[0]
        
        target_url = f"https://studio.youtube.com/video/{vid}/translations"
        print(f"Navigating to {target_url}...", flush=True)
        page.goto(target_url)
        time.sleep(5)
        print("Page URL:", page.url, flush=True)
        
        # 1. Click Upload manual
        print("Clicking 'Upload manual'...", flush=True)
        # We can locate by ID or text inside shadow root
        upload_btn = page.locator("#upload-default-language-button, ytcp-button:has-text('Upload manual')").first
        upload_btn.click()
        time.sleep(2)
        
        # 2. Click Continue with expect_file_chooser
        print("Clicking 'Continue' and waiting for file chooser...", flush=True)
        with page.expect_file_chooser(timeout=10000) as fc_info:
            continue_btn = page.locator("ytcp-button:has-text('Continue'), button:has-text('Continue')").first
            continue_btn.click()
            
        fc = fc_info.value
        print("File chooser intercepted! Uploading:", srt_file, flush=True)
        fc.set_files(srt_file)
        print("File set! Waiting 7s for editor to load...", flush=True)
        time.sleep(7)
        
        os.makedirs("scratch", exist_ok=True)
        page.screenshot(path=f"scratch/{vid}_in_editor.png")
        print(f"Saved scratch/{vid}_in_editor.png", flush=True)
        
        # 3. Click Publish
        print("Clicking 'Publish' button in editor...", flush=True)
        publish_btn = page.locator("#publish-button, ytcp-button:has-text('Publish'), button:has-text('Publish')").first
        publish_btn.click()
        time.sleep(5)
        
        page.screenshot(path=f"scratch/{vid}_published.png")
        print(f"Saved scratch/{vid}_published.png", flush=True)
        print(f"SUCCESS: Subtitles uploaded and published for {vid}!", flush=True)

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "Mata6vtnrjQ"
    upload_and_publish_video_srt(vid)
