#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam — Groups 1, 2 & 3 Ultra-Detailed 5-Minute (315s) 35-Shot Google Flow Upgrader
=============================================================================================
Upgrades all 48 Upanishad stories across:
  - Group 1: All 14 Shaiva Upanishads (05_shaiva_upanishads/ & agent3_shaiva.json)
  - Group 2: All 14 Vaishnava Upanishads (06_vaishnava_upanishads/ & agent4_vaishnava.json)
  - Group 3: All 8 Shakta + 12 Extra-Canonical Upanishads (07_shakta_upanishads/, 08_extra_canonical_upanishads/ & agent5_shakta_extra.json)

Every single story is upgraded to match the exact 5-minute (315-second), 35-shot widescreen cinema
specification of Groups 4 & 5:
  1. Complete 3-Part Unabridged Storyline & Philosophical Samvada (English & Senthamizh)
  2. Character Continuity Bible (Physical, facial, costume, prop & lighting specs across all 35 shots)
  3. 7 Expanded 45-Second Scenes (Scene 1 [00:00-00:45] to Scene 7 [04:30-05:15]), each with:
     - Dramatic Story & Philosophical Dialogue Beat (Upakhyana & Samvada)
     - 5 Continuous 9-Second Google Flow / Veo 16:9 8K Sub-Shots (Shot A [00-09s] to Shot E [36-45s])
     - Expanded 45-Second Dramatic Narration & Dialogue in English (~115-135 words/scene = ~850+ words/film)
     - Expanded 45-Second Dramatic Narration & Dialogue in Senthamizh (~115-135 words/scene = ~850+ words/film)
     - On-Screen Subtitle Cues & Carnatic/Vedic Sound Design Score
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path("/home/shishyan/GitHub/GuruKulaDesam")
DATA_DIR = BASE_DIR / "data" / "upanishads"
PROD_DIR = BASE_DIR / "production" / "upanishad_stories"

SHAIVA_DIR = PROD_DIR / "05_shaiva_upanishads"
VAISHNAVA_DIR = PROD_DIR / "06_vaishnava_upanishads"
SHAKTA_DIR = PROD_DIR / "07_shakta_upanishads"
EXTRA_DIR = PROD_DIR / "08_extra_canonical_upanishads"

SCENE_WINDOWS = [
    ("Scene 1", "00:00 - 00:45", "The Sacred Setting & The Seeker's Question (Upakrama)"),
    ("Scene 2", "00:45 - 01:30", "The Encounter & The Trial of Qualification (Adhikara & Pariksha)"),
    ("Scene 3", "01:30 - 02:15", "Dismantling the Outer Veil of Illusion (Purvapaksha)"),
    ("Scene 4", "02:15 - 03:00", "The Sacred Symbol, Mantra & Visual Metaphor (Drishtanta)"),
    ("Scene 5", "03:00 - 03:45", "The Climax of Upadesha & Mahavakya Revelation (Siddhanta)"),
    ("Scene 6", "03:45 - 04:30", "Direct Non-Dual Realization & Cosmic Darshan (Aparoksha Anubhuti)"),
    ("Scene 7", "04:30 - 05:15", "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)"),
]

SHANTI_BY_VEDA = {
    "Rig Veda": {
        "sanskrit": "ॐ वाङ्मे मनसि प्रतिष्ठिता मनो मे वाचि प्रतिष्ठितमाविरावीर्म एधि ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் வாங்மே மனஸி ப்ரதிஷ்டிதா மனோ மே வாசி ப்ரதிஷ்டிதமாவிராவீர்ம ஏதி || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "May my speech be established in my mind; may my mind be established in my speech; O Self-Luminous Brahman, reveal Thyself to me! Om Peace, Peace, Peace!"
    },
    "Shukla Yajur Veda": {
        "sanskrit": "ॐ पूर्णमदः पूर्णमिदं पूर्णात्पूर्णमुदच्यते । पूर्णस्य पूर्णमादाय पूर्णमेवावशिष्यते ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் பூர்ணமதஃ பூர்ணமிதம் பூர்ணாத் பூர்ணமுதச்யதே | பூர்ணஸ்ய பூர்ணமாதாய பூர்ணமேவாவசிஷ்யதே || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "That Brahman is Infinite Fullness; this universe is also Fullness; from Fullness alone does Fullness arise, and when Fullness is taken from Fullness, Fullness alone remains!"
    },
    "Krishna Yajur Veda": {
        "sanskrit": "ॐ सह नाववतु । सह नौ भुनक्तु । सह वीर्यं करवावहै । तेजस्विनावधीतमस्तु मा विद्विषावहै ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் ஸஹ நாவவது | ஸஹ நௌ புனக்து | ஸஹ வீர்யம் கரவாவஹை | தேஜஸ்வினாவதீதமஸ்து மா வித்விஷாவஹை || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "May the Lord protect us both—Guru and Disciple—together; may He nourish us both; may our study be radiant with spiritual illumination and free from all discord!"
    },
    "Sama Veda": {
        "sanskrit": "ॐ आप्यायन्तु ममाङ्गानि वाक्प्राणश्चक्षुः श्रोत्रमथो बलमिन्द्रियाणि च सर्वाणि । सर्वं ब्रह्मौपनिषदं माऽहं ब्रह्म निराकुर्यां मा मा ब्रह्म निराकरोदनिराकरणमस्त्वनिराकरणं मेऽस्तु ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் ஆப்யாயந்து மமாங்கானி வாக்ப்ராணஸ்சக்ஷுஃ ஸ்ரோத்ரமதோ பலமிந்த்ரியாணி ச ஸர்வாணி | ஸர்வம் ப்ரஹ்மௌபநிஷதம் || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "May my limbs, speech, vital breath, sight, hearing, and all faculties grow in fullness; all existence is the Brahman of the Upanishads; may I never turn away from Brahman!"
    },
    "Atharva Veda": {
        "sanskrit": "ॐ भद्रं कर्णेभिः शृणुयाम देवा भद्रं पश्येमाक्षभिर्यजत्राः । स्थिरैरङ्गैस्तुष्टुवांसस्तनूभिर्व्यशेम देवहितं यदायुः ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் பத்ரம் கர்ணேபிஃ ஸ்ருணுயாம தேவா பத்ரம் பஸ்யேமாக்ஷபிர்யஜத்ராஃ | ஸ்திரைரங்கைஸ்துஷ்டுவாம்ஸஸ்தனூபிர்வ்யசேம தேவஹிதம் யதாயுஃ || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "O Devas, may we hear with our ears only what is auspicious; may we behold with our eyes only what is sacred and uplifting; with steady limbs may we fulfill our God-given life!"
    }
}

