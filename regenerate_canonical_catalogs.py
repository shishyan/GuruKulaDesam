"""
Comprehensive Catalog & Manifest Regenerator
Enforces: 'Title should start where it belongs (Thiruvasagam, Thevaram, Thirukkural, etc.), then the name.'
Strictly enforces:
- Bilingual canonical naming
- Character length <= 95 (YouTube API strict limit)
- 100% mirror parity across root, site/, and docs/
"""

import os
import sys
import json
import csv
import re
import shutil
import hashlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MASTER_JSON = "master_all_598_songs_catalog.json"
MASTER_CSV = "master_all_598_songs_catalog.csv"
CATALOG_JSON = "assets/data/catalog.json"
CATALOG_JS = "assets/data/catalog.js"
LIVE_METADATA_JSON = os.path.join("data", "dumps", "live_youtube_metadata.json") if os.path.exists(os.path.join("data", "dumps", "live_youtube_metadata.json")) else "live_youtube_metadata.json"
UPDATES_JSON = "all_channel_title_updates.json"
UPDATES_CSV = "all_channel_title_updates.csv"
PENDING_JSON = "channel_direct_uploads_pending.json"
ARTIFACT_MD = r"C:\Users\Shishyan\.gemini\antigravity\brain\d351c0e2-33be-43a2-a54b-5b6e5c7cccdb\master-580-videos-audios-catalog.md"

with open(MASTER_JSON, "r", encoding="utf-8") as f:
    master_records = json.load(f)

with open(CATALOG_JSON, "r", encoding="utf-8") as f:
    site_catalog = json.load(f)

cat_by_id = {}
for cat_name, items in site_catalog.items():
    for it in items:
        cat_by_id[it["id"]] = (cat_name, it)


def clean_english_name(eng, eng_s=""):
    eng = re.sub(r"\[.*?\]", "", eng)
    eng = re.sub(r"(?i)\b(Cinematic\s+(Thirukkural|Shiva|Lord\s+Shiva|Devotional|Murugan|Amman|Vinayagar|Film)?|Full\s+Song\s+Film|Full\s+Song|Remix\s+Cinematic\s+Thirukkural\s+Film|Devotional\s+Film|Film|Song|Audio)\b", "", eng)
    prefixes = [
        "Thirukkural", "Thiruvasagam", "Thevaram", "Thiruvarutpa", "Kandhar Alangaram",
        "Kandhar Anuboothi", "Kandha Puranam", "Kandha Sashti Kavasam", "Thiruppugazh",
        "Thiruppavai", "Periyazhvar Thirumozhi", "Abhirami Andhadhi", "Vinayagar Nanmanimalai",
        "Vinayagar", "Adi Shankaracharya", "Adi Shankara", "Shiva Namavali", "Maha Vishnu",
        "Rama Bhajan", "Maha Mantra", "Bhajan", "Nama Sankeerthanam", "Amman", "Tamil Thai Vazhthu",
        "Aalaya Naatham", "Ambient Meditation", "Thirumurai", "Saraswathi Stotram", "Krishna",
        "Periyapuranam", "Devotional", "Shiva Devotional", "Murugan Devotional", "Vishnu Devotional",
        "Amman Devotional", "Vinayagar Devotional", "Heritage Song", eng_s
    ]
    pattern = r"(?i)^(" + "|".join(re.escape(p) for p in set(prefixes) if p) + r")\s*[:—–-]\s*"
    while re.search(pattern, eng):
        eng = re.sub(pattern, "", eng)
    eng = re.sub(r"\s+", " ", eng).strip(" -|")
    return eng


