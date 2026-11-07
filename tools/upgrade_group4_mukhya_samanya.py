#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam — Agent 4: Group 4 Upgrader
===========================================
Upgrades ALL 22 Mukhya Upanishad Stories & ALL 29 Samanya Vedanta Upanishad Stories
(51 total stories = 357 total scenes = 1,785 distinct 9-second 16:9 8K Google Flow / Veo sub-shots)
into Ultra-Detailed 5-Minute (300–315s) 16:9 Widescreen Screenplays.

Features per Story:
1. Complete Unabridged Storyline (Upakhyana & Samvada) — multi-paragraph philosophical & dramatic narrative.
2. Character Continuity Bible — exact physical, facial, costume, prop, and lighting continuity specs
   for every sage, seeker, monarch, and deity across all 35 sub-shots.
3. 7 Expanded 45-Second Scenes (Scene 1 to Scene 7), each containing:
   - Dramatic Story & Philosophical Dialogue Beat (Upakhyana & Samvada)
   - 5 Distinct 9-Second Continuous 16:9 8K Google Flow / Veo Sub-Shots:
     * Shot A (00s–09s): Wide Anamorphic Establishing / Architectural & Nature Entry Shot
     * Shot B (09s–18s): Medium Tracking Shot on the Guru / Deity / Seeker Action & Sacred Gesture
     * Shot C (18s–27s): Macro / Close-Up Shot on the Sacred Symbol, Experiment, Ritual Object, or Facial Expression
     * Shot D (27s–36s): Over-the-Shoulder / Two-Shot Dramatic Dialogue & Philosophical Realization
     * Shot E (36s–45s): Slow Crane Ascent / Atmospheric Transition Shot bridging into the next scene
   - Expanded 45-Second Dramatic Narration & Dialogue in English (~110–130 words per scene = ~850 words/film)
   - Expanded 45-Second Dramatic Narration & Dialogue in Senthamizh (செந்தமிழ் உரைநடை) (~110–130 words per scene = ~850 words/film)
   - On-Screen Subtitle Cues & Sound Design / Sangeetham Score
