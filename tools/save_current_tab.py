import sys
import time
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

THIRUVAIYARU_FULL = """மாதர்ப் பிறைக் கண்ணியானை மலையான் மகளொடும் பாடிப்
போதொடு நீர்சுமந் தேத்திப் புகுவா ரவர்பின் புகுவேன்
யாதுஞ் சுவடு படாமல் ஐயா றடைகின்ற போது
காதன் மடப்பிடியோடும் களிறு வருவன கண்டேன்
கண்டேன் அவன்திருப் பாதங் கண்டறி யாதன கண்டேன்.

பொருள் விளக்கம் (Spiritual Meaning):
திருநாவுக்கரசர் பெருமான் திருவையாற்றில் சகல உயிர்களிலும் அம்மையப்பரின் சிவ-சக்தி தரிசனத்தைக் கண்டு உள்ளம் உருகிப் பாடிய அற்புதத் திருப்பதிகம்."""

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        vid = "rRoJfeRQiaM"
        print(f"Current page URL: {page.url}")
        assert vid in page.url, f"Expected {vid} in URL, got {page.url}"
        
        desc_elem = page.locator('#description-textarea #textbox').first
        existing_desc = desc_elem.inner_text()
        print(f"Existing desc length: {len(existing_desc)}")
        
        if "பாடல் வரிகள்" in existing_desc:
            parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
            new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + THIRUVAIYARU_FULL + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
        else:
            new_desc = existing_desc + "\n\nபாடல் வரிகள் (Tamil Lyrics):\n" + THIRUVAIYARU_FULL + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
            
        print(f"Injecting ({len(existing_desc)} -> {len(new_desc)} chars)...", flush=True)
        desc_elem.click()
        page.keyboard.press("Control+A")
        page.keyboard.insert_text(new_desc)
        time.sleep(2)
        
        save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save"), button:has-text("Save")').first
        if save_btn.is_enabled():
            save_btn.click()
            print("Clicked Save! Waiting 6s...", flush=True)
            time.sleep(6)
            print(f"SUCCESS: Saved {vid}!")
        else:
            print("WARNING: Save button not enabled!")
    finally:
        browser.close()
