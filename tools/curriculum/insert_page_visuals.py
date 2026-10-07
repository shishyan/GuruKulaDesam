#!/usr/bin/env python3
"""
tools/curriculum/insert_page_visuals.py
Inserts authentic classical Tamil sacred oil painting showcases (minimum 2 images)
into the primary entry points and major page groups.
"""

import os
import re

PAGE_VISUAL_MAP = {
    'thirukkural.html': [
        ('assets/images/lessons/thirukkural_valluvar.jpg', 'தெய்வப்புலவர் திருவள்ளுவர்', 'உலகப் பொதுமறை திருக்குறள் அருளிய தெய்வப் புலவர் பெருமான்'),
        ('assets/images/lessons/harvesting_family_dharma.jpg', 'இல்லற மாண்பும் உழவுத் தொழிலும்', 'உழுதுண்டு வாழ்வாரே வாழ்வார் மற்றெல்லாம் தொழுதுண்டு பின்செல் பவர்')
    ],
    'saiva-neri.html': [
        ('assets/images/lessons/nataraja_cosmic_dance.jpg', 'ஆனந்த நடராஜப் பெருமான்', 'சிதம்பரப் பேரம்பலத்தில் அண்ட சராசரங்களையும் இயக்கும் ஆடல்வல்லான்'),
        ('assets/images/lessons/grade3_naalvar_saints.jpg', 'சமயக் குரவர் நால்வர் பெருமக்கள்', 'அப்பர், சுந்தரர், ஞானசம்பந்தர் மற்றும் மாணிக்கவாசகர் அருளிய திருமுறைகள்')
    ],
    'sanmargam.html': [
        ('assets/images/lessons/grade8_vallalar_jyothi.jpg', 'வள்ளலார் அருட்பெருஞ்ஜோதி தரிசனம்', 'அருட்பெருஞ்ஜோதி தனிப்பெருங்கருணை — வடலூர் சத்ய ஞான சபை'),
        ('assets/images/lessons/children_feeding_creatures.jpg', 'ஜீவகாருண்ய ஒழுக்கம்', 'எவ்வுயிரும் தன்னுயிர்போல் எண்ணும் ஆன்மநேய ஒருமைப்பாடு')
    ],
    'school.html': [
        ('assets/images/lessons/disciples_under_sacred_tree.jpg', 'குருகுல மரபுவழிக் கல்வி', 'ஆலமர நிழலில் குரு சீடர் இடையே நிகழும் விவேக உபதேசம்'),
        ('assets/images/lessons/grade9_body_is_temple.jpg', 'உடலே ஆலயம் — திருமந்திர யோகம்', 'உள்ளம் பெருங்கோயில் ஊனுடம்பு ஆலயம் — திருமூலர் யோகப் பெருநெறி')
    ],
    'syllabus.html': [
        ('assets/images/lessons/grade8_chatur_ashrama.jpg', 'நான்கு ஆசிரம தர்மங்கள் & இல்லறம்', 'பிரம்மச்சர்யம், இல்லறம், வானப்பிரஸ்தம் மற்றும் சந்நியாச படிநிலைகள்'),
        ('assets/images/lessons/grade9_shaddarshanas_dialogue.jpg', 'ஷட்தரிசன மெய்ப்பொருள் கலந்துரையாடல்', 'வேதாந்த, சித்தாந்த தத்துவங்களை ஆய்ந்தறியும் சான்றோர் பேரவை')
    ],
    'virtues.html': [
        ('assets/images/lessons/dharma_cow_calf.jpg', 'கோமாதா பூஜித ஜீவகாருண்யம்', 'அஹிம்சை, பொறுமை, ஈகை மற்றும் தூய நற்பண்புகளின் வாழ்வியல் வழிகாட்டல்'),
        ('assets/images/lessons/noble_feast_ahimsa.jpg', 'விருந்தோம்பல் & சாத்வீக உணவு', 'இல்வாழ்க்கையின் தலையாய கடமையான அதிதி சற்காரமும் அன்னதானமும்')
    ],
    'classes.html': [
        ('assets/images/lessons/temple_architecture.jpg', 'ஆகமச் சிற்பக் கலை & ஆலயம்', 'பாரம்பரிய கோயில் கட்டிடக் கலை மற்றும் சிற்ப சாஸ்திர வகுப்பு'),
        ('assets/images/lessons/scholar_palm_manuscript.jpg', 'சுவடி வாசிப்பு & மெய்யியல் ஆய்வு', 'ஓலைச்சுவடிகள் வழி தொன்மைப் பாடங்களை மீட்டெடுத்துக் கற்கும் பாங்கு')
    ],
    'about.html': [
        ('assets/images/lessons/gurukulam_sacred_refuge.jpg', 'குருகுல தேச திருத்தலம்', 'வேத சம்ரக்ஷணம் மற்றும் சனாதன தர்மத்தைப் பேணும் தவக்குடீரம்'),
        ('assets/images/lessons/wise_counsel_nobility.jpg', 'சான்றோர் வழிகாட்டல் & அறநெறி', 'காஞ்சி மகா பெரியவா அருளிய தெய்வத்தின் குரல் வழிகாட்டல்')
    ],
    'help.html': [
        ('assets/images/lessons/universal_anjali_prayer.jpg', 'அஞ்சலி முத்திரை கூட்டுப் பிரார்த்தனை', 'மாணவர், ஆசிரியர் மற்றும் சாதகர்களுக்கு உதவும் வழிகாட்டல் கூடம்'),
        ('assets/images/lessons/siddha_herbal_wisdom.jpg', 'சித்த மருத்துவ இயற்கை வாழ்வியல்', 'உடல்-மன ஆரோக்கியமும் தர்ம சிந்தனையும் ஒருங்கே வளர்க்கும் நெறி')
    ],
    'youtube.html': [
        ('assets/images/lessons/temple_bell_morning.jpg', 'விடியற்காலை நாத ஆராதனை', 'ஆலய மணியோசையும் பக்தி இசைச் சுவடிகளின் கானப் பெருவெளியும்'),
        ('assets/images/lessons/sacred_peacock_grove.jpg', 'மயில் நின்றாடும் சோலை', '580 காணொளிகளில் தவழும் இறை இசைப் பண்கள் மற்றும் பக்தி விருந்து')
    ],
    'murugan.html': [
        ('assets/images/lessons/sacred_peacock_grove.jpg', 'மயில்வாகனப் பெருமான் சுப்பிரமணியர்', 'கந்த சஷ்டி கவசம், திருப்புகழ் மற்றும் அறுபடை வீடுகளின் பெருமை'),
        ('assets/images/lessons/mountain_cave_tapas.jpg', 'பழனி மலை தவ முனிவர் தரிசனம்', 'ஞானப்பழமாய் நின்ற வேலவனின் தவக் குன்றத்து மேன்மை')
    ],
    'sakthi.html': [
        ('assets/images/lessons/panchakshara_mandala.jpg', 'ஸ்ரீ சக்ர மகாமேரு & சக்தி வழிபாடு', 'அபிராமி அந்தாதி மற்றும் லலிதா சஹஸ்ரநாம திவ்ய சக்தி'),
        ('assets/images/lessons/grade10_temple_chariot_festival.jpg', 'ஆலயத் திருத்தேர் பவானி', 'அம்பிகையின் அருள் பொழியும் பெருவிழா மற்றும் பக்தி ஆராதனை')
    ],
    'vaishnava.html': [
        ('assets/images/lessons/western_ghats_hermitage.jpg', 'துளசி வனம் & ஆசிரம சரணாகதி', 'நாலாயிர திவ்வியப் பிரபந்தமும் விஷ்ணு சகஸ்ரநாம வழிபாடும்'),
        ('assets/images/lessons/wildlife_stream_harmony.jpg', 'ஆயர்பாடி கிருஷ்ண லீலை & இயற்கை', 'பகவத் கீதை வழியே விளங்கும் உன்னத பக்தி யோக நெறி')
    ],
    'vinayagar.html': [
        ('assets/images/lessons/grade4_appar_service.jpg', 'உழவாரப் பணி & முழுமுதற் கடவுள் வழிபாடு', 'செய்கின்ற செயல்கள் அனைத்தையும் கணபதியின் பாதங்களில் அர்ப்பணிக்கும் பக்தி'),
        ('assets/images/lessons/shiva_tripundram.jpg', 'திருநீற்று நெறி & கணபதி மூல மந்திரம்', 'விநாயகர் அகவலும் தடைகள் தகர்க்கும் முதல்வன் வழிபாடும்')
    ],
    'irai-isai-virundhu.html': [
        ('assets/images/lessons/grade5_sundarar_thiruvarur.jpg', 'சுந்தரமூர்த்தி நாயனார் தேவாரம்', 'திருவாரூர் பெருங்கோயிலில் இசைத்த திருப்பதிகங்களின் இனிமை'),
        ('assets/images/lessons/grade5_manikkavasagar_thiruvasagam.jpg', 'மாணிக்கவாசகர் திருவாசகத் தேன்', 'சொல்லிப் பாடிப் பரவும் 5 சிறப்பு இசைத் தொகுப்புகளின் நாத லயம்')
    ],
    'google-site.html': [
        ('assets/images/lessons/gurukulam_sacred_refuge.jpg', 'குருகுல தேச அதிகாரப்பூர்வ தளம்', 'கூகிள் சைட்ஸ் நேரடி வலைப்பின்னல் மற்றும் ஆசிரம ஆவணங்கள்'),
        ('assets/images/lessons/chola_anicut_engineers.jpg', 'சோழர் அணைக்கட்டு பொறியியல் மாண்பு', 'பண்டைய தமிழ் ஞானமும் நவீன இணையத் தொழில்நுட்பமும் இணைந்த தளம்')
    ],
    'review_quality.html': [
        ('assets/images/lessons/scholar_palm_manuscript.jpg', 'திரைத் தரப் பரிசோதனை & சுவடி ஆய்வு', 'திருக்குறள் மாஸ்டர் சினிமா காட்சிகளின் வரலாற்று நம்பகத்தன்மை மதிப்பீடு')
    ]
}

