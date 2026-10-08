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

def wait_for_assistant_and_approve(page, timeout_sec=40):
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

    return False

def wait_and_download_video(page, dest_mp4_path: Path, max_wait_sec=240):
    """Monitors the project workspace until the video completes, then downloads and extracts the MP4."""
    print(f"[Flow] Monitoring video render (up to {max_wait_sec}s)...")
    start_t = time.time()
    
    while time.time() - start_t < max_wait_sec:
        page.wait_for_timeout(6000)
        elapsed = int(time.time() - start_t)
        
        # Check for Download batch button on the video card
        dl_btn = page.locator("button[aria-label*='Download' i]").first
        if dl_btn.count() > 0 and dl_btn.is_visible():
            print(f"[Flow] Video ready! Initiating download (Elapsed: {elapsed}s)...")
            temp_zip = dest_mp4_path.parent / f"temp_{int(time.time())}.zip"
            
            try:
                with page.expect_download(timeout=30000) as download_info:
                    dl_btn.click()
                download = download_info.value
                download.save_as(str(temp_zip))
                
                # Check if it's a zip or direct mp4
                with open(temp_zip, "rb") as f:
                    header = f.read(16)
                    
                extracted_success = False
                if header.startswith(b"PK"):
                    with zipfile.ZipFile(temp_zip, "r") as z:
                        mp4_files = [m for m in z.namelist() if m.endswith(".mp4")]
                        if mp4_files:
                            extracted_path = z.extract(mp4_files[0], dest_mp4_path.parent)
                    if dest_mp4_path.exists():
                        dest_mp4_path.unlink()
                    shutil.move(extracted_path, dest_mp4_path)
                    print(f"[Flow] SUCCESS: Extracted {dest_mp4_path.name} ({dest_mp4_path.stat().st_size} bytes)")
                    extracted_success = True
                elif b"ftyp" in header:
                    if dest_mp4_path.exists():
                        dest_mp4_path.unlink()
                    shutil.move(temp_zip, dest_mp4_path)
                    print(f"[Flow] SUCCESS: Saved direct MP4 {dest_mp4_path.name} ({dest_mp4_path.stat().st_size} bytes)")
                    extracted_success = True
                
                try:
                    temp_zip.unlink(missing_ok=True)
                except Exception:
                    pass

                if extracted_success:
                    return True
            except Exception as e:
                print(f"[Flow] Download error: {e}")
                try:
                    temp_zip.unlink(missing_ok=True)
                except Exception:
                    pass

        print(f"[Flow] Waiting for render... {elapsed}s elapsed")

    print("[Flow] Timed out waiting for video render.")
    return False

def generate_track_on_flow(track_id: str):
    """Automates generating scenes for a track on flow.google.com and builds the master film."""
    from playwright.sync_api import sync_playwright

    matches = list(PROMPTS_DIR.glob(f"*/{track_id}*.md"))
    if not matches:
        print(f"Error: No blueprint found for track {track_id}")
        return False

    bp = parse_blueprint(matches[0])
    print("\n" + "=" * 80)
    print(f"GOOGLE FLOW AUTOMATION: {bp['title']}")
    print(f"Track ID: {bp['track_id']} | Category: {bp['category']} | Scenes: {len(bp['scenes'])}")
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

                # Click New project
                new_proj = page.locator("button:has-text('New project'), [role='button']:has-text('New project')").first
                if new_proj.count() > 0 and new_proj.is_visible():
                    print("[Flow] Creating fresh project...")
                    new_proj.click()
                    page.wait_for_timeout(6000)

                # Process each scene
                for sc in scenes_to_render:
                    sc_num = sc['scene_num']
                    out_clip = track_dir / f"scene_{sc_num:02d}.mp4"
                    prompt = f"Devotional cinematic 16:9 photorealistic video: {sc['prompt']} Exclusions: {sc.get('exclusions', '')} {bp['continuity'].get('Hard Exclusions', '')}"

                    print(f"\n[Scene {sc_num}] Submitting prompt...")
                    print(f"Prompt: {prompt[:140]}...")

                    editor = page.locator("div.ProseMirror").first
                    if editor.count() == 0:
                        print("[Flow Error] ProseMirror editor not found.")
                        break

                    editor.click()
                    page.wait_for_timeout(500)
                    page.keyboard.type(prompt, delay=8)
                    page.wait_for_timeout(1000)

                    gen_btn = page.locator("button[aria-label='Start generation']").first
                    if gen_btn.is_enabled():
                        gen_btn.click()
                        print(f"[Scene {sc_num}] Generation triggered. Waiting for approval...")
                        wait_for_assistant_and_approve(page)
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
        audio_path = ensure_audio(bp['track_id'])
        out_film = RENDERS_DIR / f"{bp['category'].lower()}_{bp['track_id']}_master.mp4"
        build_master_film(bp, existing_clips, audio_path, out_film)
        return True
    else:
        print(f"[Assembly Error] No scenes available for {bp['track_id']}.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Google Flow Browser Automation Bridge")
    parser.add_argument("--open", action="store_true", help="Open Chrome to inspect flow.google.com")
    parser.add_argument("--track", type=str, help="Process a specific track by Track ID")
    parser.add_argument("--category", type=str, help="Process a category of tracks")
    parser.add_argument("--all", action="store_true", help="Process all pending tracks from the manifest")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of tracks to process")

    args = parser.parse_args()

    if args.open:
        open_session()
        return

    if args.track:
        generate_track_on_flow(args.track)
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
            ok = generate_track_on_flow(track_id)
            if ok:
                count += 1
                time.sleep(5)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
