import os
import re

GRADE_CARD_ARTWORKS = {
    1: {
        "image": "assets/images/lessons/children_feeding_creatures.jpg",
        "alt": "தரம் 1 — பாலப் பருவ நற்பண்புகள் & உயிர்களிடத்தில் அன்பு"
    },
    2: {
        "image": "assets/images/lessons/shiva_tripundram.jpg",
        "alt": "தரம் 2 — சிவ சின்னங்கள் & ஆலய வழிபாடு"
    },
    3: {
        "image": "assets/images/lessons/grade3_naalvar_saints.jpg",
        "alt": "தரம் 3 — சமய குரவர் நால்வர் & பஞ்ச பூத ஸ்தலங்கள்"
    },
    4: {
        "image": "assets/images/lessons/grade4_appar_service.jpg",
        "alt": "தரம் 4 — பன்னிரு திருமுறைகள் & அப்பர் உழவாரப் பணி"
    },
    5: {
        "image": "assets/images/lessons/grade5_sundarar_thiruvarur.jpg",
        "alt": "தரம் 5 — 63 நாயன்மார்கள் & சுந்தரமூர்த்தி நாயனார்"
    },
    6: {
        "image": "assets/images/lessons/grade6_pancha_maha_yajna.jpg",
        "alt": "தரம் 6 — நான்கு வேதங்கள் & பஞ்ச மகா யக்ஞங்கள்"
    },
    7: {
        "image": "assets/images/lessons/grade7_periyapuranam_sekkizhar.jpg",
        "alt": "தரம் 7 — பெரியபுராணம் & சேக்கிழார் பெருமான்"
    },
    8: {
        "image": "assets/images/lessons/grade8_chatur_ashrama.jpg",
        "alt": "தரம் 8 — சதுர் ஆசிரமங்கள் & இல்லற தர்மம்"
    },
    9: {
        "image": "assets/images/lessons/grade9_saiva_agamas.jpg",
        "alt": "தரம் 9 — 28 சைவ ஆகமங்கள் & உடலே ஆலயம்"
    },
    10: {
        "image": "assets/images/lessons/grade10_pati_pasu_pasam.jpg",
        "alt": "தரம் 10 — பதி பசு பாசம் & நால்வகை நெறிகள்"
    },
    11: {
        "image": "assets/images/lessons/mountain_cave_tapas.jpg",
        "alt": "தரம் 11 — வேதாந்த சித்தாந்த ஒப்பாய்வு & குகைத் தவம்"
    },
    12: {
        "image": "assets/images/lessons/grade12_jivanmukti_36tattvas.jpg",
        "alt": "தரம் 12 — ஜீவன் முக்தி & 36 தத்துவங்கள்"
    }
}

def update_kalvi_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for g, art in GRADE_CARD_ARTWORKS.items():
        media_html = f'''          <div class="grade-card-media">
            <img src="{art['image']}" alt="{art['alt']}" loading="lazy">
            <div class="grade-card-media-overlay"></div>
          </div>\n'''
        
        # Check if media_html is already there
        if f'class="grade-card-media"' in content and art['image'] in content:
            continue
            
        pattern = rf'(<a href="tharam-{g}\.html" id="grade-{g}" class="grade-card">\s*)(<div>)'
        
        def repl(m):
            return f'{m.group(1)}{media_html}          {m.group(2)}'
            
        new_content, count = re.subn(pattern, repl, content)
        if count > 0:
            content = new_content
            print(f"[{filepath}] Embedded artwork for Grade {g}")
        else:
            print(f"[{filepath}] Pattern not matched for Grade {g}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for path in ['kalvi.html', 'docs/kalvi.html', 'site/kalvi.html']:
    if os.path.exists(path):
        update_kalvi_file(path)
print("Kalvi Hub grade card artwork integration complete!")
