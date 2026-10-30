#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/flow_autonomous_generator.py
Google Flow PRO Account (`sashanaga@gmail.com` on `https://flow.google.com/`)
Autonomous Song-Specific Video Generator for Both Master Films & 9:16 Shorts!

Capabilities:
1. Auto-syncs Chrome `Profile 3` (`sashanaga@gmail.com` Google AI PRO Flow account)
   into `~/.config/google-chrome-flow-cdp` and auto-launches Chrome on CDP port `9225`
   if not already running.
2. Generates 100% song-specific, lyric-matched scenes tailored directly to the exact
   Tamil lyrics, spiritual meaning, and blueprint of `track_id` — NEVER generic clips!
3. Supports `--for-short --track <id> [--push --channel @GuruKulaDesam2]` to generate
   5 dedicated Flow clips for a song's vocal peak window, assemble its 9:16 Short via
   `shorts_viral_builder.py`, and push directly to YouTube.
"""

import os
import re
import sys
import time
import json
import shutil
import zipfile
import argparse
import subprocess
import urllib.request
from pathlib import Path

import websocket

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import (
    FLOW_RENDERS_DIR,
    PROMPTS_DIR,
    RENDERS_DIR,
    build_master_film,
    ensure_audio,
    parse_blueprint,
)

METADATA_DB = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
CDP_PORT = 9225
CHROME_BIN = "/opt/google/chrome/chrome" if Path("/opt/google/chrome/chrome").exists() else (shutil.which("google-chrome") or "google-chrome")
FLOW_CDP_PROFILE_DIR = Path.home() / ".config" / "google-chrome-flow-cdp"


def sync_flow_chrome_profile():
    """Syncs Chrome Profile 3 (`sashanaga@gmail.com` Google Flow PRO) into isolated CDP dir."""
    src_root = Path.home() / ".config" / "google-chrome"
    if not src_root.exists():
        return
    (FLOW_CDP_PROFILE_DIR / "Default").mkdir(parents=True, exist_ok=True)
    local_state = src_root / "Local State"
    if local_state.exists():
        shutil.copy2(local_state, FLOW_CDP_PROFILE_DIR / "Local State")

    # Prefer Profile 3 (sashanaga@gmail.com Flow PRO), fallback to Default
    src_prof = src_root / "Profile 3"
    if not src_prof.exists():
        src_prof = src_root / "Default"
    for item in ("Cookies", "Preferences", "Secure Preferences", "Login Data", "Web Data", "Network"):
        s = src_prof / item
        d = FLOW_CDP_PROFILE_DIR / "Default" / item
        if s.exists():
            try:
                if s.is_dir():
                    shutil.rmtree(d, ignore_errors=True)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            except Exception:
                pass


def ensure_flow_chrome_running() -> subprocess.Popen | None:
    """Checks if CDP port 9225 is active with a Flow tab; if not, launches Chrome automatically."""
    try:
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=2).read())
        if any("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "") for t in tabs):
            return None
    except Exception:
        pass

    print(f"[Flow] Launching Google Flow PRO session (`sashanaga@gmail.com`) on CDP port {CDP_PORT}...")
    sync_flow_chrome_profile()
    env = os.environ.copy()
    env["DISPLAY"] = env.get("DISPLAY", ":0")
    proc = subprocess.Popen(
        [
            CHROME_BIN,
            f"--user-data-dir={FLOW_CDP_PROFILE_DIR}",
            f"--remote-debugging-port={CDP_PORT}",
            "--no-first-run",
            "--no-default-browser-check",
            "https://flow.google.com/",
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(15):
        time.sleep(1)
        try:
            tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=2).read())
            if any("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "") for t in tabs):
                time.sleep(3)
                return proc
        except Exception:
            pass
    return proc


def get_flow_tab():
    try:
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=3).read())
    except Exception as e:
        print(f"[CDP Error] Could not connect to Chrome on port {CDP_PORT}: {e}")
        return None
    flow_tabs = [t for t in tabs if ("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "")) and t.get("type") == "page"]
    if not flow_tabs:
        print("[CDP Error] No active Google Flow tab found on port", CDP_PORT)
        return None
    return flow_tabs[0]


def connect_ws():
    tab = get_flow_tab()
    if not tab:
        return None
    ws = websocket.create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True)
    ws.send(json.dumps({
        "id": 1,
        "method": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": str(Path.home() / "Downloads")}
    }))
    json.loads(ws.recv())
    return ws


def eval_js(ws, js_code, req_id=2):
    ws.send(json.dumps({
        "id": req_id,
        "method": "Runtime.evaluate",
        "params": {"expression": js_code, "returnByValue": True}
    }))
    res = json.loads(ws.recv())
    return res.get("result", {}).get("result", {}).get("value")


def ensure_project_workspace(ws):
    """Ensures we are inside a Flow project workspace."""
    tab = get_flow_tab()
    url = tab.get("url", "") if tab else ""
    if "/project/" not in url:
        print("[Flow] Opening Flow project workspace...")
        js_new = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, a, [role="button"]'));
            const newBtn = btns.find(b => (b.innerText || '').includes('New project')) ||
                           btns.find(b => (b.innerText || '').includes('Start Creating'));
            if (newBtn) { newBtn.click(); return newBtn.innerText.trim(); }
            return null;
        })()
        """
        clicked = eval_js(ws, js_new)
        print(f"[Flow] Workspace click: {clicked}")
        time.sleep(5)