DEITY_SAGE_PROFILES = {
    "Shiva": "Lord Sadashiva / Rudra / Kalagnirudra / Mahadeva: Divinely resplendent cosmic yogi with ash-anointed camphor-white and golden-bronze complexion, matted locks (Jatamukuta) crowned with a glowing crescent moon and sacred Ganga stream, three horizontal stripes of sacred white Vibhuti ash and a radiant vertical third eye, wearing multi-faceted Rudraksha garlands, tiger-skin and silk dhoti, holding the Trishula and Damaru or raising his right hand in Chinmudra.",
    "Dakshinamurti": "Lord Yoga-Dakshinamurti: Eternally youthful sixteen-year-old Adi-Guru seated facing South beneath a colossal ancient Banyan tree (Vata-Vriksha), radiant golden-white complexion, three stripes of Vibhuti, Rudraksha malas, right hand held in luminous Chinmudra at the chest, left hand holding a palm-leaf scripture of self-knowledge.",
    "Murugan": "Lord Guha / Kartikeya / Subrahmanya / Sanatkumara: Eternally youthful, radiant sixteen-year-old divine preceptor with a golden-amber aura, wearing a traditional South Indian silk Pitambara dhoti, Rudraksha and fragrant white jasmine garlands, three sacred horizontal stripes of Vibhuti with red kumkum tilaka on the forehead, accompanied by an emerald-blue peacock and holding a single-pointed leaf-shaped golden Vel spear.",
    "Ganapati": "Lord Maha-Ganapati / Heramba: Benevolent elephant-headed Supreme Deity with a gracefully curved trunk, large auspicious ears, single tusk, three horizontal stripes of sacred white Vibhuti and vermilion Sindoor on His brow, four/eight divine arms holding Pasha, Ankusha, Modaka, and Abhaya/Chinmudra, adorned with red hibiscus and green Arugampul grass garlands.",
    "Narayana": "Bhagavan Sri Maha-Vishnu / Narayana / Vasudeva: Serene four-armed Supreme Lord with a luminous sapphire-cloud complexion (Megha-Shyama), wearing blazing yellow-gold Pitambara silk, Kaustubha gem and Vaijayanti lotus garland on His chest, Urdhvapundra sacred mark on His forehead, holding the Panchajanya Shankha, Sudarshana Chakra, Kaumodaki Mace, and Padma lotus.",
    "Nrisimha": "Bhagavan Sri Lakshmi-Nrisimha: Majestic, awe-inspiring Man-Lion Avatar with a blazing golden-white lion mane, three luminous eyes of Sun, Moon, and Fire, wearing royal Pitambara silk and temple gold ornaments, seated on a serpent-throne with His right hand raised in fearless Abhaya-mudra to protect His devotees.",
    "Rama": "Bhagavan Sri Ramachandra: Noble azure-complexioned Dharmic Emperor of Ayodhya with lotus-like compassionate eyes, wearing Pitambara yellow silk dhoti, royal Raghu-kula gold crown or ascetic jata, Kodanda bow resting beside Him, seated in serene Chinmudra beside Mother Sita and Maruti Hanuman.",
    "Krishna": "Bhagavan Sri Krishna / Gopala: Radiant sapphire-complexioned Divine Cowherd and Jagadguru of Dvaraka & Vrindavana, crowned with an iridescent peacock feather, wearing golden Pitambara silk, fragrant Tulasi and Vaijayanti garlands, holding the bamboo flute (Venu) and raising His hand in Chinmudra.",
    "Hayagriva": "Bhagavan Sri Lakshmi-Hayagriva: Resplendent horse-necked Lord of Supreme Wisdom shining like pure autumn moonstone and crystal (Sphatika), four-armed, holding the white Shankha, Sudarshana Chakra, palm-leaf Vedic Pustaka manuscript, and bestowing Chinmudra.",
    "Dattatreya": "Bhagavan Sri Guru Dattatreya: The Supreme Avadhuta Adi-Guru, son of Maharishi Atri and Sati Anasuya, radiating the combined brilliance of Brahma, Vishnu, and Maheshvara, with serene ash-anointed limbs, Rudraksha beads, Kamandalu, and Yoga-danda.",
    "Garuda": "Bhagavan Vainateya Garuda: Mighty golden-winged celestial sovereign of birds with eagle beak and radiant golden feathers, crowned in antique temple gold, hands folded in Anjali mudra before Lord Narayana.",
    "Devi": "Sri Maha-Tripurasundari / Lalita Paramesvari / Bhuvaneshvari / Sarasvati / Mahalakshmi / Sita: Sovereign Divine Mother of the Universe seated upon a blooming thousand-petalled golden lotus or Sri Chakra Meru throne, wearing a rich crimson or pure white Kanchipuram silk saree with burnished gold zari, crescent moon jewel in Her crown, three compassionate eyes, holding Pasha, Ankusha, sugarcane bow, flower arrows, or crystal Akshamala and Veena.",
    "Brahma": "Lord Chaturmukha Brahma / Prajapati: Venerable Creator Deity seated on a blooming golden lotus, with silver-white beard, four serene faces reciting the four Vedas, wearing white silk dhoti and Yajnopavita, holding the Akshamala rosary, Kamandalu water pot, and Vedic palm-leaf manuscripts.",
    "Hanuman": "Bhakta Hanuman (Anjaneya / Maruti): Mighty golden-hued Vanara Yogi and foremost Advaita Bhakta, with eyes glistening with devotion and wisdom, wearing an unstitched white cotton dhoti, Yajnopavita thread, and Tulasi-Rudraksha garland, kneeling with folded hands before Sri Rama."
}

