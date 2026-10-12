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
                print("Render complete! Allowing 5s to finalize...")
                page.wait_for_timeout(5000)
                break
            page.wait_for_timeout(4000)

        browser.close()

if __name__ == "__main__":
    with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    track_data = next(t for t in data["tracks"] if t["track_id"] == "-cmB2_XZqs0")
    s7 = next(s for s in track_data["scenes"] if s["scene_num"] == 7)
    render_and_download("-cmB2_XZqs0", 7, s7["prompt"])
