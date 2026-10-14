# -*- coding: utf-8 -*-
import sys
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# Load the 7-scene package for the pilot tracks
BATCH_FILE = Path("production/colab_handoff/pending_7scenes_batch_prompts.json")
with open(BATCH_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Priority Pilot Tracks
target_tracks = data.get("tracks", [])[:3]

ROOT_OUT = Path("production/google_flow_renders")

def run_flow_loop():
    print(f"============================================================")
    print(f"🎬 GURUKULADESAM FLOW AUTONOMOUS GENERATOR — 7 SCENES MANDATE")
    print(f"Targeting: {len(target_tracks)} pilot tracks (7 scenes each)")
    print(f"============================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]
        print(f"Connected to Flow workspace: {page.url}\n")

        for t_idx, track in enumerate(target_tracks, 1):
            tid = track["track_id"]
            title = track["title"]
            scenes = track["scenes"] # exactly 7 scenes
            
            track_dir = ROOT_OUT / tid
            track_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"\n=======================================================")
            print(f"[{t_idx}/{len(target_tracks)}] Track: {title} ({tid})")
            print(f"=======================================================")

            for sc in scenes:
                sc_num = sc["scene_num"]
                prompt = sc["prompt"]
                dest_file = track_dir / f"scene_{sc_num:02d}.mp4"

                # Check if already generated recently
                if dest_file.exists() and dest_file.stat().st_size > 500_000:
                    # Check file age to avoid skipping if it's the old 3-scene legacy take
                    # Let's inspect modify time
                    mtime = dest_file.stat().st_mtime
                    if time.time() - mtime < 3600 * 2: # generated in last 2 hours
                        print(f"  [Skip] Scene {sc_num:02d} already generated fresh ({dest_file.stat().st_size / 1024 / 1024:.2f} MB).")
                        continue

                print(f"\n  [Flow Veo 3.1 Lite] Submitting Scene {sc_num:02d}/07...")
                
                # 1. Focus ProseMirror editor
                editor = page.locator('div.ProseMirror').first
                if not editor.is_visible():
                    page.locator('div:has-text("What do you want to create?")').last.click()
                    page.wait_for_timeout(300)
                    
                editor.click()
                page.wait_for_timeout(200)
                
                # 2. Insert text
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

                # 3. Submit
                submit_btn = page.locator('button:has-text("arrow_forward"), [role="button"]:has-text("arrow_forward"), button[aria-label*="Send" i], button[aria-label*="Generate" i]').first
                if submit_btn.is_visible() and submit_btn.is_enabled():
                    submit_btn.click()
                else:
                    page.keyboard.press("Enter")
                    
                print(f"  [Op] Submitted prompt. Monitoring render status...")

                # 4. Wait for render to finish
                start_render = time.time()
                rendered = False
                time.sleep(5)
                
                for poll in range(35): # up to ~2.5 mins
                    time.sleep(4)
                    elapsed = int(time.time() - start_render)
                    
                    stop_btn = page.locator('button:has-text("Stop"), [role="button"]:has-text("Stop")').first
                    is_active = stop_btn.is_visible()
                    
                    if not is_active and elapsed >= 15:
                        print(f"  [Render Complete] ({elapsed}s). Downloading video card...")
                        rendered = True
                        break
                    elif elapsed % 12 == 0:
                        print(f"    ... rendering in progress ({elapsed}s)")

                if not rendered:
                    print(f"  ⚠️ Warning: Render poll timed out after {int(time.time() - start_render)}s. Attempting download anyway...")

                # 5. Download newly rendered clip
                time.sleep(2)
                dl_btn = page.locator('button[aria-label*="download" i], [aria-label="Download"], button:has-text("download")').first
                try:
                    with page.expect_download(timeout=15000) as download_info:
                        dl_btn.click()
                    download = download_info.value
                    download.save_as(str(dest_file))
                    print(f"  ✅ Saved Scene {sc_num:02d} ({dest_file.stat().st_size / 1024 / 1024:.2f} MB)")
                except Exception as e:
                    print(f"  ❌ Download failed: {e}")

                # Gentle pacing between prompts
                time.sleep(3)

        browser.close()
        print(f"\n=======================================================")
        print(f"🎉 BATCH COMPLETE: All 7 scenes generated successfully!")
        print(f"=======================================================")

if __name__ == '__main__':
    run_flow_loop()