SPECIAL_TRACK_MAP = {
    "-tod_ZpZMnQ": ("தேவாரம்", "Thevaram", "கடவுளைக் கடலுள் எழு (திருக்குறுந்தொகை)", "Kadavulai Kadalul Ezhu"),
    "2_rwWlC09I0": ("சிவ ஸ்தோத்திரம்", "Shiva Stotram", "ஸ்மரணாதருணாசலம்", "Smaranad Arunachalam"),
    "2mdEV1acg-U": ("திருவாசகம்", "Thiruvasagam", "குழைத்த பத்து", "Kuzhaitha Pathu"),
    "2vQYuvePk9U": ("பன்னிரு திருமுறை", "Panniru Thirumurai", "திருவையாறு சாரம்", "Thiruvaiyaaru Saaram"),
    "2vuuHMEhs20": ("திருவாசகம்", "Thiruvasagam", "போற்றித் திருஅகவல்", "Potrith Thiruagaval"),
    "57X8XwJaB0U": ("பெரியபுராணம்", "Periyapuranam", "உலகெலாம் உணர்ந்து ஓதற்கு அரியவன்", "Ulagelam Unarnthu"),
    "5vieI9fE5Y8": ("திருவருட்பா", "Thiruvarutpa", "புண்ணிய விளக்கம்", "Punniya Vilakkam"),
    "6cE4xUOmSzU": ("திருவாசகம்", "Thiruvasagam", "சிவபுராணம் (நமச்சிவாய வாழ்க)", "Sivapuranam"),
    "75W77Q-_Oe8": ("திருவாசகம்", "Thiruvasagam", "சென்னிப்பத்து", "Sennippathu"),
    "89Q2g8AllcE": ("திருவாசகம்", "Thiruvasagam", "நடராஜர் பத்து", "Natarajar Pathu"),
    "8HUmRJKyxTc": ("தேவாரம்", "Thevaram", "அவிநாசிப் பதிகம்", "Avinasi Pathigam"),
    "A2CB3LpJ0Qk": ("தேவாரம்", "Thevaram", "கரைந்து கைதொழுவாரையும்", "Karainthu Kaithozhuvar"),
    "AuEZhvVmA90": ("தேவாரம்", "Thevaram", "பிடியதன் உருவுமை (விநாயகர் காப்பு)", "Pidiyathan Uruvu"),
    "CFEYF0X6fLU": ("கந்த சஷ்டி கவசம்", "Kandha Sashti Kavasam", "முழு கவசம்", "Kandha Sashti Thuthi"),
    "CHWHsVF0V70": ("திருமந்திரம்", "Thirumanthiram", "முதலாம் தந்திரம்", "Mudhal Thanthiram"),
    "JkivipMHrzc": ("கிருஷ்ண துதி", "Krishna Thuthi", "கிருஷ்ண மந்திரம் II", "Krishna Mantra II"),
    "QFCD-U3sT4M": ("திருவாசகம்", "Thiruvasagam", "தென்னாடுடைய சிவனே போற்றி", "Thennadudaiya Sivaney"),
    "S4ogw4EfpDY": ("திருப்புகழ்", "Thiruppugazh", "திருப்புகழ் 566 (இரத்னகிரி I)", "Thiruppugazh 566 Rathnagiri I"),
    "XB7cD-5ye-k": ("திருவாசகம்", "Thiruvasagam", "திருப்படை ஆட்சி", "Thiruppadai Aatchi"),
    "ZZKjQ1SD_mQ": ("கந்தர் அலங்காரம்", "Kandhar Alangaram", "நாள் என் செய்யும்", "Naal En Seyyum"),
    "aq0j2OMVNoU": ("திருவாசகம்", "Thiruvasagam", "சிவபுராணம் (நமச்சிவாய வாழ்க)", "Sivapuranam by Children"),
    "bOxyDZgsI2c": ("திருப்புகழ்", "Thiruppugazh", "திருப்புகழ் 566 (இரத்னகிரி II)", "Thiruppugazh 566 Rathnagiri II"),
    "e9fTnxiiLnc": ("திருவாசகம்", "Thiruvasagam", "திருவார்த்தை", "Thiruvaarthai"),
    "fcWB5HrGeMs": ("திருவாசகம்", "Thiruvasagam", "திரு உந்தியார்", "Thiru Unthiyar"),
    "fdB9R7QeXo0": ("திருவாசகம்", "Thiruvasagam", "குழைத்த பத்து", "Kuzhaitha Pathu"),
    "hoZZgL3xe9k": ("திருவாசகம்", "Thiruvasagam", "எண்ணப் பதிகம்", "Ennap Pathigam"),
    "izHLRwITs_Q": ("கிருஷ்ண துதி", "Krishna Thuthi", "கிருஷ்ண மந்திரம் I", "Krishna Mantra I"),
    "j1tzixa2raU": ("திருவாசகம்", "Thiruvasagam", "தென்னாடுடைய சிவனே போற்றி", "Thennadudaiya Sivaney"),
    "p1KPCpSX53U": ("திருவருட்பா", "Thiruvarutpa", "தோடுடையார்", "Thodudaiyaar"),
    "pF7fYFU5fKs": ("திருவருட்பா", "Thiruvarutpa", "திருவடிப் புகழ்ச்சி", "Thiruvadi Pugazhchi"),
    "qr5jAhLRLUE": ("கந்தர் அநுபூதி", "Kandhar Anuboothi", "உருவாய் அருவாய்", "Uruvaai Aruvaai"),
    "r3APrd3opOs": ("திருவாசகம்", "Thiruvasagam", "திருவெம்பாவை (ஆதியும் அந்தமும்)", "Thiruvempavai"),
    "wC45ZWg05eo": ("திருவாசகம்", "Thiruvasagam", "வேண்டுமே இத்தனையும் (திருவெம்பாவை)", "Vendumey Iththanaiyum"),
    "wXD_lSlfiSQ": ("திருவாசகம்", "Thiruvasagam", "சிவபுராணம் (Symphony)", "Sivapuranam Symphony"),
    "x355fpndpTI": ("கந்தர் அநுபூதி", "Kandhar Anuboothi", "உருவாய் அருவாய்", "Uruvaai Aruvaai"),
    "xqM-FFGFDC4": ("பெரியபுராணம்", "Periyapuranam", "தில்லை வாழ் அந்தணர் சருக்கம்", "Thillai Vazh Anthanar"),
    "yrmF7nfwnsQ": ("தேவாரம்", "Thevaram", "கோளறு திருப்பதிகம்", "Kolaru Pathigam"),
}


