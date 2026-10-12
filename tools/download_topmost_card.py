import time
import os
import glob
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

DOWNLOAD_DIR = Path.home() / "Downloads"
DEST_PATH = Path("production/google_flow_renders/--4jzoezBW8/scene_04.mp4")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]
    flow_page = [page for page in ctx.pages if "flow.google.com" in page.url][0]
    
    before_files = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4")))
    
    # Scroll to top of the feed container
    flow_page.evaluate("""() => {
        const scrollers = Array.from(document.querySelectorAll('*')).filter(el => {
            const s = window.getComputedStyle(el);
            return (s.overflowY === 'auto' || s.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
        });
        scrollers.forEach(s => s.scrollTop = 0);
    }""")
    flow_page.wait_for_timeout(1000)
    
    # Locate all download buttons
    dls = flow_page.locator("button:has-text('download'), [role='button']:has-text('download'), button[aria-label*='download' i]").all()
    print(f"Total download buttons visible: {len(dls)}")
    
    if dls:
        # The topmost card has the first download button!
        print("Clicking topmost download button (Scene 4)...")
        dls[0].scroll_into_view_if_needed()
        dls[0].click()
        flow_page.wait_for_timeout(2000)
        
        # Check if resolution dropdown appeared
        menu_items = flow_page.locator("button:has-text('Original'), [role='menuitem']:has-text('Original'), button:has-text('720p'), [role='menuitem']:has-text('720p')").all()
        if menu_items:
            print(f"Clicking resolution option: {menu_items[0].inner_text()}")
            menu_items[0].click()
        else:
            print("No resolution menu opened, direct download triggered.")
            
    # Wait for downloaded file in ~/Downloads
    downloaded_file = None
    for i in range(20):
        flow_page.wait_for_timeout(2000)
        new_files = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4"))) - before_files
        cr_files = glob.glob(str(DOWNLOAD_DIR / "*.crdownload"))
        if new_files and not cr_files:
            downloaded_file = list(new_files)[0]
            break

    if not downloaded_file:
        # Check newest file modified within last 60 seconds
        all_mp4s = sorted(glob.glob(str(DOWNLOAD_DIR / "*.mp4")), key=os.path.getmtime, reverse=True)
        if all_mp4s and (time.time() - os.path.getmtime(all_mp4s[0])) < 60:
            downloaded_file = all_mp4s[0]

    if downloaded_file:
        DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(downloaded_file, str(DEST_PATH))
        size = os.path.getsize(DEST_PATH)
        print(f"SUCCESS: Scene 4 saved to {DEST_PATH} ({size:,} bytes)")
    else:
        print("ERROR: Downloaded file not detected in ~/Downloads.")
        
    browser.close()
