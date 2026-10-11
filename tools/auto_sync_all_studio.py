import sys
import os
import time
import json
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = os.path.abspath(".")
ovr = json.load(open("production/youtube_lyrics_overrides.json", encoding='utf-8'))
works = ovr.get('_works', {})
channel_vids = json.load(open("production/youtube_backup/videos.json", encoding='utf-8'))
cat = json.load(open("assets/data/catalog.json", encoding='utf-8'))

PROGRESS_FILE = "production/studio_autosync_progress.json"
if os.path.exists(PROGRESS_FILE):
    try:
        progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
    except Exception:
        progress = {}
else:
    progress = {}

def save_progress():
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

# Build catalog lookup
cat_by_clean_title = {}
cat_by_id = {}
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        sid = s.get('id')
        if sid: cat_by_id[sid] = s
        t = re.sub(r'\[.*?\]', '', s.get('title', '')).strip()
        if t: cat_by_clean_title[t] = s

def get_clean_lyrics(v):
    vid = v['id']
    title = v['snippet']['title']
    lyrics = None
    if vid in ovr:
        ref = ovr[vid].get('ref')
        if ref and ref in works:
            lyrics = works[ref].get('lyrics')
    if not lyrics and vid in cat_by_id:
        lyrics = cat_by_id[vid].get('lyrics')
    if not lyrics:
        clean_t = re.sub(r'\[.*?\]', '', title).strip()
        for ct, cs in cat_by_clean_title.items():
            if ct in clean_t or clean_t in ct:
                lyrics = cs.get('lyrics')
                break
    if not lyrics:
        return None

    # Clean lyrics of markdown/dividers
    lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
    clean = []
    for l in lines:
        if l.startswith('═') or l.startswith('---') or l.startswith('##') or l.startswith('குறள்'):
            continue
        l = re.sub(r'\|\|\s*\d+\s*\|\|', '', l).strip()
        if l:
            clean.append(l)
    return "\n".join(clean)

def run():
    print("Connecting to Chrome on port 9225...", flush=True)
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
        except Exception as e:
            print(f"ERROR: Could not connect to port 9225: {e}")
            print("Please ensure Chrome was launched with --remote-debugging-port=9225")
            return

        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        total = len(channel_vids)
        print(f"Total videos to check: {total}", flush=True)

        for i, v in enumerate(channel_vids, 1):
            vid = v['id']
            title = v['snippet']['title']

            if progress.get(vid, {}).get('done'):
                continue

            lyrics = get_clean_lyrics(v)
            if not lyrics:
                print(f"[{i}/{total}] Skipping {vid} (No lyrics found)")
                progress[vid] = {'done': True, 'skipped': True}
                save_progress()
                continue

            print(f"\n[{i}/{total}] Processing {vid}: {title[:40]}...", flush=True)
            url = f"https://studio.youtube.com/video/{vid}/translations"
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(3)

            # Look for "Edit subtitles" or "Edit" button
            # In Studio translations:
            edit_btn = page.locator("button, ytcp-button").filter(has_text=re.compile(r"Edit subtitles|Edit", re.I)).first
            if not edit_btn.is_visible():
                # check if there is "Add" button
                add_btn = page.locator("button, ytcp-button").filter(has_text=re.compile(r"Add", re.I)).first
                if add_btn.is_visible():
                    edit_btn = add_btn

            if not edit_btn or not edit_btn.is_visible():
                print(f"  Could not find Edit/Add button on {vid}")
                continue

            print("  Clicking Edit subtitles...", flush=True)
            edit_btn.click()
            time.sleep(2.5)

            # Now check for "Edit as text" toggle if available
            edit_as_text = page.locator("#toggle-button, text='Edit as text'").first
            if edit_as_text.is_visible():
                print("  Clicking 'Edit as text' for Auto-sync...", flush=True)
                edit_as_text.click()
                time.sleep(1.5)

            # Check if text box exists and populate clean lyrics if empty or needs update
            textarea = page.locator("textarea, ytcp-text-area, #content-text").first
            if textarea.is_visible():
                val = textarea.input_value() if hasattr(textarea, 'input_value') else ''
                if len(val.strip()) < 10:
                    print("  Pasting clean lyrics into Auto-sync box...", flush=True)
                    textarea.fill(lyrics)
                    time.sleep(1)

            # Find and click "Publish"
            publish_btn = page.locator("#publish-button, button:has-text('Publish'), ytcp-button:has-text('Publish')").first
            if publish_btn.is_visible():
                print("  Clicking Publish...", flush=True)
                publish_btn.click()
                time.sleep(3)
                print(f"  -> SUCCESS: Published & Auto-sync queued for {vid}!", flush=True)
                progress[vid] = {'done': True, 'timestamp': time.time()}
                save_progress()
            else:
                print("  Publish button not found/not enabled.")

if __name__ == '__main__':
    run()
