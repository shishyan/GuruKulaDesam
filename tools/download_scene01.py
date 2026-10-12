import time
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

dest_dir = Path("production/google_flow_renders/--4jzoezBW8")
dest_dir.mkdir(parents=True, exist_ok=True)
dest_clip = dest_dir / "scene_01.mp4"

print("Downloading Scene 01 clip from Google Flow...")
since_time = time.time()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]

    # Find the top card download button
    # In the screenshot, there is a download icon button above the new video
    dl_btn = page.locator('button[aria-label*="download" i], [aria-label="Download"], button:has-text("download")').first
    if not dl_btn.is_visible():
        # Fallback to SVG button with download icon
        dl_btn = page.locator('.media-card button, [role="article"] button, div[role="listitem"] button').filter(has_text="download").first

    # Set up download listener
    with page.expect_download(timeout=15000) as download_info:
        dl_btn.click()
        print("Clicked download button on Scene 01 card...")
        
    download = download_info.value
    download.save_as(str(dest_clip))
    print(f"✅ Scene 01 saved successfully to {dest_clip} ({dest_clip.stat().st_size / 1024 / 1024:.2f} MB)")
    browser.close()