def classify_where_it_belongs(vid, current_title, cat_entry):
    if vid in SPECIAL_TRACK_MAP:
        tam_s, eng_s, tam_n, eng_override = SPECIAL_TRACK_MAP[vid]
        return tam_s, eng_s, tam_n, eng_override

    cat_name, it_meta = cat_entry if cat_entry else (None, {})
    src = it_meta.get("source", "")
    auth = it_meta.get("author", "")
    combo = f"{current_title} {src} {auth}"

    # 1. Thevaram Specific Hymns
    if any(k in combo for k in ["மாசில் வீணையும்", "திருநீற்று", "மந்திரமாவது நீறு", "துஞ்சலும்", "திருவோத்தூர்", "பூத்தேர்ந்து", "அன்னம் பாலிக்கும்", "பண்டாய", "நாமார்க்கும்", "அவிநாசி", "கடவுளைக் கடலுள்", "திருக்குறுந்தொகை"]):
        tam_s, eng_s = "தேவாரம்", "Thevaram"
        if "மாசில் வீணையும்" in combo: tam_n = "மாசில் வீணையும்"
        elif "திருநீற்று" in combo or "மந்திரமாவது" in combo: tam_n = "திருநீற்றுப் பதிகம் (மந்திரமாவது நீறு)"
        elif "துஞ்சலும்" in combo: tam_n = "நமச்சிவாயப் பதிகம் (துஞ்சலும் துஞ்சல்)"
        elif "கடவுளைக் கடலுள்" in combo or "திருக்குறுந்தொகை" in combo: tam_n = "கடவுளைக் கடலுள் எழு (திருக்குறுந்தொகை)"
        elif "பூத்தேர்ந்து" in combo or "திருவோத்தூர்" in combo:
            variant = " III" if "III" in current_title else (" V" if " V" in current_title else "")
            tam_n = f"திருவோத்தூர் பதிகம் (பூத்தேர்ந்து ஆயன{variant})"
        elif "அன்னம் பாலிக்கும்" in combo: tam_n = "தில்லைத் திருப்பதிகம் (அன்னம் பாலிக்கும்)"
        elif "பண்டாய" in combo: tam_n = "பண்டாய நான்மறை"
        elif "அவிநாசி" in combo: tam_n = "அவிநாசிப் பதிகம்"
        else: tam_n = current_title.split("|")[0].strip()
        return tam_s, eng_s, tam_n, None

    # 2. Thiruvasagam Specific Hymns
    if any(k in combo for k in ["சிவபுராணம்", "அச்சோ", "பூவார் சென்னி", "யாத்திரைப் பத்து", "திருப்புலம்பல்", "அன்னைப்பத்து", "குழைத்த பத்து", "திருவெம்பாவை", "ஆதியும் அந்தமும்", "வேண்டுமே இத்தனையும்", "போற்றித் திருஅகவல்", "தென்னாடுடைய சிவனே", "எண்ணப் பதிகம்"]):
        tam_s, eng_s = "திருவாசகம்", "Thiruvasagam"
        if "சிவபுராணம்" in combo:
            variant = " II" if ("2026 (II)" in current_title or " II" in current_title) else ""
            tam_n = f"சிவபுராணம்{variant}"
        elif "அச்சோ" in combo: tam_n = "அச்சோப் பதிகம்"
        elif "பூவார் சென்னி" in combo: tam_n = "பூவார் சென்னி மன்னன் (யாத்திரைப் பத்து)"
        elif "திருப்புலம்பல்" in combo: tam_n = "திருப்புலம்பல்"
        elif "அன்னைப்பத்து" in combo: tam_n = "அன்னைப்பத்து"
        elif "குழைத்த பத்து" in combo: tam_n = "குழைத்த பத்து"
        elif "வேண்டுமே இத்தனையும்" in combo: tam_n = "வேண்டுமே இத்தனையும் (திருவெம்பாவை)"
        elif "போற்றித் திருஅகவல்" in combo: tam_n = "போற்றித் திருஅகவல்"
        elif "தென்னாடுடைய சிவனே" in combo: tam_n = "தென்னாடுடைய சிவனே போற்றி"
        elif "ஆதியும் அந்தமும்" in combo: tam_n = "திருவெம்பாவை (ஆதியும் அந்தமும்)"
        elif "எண்ணப் பதிகம்" in combo: tam_n = "எண்ணப் பதிகம்"
        else: tam_n = current_title.split("|")[0].strip()
        return tam_s, eng_s, tam_n, None

    # 3. Thirukkural
    if "அதிகாரம்" in current_title or "Thirukkural" in combo or "திருக்குறள்" in combo:
        tam_s, eng_s = "திருக்குறள்", "Thirukkural"
        m = re.search(r"அதிகாரம்\s+(\d+)\s*-\s*([^|\[\(]+)", current_title)
        if m:
            num = m.group(1).strip()
            name = m.group(2).strip()
            var = ""
            if "பகுதி 1" in current_title or " I " in current_title or " Part 1" in current_title: var = " (பகுதி 1)"
            elif "பகுதி 2" in current_title or " II " in current_title or " Part 2" in current_title: var = " (பகுதி 2)"
            elif "Remix" in current_title: var = " (Remix)"
            elif "Female" in current_title: var = " (Female)"
            elif "Sad" in current_title: var = " (Sad)"
            elif "Symphony" in current_title: var = " (Symphony)"
            elif "Pop" in current_title: var = " (Pop)"
            elif "Original" in current_title: var = " (Original)"
            tam_n = f"அதிகாரம் {num} - {name}{var}"
        else:
            tam_n = current_title.split("|")[0].strip()
        return tam_s, eng_s, tam_n, None

    # 4. Thiruvarutpa / Vallalar
    if any(k in combo for k in ["சிவ சுப்ரமணியர்", "சுப்ரமண்யர் திருவிருத்தம்", "அருட்பெருஞ்சோதி", "கொடைமட", "திருவருள் வேட்கை", "பெற்றை", "திருச்சாதனத்", "வள்ளலார்", "திருவருட்பா", "வாழ்வது தமிழ்"]):
        tam_s, eng_s = "திருவருட்பா", "Thiruvarutpa"
        if "சிவ சுப்ரமணியர்" in combo or "சுப்ரமண்யர் திருவிருத்தம்" in combo: tam_n = "சிவ சுப்ரமணியர் திருவிருத்தம்"
        elif "அருட்பெருஞ்சோதி" in combo:
            variant = " II" if (" II" in current_title or " 2" in current_title) else ""
            tam_n = f"அருட்பெருஞ்சோதி அகவல்{variant}"
        elif "கொடைமட" in combo: tam_n = "கொடைமடப் புகழ்ச்சி"
        elif "திருவருள் வேட்கை" in combo: tam_n = "திருவருள் வேட்கை"
        elif "திருச்சாதனத்" in combo: tam_n = "திருச்சாதனத் தெய்வத் திறம்"
        elif "வாழ்வது தமிழ்" in combo: tam_n = "வாழ்வது தமிழ் ஆகட்டும்"
        else: tam_n = current_title.split("|")[0].strip()
        return tam_s, eng_s, tam_n, None

    # 5. Murugan Specifics
    if "நாள் என் செய்யும்" in combo or "கந்தர் அலங்காரம்" in combo:
        return "கந்தர் அலங்காரம்", "Kandhar Alangaram", "நாள் என் செய்யும்", None
    if "உருவாய் அருவாய்" in combo or "கந்தர் அநுபூதி" in combo:
        return "கந்தர் அநுபூதி", "Kandhar Anuboothi", "உருவாய் அருவாய்", None
    if "சஷ்டி கவசம்" in combo:
        return "கந்த சஷ்டி கவசம்", "Kandha Sashti Kavasam", "முழு கவசம்", None
    if "வான் முகில்" in combo or "வான்முகில்" in combo:
        return "கந்த புராணம்", "Kandha Puranam", "வான் முகில் வழாது பெய்க", None
    if "திகட சக்கர" in combo:
        return "கந்த புராணம்", "Kandha Puranam", "திகட சக்கர சண்முகத்தோன் (காப்பு)", None
    if "திருப்புகழ்" in combo:
        return "திருப்புகழ்", "Thiruppugazh", current_title.split("|")[0].strip(), None

    # 6. Vaishnava Specifics
    if any(k in combo for k in ["திருப்பாவை", "மார்கழித் திங்கள்", "வையத்து வாழ்வீர்", "ஓங்கி உலகளந்த"]):
        tam_s, eng_s = "திருப்பாவை", "Thiruppavai"
        if "மார்கழித் திங்கள்" in combo or " 1" in current_title: tam_n = "பாசுரம் 1 - மார்கழித் திங்கள்"
        elif "வையத்து வாழ்வீர்" in combo or " 2" in current_title: tam_n = "பாசுரம் 2 - வையத்து வாழ்வீர்"
        elif "ஓங்கி உலகளந்த" in combo or " 3" in current_title: tam_n = "பாசுரம் 3 - ஓங்கி உலகளந்த"
        else: tam_n = current_title.split("|")[0].strip()
        return tam_s, eng_s, tam_n, None
    if "பெரியாழ்வார்" in combo or "கண்ணன் தாலாட்டு" in combo:
        var = " III" if (" III" in current_title or "(III)" in current_title) else ""
        return "பெரியாழ்வார் திருமொழி", "Periyazhvar Thirumozhi", f"கண்ணன் தாலாட்டு{var}", None

    # 7. Amman & Shakti
    if "அபிராமி அந்தாதி" in combo or "தனந்தரும் கல்விதரும்" in combo:
        return "அபிராமி அந்தாதி", "Abhirami Andhadhi", "தனந்தரும் கல்விதரும்", None
    if "சரஸ்வதி போற்றி" in combo or "சரஸ்வதி அஷ்டோத்தர" in combo:
        return "சரஸ்வதி போற்றி", "Saraswathi Stotram", "108 போற்றி", None
    if "மகாமாயி" in combo:
        var = " (Original Story)" if "Original" in current_title else ""
        return "அம்மன் துதி", "Amman Thuthi", f"மகாமாயி சமயபுரத்தாயே{var}", None

    # 8. Vinayagar
    if "பாலும் தெளிதேனும்" in combo or "நான்மணிமாலை" in combo:
        return "விநாயகர் நான்மணிமாலை", "Vinayagar Nanmanimalai", "பாலும் தெளிதேனும்", None
    if "கண நாதா ஓம்" in combo:
        var = " (Symphony)" if "Symphony" in current_title else (" (Original)" if "Original" in current_title else "")
        return "விநாயகர் துதி", "Vinayagar Thuthi", f"கண நாதா ஓம்{var}", None

    # 9. Adi Shankaracharya
    if "கணேச பஞ்சரத்னம்" in combo:
        return "ஆதிசங்கரர்", "Adi Shankara", "மகா கணேச பஞ்சரத்னம்", None
    if "வேதஸார சிவ" in combo:
        return "ஆதிசங்கரர்", "Adi Shankara", "வேதஸார சிவ ஸ்தோத்ரம்", None

    # 10. Heritage / Instrumental
    if "தமிழ்த்தாய் வாழ்த்து" in combo or "நீராரும் கடலுடுத்த" in combo:
        return "தமிழ்த்தாய் வாழ்த்து", "Tamil Thai Vazhthu", "நீராரும் கடலுடுத்த", None
    if "ஆலய நாதம்" in combo:
        return "ஆலய நாதம்", "Aalaya Naatham", "இந்திய ஹார்மோனிக்கா தியானம்", None
    if "Interstellar" in combo:
        return "இசைத் தியானம்", "Ambient Meditation", "இன்டர்ஸ்டெல்லார் (Interstellar)", None

    # 11. Deities
    if "நமோ நாராயணம்" in combo:
        var = " (Image Motion)" if "Image Motion" in current_title else ""
        return "மகாவிஷ்ணு துதி", "Maha Vishnu", f"நமோ நாராயணம் (தசாவதாரம்){var}", None
    if "ரகுபதி ராகவ" in combo:
        return "ராம பஜனை", "Rama Bhajan", "ரகுபதி ராகவ ராஜா ராம்", None
    if "ஹரே கிருஷ்ணா" in combo:
        return "மகா மந்திரம்", "Maha Mantra", "ஹரே கிருஷ்ணா ஹரே ராமா", None
    if "இராம கிருஷ்ண துதி" in combo:
        return "பஜனை", "Bhajan", "இராம கிருஷ்ண துதி", None
    if "இராம ராம ராம" in combo:
        return "நாம சங்கீர்த்தனம்", "Nama Sankeerthanam", "இராம ராம ராம ஹரே", None
    if "கிருஷ்ண மந்திரம்" in combo:
        var = " I" if " I" in current_title else (" II" if " II" in current_title else (" (Female)" if "Female" in current_title else ""))
        return "கிருஷ்ண துதி", "Krishna Thuthi", f"கிருஷ்ண மந்திரம்{var}", None
    if "திருவையாறு திருமுறை" in combo:
        return "பன்னிரு திருமுறை", "Panniru Thirumurai", "திருவையாறு சாரம்", None
    if "ஆதி யோகீஸ்வரர்" in combo or "ஈஸ்வர நாமவளி" in combo:
        return "சிவ நாமாவளி", "Shiva Namavali", current_title.split("|")[0].strip(), None
    if "தில்லை வாழ் அந்தணர்" in combo:
        return "பெரியபுராணம்", "Periyapuranam", "தில்லை வாழ் அந்தணர் சருக்கம்", None
    if "உலகெலாம் உணர்ந்து" in combo:
        return "பெரியபுராணம்", "Periyapuranam", "உலகெலாம் உணர்ந்து ஓதற்கு அரியவன்", None

    # Fallback by genre
    fb = {
        "சிவபெருமான் (Lord Shiva)": ("சிவ பக்திப் பாடல்", "Shiva Devotional"),
        "முருகப் பெருமான் (Lord Murugar)": ("முருகன் துதி", "Murugan Devotional"),
        "விஷ்ணு / கிருஷ்ணர் (Lord Vishnu & Krishna)": ("விஷ்ணு துதி", "Vishnu Devotional"),
        "அம்மன் / சக்தி (Goddess Amman)": ("அம்மன் துதி", "Amman Devotional"),
        "விநாயகர் (Lord Vinayagar)": ("விநாயகர் துதி", "Vinayagar Devotional"),
        "வள்ளலார் / சன்மார்க்கம் (Thiruvarutpa / Sanmargam)": ("திருவருட்பா", "Thiruvarutpa"),
        "மரபு & கலாச்சாரம் (Cultural & Heritage)": ("மரபுப் பாடல்", "Heritage Song")
    }
    fb_tam, fb_eng = fb.get(it_meta.get("genre", ""), ("பக்திப் பாடல்", "Devotional"))
    return fb_tam, fb_eng, current_title.split("|")[0].strip(), None


