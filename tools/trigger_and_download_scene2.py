import time
import json
import shutil
import zipfile
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import parse_blueprint, ensure_audio, build_master_film, RENDERS_DIR, FLOW_RENDERS_DIR

TRACK_ID = "1hoVaPwWMes"
DEST_DIR = FLOW_RENDERS_DIR / TRACK_ID
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_CLIP = DEST_DIR / "scene_02.mp4"

def trigger_and_download():
    print("Connecting to Chrome on port 9225...")
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

        print(f"Flow page: {flow_page.url}")

        # Set automated download behavior via CDP
        try:
            cdp = flow_page.context.new_cdp_session(flow_page)
            cdp.send("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": str(Path.home() / "Downloads")
            })
        except Exception as e:
            print("CDP warning:", e)

        # Count existing 'Open video in editor' buttons before trigger
        existing_ed_btns = flow_page.locator("button[aria-label='Open video in editor'], [role='button'][aria-label='Open video in editor']").count()
        print(f"Existing video cards in chat: {existing_ed_btns}")

        # Click the submit button (arrow_forward)
        send_btn = flow_page.locator("button").filter(has_text="arrow_forward").first
        if not send_btn.is_visible():
            send_btn = flow_page.locator("button:has-text('arrow_forward')").first

        print(f"Clicking submit button (visible: {send_btn.is_visible()})...")
        send_btn.click()
        flow_page.wait_for_timeout(3000)

        # Check if approval button appears
        print("Checking for credit approval...")
        for i in range(5):
            appr = flow_page.locator(".option-row:not(.read-only):has-text('Always approve'), .option-row:not(.read-only):has-text('Approve')").first
            if appr.count() > 0 and appr.is_visible():
                print(f"Found active approval option! Clicking...")
                appr.click()
                flow_page.wait_for_timeout(2000)
                break
            flow_page.wait_for_timeout(1000)

        # Monitor until NEW video appears (count > existing_ed_btns and progress % disappears)
        print("Monitoring Veo generation in queue...")
        start_time = time.time()
        new_video_ready = False

        for poll in range(60): # up to 5 minutes
            time.sleep(5)
            elapsed = int(time.time() - start_time)

            curr_ed_btns = flow_page.locator("button[aria-label='Open video in editor'], [role='button'][aria-label='Open video in editor']").count()
            stop_btn = flow_page.locator("button:has-text('stop'), [role='button']:has-text('stop')").first
            has_stop = stop_btn.count() > 0 and stop_btn.is_visible()
            pct = flow_page.locator("text=/\\b\\d{1,2}%\\b/").first
            pct_txt = pct.inner_text().strip() if (pct.count() > 0 and pct.is_visible()) else ""

            print(f"[{elapsed}s] Cards: {curr_ed_btns} (was {existing_ed_btns}) | Stop: {has_stop} | Progress: '{pct_txt}'")

            if curr_ed_btns > existing_ed_btns and not has_stop and not pct_txt:
                print(f"[{elapsed}s] NEW SCENE GENERATION COMPLETE! Total cards now: {curr_ed_btns}")
                new_video_ready = True
                time.sleep(3)
                break

        if not new_video_ready:
            print("Timed out or new video did not register.")
            browser.close()
            return

        # Click the LAST 'Open video in editor' button
        last_ed_btn = flow_page.locator("button[aria-label='Open video in editor'], [role='button'][aria-label='Open video in editor']").last
        print("Clicking latest 'Open video in editor' button...")
        last_ed_btn.click()
        flow_page.wait_for_timeout(4000)

        # Click 'Download media'
        dl_btn = flow_page.locator("button[aria-label='Download media'], [role='button'][aria-label='Download media'], button:has-text('Download media')").first
        print(f"Clicking 'Download media' (visible: {dl_btn.is_visible()})...")
        dl_btn.click()
        flow_page.wait_for_timeout(2000)

        # Select 720p / Original size
        res_btn = flow_page.locator("button:has-text('Original size'), [role='menuitem']:has-text('Original size'), button:has-text('720p')").first
        if res_btn.count() > 0 and res_btn.is_visible():
            print(f"Selecting resolution: '{res_btn.inner_text().strip()}'...")
            res_btn.click()

        # Catch downloaded file in Downloads folder
        downloads_dir = Path.home() / "Downloads"
        click_t = time.time() - 4
        downloaded = False
        for _ in range(15):
            time.sleep(1)
            mp4s = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t]
            zips = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t]
            if mp4s:
                newest = max(mp4s, key=lambda x: x.stat().st_mtime)
                if newest.stat().st_size > 500_000:
                    shutil.copy2(newest, DEST_CLIP)
                    print(f"[SUCCESS] Downloaded Scene 2: {newest.name} -> {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                    downloaded = True
                    break
            elif zips:
                newest = max(zips, key=lambda x: x.stat().st_mtime)
                with zipfile.ZipFile(newest, "r") as z:
                    names = [n for n in z.namelist() if n.endswith(".mp4")]
                    if names:
                        ext = z.extract(names[0], DEST_DIR)
                        shutil.move(ext, DEST_CLIP)
                        print(f"[SUCCESS] Extracted Scene 2: {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                        downloaded = True
                        break

        # Return back to workspace
        print("Returning to workspace...")
        flow_page.go_back()
        flow_page.wait_for_timeout(3000)
        browser.close()

    # If successfully downloaded, assemble the final master film!
    if downloaded and DEST_CLIP.exists():
        existing_clips = sorted(DEST_DIR.glob("scene_*.mp4"))
        print(f"\n[Assembly] Found {len(existing_clips)} scenes in {DEST_DIR.name}:")
        for c in existing_clips:
            print(f"  - {c.name} ({c.stat().st_size} bytes)")

        bp_file = ROOT / "production" / "google_flow_prompts" / "murugan" / "1hoVaPwWMes_Kandha_Sashti_Kavasam__Ka.md"
        bp = parse_blueprint(bp_file)
        audio_path = ensure_audio(TRACK_ID)
        out_film = RENDERS_DIR / f"murugan_{TRACK_ID}_master.mp4"
        print(f"\nAssembling Final Master Film with all 3 distinct Veo clips: {out_film.name}...")
        build_master_film(bp, existing_clips, audio_path, out_film)
        print(f"\n[MASTER FILM COMPLETE] {out_film.name} ({out_film.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == '__main__':
    trigger_and_download()
