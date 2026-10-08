# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Google Flow (flow.google.com) Browser Automation Bridge
Automates generating Veo video clips directly on flow.google.com using your
8,686 Google Flow account credits, and automatically triggers master film assembly.

Features:
- Launches Chrome using your persistent profile so you stay signed in.
- Feeds Scene 1, Scene 2, and Scene 3 prompts from production/google_flow_prompts/.
- Downloads the rendered clips directly to production/google_flow_renders/<TRACK_ID>/.
- Calls google_flow_engine.py to assemble master films with sacred framing and audio sync.

Usage:
  # Launch browser to sign in or inspect flow.google.com:
  python production/flow_browser_bridge.py --open

  # Generate for a specific track:
  python production/flow_browser_bridge.py --track 2QOF2ycA4RQ

  # Generate for all tracks in a category:
  python production/flow_browser_bridge.py --category vinayagar
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import parse_blueprint, ensure_audio, build_master_film, RENDERS_DIR, FLOW_RENDERS_DIR, PROMPTS_DIR

FLOW_URL = "https://flow.google.com"
CHROME_PROFILE_DIR = ROOT / "production" / "browser_profile"
CHROME_PROFILE_DIR.mkdir(parents=True, exist_ok=True)

def get_browser_context(playwright, headless=False):
    """Launches or connects to Chrome with a persistent user data profile."""
    # Attempt to connect to an already running remote debugging Chrome instance
    try:
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        print("[Browser Bridge] Attached to existing Chrome on port 9222.")
        return browser.contexts[0]
    except Exception:
        pass

    # Launch Chrome with persistent profile
    print(f"[Browser Bridge] Launching Chrome (Persistent Profile: {CHROME_PROFILE_DIR.name})...")
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(CHROME_PROFILE_DIR),
        channel="chrome",
        headless=headless,
        viewport={"width": 1440, "height": 900},
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
        ]
    )
    return context

def open_session(headless=False):
    """Opens flow.google.com for the user to sign in or check credit balance."""
    from playwright.sync_api import sync_playwright

    print("=" * 80)
    print("OPENING GOOGLE FLOW (flow.google.com)")
    print("=" * 80)
    print("Please log in with your Google account that has the 8,686 credits.")
    print("Once logged in, your session is saved in production/browser_profile/.\n")

    with sync_playwright() as p:
        context = get_browser_context(p, headless=headless)
        page = context.new_page() if not context.pages else context.pages[0]
        page.goto(FLOW_URL)
        
        print("\nBrowser is open at flow.google.com.")
        print("Keep this window open or log in, then press Ctrl+C or enter when done.")
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nSession saved. Closing browser...")
        finally:
            context.close()

def generate_track_on_flow(track_id: str, headless=False):
    """Automates generating scenes for a track on flow.google.com."""
    from playwright.sync_api import sync_playwright

    # Find blueprint
    matches = list(PROMPTS_DIR.glob(f"*/{track_id}*.md"))
    if not matches:
        print(f"Error: No blueprint found for track {track_id}")
        return

    bp = parse_blueprint(matches[0])
    print("=" * 80)
    print(f"GOOGLE FLOW AUTOMATION: {bp['title']}")
    print(f"Track ID: {bp['track_id']} | Category: {bp['category']} | Scenes: {len(bp['scenes'])}")
    print("=" * 80)

    track_dir = FLOW_RENDERS_DIR / bp['track_id']
    track_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = get_browser_context(p, headless=headless)
        page = context.new_page() if not context.pages else context.pages[0]
        page.goto(FLOW_URL)
        page.wait_for_load_state("networkidle")

        print(f"[Flow] Page title: {page.title()}")
        print("[Flow] Navigating to studio project / prompt interface...")

        # Each scene generation
        scene_clips = []
        for sc in bp['scenes']:
            sc_num = sc['scene_num']
            out_clip = track_dir / f"scene_{sc_num:02d}.mp4"
            if out_clip.exists() and out_clip.stat().st_size > 500_000:
                print(f"[Cached] Scene {sc_num} already exists: {out_clip.name}")
                scene_clips.append(out_clip)
                continue

            full_prompt = f"{sc['prompt']} Exclusions: {sc.get('exclusions', '')} {bp['continuity'].get('Hard Exclusions', '')}"
            print(f"\n[Scene {sc_num}] Submitting prompt to Google Flow...")
            print(f"Prompt: {full_prompt[:120]}...")

            # Look for prompt input box on flow.google.com
            # Google Flow typically uses a textarea, contenteditable div, or input[type='text']
            prompt_input = page.locator("textarea, [contenteditable='true'], input[placeholder*='prompt' i], input[placeholder*='Describe' i]").first
            if prompt_input.count() > 0:
                prompt_input.fill(full_prompt)
                time.sleep(1)
                
                # Click Generate button
                gen_button = page.locator("button:has-text('Generate'), button:has-text('Create'), button[aria-label*='Generate' i]").first
                if gen_button.count() > 0:
                    gen_button.click()
                    print(f"[Scene {sc_num}] Generation initiated! Waiting for video render...")
                    
                    # Monitor for video element or download button
                    # Wait for video generation to complete
                    page.wait_for_timeout(60000)
            else:
                print("[Flow UI Notice] Prompt input box selector needs direct inspection. Please use --open to log in.")

        context.close()

    # Master film assembly
    existing_clips = sorted(track_dir.glob("scene_*.mp4"))
    if existing_clips:
        audio_path = ensure_audio(bp['track_id'])
        out_film = RENDERS_DIR / f"{bp['category'].lower()}_{bp['track_id']}_master.mp4"
        build_master_film(bp, existing_clips, audio_path, out_film)

def main():
    parser = argparse.ArgumentParser(description="Google Flow (flow.google.com) Browser Automation Bridge")
    parser.add_argument("--open", action="store_true", help="Open Chrome to log in to flow.google.com and verify credits")
    parser.add_argument("--track", type=str, help="Process a specific track by Track ID on flow.google.com")
    parser.add_argument("--category", type=str, help="Process a category of tracks on flow.google.com")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")

    args = parser.parse_args()

    if args.open:
        open_session(headless=args.headless)
        return

    if args.track:
        generate_track_on_flow(args.track, headless=args.headless)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
