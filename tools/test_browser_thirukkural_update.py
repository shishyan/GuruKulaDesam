import sys, json, time, re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# 1. Load Kurals
data = json.load(open('production/thirukkural_all.json', encoding='utf-8'))
kurals = data['kural']

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
    vid = "IHMZsM7LJf8"
    chap = 74
    kural_block = build_kural_block(chap)
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        url = f"https://studio.youtube.com/video/{vid}/edit"
        print(f"Navigating to {url}...", flush=True)
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(6)
        
        desc_box = page.locator('#description-textarea #textbox, [aria-label*="Description"]').first
        if not desc_box.is_visible():
            print("ERROR: Desc box not visible!")
            return
            
        current_desc = desc_box.inner_text()
        print(f"Current description length: {len(current_desc)} chars")
        
        if "📜 திருக்குறள் பாடல் வரிகள்" in current_desc or "குறள் 731:" in current_desc:
            print("Video already has canonical Kurals! Skipping.")
            return
            
        # Build new description preserving existing header & hashtags
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
            
        new_desc = f"{header}\n\n{kural_block}{footer}"
        print(f"New description length: {len(new_desc)} chars")
        
        # Insert into textbox
        desc_box.click()
        page.keyboard.press("Control+A")
        page.keyboard.insert_text(new_desc)
        time.sleep(2)
        
        # Click Save
        save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save")').first
        if save_btn.is_enabled():
            save_btn.click()
            print("Clicked Save! Waiting 5s...", flush=True)
            time.sleep(5)
            print(f"SUCCESS: {vid} (Chapter {chap}) successfully updated and saved live!", flush=True)
        else:
            print("WARNING: Save button was not enabled.")
            
    finally:
        browser.close()
        p.stop()

if __name__ == "__main__":
    main()
