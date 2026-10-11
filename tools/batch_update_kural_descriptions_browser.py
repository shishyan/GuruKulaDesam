import sys, json, time, re, pathlib
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROGRESS_FILE = ROOT / "production" / "kural_descriptions_browser_progress.json"

# Load Kurals
kural_data = json.load(open(ROOT / 'production' / 'thirukkural_all.json', encoding='utf-8'))
kurals = kural_data['kural']

# Load target list
audit_data = json.load(open(ROOT / 'production' / 'all_flawed_descriptions_audit.json', encoding='utf-8'))
no_lyrics = audit_data.get('no_lyrics_at_all', [])

targets = []
for item in no_lyrics:
    t = item.get('title', '')
    m = re.search(r'அதிகாரம்\s*(\d+)', t)
    if m:
        targets.append({'chap': int(m.group(1)), 'vid': item['id'], 'title': t})

targets.sort(key=lambda x: x['chap'])

def build_kural_block(chap_num):
    start = (chap_num - 1) * 10 + 1
    end = chap_num * 10
    chap_kurals = [k for k in kurals if start <= k.get('Number', 0) <= end]
    lines = []
    lines.append("📜 திருக்குறள் பாடல் வரிகள் & பொருள் (Thirukkural Verses & Meaning):")
    lines.append("═════════════════════════════════════════════════════════════════")
    for k in chap_kurals:
        num = k.get('Number')
        l1 = k.get('Line1', '').strip()
        l2 = k.get('Line2', '').strip()
        m = (k.get('mv') or k.get('sp') or k.get('mk') or '').strip()
        lines.append(f"குறள் {num}:")
        lines.append(f"{l1}")
        lines.append(f"{l2}")
        if m:
            lines.append(f"விளக்கம்: {m}")
        lines.append("")
    lines.append("═════════════════════════════════════════════════════════════════")
    return "\n".join(lines).strip()

def main():
    progress = {}
    if PROGRESS_FILE.exists():
        try:
            progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
        except Exception:
            progress = {}

    # Mark IHMZsM7LJf8 as done since we already verified it live
    if "IHMZsM7LJf8" not in progress:
        progress["IHMZsM7LJf8"] = {'done': True, 'action': 'saved_browser', 'chap': 74, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')}
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

    print(f"Loaded {len(targets)} Thirukkural chapter targets.")
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        # Auto-accept any navigation dialogs
        page.on("dialog", lambda dialog: dialog.accept())
        
        for idx, row in enumerate(targets, 1):
            vid = row['vid']
            chap = row['chap']
            title = row['title']
            
            if progress.get(vid, {}).get('done'):
                print(f"[{idx}/{len(targets)}] Already done: {vid} (Chap {chap})")
                continue
                
            print(f"\n[{idx}/{len(targets)}] Processing {vid} (Chap {chap}): {title[:40]}...", flush=True)
            url = f"https://studio.youtube.com/video/{vid}/edit"
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(5)
            
            desc_box = page.locator('#description-textarea #textbox, [aria-label*="Description"]').first
            if not desc_box.is_visible():
                print(f"  ERROR: Desc box not visible for {vid}! Trying once more after 3s...", flush=True)
                time.sleep(3)
                if not desc_box.is_visible():
                    print(f"  SKIPPING {vid}: element not found.")
                    progress[vid] = {'done': False, 'error': 'desc_box_not_visible'}
                    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                        json.dump(progress, f, indent=2, ensure_ascii=False)
                    continue
                    
            current_desc = desc_box.inner_text()
            
            # Check if canonical kurals already present
            sample_kural_num = f"குறள் {(chap - 1) * 10 + 1}:"
            if "📜 திருக்குறள் பாடல் வரிகள்" in current_desc or sample_kural_num in current_desc:
                print(f"  Already has canonical kurals! Marking done.")
                progress[vid] = {'done': True, 'action': 'already_present'}
                with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(progress, f, indent=2, ensure_ascii=False)
                continue
                
            kural_block = build_kural_block(chap)
            
            header = ""
            footer = ""
            if "#Thirukkural" in current_desc:
                parts = current_desc.split("#Thirukkural")
                header = parts[0].strip()
                footer = "\n\n#Thirukkural" + parts[1].strip()
            elif "— குரு குல தேசம்" in current_desc:
                parts = current_desc.split("— குரு குல தேசம்")
                header = parts[0].strip()
                footer = "\n\n— குரு குல தேசம்" + parts[1].strip()
            else:
                header = current_desc.strip()
                footer = "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
                
            new_desc = f"{header}\n\n{kural_block}{footer}".strip()
            if len(new_desc) > 4950:
                print(f"  Warning: Description length {len(new_desc)} exceeds safety limit, trimming footer.")
                new_desc = f"{header}\n\n{kural_block}\n\n— குரு குல தேசம் | Guru Kula Desam".strip()
                
            print(f"  Inserting new description ({len(current_desc)} -> {len(new_desc)} chars)...", flush=True)
            desc_box.click()
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(new_desc)
            time.sleep(2)
            
            save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save")').first
            if save_btn.is_enabled():
                save_btn.click()
                print(f"  Clicked Save! Waiting 5s...", flush=True)
                time.sleep(5)
                progress[vid] = {
                    'done': True,
                    'action': 'saved_browser',
                    'chap': chap,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                print(f"  SUCCESS: {vid} (Chap {chap}) saved live!", flush=True)
            else:
                print(f"  WARNING: Save button was disabled for {vid}!")
                progress[vid] = {'done': False, 'error': 'save_disabled'}
                
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
                
            time.sleep(1)
            
    finally:
        try:
            browser.disconnect()
        except Exception:
            pass
        p.stop()
        
    print("\n" + "=" * 60)
    print("ALL THIRUKKURAL CHAPTER DESCRIPTIONS PROCESSED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
