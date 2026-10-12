import time
import json
import os
import glob
import shutil
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
import io
import urllib.request
import websocket

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

DOWNLOAD_DIR = Path.home() / "Downloads"

def generate_track_scenes(track_id: str):
    with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    track_entry = next((t for t in data["tracks"] if t["track_id"] == track_id), None)
    if not track_entry:
        raise ValueError(f"Track {track_id} not found in prompts json!")

    dest_dir = Path("production/google_flow_renders") / track_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"🎬 Processing 7 Consecrated Scenes for Track: {track_id}")
    print(f"Title: {track_entry.get('title')}")
    print(f"=======================================================")

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

            if dest_file.exists() and dest_file.stat().st_size > 100_000:
                print(f"⏩ Scene {scene_num} already exists ({dest_file.stat().st_size:,} bytes). Skipping.")
                continue

            print(f"\n--- [Track {track_id}] Generating Scene {scene_num}/7 ---")
            print(f"Prompt: {prompt[:80]}...")

            before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
            before_mp4s = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4")))

            # 1. Focus ProseMirror editor and insert prompt
            editor = flow_page.locator("div.ProseMirror").first
            editor.click()
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

            # 2. Click generate / submit
            submit_btn = flow_page.locator("button.generate-icon-button, button[aria-label*='Start generation' i]").first
            if submit_btn.is_visible() and submit_btn.is_enabled():
                submit_btn.click()
            else:
                editor.focus()
                flow_page.keyboard.press("Enter")

            flow_page.wait_for_timeout(3000)

            # 3. Wait for render to finish
            print(f"Waiting for Scene {scene_num} to start and complete render...")
            render_started = False
            for i in range(40):
                body_text = flow_page.locator("body").inner_text()
                has_stop = "Stop" in body_text
                has_pct = any(p in body_text for p in ["%", "100%"])
                if has_stop or has_pct:
                    render_started = True
                if render_started and not has_stop:
                    # Give it 5 seconds to finalize video file encoding
                    flow_page.wait_for_timeout(5000)
                    print(f"✨ Scene {scene_num} render completed in ~{i*3}s!")
                    break
                flow_page.wait_for_timeout(3000)

            # 4. Trigger download via direct CDP
            tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
            f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
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

            # 5. Wait for downloaded file and save as clean MP4
            downloaded = False
            for _ in range(30):
                flow_page.wait_for_timeout(2000)
                new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
                new_mp4s = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4"))) - before_mp4s

                recent_zips = [z for z in new_zips if (time.time() - os.path.getmtime(z)) < 90]
                if recent_zips:
                    latest_zip = sorted(recent_zips, key=os.path.getmtime, reverse=True)[0]
                    try:
                        with zipfile.ZipFile(latest_zip, 'r') as z:
                            for name in z.namelist():
                                if name.endswith('.mp4'):
                                    extracted = z.extract(name, str(dest_dir))
                                    if dest_file.exists():
                                        dest_file.unlink()
                                    os.rename(extracted, str(dest_file))
                                    print(f"✅ Scene {scene_num} saved from zip: {dest_file} ({dest_file.stat().st_size:,} bytes)")
                                    downloaded = True
                                    break
                    except Exception:
                        pass
                    if downloaded:
                        break

                recent_mp4s = [m for m in new_mp4s if (time.time() - os.path.getmtime(m)) < 90]
                if recent_mp4s:
                    latest_mp4 = sorted(recent_mp4s, key=os.path.getmtime, reverse=True)[0]
                    if dest_file.exists():
                        dest_file.unlink()
                    shutil.copy2(latest_mp4, str(dest_file))
                    print(f"✅ Scene {scene_num} saved directly: {dest_file} ({dest_file.stat().st_size:,} bytes)")
                    downloaded = True
                    break

            if not downloaded:
                raise RuntimeError(f"Failed to capture download for Scene {scene_num}")

        browser.close()
    print(f"\n🎉 All 7 scenes for track {track_id} generated and saved to {dest_dir}!")

if __name__ == "__main__":
    import sys
    track = sys.argv[1] if len(sys.argv) > 1 else "-7ppYdnUdVk"
    generate_track_scenes(track)
