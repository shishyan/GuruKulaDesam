import urllib.request
import json
import websocket
import time
import shutil
import zipfile
from pathlib import Path

DEST_DIR = Path("production/google_flow_renders/1hoVaPwWMes")
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_CLIP = DEST_DIR / "scene_03.mp4"

def download_last_video():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Click the LAST 'Open video in editor' button in the chat
    print("Clicking the LAST 'Open video in editor' button...")
    js_click_last = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'))
            .filter(b => (b.getAttribute('aria-label') || '').includes('Open video in editor'));
        if (btns.length > 0) {
            const last = btns[btns.length - 1];
            last.scrollIntoView();
            last.click();
            return { clicked: true, count: btns.length, label: last.getAttribute('aria-label') };
        }
        return { clicked: false };
    })()
    """
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_click_last, 'returnByValue': True}}))
    res1 = json.loads(ws.recv())
    print("Click result:", res1.get('result', {}).get('result', {}).get('value'))
    time.sleep(4)

    # Now we are in the editor for the Dandayudhapani video!
    # Click 'Download media'
    print("Clicking 'Download media'...")
    js_dl = """
    (() => {
        const dl = Array.from(document.querySelectorAll('button, [role="button"]'))
            .find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('download media') || (b.innerText || '').toLowerCase().includes('download media'));
        if (dl) { dl.click(); return true; }
        return false;
    })()
    """
    ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_dl, 'returnByValue': True}}))
    res2 = json.loads(ws.recv())
    print("Download click:", res2.get('result', {}).get('result', {}).get('value'))
    time.sleep(2)

    # Select 720p / Original size
    js_res = """
    (() => {
        const resBtn = Array.from(document.querySelectorAll('button, [role="menuitem"]'))
            .find(b => ['original size', '720p', '1080p'].some(w => (b.innerText || '').toLowerCase().includes(w)));
        if (resBtn) { resBtn.click(); return true; }
        return false;
    })()
    """
    ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': js_res, 'returnByValue': True}}))
    res3 = json.loads(ws.recv())
    print("Resolution click:", res3.get('result', {}).get('result', {}).get('value'))

    # Watch Downloads folder
    downloads_dir = Path.home() / "Downloads"
    click_t = time.time() - 4
    for _ in range(15):
        time.sleep(1)
        mp4s = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t]
        zips = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t]
        if mp4s:
            newest = max(mp4s, key=lambda x: x.stat().st_mtime)
            if newest.stat().st_size > 500_000:
                shutil.copy2(newest, DEST_CLIP)
                print(f"[SUCCESS] Downloaded: {newest.name} -> {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                break
        elif zips:
            newest = max(zips, key=lambda x: x.stat().st_mtime)
            with zipfile.ZipFile(newest, "r") as z:
                names = [n for n in z.namelist() if n.endswith(".mp4")]
                if names:
                    ext = z.extract(names[0], DEST_DIR)
                    shutil.move(ext, DEST_CLIP)
                    print(f"[SUCCESS] Extracted: {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                    break

    # Return back to workspace
    print("Returning to workspace...")
    ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.history.back()'}}))
    time.sleep(3)
    ws.close()

if __name__ == '__main__':
    download_last_video()
