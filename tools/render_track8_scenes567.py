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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
        print("CDP download error:", e)
        return False

def render_scenes(track_id: str, scene_nums: list[int]):
    with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    track_entry = next(t for t in data["tracks"] if t["track_id"] == track_id)
    dest_dir = Path("production/google_flow_renders") / track_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        flow_page = next(page for page in ctx.pages if "flow.google.com" in page.url)

        for num in scene_nums:
            dest_file = dest_dir / f"scene_{num:02d}.mp4"
            if dest_file.exists() and dest_file.stat().st_size > 1_000_000:
                print(f"⏩ Scene {num} already exists ({dest_file.stat().st_size:,} bytes). Skipping.")
                continue

            scene_obj = next(s for s in track_entry["scenes"] if s["scene_num"] == num)
            prompt = scene_obj["prompt"]

            print(f"\n{'='*65}")
            print(f"[Track {track_id}] Rendering Consecrated Scene {num}/7")
            print(f"Prompt: {prompt[:85]}...")
            print(f"{'='*65}")

            before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))

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

            submit_btn = flow_page.locator("button.generate-icon-button, button[aria-label*='Start generation' i], button:has-text('arrow_forward')").first
            if submit_btn.is_visible() and submit_btn.is_enabled():
                submit_btn.click()
            else:
                editor.focus()
                flow_page.keyboard.press("Enter")

            flow_page.wait_for_timeout(4000)

            print(f"Waiting for Scene {num} render...")
            render_started = False
            for i in range(50):
                body_text = flow_page.locator("body").inner_text()
                has_stop = "Stop" in body_text
                if has_stop:
                    render_started = True
                if render_started and not has_stop:
                    print(f"✨ Scene {num} completed in ~{i*4}s! Waiting 6s to finalize...")
                    flow_page.wait_for_timeout(6000)
                    break
                flow_page.wait_for_timeout(4000)

            print("Triggering download on topmost card...")
            trigger_top_download()

            downloaded = False
            for attempt in range(25):
                flow_page.wait_for_timeout(2000)
                new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip"))) - before_zips
                if new_zips:
                    latest_zip = sorted(new_zips, key=os.path.getmtime, reverse=True)[0]
                    try:
                        with zipfile.ZipFile(latest_zip, 'r') as z:
                            for name in z.namelist():
                                if name.endswith('.mp4'):
                                    extracted = z.extract(name, str(dest_dir))
                                    if dest_file.exists():
                                        dest_file.unlink()
                                    os.rename(extracted, str(dest_file))
                                    print(f"✅ Scene {num} saved: {dest_file} ({dest_file.stat().st_size:,} bytes)")
                                    downloaded = True
                                    break
                    except Exception as e:
                        print("Zip read retry:", e)
                    if downloaded:
                        break
                elif attempt in [6, 12, 18]:
                    print("Retrying download click...")
                    trigger_top_download()

            if not downloaded:
                raise RuntimeError(f"Download failed for Scene {num}")

        browser.close()
    print(f"\n🎉 Scenes {scene_nums} complete!")

if __name__ == "__main__":
    render_scenes("-bqKXZW8vFk", [5, 6, 7])