"""

import json
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path("/home/shishyan/GitHub/GuruKulaDesam")
TOOLS_DIR = BASE_DIR / "tools"
MUKHYA_DIR = BASE_DIR / "production" / "upanishad_stories" / "01_mukhya_upanishads"
SAMANYA_DIR = BASE_DIR / "production" / "upanishad_stories" / "02_samanya_vedanta_upanishads"
JSON_OUT = BASE_DIR / "data" / "upanishads" / "agent1_mukhya_samanya.json"

sys.path.insert(0, str(TOOLS_DIR))
import build_upanishad_agent1_mukhya_samanya as base_agent1


# ==============================================================================
# ADDITIONAL SAMANYA VEDANTA SPECS (#28 ANNAPURNA #53 & #29 CHULIKA #70)
# Ensures all 29 Samanya Vedanta stories + 22 Mukhya stories = 51 stories exist!
# ==============================================================================
ADDITIONAL_SAMANYA_SPECS = [
    {
        "story_id": "SAMANYA_28_ANNAPURNA_53",
        "muktika_number": 53,
        "upanishad_sanskrit": "अन्नपूर्णोपनिषद्",
        "upanishad_iast": "Annapūrṇopaniṣad",
        "upanishad_tamil": "அன்னபூர்ணா உபநிடதம்",
        "upanishad_english": "Annapurna Upanishad",
        "veda": "Atharva Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Sage Ribhu at Kashi & The Fivefold Silence of Goddess Annapurna: The Alms of Jnana-Vairagya",
        "story_title_tamil": "காசியில் ரிபு முனிவரின் தவமும் அன்னபூர்ணா தேவியின் பஞ்ச மௌன ஞான உபதேசமும்!",
        "characters": [
            "Maharishi Ribhu (The great Brahmarishi who performed a thousand years of penance in Kashi and instructed young Nidagha)",
            "Goddess Annapurna Paramesvari (Sovereign Mother of Kashi holding the jeweled ladle and golden vessel of immortal Jnana-Bhiksha)",
            "Nidagha (The earnest young Vedic seeker learning the Five Silences and Seven Jnana-Bhumikas from Sage Ribhu)"
        ],
        "mahavakya_sanskrit": "अन्नपूर्णे सदापूर्णे शङ्करप्राणवल्लभे । ज्ञानवैराग्यसिद्ध्यर्थं भिक्षां देहि च पार्वति ॥ चिन्मात्रममलं शान्तं ब्रह्मास्मीति विभावयेत् ॥",
        "mahavakya_tamil_translit": "அன்னபூர்ணே ஸதாபூர்ணே சங்கரப்ராணவல்லபே | ஞானவைராக்யஸித்த்யர்த்தம் பிக்ஷாம் தேஹி ச பார்வதி || சின்மாத்ரமமலம் சாந்தம் ப்ரஹ்மாஸ்மீதி விபாவயேத் ||",
        "mahavakya_meaning_english": "O Annapurna, ever full and complete, beloved life-consort of Shankara! Grant me the alms of supreme Self-Knowledge and Dispassion, O Parvati! Meditate ever: 'I am Pure Consciousness alone, stainless, peaceful Brahman!'",
        "mahavakya_meaning_tamil": "என்றும் பூரணமானவளே, சங்கரனின் உயிர்க் காதலியான அன்னபூர்ணா தேவியே! ஞானமும் வைராக்கியமும் சித்திக்கும்பொருட்டு எனக்கு அருட்பிச்சை அளிப்பாயாக! 'நான் களங்கமற்ற, அமைதியான தூய சைதன்ய பிரம்மமே' என்று எப்போதும் தியானிப்பாயாக!",
        "philosophical_theme": "The highest alms (Bhiksha) is Jnana-Vairagya (Self-Knowledge and Dispassion); the manifold world is only Sankalpa (mental projection) on the canvas of Chit-Akasha; mastering the Five Silences (Vak, Aksha, Kashtha, Sushupti, and Maha-Mauna) and Seven Jnana-Bhumikas leads to Jivanmukti.",
        "setting_specifics": "The ancient sacred stone ghats of Kashi and the lamp-lit golden granite sanctum of Goddess Annapurna, transitioning to Maharishi Ribhu's tranquil forest tapovanam where he instructs young Nidagha beneath a towering banyan tree.",
        "metaphor_highlight": "The Jeweled Golden Ladle & Akshaya Vessel of Goddess Annapurna bestowing Jnana-Bhiksha, Five Glowing Bronze Kuthuvilakku Lamps representing the Fivefold Silence (Pancha-Mauna), and Waves subsiding into the Ocean of Chinmatra.",
        "s1_en": "In the sacred forest hermitage of the Atharva Veda tradition, young Nidagha bowed with folded hands before the great Brahmarishi Ribhu and asked: 'O Venerable Master, by what supreme secret did you attain this unshakeable peace of Atma-Vidya?' Smiling with boundless compassion, Ribhu recounted his long penance in the luminous city of Kashi, where he worshiped Goddess Annapurna—the Eternal Mother of the Universe.",
        "s1_ta": "புனிதமான வன ஆசிரமத்தில் இளம் சீடன் நிதாகன், மகா முனிவரான ரிபுவை வணங்கி, 'குருதேவா! எத்தகைய மேலான ரகசியத்தால் தாங்கள் இந்த அசைக்க முடியாத ஆத்ம ஞானப் பேரமைதியைப் பெற்றீர்கள்?' என்று கேட்டான். கருணையோடு புன்னகைத்த ரிபு முனிவர், ஒளிமயமான காசித் திருத்தலத்தில் அன்னபூர்ணா தேவியை நோக்கித் தான் புரிந்த நெடிய தவத்தை விவரிக்கத் தொடங்கினார்.",
        "s2_en": "Pleased by Ribhu's thousand-year tapas, the Sovereign Empress Annapurna—crowned with the crescent moon and holding the jeweled ladle of infinite nourishment—appeared before him in radiant splendor. When She offered him any boon in the three worlds, Ribhu folded his hands and asked not for empires or heaven, but for the supreme alms of liberating Self-Knowledge and Vairagya!",
        "s2_ta": "ரிபு முனிவரின் தவத்தால் மகிழ்ந்த அகிலாண்ட நாயகி அன்னபூர்ணா தேவி, பிறை நிலவு சூடி, மாணிக்கக் கரண்டியும் அட்சயப் பாத்திரமும் ஏந்தி நேரில் காட்சியளித்தாள்! மூவுலகச் செல்வங்களை வரமாகத் தர முன்வந்த தேவியிடம், ரிபு முனிவர் உலகப் போகங்களை வேண்டாமல், பிறவிப் பிணியைத் தீர்க்கும் 'ஞான வைராக்கியப் பிச்சை'யை மட்டுமே வரமாகக் கேட்டார்!",
        "s3_en": "Goddess Annapurna revealed the first secret to Ribhu, which he now imparted to Nidagha: 'O child, this entire manifold universe of birth, death, and sorrow has no independent reality outside Consciousness. Just as waves are nothing but water, it is the mind's own Sankalpa—its restless imagination—that conjures bondage; when Sankalpa subsides, pure Brahman alone shines.'",
        "s3_ta": "அன்னபூர்ணா தேவி அருளிய முதல் ரகசியத்தை ரிபு முனிவர் நிதாகனுக்கு உபதேசித்தார்: 'மகனே! பிறப்பு, இறப்பு, இன்பம், துன்பம் கொண்ட இந்தப் பிரபஞ்சக் காட்சி அறிவுச் சுடரான ஆத்மாவைத் தவிர வேறில்லை. நீரில் எழும் அலைகள் நீரேயன்றி வேறில்லாதது போல, மனதின் சங்கல்பமே பந்தத்தை உருவாக்குகிறது; சங்கல்பம் அடங்கும்போது தூய பிரம்மம் மட்டுமே ஒளிர்கிறது!'",
        "s4_en": "Ribhu taught the sacred discipline of the Five Silences—from restraining speech, senses, and rigid bodily effort, to transcending deep sleep into Kashtha-Mauna and Sushupti-Mauna, where the seeker abides in the unbroken recognition that all that exists is Chinmatra—Pure Undivided Awareness—ascending through the seven stages of wisdom!",
        "s4_ta": "வாக்கு மௌனம், இந்திரிய மௌனம், காஷ்ட மௌனம், சுஷுப்தி மௌனம் ஆகிய படிகளைக் கடந்து, காணப்படும் அனைத்தும் 'சின்மாத்திரம்' எனப்படும் தூய பேரறிவே என்று உணரும் மகா மௌனத்தையும், சுபயேச்சை முதல் துரியகாமி வரையிலான ஏழு ஞான பூமிகைகளையும் ரிபு முனிவர் தெளிவாக விளக்கினார்.",
        "s5_en": "Delivering the supreme Mahavakya of Goddess Annapurna, Ribhu proclaimed: 'Neither are you this perishable body, nor the wavering breath, nor the doubting mind! Contemplate without interruption: Chinmatram Amalam Shantam Brahmasmi—I am Pure Consciousness alone, stainless, birthless, and eternally peaceful Brahman!'",
        "s5_ta": "அன்னபூர்ணா தேவியின் மகா வாக்கியத்தை ரிபு முனிவர் முழங்கினார்: 'நீ அழியும் இந்த உடலும் அல்ல; அலைபாயும் பிராணனும் அல்ல; சந்தேகிக்கும் மனமும் அல்ல! சின்மாத்ரமமலம் சாந்தம் ப்ரஹ்மாஸ்மி — நான் களங்கமற்ற, பிறப்பற்ற, நித்திய அமைதியான தூய அறிவுப் பிரம்மமே என்று இடைவிடாது உணர்வாயாக!'",
        "s6_en": "At these words, the veil of duality dissolved in Nidagha's heart. Like a hungry traveler fed at the eternal banquet of Mother Annapurna, all craving vanished. Looking inward and outward, he beheld no division between knower and known—only the ocean of Sat-Chit-Ananda, ever full, ever satisfied, and free from fear.",
        "s6_ta": "குருவின் இந்த அருள்மொழியால் நிதாகனின் இதயத்திலிருந்த இருமைத் திரை விலகியது! அன்னபூர்ணா தேவியின் அமுத விருந்தினை உண்டவன் பசி ஆறுவது போல, அவனது சகல உலக ஆசைகளும் கணத்தில் மறைந்தன. உள்ளும் புறமும் அறிபவன்-அறியப்படுவது என்ற பேதமின்றி, எங்கும் சச்சிதானந்தப் பெருங்கடலே நிறைந்திருப்பதை அவன் நேரில் உணர்ந்தான்.",
        "s7_en": "Thus concludes the Annapurna Upanishad: he who realizes this supreme nourishment of Self-Knowledge moves through the world as a Jivanmukta—composed in joy and sorrow, seeing the Divine Mother and Supreme Shiva in every living being!",
        "s7_ta": "இவ்வாறு அன்னபூர்ணா உபநிடதம் நிறைவுறுகிறது: இந்த ஆத்ம ஞான அமுதத்தை உணர்ந்த ஜீவன்முக்தன், இன்பத்திலும் துன்பத்திலும் சமநிலை கொண்டு, அனைத்து உயிர்களிலும் அன்னபூர்ணா தேவியையும் பரமசிவனையும் தரிசித்துப் பேரானந்தத்தில் நிலைத்திருக்கிறான்!"
    },
    {
        "story_id": "SAMANYA_29_CHULIKA_70",
        "muktika_number": 70,
        "upanishad_sanskrit": "चूलिकोपनिषद्",
        "upanishad_iast": "Cūlikopaniṣad",
        "upanishad_tamil": "சூளிகா உபநிடதம்",
        "upanishad_english": "Chulika Upanishad",
        "veda": "Atharva Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Maharishi Bhrigu & The Eight-Eyed Cosmic Weaver: The Crest-Jewel Where the 24 Tattvas Dissolve",
        "story_title_tamil": "பிருகு முனிவரும் எட்டுக் கண்கள் கொண்ட பிரபஞ்ச நெசவாளியும்: இருபத்து நான்கு தத்துவங்களுக்கு மேலான சூளிகாப் பரம்பொருள்!",
        "characters": [
            "Maharishi Bhrigu & The Atharva Veda Rishis (Inquiring into the 'Chulika'—the Crest-Summit of Samkhya-Vedanta synthesis)",
            "The Eight-Form Cosmic Deva / Aja Purusha (The Unborn Spirit upon whom the 24 Prakritic principles and the Brahmachari's cosmic vows rest)"
        ],
        "mahavakya_sanskrit": "अष्टपादं शुचिं हंसं त्रिसूत्रमणुमव्ययम् । तमेवं विदित्वेह मृत्युपाशैर्न बध्यते ॥",
        "mahavakya_tamil_translit": "அஷ்டபாதம் ஸுசிம் ஹம்ஸம் த்ரிஸூத்ரமணுமவ்யயம் | தமேவம் விதித்வேஹ ம்ருத்யுபாஸைர்ந பத்யதே ||",
        "mahavakya_meaning_english": "Knowing that pure, imperishable Swan of Eight Feet and Three Threads—subtler than the subtle—the wise seeker is never bound by the noose of Death!",
        "mahavakya_meaning_tamil": "எட்டுப் பாதங்களும் மூன்று இழைகளும் கொண்ட தூய, அழியாத அந்த ஆத்ம அன்னப் பறவையை (ஹம்ஸத்தை) உள்ளபடி அறிபவன், இவ்வுலகில் மரண பாசத்தால் ஒருபோதும் கட்டப்படுவதில்லை!",
        "philosophical_theme": "The Chulika (Crest/Pinnacle) uniting Vedic Mantras (Rohita, Vratya, Skambha, Prana of the Atharva Veda) with the 24 Tattvas of Prakriti and the 25th/26th Transcendental Purusha-Brahman.",
        "setting_specifics": "An ancient Atharva Vedic mountain-crest ashram (Chulika Tapovanam) overlooking a sea of golden clouds, with a sacred lotus pond, a three-stranded sacrificial cord, and a glowing Homa fire.",
        "metaphor_highlight": "The Summit Crest (Chulika) above the 24 steps of Prakriti, the Pure White Swan with Three Threads (Triloka/Triguna), and the Spider reabsorbing its cosmic web into the One Unborn Purusha.",
        "s1_en": "In the luminous Chulika Upanishad (#70 in the Muktika canon, belonging to the Atharva Veda—where 'Chulika' means the topmost crest or pinnacle of a temple tower!), the sages gathered around Maharishi Bhrigu to ask: 'Who is that One Support behind the twenty-four principles of Nature, praised under many names across all the hymns of the Vedas?'",
        "s1_ta": "முக்திக வரிசையில் 70-ஆவது உபநிடதமாகத் திகழும் அதர்வண வேதத்தின் 'சூளிகா உபநிடதத்தில்' (சூளிகா என்றால் கோபுரத்தின் உச்சி சிகரம் என்று பொருள்!), மகரிஷி பிருகுவைச் சூழ்ந்த முனிவர்கள் கேட்டனர்: 'இயற்கையின் இருபத்து நான்கு தத்துவங்களுக்கும் ஆதாரமாக நின்று, வேத மந்திரங்களில் பல பெயர்களால் போற்றப்படும் அந்த ஒரே பரம்பொருள் யார்?'",
        "s2_en": "The Acharya pointed to the pure white Swan gliding across the mountain lake: 'Behold the Ashtapada Hamsa—the Spotless Swan of Eight Feet, bound by Three Threads of the three Gunas, subtler than the atom and imperishable! Blinded by passion and ignorance, ordinary mortals see only the outer web of Nature, while the wise behold the Unborn Spirit within!'",
        "s2_ta": "மலைச் சுனையில் நீந்தும் வெண்ணிற அன்னப் பறவையைக் காட்டி ஆச்சாரியர் அருளினார்: 'எட்டுப் பாதங்களும், முக்குணங்கள் என்னும் மூன்று இழைகளும் கொண்ட தூய ஆத்ம ஹம்ஸத்தைப் பாருங்கள்! ஆசையாலும் அறியாமையாலும் மயங்கியவர்கள் வெளித்தோற்றமான பிரகிருதியை மட்டுமே காண்கிறார்கள்; ஞானிகளோ உள்ளே ஒளிரும் பிறப்பற்ற புருஷனைத் தரிசிக்கிறார்கள்!'",
        "s3_en": "Enumerating the twenty-four evolutes of Prakriti—the five elements, five subtle essences, ten senses, mind, ego, intellect, and unmanifest root-nature—the Upanishad declares that all of them are merely the garment woven by the One Deva, like a spider spinning forth and drawing back its silken threads!",
        "s3_ta": "பஞ்ச பூதங்கள், ஐந்து தன்மாத்திரைகள், பத்து இந்திரியங்கள், மனம், புத்தி, அகங்காரம், மூலப் பிரகிருதி ஆகிய இருபத்து நான்கு தத்துவங்களையும் பட்டியலிட்ட உபநிடதம், சிலந்திப் பூச்சி தன் வலையைப் பின்னித் தன்னுள்ளே இழுத்துக்கொள்வது போல் அந்த ஒரே தேவனே இவற்றைத் தோற்றுவித்து ஒடுக்குகிறான் என்று முழங்குகிறது!",
        "s4_en": "Then the Chulika Upanishad unites all the grand cosmological hymns of the Atharva Veda: 'When the Vedas sing of the Cosmic Brahmachari, or Skambha the Cosmic Pillar, or Rohita the Golden Sun, or Prana and Anadvan—know that every single hymn points exclusively to that One Partless Brahman!'",
        "s4_ta": "தொடர்ந்து அதர்வண வேதத்தின் மகா சூக்தங்களை ஒன்றிணைத்துக் காட்டுகிறது உபநிடதம்: 'வேதங்கள் பிரம்மச்சாரி சூக்தத்தாலோ, பிரபஞ்சத் தூணான ஸ்கம்பனாகவோ, ரோஹிதனாகவோ, பிராணனாகவோ எதைப் போற்றிப் பாடினாலும், அவையனைத்தும் அவயவங்களற்ற அந்த ஒரே பரம்பொருளையே குறிக்கின்றன!'",
        "s5_en": "At the climax of the teaching, the Guru proclaimed: 'Beyond the twenty-four principles of Prakriti and beyond the individual Jiva shines the Supreme Atman—without parts, without stain, peaceful, and self-luminous! Knowing Him right here in this human birth, the seeker is never again bound by the fetters of Death!'",
        "s5_ta": "உபதேசத்தின் சிகரமாக குருதேவர் முழங்கினார்: 'இருபத்து நான்கு பிரகிருதி தத்துவங்களுக்கும், தனிப்பட்ட ஜீவ பாவத்திற்கும் மேலாக, களங்கமற்ற, அவயவங்களற்ற சுயம்பிரகாச ஆத்மா ஒளிர்கிறது! அதனை இப்பிறவியிலேயே உள்ளபடி உணர்பவன் மரண பாசத்தால் ஒருபோதும் கட்டப்படுவதில்லை!'",
        "s6_en": "As the morning clouds parted below the mountain peak, the disciples beheld all forms dissolving like mist into the golden radiance of the One Unborn Witness.",
        "s6_ta": "மலைச் சிகரத்தின் கீழே காலை மேகங்கள் விலகியபோது, அனைத்து நாம-ரூபங்களும் பனிப்படலம் போல் விலகி, இரண்டற்ற ஆத்ம ஜோதியே எங்கும் நிறைந்திருப்பதைச் சீடர்கள் நேரில் உணர்ந்தனர்.",
        "s7_en": "Thus concludes the Chulika Upanishad—the crest-jewel of the Atharva Veda: he who realizes the Weaver behind the web of Nature attains supreme Kaivalya and eternal peace!",
        "s7_ta": "இவ்வாறு அதர்வண வேதத்தின் சிகர மணியான சூளிகா உபநிடதம் நிறைவுறுகிறது: பிரகிருதி வலையின் பின்னுள்ள ஆத்ம நாயகனை உணர்பவன் கைவல்ய முக்தியையும் நிலையான சாந்தியையும் அடைகிறான்!"
    }
]


# ==============================================================================
# CHARACTER VISUAL CONTINUITY ARCHETYPE REGISTRY (FOR GOOGLE FLOW 35-SHOT LOCK)
# ==============================================================================
CHARACTER_VISUAL_PROFILES = {
    "Nachiketa": "A twelve-year-old Vedic Brahmachari boy with luminous, fearless dark eyes, golden-brown skin, a neat topknot (shikha), three horizontal lines of sacred Vibhuti ash on his forehead, a single Rudraksha bead on a cotton cord around his neck, white Yajnopavita sacred thread across his left shoulder, and an unstitched knee-length hand-spun off-white cotton dhoti.",
    "Yama": "Lord Vaivasvata Yama Dharmaraja, towering and regal with a serene, compassionate yet awe-inspiring dark-bronze countenance, sculpted beard, antique burnished gold crown (kirita), dark indigo-and-burnished-gold silk pitambara dhoti, heavy Rudraksha and gold necklaces, radiating a subtle halo of golden-amber Dharma-fire.",
    "Svetaketu": "A twenty-four-year-old Vedic youth of tall, slender build, fair-olive complexion, expressive eyes that transition from scholarly pride to deep humility, wearing a crisp unstitched white cotton dhoti, saffron angavastram over his shoulder, sacred thread, and holding etched palm-leaf manuscripts.",
    "Uddalaka": "Maharishi Uddalaka Aruni, a sixty-five-year-old Sama Veda Kulapati with a flowing silver-white beard, warm compassionate eyes, sacred sandalwood and vibhuti tilaka, Rudraksha malas around his neck and wrists, dressed in earth-toned ochre-saffron hand-spun cotton dhoti and uttariya.",
    "Satyakama": "Young Satyakama Jabala, an eighteen-year-old ascetic youth with an honest, radiant face glowing with golden Brahma-Tejas, sun-bronzed skin from tending cattle in the forest, wearing a simple unbleached cotton dhoti, sacred thread, and carrying a wooden cowherd's staff and sacrificial samit twigs.",
    "Gautama": "Acharya Haridrumata Gautama, a venerable seventy-year-old Vedic preceptor with silver hair tied in a jatamukuta, calm piercing eyes, three streaks of white vibhuti, Rudraksha beads, and a saffron-bordered white cotton dhoti.",
    "Gargi": "Brahmavadini Gargi Vachaknavi, a dignified, fearless thirty-five-year-old Vedic woman philosopher with luminous dark eyes, serene scholarly authority, hair bound in a simple classical kondai adorned with white jasmine, wearing an unstitched off-white and golden-ochre handloom cotton-silk saree, sacred vibhuti tilaka, and Rudraksha mala.",
    "Maitreyi": "Brahmavadini Maitreyi, a serene thirty-year-old spiritual seeker and wife of Yajnavalkya, with radiant contemplative eyes, dressed in a pure unstitched white-and-saffron-bordered cotton saree, minimal antique gold ear-studs, sacred Rudraksha beads, and sandalwood tilaka.",
    "Yajnavalkya": "Maharishi Yajnavalkya, the peerless Shukla Yajur Veda sage in his late fifties, broad-shouldered with a majestic flowing white beard, leonine gaze, glowing golden-bronze skin, three horizontal lines of vibhuti with a sandalwood dot, wearing a rich ochre-saffron cotton dhoti, uttariya, and carrying a knotted bamboo danda.",
    "Janaka": "Rajarishi Janaka of Videha, a fifty-year-old philosopher-emperor with a calm, regal face, neatly trimmed royal beard, antique gold mukuta crown set with rubies, cream-and-gold silk royal dhoti and angavastram, and Rudraksha-gold necklace, embodying detachment amidst royal splendor.",
    "Indra": "Devaraja Indra, tall and resplendent celestial king with a noble golden complexion, ornate Vedic gold crown, Pitambara yellow-gold silk dhoti, jeweled armlets, and humble folded hands when standing as a disciple before the Guru.",
    "Virochana": "Virochana, King of the Asuras, muscular and proud-featured, wearing a heavy dark-bronze and crimson royal silk garment, elaborate golden crown, jewel necklaces, and carrying a haughty, self-satisfied expression.",
    "Uma": "Goddess Uma Haimavati / Annapurna / Parvati, divinely resplendent Mother of the Universe with a serene golden complexion, compassionate lotus eyes, wearing a rich crimson-and-burnished-gold Kanchipuram silk saree, crescent-moon jewel in her hair, Rudraksha and antique temple gold ornaments, radiating a soft white-gold aura.",
    "Bhrigu": "Bhrigu Varuni, a thirty-year-old tapasvi sage with a lean, luminous frame, matted locks tied high, glowing eyes refined by fivefold meditation, dressed in a simple white cotton dhoti and deer-skin upper cloth.",
    "Varuna": "Lord Varuna, venerable father and Guru of Bhrigu, majestic with silver-white hair and beard, dressed in pearl-white and sea-gold silk dhoti, seated on a carved stone seat beside sacred waters.",
    "Pippalada": "Maharishi Pippalada, an eighty-year-old Atharva Veda patriarch with deep-set, all-knowing eyes, long snow-white beard, weathered bronze skin, vibhuti marks, Rudraksha garlands, and ochre cotton robes, seated beneath an ancient Peepal tree.",
    "Raikva": "Sayugva Raikva, a radical, unconventional paramahamsa sage with tousled hair, a blissful carefree smile, weathered skin, wearing a simple coarse cotton loincloth/dhoti while seated in royal self-contentment beneath a wooden bullock cart.",
    "Brihadratha": "King Brihadratha of the Ikshvaku dynasty, a forty-five-year-old royal ascetic who has cast aside his crown, with sun-darkened skin, matted hair (jata), thin austere frame, wearing bark-cloth (valkala) and Rudraksha beads.",
    "Ribhu": "Maharishi Ribhu, a seventy-year-old jivanmukta sage radiating boundless peace, white beard, luminous eyes, saffron-white cotton dhoti, Rudraksha mala, and copper kamandalu.",
    "Nidagha": "Young seeker Nidagha, a twenty-two-year-old devoted brahmachari with eager, contemplative eyes, sacred thread, vibhuti tilaka, and unstitched white cotton dhoti.",
    "Narada": "Devarishi Narada, celestial sage in flowing white silk dhoti, Rudraksha malas, topknot, carrying his iconic carved wooden Mahati Veena with dual gourds.",
    "Sanatkumara": "Bhagavan Sanatkumara (Skanda), eternally youthful sixteen-year-old sage of supreme wisdom, glowing like the morning sun, adorned in saffron silk dhoti, Rudraksha beads, and vibhuti, radiating fearless Brahma-Tejas.",
    "Vajashravasa": "Maharishi Vajashravasa (Gautama), stern and wealthy sixty-year-old Vedic ritualist father of Nachiketa, with a greying beard, Rudraksha and gold necklaces, white cotton dhoti, and ceremonial wooden ladle by the sacrificial fire.",
    "Gautama": "Acharya Haridrumata Gautama, a venerable seventy-year-old Vedic preceptor with silver hair tied in a jatamukuta, calm piercing eyes, three streaks of white vibhuti, Rudraksha beads, and a saffron-bordered white cotton dhoti.",
    "Katyayani": "Katyayani, noble Vedic householder wife of Sage Yajnavalkya, dressed in a traditional turmeric-and-crimson handloom cotton saree, auspicious kumkuma tilaka, and simple gold bangles.",
    "Shaunaka": "Shaunaka Mahashala, a venerable, noble Vedic householder-scholar in crisp white silk-cotton dhoti, gold-threaded angavastram, Rudraksha mala, and three lines of sacred ash, approaching with folded hands.",
    "Jabala": "Mother Jabala, a humble, compassionate Vedic village mother in a simple earth-toned handloom cotton saree, her face radiating quiet dignity and truthfulness.",
    "Vasishtha": "Brahmarishi Vasishtha, royal preceptor of Ayodhya with a long snow-white beard, glowing ब्रह्मतेजस् (Brahma-Tejas) aura, white cotton dhoti, Rudraksha garlands, and kamandalu.",
    "Garuda": "Vainateya Garuda (Suparna), the majestic golden-winged celestial Eagle-Deity with radiant golden feathers, royal crown, and folded hands in devotion to Lord Narayana.",
    "Rama": "Bhagavan Sri Ramachandra, serene azure-complexioned Emperor of Ayodhya in Pitambara yellow silk, royal Raghu crown, Kodanda bow resting nearby, seated in Chinmudra alongside Sita Devi and Maharishi Vasishtha.",
    "Hanuman": "Bhakta Hanuman (Maruti), mighty golden-furred Vanara sage-devotee with radiant eyes of pure devotion and Advaita wisdom, wearing a white cotton dhoti, sacred thread, and Tulasi-Rudraksha garland, kneeling with folded hands."
}


def build_character_continuity_bible(story: dict) -> list:
    """Builds exact physical, costume, prop, and lighting continuity profiles for all characters in the story."""
    profiles = []
    for ch in story.get("characters", []):
        ch_head = ch.split("(")[0].strip()
        matched = None
        for key, desc in CHARACTER_VISUAL_PROFILES.items():
            if key.lower() in ch_head.lower():
                matched = f"**{ch}**: {desc}"
                break
        if not matched:
            for key, desc in CHARACTER_VISUAL_PROFILES.items():
                if key.lower() in ch.lower():
                    matched = f"**{ch}**: {desc}"
                    break
        if not matched:
            if any(w in ch_head.lower() for w in ["acharya", "rishi", "sage", "guru", "kulapati", "maharishi", "vyasa", "angiras", "manduka", "mudgala", "apantaratamas", "sankriti", "atharvangiras", "vasishtha", "shakayanya", "mahidasa", "vamadeva", "paingala"]):
                matched = (
                    f"**{ch}**: Venerable ancient Bharata Vedic Maharishi in his sixties, with a flowing silver-white beard, "
                    f"serene compassionate eyes, three horizontal lines of sacred Vibhuti ash and sandalwood paste on his forehead, "
                    f"Rudraksha malas around his neck and wrists, dressed in authentic unstitched hand-spun ochre-saffron cotton dhoti and uttariya, "
                    f"seated on a kusha-grass and deer-skin seat beside a copper kamandalu and etched palm-leaf manuscripts."
                )
            elif any(w in ch_head.lower() for w in ["king", "emperor", "pratardana", "ajatashatru", "janashruti"]):
                matched = (
                    f"**{ch}**: Noble ancient Indian Rajarishi monarch with a dignified bearded countenance, antique burnished-gold Vedic crown, "
                    f"hand-woven cream-and-gold silk dhoti and angavastram, sacred Rudraksha and gold chest ornaments, transitioning from royal grandeur "
                    f"to humble bare-chested devotion before the Guru."
                )
            elif any(w in ch_head.lower() for w in ["surya", "savitar", "pushan", "agni", "vayu", "brahma", "shiva", "narayana", "paramesvara", "garuda", "skanda", "prajapati"]):
                matched = (
                    f"**{ch}**: Resplendent Vedic Deity / Cosmic Presence rendered in authentic classical South Indian & Vedic sculptural realism—"
                    f"bathed in volumetric golden-amber and sapphire divine radiance, adorned in traditional pitambara silk, antique gold temple jewelry, "
                    f"and sacred mudras of fearlessness (Abhaya) and wisdom (Chinmudra)."
                )
            else:
                matched = (
                    f"**{ch}**: Earnest Vedic seeker / Brahmachari in ancient Bharata, with expressive dark eyes full of Shraddha (faith), "
                    f"three horizontal lines of Vibhuti ash on the forehead, white Yajnopavita sacred thread, Rudraksha neck-bead, "
                    f"and unstitched off-white hand-spun cotton dhoti."
                )
        profiles.append(matched)
    return profiles


def build_unabridged_storyline(story: dict) -> dict:
    """
    Constructs a rich, multi-paragraph Unabridged Storyline & Philosophical Upakhyana
    in both English and Senthamizh for the story header.
    """
    u_en = story["upanishad_english"]
    u_ta = story["upanishad_tamil"]
    t_en = story["story_title_english"]
    t_ta = story["story_title_tamil"]
    m_num = story["muktika_number"]
    veda = story["veda"]
    chars = "; ".join(story["characters"])
    setting = story["setting_specifics"]
    metaphor = story["metaphor_highlight"]
    theme = story["philosophical_theme"]
    mv_sa = story["mahavakya_sanskrit"]
    mv_en = story["mahavakya_meaning_english"]
    mv_ta = story["mahavakya_meaning_tamil"]

    s_en_summary = " ".join(sc["narration_en"] for sc in story["scenes"])
    s_ta_summary = " ".join(sc["narration_ta"] for sc in story["scenes"])

    para1_en = (
        f"**I. Canonical Provenance & Sacred Setting (Upakrama):** "
        f"Rooted in the immortal {veda} tradition and revered as Muktika Canon #{m_num:03d}, *{u_en}* (*{story['upanishad_iast']}*) "
        f"unfolds the timeless spiritual drama of **\"{t_en}\"** within {setting}. "
        f"The narrative brings together {chars} in a profound Upanishadic dialogue (*Samvada*) where the deepest existential questions "
        f"of life, death, consciousness, and liberation are tested not through dry academic debate, but through lived Tapas, "
        f"unshakeable Shraddha (faith), and direct spiritual experimentation."
    )
    para2_en = (
        f"**II. Dramatic Arc & Sacred Metaphor (Upakhyana & Drishtanta):** "
        f"{s_en_summary} "
        f"Throughout this seven-stage journey, the Upanishad anchors its subtlest non-dual teaching in the unforgettable visual metaphor of "
        f"**{metaphor}**—transforming an everyday phenomenon of nature or Gurukulam life into a blazing window onto the Infinite."
    )
    para3_en = (
        f"**III. Philosophical Climax & Mahavakya Realization (Siddhanta & Phala Sruti):** "
        f"At the summit of the teaching rings the eternal Sanskrit proclamation: *\"{mv_sa}\"*—\"{mv_en}\" "
        f"Establishing the core theme of {theme}, this 5-minute (315-second), 35-shot widescreen cinema master guides the viewer "
        f"from initial seeker's doubt (*Purvapaksha*) to direct, unmediated Self-realization (*Aparoksha Anubhuti*) and eternal peace (*Shanti*)."
    )

    para1_ta = (
        f"**I. வேத மூலமும் புனிதப் பின்னணியும் (உபக்ரமம்):** "
        f"புனிதமான {veda} மரபில் உதித்ததும், முக்திக வரிசையில் #{m_num:03d}-ஆவது உபநிடதமாகப் போற்றப்படுவதுமான **{u_ta}**, "
        f"**\"{t_ta}\"** என்ற காலத்தால் அழியாத ஞான வரலாற்றை நமக்குக் காட்டுகிறது. "
        f"இக்கதை நிகழும் புனிதச் சூழலில் ({setting}), குருவும் சீடனும் சந்தித்து நிகழ்த்தும் சம்வாதம் வெறும் ஏட்டுச் சுரைக்காயான தர்க்க வாதமன்று; "
        f"மாறாக, தீவிரத் தவம், சிரத்தை மற்றும் நேரடி ஆத்ம விசாரணையின் வழியே பிறப்பு-இறப்பற்ற பரம்பொருளைக் கண்டறியும் உயிரோட்டமான காவியமாகும்."
    )
    para2_ta = (
        f"**II. கதை ஓட்டமும் உபநிடத உவமையும் (உபாக்யானம் & திருஷ்டாந்தம்):** "
        f"{s_ta_summary} "
        f"ஏழு காட்சிகளாக விரியும் இந்தத் திரைக்காவியத்தில், **{metaphor}** என்னும் அற்புத உவமையின் வழியே "
        f"கண்ணுக்குப் புலப்படாத நுண்ணிய ஆத்ம தத்துவம் ஒவ்வொருவரும் நேரில் கண்டு உணரும் வண்ணம் விளக்கப்படுகிறது."
    )
    para3_ta = (
        f"**III. மகா வாக்கிய முழக்கமும் அபரோக்ஷ அனுபூதியும் (சித்தாந்தம் & பலச்ருதி):** "
        f"உபதேசத்தின் சிகரமாக *\"{story['mahavakya_tamil_translit']}\"* — அதாவது, \"{mv_ta}\" என்ற மகா வாக்கியம் முழங்குகிறது. "
        f"ஐந்து நிமிடங்கள் (315 விநாடிகள்) மற்றும் 35 தொடர்ச்சியான கோணங்கள் (35 Sub-Shots) கொண்ட இந்த அகலத்திரை ஆவணப் படம், "
        f"சாதகனின் ஐயத்தை நீக்கி, இரண்டற்ற அத்வைதப் பேரானந்தத்திலும் நித்திய சாந்தியிலும் நிலைபெறச் செய்கிறது."
    )

    return {
        "english": f"{para1_en}\n\n{para2_en}\n\n{para3_en}",
        "tamil": f"{para1_ta}\n\n{para2_ta}\n\n{para3_ta}"
    }


# ==============================================================================
# SCENE EXPANSION ENGINE: 5 SUB-SHOTS (A-E) + 110-130 WORD BILINGUAL NARRATION
# ==============================================================================

STAGE_DIALOGUE_EN = [
    (
        "Stepping across the threshold of the sacred hermitage with folded hands and trembling reverence, the seeker bows low before the illumined Master. "
        "'O Bhagavan,' the disciple pleads in earnest inquiry, 'though the outer rites and scriptures fill the world, my heart still yearns for that imperishable Truth which conquers sorrow and death!'"
    ),
    (
        "Gazing into the seeker's eyes with piercing yet boundless compassion, the Guru tests the depth of that spiritual resolve. "
        "'My child,' the Master speaks in a voice as steady as the mountain rock, 'this supreme Brahmavidya cannot be bought by wealth or grasped by a restless mind; tell me, are you ready to cast aside every fleeting illusion for the Eternal?'"
    ),
    (
        "With gentle authority, the Acharya begins to peel back the outer veil of worldly delusion—Purvapaksha—that binds ordinary mortals. "
        "'Listen closely,' the Guru instructs, raising his right hand in Chinmudra beside the sacred flame, 'for he who mistakes the perishable shadow of names and forms for the Reality wanders from birth to birth in vain!'"
    ),
    (
        "Leaning forward in rapt silence, the disciple watches as the Guru transforms a simple sacred object before them into a living mirror of the cosmos. "
        "'Behold this visible testimony right before your eyes!' the Master proclaims, while the seeker whispers in dawning wonder: 'Truly, O Lord, what was hidden to my outer sight now shines clear within my intellect!'"
    ),
    (
        "As golden light floods the sanctum and the sacred fire rises without smoke, the Guru's voice resonates like a cosmic conch with the supreme Mahavakya: '{mv_sa}' "
        "Hearing that thunderous proclamation of non-dual identity—'{mv_en}'—every lingering doubt in the disciple's heart is shattered forever!"
    ),
    (
        "Closing the eyes in effortless Nirvikalpa Samadhi, the awakened seeker experiences the boundary between observer and observed dissolving into an ocean of pure Sat-Chit-Ananda. "
        "'Wonder of wonders!' the illumined soul sings within the cave of the heart, 'I am neither the mortal body nor the wavering mind; I am That indivisible, fearless Consciousness shining in all beings!'"
    ),
    (
        "Bowing at the Guru's lotus feet as the morning sun crowns the horizon, the liberated sage receives the eternal benediction to walk the earth in fearless peace. "
        "And across the sacred ashram rings the timeless Vedic Shanti invocation: '{shanti_sa}'—'{shanti_en}'—blessing all humanity with supreme awakening! Om Shantih, Shantih, Shantih!"
    )
]

STAGE_DIALOGUE_TA = [
    (
        "புனிதமான ஆசிரமத்தின் திருவாசலைப் பணிவுடன்க் கடந்து வந்த சாதகன், இரு கரங்களையும் கூப்பி சற்குருவின் திருவடிகளில் வீழ்ந்து வணங்குகிறான். "
        "'பகவானே! உலகின் புறச் சடங்குகளும் நூல்களும் எங்கும் நிறைந்திருந்தாலும், பிறவிப் பிணியையும் மரண பயத்தையும் நிரந்தரமாகத் தீர்க்கும் அந்த அழியாத மெய்ப்பொருளையே என் உள்ளம் நாடுகிறது; கருணை கூர்ந்து எனக்கு அருள்வீராக!' என்று உருக்கமாக வேண்டுகிறான்."
    ),
    (
        "சாதகனின் கண்களில் சுடர்விடும் உண்மையான தாகத்தைத் தன் கருணைப் பார்வையால் அளந்த குருதேவர், அவனது வைராக்கியத்தையும் சிரத்தையையும் சோதிக்கத் தொடங்குகிறார். "
        "'குழந்தாய்! அலைபாயும் மனதாலோ அழியும் உலகச் செல்வத்தாலோ இந்தப் பரம பிரம்ம வித்தையை ஒருபோதும் அடைய முடியாது; நிலையற்ற மாயைக் கவர்ச்சிகளை உதறித் தள்ளிவிட்டு, நித்திய சத்தியத்தைத் தரிசிக்க நீ முழுமையாகச் சித்தமாய் இருக்கிறாயா?' என்று கம்பீரமாகக் கேட்கிறார்."
    ),
    (
        "அக்னிஹோத்ர வேள்வித் தீயின் சுடரொளியில் தன் வலக்கரத்தைச் சின்முத்திரையில் உயர்த்திய ஆச்சாரியர், சாதாரண மனிதர்களைக் கட்டிப்போடும் வெளித்தோற்ற மயக்கங்களை (பூர்வபக்ஷத்தை) ஒவ்வொன்றாகத் தகர்க்கிறார். "
        "'மகனே! நாம-ரூபங்களால் ஆன இந்த நிலையற்ற நிழலையே உண்மை என நம்பி மயங்குபவன் பிறவிச் சுழலில் மீண்டும் மீண்டும் உழல்கிறான்; ஆகவே புலன்களின் மயக்கத்தைக் கடந்து உள்முகமாகத் திரும்புவாயாக!' என்று தெளிவுபடுத்துகிறார்."
    ),
    (
        "இமைக்காமல் உற்று நோக்கும் சீடனின் முன்னால், இயற்கையின் எளிய காட்சியையும் புனிதப் பொருளையும் பிரபஞ்ச ரகசியத்தை விளக்கும் நேரடி உவமையாக (திருஷ்டாந்தமாக) குருதேவர் மாற்றுகிறார். "
        "'இதோ உன் கண்களின் முன்னால் விரியும் இந்தப் பிரத்யக்ஷ சான்றினைப் பார்!' என்று குரு காட்டும்போது, சீடன் மெய்ம்மறந்து, 'சுவாமி! என் புறக் கண்களுக்குப் புலப்படாமல் மறைந்திருந்த நுண்ணிய பேருண்மை இப்போது என் அகக்கண்ணில் தெளிவாகப் புலப்படுகிறது!' என்று போற்றுகிறான்."
    ),
    (
        "அந்தப் புனிதக் கணத்தில் பொன்மயமான பேரொளி மண்டபமெங்கும் நிறைய, குருதேவர் சங்கு நாதம் போல் உபநிடதத்தின் மகா வாக்கியத்தை முழங்குகிறார்: '{mv_ta_trans}'! "
        "'{mv_ta_mean}' என்ற அந்த இரண்டற்ற அத்வைதப் பேருண்மை சீடனின் செவிகளில் பாய்ந்தவுடன், அவனது உள்ளத்தில் பல பிறவிகளாய் உறைந்திருந்த அறியாமை இருளும் ஐயங்களும் கணப்பொழுதில் சிதறி மறைகின்றன!"
    ),
    (
        "புலன்களும் மனமும் அசைவற்று நிர்விகல்ப சமாதியில் ஆழும்போது, பார்ப்பவன்-பார்க்கப்படும் பொருள் என்ற இருமைத் திரை விலகி எங்கும் சச்சிதானந்தப் பெருங்கடலே பொங்குகிறது. "
        "'ஆகா! அழியும் இந்தப் பருவுடலும் நானல்ல, அலைபாயும் மனமும் நானல்ல; எல்லா உயிர்களின் இதயக் குகையிலும் சுயம்பிரகாசமாய் ஒளிரும் பிறப்பற்ற, அச்சமற்ற அந்தப் பூரண ஆத்மாவே நான்!' என்று ஞானி தன் நேரடி அனுபூதியில் திளைக்கிறான்."
    ),
    (
        "கீழ்வானில் உதய சூரியன் பொன்னொளி வீச, குருவின் திருவடிகளைப் பணிந்து ஆசி பெற்ற அந்த ஜீவன்முக்தன், இவ்வுலகில் எதற்கும் அஞ்சாத பேரமைதியோடு வலம் வருகிறான். "
        "அப்போது குருகுலம் முழுவதும் '{shanti_ta}' என்ற வேத சாந்தி மந்திரம் விண்ணதிர முழங்கி, இக்காவியத்தைக் கேட்கும் அனைவர் உள்ளத்திலும் அழியாத ஆத்ம சாந்தியையும் மங்கலத்தையும் நிறைக்கிறது! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!"
    )
]


def trim_or_pad_to_target(text: str, min_words: int = 110, max_words: int = 135, is_tamil: bool = False) -> str:
    """Ensures every scene's narration lands cleanly inside the 110-135 word window (~850 words per 7-scene film)."""
    words = text.split()
    if len(words) < min_words:
        if is_tamil:
            pad_clauses = [
                "இத்தகைய பரம உபநிடத சத்தியத்தை சற்குருவின் திருவடியில் அமர்ந்து சிரத்தையோடும், புலனடக்கத்தோடும், ஒருமுகப்பட்ட மனத்தோடும் கேட்பவனே பிறவிப் பெருங்கடலைக் கடந்து அழியாத அமிர்த நிலையை அடைகிறான்.",
                "அண்டத்திலும் பிண்டத்திலும் நிறைந்து நிற்கும் அந்த இரண்டற்ற பரம்பொருளை உள்ளபடி உணர்வதே மனிதப் பிறவியின் மிக உயர்ந்த பயனாகும் என்று வேத முனிவர்கள் அறுதியிட்டுக் கூறுகின்றனர்.",
                "புறப் புலன்களின் ஓட்டத்தை நிறுத்தி, இதயத் தாமரையில் ஒளிரும் சாட்சி சைதன்யத்தை நேரில் தரிசிக்கும்போது, சகல கர்ம பந்தங்களும் அறியாமை இருளும் சூரியனைக் கண்ட பனி போல் விலகி, நித்தியமான ஜீவன்முக்திப் பேரானந்தம் பிறக்கிறது."
            ]
        else:
            pad_clauses = [
                "Only the devoted seeker who approaches the illumined Preceptor with unshakeable faith, subdued senses, and one-pointed contemplation crosses beyond the ocean of mortal birth and decay into that fearlessness.",
                "Thus the ancient Vedic Rishis declare that realizing this non-dual Brahman within the cave of one's own heart is the supreme fulfillment of human existence.",
                "When the restless waves of the mind subside and the inner Witness shines forth in its own self-luminous glory, every fetter of karma and ignorance dissolves like morning mist before the rising sun."
            ]
        for cl in pad_clauses:
            if len(words) < min_words:
                text = text + " " + cl
                words = text.split()
    if len(words) > max_words:
        # Keep up to max_words and end cleanly at punctuation if possible
        subset = " ".join(words[:max_words])
        last_punct = max(subset.rfind("."), subset.rfind("!"), subset.rfind("?"), subset.rfind("'"), subset.rfind('"'))
        if last_punct > len(subset) * 0.82:
            text = subset[:last_punct + 1]
        else:
            text = subset + "."
    return text


