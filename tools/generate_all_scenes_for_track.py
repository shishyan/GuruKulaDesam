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

def generate_full_track(track_id: str):
    matches = list(Path("production/google_flow_prompts").glob(f"*/{track_id}*.md"))
    if not matches:
        print(f"Error: No blueprint for {track_id}")
        return

    bp = parse_blueprint(matches[0])
    scenes = bp["scenes"] # ALL scenes in the blueprint!
    print(f"\n================================================================================")
    print(f"GENERATING FULL {len(scenes)}-SCENE SUITE FOR: {bp['title']} ({track_id})")
    print(f"================================================================================")

    dest_dir = FLOW_RENDERS_DIR / track_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9225")
        ctx = browser.contexts[0]
        flow_page = None
        for page in ctx.pages:
            if "flow.google" in page.url:
                flow_page = page
                break

        if not flow_page:
            print("ERROR: Flow page not found on port 9225!")
            browser.close()
            return

        # Configure download behavior
        try:
            cdp = flow_page.context.new_cdp_session(flow_page)
            cdp.send("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": str(Path.home() / "Downloads")
            })
        except Exception:
            pass

        # Return to workspace if in editor
        if "/edit/" in flow_page.url:
            flow_page.go_back()
            flow_page.wait_for_timeout(3000)

        for sc in scenes:
            sc_num = sc["scene_num"]
            out_clip = dest_dir / f"scene_{sc_num:02d}.mp4"
            if out_clip.exists() and out_clip.stat().st_size > 500_000:
                print(f"[Done] Scene {sc_num} already exists ({out_clip.stat().st_size} bytes). Skipping.")
                continue

            prompt = (
                f"Devotional cinematic 16:9 photorealistic video: {sc['prompt']} "
                f"Exclusions: {sc.get('exclusions', '')} {bp['continuity'].get('Hard Exclusions', '')} "
                "No text, no subtitles, no watermarks, no modern clothing, no western faces, no plastic, no mobile phones."
            )
            print(f"\n>>> GENERATING SCENE {sc_num} of {len(scenes)} <<<")
            print(f"Prompt: {prompt[:120]}...")

            existing_cards = flow_page.locator("button[aria-label='Open video in editor'], [role='button'][aria-label='Open video in editor']").count()

            # Focus ProseMirror and type prompt
            flow_page.evaluate(
                """(text) => {
                    const el = document.querySelector('div.ProseMirror');
                    if (el) {
                        el.focus();
                        document.execCommand('selectAll', false, null);
                        document.execCommand('delete', false, null);
                        document.execCommand('insertText', false, text);
                    }
                }""",
                prompt
            )
            flow_page.wait_for_timeout(1000)

            # Click submit
            send_btn = flow_page.locator("button").filter(has_text="arrow_forward").first
            if not send_btn.is_visible():
                send_btn = flow_page.locator("button:has-text('arrow_forward')").first

            send_btn.click()
            flow_page.wait_for_timeout(3000)

            # Check for credit approval if prompted
            for _ in range(5):
                appr = flow_page.locator(".option-row:not(.read-only):has-text('Always approve'), .option-row:not(.read-only):has-text('Approve')").first
                if appr.count() > 0 and appr.is_visible():
                    print("Authorizing credit deduction...")
                    appr.click()
                    flow_page.wait_for_timeout(2000)
                    break
                flow_page.wait_for_timeout(1000)

            # Monitor generation
            print(f"Monitoring synthesis for Scene {sc_num}...")
            start_t = time.time()
            scene_ready = False
            for _ in range(60):
                time.sleep(5)
                elapsed = int(time.time() - start_t)
                curr_cards = flow_page.locator("button[aria-label='Open video in editor'], [role='button'][aria-label='Open video in editor']").count()
                stop_btn = flow_page.locator("button:has-text('stop'), [role='button']:has-text('stop')").first
                has_stop = stop_btn.count() > 0 and stop_btn.is_visible()
                pct = flow_page.locator("text=/\\b\\d{1,2}%\\b/").first
                pct_txt = pct.inner_text().strip() if (pct.count() > 0 and pct.is_visible()) else ""

                if curr_cards > existing_cards and not has_stop and not pct_txt and elapsed >= 20:
                    print(f"[{elapsed}s] Scene {sc_num} render complete!")
                    scene_ready = True
                    time.sleep(3)
                    break

            if not scene_ready:
                print(f"[Warning] Scene {sc_num} timed out. Proceeding to next.")
                continue

            # Open in editor
            last_btn = flow_page.locator("button[aria-label='Open video in editor'], [role='button'][aria-label='Open video in editor']").last
            last_btn.click()
            flow_page.wait_for_timeout(4000)

            # Trigger Download media
            dl_btn = flow_page.locator("button[aria-label='Download media'], [role='button'][aria-label='Download media'], button:has-text('Download media')").first
            dl_btn.click()
            flow_page.wait_for_timeout(2000)

            # Select 720p Original size
            res_btn = flow_page.locator("button:has-text('Original size'), [role='menuitem']:has-text('Original size'), button:has-text('720p')").first
            if res_btn.count() > 0 and res_btn.is_visible():
                res_btn.click()

            # Catch in Downloads
            downloads_dir = Path.home() / "Downloads"
            click_t = time.time() - 4
            for _ in range(15):
                time.sleep(1)
                mp4s = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t]
                zips = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t]
                if mp4s:
                    newest = max(mp4s, key=lambda x: x.stat().st_mtime)
                    if newest.stat().st_size > 500_000:
                        shutil.copy2(newest, out_clip)
                        print(f"[SUCCESS] Saved Scene {sc_num}: {out_clip.name} ({out_clip.stat().st_size} bytes)")
                        break
                elif zips:
                    newest = max(zips, key=lambda x: x.stat().st_mtime)
                    with zipfile.ZipFile(newest, "r") as z:
                        names = [n for n in z.namelist() if n.endswith(".mp4")]
                        if names:
                            ext = z.extract(names[0], dest_dir)
                            shutil.move(ext, out_clip)
                            print(f"[SUCCESS] Extracted Scene {sc_num}: {out_clip.name} ({out_clip.stat().st_size} bytes)")
                            break

            # Return back to workspace
            flow_page.go_back()
            flow_page.wait_for_timeout(3000)

        browser.close()

    # Re-assemble the master film with all newly available scenes
    all_clips = sorted(dest_dir.glob("scene_*.mp4"))
    print(f"\n[Assembly] Found {len(all_clips)} distinct scenes for {track_id}. Building rich master film...")
    audio_path = ensure_audio(track_id)
    out_film = RENDERS_DIR / f"murugan_{track_id}_master.mp4"
    build_master_film(bp, all_clips, audio_path, out_film)
    print(f"\n[MASTER FILM REBUILT WITH {len(all_clips)} SCENES] {out_film.name} ({out_film.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == '__main__':
    generate_full_track("1hoVaPwWMes")
