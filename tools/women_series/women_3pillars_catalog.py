#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools/women_series/women_3pillars_catalog.py
=========================================================================================
Zero-Video-Credit Long-Form Women's Devotional & Wisdom Pilot Catalog (3 Pillars):
  1. Pillar 1 (108 Amman Sthala Varalaru & Vratham):
     ep01_amman_garbarakshambigai — திருக்கருகாவூர் கர்ப்பரட்சாம்பிகை அம்மன் தல வரலாறு & நெய் தீப வழிபாட்டு மகிமை
  2. Pillar 2 (Anjaraipetti & Patti Vaithiyam):
     ep02_patti_vaithiyam_ulundhukali — மகளிர் எலும்பு & இடுப்பு வலிமைக்கான கருப்பு உளுந்தங்களி, எள்ளுருண்டை & பிரண்டை பாட்டி வைத்தியம்
  3. Pillar 3 (Pooja Room & Deepa Shastram):
     ep03_pooja_deepa_shastram — ஐந்து முக குத்துவிளக்கு, பஞ்ச தீப எண்ணெய் & வெள்ளிக்கிழமை மகாலட்சுமி பூஜை ரகசியங்கள்

All invariants enforced programmatically:
  - Zero Arabic digits (0-9), zero colons (:), zero hyphens/brackets (-, ()) in spoken script
  - Zero clock/bad-time windows (ராகு காலம், எமகண்டம், குளிகை)
  - Zero CTA in spoken script, titles, captions, or descriptions
  - Zero banned gflow prompt tokens ("24K", "16:9", "completely blank")
  - 16 unique photorealistic widescreen nano-pro shots per episode (zero duplicates)