def build_final_title(tam_s, eng_s, tam_n, orig_title, track_type, eng_override=None):
    # Determine descriptor
    desc = "Film" if ("Film" in track_type or "Video" in track_type or "film" in track_type) else "Audio"
    if "Remix" in orig_title:
        desc = "Remix"

    # Extract english name
    if eng_override:
        eng_n = eng_override
    else:
        parts = orig_title.split("|")
        eng_raw = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        eng_n = clean_english_name(eng_raw, eng_s)
        
        # Fallback transliterations if eng_n ended up empty
        if not eng_n:
            if "தில்லை வாழ் அந்தணர்" in tam_n:
                eng_n = "Thillai Vazh Anthanar"
            elif "உலகெலாம் உணர்ந்து" in tam_n:
                eng_n = "Ulagelam Unarnthu"
            elif "கடவுளைக் கடலுள்" in tam_n:
                eng_n = "Kadavulai Kadalul Ezhu"
            elif "எண்ணப் பதிகம்" in tam_n:
                eng_n = "Ennap Pathigam"
            else:
                eng_n = "Devotional Hymn"

    # Strip any duplicated scripture names from tam_n
    tam_n = re.sub(rf"^{re.escape(tam_s)}\s*[:—–-]\s*", "", tam_n).strip()
    tam_n = re.sub(r"\s+", " ", tam_n).strip()

    # Form title candidate 1: Full bilingual
    # e.g.: திருவாசகம்: சிவபுராணம் | Thiruvasagam: Sivapuranam [Film]
    cand = f"{tam_s}: {tam_n} | {eng_s}: {eng_n} [{desc}]"
    if len(cand) <= 95:
        return cand

    # Form title candidate 2: Compact english
    # e.g.: திருவாசகம்: சிவபுராணம் | Sivapuranam [Film]
    cand = f"{tam_s}: {tam_n} | {eng_n} [{desc}]"
    if len(cand) <= 95:
        return cand

    # Form title candidate 3: Shorten english safely
    max_eng = 95 - len(f"{tam_s}: {tam_n} | ") - len(f" [{desc}]")
    if max_eng > 6:
        cand = f"{tam_s}: {tam_n} | {eng_n[:max_eng].strip()} [{desc}]"
        if len(cand) <= 95:
            return cand

    # Candidate 4: Minimal
    cand = f"{tam_s}: {tam_n} | {desc}"
    return cand[:95].strip()


