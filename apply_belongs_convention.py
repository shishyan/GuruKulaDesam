"""
Format all 598 tracks so the title starts where it belongs (Thiruvasagam, Thevaram, Thirukkural, etc.) followed by the hymn/song name.
Strictly enforce bilingual canonical format and <= 95 characters limit for YouTube Data API.
"""

import json
import re
import csv
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MASTER_JSON = "master_all_598_songs_catalog.json"
CATALOG_JSON = "assets/data/catalog.json"
UPDATES_JSON = "all_channel_title_updates.json"

with open(MASTER_JSON, "r", encoding="utf-8") as f:
    master = json.load(f)

with open(CATALOG_JSON, "r", encoding="utf-8") as f:
    catalog_data = json.load(f)

cat_by_id = {}
for category, items in catalog_data.items():
    for it in items:
        cat_by_id[it["id"]] = (category, it)

def detect_source_and_clean_name(vid, current_title, cat_entry):
    cat_name, cat_data = cat_entry if cat_entry else (None, {})
    src_meta = cat_data.get("source", "")
    auth_meta = cat_data.get("author", "")
    combo = f"{current_title} {src_meta} {auth_meta}"

    # Extract Tamil & English & Descriptor from current title
    parts = current_title.split("|")
    tam_part = parts[0].strip()
    eng_part = parts[1].strip() if len(parts) > 1 else ""

    # Extract descriptor [Film], [Audio], etc.
    desc_match = re.search(r"\[(.*?)\]", current_title)
    descriptor = desc_match.group(1).strip() if desc_match else ""

    # Clean existing prefix if already present
    tam_clean = re.sub(r"^(திருக்குறள்|திருவாசகம்|தேவாரம்|திருவருட்பா|கந்தர் அலங்காரம்|கந்தர் அநுபூதி|கந்த புராணம்|கந்த சஷ்டி கவசம்|திருப்புகழ்|திருப்பாவை|பெரியாழ்வார் திருமொழி|அபிராமி அந்தாதி|விநாயகர் நான்மணிமாலை|விநாயகர் துதி|ஆதிசங்கரர்|சிவ நாமாவளி|மகாவிஷ்ணு துதி|ராம பஜனை|மகா மந்திரம்|பஜனை|நாம சங்கீர்த்தனம்|அம்மன் துதி|தமிழ்த்தாய் வாழ்த்து|ஆலய நாதம்|இசைத் தியானம்|பன்னிரு திருமுறை|சரஸ்வதி போற்றி|கிருஷ்ண துதி)\s*[:—–-]\s*", "", tam_part).strip()
    
    # Remove trailing/embedded parenthetical sources like (திருவாசகம்), (திருவெம்பாவை), (அப்பர் தேவாரம்)
    tam_clean = re.sub(r"\s*\((திருவாசகம்|திருவெம்பாவை|மாணிக்கவாசகர்|அப்பர் தேவாரம்|தேவாரம்|வள்ளலார் திருவருட்பா|வள்ளலார்|ஆண்டாள்|அருணகிரிநாதர்|கந்தபுராணம் வாழ்த்துப் பாடல்|5-ஆம் திருமுறை|மனோன்மணீயம் சுந்தரனார்)\)\s*", " ", tam_clean).strip()

    # Clean english part
    eng_clean = re.sub(r"\[.*?\]", "", eng_part).strip()
    eng_clean = re.sub(r"^(Thirukkural|Thiruvasagam|Thevaram|Thiruvarutpa|Kandhar Alangaram|Kandhar Anuboothi|Kandha Puranam|Kandha Sashti Kavasam|Thiruppugazh|Thiruppavai|Periyazhvar Thirumozhi|Abhirami Andhadhi|Vinayagar|Adi Shankaracharya|Shiva Namavali|Maha Vishnu|Rama Bhajan|Maha Mantra|Bhajan|Nama Sankeerthanam|Amman|Tamil Thai Vazhthu|Aalaya Naatham|Ambient Meditation|Thirumurai|Saraswathi Stotram|Krishna)\s*[:—–-]\s*", "", eng_clean).strip()
    eng_clean = re.sub(r"\s*\((Thiruvasagam|Thiruvempavai|Thevaram|Thiruvarutpa|Kandhar Alangaram)\)\s*", " ", eng_clean).strip()

    # 1. Thirukkural
    if "அதிகாரம்" in current_title or "திருக்குறள்" in combo or "Thirukkural" in combo:
        m = re.search(r"அதிகாரம்\s+(\d+)\s*-\s*([^|\[\(]+)", current_title)
        if m:
            adh_num = m.group(1).strip()
            adh_name = m.group(2).strip()
            # check if part 1 or part 2 or remix or original
            variant = ""
            if "பகுதி 1" in current_title or " I " in current_title or " Part 1" in current_title:
                variant = " (பகுதி 1)"
            elif "பகுதி 2" in current_title or " II " in current_title or " Part 2" in current_title:
                variant = " (பகுதி 2)"
            elif "Remix" in current_title:
                variant = " (Remix)"
            elif "Female" in current_title:
                variant = " (Female)"
            elif "Sad" in current_title:
                variant = " (Sad)"
            elif "Symphony" in current_title:
                variant = " (Symphony)"
            elif "Pop" in current_title:
                variant = " (Pop)"
            elif "Original" in current_title:
                variant = " (Original)"
            
            tam_source = "திருக்குறள்"
            eng_source = "Thirukkural"
            tam_name = f"அதிகாரம் {adh_num} - {adh_name}{variant}"
            return tam_source, eng_source, tam_name, eng_clean, descriptor

    # 2. Thiruvasagam
    if any(k in combo for k in ["திருவாசகம்", "Thiruvasagam", "சிவபுராணம்", "அச்சோ", "குழைத்த", "திருவெம்பாவை", "அன்னைப்பத்து", "பூவார் சென்னி", "திருப்புலம்பல்", "மாணிக்கவாசகர்", "தென்னாடுடைய", "போற்றித் திருஅகவல்", "வேண்டுமே இத்தனையும்"]):
        tam_source = "திருவாசகம்"
        eng_source = "Thiruvasagam"
        # specific hymn refinement
        if "சிவபுராணம்" in tam_clean:
            tam_name = "சிவபுராணம்"
            if "2026 (II)" in current_title or " II " in current_title:
                tam_name += " II"
        elif "அச்சோ" in tam_clean:
            tam_name = "அச்சோப் பதிகம்"
        elif "பூவார் சென்னி" in tam_clean:
            tam_name = "பூவார் சென்னி மன்னன் (யாத்திரைப் பத்து)"
        elif "திருப்புலம்பல்" in tam_clean:
            tam_name = "திருப்புலம்பல்"
        elif "அன்னைப்பத்து" in tam_clean:
            tam_name = "அன்னைப்பத்து"
        elif "தென்னாடுடைய" in tam_clean:
            tam_name = "தென்னாடுடைய சிவனே போற்றி"
        elif "குழைத்த பத்து" in tam_clean:
            tam_name = "குழைத்த பத்து"
        elif "வேண்டுமே இத்தனையும்" in tam_clean:
            tam_name = "வேண்டுமே இத்தனையும் (திருவெம்பாவை)"
        elif "போற்றித் திருஅகவல்" in tam_clean:
            tam_name = "போற்றித் திருஅகவல்"
        elif "ஆதியும் அந்தமும்" in tam_clean:
            tam_name = "திருவெம்பாவை (ஆதியும் அந்தமும்)"
        else:
            tam_name = tam_clean
        return tam_source, eng_source, tam_name, eng_clean, descriptor

    # 3. Thevaram
    if any(k in combo for k in ["தேவாரம்", "Thevaram", "திருநீற்று", "மந்திரமாவது நீறு", "மாசில் வீணையும்", "துஞ்சலும்", "திருவோத்தூர்", "பூத்தேர்ந்து", "அன்னம் பாலிக்கும்", "பண்டாய", "நாமார்க்கும்", "திருநாவுக்கரசு", "அப்பர்", "சம்பந்தர்", "சுந்தரர்", "அவிநாசி"]):
        tam_source = "தேவாரம்"
        eng_source = "Thevaram"
        if "மாசில் வீணையும்" in tam_clean:
            tam_name = "மாசில் வீணையும்"
        elif "திருநீற்று" in tam_clean or "மந்திரமாவது" in tam_clean:
            tam_name = "திருநீற்றுப் பதிகம் (மந்திரமாவது நீறு)"
        elif "துஞ்சலும்" in tam_clean:
            tam_name = "நமச்சிவாயப் பதிகம் (துஞ்சலும் துஞ்சல்)"
        elif "பூத்தேர்ந்து" in tam_clean or "திருவோத்தூர்" in tam_clean:
            tam_name = "திருவோத்தூர் பதிகம் (பூத்தேர்ந்து ஆயன)"
        elif "அன்னம் பாலிக்கும்" in tam_clean:
            tam_name = "தில்லைத் திருப்பதிகம் (அன்னம் பாலிக்கும்)"
        elif "பண்டாய" in tam_clean:
            tam_name = "பண்டாய நான்மறை"
        elif "அவிநாசி" in tam_clean:
            tam_name = "அவிநாசிப் பதிகம்"
        else:
            tam_name = tam_clean
        return tam_source, eng_source, tam_name, eng_clean, descriptor

    # 4. Thiruvarutpa / Vallalar
    if any(k in combo for k in ["திருவருட்பா", "Thiruvarutpa", "வள்ளலார்", "அருட்பெருஞ்சோதி", "சிவ சுப்ரமணியர்", "கொடைமட", "திருவருள் வேட்கை", "பெற்றை", "சுப்ரமண்யர் திருவிருத்தம்"]):
        tam_source = "திருவருட்பா"
        eng_source = "Thiruvarutpa"
        if "சிவ சுப்ரமணியர்" in tam_clean or "சுப்ரமண்யர் திருவிருத்தம்" in tam_clean:
            tam_name = "சிவ சுப்ரமணியர் திருவிருத்தம்"
        elif "அருட்பெருஞ்சோதி" in tam_clean:
            tam_name = "அருட்பெருஞ்சோதி அகவல்"
            if " II" in current_title or " 2" in current_title:
                tam_name += " II"
        elif "கொடைமட" in tam_clean:
            tam_name = "கொடைமடப் புகழ்ச்சி"
        elif "திருவருள் வேட்கை" in tam_clean:
            tam_name = "திருவருள் வேட்கை"
        elif "திருச்சாதனத்" in tam_clean:
            tam_name = "திருச்சாதனத் தெய்வத் திறம்"
        else:
            tam_name = tam_clean
        return tam_source, eng_source, tam_name, eng_clean, descriptor

    # 5. Kandhar Alangaram
    if "கந்தர் அலங்காரம்" in combo or "நாள் என் செய்யும்" in combo:
        return "கந்தர் அலங்காரம்", "Kandhar Alangaram", "நாள் என் செய்யும்", eng_clean, descriptor

    # 6. Kandhar Anuboothi
    if "கந்தர் அநுபூதி" in combo or "உருவாய் அருவாய்" in combo:
        return "கந்தர் அநுபூதி", "Kandhar Anuboothi", "உருவாய் அருவாய்", eng_clean, descriptor

    # 7. Kandha Sashti Kavasam
    if "கந்த சஷ்டி கவசம்" in combo or "Kandha Sashti" in combo or "சஷ்டி கவசம்" in combo:
        return "கந்த சஷ்டி கவசம்", "Kandha Sashti Kavasam", "முழு கவசம்", eng_clean, descriptor

    # 8. Kandha Puranam
    if "கந்த புராணம்" in combo or "வான் முகில்" in combo or "வான்முகில்" in combo:
        return "கந்த புராணம்", "Kandha Puranam", "வான் முகில் வழாது பெய்க", eng_clean, descriptor
    if "திகட சக்கர" in combo:
        return "கந்த புராணம்", "Kandha Puranam", "காப்பு - திகட சக்கர சண்முகத்தோன்", eng_clean, descriptor

    # 9. Thiruppavai
    if "திருப்பாவை" in combo or "மார்கழித் திங்கள்" in combo or "வையத்து வாழ்வீர்" in combo or "ஆண்டாள்" in combo:
        tam_source = "திருப்பாவை"
        eng_source = "Thiruppavai"
        if "மார்கழித் திங்கள்" in combo or "1" in current_title:
            tam_name = "பாசுரம் 1 - மார்கழித் திங்கள்"
        elif "வையத்து வாழ்வீர்" in combo or "2" in current_title:
            tam_name = "பாசுரம் 2 - வையத்து வாழ்வீர்"
        else:
            tam_name = tam_clean
        return tam_source, eng_source, tam_name, eng_clean, descriptor

    # 10. Periyazhvar Thirumozhi
    if "பெரியாழ்வார்" in combo or "கண்ணன் தாலாட்டு" in combo or "Periyazhvar" in combo:
        tam_source = "பெரியாழ்வார் திருமொழி"
        eng_source = "Periyazhvar Thirumozhi"
        tam_name = "கண்ணன் தாலாட்டு"
        if " III" in current_title or "(III)" in current_title:
            tam_name += " III"
        return tam_source, eng_source, tam_name, eng_clean, descriptor

    # 11. Abhirami Andhadhi
    if "அபிராமி அந்தாதி" in combo or "Abhirami Andhathi" in combo or "தனந்தரும் கல்விதரும்" in combo:
        return "அபிராமி அந்தாதி", "Abhirami Andhadhi", "தனந்தரும் கல்விதரும்", eng_clean, descriptor

    # 12. Vinayagar Nanmanimalai / Avvaiyar
    if "நான்மணிமாலை" in combo or "பாலும் தெளிதேனும்" in combo:
        return "விநாயகர் நான்மணிமாலை", "Vinayagar Nanmanimalai", "பாலும் தெளிதேனும்", eng_clean, descriptor

    # 13. Adi Shankaracharya Stotras
    if "கணேச பஞ்சரத்னம்" in combo:
        return "ஆதிசங்கரர்", "Adi Shankara", "மகா கணேச பஞ்சரத்னம்", eng_clean, descriptor
    if "வேதஸார சிவ" in combo:
        return "ஆதிசங்கரர்", "Adi Shankara", "வேதஸார சிவ ஸ்தோத்ரம்", eng_clean, descriptor

    # 14. Saraswathi Potri
    if "சரஸ்வதி போற்றி" in combo or "சரஸ்வதி அஷ்டோத்தர" in combo:
        return "சரஸ்வதி போற்றி", "Saraswathi Stotram", "108 போற்றி", eng_clean, descriptor

    # 15. Periyapuranam
    if "பெரியபுராணம்" in combo or "உலகெலாம் உணர்ந்து" in combo:
        return "பெரியபுராணம்", "Periyapuranam", "உலகெலாம் உணர்ந்து ஓதற்கு அரியவன்", eng_clean, descriptor

    # 16. Tamil Thai Vazhthu
    if "தமிழ்த்தாய் வாழ்த்து" in combo or "நீராரும் கடலுடுத்த" in combo:
        return "தமிழ்த்தாய் வாழ்த்து", "Tamil Thai Vazhthu", "நீராரும் கடலுடுத்த", eng_clean, descriptor

    # 17. Temple / Ambient Instrumental
    if "ஆலய நாதம்" in combo:
        return "ஆலய நாதம்", "Aalaya Naatham", "இந்திய ஹார்மோனிக்கா தியானம்", eng_clean, descriptor
    if "Interstellar" in combo:
        return "இசைத் தியானம்", "Ambient Meditation", "இன்டர்ஸ்டெல்லார்", eng_clean, descriptor

    # 18. Specific Deity Hymns & Bhajans
    if "நமோ நாராயணம்" in combo or "தசாவதாரம்" in combo:
        return "மகாவிஷ்ணு துதி", "Maha Vishnu", "நமோ நாராயணம் (தசாவதாரம்)", eng_clean, descriptor
    if "ரகுபதி ராகவ" in combo:
        return "ராம பஜனை", "Rama Bhajan", "ரகுபதி ராகவ ராஜா ராம்", eng_clean, descriptor
    if "ஹரே கிருஷ்ணா" in combo:
        return "மகா மந்திரம்", "Maha Mantra", "ஹரே கிருஷ்ணா ஹரே ராமா", eng_clean, descriptor
    if "இராம கிருஷ்ண துதி" in combo:
        return "பஜனை", "Bhajan", "இராம கிருஷ்ண துதி", eng_clean, descriptor
    if "இராம ராம ராம" in combo:
        return "நாம சங்கீர்த்தனம்", "Nama Sankeerthanam", "இராம ராம ராம ஹரே", eng_clean, descriptor
    if "மகாமாயி" in combo:
        return "அம்மன் துதி", "Amman Thuthi", "மகாமாயி சமயபுரத்தாயே", eng_clean, descriptor
    if "கண நாதா ஓம்" in combo:
        return "விநாயகர் துதி", "Vinayagar Thuthi", "கண நாதா ஓம்", eng_clean, descriptor
    if "திருவையாறு திருமுறை" in combo:
        return "பன்னிரு திருமுறை", "Panniru Thirumurai", "திருவையாறு சாரம்", eng_clean, descriptor
    if "ஆதி யோகீஸ்வரர்" in combo:
        return "சிவ நாமாவளி", "Shiva Namavali", "ஆதி யோகீஸ்வரர் நாம ஒளி சரணம்", eng_clean, descriptor
    if "ஈஸ்வர நாமவளி" in combo:
        return "சிவ நாமாவளி", "Shiva Namavali", tam_clean, eng_clean, descriptor
    if "கிருஷ்ண மந்திரம்" in combo:
        return "கிருஷ்ண துதி", "Krishna Thuthi", tam_clean, eng_clean, descriptor
    if "தில்லை வாழ் அந்தணர்" in combo:
        return "பெரியபுராணம்", "Periyapuranam", "தில்லை வாழ் அந்தணர் சருக்கம்", eng_clean, descriptor

    # Fallback to genre
    genre_fallback = {
        "சிவபெருமான் (Lord Shiva)": ("சிவ பக்திப் பாடல்", "Shiva Devotional"),
        "முருகப் பெருமான் (Lord Murugar)": ("முருகன் துதி", "Murugan Devotional"),
        "விஷ்ணு / கிருஷ்ணர் (Lord Vishnu & Krishna)": ("விஷ்ணு துதி", "Vishnu Devotional"),
        "அம்மன் / சக்தி (Goddess Amman)": ("அம்மன் துதி", "Amman Devotional"),
        "விநாயகர் (Lord Vinayagar)": ("விநாயகர் துதி", "Vinayagar Devotional"),
        "வள்ளலார் / சன்மார்க்கம் (Thiruvarutpa / Sanmargam)": ("திருவருட்பா", "Thiruvarutpa"),
        "மரபு & கலாச்சாரம் (Cultural & Heritage)": ("மரபுப் பாடல்", "Heritage Song")
    }
    fb_tam, fb_eng = genre_fallback.get(cat_data.get("genre", ""), ("பக்திப் பாடல்", "Devotional"))
    return fb_tam, fb_eng, tam_clean, eng_clean, descriptor


