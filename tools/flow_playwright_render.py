import time
import os
import glob
import zipfile
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

DOWNLOAD_DIR = Path.home() / "Downloads"

def generate_scene(track_id: str, scene_num: int, prompt: str):
    print(f"\n{'='*60}")
    print(f"[Playwright CDP] Track {track_id} | Scene {scene_num}/7")
    print(f"Prompt: {prompt[:80]}...")
    print(f"{'='*60}")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        flow_tabs = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url]
        if not flow_tabs:
            raise RuntimeError("No Google Flow project tab found!")
        
        page = flow_tabs[0]
        page.bring_to_front()

        # Snapshot existing zips
        before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))

        # Count existing download buttons
        initial_dl_count = page.locator('button:has-text("download"), [role="button"]:has-text("download")').count()
        print(f"Initial completed cards in Flow: {initial_dl_count}")

        # Locate ProseMirror editor
        editor = page.locator('div.ProseMirror').first
        editor.click()
        page.wait_for_timeout(300)

        # Clear and insert prompt
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(200)

        page.evaluate(
            """(text) => {
                const el = document.querySelector('div.ProseMirror');
                if (el) {
                    el.focus();
                    document.execCommand('insertText', false, text);
                }
            }""",
            prompt
        )
        page.wait_for_timeout(500)

        # Click the circular submit button (with arrow)
        submit_btn = page.locator('button:has-text("arrow_forward"), [role="button"]:has-text("arrow_forward")').first
        if submit_btn.is_visible() and submit_btn.is_enabled():
            print("Clicking submit button...")
            submit_btn.click()
        else:
            print("Pressing Enter in editor...")
            editor.focus()
            page.keyboard.press("Enter")

        page.wait_for_timeout(2000)

        # Poll until rendering starts and finishes
        print("Waiting for Veo 3.1 generation...")
        start_time = time.time()
        for i in range(50): # up to 250s
            time.sleep(5)
            elapsed = int(time.time() - start_time)
            
            # Check for stop button or progress indicator
            stop_count = page.locator('button:has-text("stop"), [role="button"]:has-text("stop")').count()
            current_dl_count = page.locator('button:has-text("download"), [role="button"]:has-text("download")').count()
            
            print(f"[{elapsed:3d}s] Rendering... StopBtn: {stop_count > 0} | Cards: {current_dl_count}")
            
            if (stop_count == 0 and current_dl_count > initial_dl_count) or (i > 4 and current_dl_count > initial_dl_count and stop_count == 0):
                print(f"✨ Generation complete! Card count grew from {initial_dl_count} to {current_dl_count}.")
                page.wait_for_timeout(3000)
                break
        else:
            print("Warning: Timed out waiting for card count to increase.")

        # Download topmost card
        dl_btn = page.locator('button:has-text("download"), [role="button"]:has-text("download")').first
        print("Clicking top download button...")
        dl_btn.scroll_into_view_if_needed()
        dl_btn.click()
        page.wait_for_timeout(2000)

        # Select resolution menu if present
        menu_opt = page.locator('button:has-text("Original"), [role="menuitem"]:has-text("Original"), [role="menuitem"]:has-text("720p")').first
        if menu_opt.is_visible():
            print(f"Selecting resolution menu option: {menu_opt.inner_text().strip()}")
            menu_opt.click()
            page.wait_for_timeout(1000)

        # Wait for zip in ~/Downloads
        print("Waiting for downloaded zip...")
        new_zip = None
        for _ in range(30):
            time.sleep(2)
            after_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
            diff = after_zips - before_zips
            cr = glob.glob(str(DOWNLOAD_DIR / "*.crdownload"))
            if diff and not cr:
                new_zip = sorted(list(diff), key=os.path.getmtime, reverse=True)[0]
                break

        if not new_zip:
            zips = sorted(glob.glob(str(DOWNLOAD_DIR / "*.zip")), key=os.path.getmtime, reverse=True)
            if zips and (time.time() - os.path.getmtime(zips[0]) < 120):
                new_zip = zips[0]

        if not new_zip:
            raise RuntimeError("No downloaded zip found!")

        print(f"📦 Downloaded archive: {new_zip} ({os.path.getsize(new_zip):,} bytes)")

        # Extract MP4
        out_dir = Path("C:/GitHub/Gurukuladesam/production/google_flow_renders") / track_id
        out_dir.mkdir(parents=True, exist_ok=True)
        dst_mp4 = out_dir / f"scene_{scene_num:02d}.mp4"

        with zipfile.ZipFile(new_zip, 'r') as z:
            mp4_names = [n for n in z.namelist() if n.lower().endswith('.mp4')]
            if not mp4_names:
                raise RuntimeError(f"No MP4 found inside zip: {z.namelist()}")
            extracted = z.extract(mp4_names[0], out_dir)
            shutil.move(extracted, dst_mp4)

        print(f"✅ Consecrated scene {scene_num} saved to {dst_mp4} ({dst_mp4.stat().st_size:,} bytes)")
        browser.close()
        return dst_mp4

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--track', required=True)
    parser.add_argument('--scene', type=int, required=True)
    parser.add_argument('--prompt', required=True)
    args = parser.parse_args()

    generate_scene(args.track, args.scene, args.prompt)