# Transform all 598 master records
new_master = []
for r in master_records:
    vid = r["video_id"]
    cat_entry = cat_by_id.get(vid)
    tam_s, eng_s, tam_n, eng_ov = classify_where_it_belongs(vid, r["canonical_title"], cat_entry)
    new_title = build_final_title(tam_s, eng_s, tam_n, r["canonical_title"], r.get("track_type", "Cinematic Film / Video"), eng_override=eng_ov)
    
    assert len(new_title) <= 95, f"Title > 95 chars: {new_title}"
    
    r_copy = dict(r)
    r_copy["canonical_title"] = new_title
    r_copy["scripture_source"] = tam_s
    r_copy["length"] = len(new_title)
    
    # Update tamil and english fields
    p = new_title.split("|")
    r_copy["tamil_title"] = p[0].strip()
    r_copy["english_title"] = re.sub(r"\[.*?\]", "", p[1]).strip() if len(p) > 1 else ""
    desc_m = re.search(r"\[(.*?)\]", new_title)
    r_copy["descriptor"] = desc_m.group(1) if desc_m else ""
    
    new_master.append(r_copy)

print(f"Standardized {len(new_master)} master tracks.")

# Save master JSON & CSV
with open(MASTER_JSON, "w", encoding="utf-8") as f:
    json.dump(new_master, f, ensure_ascii=False, indent=2)

