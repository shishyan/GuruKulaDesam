import os
import sys
import time
import json
import urllib.request
import websocket
import base64
import shutil
import zipfile
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import parse_blueprint, ensure_audio, build_master_film, RENDERS_DIR, FLOW_RENDERS_DIR, PROMPTS_DIR

CDP_PORT = 9225

def get_flow_tab():
    try:
        tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{CDP_PORT}/json/list').read())
    except Exception as e:
        print(f"[CDP Error] Could not connect to Chrome on port {CDP_PORT}: {e}")
        return None
    flow_tabs = [t for t in tabs if 'flow.google.com' in t.get('url', '')]
    if not flow_tabs:
        print("[CDP Error] No active Google Flow tab found on port", CDP_PORT)
        return None
    return flow_tabs[0]

def connect_ws():
    tab = get_flow_tab()
    if not tab:
        return None
    ws = websocket.create_connection(tab['webSocketDebuggerUrl'], suppress_origin=True)
    # Ensure automated downloads
    ws.send(json.dumps({
        'id': 1,
        'method': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': str(Path.home() / 'Downloads')}
    }))
    json.loads(ws.recv())
    return ws

def eval_js(ws, js_code, req_id=2):
    ws.send(json.dumps({
        'id': req_id,
        'method': 'Runtime.evaluate',
        'params': {'expression': js_code, 'returnByValue': True}
    }))
    res = json.loads(ws.recv())
    return res.get('result', {}).get('result', {}).get('value')

def ensure_project_workspace(ws):
    """Ensures we are in a project or navigates to new project."""
    tab = get_flow_tab()
    url = tab.get('url', '') if tab else ''
    if '/project/' not in url:
        print("[Flow] Opening new project...")
        js_new = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button, [role="button"]'))
                .find(b => (b.innerText || '').includes('New project'));
            if (btn) { btn.click(); return true; }
            return false;
        })()
        """
        eval_js(ws, js_new)
        time.sleep(4)

def submit_prompt(ws, prompt_text):
    print(f"[Flow] Submitting prompt ({len(prompt_text)} chars)...")
    # Clean up and focus ProseMirror
    js_type = f"""
    (() => {{
        const el = document.querySelector('div.ProseMirror');
        if (!el) return false;
        el.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, {json.dumps(prompt_text)});
        return true;
    }})()
    """
    ok = eval_js(ws, js_type, req_id=20)
    if not ok:
        print("[Flow Error] Could not find ProseMirror editor!")
        return False

    time.sleep(1)

    # Click submit button
    js_submit = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const sendBtn = btns.find(b => (b.innerText || '').includes('arrow_forward') || (b.getAttribute('aria-label') || '').toLowerCase().includes('send') || (b.getAttribute('aria-label') || '').toLowerCase().includes('generate'));
        if (sendBtn) {
            sendBtn.click();
            return 'CLICKED_SEND';
        }
        return 'BUTTON_NOT_FOUND';
    })()
    """
    res = eval_js(ws, js_submit, req_id=21)
    print(f"[Flow] Submit button status: {res}")
    time.sleep(3)
    return True