def assemble_canonical_title(tam_source, eng_source, tam_name, eng_name, descriptor):
    # Shorten descriptor if needed
    desc = descriptor
    if "Film" in descriptor:
        desc = "Film"
    elif "Audio" in descriptor:
        desc = "Audio"
    elif "Song" in descriptor:
        desc = "Song"
    
    # Clean redundant punctuation in names
    tam_name = re.sub(r"\s+", " ", tam_name).strip()
    eng_name = re.sub(r"\s+", " ", eng_name).strip()

    # Try full bilingual format:
    # <Tamil Source>: <Tamil Name> | <English Source>: <English Name> [<Desc>]
    cand = f"{tam_source}: {tam_name} | {eng_source}: {eng_name} [{desc}]"
    if len(cand) <= 95:
        return cand
    
    # If too long, drop english source prefix:
    # <Tamil Source>: <Tamil Name> | <English Name> [<Desc>]
    cand = f"{tam_source}: {tam_name} | {eng_name} [{desc}]"
    if len(cand) <= 95:
        return cand
    
    # If still too long, shorten descriptor or compact
    cand = f"{tam_source}: {tam_name} | {eng_name}"
    if len(cand) <= 95:
        return cand
    
    # Truncate english safely
    max_eng = 95 - len(f"{tam_source}: {tam_name} | ") - len(f" [{desc}]")
    if max_eng > 10:
        cand = f"{tam_source}: {tam_name} | {eng_name[:max_eng].strip()} [{desc}]"
        if len(cand) <= 95:
            return cand
    
    return cand[:95].strip()

# Run through master records
updated_master = []
too_long = []
for r in master:
    vid = r["video_id"]
    cat_entry = cat_by_id.get(vid)
    tam_s, eng_s, tam_n, eng_n, desc = detect_source_and_clean_name(vid, r["canonical_title"], cat_entry)
    new_title = assemble_canonical_title(tam_s, eng_s, tam_n, eng_n, desc)
    
    if len(new_title) > 95:
        too_long.append((vid, new_title, len(new_title)))
    
    r_copy = dict(r)
    r_copy["canonical_title"] = new_title
    r_copy["tamil_title"] = f"{tam_s}: {tam_n}"
    r_copy["english_title"] = eng_n
    r_copy["descriptor"] = desc
    r_copy["length"] = len(new_title)
    r_copy["scripture_source"] = tam_s
    updated_master.append(r_copy)

print(f"Total processed tracks: {len(updated_master)}")
print(f"Titles exceeding 95 chars: {len(too_long)}")

# Display 25 samples
print("\n--- SAMPLE FORMATTED TITLES (WHERE IT BELONGS FIRST) ---")
for r in updated_master[::24][:25]:
    print(f"[{r['video_id']}] ({r['length']:02d} chars) : {r['canonical_title']}")