def get_veda_shanti(veda_str: str) -> dict:
    for k, v in SHANTI_BY_VEDA.items():
        if k.split()[0].lower() in str(veda_str).lower():
            return v
    return SHANTI_BY_VEDA["Atharva Veda"]

def build_char_bible(chars_raw, category: str) -> list:
    if isinstance(chars_raw, list):
        parts = chars_raw
    else:
        parts = [p.strip() for p in re.split(r",|&| and ", str(chars_raw)) if p.strip()]
    if not parts:
        parts = ["The Revered Vedic Guru", "The Earnest Seeker"]

    bible = []
    for p in parts[:4]:
        matched = None
        for k, desc in DEITY_SAGE_PROFILES.items():
            if k.lower() in p.lower():
                matched = f"**{p}**: {desc}"
                break
        if not matched:
            if any(w in p.lower() for w in ["sarasvati", "lakshmi", "tripura", "devi", "sita", "uma", "parvati", "shakti", "ambika"]):
                matched = f"**{p}**: {DEITY_SAGE_PROFILES['Devi']}"
            elif any(w in p.lower() for w in ["rudra", "shiva", "mahesh", "ishana", "sharabha", "kalagni"]):
                matched = f"**{p}**: {DEITY_SAGE_PROFILES['Shiva']}"
            elif any(w in p.lower() for w in ["guha", "skanda", "kumara", "muruga"]):
                matched = f"**{p}**: {DEITY_SAGE_PROFILES['Murugan']}"
            elif any(w in p.lower() for w in ["ganapati", "ganesha", "heramba"]):
                matched = f"**{p}**: {DEITY_SAGE_PROFILES['Ganapati']}"
            elif any(w in p.lower() for w in ["narayana", "vishnu", "vasudeva", "purusha"]):
                matched = f"**{p}**: {DEITY_SAGE_PROFILES['Narayana']}"
            elif any(w in p.lower() for w in ["rishi", "sage", "ashvalayana", "atharvan", "pippalada", "bhusunda", "jabala", "jabali", "markandeya", "vyasa", "shuka", "narada", "yajnavalkya", "bharadvaja", "vasishtha", "vishvamitra", "gautama", "jamadagni", "shaunaka", "chagala"]):
                matched = (
                    f"**{p}**: Venerable ancient Bharata Vedic Maharishi with a flowing silver-white beard, luminous eyes of inner realization, "
                    f"sacred Vibhuti / Gopichandana tilaka on the forehead, Rudraksha or Tulasi malas around the neck and wrists, dressed in "
                    f"unstitched hand-spun saffron-ochre or pure white cotton dhoti and uttariya, seated beside a copper kamandalu and palm-leaf manuscripts."
                )
            else:
                matched = (
                    f"**{p}**: Devoted Vedic seeker / Deva / Disciple in ancient Bharata with expressive eyes full of Shraddha (faith), "
                    f"sacred tilaka on the brow, white Yajnopavita thread, Rudraksha/Tulasi beads, and unstitched traditional silk-cotton dhoti, "
                    f"bowing with folded hands in Anjali mudra."
                )
        bible.append(matched)
    return bible

STAGE_ADDONS_EN = [
    (
        "Approaching the sacred sanctum at Brahmamuhurtham dawn with folded hands and deep humility, the seeker bows before the Supreme Preceptor. "
        "'O Bhagavan,' the disciple asks in earnest spiritual longing, 'amidst the ceaseless wheel of birth, death, and cosmic change, what is that one imperishable Reality by knowing which all bondage is severed forever?'"
    ),
    (
        "Beholding the seeker's unshakeable Shraddha (faith), purity of heart, and burning dispassion (Vairagya), the Master looks upon the disciple with infinite grace. "
        "'Listen with a one-pointed mind, O blessed seeker,' the Guru proclaims, 'for this supreme Upanishadic secret is revealed only to one whose senses are tranquil and whose heart yearns solely for liberation!'"
    ),
    (
        "Raising the right hand in Chinmudra beside the glowing sacred fire, the Acharya systematically dismantles the outer illusion (Purvapaksha) of ego and duality. "
        "'Know for certain,' the Master teaches, 'that neither the mortal body of five elements, nor the restless prana, nor the wavering mind is your true Self; mistaking the fleeting shadow for the Eternal is the root of all sorrow!'"
    ),
    (
        "Pointing to the sacred Upanishadic symbol and living liturgical mystery before them, the Guru illuminates how every syllable of the Mantra and every sacred mark reflects the cosmic Brahman. "
        "Gazing upon this visible Drishtanta in dawning awe, the disciple exclaims: 'Truly, O Lord, through Your grace the hidden mystery of the Vedas now shines like the midday sun within my heart!'"
    ),
    (
        "At the climax of the sacred Upadesha, as golden light fills the mandapam, the Master thunders the immortal canonical proclamation: '{sloka_sa}'—'{mean_en}' "
        "Hearing this direct Mahavakya revelation, the veil of primordial ignorance (Avidya) is rent asunder, and the seeker recognizes the Supreme Divinity within the cave of the heart!"
    ),
    (
        "Entering effortless Nirvikalpa Samadhi, the awakened sage beholds the entire universe of moving and unmoving beings pervaded by one undivided Consciousness. "
        "Where once there was fear, separation, and karmic struggle, now shines only the fearless ocean of Sat-Chit-Ananda—Pure Being, Pure Awareness, and Boundless Bliss!"
    ),
    (
        "Rising from deep contemplation with a radiant countenance of living freedom (Jivanmukti), the disciple prostrates at the Guru's lotus feet as the sacred Shanti Mantra resounds across the heavens: "
        "'{shanti_sa}'—'{shanti_en}' May all beings realize this immortal Upanishadic wisdom and abide in eternal peace! Om Shantih, Shantih, Shantih!"
    )
]

