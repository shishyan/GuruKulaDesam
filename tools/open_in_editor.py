import urllib.request
import json
import websocket
import base64
import time
from pathlib import Path

def open_editor():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Click 'Open video in editor'
    js = """
    (() => {
        const btn = Array.from(document.querySelectorAll('button, [role="button"]'))
            .find(b => (b.getAttribute('aria-label') || '').includes('Open video in editor') || (b.innerText || '').includes('Open video in editor'));
        if (btn) {
            btn.click();
            return { clicked: true, label: btn.getAttribute('aria-label') };
        }
        return { clicked: false };
    })()
    """
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
    res = json.loads(ws.recv())
    print("Click result:", res.get('result', {}).get('result', {}).get('value'))

    time.sleep(4)

    # Take screenshot of the editor
    ws.send(json.dumps({'id': 2, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
    res_shot = json.loads(ws.recv())
    shot_path = 'C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_editor_view.png'
    with open(shot_path, 'wb') as f:
        f.write(base64.b64decode(res_shot.get('result', {}).get('data', '')))
    print("Saved screenshot to", shot_path)

    # Check for download button inside the editor
    js_buttons = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'))
            .map(b => b.getAttribute('aria-label') || b.innerText)
            .filter(Boolean);
        return btns;
    })()
    """
    ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': js_buttons, 'returnByValue': True}}))
    res_btns = json.loads(ws.recv())
    print("Buttons in editor view:", res_btns.get('result', {}).get('result', {}).get('value', []))

    # Also check if Download media is present and click it
    js_dl = """
    (() => {
        const dl = Array.from(document.querySelectorAll('button, [role="button"]'))
            .find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('download') || (b.innerText || '').toLowerCase().includes('download'));
        if (dl) {
            dl.click();
            return { clicked: true, label: dl.getAttribute('aria-label') || dl.innerText };
        }
        return { clicked: false };
    })()
    """
    ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': js_dl, 'returnByValue': True}}))
    res_dl = json.loads(ws.recv())
    print("Download button click:", res_dl.get('result', {}).get('result', {}).get('value'))

    time.sleep(2)
    # Check for resolution menu
    js_res = """
    (() => {
        const resBtn = Array.from(document.querySelectorAll('button, [role="menuitem"]'))
            .find(b => ['original size', '720p', '1080p'].some(w => (b.innerText || '').toLowerCase().includes(w)));
        if (resBtn) {
            resBtn.click();
            return { clicked: true, label: resBtn.innerText };
        }
        return { clicked: false };
    })()
    """
    ws.send(json.dumps({'id': 5, 'method': 'Runtime.evaluate', 'params': {'expression': js_res, 'returnByValue': True}}))
    res_res = json.loads(ws.recv())
    print("Resolution click:", res_res.get('result', {}).get('result', {}).get('value'))

    # Check downloads folder
    downloads_dir = Path.home() / "Downloads"
    click_t = time.time() - 5
    for _ in range(10):
        time.sleep(1)
        recent_mp4 = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t]
        recent_zip = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t]
        if recent_mp4 or recent_zip:
            target = recent_mp4[0] if recent_mp4 else recent_zip[0]
            print(f"Detected downloaded file: {target.name} ({target.stat().st_size} bytes)")
            dest_clip = Path("production/google_flow_renders/1hoVaPwWMes/scene_01.mp4")
            if target.suffix == ".mp4":
                import shutil
                shutil.copy2(target, dest_clip)
                print(f"[SUCCESS] Saved to {dest_clip}")
            elif target.suffix == ".zip":
                import zipfile, shutil
                with zipfile.ZipFile(target, "r") as z:
                    names = [n for n in z.namelist() if n.endswith(".mp4")]
                    if names:
                        extracted = z.extract(names[0], dest_clip.parent)
                        shutil.move(extracted, dest_clip)
                        print(f"[SUCCESS] Extracted zip to {dest_clip}")
            break

    ws.close()

if __name__ == '__main__':
    open_editor()