def submit_prompt(ws, prompt_text: str) -> bool:
    print(f"[Flow] Submitting song-specific prompt ({len(prompt_text)} chars)...")
    js_type = f"""
    (() => {{
        const el = document.querySelector('div.ProseMirror, textarea, [contenteditable="true"]');
        if (!el) return false;
        el.focus();
        if (el.tagName === 'TEXTAREA') {{
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeSetter.call(el, {json.dumps(prompt_text)});
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }}
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, {json.dumps(prompt_text)});
        return true;
    }})()
    """
    ok = eval_js(ws, js_type, req_id=20)
    if not ok:
        print("[Flow Error] Could not locate Flow prompt input editor!")
        return False

    time.sleep(1.5)
    js_submit = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const sendBtn = btns.find(b =>
            (b.innerText || '').includes('arrow_forward') ||
            (b.getAttribute('aria-label') || '').toLowerCase().includes('send') ||
            (b.getAttribute('aria-label') || '').toLowerCase().includes('generate') ||
            (b.getAttribute('aria-label') || '').toLowerCase().includes('create')
        );
        if (sendBtn && !sendBtn.disabled) {
            sendBtn.click();
            return 'CLICKED_SEND';
        }
        return 'BUTTON_NOT_FOUND';
    })()
    """
    res = eval_js(ws, js_submit, req_id=21)
    print(f"[Flow] Submit button status: {res}")
    time.sleep(3)
    return res == "CLICKED_SEND"


def handle_approvals_and_wait(ws, dest_mp4_path: Path, max_wait_sec=240) -> bool:
    print(f"[Flow] Monitoring render pipeline for {dest_mp4_path.name} (timeout {max_wait_sec}s)...")
    start_time = time.time()
    approved = False
    downloads_dir = Path.home() / "Downloads"

    while time.time() - start_time < max_wait_sec:
        time.sleep(4)
        elapsed = int(time.time() - start_time)

        if not approved:
            js_appr = """
            (() => {
                const optionRows = Array.from(document.querySelectorAll('.choice-container .option-row, flow-permission-message .option-row, .option-row, button'));
                const target = optionRows.find(el => (el.textContent || '').includes('Always approve')) ||
                               optionRows.find(el => (el.textContent || '').trim() === 'Approve');
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
            if res_appr and res_appr.get("clicked"):
                approved = True
                print(f"[{elapsed}s] Credit deduction approved: '{res_appr.get('text')}'!")
                time.sleep(3)

        js_status = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            const editorBtn = btns.find(b => (b.getAttribute('aria-label') || '').includes('Open video in editor'));
            const dlBtn = btns.find(b =>
                (b.getAttribute('aria-label') || '').toLowerCase().includes('download') ||
                (b.innerText || '').toLowerCase().includes('download')
            );
            return { hasEditorBtn: !!editorBtn, hasDlBtn: !!dlBtn };
        })()
        """
        st = eval_js(ws, js_status, req_id=31) or {}

        if st.get("hasEditorBtn"):
            print(f"[{elapsed}s] Video generation complete! Opening in editor...")
            eval_js(ws, """
            (() => {
                const btn = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.getAttribute('aria-label') || '').includes('Open video in editor'));
                if (btn) { btn.click(); return true; }
                return false;
            })()
            """, req_id=32)
            time.sleep(4)

        if st.get("hasDlBtn"):
            print(f"[{elapsed}s] Triggering MP4 download...")
            click_t = time.time() - 3
            eval_js(ws, """
            (() => {
                const dl = Array.from(document.querySelectorAll('button, [role="button"]'))
                    .find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('download') || (b.innerText || '').toLowerCase().includes('download'));
                if (dl) { dl.click(); return true; }
                return false;
            })()
            """, req_id=33)
            time.sleep(2)
            eval_js(ws, """
            (() => {
                const resBtn = Array.from(document.querySelectorAll('button, [role="menuitem"]'))
                    .find(b => ['1080p', 'original size', '720p'].some(w => (b.innerText || '').toLowerCase().includes(w)));
                if (resBtn) { resBtn.click(); return true; }
                return false;
            })()
            """, req_id=34)

            for _ in range(20):
                time.sleep(1)
                mp4s = sorted([f for f in downloads_dir.glob("*.mp4") if f.stat().st_mtime >= click_t], key=lambda p: p.stat().st_mtime, reverse=True)
                zips = sorted([f for f in downloads_dir.glob("download*.zip") if f.stat().st_mtime >= click_t], key=lambda p: p.stat().st_mtime, reverse=True)
                if mp4s or zips:
                    target = mp4s[0] if mp4s else zips[0]
                    dest_mp4_path.parent.mkdir(parents=True, exist_ok=True)
                    if target.suffix == ".mp4":
                        shutil.copy2(target, dest_mp4_path)
                    elif target.suffix == ".zip":
                        with zipfile.ZipFile(target, "r") as z:
                            names = [n for n in z.namelist() if n.endswith(".mp4")]
                            if names:
                                ext = z.extract(names[0], dest_mp4_path.parent)
                                shutil.move(ext, dest_mp4_path)
                    if dest_mp4_path.exists() and dest_mp4_path.stat().st_size > 200_000:
                        print(f"[SUCCESS] Saved song-specific Flow scene: {dest_mp4_path.name} ({dest_mp4_path.stat().st_size / 1e6:.2f} MB)")
                        eval_js(ws, "window.history.back()", req_id=35)
                        time.sleep(3)
                        return True

    print(f"[Flow Timeout] Did not complete within {max_wait_sec}s.")
    return False


def build_song_specific_short_prompts(track_id: str, count: int = 5) -> tuple[str, list[str]]:
    """
    Crafts `count` hyper-specific scene prompts strictly anchored to THIS song's
    title, Tamil lyrics, spiritual meaning, and any existing blueprint.
    """
    bp_matches = list(PROMPTS_DIR.glob(f"*/{track_id}*.md"))
    if bp_matches:
        bp = parse_blueprint(bp_matches[0])
        if len(bp.get("scenes", [])) >= count:
            excl = bp.get("continuity", {}).get("Hard Exclusions", "No text, no watermarks, no modern clothes.")
            prompts = [
                f"Photorealistic South Indian Chola-era devotional cinema, 9:16 vertical framing, centered subject: {sc['prompt']} Exclusions: {sc.get('exclusions', '')} {excl}"
                for sc in bp["scenes"][:count]
            ]
            return bp["title"], prompts

    meta_db = json.loads(METADATA_DB.read_text(encoding="utf-8")) if METADATA_DB.exists() else {}
    entry = meta_db.get(track_id, {})
    title = entry.get("title", track_id)
    en_meaning = re.sub(r"\s+", " ", entry.get("english_meaning", "")).strip()
    ta_meaning = re.sub(r"\s+", " ", entry.get("tamil_meaning", "")).strip()
    ta_lyrics = [l.strip() for l in entry.get("tamil_lyrics", "").splitlines() if l.strip()]

    story_context = en_meaning[:360] if en_meaning else (ta_meaning[:280] if ta_meaning else title)
    camera_beats = [
        "Opening sacred close-up establishing the exact divine subject and emotional essence",
        "Medium cinematic devotional tableau illustrating the core verse action in warm temple lamp-light",
        "Intimate expressive shot of sincere Tamil devotion and sacred ritual offering matching the hymn",
        "Sweeping Chola stone mandapam architectural perspective embodying the spiritual teaching",
        "Radiant golden-hour culmination shot of divine grace and inner peace",
    ]
    prompts = []
    for idx in range(count):
        lyric_ref = ta_lyrics[idx % len(ta_lyrics)] if ta_lyrics else title
        prompts.append(
            f"Photorealistic South Indian Chola-era sacred cinema for the Tamil hymn '{title}' "
            f"(verse theme: '{lyric_ref}'; meaning: {story_context}). "
            f"{camera_beats[idx % len(camera_beats)]}. "
            f"Warm brass kuthuvilakku oil-lamp glow, authentic Tamil cultural attire, zero onscreen text, zero watermarks, zero modern objects."
        )
    return title, prompts


def generate_flow_clips_for_short(track_id: str, scene_count: int = 5) -> list[Path]:
    """
    Generates `scene_count` dedicated song-specific clips via the Google Flow PRO account
    and writes `flow_verified.json` into `production/google_flow_renders/<track_id>/`.
    """
    title, prompts = build_song_specific_short_prompts(track_id, count=scene_count)
    track_dir = FLOW_RENDERS_DIR / track_id
    track_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 80)
    print(f"✨ GOOGLE FLOW SONG-SPECIFIC SHORT GENERATOR: {title} ({track_id})")
    print("=" * 80)

    proc = ensure_flow_chrome_running()
    ws = connect_ws()
    if not ws:
        if proc:
            proc.terminate()
        raise RuntimeError("Could not connect to Google Flow Chrome CDP session on port 9225.")

    generated_paths = []
    try:
        ensure_project_workspace(ws)
        for idx, prompt in enumerate(prompts, 1):
            dest_clip = track_dir / f"flow_short_{idx:02d}.mp4"
            if dest_clip.exists() and dest_clip.stat().st_size > 400_000:
                print(f"  [Cached] {dest_clip.name} already exists.")
                generated_paths.append(dest_clip)
                continue
            print(f"\n>>> GENERATING SONG-SPECIFIC FLOW CLIP {idx}/{scene_count} <<<")
            if submit_prompt(ws, prompt):
                if handle_approvals_and_wait(ws, dest_clip, max_wait_sec=240):
                    generated_paths.append(dest_clip)
            time.sleep(2)
    finally:
        ws.close()
        if proc:
            proc.terminate()

    if len(generated_paths) >= 3:
        manifest_file = track_dir / "flow_verified.json"
        manifest_file.write_text(
            json.dumps({
                "track_id": track_id,
                "title": title,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                "account": "sashanaga@gmail.com (Google Flow PRO)",
                "clips": [p.name for p in generated_paths],
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return generated_paths


def generate_track_scenes(track_id: str, target_scene_count: int = 3) -> bool:
    matches = list(PROMPTS_DIR.glob(f"*/{track_id}*.md"))
    if not matches:
        print(f"[Info] No markdown blueprint for {track_id}; using lyric-specific Flow Short generator...")
        clips = generate_flow_clips_for_short(track_id, scene_count=target_scene_count)
        return len(clips) >= 3

    bp = parse_blueprint(matches[0])
    track_dir = FLOW_RENDERS_DIR / bp["track_id"]
    track_dir.mkdir(parents=True, exist_ok=True)

    proc = ensure_flow_chrome_running()
    ws = connect_ws()
    if not ws:
        if proc:
            proc.terminate()
        return False

    try:
        ensure_project_workspace(ws)
        for sc in bp["scenes"][:target_scene_count]:
            sc_num = sc["scene_num"]
            dest_clip = track_dir / f"scene_{sc_num:02d}.mp4"
            if dest_clip.exists() and dest_clip.stat().st_size > 500_000:
                continue
            prompt = f"Devotional cinematic 16:9 photorealistic video: {sc['prompt']} Exclusions: {sc.get('exclusions', '')} {bp['continuity'].get('Hard Exclusions', '')}"
            if submit_prompt(ws, prompt):
                handle_approvals_and_wait(ws, dest_clip, max_wait_sec=240)
            time.sleep(2)
    finally:
        ws.close()
        if proc:
            proc.terminate()

    existing_clips = sorted(track_dir.glob("scene_*.mp4"))
    if existing_clips:
        audio_path = ensure_audio(bp["track_id"])
        out_film = RENDERS_DIR / f"{bp['category'].lower()}_{bp['track_id']}_master.mp4"
        build_master_film(bp, existing_clips, audio_path, out_film)
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Google Flow Autonomous Song-Specific Video Generator")
    parser.add_argument("--track", type=str, required=True, help="Track ID to generate song-specific Flow visuals for")
    parser.add_argument("--scenes", type=int, default=5, help="Number of song-specific scenes (default: 5)")
    parser.add_argument("--for-short", action="store_true", help="Generate song-specific clips and build 9:16 Short")
    parser.add_argument("--push", action="store_true", help="Upload built Short directly to YouTube")
    parser.add_argument("--channel", type=str, default="@GuruKulaDesam2", help="Target channel (@GuruKulaDesam or @GuruKulaDesam2)")
    args = parser.parse_args()

    if args.for_short:
        clips = generate_flow_clips_for_short(args.track, scene_count=args.scenes)
        if len(clips) < 3:
            sys.exit(f"❌ Flow generated only {len(clips)} clips for {args.track}; aborting Short build.")
        from tools.shorts_viral_builder import build_short_for_track
        meta = build_short_for_track(args.track, force_rebuild=True, brand_handle=args.channel, use_flow=True)
        if args.push:
            from tools.shorts_autonomous_daemon import upload_short_via_api
            upload_short_via_api(meta, publish_at_dt=None, channel_key=args.channel.lower())
    else:
        generate_track_scenes(args.track, target_scene_count=args.scenes)


if __name__ == "__main__":
    main()
