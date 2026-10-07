# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Colab Artworks Ingestion & Tri-Folder Mirroring Utility
Extracts `gurukuladesam_artworks.zip` generated from Google Colab,
mirrors all lesson images across ./, docs/, and site/,
updates curriculum_enricher.py with the new artworks,
updates review_quality.html if Thirukkural visuals are added,
and rebuilds all grade coursebooks.
"""

import sys
import os
import re
import shutil
import zipfile
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent

# Mapping of the remaining 11 bespoke artworks for Grades 8 to 12
NEW_ARTWORK_MAP = {
    (8, 4): {
        "image": "assets/images/lessons/grade8_chatur_ashrama.jpg",
        "caption": "சதுர் ஆசிரமங்கள் — இல்லற தர்மமே மற்ற அனைத்து ஆசிரமங்களுக்கும் தூணாக அமையும் உன்னத மாண்பு"
    },
    (9, 1): {
        "image": "assets/images/lessons/grade9_saiva_agamas.jpg",
        "caption": "இருபத்தெட்டு சைவ ஆகமங்கள் — சரியை, கிரியை, யோகம், ஞானம் நல்கும் திருக்கோயில் ஆகம சாஸ்திரம்"
    },
    (9, 2): {
        "image": "assets/images/lessons/grade9_body_is_temple.jpg",
        "caption": "உடலே ஆலயம் — 'உள்ளம் பெருங்கோயில் ஊனுடம்பு ஆலயம்' எனும் திருமந்திர மெய்ஞ்ஞானத் தத்துவம்"
    },
    (9, 3): {
        "image": "assets/images/lessons/grade9_shaddarshanas_dialogue.jpg",
        "caption": "பாரதத்தின் ஷட்தர்சனங்கள் — நியாயம், வைசேஷிகம், சாங்கியம், யோகம், மீமாம்சம், வேதாந்த தரிசன உரையாடல்"
    },
    (10, 1): {
        "image": "assets/images/lessons/grade10_pati_pasu_pasam.jpg",
        "caption": "பதி பசு பாசம் — பதிப் பரம்பொருளின் பேரருளால் ஆணவம், கன்மம், மாயை நீங்கி ஆன்மா முக்தி பெறுதல்"
    },
    (10, 4): {
        "image": "assets/images/lessons/grade10_temple_chariot_festival.jpg",
        "caption": "திருக்கோயில் தேர்த் திருவிழா — ஆயிரக்கணக்கான அடியார்கள் ஒருமனப்பட்டு வடம் பிடிக்கும் பக்திப் பெருவிழா"
    },
    (11, 2): {
        "image": "assets/images/lessons/grade11_nachiketas_yama.jpg",
        "caption": "கதா உபநிடதம் — இளம் நசிகேதன் எமதர்மனிடம் சாகா வரம் மற்றும் ஆத்ம ஞானம் உசாவும் மெய்யறிவு"
    },
    (11, 4): {
        "image": "assets/images/lessons/grade11_pancha_koshas.jpg",
        "caption": "பஞ்ச கோசங்கள் — அன்னமய, பிராணமய, மனோமய, விஞ்ஞானமய, ஆனந்தமய கோசங்கள் கடந்த ஆன்ம நிலை"
    },
    (12, 1): {
        "image": "assets/images/lessons/grade12_jivanmukti_36tattvas.jpg",
        "caption": "ஜீவன்முக்தி & 36 தத்துவங்கள் — முப்பத்தாறு தத்துவங்களையும் கடந்து உடலோடு வாழும் போதே அடையும் சிவானந்தப் பேறு"
    },
    (12, 2): {
        "image": "assets/images/lessons/grade12_thayumanavar_universal.jpg",
        "caption": "தாயுமானவ சுவாமிகள் — 'எல்லாரும் இன்புற்றிருக்க நினைப்பதுவே யல்லாமல் வேறொன்றறியேன் பராபரமே'"
    },
    (12, 5): {
        "image": "assets/images/lessons/grade12_grihastha_nirvana.jpg",
        "caption": "இல்லற தர்மமே அதிவேக முக்தி — அறவழியில் குடும்பம் நடத்தி உலகிற்கு வழிகாட்டும் சான்றோன் பெருநெறி"
    }
}

def find_zip_file():
    candidates = [
        ROOT / "gurukuladesam_artworks.zip",
        Path.home() / "Downloads" / "gurukuladesam_artworks.zip",
        Path.home() / "Desktop" / "gurukuladesam_artworks.zip"
    ]
    for c in candidates:
        if c.exists() and c.stat().st_size > 1000:
            return c
    return None

def extract_and_mirror(zip_path):
    print(f"📦 Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(ROOT)
    
    # Mirror assets/images/lessons to docs/ and site/
    lessons_dir = ROOT / "assets" / "images" / "lessons"
    for dest_root in [ROOT / "docs" / "assets" / "images" / "lessons", ROOT / "site" / "assets" / "images" / "lessons"]:
        dest_root.mkdir(parents=True, exist_ok=True)
        if lessons_dir.exists():
            for img in lessons_dir.glob("*.jpg"):
                dest = dest_root / img.name
                shutil.copy2(img, dest)
    print("✅ Mirrored all lesson artworks across root, docs/, and site/.")

def update_curriculum_enricher():
    enricher_file = ROOT / "curriculum_enricher.py"
    with open(enricher_file, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    for (g, u), data in NEW_ARTWORK_MAP.items():
        img_path = data["image"]
        new_caption = data["caption"]
        actual_img = ROOT / img_path
        
        if actual_img.exists():
            # Regex pattern for this unit's block in UNIT_VISUAL_MAP
            # e.g., (8, 4): { ... "hero_image": "...", "hero_caption": "..." }
            pattern = re.compile(
                rf'(\({g},\s*{u}\):\s*\{{[^}}]*?"hero_image":\s*")[^"]*(".*?hero_caption":\s*")[^"]*(")',
                re.DOTALL
            )
            
            def replace_unit(match):
                nonlocal modified
                modified = True
                return f'{match.group(1)}{img_path}{match.group(2)}{new_caption}{match.group(3)}'
                
            content, count = pattern.subn(replace_unit, content, count=1)
            if count > 0:
                print(f"✅ Mapped Unit ({g}, {u}) -> {img_path}")
            else:
                print(f"⚠️ Could not find exact pattern for Unit ({g}, {u})")

    if modified:
        with open(enricher_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Saved updated curriculum_enricher.py")
        
        # Re-run coursebook builder
        print("🔨 Rebuilding all grade coursebooks...")
        subprocess.run(["python", "build_all_tharam_curriculum.py"], check=True)
        print("✅ All 11 coursebooks rebuilt successfully across root, docs/, and site/!")

def main():
    print("=== Guru Kula Desam Artworks Ingestion Utility ===")
    zip_path = find_zip_file()
    if not zip_path:
        print("❌ Could not find 'gurukuladesam_artworks.zip'.")
        print("   Please ensure you have placed the downloaded zip file in Downloads or Desktop.")
        return
    
    extract_and_mirror(zip_path)
    update_curriculum_enricher()
    print("\n🎉 Ingestion completed successfully!")

if __name__ == '__main__':
    main()
