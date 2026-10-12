import urllib.request
import json
import websocket
import time
import os
import glob
import zipfile
import shutil
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

DOWNLOAD_DIR = Path.home() / "Downloads"

def generate_and_save(track_id: str, scene_num: int, prompt: str):
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
    flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
    if not flow_tabs:
        raise RuntimeError("No Google Flow tab found on port 9222!")
    
    ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)
    print(f"\n==================================================")
    print(f"🎬 Generating Track {track_id} | Consecrated Scene {scene_num}/7")
    print(f"Prompt: {prompt[:90]}...")
    print(f"==================================================")

    # 1. Allow download to Downloads dir
    ws.send(json.dumps({
        'id': 1,
        'method': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': str(DOWNLOAD_DIR)}
    }))
    ws.recv()

    # 2. Check initial download count
    js_count = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const dls = btns.filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
        return dls.length;
    })()
    """
    ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_count, 'returnByValue': True}}))
    initial_dls = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', 0)
    print(f"Initial completed cards in Flow: {initial_dls}")

    # Snapshot existing zips in Downloads
    before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))

    # 3. Enter prompt into ProseMirror editor
    escaped = json.dumps(prompt)
    js_enter = f"""
    (() => {{
        const editor = document.querySelector('div.ProseMirror');
        if (!editor) return false;
        editor.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, {escaped});
        return true;
    }})()
    """
    ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': js_enter, 'returnByValue': True}}))
    ok = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', False)
    if not ok:
        ws.close()
        raise RuntimeError("Could not find or populate ProseMirror editor")
    time.sleep(1)

    # 4. Click Submit / Generate button
    js_submit = """
    (() => {
        const buttons = Array.from(document.querySelectorAll('button, [role="button"]'));
        const sendBtn = buttons.find(b => {
            const txt = (b.innerText || '').trim();
            const aria = (b.getAttribute('aria-label') || '').trim();
            return txt === 'arrow_forward' || aria.includes('Submit') || aria.includes('Generate') || txt === 'send';
        });
        if (sendBtn && !sendBtn.disabled) {
            sendBtn.click();
            return 'clicked';
        }
        return 'not_found';
    })()
    """
    ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': js_submit, 'returnByValue': True}}))
    sub_res = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', '')
    if sub_res != 'clicked':
        # Fallback to Enter key
        ws.send(json.dumps({'id': 5, 'method': 'Input.dispatchKeyEvent', 'params': {'type': 'rawKeyDown', 'windowsVirtualKeyCode': 13, 'unmodifiedText': '\r', 'text': '\r'}}))
        ws.recv()
        ws.send(json.dumps({'id': 6, 'method': 'Input.dispatchKeyEvent', 'params': {'type': 'keyUp', 'windowsVirtualKeyCode': 13}}))
        ws.recv()
        print("Submitted prompt via Enter key")
    else:
        print("Submitted prompt via Generate button")

    # 5. Poll generation until finished
    start_time = time.time()
    generated = False
    for step in range(50): # up to 250s
        time.sleep(5)
        elapsed = int(time.time() - start_time)
        js_poll = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            const isStop = !!btns.find(b => (b.innerText || '').toLowerCase().includes('stop') || (b.getAttribute('aria-label') || '').toLowerCase().includes('stop'));
            const dls = btns.filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
            const pcts = Array.from(document.querySelectorAll('*'))
                .filter(el => el.children.length === 0 && /^\\d{1,2}%$/.test((el.innerText || '').trim()))
                .map(el => el.innerText.trim());
            return { isStop, dlCount: dls.length, pcts };
        })()
        """
        ws.send(json.dumps({'id': 100 + step, 'method': 'Runtime.evaluate', 'params': {'expression': js_poll, 'returnByValue': True}}))
        st = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', {})
        is_stop = st.get('isStop', False)
        current_dls = st.get('dlCount', 0)
        pcts = st.get('pcts', [])
        
        print(f"[{elapsed:3d}s] Veo 3.1 rendering... StopBtn: {is_stop} | Progress: {pcts} | Cards: {current_dls}")

        if (not is_stop and not pcts and current_dls > initial_dls) or (step > 4 and current_dls > initial_dls and not is_stop):
            print(f"✨ Card finished rendering ({current_dls} cards total)!")
            generated = True
            time.sleep(3)
            break

    if not generated:
        print("Warning: Render timed out or dlCount did not increment. Attempting download on top card anyway...")

    # 6. Click top download button
    js_dl = """
    (() => {
        const dls = Array.from(document.querySelectorAll('button, [role="button"]'))
            .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
        if (dls.length > 0) {
            dls[0].scrollIntoView();
            dls[0].click();
            return { clicked: true, count: dls.length };
        }
        return { clicked: false };
    })()
    """
    ws.send(json.dumps({'id': 200, 'method': 'Runtime.evaluate', 'params': {'expression': js_dl, 'returnByValue': True}}))
    dl_val = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', {})
    print("Download click result:", dl_val)
    time.sleep(2)

    # 7. Click menu resolution (Original / 720p / 1080p) if menu appeared
    js_menu = """
    (() => {
        const items = Array.from(document.querySelectorAll('button, [role="menuitem"], div[role="menuitem"]'));
        const matches = items.filter(el => {
            const t = (el.innerText || '').toLowerCase();
            return t.includes('original') || t.includes('720p') || t.includes('1080p');
        });
        if (matches.length > 0) {
            matches[0].click();
            return { clicked: true, text: matches[0].innerText };
        }
        return { clicked: false };
    })()
    """
    ws.send(json.dumps({'id': 201, 'method': 'Runtime.evaluate', 'params': {'expression': js_menu, 'returnByValue': True}}))
    menu_val = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', {})
    print("Resolution menu selection:", menu_val)

    # 8. Wait for new .zip to appear in Downloads
    print("Waiting for download to finish in ~/Downloads...")
    new_zip = None
    for _ in range(40):
        time.sleep(2)
        after_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))
        diff = after_zips - before_zips
        # also check for .crdownload
        cr = glob.glob(str(DOWNLOAD_DIR / "*.crdownload"))
        if diff and not cr:
            # Pick the most recent
            new_zip = sorted(list(diff), key=os.path.getmtime, reverse=True)[0]
            break

    if not new_zip:
        # Fallback to newest zip in Downloads if modified recently
        zips = sorted(glob.glob(str(DOWNLOAD_DIR / "*.zip")), key=os.path.getmtime, reverse=True)
        if zips and (time.time() - os.path.getmtime(zips[0]) < 120):
            new_zip = zips[0]

    if not new_zip:
        ws.close()
        raise RuntimeError("No downloaded zip found!")

    print(f"📦 Downloaded zip archive: {new_zip} ({os.path.getsize(new_zip):,} bytes)")

    # 9. Extract internal mp4 to destination
    out_dir = Path("C:/GitHub/Gurukuladesam/production/google_flow_renders") / track_id
    out_dir.mkdir(parents=True, exist_ok=True)
    dst_mp4 = out_dir / f"scene_{scene_num:02d}.mp4"

    with zipfile.ZipFile(new_zip, 'r') as z:
        mp4_names = [n for n in z.namelist() if n.lower().endswith('.mp4')]
        if not mp4_names:
            ws.close()
            raise RuntimeError(f"No MP4 inside zip: {z.namelist()}")
        extracted_path = z.extract(mp4_names[0], out_dir)
        shutil.move(extracted_path, dst_mp4)

    print(f"✅ Consecrated scene {scene_num} saved: {dst_mp4} ({dst_mp4.stat().st_size:,} bytes)")
    ws.close()
    return dst_mp4

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--track', required=True)
    parser.add_argument('--scene', type=int, required=True)
    parser.add_argument('--prompt', required=True)
    args = parser.parse_args()

    generate_and_save(args.track, args.scene, args.prompt)