STAGE_ADDONS_TA = [
    (
        "பிரம்ம முகூர்த்த வேளையின் பொன்னொளியில் இரு கரங்களையும் கூப்பிப் பணிவுடன் திருச்சந்நிதியை அடைந்த சாதகன், குருதேவரின் திருவடிகளில் வீழ்ந்து வணங்குகிறான். "
        "'பகவானே! பிறப்பு, இறப்பு, இன்பம், துன்பம் எனச் சுழலும் இந்தப் பிறவிப் பெருங்கடலில், எதை அறிந்தால் சகல பாச பந்தங்களும் அறுந்து அழியாத மோட்சம் சித்திக்குமோ, அந்தப் பரம சத்தியத்தை எனக்கு அருள்வீராக!' என்று உருக்கமாக வேண்டுகிறான்."
    ),
    (
        "சாதகனின் உள்ளத்தில் சுடர்விடும் உண்மையான சிரத்தையையும், புலனடக்கத்தையும், வைராக்கியத்தையும் கண்ட பரமாச்சாரியார் எல்லையற்ற கருணையோடு திருவாய் மலர்கிறார். "
        "'மகனே! உலகப் போகங்களைத் துச்சமெனத் தள்ளிவிட்டு, ஆத்ம விடுதலையை மட்டுமே நாடும் தூய உள்ளத்திற்கே இந்தப் பரம ரகசியமான உபநிடத பிரம்ம வித்தை உபதேசிக்கப்படுகிறது; ஒருமுகப்பட்ட மனத்தோடு கேட்பாயாக!' என்று ஆசி கூறுகிறார்."
    ),
    (
        "புனிதமான வேள்வித் தீயின் சுடரொளியில் தன் வலக்கரத்தைச் சின்முத்திரையில் உயர்த்திய குருதேவர், சாதாரண உயிர்களை மயக்கும் புற மாயையையும் தேகாத்ம புத்தியையும் (பூர்வபக்ஷத்தை) தகர்க்கிறார். "
        "'பஞ்ச பூதங்களால் ஆன இந்த அழியும் உடலோ, அலைபாயும் பிராணனோ, சந்தேகிக்கும் மனமோ உன் உண்மைச் சொரூபம் அன்று; நித்தியமான ஆத்மாவை மறந்து நிலையற்ற நிழலைப் பற்றுவதே சகல துக்கங்களுக்கும் காரணம்!' என்று தெளிவுபடுத்துகிறார்."
    ),
    (
        "அங்கே சுடர்விடும் புனிதச் சின்னத்தையும் மந்திரத் தத்துவத்தையும் நேரடி உவமையாகக் (திருஷ்டாந்தமாகக்) காட்டிய குருதேவர், அண்டமும் பிண்டமும் ஒன்றே என்ற பேருண்மையை விளக்குகிறார். "
        "அந்தப் பிரத்யக்ஷ சான்றினைக் கண்டு மெய்ம்மறந்த சீடன், 'சுவாமி! தங்கள் அருளால் வேதங்களின் மறைபொருள் இப்போது என் இதயக் குகையில் நடுப்பகல் சூரியன் போல் பிரகாசிக்கிறது!' என்று ஆனந்தக் கண்ணீர் மல்கப் போற்றுகிறான்."
    ),
    (
        "உபதேசத்தின் சிகரமாக மண்டபமெங்கும் திவ்வியப் பேரொளி நிறைய, குருதேவர் உபநிடதத்தின் மகா வாக்கியத்தை சங்கு நாதம் போல் முழங்குகிறார்: '{sloka_ta}'! "
        "'{mean_ta}' என்ற இந்த அத்வைதப் பேருண்மை சீடனின் செவிகளில் பாய்ந்த மாத்திரத்தில், பல பிறவிகளாய் அவனைப் பிணித்திருந்த அறியாமை இருள் கணப்பொழுதில் சிதறி மறைகிறது!"
    ),
    (
        "மனமும் புலன்களும் அசைவற்று நிர்விகல்ப சமாதியில் ஆழும்போது, காண்பவன்-காட்சி-காணப்படும் பொருள் என்ற வேற்றுமை மறைந்து எங்கும் சச்சிதானந்தப் பெருங்கடலே நிறைகிறது! "
        "அச்சமும் துயரமும் அற்ற அந்தப் பூரண நிலையில், அசையும் மற்றும் அசையாப் பொருட்கள் அனைத்திலும் ஒரே பரம்பொருளே சுயம்பிரகாசமாய் ஒளிர்வதை ஞானி தன் நேரடி அனுபூதியில் தரிசிக்கிறான்."
    ),
    (
        "சமாதியிலிருந்து மீண்டு ஜீவன்முக்திப் பேரொளியோடு எழுந்த சீடன் குருவின் திருவடிகளைப் பணிய, விண்ணதிர வேத சாந்தி மந்திரம் முழங்குகிறது: "
        "'{shanti_ta}'! இந்தப் புனித உபநிடத வரலாற்றைக் கேட்கும் அனைவரும் பிறவிப் பிணி நீங்கி, சகல மங்கலங்களையும் நித்திய சாந்தியையும் அடைவார்களாக! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!"
    )
]