def handle_approvals_and_wait(ws, dest_mp4_path: Path, max_wait_sec=240):
    print(f"[Flow] Monitoring render pipeline for {dest_mp4_path.name} (timeout {max_wait_sec}s)...")
    start_time = time.time()
    approved = False

    while time.time() - start_time < max_wait_sec:
        time.sleep(4)
        elapsed = int(time.time() - start_time)

        # Check for approval options
        if not approved:
            js_appr = """
            (() => {
                const optionRows = Array.from(document.querySelectorAll('.choice-container .option-row, flow-permission-message .option-row, .option-row'));
                const target = optionRows.find(el => el.textContent.includes('Always approve')) || optionRows.find(el => el.textContent.includes('Approve'));
                if (target) {
                    target.scrollIntoView();
                    target.click();
                    const span = target.querySelector('.option-label, span');
                    if (span) span.click();
                    return { clicked: true, text: target.textContent.trim() };
                }
                return { clicked: false };
            })()
            """
            res_appr = eval_js(ws, js_appr, req_id=30)
            if res_appr and res_appr.get('clicked'):
                approved = True
                print(f"[{elapsed}s] Credit deduction approved: '{res_appr.get('text')}'!")
                time.sleep(3)

        # Check if 'Open video in editor' or download buttons are present
        js_status = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            const editorBtn = btns.find(b => (b.getAttribute('aria-label') || '').includes('Open video in editor'));
            const dlBtn = btns.find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('download media') || (b.innerText || '').toLowerCase().includes('download media'));
            const isStop = btns.some(b => (b.innerText || '') === 'Stop' || (b.getAttribute('aria-label') || '') === 'Stop');
            return {
                hasEditorBtn: !!editorBtn,
                hasDlBtn: !!dlBtn,
                isStop
            };
        })()
        """
        st = eval_js(ws, js_status, req_id=31) or {}
        
        if st.get('hasEditorBtn'):
            print(f"[{elapsed}s] Video generation complete! Clicking 'Open video in editor'...")
            js_click_ed = """
            (() => {
                const btn = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.getAttribute('aria-label') || '').includes('Open video in editor'));
                if (btn) { btn.click(); return true; }
                return false;
            })()
            """
            eval_js(ws, js_click_ed, req_id=32)
            time.sleep(4)

        if st.get('hasDlBtn'):
            print(f"[{elapsed}s] In editor! Triggering download...")
            js_click_dl = """
            (() => {
                const dl = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('download media') || (b.innerText || '').toLowerCase().includes('download media'));
                if (dl) { dl.click(); return true; }
                return false;
            })()
            """
            eval_js(ws, js_click_dl, req_id=33)
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
            eval_js(ws, js_res, req_id=34)

            # Monitor Downloads folder
            downloads_dir = Path.home() / "Downloads"
            click_t = time.time() - 5
            for _ in range(15):
                time.sleep(1)
                mp4s = [f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t]
                zips = [f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t]
                if mp4s or zips:
                    target = mp4s[0] if mp4s else zips[0]
                    dest_mp4_path.parent.mkdir(parents=True, exist_ok=True)
                    if target.suffix == ".mp4":
                        shutil.copy2(target, dest_mp4_path)
                        print(f"[SUCCESS] Downloaded and saved: {dest_mp4_path.name} ({dest_mp4_path.stat().st_size} bytes)")
                    elif target.suffix == ".zip":
                        with zipfile.ZipFile(target, "r") as z:
                            names = [n for n in z.namelist() if n.endswith(".mp4")]
                            if names:
                                ext = z.extract(names[0], dest_mp4_path.parent)
                                shutil.move(ext, dest_mp4_path)
                                print(f"[SUCCESS] Extracted zip and saved: {dest_mp4_path.name} ({dest_mp4_path.stat().st_size} bytes)")
                    
                    # Navigate back from editor
                    print("[Flow] Returning to project workspace...")
                    eval_js(ws, "window.history.back()", req_id=35)
                    time.sleep(3)
                    return True

    print(f"[Flow Timeout] Did not complete within {max_wait_sec}s.")
    return False

def generate_track_scenes(track_id: str, target_scene_count: int = 3):
    matches = list(PROMPTS_DIR.glob(f"*/{track_id}*.md"))
    if not matches:
        print(f"[Error] No blueprint found for track {track_id}")
        return False

    bp = parse_blueprint(matches[0])
    print("\n" + "=" * 80)
    print(f"GOOGLE FLOW AUTONOMOUS GENERATOR: {bp['title']}")
    print(f"Track ID: {bp['track_id']} | Category: {bp['category']}")
    print("=" * 80)

    track_dir = FLOW_RENDERS_DIR / bp['track_id']
    track_dir.mkdir(parents=True, exist_ok=True)

    ws = connect_ws()
    if not ws:
        return False

    ensure_project_workspace(ws)

    scenes = bp['scenes'][:target_scene_count]
    for sc in scenes:
        sc_num = sc['scene_num']
        dest_clip = track_dir / f"scene_{sc_num:02d}.mp4"
        if dest_clip.exists() and dest_clip.stat().st_size > 500_000:
            print(f"[Cached] Scene {sc_num} already exists ({dest_clip.stat().st_size} bytes). Skipping.")
            continue

        prompt = f"Devotional cinematic 16:9 photorealistic video: {sc['prompt']} Exclusions: {sc.get('exclusions', '')} {bp['continuity'].get('Hard Exclusions', '')}"
        print(f"\n>>> GENERATING SCENE {sc_num} <<<")
        submitted = submit_prompt(ws, prompt)
        if submitted:
            ok = handle_approvals_and_wait(ws, dest_clip, max_wait_sec=240)
            if not ok:
                print(f"[Warning] Scene {sc_num} generation incomplete.")
        time.sleep(3)

    ws.close()

    # Check clips and assemble master film
    existing_clips = sorted(track_dir.glob("scene_*.mp4"))
    if existing_clips:
        print(f"\n[Assembly] Found {len(existing_clips)} scenes for {bp['track_id']}. Assembling master film...")
        try:
            audio_path = ensure_audio(bp['track_id'])
            out_film = RENDERS_DIR / f"{bp['category'].lower()}_{bp['track_id']}_master.mp4"
            build_master_film(bp, existing_clips, audio_path, out_film)
            print(f"[COMPLETE] Master film ready: {out_film.name}")
            return True
        except Exception as e:
            print(f"[Assembly Error]: {e}")
            return False
    return False

def main():
    parser = argparse.ArgumentParser(description="Google Flow Autonomous Generator")
    parser.add_argument("--track", type=str, help="Generate for specific track ID")
    parser.add_argument("--scenes", type=int, default=3, help="Number of scenes per track")
    args = parser.parse_args()

    if args.track:
        generate_track_scenes(args.track, target_scene_count=args.scenes)
    else:
        # Default to 1hoVaPwWMes (Kandha Sashti Kavasam)
        generate_track_scenes("1hoVaPwWMes", target_scene_count=3)

if __name__ == '__main__':
    main()
