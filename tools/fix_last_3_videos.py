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

ANBU_MAALAI_FULL = """அற்புதப் பொன் அம்பலத்தே ஆகின்ற அரசே
ஆரமுதே அடியேன் தன் அன்பே என் அறிவே
கற்பு அவுபெருங் கருணைக் கடலே என் கண்ணே
கண்ணுதலே ஆனந்தக் களிப்பே மெய்க்கதியே
வெற்பு அவுபசுங் கொடியை மருவு பெருந்தருவே
வேத ஆகம முடியின் விளங்கும் ஒளி விளக்கே
பொற்புறவே இவ்வுலகில் பொருந்து சித்தன் ஆனேன்
பொருத்தமும் நின்திருவருளின் பொருத்தமது தானே!

பொருள் விளக்கம் (Spiritual Meaning):
தில்லைப் பொன்னம்பலக் கூத்தப் பெருமானை "அற்புதப் பொன் அம்பலத்தே ஆகின்ற அரசே, ஆரமுதே, அடியேன் அன்பே, பேரறிவே, கருணைக் கடலே" என்று விளித்து, தன் உள்ளத்தில் நீங்காது விளங்கும் இறைவனின் பேரருளைப் போற்றிப் பாடிய வள்ளலாரின் திருவருட்பாப் பனுவல்."""

LAST_TASKS = [
    ("qPjurMK6xpI", "pancharatnam", PANCHARATNAM_5_VERSES),
    ("g42Pg2sg_gg", "vedasara", VEDASARA_FULL),
    ("FGeahfpAbiw", "anbu_maalai", ANBU_MAALAI_FULL)
]

def fix_video(page, vid, vtype, canonical_text):
    target_url = f"https://studio.youtube.com/video/{vid}/edit"
    print(f"\nTargeting {vid} ({vtype})...", flush=True)
    page.goto(target_url, wait_until="domcontentloaded")
    time.sleep(5)
    
    desc_elem = page.locator('#description-textarea #textbox').first
    existing_desc = desc_elem.inner_text()
    print(f"Current desc len: {len(existing_desc)}")
    
    if vtype == "pancharatnam":
        pattern = r'(பாடல் வரிகள்.*?═════════════════════════════════════════════════════════════════\n)(.*?)(\n═════════════════════════════════════════════════════════════════\s*📖)'
        m = re.search(pattern, existing_desc, flags=re.DOTALL)
        if m:
            new_desc = existing_desc[:m.start(2)] + canonical_text + existing_desc[m.end(2):]
        else:
            new_desc = existing_desc.replace("முதாகராத்த மோதகம் ஸதா விமுக்தி சாதகம்\nகலாதராவதம்ஸகம் விலாஸிலோகரக்ஷகம்\nஅநாயகைக நாயகம் விநாசிதேப தைத்யகம்\nநதாசுபாசு நாசகம் நமாமி தம் விநாயகம்!", canonical_text)
    else:
        parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
        new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + canonical_text + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"

    print(f"Replacing desc ({len(existing_desc)} -> {len(new_desc)} chars)...", flush=True)
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
        print(f"WARNING: Save not enabled for {vid}!")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        for vid, vtype, canonical_text in LAST_TASKS:
            try:
                fix_video(page, vid, vtype, canonical_text)
                time.sleep(3)
            except Exception as e:
                print(f"Error on {vid}: {e}")
    finally:
        browser.close()
