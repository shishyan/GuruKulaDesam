#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/upgrade_lifestyle_pages.py
Upgrades siddha.html, sannidhis.html, and grihastha.html to 50/50 visual split layout.
"""

import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

from upgrade_visual_sections import build_split_card, build_split_section, find_tag_block

LIFESTYLE_PAGES_DATA = {
    'siddha.html': {
        'badge': 'சித்த மருத்துவ விஞ்ஞானம் • SIDDHA TRADITION & HOLISTIC WELLNESS',
        'title': 'பதினெண் சித்தர் காயகல்பமும் வாசி யோகத் தவமும்',
        'cards': [
            (
                'assets/images/lessons/siddha_herbal_wisdom.jpg',
                'சித்தர்களின் மூலிகைப் பெருநெறியும் காயகல்ப மருத்துவமும்',
                'காயகல்ப மூலிகைகள் • HERBAL WISDOM',
                '✦ இயற்கை மருத்துவம்',
                'சித்தர்களின் மூலிகைப் பெருநெறியும் காயகல்ப மருத்துவமும்',
                '"உணவே மருந்து, மருந்தே உணவு" — பதினெண் சித்தர்களின் இயற்கை மருத்துவ விஞ்ஞானம்',
                'சித்தர்கள் என்பவர்கள் இயற்கையின் பஞ்சபூத சூட்சுமங்களைக் கட்டுப்படுத்தி, நோயற்ற வாழ்வே குறைவற்ற செல்வம் என்ற ஒப்பற்ற இயற்கை மருத்துவ நெறியை அருளிய மெய்ஞ்ஞானிகள் ஆவர். உடலை அழியாது பாதுகாக்கும் காயகல்ப மூலிகைகளான வல்லாரை, துளசி, தூதுவளை, கீழாநெல்லி, ஆவாரம்பூ, குப்பைமேனி, கரிசலாங்கண்ணி, கற்றாழை ஆகியவற்றின் மருத்துவ ஆற்றலை அன்றாட உணவோடு இணைத்து வாழ வழிகாட்டினர்.',
                [
                    'வாதம், பித்தம், கபம் ஆகிய முப்பிணிகளைச் சமநிலைப்படுத்தும் மூலிகைப் பயன்பாடு.',
                    '"உடம்பார் அழியின் உயிரார் அழிவர்" என்ற திருமூலர் வாக்கை மெய்ப்பிக்கும் வாழ்வியல் நெறி.',
                    'நோயற்ற உடலே ஆன்மீக விடுதலைக்கும் உன்னத தர்ம வாழ்விற்கும் முதல் கருவியாகும்.'
                ],
                False
            ),
            (
                'assets/images/lessons/thavam_tapas_meditation.jpg',
                'சித்தர்களின் வாசி யோகமும் காயகல்பத் தவமும்',
                'வாசி யோகம் • YOGIC PRANAYAMA',
                '✦ தபோவனத் தவம்',
                'சித்தர்களின் வாசி யோகமும் காயகல்பத் தவமும்',
                'மூச்சை அடக்கி மனதை ஒருமுகப்படுத்தி ஆத்ம சக்தியை விழிப்படையச் செய்யும் யோக தவ நெறிமுறை',
                'இடகலை, பிங்கலை, சுழுமுனை ஆகிய மூன்று நாடிகளையும் முறைப்படுத்தி, மூச்சுக் காற்றை வீணாக வெளியே விடாமல் உடலுக்குள்ளேயே சுழலச் செய்யும் பிராணாயாம வாசி யோகத்தை சித்தர்கள் போதித்தனர். முறையான தியானமும் காயகல்ப நெறியும் மனிதனின் ஆயுளை நீட்டித்து, மனதின் அலைபாயும் தன்மையைக் கட்டுப்படுத்தி, பிரம்ம ஞானத்திற்கு வழிவகுக்கின்றன.',
                [
                    'வாசி யோகத்தின் வழி மூளையின் நியூரான்களைப் புத்துணர்ச்சியடையச் செய்து நினைவாற்றல் பெருக்குதல்.',
                    'அஷ்டாங்க யோகத்தின் எட்டுப் படிகளை அன்றாட தியானமாக மேற்கொள்ளும் முறை.',
                    'உடலையும் மனதையும் தூய்மை செய்து சாசுவத ஆன்ம அமைதியை எய்தும் தபோவனப் பயிற்சி.'
                ],
                True
            )
        ]
    },
    'sannidhis.html': {
        'badge': 'திருக்கோயில் கட்டடக் கலை • SACRED TEMPLE ARCHITECTURE',
        'title': 'வேத ஆகம முறைப்படியான எண்கோண சந்நிதி மண்டபமும் திருவுலா வளாகமும்',
        'cards': [
            (
                'assets/images/lessons/temple_architecture.jpg',
                'வேத ஆகம முறைப்படியான எண்கோண சந்நிதி மண்டபமும் திருவுலா வளாகமும்',
                'ஆலயக் கட்டடக்கலை • TEMPLE SCIENCE',
                '✦ வாஸ்து சாஸ்திரம்',
                'வேத ஆகம முறைப்படியான எண்கோண சந்நிதி மண்டபமும் திருவுலா வளாகமும்',
                '8 மகா சந்நிதிகளின் கட்டடக்கலை, வாஸ்து ரகசியம் மற்றும் பிரபஞ்ச ஆற்றல் ஈர்ப்பு',
                'ஆசிரம மகா சந்நிதிகள் என்பவை வேத முறைப்படியான வாஸ்து சாஸ்திரம் மற்றும் ஆகம விதிகளின்படி நிர்மாணிக்கப்பட்ட ஆன்ம விழிப்புக் களங்களாகும். விநாயகர், நடராஜர், முருகன், லலிதா பரமேஸ்வரி, ரங்கநாதர்-கிருஷ்ணர், வள்ளலார், திருவள்ளுவர் மற்றும் மகா பெரியவா ஆகிய 8 சந்நிதிகளும் மனித உடலின் அஷ்ட ஆதார சக்கரங்களோடு தொடர்புபடுத்திப் பிரதிஷ்டை செய்யப்பட்டுள்ளன.',
                [
                    'கருவறை விமாநம் மற்றும் ராஜகோபுரம் வழியே பிரபஞ்ச நேர்மறை அலைகள் ஈர்க்கப்படுதல்.',
                    'உஷத் காலம் முதல் அர்த்தஜாமம் வரையிலான நாற்பொழுது ஆசிரம காலச்சக்கர பூஜை முறைகள்.',
                    'திருக்கோயில் சுற்று வளாகத்தில் பக்தர்கள் பெறும் மன அமைதியும் தியான அதிர்வுகளும்.'
                ],
                False
            ),
            (
                'assets/images/lessons/temple_bell_morning.jpg',
                'விடியற்காலை நாத ஆராதனையும் ஆலய மணியோசையும்',
                'நாத தத்துவம் • TEMPLE BELL RESONANCE',
                '✦ உஷத் கால ஆராதனை',
                'விடியற்காலை நாத ஆராதனையும் ஆலய மணியோசையும்',
                'மணியோசையின் நாத அதிர்வுகளும் திருப்பள்ளியெழுச்சி பக்திப் பிரவாகமும்',
                'விடியற்காலை பிரம்ம முகூர்த்தத்தில் ஆலய மணியோசை ஒலிக்கும் போது உண்டாகும் நாத அதிர்வுகள் மனித மூளையின் இடது-வலது பாகங்களை ஒருங்கிணைத்து ஆழ்ந்த அமைதியைத் தருகின்றன. திருப்பள்ளியெழுச்சி, காயத்ரி ஜபம் மற்றும் திருமுறை ஓதுதல் ஆகியவை அன்றைய நாளைத் தெய்வீக உற்சாகத்தோடு தொடங்க உதவுகின்றன.',
                [
                    'வெண்கல மணியோசையின் அதிர்வலைகள் தீய சக்திகளையும் மனச்சோர்வையும் அகற்றுதல்.',
                    'ஆசிரம நாற்பொழுது வழிபாட்டு நெறியின் படி நேர மேலாண்மையும் ஆத்ம சாதகமும்.',
                    'மாணவர்கள் விடியலில் எழுந்து கல்வி பயிலும் பிரம்ம முகூர்த்த வித்யா காலம்.'
                ],
                True
            )
        ]
    },
    'grihastha.html': {
        'badge': 'இல்லற தர்மம் • GRIHASTHA DHARMA SANCTUARY',
        'title': 'சான்றாண்மை இல்லறக் காட்சியும் பூத யக்ஞ மாண்பும்',
        'cards': [
            (
                'assets/images/lessons/grade12_grihastha_nirvana.jpg',
                'சான்றாண்மை இல்லறக் காட்சியும் மாண்புறு குடும்ப தர்மமும்',
                'இல்லற மாண்பு • NOBLE FAMILY LIVING',
                '✦ குடும்ப சாம்ராஜ்யம்',
                'சான்றாண்மை இல்லறக் காட்சியும் மாண்புறு குடும்ப தர்மமும்',
                'அறநெறி வழியில் இல்லறம் ஆற்றி சான்றோனாய் வாழ்ந்து முக்தி எய்தும் உன்னத வாழ்வியல்',
                '"அறனெனப் பட்டதே இல்வாழ்க்கை அஃதும் பிறன்பழிப்ப தில்லாயின் நன்று" — சனாதன பாரதத்தில் இல்லற தர்மமே மற்ற அனைத்து ஆசிரமங்களுக்கும் உணவும் வாழ்வும் அளிக்கும் தலையாய ஆசிரமமாகும். இல்வாழ்க்கையில் இருந்து கொண்டே தர்மம், பொருள், இன்பம் ஆகிய மூன்றையும் நெறி தவறாது துய்த்துப் பரம முக்தியை அடைய முடியும் என்பதற்கு நம் முன்னோர்கள் சான்றாகத் திகழ்ந்தனர்.',
                [
                    'கணவன்-மனைவி இடையே நிலவும் ஆன்ம ஒருமைப்பாடு மற்றும் பரஸ்பர மரியாதை.',
                    'குழந்தைகளை அறநெறியிலும் தெய்வீகப் பண்புகளிலும் வளர்க்கும் சான்றாண்மை நெறி.',
                    'குடும்பத்தின் மகிழ்ச்சியே நாட்டின் அமைதிக்கும் ஆன்மீக விழிப்புக்கும் மூலாதாரம்.'
                ],
                False
            ),
            (
                'assets/images/lessons/dharma_cow_calf.jpg',
                'பூத யக்ஞம் — கோமாதா வழிபாடு மற்றும் வாயில்லா உயிர்களிடத்தில் அன்பு',
                'பூத யக்ஞம் • UNIVERSAL AHIMSA',
                '✦ கோசம்ரக்ஷணம்',
                'பூத யக்ஞம் — கோமாதா வழிபாடு மற்றும் வாயில்லா உயிர்களிடத்தில் அன்பு',
                '"எல்லா உயிர்களும் இன்புற்று வாழ்க" — இல்லறத்தார் ஆற்ற வேண்டிய நித்திய வேள்வி',
                'இல்லறத்தார் தினசரி ஆற்ற வேண்டிய பஞ்ச மகா யக்ஞங்களில் பூத யக்ஞம் மிக முக்கியமானதாகும். பசுக்கள், கன்றுகள், பறவைகள், தெருவிலங்குகள் மற்றும் மரஞ்செடிகளுக்குத் தினமும் அன்புடன் உணவளித்து ஆதரிக்கும் போது, மனிதனின் சுயநலம் மறைந்து உலகளாவிய கருணை உள்ளம் மலர்கிறது.',
                [
                    'கோபூஜை மற்றும் பசுசம்ரக்ஷணத்தினால் குடும்பத்தில் சகல தோஷங்களும் நீங்கி சுபிக்ஷம் பெருகுதல்.',
                    'வாயில்லா ஜீவராசிகளின் பசியைப் போக்குவதே கடவுளுக்குச் செய்யும் நேரடிப் பூஜை.',
                    'குழந்தைகளின் உள்ளத்தில் சிறுவயதிலேயே உயிரிரக்கப் பண்பை விதைக்கும் குடும்ப ஆசாரம்.'
                ],
                True
            )
        ]
    }
}

def upgrade_lifestyle_page(filename):
    data = LIFESTYLE_PAGES_DATA[filename]
    cards = []
    for c in data['cards']:
        cards.append(build_split_card(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8]))
    section_html = build_split_section(data['badge'], data['title'], cards)
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    updated = False
    
    if filename == 'siddha.html':
        # Remove the two lesson-hero-visual-cards
        # 1. First card
        card1_span = find_tag_block(content, r'<div class="lesson-hero-visual-card"', '<div', '</div>')
        if card1_span:
            # check for comment before card1
            pre1 = re.search(r'<!--\s*Sacred Artwork:[^-]*-->\s*$', content[:card1_span[0]], re.IGNORECASE)
            s1 = pre1.start() if pre1 else card1_span[0]
            content = content[:s1] + section_html.strip() + content[card1_span[1]:]
            
            # 2. Second card later in file
            card2_span = find_tag_block(content, r'<div class="lesson-hero-visual-card"', '<div', '</div>')
            if card2_span:
                pre2 = re.search(r'<!--\s*Sacred Artwork:[^-]*-->\s*$', content[:card2_span[0]], re.IGNORECASE)
                s2 = pre2.start() if pre2 else card2_span[0]
                content = content[:s2] + content[card2_span[1]:]
            updated = True
            print("[siddha.html] Upgraded visual cards to unified 50/50 split section.")

    elif filename == 'sannidhis.html':
        card_span = find_tag_block(content, r'<div class="sannidhi-hero-visual-card"', '<div', '</div>')
        if card_span:
            pre = re.search(r'<!--\s*SACRED TEMPLE ARCHITECTURE VISUAL[^-]*-->\s*$', content[:card_span[0]], re.IGNORECASE)
            s = pre.start() if pre else card_span[0]
            content = content[:s] + section_html.strip() + content[card_span[1]:]
            updated = True
            print("[sannidhis.html] Upgraded visual card to unified 50/50 split section.")

    elif filename == 'grihastha.html':
        card1_span = find_tag_block(content, r'<div class="lesson-hero-visual-card"', '<div', '</div>')
        if card1_span:
            pre1 = re.search(r'<!--\s*Sacred Artwork:[^-]*-->\s*$', content[:card1_span[0]], re.IGNORECASE)
            s1 = pre1.start() if pre1 else card1_span[0]
            content = content[:s1] + section_html.strip() + content[card1_span[1]:]
            
            card2_span = find_tag_block(content, r'<div class="lesson-hero-visual-card"', '<div', '</div>')
            if card2_span:
                pre2 = re.search(r'<!--\s*Sacred Artwork:[^-]*-->\s*$', content[:card2_span[0]], re.IGNORECASE)
                s2 = pre2.start() if pre2 else card2_span[0]
                content = content[:s2] + content[card2_span[1]:]
            updated = True
            print("[grihastha.html] Upgraded visual cards to unified 50/50 split section.")

    if updated:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("=== Upgrading Lifestyle Pages (siddha, sannidhis, grihastha) ===")
    for fn in LIFESTYLE_PAGES_DATA:
        if os.path.exists(fn):
            upgrade_lifestyle_page(fn)

if __name__ == '__main__':
    main()