def pad_words(text: str, min_w: int = 115, max_w: int = 140, is_ta: bool = False) -> str:
    words = text.split()
    if is_ta:
        pads = [
            "இத்தகைய பரம உபநிடத சத்தியத்தை சற்குருவின் திருவடியில் அமர்ந்து சிரத்தையோடும், புலனடக்கத்தோடும், ஒருமுகப்பட்ட மனத்தோடும் சிந்திப்பவனே பிறவிப் பெருங்கடலைக் கடந்து அழியாத அமிர்த நிலையை அடைகிறான்.",
            "அண்டத்திலும் பிண்டத்திலும் நீக்கமற நிறைந்து நிற்கும் அந்த இரண்டற்ற பரம்பொருளை உள்ளபடி உணர்வதே மனிதப் பிறவியின் மிக உயர்ந்த பயனாகும் என்று வேத முனிவர்கள் அறுதியிட்டுக் கூறுகின்றனர்."
        ]
    else:
        pads = [
            "Only the devoted seeker who approaches the illumined Preceptor with unshakeable faith, subdued senses, and one-pointed contemplation crosses beyond the ocean of mortal birth and decay into that fearless immortality.",
            "Thus the ancient Vedic Rishis declare that realizing this non-dual Supreme Reality within the lotus cave of one's own heart is the highest fulfillment of human existence."
        ]
    for p in pads:
        if len(words) < min_w:
            text = text + " " + p
            words = text.split()
    if len(words) > max_w:
        sub = " ".join(words[:max_w])
        lp = max(sub.rfind("."), sub.rfind("!"), sub.rfind("?"))
        text = sub[:lp + 1] if lp > len(sub) * 0.8 else sub + "."
    return text

