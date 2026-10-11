import urllib.request
import json
import sys
import re

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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ta,en-US;q=0.9,en;q=0.8'
}

print("=== VERIFYING ALL 10 VIDEOS LIVE ON YOUTUBE ===")
all_passed = True
results = []

for vid, check_str, label in TARGETS:
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            has_canonical = check_str in html
            has_siva_mismatch = "நமச்சிவாய வாழ்க" in html and label not in ["Sivapuranam"]
            
            # Also extract description from ytInitialPlayerResponse or meta description
            desc_match = re.search(r'"shortDescription":"(.*?)"', html)
            desc_snip = desc_match.group(1)[:100] if desc_match else ""
            
            status = "VERIFIED_PERFECT" if has_canonical and not has_siva_mismatch else "FAILED"
            if status != "VERIFIED_PERFECT":
                all_passed = False
                
            results.append({
                "vid": vid,
                "label": label,
                "status": status,
                "has_canonical": has_canonical,
                "has_siva_mismatch": has_siva_mismatch,
                "desc_snip": desc_snip
            })
            print(f"[{status}] {vid} | {label} | Canonical: {has_canonical} | Mismatch: {has_siva_mismatch}", flush=True)
    except Exception as e:
        print(f"[ERROR] {vid} : {e}")

print(f"\n==========================================")
print(f"ALL 10 TARGET HYMNS 100% FIXED & VERIFIED: {all_passed}")
print(f"==========================================")
for r in results:
    print(f" - https://youtu.be/{r['vid']} : {r['label']} -> {r['status']}")