with open(MASTER_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "S.No", "Video ID", "Canonical Title", "Scripture Source", "Tamil Title",
        "English Title", "Descriptor", "Length (Chars)", "Genre", "Track Type",
        "Author", "Source", "Playlists", "YouTube URL", "Duration", "Published Date"
    ])
    for i, r in enumerate(new_master, 1):
        writer.writerow([
            i, r["video_id"], r["canonical_title"], r.get("scripture_source", ""),
            r["tamil_title"], r["english_title"], r["descriptor"], r["length"],
            r["genre"], r["track_type"], r["author"], r["source"],
            " ; ".join(r["playlists"]), r["youtube_url"], r["duration"], r["published_at"]
        ])

print("Saved master_all_598_songs_catalog.json and .csv")

# Update assets/data/catalog.json
title_map = {r["video_id"]: r["canonical_title"] for r in new_master}
for cat_name, items in site_catalog.items():
    for it in items:
        if it["id"] in title_map:
            it["title"] = title_map[it["id"]]

with open(CATALOG_JSON, "w", encoding="utf-8") as f:
    json.dump(site_catalog, f, ensure_ascii=False, indent=2)

with open(CATALOG_JS, "w", encoding="utf-8") as f:
    f.write(f"// Complete Curated Web Catalog (598 Compositions Across 8 Sacred Genres)\nwindow.GKD_SITE_CATALOG = {json.dumps(site_catalog, ensure_ascii=False, indent=2)};\n")

