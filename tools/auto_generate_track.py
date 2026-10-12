import time
import os
import glob
import zipfile
import shutil
import sys
import io
import urllib.request
import websocket
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)

DOWNLOAD_DIR = Path.home() / "Downloads"

def trigger_top_download():
    try:
        tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
        f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
        if not f_tabs:
            return False
        ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)
        ws.send(json.dumps({'id': 1, 'method': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': str(DOWNLOAD_DIR)}}))
        ws.recv()

        js_click = """
        (() => {
            const dls = Array.from(document.querySelectorAll('button, [role="button"]'))
                .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
            if (dls.length > 0) {
                dls[0].scrollIntoView();
                dls[0].click();
                return true;
            }
            return false;
        })()
        """
        ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_click, 'returnByValue': True}}))
        ws.recv()
        ws.close()
        return True
    except Exception as e:
        print("CDP download trigger error:", e)
        return False

def generate_scenes_for_track(track_id: str):
    with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    track_entry = next((t for t in data["tracks"] if t["track_id"] == track_id), None)
    if not track_entry:
        raise ValueError(f"Track {track_id} not found in prompts json!")

    dest_dir = Path("production/google_flow_renders") / track_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*65}")
    print(f"🎬 Processing 7 Consecrated Scenes for Track: {track_id}")
    print(f"{'='*65}")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        flow_page = next((page for page in ctx.pages if "flow.google.com" in page.url), None)
        if not flow_page:
            raise RuntimeError("No Google Flow tab open on port 9222!")

        for scene in track_entry["scenes"]:
            scene_num = scene["scene_num"]
            prompt = scene["prompt"]
            dest_file = dest_dir / f"scene_{scene_num:02d}.mp4"

            if dest_file.exists() and dest_file.stat().st_size > 1_000_000:
                print(f"⏩ Scene {scene_num} already exists ({dest_file.stat().st_size:,} bytes). Skipping.")
                continue

            max_retries = 3
            for attempt in range(1, max_retries + 1):
                print(f"\n--- [Track {track_id}] Generating Scene {scene_num}/7 (Attempt {attempt}/{max_retries}) ---")
                print(f"Prompt: {prompt[:80]}...")

                before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))

                # Ensure Agent sidebar is closed so primary prompt box is active
                try:
                    close_btn = flow_page.locator("button[aria-label*='close' i], button:has-text('close')").first
                    if close_btn.is_visible(timeout=1500):
                        close_btn.click(force=True)
                        flow_page.wait_for_timeout(1000)
                except Exception:
                    pass

                # Ensure Agent mode is toggled OFF (switch to standard/manual generation mode)
                try:
                    agent_chip = flow_page.locator("button.agent-mode-chip-checked").first
                    if agent_chip.is_visible(timeout=1000):
                        agent_chip.click(force=True)
                        flow_page.wait_for_timeout(500)
                except Exception:
                    pass

                # 1. Focus ProseMirror editor and insert prompt
                editor = flow_page.locator("div.ProseMirror").first
                try:
                    editor.click(force=True, timeout=5000)
                except Exception:
                    flow_page.evaluate("() => { const el = document.querySelector('div.ProseMirror'); if (el) el.focus(); }")
                flow_page.wait_for_timeout(300)
                flow_page.keyboard.press("Control+A")
                flow_page.keyboard.press("Backspace")
                flow_page.wait_for_timeout(300)

                flow_page.evaluate(
                    """(text) => {
                        const el = document.querySelector('div.ProseMirror');
                        if (el) {
                            el.focus();
                            document.execCommand('insertText', false, text);
                        }
                    }""",
                    prompt
                )
                flow_page.wait_for_timeout(500)

                # Ensure Video mode is selected in Settings trigger
                try:
                    settings_btn = flow_page.locator("button.settings-trigger-button").first
                    if settings_btn.is_visible(timeout=1000):
                        btn_txt = settings_btn.inner_text().lower()
                        if "video" not in btn_txt:
                            print("Switching settings to Video mode...")
                            settings_btn.click(force=True)
                            flow_page.wait_for_timeout(500)
                            flow_page.locator("button:has-text('Video')").first.click(force=True)
                            flow_page.wait_for_timeout(500)
                            flow_page.keyboard.press("Escape")
                            flow_page.wait_for_timeout(500)
                except Exception as e:
                    print("Video mode check:", e)

                # 2. Click generate / submit
                submit_btn = flow_page.locator("button[aria-label*='Start generation' i], button.generate-icon-button, button:has-text('arrow_forward')").last
                clicked = False
                try:
                    if submit_btn.is_visible(timeout=3000):
                        submit_btn.click(force=True, timeout=5000)
                        clicked = True
                except Exception:
                    pass

                if not clicked:
                    editor.focus()
                    flow_page.keyboard.press("Enter")

                flow_page.wait_for_timeout(4000)

                # 3. Wait for render to finish or detect failure
                print(f"Waiting for Scene {scene_num} to start and complete render...")
                render_started = False
                generation_failed = False
                for i in range(45):
                    flow_page.wait_for_timeout(3000)
                    try:
                        body_text = flow_page.locator("body").inner_text(timeout=4000)
                    except Exception:
                        continue
                    
                    has_stop = "Stop" in body_text
                    # Check for progress percentage (e.g. 15%, 45%, 93%)
                    import re
                    has_pct = bool(re.search(r'\b\d{1,2}%\b', body_text))

                    if has_stop or has_pct:
                        render_started = True

                    # Check for server-side generation failure
                    if "Sorry, this video failed to generate" in body_text or "Failed to generate" in body_text:
                        print(f"⚠️ Google Flow reported transient server error on Scene {scene_num}. Retrying...")
                        generation_failed = True
                        break

                    if render_started and not has_stop and not has_pct:
                        print(f"✨ Scene {scene_num} render completed in ~{i*3}s! Waiting 8s to settle new card...")
                        flow_page.wait_for_timeout(8000)
                        break

                if generation_failed or not render_started:
                    if not render_started:
                        print(f"⚠️ Scene {scene_num} render did not start. Retrying prompt submission...")
                    else:
                        print("🔄 Reloading Google Flow to clear transient error card...")
                        flow_page.reload()
                        flow_page.wait_for_timeout(6000)
                    continue

                # 4. Trigger download
                print("Triggering direct CDP download...")
                trigger_top_download()

                # 5. Wait for downloaded zip and extract
                downloaded = False
                for dl_try in range(25):
                    flow_page.wait_for_timeout(2000)
                    new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip"))) - before_zips
                    if new_zips:
                        latest_zip = sorted(new_zips, key=os.path.getmtime, reverse=True)[0]
                        try:
                            with zipfile.ZipFile(latest_zip, 'r') as z:
                                for name in z.namelist():
                                    if name.endswith('.mp4'):
                                        extracted = z.extract(name, str(dest_dir))
                                        import hashlib
                                        extracted_hash = hashlib.md5(open(extracted, 'rb').read()).hexdigest()
                                        existing_hashes = {hashlib.md5(open(f, 'rb').read()).hexdigest() for f in dest_dir.glob("scene_*.mp4") if f != dest_file}
                                        if extracted_hash in existing_hashes:
                                            print(f"⚠️ Extracted video is identical to previous scene (MD5: {extracted_hash[:8]}). Waiting for new video...")
                                            os.remove(extracted)
                                            continue
                                        if dest_file.exists():
                                            dest_file.unlink()
                                        os.rename(extracted, str(dest_file))
                                        print(f"✅ Scene {scene_num} saved: {dest_file} ({dest_file.stat().st_size:,} bytes, md5: {extracted_hash[:8]})")
                                        downloaded = True
                                        break
                        except Exception as e:
                            print("Zip reading retry:", e)
                        if downloaded:
                            break
                    elif dl_try in [6, 12, 18]:
                        print("Retrying download click...")
                        trigger_top_download()

                if downloaded:
                    break
            else:
                raise RuntimeError(f"Failed to generate and download Scene {scene_num} after {max_retries} attempts.")

        browser.close()
    print(f"\n🎉 All 7 scenes for track {track_id} generated and saved to {dest_dir}!")

if __name__ == "__main__":
    track = sys.argv[1] if len(sys.argv) > 1 else "-bqKXZW8vFk"
    generate_scenes_for_track(track)
