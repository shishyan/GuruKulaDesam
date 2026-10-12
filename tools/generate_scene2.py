import time
import json
import urllib.request
import websocket
import shutil
import zipfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import parse_blueprint, ensure_audio, build_master_film, RENDERS_DIR, FLOW_RENDERS_DIR, PROMPTS_DIR

TRACK_ID = "1hoVaPwWMes"
DEST_DIR = FLOW_RENDERS_DIR / TRACK_ID
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_CLIP = DEST_DIR / "scene_02.mp4"

SCENE_PROMPT = (
    "Devotional cinematic 16:9 photorealistic video: Create a single continuous 16:9 cinematic low-angle tracking shot at 24 fps "
    "following barefoot Tamil devotees in bright yellow and saffron dhotis climbing the carved stone steps of Palani hill. "
    "Devotees carry vibrant wooden peacock Kavadis adorned with fresh yellow marigolds, their foreheads gleaming with sacred "
    "white Tripundra Vibhuti and fragrant red kumkum. Exclusions: No modern footwear, no plastic bags, no text. "
    "No text, no subtitles, no watermarks, no modern clothing, no western faces, no plastic, no mobile phones."
)

def run():
    print(f"Connecting to Google Flow on port 9225 to generate Scene 2 for {TRACK_ID}...")
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Set download path
    ws.send(json.dumps({
        'id': 1,
        'method': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': str(Path.home() / 'Downloads')}
    }))
    json.loads(ws.recv())

    # Ensure in workspace (if in editor, go back)
    ws.send(json.dumps({
        'id': 2,
        'method': 'Runtime.evaluate',
        'params': {
            'expression': '(() => { if (window.location.href.includes("/edit/")) window.history.back(); return window.location.href; })()',
            'returnByValue': True
        }
    }))
    json.loads(ws.recv())
    time.sleep(3)

    # Type prompt into ProseMirror
    print("Typing Scene 2 prompt into chat...")
    js_type = f"""
    (() => {{
        const el = document.querySelector('div.ProseMirror');
        if (!el) return false;
        el.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, {json.dumps(SCENE_PROMPT)});
        return true;
    }})()
    """
    ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': js_type, 'returnByValue': True}}))
    res_type = json.loads(ws.recv())
    print("Typed prompt:", res_type.get('result', {}).get('result', {}).get('value'))
    time.sleep(1)

    # Click submit
    print("Clicking submit button...")
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
    ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': js_submit, 'returnByValue': True}}))
    res_sub = json.loads(ws.recv())
    print("Submit status:", res_sub.get('result', {}).get('result', {}).get('value'))
    time.sleep(4)

    # Monitor generation
    print("Monitoring Veo generation in queue...")
    start_time = time.time()
    for poll in range(60):
        time.sleep(5)
        elapsed = int(time.time() - start_time)

        # Check for progress percentage or stop button
        js_status = """
        (() => {
            const pcts = Array.from(document.querySelectorAll('*'))
                .filter(el => el.children.length === 0 && /^\\d{1,2}%$/.test((el.innerText || '').trim()))
                .map(el => el.innerText.trim());
            const hasStop = Array.from(document.querySelectorAll('button')).some(b => b.innerText === 'Stop' || b.getAttribute('aria-label') === 'Stop');
            return { pcts, hasStop };
        })()
        """
        ws.send(json.dumps({'id': 100 + poll, 'method': 'Runtime.evaluate', 'params': {'expression': js_status, 'returnByValue': True}}))
        res_st = json.loads(ws.recv())
        st = res_st.get('result', {}).get('result', {}).get('value', {})
        pcts = st.get('pcts', [])
        has_stop = st.get('hasStop', False)
        print(f"[{elapsed}s] Stop visible: {has_stop} | Progress: {pcts}")

        # Once stop disappears and elapsed > 25s
        if not has_stop and len(pcts) == 0 and elapsed >= 25:
            print(f"[{elapsed}s] Scene 2 generation complete! Opening latest video in editor...")
            time.sleep(3)

            # Click the LAST 'Open video in editor' button in chat
            js_last_ed = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .filter(b => (b.getAttribute('aria-label') || '').includes('Open video in editor'));
                if (btns.length > 0) {
                    const last = btns[btns.length - 1];
                    last.scrollIntoView();
                    last.click();
                    return { clicked: true, total: btns.length };
                }
                return { clicked: false };
            })()
            """
            ws.send(json.dumps({'id': 300, 'method': 'Runtime.evaluate', 'params': {'expression': js_last_ed, 'returnByValue': True}}))
            res_ed = json.loads(ws.recv())
            print("Open in editor:", res_ed.get('result', {}).get('result', {}).get('value'))
            time.sleep(4)

            # Trigger Download media
            js_dl = """
            (() => {
                const dl = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('download media') || (b.innerText || '').toLowerCase().includes('download media'));
                if (dl) { dl.click(); return true; }
                return false;
            })()
            """
            ws.send(json.dumps({'id': 301, 'method': 'Runtime.evaluate', 'params': {'expression': js_dl, 'returnByValue': True}}))
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
            ws.send(json.dumps({'id': 302, 'method': 'Runtime.evaluate', 'params': {'expression': js_res, 'returnByValue': True}}))
            res_res = json.loads(ws.recv())
            print("Resolution click:", res_res.get('result', {}).get('result', {}).get('value'))

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
                        print(f"[SUCCESS] Downloaded Scene 2: {newest.name} -> {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                        break
                elif zips:
                    newest = max(zips, key=lambda x: x.stat().st_mtime)
                    with zipfile.ZipFile(newest, "r") as z:
                        names = [n for n in z.namelist() if n.endswith(".mp4")]
                        if names:
                            ext = z.extract(names[0], DEST_DIR)
                            shutil.move(ext, DEST_CLIP)
                            print(f"[SUCCESS] Extracted Scene 2: {DEST_CLIP.name} ({DEST_CLIP.stat().st_size} bytes)")
                            break

            # Return to workspace
            ws.send(json.dumps({'id': 303, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.history.back()'}}))
            time.sleep(3)
            break

    ws.close()

    # Verify all 3 scenes and assemble master film
    existing_clips = sorted(DEST_DIR.glob("scene_*.mp4"))
    print(f"\n[Assembly] Found {len(existing_clips)} scenes in {DEST_DIR.name}:")
    for c in existing_clips:
        print(f"  - {c.name} ({c.stat().st_size} bytes)")

    bp_file = ROOT / "production" / "google_flow_prompts" / "murugan" / "1hoVaPwWMes_Kandha_Sashti_Kavasam__Ka.md"
    bp = parse_blueprint(bp_file)
    audio_path = ensure_audio(TRACK_ID)
    out_film = RENDERS_DIR / f"murugan_{TRACK_ID}_master.mp4"
    print(f"\nAssembling Final Master Film: {out_film.name}...")
    build_master_film(bp, existing_clips, audio_path, out_film)
    print(f"\n[MASTER FILM COMPLETE] {out_film.name} ({out_film.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == '__main__':
    run()