print("Saved assets/data/catalog.json and catalog.js")

# Mirror catalogs across site/ and docs/
target_dirs = ["assets/data", "site/assets/data", "docs/assets/data"]
files_to_sync = [
    "master_all_598_songs_catalog.json",
    "master_all_598_songs_catalog.csv",
    "catalog.json",
    "catalog.js"
]

for d in target_dirs:
    os.makedirs(d, exist_ok=True)
    for fn in files_to_sync:
        src_path = fn if os.path.exists(fn) else os.path.join("assets/data", fn)
        dst_path = os.path.join(d, fn)
        if os.path.abspath(src_path) != os.path.abspath(dst_path):
            shutil.copy2(src_path, dst_path)

print("Mirrored all catalogs to assets/data, site/assets/data, docs/assets/data.")

# Verify mirror hash parity
def hash_file(path):
    with open(path, "rb") as fp:
        return hashlib.sha256(fp.read()).hexdigest()

for fn in files_to_sync:
    hashes = [hash_file(os.path.join(d, fn)) for d in target_dirs]
    assert all(h == hashes[0] for h in hashes), f"Mirror parity error for {fn}"

print("100% SHA-256 hash parity verified across all mirrors!")

# Re-generate all_channel_title_updates.json & channel_direct_uploads_pending.json
# Load live YouTube metadata if available
live_meta = {}
if os.path.exists(LIVE_METADATA_JSON):
    with open(LIVE_METADATA_JSON, "r", encoding="utf-8") as f:
        live_meta = json.load(f)

