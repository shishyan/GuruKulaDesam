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

DOWNLOAD_DIR = Path.home() / "Downloads"

def render_and_download(track_id: str, scene_num: int, prompt: str):
    print(f"\n{'='*65}")
    print(f"[Google Flow] Generating Track {track_id} | Consecrated Scene {scene_num}/7")
    print(f"Prompt: {prompt[:90]}...")
    print(f"{'='*65}")

    out_dir = Path("production/google_flow_renders") / track_id
    out_dir.mkdir(parents=True, exist_ok=True)
    dst_mp4 = out_dir / f"scene_{scene_num:02d}.mp4"

    if dst_mp4.exists() and dst_mp4.stat().st_size > 1000000:
        print(f"Scene {scene_num} already exists ({dst_mp4.stat().st_size:,} bytes). Skipping.")
        return

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        flow_tabs = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url]
        if not flow_tabs:
            raise RuntimeError("No Google Flow project tab found!")
        
        page = flow_tabs[0]
        page.bring_to_front()

        before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))

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

        submit_btn = page.locator("button.generate-icon-button, button[aria-label*='Start generation' i], button:has-text('arrow_forward')").first
        if submit_btn.is_visible() and submit_btn.is_enabled():
            submit_btn.click()
        else:
            editor.focus()
            page.keyboard.press("Enter")

        page.wait_for_timeout(4000)

        print("Waiting for Veo 3.1 render...")
        render_started = False
        for i in range(40):
            body_text = page.locator("body").inner_text()
            has_stop = "Stop" in body_text
            if has_stop:
                render_started = True
            print(f"[{i*4:3d}s] Stop visible: {has_stop}")
            if render_started and not has_stop:
                print("Render complete! Allowing 4s to finalize...")
                page.wait_for_timeout(4000)
                break
            page.wait_for_timeout(4000)

        browser.close()

    # Trigger download via direct CDP
    print("Triggering direct CDP download...")
    time.sleep(2)
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

    # Wait for zip and extract
    print("Waiting for downloaded zip...")
    for _ in range(30):
        time.sleep(2)
        new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip"))) - before_zips
        if new_zips:
            latest_zip = sorted(new_zips, key=os.path.getmtime, reverse=True)[0]
            try:
                with zipfile.ZipFile(latest_zip, 'r') as z:
                    for name in z.namelist():
                        if name.endswith('.mp4'):
                            extracted = z.extract(name, str(out_dir))
                            if dst_mp4.exists():
                                dst_mp4.unlink()
                            os.rename(extracted, str(dst_mp4))
                            print(f"✅ Successfully saved {dst_mp4.name} ({dst_mp4.stat().st_size:,} bytes)")
                            return
            except Exception as e:
                print("Zip read error, retrying:", e)

    raise RuntimeError(f"Download failed for Scene {scene_num}")

if __name__ == "__main__":
    with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    track_data = next(t for t in data["tracks"] if t["track_id"] == "-cmB2_XZqs0")
    s6 = next(s for s in track_data["scenes"] if s["scene_num"] == 6)
    render_and_download("-cmB2_XZqs0", 6, s6["prompt"])
