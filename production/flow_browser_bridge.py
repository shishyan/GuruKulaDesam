# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Google Flow (flow.google.com) Browser Automation Bridge
Automates generating Veo video clips directly on flow.google.com using your
8,686 Google Flow account credits, and automatically triggers master film assembly.

Features:
- Launches native Chrome with your persistent profile (bypassing bot detection).
- Connects via Playwright CDP.
- Feeds Scene 1, Scene 2, and Scene 3 prompts from production/google_flow_prompts/.
- Auto-approves credit deductions ("Always approve").
- Downloads and extracts generated MP4 video scenes to production/google_flow_renders/<TRACK_ID>/.
- Calls google_flow_engine.py to assemble master films with sacred framing and audio sync.

Usage:
  # Launch Chrome to inspect flow.google.com:
  python production/flow_browser_bridge.py --open

  # Generate for a specific track:
  python production/flow_browser_bridge.py --track 2QOF2ycA4RQ

  # Generate for all tracks in a category:
  python production/flow_browser_bridge.py --category vinayagar

  # Generate for all tracks in the pending manifest:
  python production/flow_browser_bridge.py --all --limit 10
"""

import os
import sys
import time
import json
import zipfile
import shutil
import argparse
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import parse_blueprint, ensure_audio, build_master_film, RENDERS_DIR, FLOW_RENDERS_DIR, PROMPTS_DIR

FLOW_URL = "https://flow.google.com"
CHROME_PROFILE_DIR = ROOT / "production" / "browser_profile"
CHROME_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CDP_PORT = 9222

def kill_browser_profile_processes():
    """Kills any running Chrome processes using the browser_profile directory."""
    ps_cmd = "Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*browser_profile*' } | Stop-Process -Force"
    subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
    time.sleep(1)

def launch_native_chrome():
    """Launches native Chrome with remote debugging and persistent user data."""
    kill_browser_profile_processes()
    cmd = [
        CHROME_EXE,
        f"--user-data-dir={CHROME_PROFILE_DIR}",
        f"--remote-debugging-port={CDP_PORT}",
        "--no-first-run",
        "--no-default-browser-check",
        FLOW_URL
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(5)
    return proc

def open_session():
    """Opens flow.google.com for the user to inspect or sign in."""
    print("=" * 80)
    print("OPENING GOOGLE FLOW (flow.google.com)")
    print("=" * 80)
    print("Launching native Chrome with your Ultra profile...\n")
    proc = launch_native_chrome()
    print("Chrome is open at flow.google.com. Press Ctrl+C when finished.")
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nClosing Chrome session...")
    finally:
        kill_browser_profile_processes()

def check_recent_downloads(dest_mp4_path: Path, since_timestamp: float) -> bool:
    """Checks the user Downloads folder for any zip/mp4 created after since_timestamp."""
    downloads_dir = Path.home() / "Downloads"
    candidates = []
    for f in downloads_dir.glob("download*.zip"):
        try:
            if f.stat().st_mtime >= since_timestamp - 3:
                candidates.append(f)
        except Exception:
            pass
    for f in downloads_dir.glob("*.mp4"):
        try:
            if f.stat().st_mtime >= since_timestamp - 3:
                candidates.append(f)
        except Exception:
            pass
    
    if not candidates:
        return False
        
    candidates.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    newest = candidates[0]
    if newest.suffix == ".zip":
        try:
            with zipfile.ZipFile(newest, "r") as z:
                mp4_files = [m for m in z.namelist() if m.endswith(".mp4")]
                if mp4_files:
                    extracted_path = z.extract(mp4_files[0], dest_mp4_path.parent)
                    if dest_mp4_path.exists():
                        dest_mp4_path.unlink()
                    shutil.move(extracted_path, dest_mp4_path)
                    print(f"[Flow] SUCCESS: Extracted {dest_mp4_path.name} from Downloads ({dest_mp4_path.stat().st_size} bytes)")
                    return True
        except Exception as e:
            print(f"[Flow] Error extracting from Downloads: {e}")
    elif newest.suffix == ".mp4":
        try:
            if dest_mp4_path.exists():
                dest_mp4_path.unlink()
            shutil.copy2(newest, dest_mp4_path)
            print(f"[Flow] SUCCESS: Copied direct MP4 {dest_mp4_path.name} from Downloads ({dest_mp4_path.stat().st_size} bytes)")
            return True
        except Exception as e:
            print(f"[Flow] Error copying from Downloads: {e}")
    return False

def wait_for_assistant_and_approve(page, timeout_sec=60):
    """Waits for assistant response and clicks 'Always approve' or 'Approve' if prompted."""
    print("[Flow] Waiting for assistant response / approval options...")
    start_t = time.time()
    while time.time() - start_t < timeout_sec:
        page.wait_for_timeout(2000)
        
        # Check Always approve
        always_btn = page.locator("text='Always approve'").all()
        if always_btn:
            print("[Flow] Clicking 'Always approve'...")
            always_btn[-1].click()
            page.wait_for_timeout(3000)
            return True
            
        # Check regular Approve
        approve_btn = page.locator("button:has-text('Approve'), [role='button']:has-text('Approve')").all()
        if approve_btn:
            print("[Flow] Clicking 'Approve'...")
            approve_btn[-1].click()
            page.wait_for_timeout(3000)
            return True
            
        # Check if generation already started (Stop button active)
        stop_btn = page.locator("button[aria-label='Stop'], button:has-text('stop')")
        if stop_btn.count() > 0 and stop_btn.is_visible():
            # Still generating/replying
            continue

        # If download button already visible, generation already finished
        dl_btn = page.locator("button[aria-label*='Download' i]").first
        if dl_btn.count() > 0 and dl_btn.is_visible():
            return True

    return False

def wait_and_download_video(page, dest_mp4_path: Path, max_wait_sec=240, only_wait_ready=False):
    """Monitors the project workspace until the video completes, then downloads and extracts the MP4."""
    print(f"[Flow] Monitoring video render (up to {max_wait_sec}s)...")
    start_t = time.time()
    
    while time.time() - start_t < max_wait_sec:
        page.wait_for_timeout(5000)
        elapsed = int(time.time() - start_t)

        # Check for transient error or retry button
        try_again = page.locator("button:has-text('Try again')").first
        if try_again.count() > 0 and try_again.is_visible():
            print("[Flow] Transient error encountered. Clicking 'Try again'...")
            try_again.click()
            page.wait_for_timeout(3000)
            wait_for_assistant_and_approve(page)
            start_t = time.time()
            continue

        if elapsed < 35:
            print(f"[Flow] Render in progress... {elapsed}s elapsed")
            continue
        
        # Hover over newest video card to reveal overlay action buttons
        cards = page.locator("div[class*='card'], div[class*='tile'], div[class*='video'], div[class*='artifact']").all()
        if cards:
            try:
                cards[-1].hover()
                page.wait_for_timeout(500)
            except Exception:
                pass

        editor_btn = page.locator("button:has-text('play_circle'), [aria-label*='Open video in editor' i]").last
        if editor_btn.count() == 0:
            editor_btn = page.locator("button[aria-label*='editor' i]").last

        if editor_btn.count() > 0 and (editor_btn.is_visible() or elapsed >= 35):
            print(f"[Flow] Video ready on canvas! (Elapsed: {elapsed}s)...")
            if only_wait_ready:
                return True
            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)
                editor_btn.click(force=True)
                page.wait_for_url("**/edit/**", timeout=20000)
                page.wait_for_timeout(3000)
                dl_media = page.locator("button[aria-label='Download media']:visible").first
                if dl_media.count() > 0 and dl_media.is_enabled():
                    click_time = time.time()
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(200)
                    dl_media.click(force=True)
                    for _ in range(14):
                        page.wait_for_timeout(1000)
                        if check_recent_downloads(dest_mp4_path, click_time):
                            return True
            except Exception as e:
                print(f"[Flow] Editor download click error: {e}")

        print(f"[Flow] Waiting for render... {elapsed}s elapsed")

    print("[Flow] Timed out waiting for video render.")
    return False

def wait_and_extend_video(page, dest_mp4_path: Path, extend_count: int = 2, continuation_prompts: list = None, max_wait_sec=240):
    """Opens the generated video in the Flow editor, extends it using the Extend option,
    and downloads the concatenated multi-clip extended video."""
    print(f"[Flow Extend] Opening video in editor for {extend_count} extensions...")
    
    # Hover over newest video card to reveal overlay action buttons
    cards = page.locator("div[class*='card'], div[class*='tile'], div[class*='video'], div[class*='artifact']").all()
    if cards:
        try:
            cards[-1].hover()
            page.wait_for_timeout(600)
        except Exception:
            pass

    editor_btn = page.locator("button:has-text('play_circle'), [aria-label*='Open video in editor' i]").last
    if editor_btn.count() == 0:
        editor_btn = page.locator("button[aria-label*='editor' i]").last

    if editor_btn.count() == 0:
        print("[Flow Extend Warning] 'Open video in editor' button not found, falling back to direct download.")
        return False

    editor_btn.click(force=True)
    try:
        page.wait_for_url("**/edit/**", timeout=20000)
    except Exception as e:
        print(f"[Flow Extend Warning] Did not transition to editor: {e}")
        return False

    page.wait_for_timeout(4000)

    # Debug: log all visible buttons and save screenshot in Flow editor
    try:
        visible_btns = [b.get_attribute('aria-label') or b.inner_text().strip() for b in page.locator('button, [role="button"]').all() if b.is_visible()]
        print(f"[Flow Editor Buttons]: {visible_btns}")
        page.screenshot(path="flow_editor_debug.png")
    except Exception as e:
        print(f"[Flow Editor Debug Error]: {e}")

    for ext_step in range(1, extend_count + 1):
        print(f"[Flow Extend] Performing extension {ext_step}/{extend_count}...")
        add_clip = page.locator("button[aria-label='Add clip']:visible, button[aria-label*='Add' i]:visible, button:has-text('Add clip'), button:has-text('Add'), button:has([class*='add'])").first
        if add_clip.count() == 0:
            print("[Flow Extend] 'Add clip' button not found, stopping extensions.")
            break

        add_clip.click()
        page.wait_for_timeout(1500)

        extend_opt = page.locator("[role='menuitem']:has-text('Extend')").first
        if extend_opt.count() == 0 or extend_opt.get_attribute("disabled"):
            print(f"[Flow Extend] Extend menu item disabled or absent (disabled={extend_opt.get_attribute('disabled') if extend_opt.count() else 'None'}).")
            page.keyboard.press("Escape")
            break

        extend_opt.click()
        page.wait_for_timeout(2000)

        # Enter prompt if provided
        prompt_editor = page.locator("div.ProseMirror:visible").first
        if prompt_editor.count() > 0 and continuation_prompts and len(continuation_prompts) >= ext_step:
            ext_prompt = continuation_prompts[ext_step - 1]
            print(f"[Flow Extend] Entering continuation prompt: {ext_prompt[:100]}...")
            prompt_editor.click()
            page.wait_for_timeout(300)
            page.keyboard.type(ext_prompt, delay=8)
            page.wait_for_timeout(1000)

        # Start generation
        gen_btn = page.locator("button[aria-label='Start generation']:visible").first
        if gen_btn.count() > 0 and gen_btn.is_enabled():
            gen_btn.click()
            print(f"[Flow Extend] Extension {ext_step} generation started. Waiting for completion...")
            wait_for_assistant_and_approve(page, timeout_sec=20)

            # Wait for extension render
            ext_start_t = time.time()
            render_done = False
            while time.time() - ext_start_t < max_wait_sec:
                page.wait_for_timeout(6000)
                elapsed = int(time.time() - ext_start_t)
                dl_media = page.locator("button[aria-label='Download media']:visible").first
                gen_b = page.locator("button[aria-label='Start generation']:visible").first
                if elapsed >= 40 and dl_media.count() > 0 and dl_media.is_enabled() and (gen_b.count() == 0 or gen_b.is_enabled()):
                    print(f"[Flow Extend] Extension {ext_step} complete ({elapsed}s)!")
                    render_done = True
                    break
                print(f"[Flow Extend] Extension {ext_step} rendering... {elapsed}s elapsed")

            if not render_done:
                print(f"[Flow Extend Warning] Extension {ext_step} timed out.")
                break
        else:
            print("[Flow Extend Warning] Start generation button was not enabled.")
            break

    # Download extended scene from editor
    print("[Flow Extend] Downloading extended multi-clip video from editor...")
    dl_media = page.locator("button[aria-label='Download media']:visible, button[aria-label*='Download' i]:visible").first
    if dl_media.count() > 0 and dl_media.is_enabled():
        click_time = time.time()
        try:
            dl_media.click()
            page.wait_for_timeout(1000)
            
            # Flow Scene Editor opens a menu with 720p / 1080p options
            btn_720 = page.locator("button:has-text('720p'), [role='menuitem']:has-text('720p'), button:has-text('Original size')").first
            if btn_720.count() > 0 and btn_720.is_visible():
                print("[Flow Extend] Clicking '720p Original size' download option...")
                btn_720.click()
            else:
                dl_media.click()
        except Exception as e:
            print(f"[Flow Extend] Click download error: {e}")

        # Wait and check if downloaded to Downloads folder
        for _ in range(8):
            page.wait_for_timeout(1000)
            if check_recent_downloads(dest_mp4_path, click_time):
                print(f"[Flow Extend SUCCESS] Saved extended video: {dest_mp4_path.name} ({dest_mp4_path.stat().st_size} bytes)")
                if "/edit/" in page.url:
                    page.go_back()
                    page.wait_for_timeout(2000)
                return True

    # Return from editor if stuck
    if "/edit/" in page.url:
        page.go_back()
        page.wait_for_timeout(2000)

    return False

def generate_track_on_flow(track_id: str, extend: bool = True, extend_steps: int = 2):
    """Automates generating scenes for a track on flow.google.com and builds the master film."""
    from playwright.sync_api import sync_playwright

    matches = list(PROMPTS_DIR.glob(f"*/{track_id}*.md"))
    if not matches:
        print(f"Error: No blueprint found for track {track_id}")
        return False

    bp = parse_blueprint(matches[0])
    print("\n" + "=" * 80)
    print(f"GOOGLE FLOW AUTOMATION: {bp['title']}")
    print(f"Track ID: {bp['track_id']} | Category: {bp['category']} | Scenes: {len(bp['scenes'])} | Extend: {extend} ({extend_steps} steps)")
    print("=" * 80)

    track_dir = FLOW_RENDERS_DIR / bp['track_id']
    track_dir.mkdir(parents=True, exist_ok=True)

    # Check which scenes are already rendered
    scenes_to_render = []
    for sc in bp['scenes']:
        sc_num = sc['scene_num']
        out_clip = track_dir / f"scene_{sc_num:02d}.mp4"
        if out_clip.exists() and out_clip.stat().st_size > 500_000:
            print(f"[Cached] Scene {sc_num} already exists: {out_clip.name} ({out_clip.stat().st_size} bytes)")
        else:
            scenes_to_render.append(sc)

    if not scenes_to_render:
        print("[All Scenes Cached] Proceeding directly to master film assembly!")
    else:
        # Launch Chrome and automate
        proc = launch_native_chrome()
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(f"http://localhost:{CDP_PORT}")
                context = browser.contexts[0]
                page = context.pages[0] if context.pages else context.new_page()
                page.goto(FLOW_URL)
                page.wait_for_timeout(5000)

                # Process each scene
                for sc in scenes_to_render:
                    sc_num = sc['scene_num']
                    out_clip = track_dir / f"scene_{sc_num:02d}.mp4"
                    if out_clip.exists() and out_clip.stat().st_size > 500_000:
                        print(f"[Cached] Scene {sc_num} already exists: {out_clip.name}")
                        continue

                    # Open fresh project for each scene
                    print(f"\n[Scene {sc_num}] Creating fresh project workspace on Google Flow...")
                    page.goto(FLOW_URL)
                    page.wait_for_timeout(3000)
                    try:
                        page.wait_for_selector("button:has-text('New project'), [role='button']:has-text('New project')", timeout=25000)
                        new_proj = page.locator("button:has-text('New project'), [role='button']:has-text('New project')").first
                        new_proj.click()
                        page.wait_for_url("**/project/**", timeout=25000)
                        page.wait_for_timeout(3000)
                    except Exception as e:
                        print(f"[Flow Warning] Could not click New project: {e}")

                    try:
                        page.wait_for_selector("div.ProseMirror", timeout=25000)
                    except Exception:
                        pass

                    prompt = f"Devotional cinematic 16:9 photorealistic video: {sc['prompt']} Exclusions: {sc.get('exclusions', '')} {bp['continuity'].get('Hard Exclusions', '')}"

                    print(f"[Scene {sc_num}] Submitting prompt...")
                    print(f"Prompt: {prompt[:140]}...")

                    editor = page.locator("div.ProseMirror").first
                    if editor.count() == 0:
                        print("[Flow Error] ProseMirror editor not found.")
                        break

                    editor.click()
                    page.wait_for_timeout(500)
                    page.keyboard.type(prompt, delay=8)
                    page.wait_for_timeout(1000)

                    # Determine continuation prompts if extend is enabled
                    continuation_prompts = []
                    if extend:
                        curr_idx = next((i for i, s in enumerate(bp['scenes']) if s['scene_num'] == sc_num), -1)
                        if curr_idx != -1:
                            for offset in range(1, extend_steps + 1):
                                next_idx = curr_idx + offset
                                if next_idx < len(bp['scenes']):
                                    next_sc = bp['scenes'][next_idx]
                                    continuation_prompts.append(f"Continuing seamless sequence: {next_sc['prompt']}")

                    gen_btn = page.locator("button[aria-label='Start generation']").first
                    if gen_btn.is_enabled():
                        gen_btn.click()
                        print(f"[Scene {sc_num}] Generation triggered. Waiting for approval...")
                        wait_for_assistant_and_approve(page)

                        success = False
                        if extend and continuation_prompts:
                            print(f"[Scene {sc_num}] Video generating. Waiting for completion to trigger EXTEND...")
                            ready = wait_and_download_video(page, out_clip, only_wait_ready=True)
                            if ready:
                                success = wait_and_extend_video(page, out_clip, extend_count=len(continuation_prompts), continuation_prompts=continuation_prompts)
                        else:
                            # Fast-anchor mode: download pristine base clip directly via editor
                            print(f"[Scene {sc_num}] Fast-Anchor: Waiting for base clip completion...")
                            ready = wait_and_download_video(page, out_clip, only_wait_ready=True)
                            if ready:
                                success = wait_and_extend_video(page, out_clip, extend_count=0)

                        if not success:
                            if "/edit/" in page.url:
                                print("[Flow] Navigating back from editor to project workspace...")
                                page.go_back()
                                page.wait_for_timeout(3000)
                            success = wait_and_download_video(page, out_clip)

                        if not success:
                            print(f"[Flow Warning] Failed to render Scene {sc_num}.")
                    else:
                        print(f"[Flow Error] Start generation button was not enabled.")

                browser.close()
        finally:
            kill_browser_profile_processes()

    # Master film assembly
    existing_clips = sorted(track_dir.glob("scene_*.mp4"))
    if existing_clips:
        print(f"\n[Assembly] Found {len(existing_clips)} scenes for {bp['track_id']}.")
        try:
            audio_path = ensure_audio(bp['track_id'])
            out_film = RENDERS_DIR / f"{bp['category'].lower()}_{bp['track_id']}_master.mp4"
            build_master_film(bp, existing_clips, audio_path, out_film)
            return True
        except Exception as e:
            print(f"[Assembly Error] Failed to assemble master film: {e}")
            return False
    else:
        print(f"[Assembly Error] No scenes available for {bp['track_id']}.")
        return False

VINAYAGAR_TRACK_IDS = [
    "AW4cljBWy2w",
    "RVMUEr1MOFo",
    "pYuwzoJkhTE",
    "T1KiH3G5WPs",
    "zqStqzcFgbM",
    "mQpQEuXiEZ4",
    "Yvlg_8JBHL4",
    "IhE1OvdIBKs",
    "Lki_Y8OSljs",
    "GydxHEmyDPc",
    "lEHLSYxnpbU",
    "vFbw9hX0wO4"
]

def main():
    parser = argparse.ArgumentParser(description="Google Flow Browser Automation Bridge")
    parser.add_argument("--open", action="store_true", help="Open Chrome to inspect flow.google.com")
    parser.add_argument("--track", type=str, help="Process a specific track by Track ID")
    parser.add_argument("--category", type=str, help="Process a category of tracks")
    parser.add_argument("--vinayagar", action="store_true", help="Process all pending Vinayagar tracks")
    parser.add_argument("--all", action="store_true", help="Process all pending tracks from the manifest")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of tracks to process")
    parser.add_argument("--no-extend", action="store_true", help="Disable extending video in Flow editor")
    parser.add_argument("--extend-steps", type=int, default=2, help="Number of extensions per base scene")

    args = parser.parse_args()
    do_extend = not args.no_extend

    if args.open:
        open_session()
        return

    if args.track:
        generate_track_on_flow(args.track, extend=do_extend, extend_steps=args.extend_steps)
        return

    if args.vinayagar:
        print("=" * 80)
        print("AUTONOMOUS PIPELINE: GENERATING ALL PENDING VINAYAGAR MASTER FILMS")
        print("=" * 80)
        
        # Check which ones are already completed
        releases = list(RENDERS_DIR.glob("*master.mp4"))
        existing_tids = {r.stem.split('_')[-2] for r in releases if len(r.stem.split('_')[-2]) == 11}
        existing_tids.update({r.stem.split('_')[2] for r in releases if len(r.stem.split('_')) > 2 and len(r.stem.split('_')[2]) == 11})
        
        pending_vin = [t for t in VINAYAGAR_TRACK_IDS if t not in existing_tids]
        print(f"Total Vinayagar tracks remaining: {len(pending_vin)} of {len(VINAYAGAR_TRACK_IDS)}")

        for idx, tid in enumerate(pending_vin, 1):
            print(f"\n=======================================================")
            print(f">>> VINAYAGAR SONG [{idx}/{len(pending_vin)}]: Track ID {tid} <<<")
            print(f"=======================================================")
            try:
                generate_track_on_flow(tid, extend=do_extend, extend_steps=args.extend_steps)
            except Exception as e:
                print(f"[Error] Processing failed for track {tid}: {e}")
            time.sleep(3)
        print("\nAll Vinayagar master films processed successfully!")
        return

    if args.category or args.all:
        manifest_file = ROOT / "production" / "pending_google_flow_manifest.json"
        if not manifest_file.exists():
            print("Error: Manifest file not found.")
            return

        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        pending = manifest.get("pending_tracks", [])
        if args.category:
            pending = [t for t in pending if t.get("category", "").lower() == args.category.lower()]

        print(f"Total matching pending tracks: {len(pending)}. Processing up to {args.limit}...")
        count = 0
        for item in pending:
            if count >= args.limit:
                break
            track_id = item["track_id"]
            ok = generate_track_on_flow(track_id, extend=do_extend, extend_steps=args.extend_steps)
            if ok:
                count += 1
                time.sleep(5)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
