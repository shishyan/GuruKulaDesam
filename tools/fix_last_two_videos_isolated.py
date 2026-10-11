import sys
import time
import json
import urllib.request
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

THIGADA_CORRECT = """திகட சக்கரச் செம்முக மைந்துளான்
சகட சக்கரத் தாமரை நாயகன்
அகட சக்கர வின்மணி யாவுறை
விகட சக்கரன் மெய்ப்பதம் போற்றுவாம்.

பொருள் விளக்கம் (Spiritual Meaning):
கந்த புராணத்தின் தொடக்கக் காப்புச் செய்யுள். கச்சியப்ப சிவாச்சாரியார் நூலைத் தொடங்கும் முன் விநாயகப் பெருமானின் திருவடிகளைப் போற்றி வணங்குகிறார் என்பது இதன் கருத்து."""

VEDASARA_CORRECT = """பசூநாம் பதிம் பாபநாசம் பரீசம்
கஜேந்த்ரஸ்ய க்ருத்திம் வஸாநம் வரேண்யம்
ஜடாதாரினம் நீலகண்டம் மஹேசம்
பரமேச்வரம் அம்பிகாகாந்தமீசம் || 1 ||

பரேசம் மஹேசம் புஜங்கேச பூஷம்
பரவ்யோம வாசம் சுராணாம் நிவாஸம்
சிவம் சாந்தமீசான மீடே'பி நௌமி
மஹா தேவ சம்போ கிரீசாம்பிகேசம் || 2 ||

பொருள் விளக்கம் (Spiritual Meaning):
ஆதிசங்கர பகவற்பாதாள் அருளிய வேதஸார சிவ ஸ்தோத்திரம். அனைத்து உயிர்களுக்கும் தலைவரான, பாவங்களை நாசம் செய்கின்ற, அம்பிகையின் நாதரான பரமேஸ்வரனைப் போற்றித் தொழுகிறோம்."""

TARGETS = [
    {
        "vid": "_eG3rWRIvJo",
        "title": "Thigada Sakkara",
        "lyrics": THIGADA_CORRECT
    },
    {
        "vid": "g42Pg2sg_gg",
        "title": "Vedasaara Shiva Stotram",
        "lyrics": VEDASARA_CORRECT
    }
]

def switch_to_new_tab(target_vid):
    target_url = f"https://studio.youtube.com/video/{target_vid}/edit"
    with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
        targets = json.loads(r.read().decode())
    old_pages = [t for t in targets if t.get('type') == 'page']
    
    # Open new tab
    req = urllib.request.Request(f"http://127.0.0.1:9225/json/new?{target_url}", method='PUT')
    with urllib.request.urlopen(req) as resp:
        new_data = json.loads(resp.read().decode())
        print(f"Opened fresh tab {new_data['id']} for {target_vid}", flush=True)
        
    time.sleep(2)
    # Close old pages
    for op in old_pages:
        try:
            req_close = urllib.request.Request(f"http://127.0.0.1:9225/json/close/{op['id']}", method='PUT')
            urllib.request.urlopen(req_close)
        except:
            pass
    time.sleep(4)

def run():
    for item in TARGETS:
        vid = item['vid']
        title = item['title']
        lyrics = item['lyrics']
        
        print(f"\n==========================================")
        print(f"Processing {vid} ({title})...", flush=True)
        switch_to_new_tab(vid)
        
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
            try:
                page = browser.contexts[0].pages[0]
                print(f"Connected to page: {page.url}", flush=True)
                assert vid in page.url, f"Expected {vid} in {page.url}"
                
                desc_elem = page.locator('#description-textarea #textbox').first
                existing_desc = desc_elem.inner_text()
                print(f"Current description len: {len(existing_desc)}")
                
                if "பாடல் வரிகள்" in existing_desc:
                    parts = re.split(r'பாடல் வரிகள்.*?:', existing_desc)
                    new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"
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
                    print(f"SUCCESS: Saved {vid} ({title})!", flush=True)
                else:
                    print("WARNING: Save button not enabled!")
            finally:
                browser.close()

if __name__ == "__main__":
    run()
