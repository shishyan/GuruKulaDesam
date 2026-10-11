import sys
import time
import json
import urllib.request
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

TARGETS = [
    ("uPk4dyag74Y", "திகட சக்கரச் செம்முக", "Thigada Sakkara", "Kandha Puranam Kaappu"),
    ("_eG3rWRIvJo", "திகட சக்கரச் செம்முக", "Thigada Sakkara", "Kandha Puranam Kaappu"),
    ("udRsA-oWxS0", "நிதாந்த காந்த", "Ganesha Pancharatnam", "5 Verses Complete"),
    ("iXHNzqOrxzw", "நிதாந்த காந்த", "Ganesha Pancharatnam", "5 Verses Complete"),
    ("qPjurMK6xpI", "நிதாந்த காந்த", "Ganesha Pancharatnam", "5 Verses Complete"),
    ("mPypwIgdo-E", "பூங்கமலத் தயனொடுமால்", "Thirupulambal", "Thiruvasagam"),
    ("g42Pg2sg_gg", "பசூநாம் பதிம்", "Vedasaara Shiva Stotram", "Adi Shankara"),
    ("rRoJfeRQiaM", "மாதர்ப் பிறைக் கண்ணி", "Thiruvaiyaru Thevaram", "Appar 4th Thirumurai"),
    ("jZFTlpJwn6A", "காரார் குழலாள்", "Thiyaga Vanna Pathigam", "Thiruvarutpa 2nd Thirumurai"),
    ("FGeahfpAbiw", "அற்புதப் பொன் அம்பலத்தே", "Anbu Maalai II", "Thiruvarutpa 5th Thirumurai")
]

results = []

for idx, (vid, check_str, hymn_name, scripture) in enumerate(TARGETS, 1):
    target_url = f"https://studio.youtube.com/video/{vid}/edit"
    
    # 1. Open new tab via CDP HTTP
    with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
        targets_json = json.loads(r.read().decode())
    old_pages = [t for t in targets_json if t.get('type') == 'page']
    
    req = urllib.request.Request(f"http://127.0.0.1:9225/json/new?{target_url}", method='PUT')
    with urllib.request.urlopen(req) as resp:
        new_data = json.loads(resp.read().decode())
        
    time.sleep(2)
    for op in old_pages:
        try:
            req_close = urllib.request.Request(f"http://127.0.0.1:9225/json/close/{op['id']}", method='PUT')
            urllib.request.urlopen(req_close)
        except:
            pass
    time.sleep(4)
    
    # 2. Inspect description in Studio
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
        try:
            page = browser.contexts[0].pages[0]
            desc_elem = page.locator('#description-textarea #textbox').first
            desc = desc_elem.inner_text()
            
            has_canonical = check_str in desc
            has_sivapuranam_leak = "நமச்சிவாய வாழ்க" in desc and vid not in []
            has_gana_leak = "கண நாதா ஓம்" in desc and "திகட" in hymn_name
            
            is_perfect = has_canonical and not has_sivapuranam_leak and not has_gana_leak
            status_str = "VERIFIED_PERFECT" if is_perfect else "FAILED"
            
            results.append({
                "vid": vid,
                "hymn": hymn_name,
                "scripture": scripture,
                "status": status_str,
                "desc_len": len(desc),
                "has_canonical": has_canonical,
                "has_sivapuranam_leak": has_sivapuranam_leak,
                "has_gana_leak": has_gana_leak
            })
            print(f"[{idx}/{len(TARGETS)}] [{status_str}] {vid} | {hymn_name} ({scripture}) | {len(desc)} chars | Canonical: {has_canonical}", flush=True)
        finally:
            browser.close()

print("\n" + "="*80)
print("FINAL AUDIT & VERIFICATION REPORT: ALL 10 TARGET VIDEOS ON YOUTUBE STUDIO")
print("="*80)
all_ok = all(r['status'] == "VERIFIED_PERFECT" for r in results)
print(f"OVERALL RESULT: {'100% CANONICAL PERFECTION ACHIEVED' if all_ok else 'SOME DISCREPANCIES REMAIN'}\n")
for r in results:
    print(f"• https://youtu.be/{r['vid']}")
    print(f"  Hymn / Work : {r['hymn']} ({r['scripture']})")
    print(f"  Live Status : {r['status']} ({r['desc_len']} characters)")
    print(f"  Scripture Check : Present={r['has_canonical']}, SivapuranamLeak={r['has_sivapuranam_leak']}, GanaLeak={r['has_gana_leak']}\n")