def build_dramatic_beat(story: dict, scene_idx: int, sc: dict) -> str:
    """Builds the Dramatic Story & Philosophical Dialogue Beat (Upakhyana & Samvada) for a scene."""
    stage_num, dur_win, stage_title = base_agent1.SCENE_TEMPLATE_WINDOWS[scene_idx]
    chars = story["characters"]
    primary_char = chars[0].split("(")[0].strip()
    secondary_char = chars[1].split("(")[0].strip() if len(chars) > 1 else "the devoted Vedic seeker"
    metaphor = story["metaphor_highlight"]
    setting = story["setting_specifics"]

    beats = [
        (
            f"**Upakrama (The Sacred Arrival & Existential Question):** In {setting}, {secondary_char} approaches {primary_char} "
            f"at Brahmamuhurtham dawn. Burdened by the limits of mortal action and outer phenomena, the seeker poses the foundational question "
            f"of the *{story['upanishad_english']}*, initiating the sacred *Samvada* (philosophical dialogue) beside the blazing Agnihotra altar."
        ),
        (
            f"**Adhikara & Pariksha (The Test of Qualification & Vairagya):** {primary_char} examines the inner readiness (*Adhikara*), "
            f"faith (*Shraddha*), and dispassion (*Vairagya*) of {secondary_char}. Worldly attachments, intellectual pride, and partial views "
            f"are tested in the crucible of Guru-Shishya inquiry before the deeper secret is unlocked."
        ),
        (
            f"**Purvapaksha (Dismantling the Outer Veil of Illusion):** Through sharp dialectical dialogue, {primary_char} exposes the fallacy "
            f"of identifying the immortal Self with the perishable body, senses, breath, or ritualistic ego. The seeker's initial misconception "
            f"dissolves as the Guru points beyond name and form (*Nama-Rupa*)."
        ),
        (
            f"**Drishtanta (The Sacred Experiment & Visual Metaphor):** Centerpiece demonstration of **{metaphor}**. "
            f"{primary_char} and {secondary_char} engage in a tactile, visual contemplation where the subtlest principle of Advaita Vedanta "
            f"is proven directly before the seeker's eyes, bridging the empirical world and the transcendental Witness."
        ),
        (
            f"**Siddhanta (The Climax of Upadesha & Mahavakya Proclamation):** At the dramatic zenith of the 5-minute film, {primary_char} "
            f"raises the hand in Chinmudra and proclaims the canonical Mahavakya: *\"{story['mahavakya_sanskrit']}\"* "
            f"({story['mahavakya_meaning_english']}), striking down the final veil of ignorance (*Avidya*)."
        ),
        (
            f"**Aparoksha Anubhuti (Direct Non-Dual Realization & Cosmic Vision):** The verbal teaching blossoms into immediate, unmediated "
            f"experience (*Aparoksha Jnana*). {secondary_char} abides in motionless Nirvikalpa Samadhi as the microcosmic heart-cave (*Dahara Akasha*) "
            f"and the macrocosmic universe merge into one undivided ocean of *Sat-Chit-Ananda*."
        ),
        (
            f"**Phala Sruti & Shanti (The Eternal Benediction & Living Wisdom):** Returning from deep Samadhi into illumined living liberation "
            f"(*Jivanmukti*), {primary_char} and {secondary_char} chant the canonical {story['veda']} Shanti Mantra in unison, bestowing "
            f"fearlessness (*Abhayam*) and immortal peace upon all who contemplate this Upanishad."
        )
    ]
    return beats[scene_idx]


