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

THIYAGA_VANNA_PATHIGAM_FULL = """காரார் குழலாள் உமையோ டயில்வேல்
காளையொ டுந்தான் அமர்கின்ற
ஏரார் கோலம் கண்டு களிப்பான்
எண்ணும் எமக்கொன் றருளானேல்
நீரார் சடைமேல் பிறையொன் றுடையான்
நிதிக்கோன் தோழன் எனநின்றான்
பேரார் ஒற்றி யூரான் தியாகப்
பெருமான் பிச்சைப் பெருமானே.

பொருள் விளக்கம் (Spiritual Meaning):
வள்ளலார் இராமலிங்க அடிகளார் திருவொற்றியூரில் எழுந்தருளியுள்ள தியாகப்பெருமானை, உமையம்மையோடும் முருகப்பெருமானோடும் வீற்றிருக்கும் திருக்கோலத்தைக் கண்டு களித்து உள்ளம் உருகிப் போற்றிய அற்புதத் திருவருட்பாப் பாடல்."""

TARGETS = [
    ("g42Pg2sg_gg", "Vedasaara Shiva Stotram", VEDASARA_FULL),
    ("rRoJfeRQiaM", "Thiruvaiyaru Thevaram", THIRUVAIYARU_FULL),
    ("jZFTlpJwn6A", "Thiyaga Vanna Pathigam", THIYAGA_VANNA_PATHIGAM_FULL)
]

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        for vid, label, canonical_lyrics in TARGETS:
            print(f"\n==========================================")
            print(f"Loading {vid} ({label})...", flush=True)
            
            # Fresh hard navigation
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded")
            time.sleep(5)
            
            # Verify URL
            print(f"Page loaded: {page.url}")
            
            desc_elem = page.locator('#description-textarea #textbox').first
            existing_desc = desc_elem.inner_text()
            print(f"Current description ({len(existing_desc)} chars):\n{repr(existing_desc[:120])}")
            
            # Format replacement
            if "பாடல் வரிகள்" in existing_desc:
                parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
                new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + canonical_lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
            elif "நமச்சிவாய வாழ்க" in existing_desc:
                idx = existing_desc.find("நமச்சிவாய வாழ்க")
                new_desc = existing_desc[:idx] + "பாடல் வரிகள் (Tamil Lyrics):\n" + canonical_lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
            else:
                new_desc = existing_desc + "\n\nபாடல் வரிகள் (Tamil Lyrics):\n" + canonical_lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
                
            print(f"Prepared new desc ({len(existing_desc)} -> {len(new_desc)} chars). Injecting...", flush=True)
            desc_elem.click()
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(new_desc)
            time.sleep(2)
            
            save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save"), button:has-text("Save")').first
            if save_btn.is_enabled():
                save_btn.click()
                print("Clicked Save! Waiting 6s for toast...", flush=True)
                time.sleep(6)
                print(f"SUCCESS: Saved {vid} ({label})!", flush=True)
            else:
                print(f"WARNING: Save button not enabled for {vid}!", flush=True)
                
            time.sleep(2)
            
    finally:
        browser.close()