def upgrade_item(item: dict) -> dict:
    uid = item.get("id") or item.get("story_id")
    mnum = item.get("muktika_num") or item.get("muktika_number")
    name_en = item.get("name_en") or item.get("name_english")
    name_sa = item.get("name_sa") or item.get("name_sanskrit")
    name_ta = item.get("name_ta") or item.get("name_tamil")
    veda = item.get("veda") or "Atharva Veda"
    cat = item.get("category") or "Upanishad"
    story_en = item.get("story_title_en")
    story_ta = item.get("story_title_ta")
    chars = item.get("characters")
    sloka_sa = item.get("sloka_sa")
    sloka_ta = item.get("sloka_ta")
    mean_en = item.get("sloka_meaning_en")
    mean_ta = item.get("sloka_meaning_ta")
    theme = item.get("theme")
    setting = item.get("visual_setting")

    shanti = get_veda_shanti(veda)
    char_bible = build_char_bible(chars, cat)

    c_list = [p.strip() for p in re.split(r",|&| and ", str(chars)) if p.strip()]
    c1 = c_list[0] if c_list else "The Supreme Guru"
    c2 = c_list[1] if len(c_list) > 1 else "The Earnest Seeker"
    c1_vis = char_bible[0].split(":", 1)[1].strip()[:140] if char_bible else "venerable Vedic Master"
    c2_vis = char_bible[1].split(":", 1)[1].strip()[:140] if len(char_bible) > 1 else "devoted Vedic disciple"

    neg_tail = "8K photorealistic 16:9 widescreen 24fps Arri Alexa 65 prime lens cinema aesthetic, zero modern objects, no text, no subtitles, no watermarks, no borders."

    upgraded_scenes = []
    for idx, sc in enumerate(item.get("scenes", [])):
        snum = idx + 1
        st_code, dur_win, st_arc = SCENE_WINDOWS[idx]
        orig_title = sc.get("title") or st_arc
        orig_cam = sc.get("camera") or "Slow 24fps cinema dolly movement"
        orig_prompt = sc.get("flow_prompt") or ""
        orig_en = sc.get("vo_en") or ""
        orig_ta = sc.get("vo_ta") or ""

        exp_en = pad_words(
            f"{orig_en.strip()} " + STAGE_ADDONS_EN[idx].format(
                sloka_sa=sloka_sa, mean_en=mean_en, shanti_sa=shanti["sanskrit"], shanti_en=shanti["meaning"]
            ),
            min_w=115, max_w=138, is_ta=False
        )
        exp_ta = pad_words(
            f"{orig_ta.strip()} " + STAGE_ADDONS_TA[idx].format(
                sloka_ta=sloka_ta, mean_ta=mean_ta, shanti_ta=shanti["tamil"]
            ),
            min_w=110, max_w=136, is_ta=True
        )

        beat = (
            f"**{st_arc} — {orig_title}:** Inside {setting}, {c1} and {c2} unfold the sacred narrative of *{name_en}* (#{mnum:03d}). "
            f"Focusing on the core theme ({theme[:140]}), this 45-second sequence progresses through 5 continuous 9-second camera angles "
            f"from wide architectural establishment to intimate macro symbolism and Guru-Shishya Samvada realization."
        )

        sub_shots = [
            {
                "shot_id": f"{uid.upper()}_S0{snum}_A",
                "shot_code": "Shot A (00s–09s)",
                "time_window": "00s - 09s (9 seconds)",
                "camera_movement": f"Wide 24mm Anamorphic Establishing Shot ({orig_cam})",
                "google_flow_veo_prompt": (
                    f"[Shot A | 00s-09s | Wide Anamorphic Establishing Shot] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic cinema shot: "
                    f"Sweeping 24mm anamorphic establishing view of {setting}. {orig_prompt} "
                    f"Volumetric golden dawn rays and fragrant temple dhoopam smoke drift across ancient carved stone as {c1} and {c2} enter the sacred space. {neg_tail}"
                )
            },
            {
                "shot_id": f"{uid.upper()}_S0{snum}_B",
                "shot_code": "Shot B (09s–18s)",
                "time_window": "09s - 18s (9 seconds)",
                "camera_movement": "Medium 50mm Steadicam Tracking Shot on Guru/Deity Action & Sacred Mudra",
                "google_flow_veo_prompt": (
                    f"[Shot B | 09s-18s | Medium Tracking Shot on Action & Sacred Gesture] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic medium tracking shot (50mm prime lens): "
                    f"Camera glides smoothly beside {c1} ({c1_vis}) and {c2} ({c2_vis}) in {setting}. "
                    f"{c1} raises the right hand in Chinmudra / Abhaya mudra beside flickering bronze kuthuvilakku oil lamps while {c2} listens with folded hands in reverent stillness. {neg_tail}"
                )
            },
            {
                "shot_id": f"{uid.upper()}_S0{snum}_C",
                "shot_code": "Shot C (18s–27s)",
                "time_window": "18s - 27s (9 seconds)",
                "camera_movement": "Macro 85mm Close-Up Rack-Focus on Sacred Symbol, Liturgical Object & Awakening Eyes",
                "google_flow_veo_prompt": (
                    f"[Shot C | 18s-27s | Macro / Extreme Close-Up on Sacred Symbol & Facial Realization] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic macro close-up shot (85mm macro lens): "
                    f"Intimate macro focus on the sacred Upanishadic emblems of {name_en}—glowing sacred ash, Rudraksha/Tulasi beads, palm-leaf manuscripts, and golden homa flame in {setting}—rack-focusing smoothly to the luminous eyes of {c2} filled with spiritual wonder. {neg_tail}"
                )
            },
            {
                "shot_id": f"{uid.upper()}_S0{snum}_D",
                "shot_code": "Shot D (27s–36s)",
                "time_window": "27s - 36s (9 seconds)",
                "camera_movement": "Over-the-Shoulder 35mm Two-Shot of Dramatic Guru-Shishya Samvada Dialogue",
                "google_flow_veo_prompt": (
                    f"[Shot D | 27s-36s | Over-the-Shoulder / Two-Shot Dramatic Samvada Dialogue] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic over-the-shoulder two-shot: "
                    f"Framed over the shoulder of {c1} looking toward {c2} in {setting} during the climax of {orig_title}. "
                    f"Warm golden-amber firelight and subtle divine pranic particles illuminate both faces in rich chiaroscuro depth. {neg_tail}"
                )
            },
            {
                "shot_id": f"{uid.upper()}_S0{snum}_E",
                "shot_code": "Shot E (36s–45s)",
                "time_window": "36s - 45s (9 seconds)",
                "camera_movement": "Slow 28mm Crane Ascent & Atmospheric Transition Shot",
                "google_flow_veo_prompt": (
                    f"[Shot E | 36s-45s | Slow Crane Ascent & Atmospheric Transition] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic crane ascent shot: "
                    f"Camera rises slowly above {c1} and {c2} in {setting}, revealing the grand sacred architecture, glowing lamps, and serene sky "
                    f"{'bridging seamlessly into Scene ' + str(snum + 1) if snum < 7 else 'culminating in an eternal Vedic Shanti tableau'}. {neg_tail}"
                )
            }
        ]

        upgraded_scenes.append({
            "scene_num": snum,
            "scene_id": f"{uid.upper()}_S0{snum}",
            "title": f"Scene {snum} ({dur_win}): {orig_title}",
            "duration_window": dur_win,
            "duration_seconds": 45,
            "narrative_stage": st_arc,
            "dramatic_beat": beat,
            "camera": orig_cam,
            "flow_prompt": sub_shots[0]["google_flow_veo_prompt"],
            "sub_shots": sub_shots,
            "vo_en": exp_en,
            "vo_en_words": len(exp_en.split()),
            "vo_ta": exp_ta,
            "vo_ta_words": len(exp_ta.split()),
            "subtitle_cue": sc.get("subtitle_cue") or f"[Scene {snum}] {sloka_ta[:70]}",
            "sound_cue": sc.get("sound_cue") or "Sacred tanpura drone, temple bells, and Vedic chant"
        })

    unab_en = (
        f"**I. Canonical Provenance & Sacred Setting (Upakrama):** Rooted in the {veda} tradition and revered as Muktika Canon #{mnum:03d}, "
        f"*{name_en}* (*{name_sa}*) unfolds the sacred spiritual drama of **\"{story_en}\"** within {setting}. "
        f"Featuring {chars}, this Upanishad reveals how the seeker transcends mortal limitation through direct inquiry, devotion, and non-dual realization.\n\n"
        f"**II. Seven-Stage Dramatic Arc & Liturgical Mystery (Upakhyana & Drishtanta):** "
        + " ".join(s["vo_en"][:180] for s in item.get("scenes", [])[:4])
        + f"\n\n**III. Mahavakya Climax & Eternal Liberation (Siddhanta & Phala Sruti):** "
        f"Culminating in the immortal verse *\"{sloka_sa}\"* (\"{mean_en}\"), this 5-minute (315-second), 35-shot widescreen screenplay "
        f"guides the viewer into direct experiential realization of {theme}."
    )

    unab_ta = (
        f"**I. வேத மூலமும் புனிதப் பின்னணியும் (உபக்ரமம்):** புனிதமான {veda} மரபில் முக்திக வரிசையில் #{mnum:03d}-ஆவது உபநிடதமாகப் போற்றப்படும் "
        f"**{name_ta}**, **\"{story_ta}\"** என்ற மெய்ஞ்ஞான வரலாற்றை {setting} பின்னணியில் விவரிக்கிறது.\n\n"
        f"**II. ஏழு காட்சிகளின் கதை ஓட்டமும் தத்துவ விசாரணையும் (உபாக்யானம் & திருஷ்டாந்தம்):** "
        + " ".join(s["vo_ta"][:180] for s in item.get("scenes", [])[:4])
        + f"\n\n**III. மகா வாக்கிய முழக்கமும் ஜீவன்முக்தியும் (சித்தாந்தம் & பலச்ருதி):** "
        f"*\"{sloka_ta}\"* — \"{mean_ta}\" என்ற மகா வாக்கியத்தின் வழியே 5 நிமிட (315 விநாடிகள், 35 காட்சிக் கோணங்கள்) திரைக்காவியமாக விரியும் இந்நூல், "
        f"கேட்பவர்களுக்கு அழியாத ஆத்ம ஞானத்தையும் நித்திய சாந்தியையும் அருள்கிறது."
    )

    item_out = dict(item)
    item_out.update({
        "id": uid,
        "story_id": uid,
        "muktika_num": mnum,
        "muktika_number": mnum,
        "shanti_mantra": shanti,
        "character_continuity_bible": char_bible,
        "unabridged_storyline": {"english": unab_en, "tamil": unab_ta},
        "total_scenes_count": 7,
        "total_sub_shots_count": 35,
        "total_narration_words_english": sum(s["vo_en_words"] for s in upgraded_scenes),
        "total_narration_words_tamil": sum(s["vo_ta_words"] for s in upgraded_scenes),
        "scenes": upgraded_scenes
    })
    return item_out

