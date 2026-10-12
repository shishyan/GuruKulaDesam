import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

DEST_DIR = Path("production/google_flow_renders/1hoVaPwWMes")
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_CLIP = DEST_DIR / "scene_01.mp4"

def monitor_flow():
    print("Monitoring Google Flow on port 9225...")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9225")
        ctx = browser.contexts[0]
        flow_page = None
        for page in ctx.pages:
            if "flow.google" in page.url:
                flow_page = page
                break

        if not flow_page:
            print("ERROR: Flow page not found!")
            browser.close()
            return

        print(f"Monitoring page: {flow_page.url}")
        
        # Configure download behavior via CDP
        try:
            cdp = flow_page.context.new_cdp_session(flow_page)
            cdp.send("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": str(Path.home() / "Downloads")
            })
            print("Configured CDP automated download path.")
        except Exception as e:
            print("CDP setDownloadBehavior warning:", e)

        start_time = time.time()
        approved = False
        completed = False

        while time.time() - start_time < 300: # 5 minutes max
            time.sleep(4)
            elapsed = int(time.time() - start_time)

            # Check for approval button
            appr_btns = flow_page.locator("button:has-text('Always approve'), [role='button']:has-text('Always approve')").all()
            if not appr_btns:
                appr_btns = flow_page.locator("button:has-text('Approve'), [role='button']:has-text('Approve')").all()
            
            if appr_btns and not approved:
                for b in appr_btns:
                    if b.is_visible():
                        txt = b.inner_text().strip()
                        print(f"[{elapsed}s] Found approval button: '{txt}'. Clicking...")
                        try:
                            b.click()
                            approved = True
                            flow_page.wait_for_timeout(2000)
                            flow_page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_after_approval.png")
                            print("Clicked approve! Screenshot saved.")
                            break
                        except Exception as e:
                            print("Click error:", e)

            # Check if still generating (Stop button or progress percentage)
            stop_btn = flow_page.locator("button:has-text('stop'), [role='button']:has-text('stop')").first
            is_generating = stop_btn.is_visible()

            # Check percentage indicator if visible
            pct = flow_page.locator("text=/\\b\\d{1,2}%\\b/").first
            pct_txt = pct.inner_text().strip() if (pct.count() > 0 and pct.is_visible()) else ""

            # Check for download button or generated video element
            dl_btns = flow_page.locator("button[aria-label*='Download' i], [role='button'][aria-label*='Download' i], button:has-text('Download')").all()
            visible_dl = [b for b in dl_btns if b.is_visible()]

            # Also check video tags
            videos = flow_page.locator("video").all()
            
            print(f"[{elapsed}s] Generating: {is_generating} | Pct: '{pct_txt}' | DL buttons: {len(visible_dl)} | Videos: {len(videos)}")

            if not is_generating and len(visible_dl) > 0:
                print(f"[{elapsed}s] Generation COMPLETE! {len(visible_dl)} download button(s) found.")
                flow_page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_generation_ready.png")
                
                # Click the first download button
                target_dl = visible_dl[0]
                print(f"Clicking download button '{target_dl.inner_text().strip() or target_dl.get_attribute('aria-label')}'...")
                
                # Record timestamp before click
                click_t = time.time()
                target_dl.click()
                flow_page.wait_for_timeout(2000)

                # Check if resolution menu popped up (e.g. 1080p / 720p / Original)
                res_btn = flow_page.locator("button:has-text('Original size'), [role='menuitem']:has-text('Original size'), button:has-text('720p'), [role='menuitem']:has-text('720p'), button:has-text('1080p'), [role='menuitem']:has-text('1080p')").first
                if res_btn.count() > 0 and res_btn.is_visible():
                    print(f"Selecting resolution option: {res_btn.inner_text().strip()}...")
                    res_btn.click()
                    flow_page.wait_for_timeout(3000)

                # Monitor Downloads folder for the downloaded video
                downloads_dir = Path.home() / "Downloads"
                found_dl = False
                for _ in range(20):
                    time.sleep(1)
                    # Check recent mp4 in Downloads
                    mp4s = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t - 2]
                    zips = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t - 2]
                    if mp4s:
                        newest = max(mp4s, key=lambda x: x.stat().st_mtime)
                        if newest.stat().st_size > 500_000:
                            import shutil
                            shutil.copy2(newest, DEST_CLIP)
                            print(f"[SUCCESS] Downloaded and saved clip to: {DEST_CLIP} ({DEST_CLIP.stat().st_size} bytes)")
                            found_dl = True
                            completed = True
                            break
                    elif zips:
                        import zipfile, shutil
                        newest = max(zips, key=lambda x: x.stat().st_mtime)
                        with zipfile.ZipFile(newest, "r") as z:
                            mp4_names = [m for m in z.namelist() if m.endswith(".mp4")]
                            if mp4_names:
                                ext = z.extract(mp4_names[0], DEST_DIR)
                                shutil.move(ext, DEST_CLIP)
                                print(f"[SUCCESS] Extracted zip to {DEST_CLIP} ({DEST_CLIP.stat().st_size} bytes)")
                                found_dl = True
                                completed = True
                                break

                if found_dl:
                    break
                else:
                    print("Did not detect downloaded file yet; retrying...")

        flow_page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_monitor_final.png")
        browser.close()
        return completed

if __name__ == "__main__":
    monitor_flow()