def build_showcase_html(images):
    cards = []
    for src, title, desc in images:
        cards.append(f"""      <div class="showcase-visual-card">
        <img src="{src}" alt="{title}" class="showcase-visual-img" loading="lazy">
        <div class="showcase-visual-caption">
          <div class="showcase-caption-title">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg>
            <span>{title}</span>
          </div>
          <div class="showcase-caption-desc">{desc}</div>
        </div>
      </div>""")
    cards_str = "\n".join(cards)
    return f"""
    <!-- Sacred Classical Heritage Visual Showcase -->
    <section class="page-visual-showcase-grid" aria-label="புனித மரபுசார் ஓவியக் காட்சி">
{cards_str}
    </section>
"""

def insert_visuals_into_file(filepath):
    filename = os.path.basename(filepath)
    if filename not in PAGE_VISUAL_MAP:
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already inserted
    if 'class="page-visual-showcase-grid"' in content:
        print(f"[SKIP] Visual showcase already in {filename}")
        return False

    images = PAGE_VISUAL_MAP[filename]
    showcase_html = build_showcase_html(images)

    # Strategy: Find end of hero block or main start
    # Try inserting right after hero-banner
    hero_match = re.search(r'(<div class="hero-banner"[^>]*>.*?</div>)', content, re.DOTALL)
    if hero_match:
        pos = hero_match.end()
        new_content = content[:pos] + showcase_html + content[pos:]
    else:
        # Try inserting right after <main...>
        main_match = re.search(r'(<main[^>]*>)', content)
        if main_match:
            pos = main_match.end()
            new_content = content[:pos] + showcase_html + content[pos:]
        else:
            print(f"[WARN] Could not find insertion point in {filename}")
            return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Inserted sacred heritage visuals into {filename}")
    return True

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    docs_dir = os.path.join(repo_root, 'docs')
    count = 0
    for filename in sorted(PAGE_VISUAL_MAP.keys()):
        filepath = os.path.join(docs_dir, filename)
        if os.path.exists(filepath):
            if insert_visuals_into_file(filepath):
                count += 1
    print(f"\nDone! Updated {count} pages with sacred heritage visuals.")

if __name__ == '__main__':
    main()
