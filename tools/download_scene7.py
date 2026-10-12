import time
import os
import glob
import shutil
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright

DOWNLOAD_DIR = Path.home() / "Downloads"
DEST_PATH = Path("production/google_flow_renders/4-FJ8eh7Als/scene_07.mp4")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]
    flow_page = [page for page in ctx.pages if "flow.google.com" in page.url][0]
    
    before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
    before_mp4s = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4")))
    
    # Locate all download buttons
    dls = flow_page.locator("button:has-text('download'), [role='button']:has-text('download'), button[aria-label*='download' i]").all()
    print(f"Total download buttons visible: {len(dls)}")
    
    if dls:
        print("Clicking topmost download button (Scene 7)...")
        dls[0].scroll_into_view_if_needed()
        dls[0].click()
        flow_page.wait_for_timeout(2000)
        
        # Check if resolution dropdown appeared
        menu_items = flow_page.locator("button:has-text('Original'), [role='menuitem']:has-text('Original'), button:has-text('720p'), [role='menuitem']:has-text('720p')").all()
        if menu_items:
            print(f"Clicking resolution option: {menu_items[0].inner_text()}")
            menu_items[0].click()
            
    # Wait for downloaded file in ~/Downloads
    downloaded_file = None
    for i in range(25):
        flow_page.wait_for_timeout(2000)
        new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip"))) - before_zips
        cr_files = glob.glob(str(DOWNLOAD_DIR / "*.crdownload"))
        if new_zips and not cr_files:
            downloaded_file = list(new_zips)[0]
            break
        new_mp4s = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4"))) - before_mp4s
        if new_mp4s and not cr_files:
            downloaded_file = list(new_mp4s)[0]
            break

    if not downloaded_file:
        all_zips = sorted(glob.glob(str(DOWNLOAD_DIR / "*.zip")), key=os.path.getmtime, reverse=True)
        if all_zips and (time.time() - os.path.getmtime(all_zips[0])) < 90:
            downloaded_file = all_zips[0]

    if downloaded_file:
        DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        if downloaded_file.endswith(".zip"):
            with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
                mp4_names = [n for n in zip_ref.namelist() if n.lower().endswith(".mp4")]
                if mp4_names:
                    extracted_path = zip_ref.extract(mp4_names[0], str(DOWNLOAD_DIR / "temp_extract"))
                    shutil.move(extracted_path, str(DEST_PATH))
                    print(f"Extracted and saved: {DEST_PATH} ({DEST_PATH.stat().st_size:,} bytes)")
        else:
            shutil.copy2(downloaded_file, str(DEST_PATH))
            print(f"SUCCESS: Scene 7 saved to {DEST_PATH} ({DEST_PATH.stat().st_size:,} bytes)")
    else:
        print("ERROR: Downloaded file not detected in ~/Downloads.")