def build_five_subshots_for_scene(story: dict, scene_idx: int, sc: dict, char_bible: list) -> list:
    """
    Generates 5 distinct, continuous 9-second 16:9 8K 24fps Google Flow / Veo prompts
    (Shot A [00-09s], Shot B [09-18s], Shot C [18-27s], Shot D [27-36s], Shot E [36-45s])
    engineered so Google Flow builds a seamless 45-second scene without repetitive looping.
    """
    sid = story["story_id"]
    sc_num = scene_idx + 1
    setting = story["setting_specifics"]
    metaphor = story["metaphor_highlight"]
    chars = story["characters"]
    c1 = chars[0].split("(")[0].strip()
    c2 = chars[1].split("(")[0].strip() if len(chars) > 1 else "the earnest Vedic disciple"

    # Extract concise visual descriptors from char_bible
    c1_vis = char_bible[0].split(":", 1)[1].strip() if char_bible else "venerable Vedic sage in saffron-ochre cotton dhoti, vibhuti, and Rudraksha"
    c2_vis = char_bible[1].split(":", 1)[1].strip() if len(char_bible) > 1 else "devoted young Vedic seeker in unstitched white cotton dhoti and sacred thread"

    base_veo = sc.get("veo_prompt", "").replace("no text, no subtitles, no modern elements, no borders.", "").strip()
    neg_tail = "8K photorealistic 16:9 widescreen 24fps Arri Alexa 65 prime lens cinema aesthetic, zero modern objects, no text, no subtitles, no watermarks, no borders."

    shot_a_prompt = (
        f"[Shot A | 00s-09s | Wide Anamorphic Establishing Shot] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic cinema shot: "
        f"Sweeping 24mm anamorphic establishing view of {setting}. {base_veo} "
        f"Volumetric golden sunrise rays and fragrant Agnihotra smoke drift slowly across ancient carved stone and banyan roots as {c1} and {c2} "
        f"are framed in the sacred environment. {neg_tail}"
    )

    shot_b_prompt = (
        f"[Shot B | 09s-18s | Medium Tracking Shot on Action & Sacred Gesture] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic medium tracking shot (50mm prime lens): "
        f"Camera glides smoothly at eye level beside {c1} ({c1_vis[:140]}) and {c2} ({c2_vis[:140]}) inside {setting}. "
        f"{c1} raises the right hand in sacred Chinmudra while performing the canonical teaching gesture toward the sacred Homa fire and palm-leaf manuscripts, "
        f"while {c2} leans forward with folded hands in Anjali mudra. Warm flickering brass deepam firelight on natural cotton and Rudraksha textures. {neg_tail}"
    )

    shot_c_prompt = (
        f"[Shot C | 18s-27s | Macro / Extreme Close-Up on Sacred Symbol & Facial Realization] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic macro close-up shot (85mm macro prime lens, shallow depth of field): "
        f"Intimate macro focus on the signature Upanishadic symbol and experiment of {metaphor} illuminated by warm golden oil-lamp and solar rays, "
        f"rack-focusing smoothly to the expressive eyes of {c2} glistening with sudden philosophical awe and spiritual awakening. "
        f"Every grain of sacred Vibhuti ash, copper vessel reflection, Rudraksha bead, and golden dust mote rendered in tactile 8K clarity. {neg_tail}"
    )

    shot_d_prompt = (
        f"[Shot D | 27s-36s | Over-the-Shoulder / Two-Shot Dramatic Samvada Dialogue] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic over-the-shoulder dramatic two-shot: "
        f"Framed over the saffron-draped shoulder of {c1} looking toward {c2} in {setting}, capturing the intense Upanishadic Samvada dialogue. "
        f"As {c1} speaks the immortal Vedic truth, subtle golden pranic light and sacred fire sparks illuminate both faces in balanced chiaroscuro lighting, "
        f"conveying deep emotional stakes and Guru-Shishya transmission. {neg_tail}"
    )

    next_bridge = (
        f"bridging seamlessly into Scene {sc_num + 1}" if sc_num < 7
        else "rising into a timeless, serene final Vedic benediction tableau"
    )
    shot_e_prompt = (
        f"[Shot E | 36s-45s | Slow Crane Ascent & Atmospheric Transition] Continuous 9-second 16:9 widescreen 8K 24fps photorealistic crane ascent shot: "
        f"Camera rises slowly and majestically above {c1} and {c2} in {setting}, looking out over the shimmering sacred river, blooming lotuses, "
        f"and towering banyan canopy bathed in golden-amber light, {next_bridge}. {neg_tail}"
    )

    return [
        {
            "shot_id": f"{sid}_S0{sc_num}_A",
            "shot_code": "Shot A (00s–09s)",
            "time_window": "00s - 09s (9 seconds)",
            "camera_movement": "Wide 24mm Anamorphic Establishing Dolly / Pan across the sacred architectural and natural setting",
            "google_flow_veo_prompt": shot_a_prompt
        },
        {
            "shot_id": f"{sid}_S0{sc_num}_B",
            "shot_code": "Shot B (09s–18s)",
            "time_window": "09s - 18s (9 seconds)",
            "camera_movement": "Medium 50mm Tracking Shot on Guru/Deity/Seeker action, posture, and sacred Mudra gesture",
            "google_flow_veo_prompt": shot_b_prompt
        },
        {
            "shot_id": f"{sid}_S0{sc_num}_C",
            "shot_code": "Shot C (18s–27s)",
            "time_window": "18s - 27s (9 seconds)",
            "camera_movement": "Macro 85mm Close-Up Rack-Focus on the Sacred Symbol, Experiment, Ritual Object & Facial Expression",
            "google_flow_veo_prompt": shot_c_prompt
        },
        {
            "shot_id": f"{sid}_S0{sc_num}_D",
            "shot_code": "Shot D (27s–36s)",
            "time_window": "27s - 36s (9 seconds)",
            "camera_movement": "Over-the-Shoulder / Two-Shot Dramatic Dialogue & Philosophical Realization (Samvada)",
            "google_flow_veo_prompt": shot_d_prompt
        },
        {
            "shot_id": f"{sid}_S0{sc_num}_E",
            "shot_code": "Shot E (36s–45s)",
            "time_window": "36s - 45s (9 seconds)",
            "camera_movement": "Slow Crane Ascent / Atmospheric Horizon Transition bridging into the next narrative beat",
            "google_flow_veo_prompt": shot_e_prompt
        }
    ]


