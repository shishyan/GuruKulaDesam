import time
import os
import glob
import shutil
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright

DOWNLOAD_DIR = Path.home() / "Downloads"
DEST_PATH = Path("production/google_flow_renders/--4jzoezBW8/scene_05.mp4")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]
    flow_page = [page for page in ctx.pages if "flow.google.com" in page.url][0]
    
    # Snapshot zip and mp4 files
    before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
    before_mp4s = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4")))
    
    print("Waiting for Scene 5 render to complete...")
    for i in range(25):
        time.sleep(3)
        body = flow_page.locator("body").inner_text()
        has_stop = "Stop" in body
        print(f"[{i*3}s] Active render: {has_stop}")
        if not has_stop:
            print("Render completed! Triggering download...")
            break
            
    time.sleep(2)
    # Scroll to top
    flow_page.evaluate("""() => {
        const scrollers = Array.from(document.querySelectorAll('*')).filter(el => {
            const s = window.getComputedStyle(el);
            return (s.overflowY === 'auto' || s.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
        });
        scrollers.forEach(s => s.scrollTop = 0);
    }""")
    flow_page.wait_for_timeout(1000)
    
    dls = flow_page.locator("button:has-text('download'), [role='button']:has-text('download'), button[aria-label*='download' i]").all()
    if dls:
        print("Clicking download button...")
        dls[0].scroll_into_view_if_needed()
        dls[0].click()
        flow_page.wait_for_timeout(2000)
        
        # Check resolution dropdown if any
        menu_items = flow_page.locator("button:has-text('Original'), [role='menuitem']:has-text('Original'), button:has-text('720p'), [role='menuitem']:has-text('720p')").all()
        if menu_items:
            menu_items[0].click()

    # Poll Downloads folder for newly downloaded zip or mp4
    for i in range(20):
        flow_page.wait_for_timeout(2000)
        new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip"))) - before_zips
        new_mp4s = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4"))) - before_mp4s
        
        # If new zip downloaded
        if new_zips:
            latest_zip = sorted(list(new_zips), key=os.path.getmtime, reverse=True)[0]
            with zipfile.ZipFile(latest_zip, 'r') as z:
                for name in z.namelist():
                    if name.endswith('.mp4'):
                        extracted = z.extract(name, str(DEST_PATH.parent))
                        if DEST_PATH.exists():
                            DEST_PATH.unlink()
                        os.rename(extracted, str(DEST_PATH))
                        print(f"SUCCESS: Scene 5 extracted and saved to {DEST_PATH} ({DEST_PATH.stat().st_size:,} bytes)")
                        browser.close()
                        exit(0)
                        
        # If direct mp4 downloaded
        if new_mp4s:
            latest_mp4 = sorted(list(new_mp4s), key=os.path.getmtime, reverse=True)[0]
            shutil.copy2(latest_mp4, str(DEST_PATH))
            print(f"SUCCESS: Scene 5 copied and saved to {DEST_PATH} ({DEST_PATH.stat().st_size:,} bytes)")
            browser.close()
            exit(0)
            
    print("ERROR: Scene 5 download not captured in time.")
    browser.close()
