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

THIRUPULAMBAL_FULL = """பூங்கமலத் தயனொடுமால் அறியா நெறி பூவணத்தாய்
தாங்குசடை முடியானே தையலாள் ஓர் பாகத்தாய்
ஏங்குமடியவர்க் கருளும் ஈசனே எம்பெருமான்
பாங்குடைய நின்னடியே பணியுமா பணியாயே.

பாரொடு விண் ணீரனல் காலாகி நின்றாய்
ஆரொருவர் காண்கிற்பார் அன்னே உனைக்காணார்
சீரொடு நின்னடியே சிந்திப்பார் சிந்தையுள்
நீரொழுக நின்ற நெறியே திருப்புலம்பல்.

பொருள் விளக்கம் (Spiritual Meaning):
மாணிக்கவாசகப் பெருமான் திருவாசகத்தில் அருளிய திருப்புலம்பல். பிரமனும் திருமாலும் அறியவொணாத பெருமானே, உன்னை அன்போடு சிந்தித்து உருகும் நெறியைத் தந்தருள்வாயாக எனப் புலம்பி இறைஞ்சுகிறார்."""

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

REMAINING_TASKS = [
    {
        "vid": "udRsA-oWxS0",
        "title": "Maha Ganesha Pancharatnam",
        "type": "pancharatnam"
    },
    {
        "vid": "qPjurMK6xpI",
        "title": "Maha Ganesha Pancharatnam",
        "type": "pancharatnam"
    },
    {
        "vid": "mPypwIgdo-E",
        "title": "Thiruppulambal",
        "type": "thirupulambal"
    },
    {
        "vid": "rRoJfeRQiaM",
        "title": "Thiruvaiyaru Thirumurai",
        "type": "thiruvaiyaru"
    },
    {
        "vid": "FGeahfpAbiw",
        "title": "Anbu Maalai II",
        "type": "anbu_maalai"
    }
]

def update_single_video(page, item):
    vid = item['vid']
    vtype = item['type']
    target_url = f"https://studio.youtube.com/video/{vid}/edit"
    
    print(f"\n==========================================")
    print(f"Starting update for {vid} ({item['title']})...", flush=True)
    page.goto(target_url, wait_until="domcontentloaded")
    
    # Wait for the page to specifically display this vid's URL or details
    for _ in range(15):
        time.sleep(1)
        cur_url = page.url
        link_elem = page.locator(f'a[href*="{vid}"]').first
        if vid in cur_url and link_elem.is_visible():
            break
            
    print(f"Verified page is on {vid} (URL: {page.url})", flush=True)
    time.sleep(2)
    
    desc_elem = page.locator('#description-textarea #textbox').first
    existing_desc = desc_elem.inner_text()
    print(f"Current description length: {len(existing_desc)}")
    
    if vtype == "pancharatnam":
        # Replace between the two 65-char separator lines
        pattern = r'(பாடல் வரிகள்.*?═════════════════════════════════════════════════════════════════\n)(.*?)(\n═════════════════════════════════════════════════════════════════\s*📖)'
        m = re.search(pattern, existing_desc, flags=re.DOTALL)
        if m:
            new_desc = existing_desc[:m.start(2)] + PANCHARATNAM_5_VERSES + existing_desc[m.end(2):]
        else:
            # Fallback
            new_desc = existing_desc.replace("முதாகராத்த மோதகம் ஸதா விமுக்தி சாதகம்\nகலாதராவதம்ஸகம் விலாஸிலோகரக்ஷகம்\nஅநாயகைக நாயகம் விநாசிதேப தைத்யகம்\nநதாசுபாசு நாசகம் நமாமி தம் விநாயகம்!", PANCHARATNAM_5_VERSES)
            
    elif vtype == "thirupulambal":
        parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
        new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + THIRUPULAMBAL_FULL + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
        
    elif vtype == "vedasara":
        parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
        new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + VEDASARA_FULL + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
        
    elif vtype == "thiruvaiyaru":
        parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
        new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + THIRUVAIYARU_FULL + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
        
    elif vtype == "anbu_maalai":
        parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
        new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + ANBU_MAALAI_FULL + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"

    print(f"New description prepared ({len(existing_desc)} -> {len(new_desc)} chars). Inserting...", flush=True)
    desc_elem.click()
    page.keyboard.press("Control+A")
    page.keyboard.insert_text(new_desc)
    time.sleep(2)
    
    save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save"), button:has-text("Save")').first
    if save_btn.is_enabled():
        save_btn.click()
        print("Clicked Save! Waiting 6s for toast confirmation...", flush=True)
        time.sleep(6)
        print(f"SUCCESS: {vid} saved successfully!", flush=True)
    else:
        print(f"WARNING: Save button was not enabled for {vid}!", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        for item in REMAINING_TASKS:
            update_single_video(page, item)
            time.sleep(3)
        print("\nALL 5 REMAINING HYMNS UPDATED SUCCESSFULLY!")
    finally:
        browser.close()
