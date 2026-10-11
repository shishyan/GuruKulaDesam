import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

THIGADA_CORRECT_LYRICS = """திகட சக்கரச் செம்முக மைந்துளான்
சகட சக்கரத் தாமரை நாயகன்
அகட சக்கர வின்மணி யாவுறை
விகட சக்கரன் மெய்ப்பதம் போற்றுவாம்.

பொருள் விளக்கம் (Spiritual Meaning):
கந்த புராணத்தின் தொடக்கக் காப்புச் செய்யுள். கச்சியப்ப சிவாச்சாரியார் நூலைத் தொடங்கும் முன் விநாயகப் பெருமானின் திருவடிகளைப் போற்றி வணங்குகிறார் என்பது இதன் கருத்து."""

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
try:
    page = browser.contexts[0].pages[0]
    vid = "uPk4dyag74Y"
    url = f"https://studio.youtube.com/video/{vid}/edit"
    print(f"Navigating to {url}...", flush=True)
    page.goto(url, wait_until="domcontentloaded")
    time.sleep(5)
    
    # 1. Get existing description
    desc_elem = page.locator('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox').first
    existing_desc = desc_elem.inner_text()
    print(f"Existing desc length: {len(existing_desc)}")
    
    # 2. Check if already updated or needs replace
    if "திகட சக்கரச் செம்முக" in existing_desc:
        print("Already contains Thigada Sakkara lyrics!")
    elif "கண நாதா ஓம்" in existing_desc:
        print("Replacing 'கண நாதா ஓம்' with Thigada Sakkara...")
        import re
        parts = re.split(r'📜\s*பாடல் வரிகள்.*?═════════════════════════════════════════════════════════════════', existing_desc, flags=re.DOTALL)
        if len(parts) >= 2:
            before_lyrics = parts[0] + "📜 பாடல் வரிகள் (CANONICAL TAMIL SCRIPTURE LYRICS)\n═════════════════════════════════════════════════════════════════\n"
            after_parts = re.split(r'═════════════════════════════════════════════════════════════════\s*📖', parts[1], flags=re.DOTALL)
            if len(after_parts) >= 2:
                after_lyrics = "\n\n═════════════════════════════════════════════════════════════════\n📖" + after_parts[1]
                new_desc = before_lyrics + THIGADA_CORRECT_LYRICS + after_lyrics
            else:
                new_desc = before_lyrics + THIGADA_CORRECT_LYRICS + "\n\n" + parts[1]
        else:
            new_desc = existing_desc.replace("கண நாதா ஓம்", THIGADA_CORRECT_LYRICS)
            
        # Focus and fill
        desc_elem.click()
        page.keyboard.press("Control+A")
        # In Playwright, fill or insertText
        page.keyboard.insert_text(new_desc)
        time.sleep(2)
        print("Inserted new description. Now searching for Save button...")
        
        # In YouTube Studio, the save button is #save or [aria-label="Save"] or text "Save"
        # Let's inspect candidate buttons
        save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save"), button:has-text("Save")').first
        print("Save button visible:", save_btn.is_visible(), "enabled:", save_btn.is_enabled())
        if save_btn.is_enabled():
            save_btn.click()
            print("Clicked Save button! Waiting 5s...")
            time.sleep(5)
            # Check for toast notification or save button disabled
            print("After click, save button enabled:", save_btn.is_enabled())
        else:
            print("Save button is not enabled!")
            
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/test_thigada_after_save.png")
    print("Screenshot saved to test_thigada_after_save.png")
finally:
    browser.close()
    p.stop()
