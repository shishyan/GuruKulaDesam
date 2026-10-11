import sys
import time
import json
import urllib.request
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
தமேகதந்தமேவ தம் விசிந்தயாமி ஸந்ததம் || 5 ||

பொருள் விளக்கம் (Spiritual Meaning):
ஆதிசங்கரர் அருளிய ஐந்து ஸ்லோகங்களிலும் விநாயகப் பெருமானின் மோதகம் ஏந்திய திருக்கரம், பிறைசூடிய அழகு, கஜமுகாசுரனை அழித்த வீரம், வணங்குவோரின் துன்பம் நீக்கும் கருணை, ஒற்றைத் தந்த திருவுருவம் ஆகியவை போற்றப்படுகின்றன."""

vid = "qPjurMK6xpI"
target_url = f"https://studio.youtube.com/video/{vid}/edit"

# Switch to fresh tab
with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
    targets = json.loads(r.read().decode())
old_pages = [t for t in targets if t.get('type') == 'page']

req = urllib.request.Request(f"http://127.0.0.1:9225/json/new?{target_url}", method='PUT')
with urllib.request.urlopen(req) as resp:
    new_data = json.loads(resp.read().decode())
    print("Opened fresh tab:", new_data['id'])
time.sleep(2)

for op in old_pages:
    try:
        req_close = urllib.request.Request(f"http://127.0.0.1:9225/json/close/{op['id']}", method='PUT')
        urllib.request.urlopen(req_close)
    except:
        pass
time.sleep(4)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        print("Page URL:", page.url)
        assert vid in page.url
        desc_elem = page.locator('#description-textarea #textbox').first
        desc = desc_elem.inner_text()
        print(f"Current desc len: {len(desc)}")
        
        # In qPjurMK6xpI:
        # replace between separators or replace lyrics section
        if "பாடல் வரிகள்" in desc:
            parts = re.split(r'பாடல் வரிகள்.*?:', desc)
            new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + PANCHARATNAM_5_VERSES + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
        else:
            new_desc = desc + "\n\nபாடல் வரிகள் (Tamil Lyrics):\n" + PANCHARATNAM_5_VERSES + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
            
        print(f"Prepared new desc ({len(desc)} -> {len(new_desc)} chars). Injecting...")
        desc_elem.click()
        page.keyboard.press("Control+A")
        page.keyboard.insert_text(new_desc)
        time.sleep(2)
        
        save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save"), button:has-text("Save")').first
        if save_btn.is_enabled():
            save_btn.click()
            print("Clicked Save! Waiting 6s...")
            time.sleep(6)
            print("SUCCESS: Saved qPjurMK6xpI!")
        else:
            print("WARNING: Save button not enabled!")
    finally:
        browser.close()
