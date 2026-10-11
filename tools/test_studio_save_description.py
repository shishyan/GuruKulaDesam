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

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    vid = "uPk4dyag74Y"
    url = f"https://studio.youtube.com/video/{vid}/edit"
    print(f"Navigating to {url}...", flush=True)
    page.goto(url, wait_until="domcontentloaded")
    time.sleep(5)
    
    print(f"Current page URL: {page.url}", flush=True)
    
    # 1. Inspect existing description
    existing_desc = page.evaluate('''() => {
        const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
        return descBox ? descBox.innerText : null;
    }''')
    
    if not existing_desc:
        print("ERROR: Description box not found!", flush=True)
        sys.exit(1)
        
    print(f"Found existing description ({len(existing_desc)} chars).", flush=True)
    
    # Replace generic Gana Natha chant with Thigada Sakkara
    if "கண நாதா ஓம்" in existing_desc:
        print("Found 'கண நாதா ஓம்' in description! Replacing...", flush=True)
        # We replace the lyrics section
        import re
        # Find start of lyrics section
        parts = re.split(r'📜\s*பாடல் வரிகள்.*?═════════════════════════════════════════════════════════════════', existing_desc, flags=re.DOTALL)
        if len(parts) >= 2:
            before_lyrics = parts[0] + "📜 பாடல் வரிகள் (CANONICAL TAMIL SCRIPTURE LYRICS)\n═════════════════════════════════════════════════════════════════\n"
            # find end of lyrics before translation/credits
            after_parts = re.split(r'═════════════════════════════════════════════════════════════════\s*📖', parts[1], flags=re.DOTALL)
            if len(after_parts) >= 2:
                after_lyrics = "\n\n═════════════════════════════════════════════════════════════════\n📖" + after_parts[1]
                new_desc = before_lyrics + THIGADA_CORRECT_LYRICS + after_lyrics
            else:
                new_desc = before_lyrics + THIGADA_CORRECT_LYRICS + "\n\n" + parts[1]
        else:
            new_desc = existing_desc.replace("கண நாதா ஓம்", THIGADA_CORRECT_LYRICS)
    else:
        print("Existing description does not contain 'கண நாதா ஓம்'.", flush=True)
        new_desc = existing_desc
        
    # Inject into description box
    res = page.evaluate('''(newText) => {
        const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
        if (!descBox) return { success: false, error: 'no desc box' };
        
        descBox.focus();
        // Select all and replace
        document.execCommand('selectAll', false, null);
        document.execCommand('insertText', false, newText);
        
        // Dispatch input event so YouTube detects changes
        descBox.dispatchEvent(new Event('input', { bubbles: true }));
        descBox.dispatchEvent(new Event('change', { bubbles: true }));
        
        const saveBtn = document.querySelector('#save-button, ytcp-button#save-button');
        return {
            success: true,
            newLen: descBox.innerText.length,
            saveBtnDisabled: saveBtn ? saveBtn.getAttribute('disabled') : 'no button'
        };
    }''', new_desc)
    
    print("Injection result:", res, flush=True)
    time.sleep(2)
    
    # Click Save if enabled
    save_res = page.evaluate('''() => {
        const saveBtn = document.querySelector('#save-button, ytcp-button#save-button');
        if (saveBtn && !saveBtn.hasAttribute('disabled') && saveBtn.getAttribute('aria-disabled') !== 'true') {
            saveBtn.click();
            return { clicked: true };
        }
        return { clicked: false, attr: saveBtn ? saveBtn.getAttribute('disabled') : 'none' };
    }''')
    print("Save button click result:", save_res, flush=True)
    time.sleep(4)
    
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/after_thigada_save.png")
    print("Saved screenshot to after_thigada_save.png", flush=True)
