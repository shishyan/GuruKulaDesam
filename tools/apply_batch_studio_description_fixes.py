import sys
import time
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

LYRICS_MAP = {
    "thigada": """திகட சக்கரச் செம்முக மைந்துளான்
சகட சக்கரத் தாமரை நாயகன்
அகட சக்கர வின்மணி யாவுறை
விகட சக்கரன் மெய்ப்பதம் போற்றுவாம்.

பொருள் விளக்கம் (Spiritual Meaning):
கந்த புராணத்தின் தொடக்கக் காப்புச் செய்யுள். கச்சியப்ப சிவாச்சாரியார் நூலைத் தொடங்கும் முன் விநாயகப் பெருமானின் திருவடிகளைப் போற்றி வணங்குகிறார் என்பது இதன் கருத்து.""",

    "pancharatnam": """முதாகராத்த மோதகம் ஸதா விமுக்தி ஸாதகம்
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
தமேகதந்தமேவ தம் விசிந்தயாமி ஸந்ததம் || 5 ||

பொருள் விளக்கம் (Spiritual Meaning):
ஆதிசங்கரர் அருளிய ஐந்து ஸ்லோகங்களிலும் விநாயகப் பெருமானின் மோதகம் ஏந்திய திருக்கரம், பிறைசூடிய அழகு, கஜமுகாசுரனை அழித்த வீரம், வணங்குவோரின் துன்பம் நீக்கும் கருணை, ஒற்றைத் தந்த திருவுருவம் ஆகியவை போற்றப்படுகின்றன.""",

    "thirupulambal": """பூங்கமலத் தயனொடுமால் அறியா நெறி பூவணத்தாய்
தாங்குசடை முடியானே தையலாள் ஓர் பாகத்தாய்
ஏங்குமடியவர்க் கருளும் ஈசனே எம்பெருமான்
பாங்குடைய நின்னடியே பணியுமா பணியாயே.

பாரொடு விண் ணீரனல் காலாகி நின்றாய்
ஆரொருவர் காண்கிற்பார் அன்னே உனைக்காணார்
சீரொடு நின்னடியே சிந்திப்பார் சிந்தையுள்
நீரொழுக நின்ற நெறியே திருப்புலம்பல்.

பொருள் விளக்கம் (Spiritual Meaning):
மாணிக்கவாசகப் பெருமான் திருவாசகத்தில் அருளிய திருப்புலம்பல். பிரமனும் திருமாலும் அறியவொணாத பெருமானே, உன்னை அன்போடு சிந்தித்து உருகும் நெறியைத் தந்தருள்வாயாக எனப் புலம்பி இறைஞ்சுகிறார்.""",

    "vedasara": """பசூநாம் பதிம் பாபநாசம் பரீசம்
கஜேந்த்ரஸ்ய க்ருத்திம் வஸாநம் வரேண்யம்
ஜடாதாரினம் நீலகண்டம் மஹேசம்
பரமேச்வரம் அம்பிகாகாந்தமீசம் || 1 ||

பரேசம் மஹேசம் புஜங்கேச பூஷம்
பரவ்யோம வாசம் சுராணாம் நிவாஸம்
சிவம் சாந்தமீசான மீடே'பி நௌமி
மஹா தேவ சம்போ கிரீசாம்பிகேசம் || 2 ||

பொருள் விளக்கம் (Spiritual Meaning):
ஆதிசங்கர பகவற்பாதாள் அருளிய வேதஸார சிவ ஸ்தோத்திரம். அனைத்து உயிர்களுக்கும் தலைவரான, பாவங்களை நாசம் செய்கின்ற, அம்பிகையின் நாதரான பரமேஸ்வரனைப் போற்றித் தொழுகிறோம்.""",

    "thiruvaiyaru": """மாதர்ப் பிறைக் கண்ணியானை மலையான் மகளொடும் பாடிப்
போதொடு நீர்சுமந் தேத்திப் புகுவா ரவர்பின் புகுவேன்
யாதுஞ் சுவடு படாமல் ஐயா றடைகின்ற போது
காதன் மடப்பிடியோடும் களிறு வருவன கண்டேன்
கண்டேன் அவன்திருப் பாதங் கண்டறி யாதன கண்டேன்.

பொருள் விளக்கம் (Spiritual Meaning):
திருநாவுக்கரசர் பெருமான் திருவையாற்றில் சகல உயிர்களிலும் அம்மையப்பரின் சிவ-சக்தி தரிசனத்தைக் கண்டு உள்ளம் உருகிப் பாடிய அற்புதத் திருப்பதிகம்.""",

    "thiyaga_vanna_pathigam": """காரார் குழலாள் உமையோ டயில்வேல்
காளையொ டுந்தான் அமர்கின்ற
ஏரார் கோலம் கண்டு களிப்பான்
எண்ணும் எமக்கொன் றருளானேல்
நீரார் சடைமேல் பிறையொன் றுடையான்
நிதிக்கோன் தோழன் எனநின்றான்
பேரார் ஒற்றி யூரான் தியாகப்
பெருமான் பிச்சைப் பெருமானே.

பொருள் விளக்கம் (Spiritual Meaning):
வள்ளலார் இராமலிங்க அடிகளார் திருவொற்றியூரில் எழுந்தருளியுள்ள தியாகப்பெருமானை, உமையம்மையோடும் முருகப்பெருமானோடும் வீற்றிருக்கும் திருக்கோலத்தைக் கண்டு களித்து உள்ளம் உருகிப் போற்றிய அற்புதத் திருவருட்பாப் பாடல்.""",

    "anbu_maalai": """அற்புதப் பொன் அம்பலத்தே ஆகின்ற அரசே
ஆரமுதே அடியேன் தன் அன்பே என் அறிவே
கற்பு அவுபெருங் கருணைக் கடலே என் கண்ணே
கண்ணுதலே ஆனந்தக் களிப்பே மெய்க்கதியே
வெற்பு அவுபசுங் கொடியை மருவு பெருந்தருவே
வேத ஆகம முடியின் விளங்கும் ஒளி விளக்கே
பொற்புறவே இவ்வுலகில் பொருந்து சித்தன் ஆனேன்
பொருத்தமும் நின்திருவருளின் பொருத்தமது தானே!

பொருள் விளக்கம் (Spiritual Meaning):
தில்லைப் பொன்னம்பலக் கூத்தப் பெருமானை "அற்புதப் பொன் அம்பலத்தே ஆகின்ற அரசே, ஆரமுதே, அடியேன் அன்பே, பேரறிவே, கருணைக் கடலே" என்று விளித்து, தன் உள்ளத்தில் நீங்காது விளங்கும் இறைவனின் பேரருளைப் போற்றிப் பாடிய வள்ளலாரின் திருவருட்பாப் பனுவல்."""
}

