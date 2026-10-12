import time
import os
import glob
import zipfile
import shutil
import sys
import io
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

DOWNLOAD_DIR = Path.home() / "Downloads"

def generate_and_save_scene(track_id: str, scene_num: int, prompt: str):
    print(f"\n{'='*65}")
    print(f"[Google Flow] Generating Track {track_id} | Consecrated Scene {scene_num}/7")
    print(f"Prompt: {prompt[:90]}...")
    print(f"{'='*65}")

    out_dir = Path("C:/GitHub/Gurukuladesam/production/google_flow_renders") / track_id
    out_dir.mkdir(parents=True, exist_ok=True)
    dst_mp4 = out_dir / f"scene_{scene_num:02d}.mp4"

    if dst_mp4.exists() and dst_mp4.stat().st_size > 1000000:
        print(f"Scene {scene_num} already exists ({dst_mp4.stat().st_size:,} bytes). Skipping.")
        return dst_mp4

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        flow_tabs = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url]
        if not flow_tabs:
            raise RuntimeError("No Google Flow project tab found!")
        
        page = flow_tabs[0]
        page.bring_to_front()

        before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
        initial_dl_count = page.locator('button:has-text("download"), [role="button"]:has-text("download")').count()

        editor = page.locator('div.ProseMirror').first
        editor.click()
        page.wait_for_timeout(300)
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

        submit_btn = page.locator('button:has-text("arrow_forward"), [role="button"]:has-text("arrow_forward")').first
        if submit_btn.is_visible() and submit_btn.is_enabled():
            submit_btn.click()
        else:
            editor.focus()
            page.keyboard.press("Enter")

        page.wait_for_timeout(3000)

        print("Waiting for Veo 3.1 - Lite rendering to finalize...")
        start_time = time.time()
        for i in range(50):
            time.sleep(5)
            elapsed = int(time.time() - start_time)
            stop_count = page.locator('button:has-text("stop"), [role="button"]:has-text("stop")').count()
            current_dl_count = page.locator('button:has-text("download"), [role="button"]:has-text("download")').count()
            
            print(f"[{elapsed:3d}s] Veo 3.1 rendering... StopBtn: {stop_count > 0} | Cards: {current_dl_count}")
            
            if (stop_count == 0 and current_dl_count > initial_dl_count) or (i > 4 and current_dl_count > initial_dl_count and stop_count == 0):
                print(f"Card ready! Increment: {initial_dl_count} -> {current_dl_count}")
                page.wait_for_timeout(3000)
                break
        else:
            print("Warning: Render timed out or count did not increment. Attempting download on top card...")

        dl_btn = page.locator('button:has-text("download"), [role="button"]:has-text("download")').first
        dl_btn.scroll_into_view_if_needed()
        dl_btn.click()
        page.wait_for_timeout(2000)

        menu_opt = page.locator('button:has-text("Original"), [role="menuitem"]:has-text("Original"), [role="menuitem"]:has-text("720p")').first
        if menu_opt.is_visible():
            menu_opt.click()
            page.wait_for_timeout(1000)

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

        with zipfile.ZipFile(new_zip, 'r') as z:
            mp4_names = [n for n in z.namelist() if n.lower().endswith('.mp4')]
            if not mp4_names:
                raise RuntimeError(f"No MP4 found inside zip: {z.namelist()}")
            extracted = z.extract(mp4_names[0], out_dir)
            shutil.move(extracted, dst_mp4)

        print(f"Successfully saved {dst_mp4.name} ({dst_mp4.stat().st_size:,} bytes)")
        browser.close()
        return dst_mp4

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--track', required=True)
    parser.add_argument('--scene', type=int, required=True)
    parser.add_argument('--prompt', required=True)
    args = parser.parse_args()

    generate_and_save_scene(args.track, args.scene, args.prompt)