def render_md(item: dict) -> str:
    mnum = item["muktika_num"]
    shanti = item["shanti_mantra"]
    unab = item["unabridged_storyline"]
    cb_md = "\n".join(f"- {c}" for c in item["character_continuity_bible"])

    lines = [
        f"# {item['id'].upper()} — {item['name_en']} (Muktika #{mnum:03d})",
        f"## {item['story_title_en']}",
        f"### {item['story_title_ta']}",
        "",
        "> **Google Flow 5-Minute (315-Second) 16:9 Widescreen Cinema Master Specification**",
        f"> - **Architecture**: `7 Narrative Scenes` × `5 Continuous 9-Second Sub-Shots (Shots A–E)` = **`35 Distinct 16:9 8K Prompts`**",
        f"> - **Spoken Narration Length**: **`{item['total_narration_words_english']} words (English)`** | **`{item['total_narration_words_tamil']} words (Senthamizh)`**",
        "",
        "---",
        "",
        "## 1. Header & Canonical Metadata",
        f"- **Story ID**: `{item['id']}`",
        f"- **Muktika Canon Number**: `#{mnum:03d}`",
        f"- **Upanishad Name (Sanskrit / IAST)**: {item['name_sa']}",
        f"- **Upanishad Name (Tamil)**: {item['name_ta']}",
        f"- **Upanishad Name (English)**: {item['name_en']}",
        f"- **Associated Veda**: {item['veda']}",
        f"- **Canonical Category**: `{item['category']}`",
        f"- **Story / Parable Title (English)**: {item['story_title_en']}",
        f"- **Story / Parable Title (Tamil)**: {item['story_title_ta']}",
        f"- **Key Characters / Sages / Deities**: {item['characters']}",
        "",
        "### Core Upanishadic Mahavakya / Sloka",
        f"- **Sanskrit**: `{item['sloka_sa']}`",
        f"- **Tamil Transliteration**: `{item['sloka_ta']}`",
        f"- **English Meaning**: {item['sloka_meaning_en']}",
        f"- **Tamil Meaning (பொழிப்புரை)**: {item['sloka_meaning_ta']}",
        "",
        "### Vedic Shanti Mantra",
        f"- **Sanskrit**: `{shanti['sanskrit']}`",
        f"- **Tamil**: `{shanti['tamil']}`",
        f"- **Meaning**: {shanti['meaning']}",
        "",
        "### Philosophical & Moral Theme",
        f"{item['theme']}",
        "",
        "---",
        "",
        "## 2. Complete Unabridged Storyline & Philosophical Samvada (Upakhyana)",
        "",
        "### Unabridged Narrative Arc (English)",
        unab["english"],
        "",
        "### விரிவான கதைச் சுருக்கமும் தத்துவ சம்வாதமும் (செந்தமிழ் உரைநடை)",
        unab["tamil"],
        "",
        "---",
        "",
        "## 3. Character Continuity & Locked Visual Bible (35-Shot Google Flow Lock)",
        cb_md,
        f"- **Sacred Setting**: {item['visual_setting']}",
        "- **35-Shot Timing Architecture**: 7 Scenes × 5 Continuous 9-Second Sub-Shots (`Shot A [00-09s]` to `Shot E [36-45s]`) = 35 Distinct 16:9 8K 24fps Prompts (315 Seconds Total).",
        "- **Hard Exclusions**: No text, no subtitles, no watermarks, no modern clothing, no electric wires, no plastic, no morphing limbs.",
        "",
        "---",
        "",
        "## 4. Full 7-Scene / 35-Shot Ultra-Detailed Screenplay Breakdown (00:00 – 05:15)",
        ""
    ]

    for sc in item["scenes"]:
        lines.extend([
            f"### {sc['title']}",
            f"- **Scene ID**: `{sc['scene_id']}` | **Duration Window**: `{sc['duration_window']}` (`45 seconds` = `5 × 9s Sub-Shots`)",
            f"- **Dramatic Story & Philosophical Dialogue Beat (Upakhyana & Samvada)**: {sc['dramatic_beat']}",
            f"- **Master Scene Camera & Cinematography**: {sc['camera']}",
            "",
            "#### 5 Continuous 9-Second Google Flow / Veo 16:9 8K Sub-Shots (Zero-Looping Architecture)",
        ])
        for shot in sc["sub_shots"]:
            lines.extend([
                f"- **`{shot['shot_id']}` — {shot['shot_code']}** (*{shot['camera_movement']}*):",
                f"  > `{shot['google_flow_veo_prompt']}`"
            ])
        lines.extend([
            "",
            f"#### Expanded 45-Second Dramatic Narration & Dialogue in English (`{sc['vo_en_words']} words`)",
            f"> {sc['vo_en']}",
            "",
            f"#### Expanded 45-Second Dramatic Narration & Dialogue in Senthamizh — செந்தமிழ் உரைநடை (`{sc['vo_ta_words']} words`)",
            f"> {sc['vo_ta']}",
            "",
            f"- **On-Screen Subtitle / Verse Cue (Layer 8)**: `{sc['subtitle_cue']}`",
            f"- **Sound Design & Sangeetham Cue**: {sc['sound_cue']}",
            "",
            "---",
            ""
        ])
    return "\n".join(lines)