"""

from __future__ import annotations
import re

BANNED_CTA_PATTERNS = [
    r"\bsubscribe\b", r"\blike\b", r"\bcomment\b", r"\bshare\b", r"\bnotification\b", r"\bbell icon\b",
    r"சப்ஸ்கிரைப்", r"(?:^|\s)லைக்(?:\s|$|[,.!?])", r"கமெண்ட்", r"(?:^|\s)ஷேர்(?:\s|$|[,.!?])", r"பெல் பட்டன்", r"மறக்காம",
]
BANNED_TIMING_PATTERNS = [
    r"ராகு\s*காலம்", r"எமகண்டம்", r"குளிகை", r"கௌரி\s*நல்ல\s*நேரம்",
]
BANNED_PROMPT_TOKENS = ["24K", "24k", "16:9", "completely blank", "empty box"]

SCENE_STYLE_PREFIX = (
    "Photorealistic widescreen South Indian sacred cinema & heritage realism, "
    "ARRI Alexa 65mm lens, natural skin and temple stone textures, warm golden sunlight and glowing brass oil lamps, "
    "single unified cohesive camera frame with no split-screen and no collage dividers, "
    "subjects composed cleanly with rich atmospheric depth, "
    "pure artwork with zero text, zero letters, zero numbers, zero watermarks, and zero UI icons. "
)

EPISODES = [
    # =========================================================================
    # EPISODE 1 — PILLAR 1: 108 AMMAN STHALA VARALARU & VRATHAM
    # =========================================================================
    {
        "id": "ep01",
        "slug": "ep01_amman_garbarakshambigai",
        "pillar": "Pillar 1: 108 அம்மன் தல வரலாறு & விரத மகிமை",
        "title_pill": "அம்மன் தல வரலாறு • திருக்கருகாவூர் கர்ப்பரட்சாம்பிகை மகிமை",
        "yt_title": "திருக்கருகாவூர் கர்ப்பரட்சாம்பிகை அம்மன் தல வரலாறு & நெய் தீப வழிபாட்டு முறை | @TamilDailyLife",
        "yt_description": (
            "திருக்கருகாவூர் அருள்மிகு முல்லைவனநாதர் மற்றும் கர்ப்பரட்சாம்பிகை அம்மன் திருக்கோயிலின் "
            "முழுமையான புராணத் தல வரலாறு, வேதிகை அம்மையாரின் கருவைக் காத்த அம்பிகையின் கருணை, "
            "மற்றும் மகளிர் இல்லத்தில் கடைப்பிடிக்கும் புனித பசு நெய் தீப வழிபாட்டு முறை.\n\n"
            "தொகுப்பு:\n"
            "- முல்லைவனச் சோலையும் சுயம்பு முல்லைவனநாதர் திருமேனியும்\n"
            "- நித்ருவ முனிவர் மற்றும் வேதிகை அம்மையாரின் தவ வாழ்வு\n"
            "- கலசத்தில் கருவைக் காத்து அருளிய கர்ப்பரட்சாம்பிகை தாயின் வரலாறு\n"
            "- தங்கப் படியில் பசு நெய் மெழுகி வழிபடும் மரபும் இல்லற வழிபாட்டு முறையும்\n\n"
            "#Garbarakshambigai #Thirukarukavur #AmmanVaralaru #TamilDevotional #GuruKulaDesam #TamilDailyLife"
        ),
        "thumbnail_prompt": (
            "A-grade Tamil devotional theatrical cinema movie-poster artwork, widescreen full-bleed seamless composition "
            "(pure poster artwork with zero UI buttons or play icons). "
            "Right side (right half of the frame): Zoomed-in chest-up commanding divine figure of compassionate South Indian "
            "Goddess Garbarakshambigai Amman inside an ancient Chola granite sanctum, wearing rich crimson-emerald Kanchipuram silk, "
            "blooming mullai jasmine garlands, red kumkum tilak, and solid polished gold temple jewelry, right hand raised in protective "
            "Abhaya Mudra and left hand resting gracefully near a sacred golden Kalasha pot, illuminated by intense warm golden rim-lighting "
            "and glowing brass oil lamps. "
            "Left side (left half of the frame): Monumental, massive TV-readable Tamil cinema poster typography occupying the left half with grand prominence. "
            "Top: Distinct dark midnight-indigo pill badge with glowing gold border displaying அம்மன் வரலாறு (no quotation marks). "
            "Center/Bottom: Huge, gigantic 3D-extruded solid polished gold Tamil cinema lettering திருக்கருகாவூர் அம்மன் (written once cleanly) "
            "across a rich royal crimson-maroon velvet banner with sharp metallic bevels, deep drop-shadows, and specular glints, perfectly legible on mobile screens. "
            "Background: Full-bleed ancient Chola temple corridor bathed in golden morning incense mist and glowing brass lamps, zero dead space, "
            "no text or numbers in the lower-right corner."
        ),
        "sections": [
            {
                "id": "s1_intro",
                "badge": "அம்மன் தல வரலாறு • அறிமுகம்",
                "is_story": False,
                "paragraphs": [
                    "சிவாயநம! அன்பான தாய்மார்களே, சகோதரிகளே! நம் குரு குல தேசம் வழங்கும் மகளிர் சிறப்புத் தல வரலாற்றுத் தொடருக்கு உங்களை இருகரம் கூப்பி வரவேற்கிறோம்.",
                    "ஒரு பெண்ணின் வாழ்க்கையிலேயே மிக உன்னதமான தவம் தாய்மை. ஒரு உயிரைத் தன் கருவறையில் சுமந்து, அந்தப் பிஞ்சுக் குழந்தையை நல்லபடியாக இந்த உலகிற்குக் கொண்டு வர வேண்டும் என்று ஒவ்வொரு தாயும் தினமும் இறைவனிடம் உருகி வேண்டுவாள்.",
                    "அப்படித் தாய்மையைக் காப்பதற்காகவே, உலக அன்னையான பார்வதி தேவி தானே மண்ணில் இறங்கி வந்து, ஒரு தாயின் கருவைப் பொற்கலசத்தில் வைத்துக் காத்தருளிய அற்புதத் திருத்தலம் நம் சோழ வளநாட்டில் தஞ்சாவூருக்கு அருகே அமைந்திருக்கிறது. அதுதான் தேவாரப் பாடல் பெற்ற திருக்கருகாவூர் அருள்மிகு கர்ப்பரட்சாம்பிகை அம்மன் திருக்கோயில்! வாருங்கள், மெய்சிலிர்க்க வைக்கும் அந்தப் புனிதத் தல வரலாற்றை இப்போது பார்ப்போம்."
                ],
            },
            {
                "id": "s2_story1",
                "badge": "புராணத் தல வரலாறு • பாகம் ஒன்று",
                "is_story": True,
                "paragraphs": [
                    "முன்னொரு காலத்தில், காவிரியின் கிளை நதியான வெட்டாற்றங்கரையில் மணம் வீசும் முல்லைக் கொடிகள் அடர்ந்த பசுமையான வனம் ஒன்று இருந்தது. அங்கே கௌதம முனிவர், கார்க்கிய முனிவர் உள்ளிட்ட தவ சீலர்களோடு நித்ருவர் என்ற சிவபக்த முனிவரும், அவரது பதிவிரதை மனைவியான வேதிகை அம்மையாரும் அமைதியாக ஆசிரமம் அமைத்து வாழ்ந்து வந்தார்கள்.",
                    "இல்லற தர்மத்தின் பயனாக வேதிகை அம்மையார் கருவுற்றாள். தன் கணவருக்குப் பணிவிடை செய்வதிலும், முல்லைவனத்து ஈசனுக்கும் அம்பிகைக்கும் தினமும் மலர் பறித்து நெய் தீபம் ஏற்றுவதிலும் அவள் உள்ளம் எப்போதும் தோய்ந்திருந்தது.",
                    "ஒரு நாள் நித்ருவ முனிவர் புனித யாத்திரை நிமித்தமாக வெளியூர் சென்றிருந்த வேளையில், நிறைமாதக் கர்ப்பிணியாக இருந்த வேதிகை அம்மையார் களைப்பினால் ஆசிரமத்திற்கு உள்ளே சற்றுக் கண்ணயர்ந்து படுத்திருந்தாள். அந்த நேரத்தில் ஊர்த்துவபாதர் என்ற முனிவர் ஆசிரம வாசலில் நின்று பிட்சை கேட்டார். கர்ப்பக் களைப்பினால் மயங்கியிருந்த வேதிகையால் உடனே எழுந்து வர முடியவில்லை."
                ],
            },
            {
                "id": "s3_story2",
                "badge": "அம்பிகையின் திருவருள் • பாகம் இரண்டு",
                "is_story": True,
                "paragraphs": [
                    "தன்னை அவமதித்துவிட்டதாகத் தவறாக எண்ணிய அந்த முனிவர் சினம் கொண்டதால், வேதிகை அம்மையாரின் உடலைக் கொடிய நோய் தாக்கி அவளது வயிற்றிலிருந்த சிசு சிதைந்து போகும் பேராபத்து சூழ்ந்தது. செய்வதறியாது தவித்த வேதிகை அம்மையார், கண்ணீர் மல்க முல்லைவனத்து அம்பிகையை நோக்கி, அம்மா ஜகன்மாதா! அறியாமல் நடந்த பிழைக்காக என் வயிற்றில் வளரும் இந்தப் பிஞ்சு உயிரைக் கைவிட்டு விடாதே தாயே என்று கதறி அழுதாள்.",
                    "பக்தையின் அழுகுரல் கேட்ட மாத்திரத்தில், கயிலாயத்திலிருந்து கருணைக் கடலான அம்பிகை ஓடோடி வந்தாள்! கலைந்து போகவிருந்த அந்தச் சிசுவைத் தன் இரு திருக்கரங்களால் ஏந்தி, ஒரு புனித மண் கலசத்திற்குள்ளே வைத்துத் தாயின் கருவறை போலவே வெப்பமும் உயிர்ப்பும் ஊட்டிப் பாதுகாத்தாள்! உரிய காலம் கழிந்ததும் அழகான ஆண் குழந்தையாக வேதிகையின் கரங்களில் ஒப்படைத்தாள்!",
                    "அன்று முதல் அந்தத் தாய்க்குக் கர்ப்பரட்சாம்பிகை, அதாவது கருவைக் காக்கும் அன்னை என்ற திருநாமமும், அந்த ஊருக்குத் திருக்கருகாவூர் என்ற புனிதப் பெயரும் நிலைபெற்றது! வேதிகை அம்மையாரின் வேண்டுகோளின்படி, இனி எந்தப் பெண் என்னை நினைத்து உருகி வேண்டினாலும் அவளது தாய்மையையும் குழந்தையையும் நானே உடனிருந்து காப்பேன் என்று அம்பிகை அங்கே சுயம்பு அருட்கோலத்தில் எழுந்தருளினாள்."
                ],
            },
            {
                "id": "s4_practice",
                "badge": "மகளிர் விரத & நெய் தீப வழிபாடு",
                "is_story": False,
                "paragraphs": [
                    "இந்தத் திருக்கோயிலில் உள்ள முல்லைவனநாதர் சிவலிங்கத் திருமேனி புற்று மண்ணால் ஆன சுயம்பு மூர்த்தி. அதனால்தான் இவருக்கு நீரபிஷேகம் செய்யாமல் புனுகுச் சட்டம் மட்டுமே சாத்தப்படுகிறது; இன்றும் அந்த லிங்கத் திருமேனியில் முல்லைக் கொடிகள் படர்ந்த தழும்புகளைக் கண்கூடாகத் தரிசிக்கலாம்.",
                    "சரி, தாய்மார்களும் சகோதரிகளும் கர்ப்பரட்சாம்பிகை அம்மனை எப்படி வழிபட வேண்டும் என்பதைப் பார்ப்போம். குழந்தை வரம் வேண்டுபவர்கள், அம்மன் சந்நிதியின் தங்கப் படியைத் தூய பசு நெய்யால் மெழுகி, கோலமிட்டு நெய் தீபம் ஏற்றி வழிபடுவது தொன்றுதொட்டு வரும் புனித மரபு. அங்கே மந்திரித்துத் தரப்படும் நெய்யை நாற்பத்தி எட்டு நாட்கள் கணவனும் மனைவியும் இரவு உணவிற்குப் பின் சிறிதளவு உட்கொண்டு வர மழலைச் செல்வம் கைகூடும் என்பது அசைக்க முடியாத நம்பிக்கை.",
                    "கர்ப்பிணிப் பெண்களுக்கு அம்மனின் திருப்பாதத்தில் வைத்துப் பூஜிக்கப்பட்ட சுத்தமான ஆமணக்கு எண்ணெய் பிரசாதமாக வழங்கப்படுகிறது; இது சுகப்பிரசவம் அருளும் அருமருந்தாகப் போற்றப்படுகிறது. நேரில் செல்ல இயலாத சகோதரிகள், செவ்வாய் அல்லது வெள்ளிக்கிழமை மாலையில் உங்கள் வீட்டுப் பூஜை அறையிலேயே ஒரு தூய அகல் விளக்கில் பசு நெய் தீபம் ஏற்றி, திருக்கருகாவூர் கர்ப்பரட்சாம்பிகை தாயே போற்றி என்று பதினோரு முறை மனமுருகி வேண்டிக் கொள்ளலாம்."
                ],
            },
            {
                "id": "s5_closing",
                "badge": "குடும்ப ஆசீர்வாதம் • நிறைவு",
                "is_story": False,
                "paragraphs": [
                    "தஞ்சாவூர் கும்பகோணம் சாலையில் பாபநாசத்திற்குத் தெற்கே அமைந்துள்ள இந்தத் திருக்கருகாவூர் ஆலயத்தை வாழ்வில் ஒருமுறையேனும் குடும்பத்தோடு சென்று தரிசிப்பது மாபெரும் புண்ணியம்.",
                    "அன்னை கர்ப்பரட்சாம்பிகையின் திருவருளால், குழந்தை வரம் வேண்டும் சகோதரிகளின் இல்லங்களில் விரைவில் மழலைச் சிரிப்பு ஒலிக்கவும், கர்ப்பிணித் தாய்மார்கள் அனைவரும் அச்சமின்றி நலமுடன் சுகப்பிரசவம் அடையவும், நம் பிள்ளைகள் நீண்ட ஆயுளோடும் நிறைந்த ஞானத்தோடும் வாழவும் எல்லாம் வல்ல முல்லைவனநாதரையும் கர்ப்பரட்சாம்பிகை தாயையும் மனதாரப் பிரார்த்திக்கிறோம்.",
                    "அடுத்த சிறப்புப் பதிவில் மற்றொரு அற்புத அம்மன் தல வரலாற்றோடு உங்களைச் சந்திக்கிறோம். நல்லதே நினைப்போம், நல்லதே நடக்கும்! சிவாயநம!"
                ],
            },
        ],
        "shot_prompts": [
            # s1_intro (shots 1..3)
            "Towering ancient Chola granite gopuram of Thirukarukavur temple beside lush green paddy fields and Vettaru river at golden sunrise with glowing brass oil lamps.",
            "Serene South Indian Tamil woman in crimson Kanchipuram silk saree lighting a five-wick brass kuthuvilakku oil lamp in a sunlit temple courtyard with mullai jasmine flowers.",
            "Close-up of blooming fragrant white mullai jasmine garlands and a glowing golden Kalasha pot adorned with mango leaves and coconut inside an ancient stone mandapam.",
            # s2_story1 (shots 4..6)
            "Ancient lush green Mullai forest hermitage beside the tranquil Vettaru river in Chola country with deer, blooming white jasmine creepers, and morning mist.",
            "Devout Vedic sage Nidhruva in white cotton veshti and rudraksha beads alongside his pious wife Vedikai offering white mullai flowers before a forest Shiva shrine.",
            "Expectant devout mother Vedikai resting peacefully inside a humble palm-thatched Vedic cottage while an elderly ascetic sage stands outside the wooden doorway in midday sunlight.",
            # s3_story2 (shots 7..10)
            "Tearful devout Tamil woman Vedikai kneeling with folded hands before a glowing forest Amman shrine surrounded by fragrant mullai creepers, praying earnestly.",
            "Radiant divine descent of compassionate Goddess Parvati Garbarakshambigai in crimson-emerald silk surrounded by a warm golden celestial aura inside the forest hermitage.",
            "Sacred miracle scene: Compassionate Goddess Garbarakshambigai gently blessing a luminous sacred earthen-gold Kalasha pot wreathed in warm divine golden light and lotus petals.",
            "Joyful reunion: Sage Nidhruva and grateful mother Vedikai holding their healthy newborn infant wrapped in soft cotton cloth, bowing before radiant Goddess Garbarakshambigai.",
            # s4_practice (shots 11..14)
            "Ancient Chola granite sanctum view of Swayambhu Mullai Vananathar Shiva Lingam adorned with fragrant white mullai flower garlands and golden vilva leaves amidst camphor flame.",
            "Sacred temple ritual close-up: A Tamil woman's graceful hands anointing the golden sanctum threshold step with pure golden cow ghee and lighting clay agal ghee lamps.",
            "Polished brass vessel filled with pure golden cow ghee, fresh red lotus blossoms, turmeric, kumkum, and betel leaves placed reverently on a banana leaf before Amman sanctum.",
            "Graceful Tamil homemaker in traditional silk saree lighting a clay agal ghee lamp in her peaceful home pooja room on Friday evening, praying with calm devotion.",
            # s5_closing (shots 15..16)
            "Happy South Indian family — parents, grandmother, and smiling young child — walking peacefully along the pillared stone prakaram of Thirukarukavur temple at golden twilight.",
            "Grand sanctum camphor deeparadhana harathi before compassionate Goddess Garbarakshambigai Amman resplendent in silk and jasmine garlands, radiating maternal grace.",
        ],
    },

    # =========================================================================
    # EPISODE 2 — PILLAR 2: ANJARAIPETTI & PATTI VAITHIYAM
    # =========================================================================
    {
        "id": "ep02",
        "slug": "ep02_patti_vaithiyam_ulundhukali",
        "pillar": "Pillar 2: அஞ்சறைப்பெட்டி & பாட்டி வைத்தியம்",
        "title_pill": "பாட்டி வைத்தியம் • கருப்பு உளுந்தங்களி, எள்ளுருண்டை & பிரண்டை ரகசியம்",
        "yt_title": "மகளிர் இடுப்பு & எலும்பு வலிமைக்கான கருப்பு உளுந்தங்களி, எள்ளுருண்டை & பிரண்டை பாட்டி வைத்தியம்",
        "yt_description": (
            "தமிழ் மூதாட்டிகள் தலைமுறை தலைமுறையாகப் பெண்களின் இடுப்பு எலும்பு, மூட்டு மற்றும் இரத்த வலிமைக்காகக் "
            "கற்றுக் கொடுத்த மூன்று தங்க உணவுகள்: தோல் நீக்காத கருப்பு உளுந்தங்களி, கருப்பு எள்ளுருண்டை மற்றும் "
            "இளம் பிரண்டை நெய் துவையல் செய்முறை மற்றும் உணவியல் நுணுக்கங்கள்.\n\n"
            "தொகுப்பு:\n"
            "- பெண்களின் இடுப்பு எலும்பைக் காக்கும் தோல் நீக்காத கருப்பு உளுந்தங்களி செய்முறை\n"
            "- இரும்புச்சத்தும் சுண்ணாம்புச்சத்தும் நிறைந்த கல் உரல் கருப்பு எள்ளுருண்டை\n"
            "- வஜ்ரவல்லி எனப்படும் இளம் பிரண்டை நெய் துவையலும் எடுத்துக்கொள்ளும் முறையும்\n\n"
            "#PattiVaithiyam #Ulundhukali #TamilTraditionalFood #WomenHealthTamil #GuruKulaDesam #TamilDailyLife"
        ),
        "thumbnail_prompt": (
            "A-grade Tamil traditional wellness cinema movie-poster artwork, widescreen full-bleed seamless composition "
            "(pure poster artwork with zero UI buttons or play icons). "
            "Right side (right half of the frame): Zoomed-in chest-up warm, dignified South Indian Tamil grandmother wearing a "
            "traditional mustard-maroon cotton saree, silver hair in a neat bun, vibhuti and small kumkum bindi, smiling lovingly "
            "while presenting a steaming traditional clay pot of glossy dark-brown Karuppu Ulundhukali drizzled with golden gingelly oil "
            "beside black sesame balls and fresh green pirandai herbs, illuminated by warm golden kitchen oil-lamp rim-lighting. "
            "Left side (left half of the frame): Monumental, massive TV-readable Tamil cinema poster typography occupying the left half with grand prominence. "
            "Top: Distinct dark midnight-indigo pill badge with glowing gold border displaying பாட்டி வைத்தியம் (no quotation marks). "
            "Center/Bottom: Huge, gigantic 3D-extruded solid polished gold Tamil cinema lettering உளுந்தங்களி ரகசியம் (written once cleanly) "
            "across a rich royal crimson-maroon velvet banner with sharp metallic bevels, deep drop-shadows, and specular glints, perfectly legible on mobile screens. "
            "Background: Full-bleed traditional Tamil heritage kitchen with brass anjaraipetti spice box and warm morning sunbeams, zero dead space, "
            "no text or numbers in the lower-right corner."
        ),
        "sections": [
            {
                "id": "s1_intro",
                "badge": "பாட்டி வைத்தியம் • மகளிர் நலம்",
                "is_story": False,
                "paragraphs": [
                    "சிவாயநம! அன்பான சகோதரிகளே, தாய்மார்களே! நம் இல்லத்தின் ஆணிவேராக நின்று குடும்பம் முழுவதையும் தாங்கிப் பிடிப்பது ஒரு பெண்ணின் உடல் நலமும் மன வலிமையும்தான்.",
                    "காலை எழுந்தது முதல் இரவு உறங்கும் வரை ஓயாமல் உழைக்கும் பல சகோதரிகளுக்கு, முப்பது வயதைக் கடந்த உடனேயே இடுப்பு வலி, முதுகுத் தண்டு சோர்வு, மூட்டு வலி மற்றும் இரத்தச் சோகை ஆகியவை மெல்ல எட்டிப் பார்க்கத் தொடங்குகின்றன. ஆனால் நம் பாட்டிமார்கள் எண்பது வயதிலும் குனிந்து நிமிர்ந்து சுறுசுறுப்பாக வேலை செய்தார்களே, அதன் ரகசியம் என்ன?",
                    "மருந்தையே உணவாகச் சமைத்துக் கொடுத்த நம் தமிழ் மூதாட்டிகளின் அஞ்சறைப்பெட்டி அறிவியல்தான் அந்த ரகசியம்! பெண்களின் எலும்பு, இடுப்பு மற்றும் இரத்த வலிமைக்கு நம் முன்னோர்கள் வகுத்துக் கொடுத்த மூன்று நிகரற்ற பாரம்பரிய உணவுகளைச் சரியான செய்முறையோடு இப்போது விரிவாகப் பார்ப்போம்."
                ],
            },
            {
                "id": "s2_remedy1",
                "badge": "முதல் அருமருந்து • கருப்பு உளுந்தங்களி",
                "is_story": True,
                "paragraphs": [
                    "முதலாவது தங்க உணவு, தோல் நீக்காத கருப்பு உளுந்தங்களி! பெண்களின் இடுப்பு எலும்பிற்கு உளுந்தை விடச் சிறந்த தோழன் வேறு எதுவுமே இல்லை என்று சித்த மருத்துவம் போற்றுகிறது. வெள்ளை உளுந்தை விட, மேல் தோலோடு இருக்கும் கருப்பு உளுந்தில்தான் நார்ச்சத்தும், சுண்ணாம்புச்சத்தும், இரும்புச்சத்தும் முழுமையாக நிறைந்திருக்கின்றன.",
                    "இதைச் செய்யும் பாரம்பரிய முறை மிகவும் எளிமையானது. ஒரு பங்கு தோல் நீக்காத கருப்பு உளுந்தோடு, கால் பங்கு பச்சரிசி சேர்த்து வெறும் வாணலியில் மிதமான தீயில் நல்ல மணம் வரும் வரை வறுத்து, ஆறிய பின் நைசான மாவாக அரைத்து வைத்துக் கொள்ளுங்கள். அடிகனமான பாத்திரத்தில் சுத்தமான பனை கருப்பட்டியைத் தண்ணீரில் கரைத்து வடிகட்டி கொதிக்க விட வேண்டும்.",
                    "கருப்பட்டி நீர் கொதிக்கும்போது உளுத்த மாவைச் சிறிது சிறிதாகத் தூவிக் கட்டியில்லாமல் கிளறி, அதனுடன் செக்கில் ஆட்டிய சுத்தமான நல்லெண்ணெயை தாராளமாக ஊற்றி அல்வா பதத்திற்குச் சுருளக் கிளறி இறக்கினால் மணமணக்கும் கருப்பு உளுந்தங்களி தயார்! பூப்படைந்த இளம் பெண்கள் முதல் தாய்மார்கள் வரை வாரம் ஒருமுறை காலை வேளையில் இதைச் சூடாக உண்டு வர, இடுப்பு எலும்புகளும் கருப்பையும் இரும்பு போல வலுப்பெறும்."
                ],
            },
            {
                "id": "s3_remedy2",
                "badge": "இரண்டாம் அருமருந்து • கருப்பு எள்ளுருண்டை",
                "is_story": True,
                "paragraphs": [
                    "இரண்டாவது அற்புத உணவு, கல் உரலில் இடித்த கருப்பு எள்ளுருண்டை! பெண்களுக்கு ஏற்படும் முடி உதிர்தல், உடல் வறட்சி, மாதாந்திரச் சோர்வு மற்றும் இரத்தச் சோகைக்குக் கருப்பு எள் ஒரு வரப்பிரசாதம். பாலில் இருப்பதை விடப் பல மடங்கு சுண்ணாம்புச்சத்தும் தாமிரம், துத்தநாகம் போன்ற நுண்ணூட்டங்களும் இந்தச் சிறிய கருப்பு எள்ளில் பொதிந்துள்ளன.",
                    "சுத்தமான கருப்பு எள்ளை கல் மண் நீக்கிக் கழுவி வெயிலில் உலர்த்தி, இரும்பு வாணலியில் படபடவெனப் பொரியும் வரை மிதமான தீயில் வறுத்துக் கொள்ள வேண்டும். அதனுடன் சரிபாதி அளவு துருவிய பனை வெல்லம் அல்லது நாட்டு வெல்லம், வாசனைக்கு இரண்டு ஏலக்காய் சேர்த்து உரலில் இடித்துச் சிறிய உருண்டைகளாகப் பிடித்து வைத்துக் கொள்ளலாம்.",
                    "தினமும் காலை உணவிற்குப் பிறகு ஒரே ஒரு சிறிய எள்ளுருண்டையை நன்றாக மென்று சாப்பிட்டு வர, பெண்களின் இரத்த அணுக்கள் சீராக உயரும்; எலும்புத் தேய்மானம் தடுக்கப்பட்டு முகத்தில் இயற்கையான பொலிவு கூடும். கர்ப்பிணித் தாய்மார்கள் மட்டும் எள் சூடு என்பதால் மருத்துவர் ஆலோசனைப்படி தவிர்ப்பது நல்லது."
                ],
            },
            {
                "id": "s4_remedy3",
                "badge": "மூன்றாம் அருமருந்து • இளம் பிரண்டை துவையல்",
                "is_story": False,
                "paragraphs": [
                    "மூன்றாவது மூலிகைப் பொக்கிஷம், வஜ்ரவல்லி என்று சித்தர்களால் அழைக்கப்படும் இளம் பிரண்டை நெய் துவையல்! வஜ்ரம் என்றால் வைரம் போல எலும்புகளை உறுதியாக்குவது என்று பொருள். நாம் உண்ணும் உணவில் உள்ள சுண்ணாம்புச்சத்தை எலும்புகள் முழுமையாக உறிஞ்சிக் கொள்ளப் பிரண்டையும், செரிமான அக்னியைத் தூண்ட மிளகும் சீரகமும் பெரிதும் உதவுகின்றன.",
                    "செய்முறையைக் கவனியுங்கள். விரலால் ஒடித்தால் எளிதில் உடையும் இளம் நுனிப் பிரண்டையைத் தேர்ந்தெடுத்து, அதன் கணுக்களையும் நாரையும் சுத்தமாக நீக்கி, கைகளில் சிறிது நல்லெண்ணெய் தடவிக் கொண்டு நறுக்க வேண்டும். வாணலியில் தூய பசு நெய் அல்லது நல்லெண்ணெய் விட்டுப் பிரண்டைத் துண்டுகள் நிறம் மாறும் வரை நன்றாக வதக்குவது மிக மிக முக்கியம்; நன்றாக வதங்கினால்தான் நாக்கில் அரிப்பு ஏற்படாது.",
                    "அதோடு சிறிது உளுத்தம்பருப்பு, காய்ந்த மிளகாய், பத்து மிளகு, நான்கு பல் பூண்டு, சிறிது புளி மற்றும் கல் உப்பு சேர்த்து வதக்கி அம்மியில் அரைத்தால் சுவையான பிரண்டை துவையல் தயார்! மாதம் இருமுறை மதிய உணவில் சூடான சாதத்தில் ஒரு தேக்கரண்டி பசு நெய் விட்டு இந்தத் துவையலைப் பிசைந்து சாப்பிட்டு வர, மூட்டு வலியும் வாயுத் தொல்லையும் பறந்தோடும்."
                ],
            },
            {
                "id": "s5_closing",
                "badge": "ஆரோக்கிய வாழ்வியல் • நிறைவு",
                "is_story": False,
                "paragraphs": [
                    "அன்பான சகோதரிகளே, விலை உயர்ந்த செயற்கை பானங்களைத் தேடி ஓடாமல், நம் சமையலறையிலேயே இருக்கும் கருப்பு உளுந்து, கருப்பு எள், பனை கருப்பட்டி, நல்லெண்ணெய் மற்றும் இளம் பிரண்டையை நம் வாராந்திர உணவுப் பட்டியலில் இணைத்துக் கொள்வோம்.",
                    "ஒரு தாய் ஆரோக்கியமாக இருந்தால் அந்த இல்லமே ஆனந்தமாகப் பூத்துக் குலுங்கும்! நம் பெண் குழந்தைகளுக்கும் இந்தப் பாரம்பரியச் சுவையைச் சிறுவயது முதலே பழக்கப்படுத்துவோம். நீங்கள் அனைவரும் நோயற்ற வாழ்வும் குறைவற்ற செல்வமும் பெற்று நீடூழி வாழ இறைவனைப் பிரார்த்திக்கிறோம்.",
                    "அடுத்த பதிவில் மற்றுமொரு பயனுள்ள பாட்டி வைத்தியக் குறிப்போடு உங்களைச் சந்திக்கிறோம். நல்லதே நினைப்போம், நல்லதே நடக்கும்! சிவாயநம!"
                ],
            },
        ],
        "shot_prompts": [
            # s1_intro (shots 1..3)
            "Sunlit traditional South Indian Tamil courtyard home at dawn where a healthy smiling grandmother and young woman prepare traditional ingredients beside a brass kuthuvilakku lamp.",
            "Macro heritage view of an ornate antique brass Tamil anjaraipetti seven-cup spice box filled with black pepper, cumin, fenugreek, turmeric root, mustard, and dry red chilies on dark teakwood.",
            "Traditional Tamil rustic kitchen table displaying whole black urad dal in a bamboo winnow, palm jaggery karupatti blocks, black sesame seeds, cold-pressed gingelly oil in brass jug, and fresh green pirandai.",
            # s2_remedy1 (shots 4..7)
            "Close-up of whole unhusked black urad dal with white inner grain visible alongside raw rice resting in a traditional woven palm-leaf basket bathed in warm golden morning light.",
            "Traditional iron kadai over a gentle wood-fire stove dry-roasting whole black urad dal as aromatic steam rises in a clean South Indian heritage kitchen.",
            "Dark iron-rich palm jaggery karupatti dissolving into a glossy amber syrup bubbling gently inside a heavy bronze uruli vessel.",
            "Glossy, rich dark-brown traditional Tamil Karuppu Ulundhukali served warm in an earthen clay bowl topped with a shimmering spoonful of golden cold-pressed gingelly oil on a green banana leaf.",
            # s3_remedy2 (shots 8..10)
            "Macro close-up of shiny nutrient-rich black sesame seeds and grated golden palm jaggery with green cardamom pods arranged in polished brass bowls.",
            "Traditional South Indian granite stone mortar and wooden pestle pounding roasted black sesame seeds and golden jaggery together in warm kitchen sunlight.",
            "Neatly hand-rolled glossy Tamil Karuppu Ellurundai black sesame jaggery balls arranged on a fresh green banana leaf beside a brass tumbler of warm water.",
            # s4_remedy3 (shots 11..14)
            "Fresh tender green four-angled Pirandai adamant creeper stems growing lushly on a sunlit South Indian garden trellis with morning dewdrops.",
            "Clean hands oiled with golden gingelly oil neatly trimming the nodes and fibers from tender green pirandai segments on a wooden cutting board.",
            "Tender green pirandai pieces sautéing in pure golden cow ghee with garlic cloves, whole black peppercorns, urad dal, and red chilies inside a cast-iron skillet.",
            "Freshly stone-ground vibrant green Pirandai Thuvaiyal chutney served beside steaming white rice and a drizzle of golden cow ghee on a traditional banana leaf.",
            # s5_closing (shots 15..16)
            "Three generations of joyful South Indian women — grandmother, mother, and teenage daughter — sharing a wholesome traditional banana-leaf meal together in a warm sunlit home.",
            "Serene closing still-life of a glowing clay oil lamp beside the brass anjaraipetti spice box, ulundhukali bowl, ellurundai, and fresh herbs in golden evening light.",
        ],
    },

    # =========================================================================
    # EPISODE 3 — PILLAR 3: POOJA ROOM & DEEPA SHASTRAM
    # =========================================================================
    {
        "id": "ep03",
        "slug": "ep03_pooja_deepa_shastram",
        "pillar": "Pillar 3: பூஜை அறை & தீப சாஸ்திர ரகசியங்கள்",
        "title_pill": "தீப சாஸ்திரம் • குத்துவிளக்கு & வெள்ளிக்கிழமை மகாலட்சுமி பூஜை",
        "yt_title": "ஐந்து முக குத்துவிளக்கு, பஞ்ச தீப எண்ணெய் & வெள்ளிக்கிழமை மகாலட்சுமி பூஜை ரகசியங்கள் | Deepa Shastram",
        "yt_description": (
            "இல்லத்தில் ஐஸ்வர்யமும் மன அமைதியும் நிலைத்திருக்கப் பூஜை அறையில் கடைப்பிடிக்க வேண்டிய "
            "தீப சாஸ்திர விதிகள், ஐந்து முக குத்துவிளக்கின் ஆன்மீகத் தத்துவம், பஞ்ச தீப எண்ணெய் மற்றும் "
            "திரி வகைகள், தீபம் குளிரவைக்கும் முறை மற்றும் வெள்ளிக்கிழமை மகாலட்சுமி வழிபாட்டு ரகசியங்கள்.\n\n"
            "தொகுப்பு:\n"
            "- குத்துவிளக்கின் ஐந்து பாகங்களில் உறையும் தெய்வங்களும் ஐந்து முகத் தத்துவமும்\n"
            "- பஞ்ச தீப எண்ணெய் கலவையும் தவிர்க்க வேண்டிய எண்ணெய்களும்\n"
            "- தாமரைத் தண்டு, வாழைத் தண்டு, பஞ்சுத் திரி மற்றும் திசை சாஸ்திரம்\n"
            "- வெள்ளிக்கிழமை கல் உப்பு, மஞ்சள் மற்றும் தாமரை மலர் மகாலட்சுமி பூஜை முறை\n\n"
            "#DeepaShastram #MahalakshmiPoojai #Kuthuvilakku #PoojaRoomTipsTamil #GuruKulaDesam #TamilDailyLife"
        ),
        "thumbnail_prompt": (
            "A-grade Tamil devotional theatrical cinema movie-poster artwork, widescreen full-bleed seamless composition "
            "(pure poster artwork with zero UI buttons or play icons). "
            "Right side (right half of the frame): Zoomed-in chest-up radiant divine figure of South Indian Goddess Mahalakshmi "
            "seated gracefully upon a blooming pink lotus, wearing crimson-gold Kanchipuram silk saree and solid polished gold temple ornaments, "
            "blessing a brilliantly glowing five-faced brass Kuthuvilakku oil lamp surrounded by pink lotuses, turmeric, kumkum, and rock salt in a brass bowl, "
            "illuminated by intense warm golden rim-lighting. "
            "Left side (left half of the frame): Monumental, massive TV-readable Tamil cinema poster typography occupying the left half with grand prominence. "
            "Top: Distinct dark midnight-indigo pill badge with glowing gold border displaying தீப சாஸ்திரம் (no quotation marks). "
            "Center/Bottom: Huge, gigantic 3D-extruded solid polished gold Tamil cinema lettering குத்துவிளக்கு ரகசியம் (written once cleanly) "
            "across a rich royal crimson-maroon velvet banner with sharp metallic bevels, deep drop-shadows, and specular glints, perfectly legible on mobile screens. "
            "Background: Full-bleed sacred carved wooden home pooja mandapam glowing with golden oil lamps and gentle incense, zero dead space, "
            "no text or numbers in the lower-right corner."
        ),
        "sections": [
            {
                "id": "s1_intro",
                "badge": "தீப சாஸ்திரம் • மங்கல இல்லறம்",
                "is_story": False,
                "paragraphs": [
                    "சிவாயநம! அன்பான சகோதரிகளே, தாய்மார்களே! ஒரு வீட்டின் தலைவாசலைத் தாண்டி உள்ளே அடியெடுத்து வைத்தவுடனேயே, அந்த இல்லத்தில் நிலவும் தெய்வீக அதிர்வையும் அமைதியையும் தீர்மானிப்பது நம் பூஜை அறையில் சுடர்விட்டு எரியும் மங்கல தீபம்தான்!",
                    "இருள் விலகினால் ஒளி பிறக்கும்; இல்லத்தில் ஒளி பிறந்தால் அங்கே திருமகளான மகாலட்சுமி நிரந்தரமாக வாசம் செய்வாள் என்பது நம் ஆன்றோர்களின் வாக்கு. ஆனால் தினமும் நாம் ஏற்றும் குத்துவிளக்கில் எத்தனை முகம் ஏற்ற வேண்டும், எந்த எண்ணெய் ஊற்ற வேண்டும், எந்தத் திசை நோக்கித் திரி போட வேண்டும் என்பதில் பல சகோதரிகளுக்குச் சிறு சந்தேகங்கள் உண்டு.",
                    "நம் ஆகமங்களும் முன்னோர்களும் வகுத்துத் தந்த தூய தீப சாஸ்திர நுணுக்கங்களையும், வெள்ளிக்கிழமை மகாலட்சுமி வழிபாட்டு முறையையும் இப்போது தெளிவாகப் பார்ப்போம்."
                ],
            },
            {
                "id": "s2_kuthuvilakku",
                "badge": "ஐந்து முக குத்துவிளக்குத் தத்துவம்",
                "is_story": True,
                "paragraphs": [
                    "முதலில், நம் பாரம்பரியக் குத்துவிளக்கின் தெய்வீக வடிவமைப்பை அறிந்து கொள்வோம். குத்துவிளக்கின் தாமரை போன்ற அடிப்பாகம் படைக்கும் கடவுளான பிரம்ம தேவனைக் குறிக்கிறது. நடுவே நிமிர்ந்து நிற்கும் நீண்ட தண்டுப் பாகம் காக்கும் கடவுளான மகாவிஷ்ணுவையும், எண்ணெய் தாங்கி நிற்கும் அகன்ற கிண்ணப் பாகம் ருத்ர பரமேஸ்வரனையும் குறிக்கின்றன.",
                    "அந்தக் கிண்ணத்தின் ஐந்து முகங்களும் மகேஸ்வர தத்துவத்தையும், சுடர்விட்டு எரியும் ஜோதியானது சதாசிவத்தையும், அந்த ஒளியின் வெப்பம் பராசக்தியையும் உணர்த்துகின்றன! அதுமட்டுமல்ல, ஒரு இல்லத்தரசியின் ஐந்து உயர்ந்த குணங்களான அன்பு, நுண்ணறிவு, மன உறுதி, நிதானம் மற்றும் பொறுமை ஆகிய ஐந்தையும் குத்துவிளக்கின் ஐந்து முகங்கள் பிரதிபலிக்கின்றன.",
                    "தினமும் ஒரு முகம் ஏற்றினால் மத்திம பலனும், இரு முகம் ஏற்றினால் கணவன் மனைவி ஒற்றுமையும், மூன்று முகம் ஏற்றினால் புத்திர சுகமும், நான்கு முகம் ஏற்றினால் பசு மற்றும் பூமி வளமும், வெள்ளிக்கிழமைகளில் ஐந்து முகங்களும் சேர்த்து ஏற்றினால் சகல ஐஸ்வர்யங்களும் இல்லத்தில் பெருக்கெடுக்கும் என்பது தீப சாஸ்திர மரபு!"
                ],
            },
            {
                "id": "s3_oil_wick",
                "badge": "பஞ்ச தீப எண்ணெய் & திரி ரகசியம்",
                "is_story": True,
                "paragraphs": [
                    "அடுத்ததாக, தீபத்திற்கு ஊற்றும் எண்ணெயும் திரியும் மிக மிக முக்கியம். எப்போதும் கடலை எண்ணெய், சூரியகாந்தி எண்ணெய் அல்லது கலப்பட எண்ணெய்களைத் தீபத்திற்குப் பயன்படுத்தவே கூடாது. தூய பசு நெய் மகாலட்சுமியின் அருளையும் செல்வ வளத்தையும் தரும்; சுத்தமான நல்லெண்ணெய் சகல தோஷங்களையும் நீக்கி ஆரோக்கியம் தரும்.",
                    "பசு நெய், நல்லெண்ணெய், இலுப்பை எண்ணெய், ஆமணக்கு எண்ணெய், தேங்காய் எண்ணெய் ஆகிய ஐந்தும் கலந்த பஞ்ச தீப எண்ணெயைக் கொண்டு வெள்ளிக்கிழமை தீபம் ஏற்றுவது அற்புதமான நேர்மறை அதிர்வுகளை வீடு முழுவதும் பரப்பும். அதேபோல் பஞ்சுத் திரி குடும்ப நலனையும், தாமரைத் தண்டுத் திரி முன்வினை மற்றும் கடன் தீர்வையும், வாழைத் தண்டுத் திரி குழந்தை பாக்கியத்தையும், மஞ்சள் நீரில் நனைத்து உலர்த்திய புதுத் துணித் திரி அம்பிகையின் பரிபூரண அருளையும் பெற்றுத் தரும்.",
                    "திசை சாஸ்திரப்படி, கிழக்குத் திசை நோக்கித் தீபம் ஏற்றினால் துன்பங்கள் விலகி மன அமைதி கிட்டும்; வடக்குத் திசை நோக்கித் தீபம் ஏற்றினால் கல்வி வளமும் குபேர சம்பத்தும் பெருகும்; மேற்குத் திசை கடன் மற்றும் சனி தோஷம் நீங்க உதவும். ஆனால் எக்காரணம் கொண்டும் தெற்குத் திசை நோக்கி வீட்டுப் பூஜை அறையில் தீபம் ஏற்றக் கூடாது."
                ],
            },
            {
                "id": "s4_friday_pooja",
                "badge": "வெள்ளிக்கிழமை திருமகள் பூஜை முறை",
                "is_story": False,
                "paragraphs": [
                    "இனி, வெள்ளிக்கிழமை மாலை அல்லது அதிகாலையில் சகோதரிகள் செய்ய வேண்டிய எளிய மகாலட்சுமி பூஜை முறையைப் பார்ப்போம். வியாழக்கிழமை மாலையே விளக்குகளைப் புளி மற்றும் சபீனா இன்றி எலுமிச்சை மற்றும் மஞ்சள் கொண்டு பளபளப்பாகத் துலக்கி, சந்தனம் குங்குமம் இட்டுத் தயாராக வைத்துக் கொள்ள வேண்டும்; வெள்ளிக்கிழமை அன்று விளக்கைத் தேய்த்துக் கழுவக் கூடாது என்பது முக்கிய மரபு.",
                    "வெள்ளிக்கிழமை பிரம்ம முகூர்த்தம் அல்லது மாலை சந்தியா வேளையில், நிலைவாசற்படியில் மஞ்சள் பூசிக் குங்குமப் பொட்டு வைத்து மாக்கோலம் இட்டு இருபுறமும் அகல் விளக்கு ஏற்றுங்கள். பூஜை அறையில் ஒரு சிறிய மண் அல்லது பீங்கான் கிண்ணத்தில் சுத்தமான கல் உப்பு நிரப்பி, அதன் மேல் மஞ்சள் குங்குமம் மற்றும் ஒரு ஏலக்காய் வைத்து, தாமரை அல்லது மல்லிகை மலர்களால் திருமகளை அர்ச்சித்து, பால் பாயசம் அல்லது கல்கண்டு நைவேத்தியம் படைத்து வழிபடுங்கள்.",
                    "மிக முக்கியமான சாஸ்திர விதி, பூஜை முடிந்த பிறகு விளக்கை ஒருபோதும் வாயால் ஊதியோ கையால் வீசியோ அணைக்கக் கூடாது! விளக்கு குளிரவைக்கிறோம் என்று சொல்லி, ஒரு பூவின் காம்பினால் திரியை மெல்ல எண்ணெய்க்குள் இழுத்துச் சாந்தப்படுத்த வேண்டும்."
                ],
            },
            {
                "id": "s5_closing",
                "badge": "மங்கல ஆசீர்வாதம் • நிறைவு",
                "is_story": False,
                "paragraphs": [
                    "அன்பான சகோதரிகளே, தூய்மையான உள்ளத்தோடும், சாஸ்திர மரபு மாறாத பக்தியோடும் ஒரு தாய் ஏற்றி வைக்கும் ஒற்றை நெய் தீபம், அந்தக் குடும்பத்தின் ஏழு தலைமுறைக்கும் ஒளி வழிகாட்டும் வல்லமை கொண்டது!",
                    "வரும் வெள்ளிக்கிழமை முதல் இந்த எளிய தீப சாஸ்திர முறைகளை உங்கள் இல்லத்தில் மகிழ்ச்சியோடு கடைப்பிடித்துப் பாருங்கள். அன்னை மகாலட்சுமியின் பரிபூரண கடாட்சத்தால் உங்கள் இல்லத்தில் அஷ்ட ஐஸ்வர்யங்களும், மன நிம்மதியும், மங்கல ஓசையும் என்றென்றும் நிறைந்திருக்க மனதாரப் பிரார்த்திக்கிறோம்.",
                    "மற்றொரு புனிதமான பூஜை அறை வழிகாட்டியோடு அடுத்த பதிவில் உங்களைச் சந்திக்கிறோம். நல்லதே நினைப்போம், நல்லதே நடக்கும்! சிவாயநம!"
                ],
            },
        ],
        "shot_prompts": [
            # s1_intro (shots 1..3)
            "Traditional carved Rosewood South Indian home pooja room glowing warmly with two brass kuthuvilakku oil lamps, fragrant jasmine garlands, and morning sunbeams.",
            "Graceful South Indian Tamil woman in emerald-gold silk saree drawing a white rice-flour lotus kolam at a turmeric-anointed wooden home threshold with two lit clay agal lamps.",
            "Radiant close-up of a polished brass five-faced Kuthuvilakku oil lamp with five golden flames shimmering cleanly against a serene temple shrine backdrop.",
            # s2_kuthuvilakku (shots 4..6)
            "Detailed artistic close-up of a tall traditional South Indian brass Kuthuvilakku standing on a lotus base with Annapakshi swan finial, adorned with sandalwood paste, kumkum, and jasmine garland.",
            "Top-angle warm cinematic shot of all five spouts of a brass Kuthuvilakku burning with steady golden flames illuminating fresh red lotus petals below.",
            "Devout Tamil husband, wife, and young daughter bowing together with serene smiles before the glowing five-wick brass Kuthuvilakku in their peaceful home pooja room.",
            # s3_oil_wick (shots 7..10)
            "Five small polished brass bowls arranged neatly on a wooden tray holding golden cow ghee, sesame oil, iluppai oil, castor oil, and pure coconut oil surrounded by fresh flowers.",
            "Macro heritage arrangement of sacred lamp wicks on a brass plate: pure white hand-rolled cotton wicks, natural dried lotus-stem fibers, banana-stem fibers, and yellow turmeric-dyed cotton wicks.",
            "Golden stream of pure cow ghee being poured gently from a small brass spoon into a clean terracotta clay agal lamp resting on a lotus kolam.",
            "Compassionate close-up of a single golden lamp flame burning steadily facing the rising morning sun through an east-facing carved wooden window.",
            # s4_friday_pooja (shots 11..14)
            "Traditional Thursday evening lamp preparation: Polished gleaming brass kuthuvilakku beside fresh yellow lemon halves, turmeric powder, sandalwood paste, and kumkum on a clean cloth.",
            "Auspicious Friday Mahalakshmi offering: An earthen bowl brimming with pure white crystal rock salt topped with turmeric, red kumkum, and green cardamom pods beside pink lotus blossoms.",
            "Sanctum-style home altar of Goddess Mahalakshmi adorned with fresh pink lotus flowers, gold coins, steaming milk payasam in a silver cup, and rock-sugar kalkandu.",
            "Sacred lamp-cooling etiquette close-up: A woman's gentle fingers using a jasmine flower stem to softly draw back a cotton wick inside the brass lamp oil bowl with reverence.",
            # s5_closing (shots 15..16)
            "Radiant divine vision of Goddess Mahalakshmi seated on a blooming pink lotus showering golden grace over a serene lamp-lit Tamil family home.",
            "Peaceful twilight panorama of a South Indian home veranda and pooja room glowing with rows of warm brass and clay oil lamps, radiating prosperity and calm.",
        ],
    },
]


def validate_catalog() -> None:
    for ep in EPISODES:
        # Check shot count & uniqueness
        shots = ep["shot_prompts"]
        assert len(shots) == 16, f"{ep['id']}: expected 16 shots, got {len(shots)}"
        assert len(set(shots)) == 16, f"{ep['id']}: duplicate shot prompts!"

        # Check prompt token bans
        for p in shots + [ep["thumbnail_prompt"]]:
            for tok in BANNED_PROMPT_TOKENS:
                assert tok not in p, f"{ep['id']}: banned prompt token '{tok}' found in prompt: {p[:120]}"

        # Check CTA bans in title & description
        for field_name in ("yt_title", "yt_description", "title_pill"):
            val = ep[field_name]
            for pat in BANNED_CTA_PATTERNS:
                assert not re.search(pat, val, re.IGNORECASE), f"{ep['id']}.{field_name} matched CTA pattern {pat}"

        # Check spoken script hygiene
        for sec in ep["sections"]:
            for p_idx, para in enumerate(sec["paragraphs"]):
                assert not re.search(r"[0-9]", para), f"{ep['id']}.{sec['id']}[{p_idx}] contains digits: {para}"
                assert ":" not in para, f"{ep['id']}.{sec['id']}[{p_idx}] contains colon: {para}"
                assert "-" not in para and "(" not in para and ")" not in para, (
                    f"{ep['id']}.{sec['id']}[{p_idx}] contains hyphen/parens: {para}"
                )
                for pat in BANNED_CTA_PATTERNS:
                    assert not re.search(pat, para, re.IGNORECASE), f"{ep['id']}.{sec['id']} matched CTA {pat}"
                for pat in BANNED_TIMING_PATTERNS:
                    assert not re.search(pat, para, re.IGNORECASE), f"{ep['id']}.{sec['id']} matched timing {pat}"


if __name__ == "__main__":
    validate_catalog()
    for ep in EPISODES:
        chars = sum(len(p) for s in ep["sections"] for p in s["paragraphs"])
        words = sum(len(p.split()) for s in ep["sections"] for p in s["paragraphs"])
        print(f"{ep['id']} ({ep['slug']}): {len(ep['sections'])} sections, {words} words, {chars} chars, 16 unique shots — VALID!")
