import urllib.request
import json
import websocket
import base64
import time
from pathlib import Path
import os
import glob

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

DOWNLOAD_DIR = Path.home() / "Downloads"

def generate_scene(track_id: str, scene_num: int, prompt: str):
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
    flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
    if not flow_tabs:
        raise RuntimeError("No Google Flow tab found!")
    
    ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)
    print(f"\n==========================================")
    print(f"Starting Track: {track_id} | Scene {scene_num}")
    print(f"Prompt: {prompt[:80]}...")
    print(f"==========================================")

    # Allow downloads to ~/Downloads
    ws.send(json.dumps({
        'id': 1,
        'method': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': str(DOWNLOAD_DIR)}
    }))
    ws.recv()

    # Step 1: Count current download buttons / videos
    js_initial = """
    (() => {
        const dls = Array.from(document.querySelectorAll('button, [role="button"]'))
            .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
        return { dlCount: dls.length };
    })()
    """
    ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_initial, 'returnByValue': True}}))
    initial_dls = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', {}).get('dlCount', 0)
    print(f"Initial completed video cards in Flow: {initial_dls}")

    # Snapshot existing files in Downloads
    before_files = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4")))

    # Step 2: Insert prompt into ProseMirror editor
    escaped_prompt = json.dumps(prompt)
    js_insert = f"""
    (() => {{
        const editor = document.querySelector('div.ProseMirror');
        if (!editor) return false;
        editor.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, {escaped_prompt});
        return true;
    }})()
    """
    ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': js_insert, 'returnByValue': True}}))
    inserted = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', False)
    if not inserted:
        raise RuntimeError("Failed to locate or insert prompt into ProseMirror editor")
    
    time.sleep(1)

    # Step 3: Click Submit / Generate button (or press Enter)
    js_submit = """
    (() => {
        // Look for send/arrow_forward button or press Enter
        const buttons = Array.from(document.querySelectorAll('button, [role="button"]'));
        const sendBtn = buttons.find(b => {
            const txt = (b.innerText || '').trim();
            const aria = (b.getAttribute('aria-label') || '').trim();
            return txt === 'arrow_forward' || aria.includes('Submit') || aria.includes('Generate') || txt === 'send';
        });
        if (sendBtn && !sendBtn.disabled) {
            sendBtn.click();
            return 'clicked_button';
        }
        return 'needs_enter';
    })()
    """
    ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': js_submit, 'returnByValue': True}}))
    submit_action = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', '')
    print(f"Submit action: {submit_action}")

    if submit_action == 'needs_enter' or submit_action != 'clicked_button':
        # Dispatch Enter key
        ws.send(json.dumps({
            'id': 5,
            'method': 'Input.dispatchKeyEvent',
            'params': {'type': 'rawKeyDown', 'windowsVirtualKeyCode': 13, 'unmodifiedText': '\r', 'text': '\r'}
        }))
        ws.recv()
        ws.send(json.dumps({
            'id': 6,
            'method': 'Input.dispatchKeyEvent',
            'params': {'type': 'keyUp', 'windowsVirtualKeyCode': 13}
        }))
        ws.recv()
        print("Dispatched Enter key to submit.")

    # Step 4: Poll generation until complete
    print("Waiting for Veo 3.1 - Lite to generate video (typically ~35-45s)...")
    start_time = time.time()
    generation_started = False
    
    for i in range(40): # max 200s
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
            return {
                isStop,
                dlCount: dls.length,
                pcts
            };
        })()
        """
        ws.send(json.dumps({'id': 100 + i, 'method': 'Runtime.evaluate', 'params': {'expression': js_poll, 'returnByValue': True}}))
        st = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', {})
        
        is_stop = st.get('isStop', False)
        current_dls = st.get('dlCount', 0)
        pcts = st.get('pcts', [])
        
        if is_stop or pcts:
            generation_started = True

        print(f"[{elapsed}s] Active render: {is_stop} | Progress: {pcts} | Cards: {current_dls}")

        # Check if generation finished (new card added or stopped generating with >= 1 new card)
        if (generation_started and not is_stop and current_dls > initial_dls) or (current_dls > initial_dls):
            print(f"✨ Scene {scene_num} generation finished! New card detected ({current_dls} vs {initial_dls}).")
            time.sleep(2)
            break
    else:
        print("Warning: Wait loop timed out or count didn't increment. Checking download buttons...")

    # Step 5: Click Download on the latest video card
    js_click_latest_dl = """
    (() => {
        const dls = Array.from(document.querySelectorAll('button, [role="button"]'))
            .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
        if (dls.length > 0) {
            const target = dls[dls.length - 1]; // latest card
            target.scrollIntoView();
            target.click();
            return { success: true, count: dls.length };
        }
        return { success: false };
    })()
    """
    ws.send(json.dumps({'id': 300, 'method': 'Runtime.evaluate', 'params': {'expression': js_click_latest_dl, 'returnByValue': True}}))
    dl_res = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', {})
    print("Clicked download button:", dl_res)
    time.sleep(2)

    # Check for resolution menu popup (e.g. Original / 720p / 1080p)
    js_select_res = """
    (() => {
        const items = Array.from(document.querySelectorAll('button, [role="menuitem"], div[role="menuitem"]'));
        const opt = items.find(el => {
            const t = (el.innerText || '').toLowerCase();
            return t.includes('original') || t.includes('720p') || t.includes('1080p');
        });
        if (opt) {
            opt.click();
            return { clicked: true, text: opt.innerText };
        }
        return { clicked: false };
    })()
    """
    ws.send(json.dumps({'id': 301, 'method': 'Runtime.evaluate', 'params': {'expression': js_select_res, 'returnByValue': True}}))
    res_select = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value', {})
    if res_select.get('clicked'):
        print("Selected resolution option:", res_select.get('text'))

    # Step 6: Wait for file in Downloads folder
    print("Waiting for file download to complete...")
    downloaded_file = None
    for _ in range(30):
        time.sleep(2)
        after_files = set(glob.glob(str(DOWNLOAD_DIR / "*.mp4")))
        new_files = after_files - before_files
        # Also check for .crdownload
        cr_files = glob.glob(str(DOWNLOAD_DIR / "*.crdownload"))
        if new_files and not cr_files:
            downloaded_file = list(new_files)[0]
            break
        elif new_files:
            # File exists but still downloading
            continue

    if not downloaded_file:
        # Check most recently modified mp4 in Downloads
        all_mp4s = sorted(glob.glob(str(DOWNLOAD_DIR / "*.mp4")), key=os.path.getmtime, reverse=True)
        if all_mp4s and (time.time() - os.path.getmtime(all_mp4s[0])) < 120:
            downloaded_file = all_mp4s[0]

    if not downloaded_file:
        print("ERROR: Could not detect newly downloaded mp4 file!")
        ws.close()
        return None

    dest_dir = Path("production/google_flow_renders") / track_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / f"scene_{scene_num:02d}.mp4"

    # Move/copy file to target
    import shutil
    shutil.copy2(downloaded_file, str(dest_path))
    size = os.path.getsize(dest_path)
    print(f"✅ Scene {scene_num} saved successfully to {dest_path} ({size:,} bytes)")

    ws.close()
    return dest_path

if __name__ == "__main__":
    import sys
    track = sys.argv[1] if len(sys.argv) > 1 else "--4jzoezBW8"
    scene = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    
    with open("production/colab_handoff/pending_7scenes_batch_prompts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    track_data = next((t for t in data["tracks"] if t["track_id"] == track), None)
    if not track_data:
        print(f"Track {track} not found in prompts json!")
        sys.exit(1)
        
    scene_data = next((s for s in track_data["scenes"] if s["scene_num"] == scene), None)
    if not scene_data:
        print(f"Scene {scene} not found for track {track}!")
        sys.exit(1)
        
    generate_scene(track, scene, scene_data["prompt"])