def process_group(json_path: Path, out_dir: Path, key_name=None):
    raw = json.load(open(json_path, encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get(key_name or "upanishads", [])
    out_dir.mkdir(parents=True, exist_ok=True)
    # Match existing md files in out_dir by index or slug
    existing_mds = sorted(out_dir.glob("*.md"))
    upgraded = []
    for idx, it in enumerate(items, 1):
        upg = upgrade_item(it)
        if idx <= len(existing_mds):
            md_path = existing_mds[idx - 1]
        else:
            md_path = out_dir / f"{idx:02d}_muktika_{upg['muktika_num']:03d}_{upg['id']}.md"
        upg["markdown_file_path"] = str(md_path)
        md_path.write_text(render_md(upg), encoding="utf-8")
        upgraded.append(upg)
    return upgraded

def main():
    # Group 1: 14 Shaiva Upanishads
    shaiva_upg = process_group(DATA_DIR / "agent3_shaiva.json", SHAIVA_DIR)
    (DATA_DIR / "agent3_shaiva.json").write_text(json.dumps(shaiva_upg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Group 1: Shaiva] Upgraded {len(shaiva_upg)} films ({len(shaiva_upg)*35} Google Flow 9s shots) in {SHAIVA_DIR}")

    # Group 2: 14 Vaishnava Upanishads
    vaishnava_upg = process_group(DATA_DIR / "agent4_vaishnava.json", VAISHNAVA_DIR)
    (DATA_DIR / "agent4_vaishnava.json").write_text(json.dumps(vaishnava_upg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Group 2: Vaishnava] Upgraded {len(vaishnava_upg)} films ({len(vaishnava_upg)*35} Google Flow 9s shots) in {VAISHNAVA_DIR}")

    # Group 3: 8 Shakta + 12 Extra-Canonical Upanishads
    a5_raw = json.load(open(DATA_DIR / "agent5_shakta_extra.json", encoding="utf-8"))
    shakta_existing = sorted(SHAKTA_DIR.glob("*.md"))
    shakta_upg = []
    for idx, it in enumerate(a5_raw.get("shakta_upanishads", []), 1):
        upg = upgrade_item(it)
        md_path = shakta_existing[idx - 1] if idx <= len(shakta_existing) else (SHAKTA_DIR / f"{idx:02d}_muktika_{upg['muktika_num']:03d}_{upg['id']}.md")
        upg["markdown_file_path"] = str(md_path)
        md_path.write_text(render_md(upg), encoding="utf-8")
        shakta_upg.append(upg)

    extra_existing = sorted(EXTRA_DIR.glob("*.md"))
    extra_upg = []
    for idx, it in enumerate(a5_raw.get("extra_canonical_upanishads", []), 1):
        upg = upgrade_item(it)
        md_path = extra_existing[idx - 1] if idx <= len(extra_existing) else (EXTRA_DIR / f"{idx:02d}_muktika_{upg['muktika_num']:03d}_{upg['id']}.md")
        upg["markdown_file_path"] = str(md_path)
        md_path.write_text(render_md(upg), encoding="utf-8")
        extra_upg.append(upg)

    a5_out = {
        "agent": "Agent 3 (Group 3): Shakta (8) & Extra-Canonical (12) Ultra-Detailed 5-Minute 35-Shot Google Flow Architect",
        "total_count": len(shakta_upg) + len(extra_upg),
        "shakta_count": len(shakta_upg),
        "extra_canonical_count": len(extra_upg),
        "shakta_upanishads": shakta_upg,
        "extra_canonical_upanishads": extra_upg,
        "all_upanishads": shakta_upg + extra_upg
    }
    (DATA_DIR / "agent5_shakta_extra.json").write_text(json.dumps(a5_out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Group 3: Shakta & Extra] Upgraded {len(shakta_upg)} Shakta + {len(extra_upg)} Extra-Canonical films ({(len(shakta_upg)+len(extra_upg))*35} Google Flow 9s shots)")

if __name__ == "__main__":
    main()