TARGET_CONFIG = {
    "_eG3rWRIvJo": "thigada",
    "udRsA-oWxS0": "pancharatnam",
    "iXHNzqOrxzw": "pancharatnam",
    "qPjurMK6xpI": "pancharatnam",
    "mPypwIgdo-E": "thirupulambal",
    "g42Pg2sg_gg": "vedasara",
    "rRoJfeRQiaM": "thiruvaiyaru",
    "jZFTlpJwn6A": "thiyaga_vanna_pathigam",
    "FGeahfpAbiw": "anbu_maalai"
}

def transform_description(vid, existing_desc):
    work_key = TARGET_CONFIG[vid]
    canonical_lyrics = LYRICS_MAP[work_key]
    
    # Format A: Standard 📜 பாடல் வரிகள் section with decorative lines
    if "📜 பாடல் வரிகள்" in existing_desc:
        parts = re.split(r'📜\s*பாடல் வரிகள்.*?═════════════════════════════════════════════════════════════════', existing_desc, flags=re.DOTALL)
        if len(parts) >= 2:
            before_lyrics = parts[0] + "📜 பாடல் வரிகள் (CANONICAL TAMIL SCRIPTURE LYRICS)\n═════════════════════════════════════════════════════════════════\n"
            after_parts = re.split(r'═════════════════════════════════════════════════════════════════\s*📖', parts[1], flags=re.DOTALL)
            if len(after_parts) >= 2:
                after_lyrics = "\n\n═════════════════════════════════════════════════════════════════\n📖" + after_parts[1]
                return before_lyrics + canonical_lyrics + after_lyrics
            else:
                return before_lyrics + canonical_lyrics + "\n\n" + parts[1]

    # Format B: பாடல் வரிகள் (Tamil Lyrics): section
    if "பாடல் வரிகள் (Tamil Lyrics):" in existing_desc or "பாடல் வரிகள்:" in existing_desc:
        parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
        if len(parts) >= 2:
            before = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n"
            return before + canonical_lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
                
    # Format C: Sivapuranam text present
    if "நமச்சிவாய வாழ்க" in existing_desc:
        sub = re.sub(r'நமச்சிவாய வாழ்க.*?(?=— குரு குல தேசம்|\Z)', canonical_lyrics + "\n\n", existing_desc, flags=re.DOTALL)
        return sub
        
    # Format D: Gana natha om present
    if "கண நாதா ஓம்" in existing_desc:
        sub = re.sub(r'கண நாதா ஓம்.*?(?=— குரு குல தேசம்|\Z)', canonical_lyrics + "\n\n", existing_desc, flags=re.DOTALL)
        if sub != existing_desc:
            return sub
        return existing_desc.replace("கண நாதா ஓம்", canonical_lyrics)
        
    # Format E: Pancharatnam single verse
    if "முதாகராத்த மோதகம்" in existing_desc and "நிதாந்த காந்த" not in existing_desc:
        idx = existing_desc.find("முதாகராத்த மோதகம்")
        after_idx = existing_desc.find("═══════════", idx)
        if after_idx != -1:
            return existing_desc[:idx] + canonical_lyrics + "\n\n" + existing_desc[after_idx:]
        else:
            return existing_desc[:idx] + canonical_lyrics
            
    # Default fallback: append lyrics section
    return existing_desc + "\n\n📜 பாடல் வரிகள் (CANONICAL TAMIL SCRIPTURE LYRICS)\n═════════════════════════════════════════════════════════════════\n" + canonical_lyrics

