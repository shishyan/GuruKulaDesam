import sys
import time
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PANCHARATNAM_5_VERSES = """முதாகராத்த மோதகம் ஸதா விமுக்தி ஸாதகம்
களாதராவதம்ஸகம் விலாஸிலோக ரக்ஷகம் |
அநாயகைக நாயகம் வினாஶிதேப தைத்யகம்
நதாஶுபாஶு நாஶகம் நமாமி தம் விநாயகம் || 1 ||

நதேதராதி பீகரம் நவோதிதார்க பாஸ்வரம்
நமத்ஸுராரி நிர்ஜரம் நதாதிகாபதுத்தரம் |
ஸுரேஶ்வரம் நிதீஶ்வரம் கஜேஶ்வரம் கணேஶ்வரம்
மஹேஶ்வரம் தமாஶ்ரயே பராத்பரம் நிரந்தரம் || 2 ||

ஸமஸ்த லோக ஶங்கரம் நிரஸ்த தைத்ய குஞ்ஜரம்
தரேதரோதரம் வரம் வரேப வக்த்ரமக்ஷரம் |
க்ருபாகரம் க்ஷமாகரம் முதாகரம் யஶஸ்கரம்
மனஸ்கரம் நமஸ்க்ருதாம் நமஸ்கரோமி பாஸ்வரம் || 3 ||

அகிஞ்சனார்தி மார்ஜனம் சிரந்தனோக்தி பாஜனம்
புராரி பூர்வ நந்தனம் ஸுராரி கர்வ சர்வணம் |
ப்ரபஞ்ச நாஶ பீஷணம் தனஞ்ஜயாதி பூஷணம்
கபோல தானவாரணம் பஜே புராண வாரணம் || 4 ||

நிதாந்த காந்த தந்த காந்தி மந்தகாந்த காத்மஜம்
அசிந்த்ய ரூப மந்தஹீன மந்தராய க்ருந்தனம் |
ஹ்ருதந்தரே நிரந்தரம் வஸந்தமேவ யோகினாம்
தமேகதந்தமேவ தம் விசிந்தயாமி ஸந்ததம் || 5 ||"""

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        vid = "udRsA-oWxS0"
        
        print("Navigating to about:blank to unmount previous video...", flush=True)
        page.goto("about:blank")
        time.sleep(2)
        
        target_url = f"https://studio.youtube.com/video/{vid}/edit"
        print(f"Navigating to {target_url}...", flush=True)
        page.goto(target_url, wait_until="domcontentloaded")
        time.sleep(5)
        
        print(f"Current page URL: {page.url}", flush=True)
        assert vid in page.url, f"Expected {vid} in URL, got {page.url}"
        
        desc_elem = page.locator('#description-textarea #textbox').first
        existing_desc = desc_elem.inner_text()
        print(f"Existing desc length: {len(existing_desc)} chars")
        
        # Replace between separators
        pattern = r'(பாடல் வரிகள்.*?═════════════════════════════════════════════════════════════════\n)(.*?)(\n═════════════════════════════════════════════════════════════════\s*📖)'
        m = re.search(pattern, existing_desc, flags=re.DOTALL)
        if m:
            new_desc = existing_desc[:m.start(2)] + PANCHARATNAM_5_VERSES + existing_desc[m.end(2):]
        else:
            new_desc = existing_desc.replace("முதாகராத்த மோதகம் ஸதா விமுக்தி சாதகம்\nகலாதராவதம்ஸகம் விலாஸிலோகரக்ஷகம்\nஅநாயகைக நாயகம் விநாசிதேப தைத்யகம்\nநதாசுபாசு நாசகம் நமாமி தம் விநாயகம்!", PANCHARATNAM_5_VERSES)
            
        print(f"New desc length: {len(new_desc)} chars. Inserting...", flush=True)
        desc_elem.click()
        page.keyboard.press("Control+A")
        page.keyboard.insert_text(new_desc)
        time.sleep(2)
        
        save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save"), button:has-text("Save")').first
        if save_btn.is_enabled():
            save_btn.click()
            print("Clicked Save! Waiting 5s...", flush=True)
            time.sleep(5)
            print("SUCCESS! Saved udRsA-oWxS0!")
        else:
            print("Save button not enabled!")
    finally:
        browser.close()
