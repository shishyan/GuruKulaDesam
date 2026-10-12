import time
import json
import urllib.request
import websocket
import base64
import shutil
import zipfile
from pathlib import Path

DEST_DIR = Path("production/google_flow_renders/1hoVaPwWMes")
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_CLIP = DEST_DIR / "scene_03.mp4"

def monitor_scene3():
    print("Connecting to Flow on port 9225 to monitor Scene 3...")
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Set download behavior
    ws.send(json.dumps({
        'id': 1,
        'method': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': str(Path.home() / 'Downloads')}
    }))
    json.loads(ws.recv())

    start_time = time.time()
    for poll in range(60): # up to 5 minutes
        time.sleep(5)
        elapsed = int(time.time() - start_time)

        # Check percentage or stop button
        js_chk = """
        (() => {
            const body = document.body ? document.body.innerText : '';
            const pcts = Array.from(document.querySelectorAll('*'))
                .filter(el => el.children.length === 0 && /^\\d{1,2}%$/.test((el.innerText || '').trim()))
                .map(el => el.innerText.trim());
            const hasStop = Array.from(document.querySelectorAll('button')).some(b => b.innerText === 'Stop' || b.getAttribute('aria-label') === 'Stop');
            return { pcts, hasStop };
        })()
        """
        ws.send(json.dumps({'id': 10 + poll, 'method': 'Runtime.evaluate', 'params': {'expression': js_chk, 'returnByValue': True}}))
        res = json.loads(ws.recv())
        st = res.get('result', {}).get('result', {}).get('value', {})
        pcts = st.get('pcts', [])
        has_stop = st.get('hasStop', False)
        print(f"[{elapsed}s] Stop visible: {has_stop} | Progress: {pcts}")

        if not has_stop and len(pcts) == 0:
            print(f"[{elapsed}s] Generation COMPLETE! Navigating to editor...")
            time.sleep(3)
            
            # Click on the newly generated card (top left card on canvas)
            js_click_new_card = """
            (() => {
                // Find all cards on canvas
                const cards = Array.from(document.querySelectorAll('*')).filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.left > 100 && r.left < 500 && r.top > 60 && r.top < 400 && r.width > 150 && r.height > 100;
                });
                // Sort by top-left
                cards.sort((a, b) => a.getBoundingClientRect().left - b.getBoundingClientRect().left);
                if (cards.length > 0) {
                    const target = cards[0];
                    const r = target.getBoundingClientRect();
                    return { clicked: true, left: r.left, top: r.top, width: r.width, height: r.height };
                }
                return { clicked: false };
            })()
            """
            ws.send(json.dumps({'id': 200, 'method': 'Runtime.evaluate', 'params': {'expression': js_click_new_card, 'returnByValue': True}}))
            res_card = json.loads(ws.recv())
            card_info = res_card.get('result', {}).get('result', {}).get('value', {})
            print("Card info:", card_info)
            if card_info.get('clicked'):
                cx = card_info['left'] + card_info['width'] / 2
                cy = card_info['top'] + card_info['height'] / 2
                ws.send(json.dumps({'id': 201, 'method': 'Input.dispatchMouseEvent', 'params': {'type': 'mousePressed', 'x': cx, 'y': cy, 'button': 'left', 'clickCount': 1}}))
                json.loads(ws.recv())
                ws.send(json.dumps({'id': 202, 'method': 'Input.dispatchMouseEvent', 'params': {'type': 'mouseReleased', 'x': cx, 'y': cy, 'button': 'left', 'clickCount': 1}}))
                json.loads(ws.recv())
                time.sleep(2)

            # Click 'Open video in editor'
            js_open_ed = """
            (() => {
                const btn = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.getAttribute('aria-label') || '').includes('Open video in editor'));
                if (btn) { btn.click(); return true; }
                return false;
            })()
            """
            ws.send(json.dumps({'id': 203, 'method': 'Runtime.evaluate', 'params': {'expression': js_open_ed, 'returnByValue': True}}))
            res_ed = json.loads(ws.recv())
            print("Open in editor:", res_ed.get('result', {}).get('result', {}).get('value'))
            time.sleep(4)

            # Click Download media
            js_dl = """
            (() => {
                const dl = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('download media') || (b.innerText || '').toLowerCase().includes('download media'));
                if (dl) { dl.click(); return true; }
                return false;
            })()
            """
            ws.send(json.dumps({'id': 204, 'method': 'Runtime.evaluate', 'params': {'expression': js_dl, 'returnByValue': True}}))
            res_dl = json.loads(ws.recv())
            print("Download click:", res_dl.get('result', {}).get('result', {}).get('value'))
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
            ws.send(json.dumps({'id': 205, 'method': 'Runtime.evaluate', 'params': {'expression': js_res, 'returnByValue': True}}))
            res_res = json.loads(ws.recv())
            print("Resolution click:", res_res.get('result', {}).get('result', {}).get('value'))

            # Watch Downloads folder for new video
            downloads_dir = Path.home() / "Downloads"
            click_t = time.time() - 5
            found = False
            for _ in range(15):
                time.sleep(1)
                mp4s = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t]
                zips = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t]
                if mp4s:
                    newest = max(mp4s, key=lambda x: x.stat().st_mtime)
                    if newest.stat().st_size > 500_000:
                        shutil.copy2(newest, DEST_CLIP)
                        print(f"[SUCCESS] Downloaded Scene 3: {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                        found = True
                        break
                elif zips:
                    newest = max(zips, key=lambda x: x.stat().st_mtime)
                    with zipfile.ZipFile(newest, "r") as z:
                        names = [n for n in z.namelist() if n.endswith(".mp4")]
                        if names:
                            ext = z.extract(names[0], DEST_DIR)
                            shutil.move(ext, DEST_CLIP)
                            print(f"[SUCCESS] Extracted Scene 3: {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                            found = True
                            break

            # Return to project workspace
            print("Returning back to workspace...")
            ws.send(json.dumps({'id': 206, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.history.back()'}}))
            time.sleep(3)
            break

    ws.close()

if __name__ == '__main__':
    monitor_scene3()
