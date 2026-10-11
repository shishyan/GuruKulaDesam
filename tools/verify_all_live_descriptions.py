import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

TARGETS = [
    ("uPk4dyag74Y", "திகட சக்கரச் செம்முக", "Thigada Sakkara"),
    ("_eG3rWRIvJo", "திகட சக்கரச் செம்முக", "Thigada Sakkara"),
    ("udRsA-oWxS0", "நிதாந்த காந்த", "Ganesha Pancharatnam 5 verses"),
    ("iXHNzqOrxzw", "நிதாந்த காந்த", "Ganesha Pancharatnam 5 verses"),
    ("qPjurMK6xpI", "நிதாந்த காந்த", "Ganesha Pancharatnam 5 verses"),
    ("mPypwIgdo-E", "பூங்கமலத் தயனொடுமால்", "Thirupulambal"),
    ("g42Pg2sg_gg", "பசூநாம் பதிம்", "Vedasaara Shiva Stotram"),
    ("rRoJfeRQiaM", "மாதர்ப் பிறைக் கண்ணி", "Thiruvaiyaru Thevaram"),
    ("jZFTlpJwn6A", "காரார் குழலாள்", "Thiyaga Vanna Pathigam"),
    ("FGeahfpAbiw", "அற்புதப் பொன் அம்பலத்தே", "Anbu Maalai")
]

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    try:
        page = browser.contexts[0].pages[0]
        results = []
        for vid, check_str, label in TARGETS:
            url = f"https://studio.youtube.com/video/{vid}/edit"
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(4)
            desc_elem = page.locator('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox').first
            desc = desc_elem.inner_text()
            has_check = check_str in desc
            has_siva_mismatch = "நமச்சிவாய வாழ்க" in desc and label not in ["Sivapuranam"]
            has_gana_mismatch = "கண நாதா ஓம்" in desc and label not in ["Gana Natha"]
            
            status = "VERIFIED_PERFECT" if has_check and not has_siva_mismatch and not has_gana_mismatch else "FAILED"
            results.append({
                "vid": vid,
                "label": label,
                "status": status,
                "has_check": has_check,
                "has_siva_mismatch": has_siva_mismatch,
                "has_gana_mismatch": has_gana_mismatch,
                "len": len(desc)
            })
            print(f"[{status}] {vid} ({label}): len={len(desc)}, canonical_present={has_check}", flush=True)
            
        print("\n=== FINAL VERIFICATION SUMMARY ===")
        all_passed = all(r['status'] == "VERIFIED_PERFECT" for r in results)
        print(f"All 10 Defective Videos Fixed: {all_passed}")
        for r in results:
            print(f" - {r['vid']}: {r['label']} -> {r['status']} ({r['len']} chars)")
    finally:
        browser.close()