def main():
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        results = []
        
        for idx, (vid, work) in enumerate(TARGET_CONFIG.items(), 1):
            url = f"https://studio.youtube.com/video/{vid}/edit"
            print(f"\n[{idx}/{len(TARGET_CONFIG)}] Processing {vid} ({work})...", flush=True)
            print(f"Navigating to {url}...", flush=True)
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(5)
            
            # Locate description textarea
            desc_elem = page.locator('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox').first
            if not desc_elem.is_visible():
                print(f"ERROR: Description element not visible for {vid}!", flush=True)
                results.append({"vid": vid, "work": work, "status": "elem_not_found"})
                continue
                
            existing_desc = desc_elem.inner_text()
            sample_phrase = LYRICS_MAP[work].split('\n')[0]
            
            if sample_phrase in existing_desc:
                # Also check Pancharatnam has verse 5
                if work == "pancharatnam" and "நிதாந்த காந்த" not in existing_desc:
                    print("Pancharatnam needs verses 2-5 injection...", flush=True)
                else:
                    print(f"ALREADY HAS CANONICAL LYRICS for {vid}! Skipping.", flush=True)
                    results.append({"vid": vid, "work": work, "status": "already_up_to_date"})
                    continue
                    
            new_desc = transform_description(vid, existing_desc)
            print(f"Updating description ({len(existing_desc)} -> {len(new_desc)} chars)...", flush=True)
            
            # Focus and fill
            desc_elem.click()
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(new_desc)
            time.sleep(2)
            
            # Click Save
            save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save"), button:has-text("Save")').first
            if save_btn.is_enabled():
                save_btn.click()
                print("Clicked Save! Waiting 5s...", flush=True)
                time.sleep(5)
                results.append({"vid": vid, "work": work, "status": "saved_successfully"})
                print(f"SUCCESS: {vid} saved successfully!", flush=True)
            else:
                print(f"WARNING: Save button not enabled for {vid}!", flush=True)
                results.append({"vid": vid, "work": work, "status": "save_not_enabled"})
                
            time.sleep(2)
            
        print("\n=================== BATCH SUMMARY ===================")
        for r in results:
            print(f"{r['vid']} ({r['work']}): {r['status']}")
            
    finally:
        browser.close()
        p.stop()

if __name__ == "__main__":
    main()