def expand_scene_narration_en(story: dict, scene_idx: int, orig_en: str) -> str:
    """Expands a scene's English narration to ~110-130 words with rich Upanishadic Samvada dialogue."""
    shanti = base_agent1.SHANTI_MANTRAS_BY_VEDA[story["veda"]]
    addon = STAGE_DIALOGUE_EN[scene_idx].format(
        mv_sa=story["mahavakya_sanskrit"],
        mv_en=story["mahavakya_meaning_english"],
        shanti_sa=shanti["sanskrit"],
        shanti_en=shanti["meaning"]
    )
    combined = f"{orig_en.strip()} {addon}"
    return trim_or_pad_to_target(combined, min_words=112, max_words=132, is_tamil=False)


def expand_scene_narration_ta(story: dict, scene_idx: int, orig_ta: str) -> str:
    """Expands a scene's Senthamizh narration to ~110-130 words with classical Tamil commentary & dialogue."""
    shanti = base_agent1.SHANTI_MANTRAS_BY_VEDA[story["veda"]]
    addon = STAGE_DIALOGUE_TA[scene_idx].format(
        mv_ta_trans=story["mahavakya_tamil_translit"],
        mv_ta_mean=story["mahavakya_meaning_tamil"],
        shanti_ta=shanti["tamil"]
    )
    combined = f"{orig_ta.strip()} {addon}"
    return trim_or_pad_to_target(combined, min_words=112, max_words=132, is_tamil=True)


