import sys
import time
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

VEDASARA_FULL = """பசூநாம் பதிம் பாபநாசம் பரீசம்
கஜேந்த்ரஸ்ய க்ருத்திம் வஸாநம் வரேண்யம்
ஜடாதாரினம் நீலகண்டம் மஹேசம்
பரமேச்வரம் அம்பிகாகாந்தமீசம் || 1 ||

பரேசம் மஹேசம் புஜங்கேச பூஷம்
பரவ்யோம வாசம் சுராணாம் நிவாஸம்
சிவம் சாந்தமீசான மீடே'பி நௌமி
மஹா தேவ சம்போ கிரீசாம்பிகேசம் || 2 ||

பொருள் விளக்கம் (Spiritual Meaning):
ஆதிசங்கர பகவற்பாதாள் அருளிய வேதஸார சிவ ஸ்தோத்திரம். அனைத்து உயிர்களுக்கும் தலைவரான, பாவங்களை நாசம் செய்கின்ற, அம்பிகையின் நாதரான பரமேஸ்வரனைப் போற்றித் தொழுகிறோம்."""

THIRUVAIYARU_FULL = """மாதர்ப் பிறைக் கண்ணியானை மலையான் மகளொடும் பாடிப்
போதொடு நீர்சுமந் தேத்திப் புகுவா ரவர்பின் புகுவேன்
யாதுஞ் சுவடு படாமல் ஐயா றடைகின்ற போது
காதன் மடப்பிடியோடும் களிறு வருவன கண்டேன்
கண்டேன் அவன்திருப் பாதங் கண்டறி யாதன கண்டேன்.

பொருள் விளக்கம் (Spiritual Meaning):
திருநாவுக்கரசர் பெருமான் திருவையாற்றில் சகல உயிர்களிலும் அம்மையப்பரின் சிவ-சக்தி தரிசனத்தைக் கண்டு உள்ளம் உருகிப் பாடிய அற்புதத் திருப்பதிகம்."""

def process_video(page, vid, label, lyrics):
    target_url = f"https://studio.youtube.com/video/{vid}/edit"
    print(f"\n==========================================")
    print(f"Loading {vid} ({label})...", flush=True)
    
    if vid not in page.url:
        page.goto(target_url, wait_until="domcontentloaded")
        time.sleep(5)
    else:
        time.sleep(2)
        
    print(f"Current page URL: {page.url}", flush=True)
    desc_elem = page.locator('#description-textarea #textbox').first
    existing_desc = desc_elem.inner_text()
    print(f"Existing desc len: {len(existing_desc)}")
    
    if "பாடல் வரிகள்" in existing_desc:
        parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
        new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
    elif "நமச்சிவாய வாழ்க" in existing_desc:
        idx = existing_desc.find("நமச்சிவாய வாழ்க")
        new_desc = existing_desc[:idx] + "பாடல் வரிகள் (Tamil Lyrics):\n" + lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
    else:
        new_desc = existing_desc + "\n\nபாடல் வரிகள் (Tamil Lyrics):\n" + lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
        
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
        print(f"SUCCESS: Saved {vid} ({label})!", flush=True)
    else:
        print(f"WARNING: Save not enabled for {vid}!")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        # 1. Process g42Pg2sg_gg
        process_video(page, "g42Pg2sg_gg", "Vedasaara Shiva Stotram", VEDASARA_FULL)
        
        # 2. Process rRoJfeRQiaM
        process_video(page, "rRoJfeRQiaM", "Thiruvaiyaru Thevaram", THIRUVAIYARU_FULL)
    finally:
        browser.close()
