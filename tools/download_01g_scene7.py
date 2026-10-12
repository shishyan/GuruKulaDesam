import os
import glob
import time
import zipfile
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

DOWNLOAD_DIR = Path.home() / "Downloads"
DEST_PATH = Path("production/google_flow_renders/01g0sJdaL2I/scene_07.mp4")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]
    flow_page = [page for page in ctx.pages if "flow.google.com" in page.url][0]
    
    before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
    
    # Locate all download buttons
    dls = flow_page.locator("button:has-text('download'), [role='button']:has-text('download'), button[aria-label*='download' i]").all()
    print(f"Total download buttons visible: {len(dls)}")
    
    if dls:
        print("Clicking topmost download button (Scene 7)...")
        dls[0].scroll_into_view_if_needed()
        dls[0].click()
        flow_page.wait_for_timeout(2000)
        
        menu_items = flow_page.locator("button:has-text('Original'), [role='menuitem']:has-text('Original'), button:has-text('720p'), [role='menuitem']:has-text('720p')").all()
        if menu_items:
            print(f"Clicking resolution option: {menu_items[0].inner_text()}")
            menu_items[0].click()
            
    # Wait for downloaded zip in ~/Downloads
    downloaded_zip = None
    for i in range(25):
        flow_page.wait_for_timeout(2000)
        new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip"))) - before_zips
        cr_files = glob.glob(str(DOWNLOAD_DIR / "*.crdownload"))
        if new_zips and not cr_files:
            downloaded_zip = sorted(list(new_zips), key=os.path.getmtime, reverse=True)[0]
            break

    if downloaded_zip:
        DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(downloaded_zip, 'r') as z:
            for name in z.namelist():
                if name.endswith('.mp4'):
                    extracted = z.extract(name, str(DEST_PATH.parent))
                    if DEST_PATH.exists():
                        DEST_PATH.unlink()
                    os.rename(extracted, str(DEST_PATH))
                    print(f"✅ SUCCESS: Scene 7 saved to {DEST_PATH} ({DEST_PATH.stat().st_size:,} bytes)")
                    break
    else:
        print("ERROR: Downloaded zip not detected in ~/Downloads.")
        
    browser.close()
