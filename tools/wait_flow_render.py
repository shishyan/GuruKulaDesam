import urllib.request
import json
import websocket
import base64
import time
from pathlib import Path

DEST_DIR = Path("production/google_flow_renders/1hoVaPwWMes")
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_CLIP = DEST_DIR / "scene_01.mp4"

def wait_render():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    print("Monitoring Veo generation on Google Flow...")
    start_time = time.time()
    
    # Configure download path
    ws.send(json.dumps({
        'id': 100,
        'method': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': str(Path.home() / 'Downloads')}
    }))
    json.loads(ws.recv())

    for poll in range(60): # up to 5 minutes
        time.sleep(5)
        elapsed = int(time.time() - start_time)

        # Evaluate state: check stop button, video elements, download buttons, text
        js_status = """
        (() => {
            const body = document.body ? document.body.innerText : '';
            const isStopVisible = !!Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Stop') || b.getAttribute('aria-label') === 'Stop');
            const videos = Array.from(document.querySelectorAll('video')).map(v => ({ src: v.src, currentSrc: v.currentSrc }));
            const dlButtons = Array.from(document.querySelectorAll('button, [role="button"]'))
                .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'))
                .map(b => ({ label: b.getAttribute('aria-label') || b.innerText }));
            const pcts = Array.from(document.querySelectorAll('*'))
                .filter(el => el.children.length === 0 && /^\\d{1,2}%$/.test((el.innerText || '').trim()))
                .map(el => el.innerText.trim());
            return {
                isStopVisible,
                videosCount: videos.length,
                dlButtons,
                pcts,
                snippet: body.slice(body.length - 400)
            };
        })()
        """
        ws.send(json.dumps({'id': 10 + poll, 'method': 'Runtime.evaluate', 'params': {'expression': js_status, 'returnByValue': True}}))
        res = json.loads(ws.recv())
        st = res.get('result', {}).get('result', {}).get('value', {})
        
        print(f"[{elapsed}s] Generating: {st.get('isStopVisible')} | Pct: {st.get('pcts')} | Videos: {st.get('videosCount')} | DL: {st.get('dlButtons')}")

        # If download buttons appear or videos appear and generation stopped
        if not st.get('isStopVisible') and (st.get('dlButtons') or st.get('videosCount', 0) > 0):
            print(f"[{elapsed}s] VIDEO GENERATION COMPLETE! Taking screenshot...")
            ws.send(json.dumps({'id': 500, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
            res_shot = json.loads(ws.recv())
            img_b64 = res_shot.get('result', {}).get('data', '')
            shot_path = 'C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_video_complete.png'
            with open(shot_path, 'wb') as f:
                f.write(base64.b64decode(img_b64))
            print("Saved screenshot to", shot_path)
            
            # Click download button
            js_dl = """
            (() => {
                const dlBtn = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
                if (dlBtn) {
                    dlBtn.click();
                    return { clicked: true, label: dlBtn.getAttribute('aria-label') || dlBtn.innerText };
                }
                return { clicked: false };
            })()
            """
            ws.send(json.dumps({'id': 501, 'method': 'Runtime.evaluate', 'params': {'expression': js_dl, 'returnByValue': True}}))
            res_dl = json.loads(ws.recv())
            print("Download button click:", res_dl.get('result', {}).get('result', {}).get('value'))
            time.sleep(3)

            # Check for resolution menu (720p / Original / 1080p)
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
            ws.send(json.dumps({'id': 502, 'method': 'Runtime.evaluate', 'params': {'expression': js_res, 'returnByValue': True}}))
            res_res = json.loads(ws.recv())
            print("Resolution click:", res_res.get('result', {}).get('result', {}).get('value'))
            
            # Watch Downloads folder for new video
            downloads_dir = Path.home() / "Downloads"
            click_time = time.time() - 5
            for _ in range(15):
                time.sleep(1)
                mp4s = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_time]
                zips = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_time]
                if mp4s:
                    newest = max(mp4s, key=lambda x: x.stat().st_mtime)
                    if newest.stat().st_size > 500_000:
                        import shutil
                        shutil.copy2(newest, DEST_CLIP)
                        print(f"[SUCCESS] Downloaded and saved video to: {DEST_CLIP} ({DEST_CLIP.stat().st_size} bytes)")
                        break
                elif zips:
                    import zipfile, shutil
                    newest = max(zips, key=lambda x: x.stat().st_mtime)
                    with zipfile.ZipFile(newest, "r") as z:
                        mp4_names = [m for m in z.namelist() if m.endswith(".mp4")]
                        if mp4_names:
                            ext = z.extract(mp4_names[0], DEST_DIR)
                            shutil.move(ext, DEST_CLIP)
                            print(f"[SUCCESS] Extracted zip to: {DEST_CLIP} ({DEST_CLIP.stat().st_size} bytes)")
                            break
            break

    ws.close()

if __name__ == '__main__':
    wait_render()