# All channel updates
all_channel_updates = []
for r in new_master:
    vid = r["video_id"]
    if vid in live_meta:
        cur_t = live_meta[vid].get("title", "")
        new_t = r["canonical_title"]
        all_channel_updates.append({
            "video_id": vid,
            "current_title": cur_t,
            "new_title": new_t,
            "changed": cur_t != new_t,
            "length": len(new_t),
            "playlists": r["playlists"]
        })

with open(UPDATES_JSON, "w", encoding="utf-8") as f:
    json.dump(all_channel_updates, f, ensure_ascii=False, indent=2)

with open(UPDATES_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Video ID", "Current YouTube Title", "New Canonical Title", "Length", "Changed"])
    for u in all_channel_updates:
        writer.writerow([u["video_id"], u["current_title"], u["new_title"], u["length"], u["changed"]])

print(f"Generated {len(all_channel_updates)} updates in all_channel_title_updates.json & .csv")

# Filter only Channel Direct Uploads (excluding DistroKid Topic tracks)
channel_direct_uploads = []
for u in all_channel_updates:
    vid = u["video_id"]
    desc = live_meta.get(vid, {}).get("description", "")
    if "Provided to YouTube by DistroKid" not in desc:
        channel_direct_uploads.append(u)

with open(PENDING_JSON, "w", encoding="utf-8") as f:
    json.dump(channel_direct_uploads, f, ensure_ascii=False, indent=2)

print(f"Saved {len(channel_direct_uploads)} Direct Channel Uploads in {PENDING_JSON}")
