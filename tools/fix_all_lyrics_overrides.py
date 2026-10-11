#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_all_lyrics_overrides.py
Applies canonical lyric fixes to youtube_lyrics_overrides.json and all_songs_lyrics_and_meanings.json.
Fixes:
- Naatha Vindhugal (nuSx1NgiCuo, C9Ea0-FfMNs)
- Muthaith Tharu (3oJ2OPG-WCs, On2xoZqBsss)
- Seer Ulaaviya 712 (YxP_uh3dM18, iPFEtwdcIxc, Nvx3ObuSndM)
- Rathinagiri 566 (S4ogw4EfpDY, bOxyDZgsI2c)
- Thiruppugazh Vilasam (l3E27q5r-nk)
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES_FILE = ROOT / "production" / "youtube_lyrics_overrides.json"
LYRICS_DB_FILE = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"

RATHINAGIRI_566_LYRICS = """சுற்ற கபடோடு பல சூதுவினையான பல
கற்ற களவோடு பழிகாரர் கொலைகாரர்
சுற்ற விழலான பவிஷோடு கடல்மூழ்கி
வரு துயர்மேவித் துக்க சமுசார வலைமீனே

தீயில் மெழுகான உடல் சுத்தமறி யாதபடி
காயமதில் மேவிவரும் பொறியாலே சற்றுமறி
யாதகலி காலன்வரு நேரமதில் தத்துமொரு
அறியாம லோடியாடி வருசூதர் ஐவர்சத்த

பரிசான மணரூப ரசமான பொய்மைவிளை
யாடித் தக்கமட வார்மனையை நாடியவரோடு
சித்து விளையாடுவினை சீசி யிதுநாறும்
உடல் தத்தி முடிவாகி விடுவேனொ முடியாது

திக்குமுகி லாடஅரி யாடஅய னாடசிவ
னொத்துவிளை யாடபரை யாடவர ராடபல
திக்கசுரர் வாடசுரர் பாடமறை பாடஎதிர்
பூதகண மாடவொளி யாடவிடு வடிவேலா

சித்தமலை காமுககுகா நமசி வாயனொடு
ரத்நகிரி வாழ்முருக னேயிளைய வாவமரர்
பெருமாளே!"""

RATHINAGIRI_566_MEANING = """உலக மாயையிலும் தீவினைகளிலும் உழன்று அழியாமல், தன் அருள் திருவடியைத் தந்தருள வேண்டும் என்று இரத்தினகிரி முருகப்பெருமானை அருணகிரிநாதர் வேண்டும் நாதத் திருப்புகழ்."""

THIRUPPUGAZH_VILASAM_LYRICS = """துங்க வெண்பொடி அணிந்துநின் கோயில் தொழும்பு செய்துநின்
துணைப்பதம் ஏத்திச் செங்கண் மால்அயன்
தேடியும் காணாச் செல்வ நின்அருள்
சேர்குவ தென்றோ எங்கள் உள்ளுவந்

தூறிய அமுதே இன்ப மேஇமை
யான்மகட் கரசே திங்கள் தங்கிய
சடையுடை மருந்தே திகழும் ஒற்றியூர்ச்
சிவபெரு மானே!"""

THIRUPPUGAZH_VILASAM_MEANING = """திருவொற்றியூர் சிவபெருமானின் திருவடிகளைத் தொழுது, திருநீறு அணிந்து, என்றும் அவன் திருவருளை அடைந்து இன்புற வேண்டும் எனப் போற்றும் வள்ளலாரின் திருவருட்பாத் திருப்புகழ் விலாசம்."""

def main():
    with open(OVERRIDES_FILE, "r", encoding="utf-8") as f:
        overrides = json.load(f)

    with open(LYRICS_DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    works = overrides.setdefault("_works", {})

    # 1. Add works
    works["rathinagiri566"] = {
        "status": "ok",
        "source": "Arunagirinathar, Thiruppugazh 566 (Rathnagiri) 'Sutra Kabadodu' (public domain); kaumaram.com / mayuragiri.com",
        "lyrics": RATHINAGIRI_566_LYRICS,
        "meaning": RATHINAGIRI_566_MEANING
    }

    works["thiruppugazh_vilasam"] = {
        "status": "ok",
        "source": "Vallalar (Ramalinga Adigal), Thiruvarutpa 'Thiruppugazh Vilasam' (Thiruvottriyur Shiva); sangampedia.net / projectmadurai.org",
        "lyrics": THIRUPPUGAZH_VILASAM_LYRICS,
        "meaning": THIRUPPUGAZH_VILASAM_MEANING
    }

    # 2. Map track overrides
    track_mappings = {
        # Naatha Vindhugal
        "nuSx1NgiCuo": "naathavindhu",
        "C9Ea0-FfMNs": "naathavindhu",

        # Muthaith Tharu
        "3oJ2OPG-WCs": "muthaitharu",
        "On2xoZqBsss": "muthaitharu",

        # Seer Ulaaviya 712
        "YxP_uh3dM18": "seerulaaviya",
        "iPFEtwdcIxc": "seerulaaviya",
        "Nvx3ObuSndM": "seerulaaviya",

        # Rathinagiri 566
        "S4ogw4EfpDY": "rathinagiri566",
        "bOxyDZgsI2c": "rathinagiri566",

        # Thiruppugazh Vilasam
        "l3E27q5r-nk": "thiruppugazh_vilasam",
    }

    for tid, ref_key in track_mappings.items():
        overrides[tid] = {"ref": ref_key}
        print(f"Mapped override: {tid} -> {ref_key}")

        # Also update DB directly
        ref_work = works.get(ref_key, {})
        if tid in db and ref_work:
            db[tid]["tamil_lyrics"] = ref_work.get("lyrics", "")
            db[tid]["tamil_meaning"] = ref_work.get("meaning", "")
            db[tid]["author"] = ref_work.get("source", db[tid].get("author", ""))
            print(f"Updated DB entry for {tid}: {ref_work.get('lyrics', '')[:40]}...")

    with open(OVERRIDES_FILE, "w", encoding="utf-8") as f:
        json.dump(overrides, f, ensure_ascii=False, indent=2)
    print(f"\nSaved updated {OVERRIDES_FILE}")

    with open(LYRICS_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"Saved updated {LYRICS_DB_FILE}")

if __name__ == "__main__":
    main()