def upgrade_story_record(raw_story: dict) -> dict:
    """
    Upgrades a single Mukhya or Samanya Vedanta story dictionary with:
    - Unabridged Storyline (English & Senthamizh)
    - Character Continuity Bible (for all characters across 35 shots)
    - 7 Expanded 45-second Scenes, each with 5 Google Flow 9s Sub-Shots (Shots A-E)
      and ~110-130 word English and Senthamizh narrations (~850 words per 5-minute film).
    """
    shanti = base_agent1.SHANTI_MANTRAS_BY_VEDA[raw_story["veda"]]
    char_bible = build_character_continuity_bible(raw_story)
    unabridged = build_unabridged_storyline(raw_story)

    upgraded_scenes = []
    for idx, sc in enumerate(raw_story["scenes"]):
        sc_num, dur_win, sc_arc_title = base_agent1.SCENE_TEMPLATE_WINDOWS[idx]
        beat = build_dramatic_beat(raw_story, idx, sc)
        sub_shots = build_five_subshots_for_scene(raw_story, idx, sc, char_bible)
        vo_en = expand_scene_narration_en(raw_story, idx, sc["narration_en"])
        vo_ta = expand_scene_narration_ta(raw_story, idx, sc["narration_ta"])

        upgraded_scenes.append({
            "scene_number": idx + 1,
            "scene_id": f"{raw_story['story_id']}_S0{idx + 1}",
            "scene_title": f"{sc_num} ({dur_win}): {sc_arc_title}",
            "duration_window": dur_win,
            "duration_seconds": 45,
            "narrative_stage": sc_arc_title,
            "dramatic_story_and_dialogue_beat": beat,
            "camera_and_cinematography": sc["camera"],
            "veo_16_9_video_prompt": sc["veo_prompt"],
            "sub_shots": sub_shots,
            "voiceover_english": vo_en,
            "voiceover_english_word_count": len(vo_en.split()),
            "voiceover_tamil": vo_ta,
            "voiceover_tamil_word_count": len(vo_ta.split()),
            "on_screen_subtitle_cue": sc["subtitle_cue"],
            "sound_design_and_sangeetham_cue": sc["sound_cue"]
        })

    # Rebuild YouTube metadata using the upgraded first scene hook
    raw_copy_for_yt = dict(raw_story)
    yt_meta = base_agent1.build_youtube_metadata(raw_copy_for_yt)

    visual_bible = dict(base_agent1.LOCKED_VISUAL_BIBLE_BASE)
    visual_bible["story_specific_setting"] = raw_story["setting_specifics"]
    visual_bible["signature_visual_metaphor"] = raw_story["metaphor_highlight"]
    visual_bible["character_continuity_bible"] = char_bible
    visual_bible["google_flow_35_shot_architecture"] = (
        "7 Narrative Scenes x 5 Continuous 9-Second Sub-Shots (Shot A [00-09s], Shot B [09-18s], "
        "Shot C [18-27s], Shot D [27-36s], Shot E [36-45s]) = 35 Distinct 16:9 8K 24fps Prompts (315 Seconds Total)."
    )

    total_en_words = sum(s["voiceover_english_word_count"] for s in upgraded_scenes)
    total_ta_words = sum(s["voiceover_tamil_word_count"] for s in upgraded_scenes)

    return {
        "story_id": raw_story["story_id"],
        "muktika_number": raw_story["muktika_number"],
        "upanishad_names": {
            "sanskrit": raw_story["upanishad_sanskrit"],
            "iast": raw_story["upanishad_iast"],
            "tamil": raw_story["upanishad_tamil"],
            "english": raw_story["upanishad_english"]
        },
        "associated_veda": raw_story["veda"],
        "category": raw_story["category"],
        "story_title": {
            "english": raw_story["story_title_english"],
            "tamil": raw_story["story_title_tamil"]
        },
        "key_characters": raw_story["characters"],
        "core_mahavakya": {
            "sanskrit_sloka": raw_story["mahavakya_sanskrit"],
            "tamil_transliteration": raw_story["mahavakya_tamil_translit"],
            "meaning_english": raw_story["mahavakya_meaning_english"],
            "meaning_tamil": raw_story["mahavakya_meaning_tamil"]
        },
        "shanti_mantra": shanti,
        "philosophical_and_moral_theme": raw_story["philosophical_theme"],
        "unabridged_storyline": unabridged,
        "youtube_metadata": yt_meta,
        "locked_visual_continuity_bible": visual_bible,
        "total_scenes_count": len(upgraded_scenes),
        "total_sub_shots_count": len(upgraded_scenes) * 5,
        "total_narration_words_english": total_en_words,
        "total_narration_words_tamil": total_ta_words,
        "scenes": upgraded_scenes
    }


def render_upgraded_markdown(story: dict) -> str:
    """Renders the Ultra-Detailed 5-Minute 35-Shot Markdown Screenplay for a story."""
    u = story["upanishad_names"]
    mv = story["core_mahavakya"]
    sm = story["shanti_mantra"]
    yt = story["youtube_metadata"]
    vb = story["locked_visual_continuity_bible"]
    unab = story["unabridged_storyline"]
    chars_md = "\n".join(f"  - {c}" for c in story["key_characters"])
    char_bible_md = "\n".join(f"- {cb}" for cb in vb["character_continuity_bible"])
    tags_md = ", ".join(f"`{t}`" for t in yt["youtube_tags"])

    lines = [
        f"# {story['story_id']} — {u['english']} (Muktika #{story['muktika_number']:03d})",
        f"## {story['story_title']['english']}",
        f"### {story['story_title']['tamil']}",
        "",
        "> **Google Flow 5-Minute (315-Second) 16:9 Widescreen Cinema Master Specification**",
        f"> - **Architecture**: `7 Narrative Scenes` × `5 Continuous 9-Second Sub-Shots (Shots A–E)` = **`35 Distinct 16:9 8K Prompts`**",
        f"> - **Spoken Narration Length**: **`{story['total_narration_words_english']} words (English)`** | **`{story['total_narration_words_tamil']} words (Senthamizh)`**",
        "",
        "---",
        "",
        "## 1. Header & Canonical Metadata",
        "",
        f"- **Story ID**: `{story['story_id']}`",
        f"- **Muktika Canon Number**: `#{story['muktika_number']:03d}` (of 108 Upanishads)",
        f"- **Upanishad Name (Sanskrit)**: {u['sanskrit']}",
        f"- **Upanishad Name (IAST)**: *{u['iast']}*",
        f"- **Upanishad Name (Tamil)**: {u['tamil']}",
        f"- **Upanishad Name (English)**: {u['english']}",
        f"- **Associated Veda**: {story['associated_veda']}",
        f"- **Canonical Category**: `{story['category']}`",
        f"- **Story / Parable Title (English)**: {story['story_title']['english']}",
        f"- **Story / Parable Title (Tamil)**: {story['story_title']['tamil']}",
        f"- **Key Characters / Sages / Deities**:",
        chars_md,
        "",
        "### Core Mahavakya / Upanishadic Verse",
        f"- **Authentic Sanskrit Sloka**:",
        f"  > **{mv['sanskrit_sloka']}**",
        f"- **Tamil Transliteration**:",
        f"  > *{mv['tamil_transliteration']}*",
        f"- **English Meaning**: {mv['meaning_english']}",
        f"- **Tamil Meaning (தமிழ் பொருள்)**: {mv['meaning_tamil']}",
        "",
        "### Vedic Shanti Mantra",
        f"- **Sanskrit**: `{sm['sanskrit']}`",
        f"- **Tamil**: `{sm['tamil']}`",
        f"- **Meaning**: {sm['meaning']}",
        "",
        "### Philosophical & Moral Theme",
        f"{story['philosophical_and_moral_theme']}",
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
        "",
        "### Character Physical, Costume & Lighting Continuity Profiles",
        char_bible_md,
        "",
        "### Global & Story-Specific Visual Continuity Parameters",
        f"- **Aspect Ratio & Cinema Spec**: {vb['aspect_ratio_and_format']}",
        f"- **35-Shot Timing Architecture**: {vb['google_flow_35_shot_architecture']}",
        f"- **Historical Epoch & Setting**: {vb['historical_epoch_and_setting']}",
        f"- **Story-Specific Sacred Setting**: {vb['story_specific_setting']}",
        f"- **Signature Visual Metaphor / Drishtanta**: {vb['signature_visual_metaphor']}",
        f"- **Lighting & Color Palette**: {vb['lighting_and_color_palette']}",
        f"- **Costume & Prop Continuity**: {vb['costume_and_prop_continuity']}",
        f"- **Hard Negative Exclusions**: {vb['hard_negative_exclusions']}",
        f"- **8-Layer Compositing Compatibility**: {vb['8_layer_compositing_note']}",
        "",
        "### YouTube 16:9 Long-Form Metadata Block",
        f"- **16:9 Title (Tamil)**: `{yt['youtube_title_tamil']}`",
        f"- **16:9 Title (English)**: `{yt['youtube_title_english']}`",
        f"- **Opening Hook (Tamil)**: {yt['youtube_hook_tamil']}",
        f"- **Opening Hook (English)**: {yt['youtube_hook_english']}",
        f"- **Description UTF-8 Byte Count**: `{yt['youtube_description_utf8_bytes']} / 5000 bytes`",
        f"- **Tags**: {tags_md}",
        "",
        "```text",
        yt["youtube_description"],
        "```",
        "",
        "---",
        "",
        "## 4. Full 7-Scene / 35-Shot Ultra-Detailed Screenplay Breakdown (00:00 – 05:15)",
        ""
    ]

    for sc in story["scenes"]:
        lines.extend([
            f"### {sc['scene_title']}",
            "",
            f"- **Scene ID**: `{sc['scene_id']}` | **Duration Window**: `{sc['duration_window']}` (`45 seconds` = `5 × 9s Sub-Shots`)",
            f"- **Dramatic Story & Philosophical Dialogue Beat (Upakhyana & Samvada)**:",
            f"  {sc['dramatic_story_and_dialogue_beat']}",
            f"- **Master Scene Camera & Cinematography Summary**: {sc['camera_and_cinematography']}",
            f"- **Master Scene Overview Prompt**: `{sc['veo_16_9_video_prompt']}`",
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
            f"#### Expanded 45-Second Dramatic Narration & Dialogue in English (`{sc['voiceover_english_word_count']} words`)",
            f"> {sc['voiceover_english']}",
            "",
            f"#### Expanded 45-Second Dramatic Narration & Dialogue in Senthamizh — செந்தமிழ் உரைநடை (`{sc['voiceover_tamil_word_count']} words`)",
            f"> {sc['voiceover_tamil']}",
            "",
            f"- **On-Screen Subtitle / Verse Cue (Layer 8 WhisperX / ASS)**:",
            f"  > `{sc['on_screen_subtitle_cue']}`",
            f"- **Sound Design & Sangeetham Score**:",
            f"  > {sc['sound_design_and_sangeetham_cue']}",
            "",
            "---",
            ""
        ])

    return "\n".join(lines)


def main():
    MUKHYA_DIR.mkdir(parents=True, exist_ok=True)
    SAMANYA_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)

    # Remove old stray duplicate file 28_SAMANYA_28_ANNAPURNA_53.md if present so naming is 100% uniform
    old_annapurna = SAMANYA_DIR / "28_SAMANYA_28_ANNAPURNA_53.md"
    if old_annapurna.exists():
        old_annapurna.unlink()

    raw_mukhya_all = (
        base_agent1.MUKHYA_PART1
        + base_agent1.MUKHYA_PART2
        + base_agent1.MUKHYA_PART3
        + base_agent1.MUKHYA_PART4
        + base_agent1.MUKHYA_PART5
    )
    all_samanya_specs = list(base_agent1.SAMANYA_SPECS) + ADDITIONAL_SAMANYA_SPECS
    raw_samanya_all = [base_agent1.expand_samanya_spec_to_story(sp) for sp in all_samanya_specs]

    mukhya_upgraded = []
    for st in raw_mukhya_all:
        upg = upgrade_story_record(st)
        fname = f"{upg['story_id']}_Muktika{upg['muktika_number']:03d}_{base_agent1.slugify(upg['upanishad_names']['english'])}.md"
        fpath = MUKHYA_DIR / fname
        upg["markdown_file_path"] = str(fpath)
        fpath.write_text(render_upgraded_markdown(upg), encoding="utf-8")
        mukhya_upgraded.append(upg)

    samanya_upgraded = []
    for st in raw_samanya_all:
        upg = upgrade_story_record(st)
        fname = f"{upg['story_id']}_Muktika{upg['muktika_number']:03d}_{base_agent1.slugify(upg['upanishad_names']['english'])}.md"
        fpath = SAMANYA_DIR / fname
        upg["markdown_file_path"] = str(fpath)
        fpath.write_text(render_upgraded_markdown(upg), encoding="utf-8")
        samanya_upgraded.append(upg)

    all_stories = mukhya_upgraded + samanya_upgraded
    unique_muktika_nums = sorted(list({s["muktika_number"] for s in all_stories}))

    total_scenes = sum(s["total_scenes_count"] for s in all_stories)
    total_sub_shots = sum(s["total_sub_shots_count"] for s in all_stories)
    total_en_words = sum(s["total_narration_words_english"] for s in all_stories)
    total_ta_words = sum(s["total_narration_words_tamil"] for s in all_stories)

    dataset = {
        "agent": "Agent 4 (Group 4): Mukhya (22 Stories) & Samanya Vedanta (29 Stories) Ultra-Detailed 5-Minute 35-Shot Google Flow Architect",
        "channel": "@guru-kula-desam",
        "aspect_ratio": "16:9 Widescreen Long-Form (00:00 - 05:15 per 7-Scene / 35-Shot Film)",
        "summary_counts": {
            "total_story_documents": len(all_stories),
            "mukhya_upanishad_stories_count": len(mukhya_upgraded),
            "mukhya_distinct_upanishads_count": len({s["muktika_number"] for s in mukhya_upgraded}),
            "samanya_vedanta_stories_count": len(samanya_upgraded),
            "total_7_scene_packages_generated": total_scenes,
            "total_35_sub_shot_veo_prompts_generated": total_sub_shots,
            "total_english_narration_words": total_en_words,
            "total_tamil_narration_words": total_ta_words,
            "avg_english_words_per_story": round(total_en_words / len(all_stories), 1),
            "avg_tamil_words_per_story": round(total_ta_words / len(all_stories), 1),
            "unique_muktika_numbers_covered": unique_muktika_nums
        },
        "mukhya_upanishad_stories": mukhya_upgraded,
        "samanya_vedanta_upanishad_stories": samanya_upgraded
    }

    JSON_OUT.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SUCCESS] Upgraded {len(mukhya_upgraded)} Mukhya Upanishad story .md files in {MUKHYA_DIR}")
    print(f"[SUCCESS] Upgraded {len(samanya_upgraded)} Samanya Vedanta Upanishad story .md files in {SAMANYA_DIR}")
    print(f"[SUCCESS] Updated master JSON dataset at {JSON_OUT}")
    print(f"          Total Stories: {len(all_stories)} (22 Mukhya + 29 Samanya Vedanta)")
    print(f"          Total Scenes:  {total_scenes} (7 per story)")
    print(f"          Total Shots:   {total_sub_shots} (35 9-second Google Flow prompts per story)")
    print(f"          Avg Narration: {dataset['summary_counts']['avg_english_words_per_story']} EN words/film | {dataset['summary_counts']['avg_tamil_words_per_story']} TA words/film")


if __name__ == "__main__":
    main()
