#!/usr/bin/env python3
"""
Agent 1: Mukhya & Samanya Vedanta Upanishads Story & 7-Scene Screenplay Architect
=================================================================================
Generates complete, canonical 7-scene 16:9 YouTube video story documents for:
  1. All 13 Mukhya (Principal) Upanishads (22 distinct narrative stories/parables)
  2. All 24 Samanya Vedanta Upanishads (#11-12, 24-25, 27, 32, 33, 35, 36, 38,
     41, 49, 54, 56, 57, 59, 60, 62, 69, 70, 72, 85, 90, 108 in the Muktika canon;
     plus #102 Brihajjabala cross-reference note)

Outputs:
  - /home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/01_mukhya_upanishads/*.md
  - /home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/02_samanya_vedanta_upanishads/*.md
  - /home/shishyan/GitHub/GuruKulaDesam/data/upanishads/agent1_mukhya_samanya.json
"""

import json
import os
import re
from pathlib import Path

BASE_DIR = Path("/home/shishyan/GitHub/GuruKulaDesam")
MUKHYA_DIR = BASE_DIR / "production" / "upanishad_stories" / "01_mukhya_upanishads"
SAMANYA_DIR = BASE_DIR / "production" / "upanishad_stories" / "02_samanya_vedanta_upanishads"
JSON_OUT = BASE_DIR / "data" / "upanishads" / "agent1_mukhya_samanya.json"

LOCKED_VISUAL_BIBLE_BASE = {
    "aspect_ratio_and_format": "16:9 Widescreen | 8K Photorealistic | 24fps Cinema Master (Arri Alexa 65 Prime Lens Aesthetic)",
    "historical_epoch_and_setting": (
        "Authentic Ancient Bharata Vedic Gurukulam, sacred forest hermitages (Tapovanam) along the "
        "Ganga, Yamuna, and Narmada rivers, and monumental South Indian Dravidian granite temple mandapams."
    ),
    "lighting_and_color_palette": (
        "Golden Brahmamuhurtham sunrise rays, warm sacred Agnihotra homa firelight, brass oil lamps (Thoopam & Dheepam), "
        "and ethereal cosmic indigo starlight during Aparoksha Anubhuti sequences."
    ),
    "costume_and_prop_continuity": (
        "Sages and seekers adorned in authentic hand-spunochre/saffron/unstitched white cotton dhotis and uttariyas, "
        "sacred Vibhuti (three horizontal ash lines) or sandalwood tilaka, Rudraksha malas, darbha grass rings, "
        "copper kamandalus, and etched palm-leaf manuscripts (Olai Chuvadi)."
    ),
    "hard_negative_exclusions": (
        "NO modern clothing, NO eyeglasses, NO wristwatches, NO electric lights, NO plastic or synthetic materials, "
        "NO printed paper books, NO Western architectural arches, NO on-screen text, NO burned-in subtitles, "
        "NO watermarks, NOdecorative borders in the raw AI video generation."
    ),
    "8_layer_compositing_note": (
        "Compatible with Guru Kula Desam v6.0 8-Layer 1080p/4K Pipeline: Layer 1 Base 16:9 Cut, Layer 2 Upward Rainbow Rain (6% center), "
        "Layer 3 Perimeter Mist (15% edge), Layer 4 18 Side Lamps (9L/9R), Layer 5 Top Center Tamil Title Header, "
        "Layer 6 Dual Bottom Temple Thoopam Burners, Layer 7 Channel Avatar Watermark, Layer 8 WhisperX/ASS Synchronized Subtitles."
    )
}

SCENE_TEMPLATE_WINDOWS = [
    ("Scene 1", "00:00 - 00:45", "The Sacred Setting & The Seeker's Question (Upakrama)"),
    ("Scene 2", "00:45 - 01:30", "The Encounter / The Trial of Qualification (Adhikara & Pariksha)"),
    ("Scene 3", "01:30 - 02:15", "The First Teaching / The Outer Layer of Illusion (Purvapaksha)"),
    ("Scene 4", "02:15 - 03:00", "The Deeper Inquiry & Sacred Experiment / Metaphor (Drishtanta)"),
    ("Scene 5", "03:00 - 03:45", "The Climax of Upadesha / The Mahavakya Revelation (Siddhanta)"),
    ("Scene 6", "03:45 - 04:30", "Direct Realization & Cosmic Vision (Aparoksha Anubhuti)"),
    ("Scene 7", "04:30 - 05:15", "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)"),
]


MUKHYA_PART1 = [
    {
        "story_id": "MUKHYA_01_ISHA_01",
        "muktika_number": 1,
        "upanishad_sanskrit": "ईशावास्योपनिषद्",
        "upanishad_iast": "Īśāvāsyopaniṣad",
        "upanishad_tamil": "ஈசாவாஸ்ய உபநிடதம்",
        "upanishad_english": "Isha Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "The Golden Disc of Pushan: The Dying Seeker's Vision of the All-Pervading Lord",
        "story_title_tamil": "பொன்மயமான மூடியைத் திறக்கும் சத்திய தரிசனம்: ஈசாவாஸ்ய உபநிடதக் கதை",
        "characters": [
            "Acharya Vajasasaneya (Vedic Rishi of the Shukla Yajur Veda)",
            "Devavrata (An aging Karma-Yogi householder facing the twilight of life)",
            "Pushan / Surya Narayana (The Golden Solar Deity veiling the Supreme Truth)",
            "Agni Jatavedas (The Sacred Fire invoked to guide the soul along the auspicious path)"
        ],
        "mahavakya_sanskrit": "ईशा वास्यमिदं सर्वं यत्किञ्च जगत्यां जगत् । तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम् ॥",
        "mahavakya_tamil_translit": "ஈஸா வாஸ்யமிதம் ஸர்வம் யத்கிஞ்ச ஜகத்யாம் ஜகத் | தேன த்யக்தேன புஞ்ஜீதா மா க்ருதஃ கஸ்யஸ்வித் தனம் ||",
        "mahavakya_meaning_english": "All this that moves in this moving universe is pervaded and enveloped by the Lord. Enjoy through renunciation; covet not anyone's wealth.",
        "mahavakya_meaning_tamil": "இயங்கும் இப்பிரபஞ்சத்தில் உள்ள அனைத்தும் இறைவனால் சூழப்பட்டுள்ளன. தியாக உணர்வுடன் அவற்றை அனுபவிப்பாயாக; எவருடைய செல்வத்திற்கும் பேராசை கொள்ளாதே.",
        "philosophical_theme": "Synthesis of Karma (Sacred Action) and Vidya (Self-Knowledge); seeing the Divine indwelling every atom and piercing the dazzling golden veil (Hiranmaya Patra) of phenomena at the threshold of death.",
        "setting_specifics": "Vajasasaneya Ashram on the sacred banks of the Sarasvati River at twilight and dawn, with a blazing Agnihotra altar facing the rising golden sun.",
        "metaphor_highlight": "Hiranmaya Patra (The dazzling golden vessel/disc covering the face of Satya, the Supreme Truth).",
        "scenes": [
            {
                "camera": "Slow 35mm dolly push-in across a misty Sarasvati river ghat at Brahmamuhurtham; warm rim-light from clay lamps reflecting off ripples.",
                "veo_prompt": "Cinematic 16:9 widescreen 8K 24fps photorealistic shot of an ancient Vedic hermitage along a misty sacred river at dawn in ancient India. An elderly bearded householder in unstitched white cotton dhoti and Rudraksha beads approaches a serene sage seated beside a glowing Agnihotra fire pit under a towering banyan tree. Golden sunrise rays pierce through sacred smoke, copper kamandalu and palm-leaf manuscripts nearby, no text, no subtitles, no modern elements, no borders.",
                "narration_en": "Along the sacred banks of the Sarasvati, Devavrata—who had spent a hundred years performing selfless Vedic sacrifices—felt his mortal breath growing faint. Approaching Acharya Vajasasaneya before the morning fire, he asked with trembling hands: 'O Master, I have worked without rest, yet death approaches and the dazzling brilliance of this world still blinds my eyes. Who truly owns this universe, and how does a mortal cross beyond sorrow?'",
                "narration_ta": "சரஸ்வதி நதிக்கரையின் புனிதமான வைகறைப் பொழுதில், நூறாண்டு காலம் கர்ம யோகத்தில் ஈடுபட்ட முதியவர் தேவவிரதர், தனது இறுதிக்காலம் நெருங்குவதை உணர்ந்தார். அக்னிஹோத்ர வேள்வித் தீயின் முன் அமர்ந்திருந்த ஆச்சாரிய வாஜசனேயரை அணுகி, 'குருதேவா! வாழ்நாள் முழுவதும் கடமைகளைச் செய்தேன், ஆயினும் மரணத்தின் வாசலில் என் கண்கள் உலகின் மாயை ஒளியால் மறைக்கப்பட்டுள்ளன. இப்பிரபஞ்சத்தின் உண்மையான தலைவன் யார்? மரண பயத்தைக் கடக்கும் வழி யாது?' என்று பணிவுடன் கேட்டார்.",
                "subtitle_cue": "ஈசாவாஸ்ய உபநிடதம்: இப்பிரபஞ்சத்தின் உண்மையான தலைவன் யார்?",
                "sound_cue": "Deep Tanpura drone in Shadjam, gentle Sarasvati river water lapping, soft crackling of sacred Homa fire."
            },
            {
                "camera": "Low-angle medium close-up orbiting 45 degrees around the sage and the seeker; firelight flickering across golden brass vessels and gold coins offered on a wooden tray.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot inside a thatched Vedic gurukulam courtyard. The elderly seeker places a brass tray of ancestral gold coins and harvested grain before the calm Vedic guru wearing saffron uttariya and vibhuti ash marks. The guru gently touches a single grain and points toward the vast sunlit sky and flowing river, warm firelight and natural morning sun, zero modern objects, zero text, zero borders.",
                "narration_en": "Devavrata laid his lifelong savings and ritual vessels at the Guru's feet, thinking renunciation meant abandoning the world in fear. The Acharya smiled gently and tested his understanding: 'If you flee from action out of fear, where will you hide from the Creator? Look upon this grain, this gold, and your own beating heart—do any of them belong to you to hoard, or to cast away in pride?'",
                "narration_ta": "தேவவிரதர் தான் சேர்த்த செல்வங்களையும் வேள்விப் பாத்திரங்களையும் குருவின் திருவடிகளில் வைத்து, உலகைத் துறப்பதே விடுதலை என எண்ணினார். ஆச்சாரியர் புன்னகைத்து அவரைச் சோதித்தார்: 'அச்சத்தினால் கடமைகளைத் துறந்து ஓடினால், இறைவனிடமிருந்து எங்கே ஒளிய முடியும்? இந்த தானியமும், பொன்னும், உன் இதயத் துடிப்பும் உனக்குச் சொந்தமானவையா? அவற்றை என்னுடையது எனப் பற்றிக்கொள்வதும், ஆணவத்தால் வெறுப்பதும் அறியாமையல்லவா?'",
                "subtitle_cue": "ஈஸா வாஸ்யமிதம் ஸர்வம் — அனைத்தும் இறைவனால் சூழப்பட்டுள்ளன.",
                "sound_cue": "Resonant Veena alapana in Raga Bhupalam, subtle temple bell chime."
            },
            {
                "camera": "Split-lighting dramatic tracking shot moving from dark dense forest shadows toward a blindingly bright golden sun reflection on water.",
                "veo_prompt": "16:9 8K photorealistic 24fps cinematic frame showing a symbolic contrast in an ancient Indian forest hermitage: on the left, ascetics sitting in dark shadowy caves; on the right, ritualists surrounded by thick ceremonial smoke and dazzling golden vessels. In the center, the Vedic Acharya raises his hand in Chinmudra under balanced golden light, palm leaves and Rudraksha beads visible, no text, no watermarks, no borders.",
                "narration_en": "The Master revealed the twin traps of illusion: 'Into blinding darkness enter those who worship ignorant action alone; yet into an even greater darkness enter those who delight in dry knowledge while scorning sacred duty! Action purifies the heart, and self-knowledge liberates the soul. By Karma one overcomes mortal decay; by Vidya one tastes eternal immortality.'",
                "narration_ta": "மாயையின் இரு பெரும் வலைகளை குருதேவர் விளக்கினார்: 'அறியாமையுடன் கூடிய வெறும் சடங்குகளை மட்டும் வழிபடுபவர்கள் இருளில் நுழைகிறார்கள்; ஆனால் கடமைகளைப் புறக்கணித்து வெறும் ஏட்டு அறிவில் மட்டும் மயங்குபவர்கள் அதைவிடப் பெரிய இருளில் வீழ்கிறார்கள்! கர்மம் உள்ளத்தைத் தூய்மையாக்குகிறது; ஆத்ம வித்தையோ அழியாத அமிர்த நிலையை அருள்கிறது.'",
                "subtitle_cue": "அவித்யயா ம்ருத்யும் தீர்த்வா வித்யயா அம்ருதமஸ்னுதே!",
                "sound_cue": "Rhythmic Mridangam pulse soft and steady beneath Vedic Shukla Yajur Veda svaras."
            },
            {
                "camera": "Macro focus shifting from a brass water pot reflecting the blazing sun to the wide expanse of the horizon where wind stirs the banyan leaves.",
                "veo_prompt": "Cinematic 8K 24fps 16:9 macro-to-wide rack focus shot in a Vedic ashram. Foreground shows a polished brass Purnakumbha pot filled with sacred water reflecting the blinding golden sun disk cleanly; background reveals wind rustling ancient peepal tree leaves and deer standing completely still by the riverbank. Ethereal golden morning mist, photorealistic textures, no text, no subtitles, no borders.",
                "narration_ta": "பின்னர் குருதேவர் பூர்ணகும்பத்தில் உள்ள நீரில் பிரதிபலிக்கும் சூரியனைக் காட்டினார்: 'அந்தப் பரம்பொருள் அசைவற்றது, ஆயினும் மனதை விட வேகமானது! புலன்களால் அதனை எட்டிப் பிடிக்க முடியாது. அது வெகு தொலைவிலும் உள்ளது, மிக அருகிலும் நம் உள்ளுக்குள்ளும் உள்ளது. எல்லா உயிர்களிலும் தன்னையே காண்பவன், அதன் பின் எவரிடமும் வெறுப்போ மயக்கமோ கொள்வதில்லை.'",
                "narration_en": "Pointing to the sun mirrored in a still brass vessel of sacred water, the Guru demonstrated the paradox of the Atman: 'That One is unmoving, yet swifter than the mind! The senses cannot overtake It, for It already stands ahead. It moves and It moves not; It is far away, and yet It is nearer than your own breath. He who beholds all beings in the Self, and the Self in all beings, never shrinks from anything in sorrow or delusion.'",
                "subtitle_cue": "யஸ்து ஸர்வாணி பூதானி ஆத்மன்யேவானுபஸ்யதி — எல்லா உயிர்களிலும் ஆத்மாவைத் தரிசிப்பவன்.",
                "sound_cue": "Soaring Bansuri flute melody echoing across the river valley, gentle wind through peepal leaves."
            },
            {
                "camera": "Majestic crane rise behind Devavrata and the Guru facing the blazing eastern horizon as the solar orb rises above the Sarasvati waters.",
                "veo_prompt": "Epic 16:9 8K 24fps photorealistic crane shot at sunrise over a sacred Indian river. The dying elderly seeker and the Vedic sage stand with folded hands in Anjali mudra facing a colossal, blazing golden sun disk rising through shimmering golden mist. Sacred Homa flames rise in the foreground, saffron robes glowing in backlight, deeply spiritual atmosphere, no text, no borders.",
                "narration_en": "As Devavrata's final hour dawned and the blazing sun rose over the river, the Guru chanted the supreme prayer of unveiling: 'hiranmayena patrena satyasyapihitam mukham! The face of Truth is covered by a dazzling golden disc. O Pushan, Nourisher of the world, draw aside that blinding golden veil so that I, who am devoted to Truth, may behold the Imperishable Reality!'",
                "narration_ta": "தேவவிரதரின் இறுதி மூச்சு நெருங்கிய வேளையில், கீழ்வானில் உதித்த செங்கதிரோனை நோக்கி குருதேவர் மகா மந்திரத்தை முழங்கினார்: 'ஹிரண்மயேன பாத்ரேண ஸத்யஸ்யாபிஹிதம் முகம்! சத்தியத்தின் திருமுகம் பொன்மயமான ஒளித்தட்டால் மூடப்பட்டுள்ளது. உலகைப் பேணும் சூரிய தேவனே! சத்தியத்தையே தர்மமாகக் கொண்ட நான் மெய்ப்பொருளைத் தரிசிக்கும்படி, அந்தப் பொன் மூடியைத் திறப்பாயாக!'",
                "subtitle_cue": "ஹிரண்மயேன பாத்ரேண ஸத்யஸ்யாபிஹிதம் முகம் — பொன்மயமான மூடியைத் திறப்பாயாக!",
                "sound_cue": "Full-voiced Vedic chanting of 'Hiranmayena Patrena', resonant conch (Shankha) blow and deep temple gong."
            },
            {
                "camera": "Slow 360-degree ethereal push-in into Devavrata's serene eyes as the blinding solar glare parts into a calm, infinite sapphire-and-gold radiance.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 spiritual realization shot. The blinding golden glare of the sun parts like a golden curtain in the sky, revealing a serene, infinite cosmic radiance of soft white-gold light. Below on the river ghat, the elderly seeker sits in Padmasana with a blissful, peaceful smile as his breath merges into the morning breeze and sacred firelight, no text, no overlays, no borders.",
                "narration_en": "In that sacred instant, the dazzling glare of external names and forms parted within Devavrata's consciousness. Beholding the Purusha within the Sun as identical with the Witness within his own heart, he whispered: 'So'ham Asmi—He Who is yonder, that very Purusha am I! Let my vital breath merge into the immortal Wind, and let this body return to ashes. O Agni, lead us by the auspicious path!'",
                "narration_ta": "அந்தத் தெய்வீகக் கணத்தில், புற உலகின் பளபளப்பான மாயைத் திரை தேவவிரதரின் அகக்கண்ணிலிருந்து விலகியது. சூரிய மண்டலத்தின் நடுவே உறையும் புருஷனும் தன் இதயத்தில் ஒளிரும் ஆத்மாவும் ஒன்றே என்பதை நேரடியாக உணர்ந்த அவர், 'ஸோஹம் அஸ்மி — அந்தப் பரம்பொருளே நான்! என் பிராணன் அழியாத வாயுவில் கலக்கட்டும், இவ்வுடல் சாம்பலாகட்டும்; அக்னி தேவனே, எங்களை நல்வழியில் நடத்துவாயாக!' என்று கூறிப் பேரமைதியில் ஆழ்ந்தார்.",
                "subtitle_cue": "ஸோஹம் அஸ்மி — அந்தப் பூரண பரம்பொருளே நான்!",
                "sound_cue": "Ethereal Swarmandal harp glissando, celestial chorus hum, warm crackling fire fading into tranquil stillness."
            },
            {
                "camera": "Wide symmetrical locked-off tableau of the Sarasvati ashram bathed in tranquil golden morning light, crane slowly pulling back over lotus blooms.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic final tableau of a tranquil Vedic gurukulam by a lotus-filled river in golden morning light. Young disciples and the Acharya chant in unison around the sacred fire altar while white swans glide across the shimmering water. Pure ancient Bharata atmosphere, rich natural colors, zero modern elements, zero text, zero borders.",
                "narration_en": "Thus concludes the Isha Upanishad with the timeless mantra of fullness: 'Om Purnamadah Purnamidam—That Supreme Brahman is Whole, and this visible universe is Whole. From the Whole comes forth the Whole; and when the Whole is taken from the Whole, the Whole alone forever remains!'",
                "narration_ta": "இவ்வாறு ஈசாவாஸ்ய உபநிடதம் பூரணத்துவத்தின் சாந்தி மந்திரத்தோடு நிறைவடைகிறது: 'ஓம் பூர்ணமதஃ பூர்ணமிதம் — அந்தப் பரம்பொருளும் பூரணமானது, தோன்றியுள்ள இப்பிரபஞ்சமும் பூரணமானது. பூரணத்திலிருந்து பூரணமே தோன்றியது; பூரணத்திலிருந்து பூரணத்தை எடுத்தாலும், எஞ்சியிருப்பதும் பூரணமே! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!'",
                "subtitle_cue": "ஓம் பூர்ணமதஃ பூர்ணமிதம் பூர்ணாத் பூர்ணமுதச்யதே | ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
                "sound_cue": "Unison Gurukulam Vedic chorus chanting 'Om Purnamadah Purnamidam', fading out with Tanpura and temple bells."
            }
        ]
    },
    {
        "story_id": "MUKHYA_02_KENA_01",
        "muktika_number": 2,
        "upanishad_sanskrit": "केनोपनिषद्",
        "upanishad_iast": "Kenopaniṣad",
        "upanishad_tamil": "கேன உபநிடதம்",
        "upanishad_english": "Kena Upanishad",
        "veda": "Sama Veda",
        "category": "Mukhya",
        "story_title_english": "The Yaksha, the Blade of Grass & Goddess Uma Haimavati: How the Gods Lost Their Pride",
        "story_title_tamil": "ஒற்றைப் புல்லும் உமா ஹைமவதியின் உபதேசமும்: தேவர்களின் ஆணவம் அழிந்த கதை",
        "characters": [
            "Indra (King of the Devas)",
            "Agni Jatavedas (God of Fire, who could not burn a single blade of grass)",
            "Vayu Matarisvan (God of Wind, who could not move a single blade of grass)",
            "The Resplendent Yaksha (Brahman appearing as a mysterious Effulgent Spirit)",
            "Goddess Uma Haimavati (Daughter of the Snowy Himalayas, Personified Brahmavidya)"
        ],
        "mahavakya_sanskrit": "केनेषितं पतति प्रेषितं मनः केन प्राणः प्रथमः प्रैति युक्तः । श्रोत्रस्य श्रोत्रं मनसो मनो यद् वाचो ह वाचम् ॥",
        "mahavakya_tamil_translit": "கேனேஷிதம் பததி ப்ரேஷிதம் மனஃ கேன ப்ராணஃ ப்ரதமஃ ப்ரைதி யுக்தஃ | ஸ்ரோத்ரஸ்ய ஸ்ரோத்ரம் மனஸோ மனோ யத் வாசோ ஹ வாசம் ||",
        "mahavakya_meaning_english": "By Whom willed and directed does the mind speed toward its object? That which is the Ear of the ear, the Mind of the mind, the Speech of speech—know That alone to be Brahman!",
        "mahavakya_meaning_tamil": "யாரால் ஏவப்பட்டு மனம் தன் இலக்கை நோக்கிப் பாய்கிறது? காதுக்குக் காதாகவும், மனதிற்கு மனதாகவும், வாக்கிற்கு வாக்காகவும் விளங்கும் அதுவே பிரம்மம்!",
        "philosophical_theme": "Humility before the Ultimate Source; all cosmic powers (Agni, Vayu, Indra) and human faculties (mind, breath, speech, sight) have no independent power save through Brahman.",
        "setting_specifics": "A grand Sama Veda Gurukulam transitioning into the snow-crowned golden peaks of Mount Himavat (Himalayas) where the Yaksha and Goddess Uma appear.",
        "metaphor_highlight": "A single dry blade of Darbha grass (Trinam) that neither the cosmic Fire can burn nor the cosmic Wind can blow away, and the flash of lightning (Vidyut) on Mount Himavat.",
        "scenes": [
            {
                "camera": "Intimate tracking shot inside a Sama Veda Gurukulam hall with carved granite pillars; morning shafts of light illuminating dust motes.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in an ancient South Indian granite temple mandapam gurukulam. A young brahmachari disciple in white dhoti and sacred thread sits reverently before an elderly Sama Veda Acharya holding a palm-leaf manuscript. Golden morning sunlight streams through pillared corridors, brass oil lamps glowing softly, no modern items, no text, no borders.",
                "narration_en": "In the sacred Sama Veda assembly, a devoted disciple asked the question that opens the Kena Upanishad: 'Kenesitam patati presitam manah—By whose mere wish does the mind fly toward its objects? Who commands the first vital breath to move? Tell me, Master, who is that unseen Director behind the eye and the ear?'",
                "narration_ta": "சாம வேத குருகுல மண்டபத்தில், பணிவுடைய சீடன் ஒருவன் தன் குருவிடம் கேட்டான்: 'கேனேஷிதம் பததி ப்ரேஷிதம் மனஃ — குருதேவா! யாரால் ஏவப்பட்டு நம் மனம் எண்ணங்களை நோக்கிப் பாய்கிறது? முதல் பிராணன் யாரால் இயக்கப்பட்டுத் தன் பணியைச் செய்கிறது? கண்ணுக்குக் கண்ணாகவும் காதுக்குக் காதாகவும் நின்று இயக்கும் அந்த மறைபொருள் யாது?'",
                "subtitle_cue": "கேன உபநிடதம்: மனதையும் பிராணனையும் உள்ளிருந்து இயக்குபவர் யார்?",
                "sound_cue": "Sama Veda melodic chant opening, gentle Tanpura and Veena resonance."
            },
            {
                "camera": "Sweeping crane shot over a celestial Himalayan plateau bathed in golden twilight; Devas celebrating around radiant ceremonial fires.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic scene on a majestic high-altitude Himalayan stone terrace above golden clouds. Ancient Vedic celestial kings (Indra, Agni, Vayu) in traditional royal silk pitambara dhotis and ornate gold mukutas celebrate victory with raised arms. In the distance, a towering, mysterious pillar of serene white-gold light (the Yaksha) appears on a snow-clad ridge, no text, no borders.",
                "narration_en": "To explain how even the greatest powers forget their Source, the Guru recounted the ancient parable of the Devas. Once, Brahman won a great victory for the gods over the forces of darkness. Yet in the intoxication of triumph, Agni, Vayu, and Indra boasted: 'Ours alone is this victory! Ours alone is this glory!' Seeing their pride, Brahman appeared on the horizon as a mysterious, effulgent Yaksha.",
                "narration_ta": "மாபெரும் சக்திகளும் தங்களின் மூலத்தை மறந்து ஆணவம் கொள்வதை விளக்க, குருதேவர் தேவர்களின் புராண நிகழ்வைக் கூறினார். ஒருமுறை அசுரர்களுக்கு எதிரான போரில் பிரம்மத்தின் அருளால் தேவர்கள் வெற்றி பெற்றனர். ஆனால் இந்திரனும் அக்னியும் வாயுவும், 'இந்த வெற்றி எங்களுடையதே! இந்த மகிமை எங்கள் வலிமையாலேயே கிடைத்தது!' என்று ஆணவம் கொண்டனர். அவர்களின் அகந்தையை அழிக்க, பிரம்மம் ஓர் ஒளிமயமான 'யக்ஷ' வடிவத்தில் தோன்றியது.",
                "subtitle_cue": "தேவர்களின் ஆணவத்தை அழிக்க ஒளிமயமான யக்ஷ வடிவில் தோன்றிய பிரம்மம்!",
                "sound_cue": "Majestic Nagaswaram and Tavil fanfare shifting into a mysterious, deep contrabass drone."
            },
            {
                "camera": "Dramatic close-up and low-angle tracking shot of Agni approaching the Yaksha; macro focus on a single delicate blade of dry darbha grass resting on a stone.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 dramatic shot on a rocky Himalayan ridge. The radiant figure of Agni Deva in fiery red-gold traditional silk garments directs intense golden flames from his palms toward a single tiny blade of dry darbha grass resting before a serene luminous spiritual presence. The tiny blade of grass remains completely untouched and green-gold, no text, no subtitles, no borders.",
                "narration_en": "The gods sent Agni first to discover who this radiant stranger was. Agni strode up and declared, 'I am Jatavedas, the all-consuming Fire! I can burn whatever exists on earth!' Silently, the Yaksha placed a single dry blade of grass before him: 'Burn this.' Agni rushed at it with all his cosmic fury—yet he could not even scorch that tiny blade of grass! Ashamed, he returned in silence.",
                "narration_ta": "அந்த ஒளிவடிவம் யார் எனத் தெரிந்துவர தேவர்கள் முதலில் அக்னி தேவனை அனுப்பினர். அக்னி கர்வத்துடன் சென்று, 'நான் ஜாதவேதன்! இவ்வுலகில் உள்ள அனைத்தையும் எரிக்கும் வல்லமை கொண்டவன்!' என்றான். யக்ஷன் அமைதியாக ஒரு சிறிய உலர்ந்த புல்லை அவனது முன்னால் வைத்து, 'இதை எரித்துப் பார்' என்றது. அக்னி தன் முழு ஆற்றலையும் திரட்டிப் பாய்ந்தும், அந்த ஒற்றைப் புல்லைக் கூட எரிக்க முடியாமல் வெட்கத்துடன் திரும்பினான்.",
                "subtitle_cue": "உலகையே எரிக்கும் அக்னியால் அந்த ஒற்றைப் புல்லைக் கூட எரிக்க முடியவில்லை!",
                "sound_cue": "Roaring fire whoosh sound effects suddenly dropping into complete, humbling silence."
            },
            {
                "camera": "Dynamic swirling wind shot as Vayu approaches the blade of grass; leaves and clouds swirl in the background while the single grass blade stands immovable.",
                "veo_prompt": "16:9 8K 24fps photorealistic cinematic shot on a windswept Himalayan peak. Vayu Deva in flowing blue-white silk garments summons a mighty tempest; snow and clouds swirl violently in the sky, yet in the foreground on a flat granite rock, a single delicate blade of darbha grass stands completely still and unmoved before the glowing Yaksha, no text, no watermarks, no borders.",
                "narration_en": "Next went Vayu, Lord of the Tempest. 'I am Matarisvan!' he boasted. 'I can sweep away anything upon the earth!' Again the Yaksha laid down that single blade of grass: 'Blow this away.' Vayu summoned hurricanes that shook the mountains, yet the tiny blade did not quiver by a hair's breadth! Defeated, Vayu returned and told Indra: 'Even we cannot fathom who this Great Being is.'",
                "narration_ta": "அடுத்து வாயு பகவான் விரைந்து சென்று, 'நான் மாதரிஸ்வன்! பூமியில் உள்ள எதனையும் ஊதித் தள்ளும் வல்லமை படைத்தவன்!' என்று முழங்கினான். யக்ஷன் மீண்டும் அந்த ஒற்றைப் புல்லைக் காட்டி, 'இதை அசைத்துப் பார்' என்றது. மலைகளையே உலுக்கும் புயற்காற்றை வாயு வீசியபோதும், அந்தச் சிறு புல் அணுவளவும் அசையவில்லை! தோல்வியுற்ற வாயு திரும்பிச் சென்று, 'அந்த மகா சக்தி யார் என்பதை எங்களால் அறிய முடியவில்லை' என்றான்.",
                "subtitle_cue": "மலைகளை உலுக்கும் வாயுவாலும் அந்தச் சிறு புல்லை அசைக்க முடியவில்லை!",
                "sound_cue": "Howling mountain wind tempest abruptly resolving into a single pure Bansuri note."
            },
            {
                "camera": "Slow reverent crane shot as Indra approaches the spot on Mount Himavat; the Yaksha vanishes and Goddess Uma Haimavati appears in golden splendor.",
                "veo_prompt": "Breathtaking 16:9 8K 24fps photorealistic scene on snow-covered Mount Himavat at sunrise. King Indra stands with bowed head and folded hands in humble devotion. Before him stands Goddess Uma Haimavati, resplendent in golden Kanchipuram silk saree, Rudraksha and gold temple jewelry, radiating serene divine wisdom against sparkling snow peaks, no text, no subtitles, no borders.",
                "narration_en": "When Indra himself hastened toward the Yaksha, the form vanished into thin air! Instead of fleeing in pride, Indra stood in humble contemplation on the snowy heights. There, in the very sky where the Yaksha had stood, appeared a woman of surpassing golden radiance—Uma Haimavati, Daughter of the Himalayas! Indra bowed low and asked: 'O Mother, who was that Effulgent Being?'",
                "narration_ta": "இந்திரன் தானே நேரில் சென்றபோது, அந்த யக்ஷ உருவம் அங்கிருந்து மறைந்தது! ஆனால் இந்திரன் ஆணவமின்றி அங்கேயே பணிவுடன் நின்று தியானித்தான். அப்போது அதே ஆகாயத்தில், இமயமலையின் புதல்வியான அன்னை உமா ஹைமவதி பொன்மயமான பேரொளியுடன் திருக்காட்சி தந்தாள்! இந்திரன் சிரம் தாழ்த்தி வணங்கி, 'தாயே! சற்று முன் இங்கே தோன்றி மறைந்த அந்த ஒளிப்பொருள் யார்?' என்று கேட்டான்.",
                "subtitle_cue": "பொன்மயமான உமா ஹைமவதி தோன்றிப் பிரம்ம தத்துவத்தை உபதேசித்தாள்!",
                "sound_cue": "Celestial Veena and Violin duet in Raga Kalyani, shimmering temple bells."
            },
            {
                "camera": "Close-up of Uma Haimavati's compassionate gaze transitioning to a sudden flash of golden lightning across dark monsoon clouds and the blink of a contemplative eye.",
                "veo_prompt": "16:9 8K 24fps photorealistic cinematic sequence showing Goddess Uma Haimavati blessing Indra with Abhaya mudra on the Himalayan peak, seamlessly illuminating the sky with a brilliant golden flash of lightning across deep indigo clouds. Close-up of a serene human eye blinking in sudden spiritual awakening, photorealistic lighting, no text, no borders.",
                "narration_en": "Goddess Uma spoke the immortal truth: 'Brahmeti ha vavajanat—It was Brahman indeed! Through the victory of Brahman alone did you grow great, O Devas, though you claimed the glory for yourselves!' The Upanishad compares this awakening to a sudden flash of lightning across the sky—or the winking of an eye! In a single instant of grace and humility, the Self reveals Itself.",
                "narration_ta": "அன்னை உமா தேவி அருளினாள்: 'அது பிரம்மமே ஆகும்! பிரம்மத்தின் வெற்றியினாலேயே தேவர்களாகிய நீங்கள் பெருமை பெற்றீர்கள்; ஆனால் மயக்கத்தால் அதனை உங்கள் வெற்றியாக எண்ணினீர்கள்!' இந்தப் பிரம்ம ஞானம் ஆகாயத்தில் திடீரென வெட்டும் மின்னலைப் போன்றது என்றும், கண் இமைக்கும் நேரத்தில் நிகழும் நேரடி அனுபூதி என்றும் உபநிடதம் போற்றுகிறது.",
                "subtitle_cue": "பிரம்மத்தின் வெற்றியினாலேயே நீங்கள் பெருமை பெற்றீர்கள் — உமா தேவியின் உபதேசம்!",
                "sound_cue": "Crisp distant thunder clap and golden harp chime followed by deep meditative Omkaram."
            },
            {
                "camera": "Return to the Sama Veda Gurukulam; wide pull-back shot of the Acharya and disciple seated in silent meditation beside a blooming lotus pond.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic shot of the ancient Sama Veda gurukulam courtyard at full morning light. The Acharya and young disciple sit in peaceful Padmasana meditation near a lotus pond while sacred smoke rises gently from the Homa altar. Timeless Vedic serenity, rich natural textures, zero modern items, zero text, zero borders.",
                "narration_en": "Because Indra approached the Truth first and learned it from Uma, he became supreme among the gods. The Kena Upanishad concludes with the royal foundation of this wisdom: 'Tapo damah karmeti tasya pratistha—Austerity, self-restraint, and selfless work are its firm foundation; the Vedas are its limbs, and Truth is its eternal abode!'",
                "narration_ta": "உமா தேவியிடம் முதன்முதலில் பணிவுடன் சத்தியத்தை உணர்ந்ததால் இந்திரன் தேவர்களில் முதன்மையானான். கேன உபநிடதம் இந்தப் பிரம்ம வித்தையின் அடித்தளத்தை இவ்வாறு நிறைவு செய்கிறது: 'தபோ தமஃ கர்மேதி தஸ்ய ப்ரதிஷ்டா — தவமும், புலனடக்கமும், நிஷ்காமிய கர்மமுமே இந்த ஞானத்திற்குக் கால்கள்; வேதங்களே இதன் அங்கங்கள்; சத்தியமே இதன் நிலையான உறைவிடம்!'",
                "subtitle_cue": "தவமும், புலனடக்கமும், நற்செயலுமே பிரம்ம வித்தையின் அடித்தளம்; சத்தியமே அதன் உறைவிடம்!",
                "sound_cue": "Sama Veda Shanti Mantra 'Om Apyayantu Mamangani' chanted in resonant harmony."
            }
        ]
    },
    {
        "story_id": "MUKHYA_03_KATHA_01",
        "muktika_number": 3,
        "upanishad_sanskrit": "कठोपनिषद्",
        "upanishad_iast": "Kaṭhopaniṣad",
        "upanishad_tamil": "கட உபநிடதம் (பாகம் 1)",
        "upanishad_english": "Katha Upanishad (Part 1)",
        "veda": "Krishna Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "Nachiketa at the House of Death: The Boy Who Refused Kingdoms for Immortality",
        "story_title_tamil": "எமதர்மராஜனின் வாசலில் நசிகேதன்: மரணத்தின் ரகசியத்தைக் கேட்ட சிறுவன்",
        "characters": [
            "Nachiketa (The fearless young Vedic seeker possessed of pure Shraddha/Faith)",
            "Vajashravasa / Gautama (Nachiketa's father performing the Vishvajit sacrifice)",
            "Yama Dharmaraja (The Lord of Death and Supreme Guru of Atma-Vidya)",
            "Yama's Queen / Household Attendants (Who warn Yama of the fasting Brahmana guest)"
        ],
        "mahavakya_sanskrit": "श्रेयश्च प्रेयश्च मनुष्यमेतः तौ सम्परीत्य विविनक्ति धीरः । श्रेयो हि धीरोऽभिप्रेयसो वृणीते ॥",
        "mahavakya_tamil_translit": "ஸ்ரேயஸ்ச ப்ரேயஸ்ச மனுஷ்யமேதஃ தௌ ஸம்பரீத்ய விவினக்தி தீரஃ | ஸ்ரேயோ ஹி தீரோऽபிப்ரேயஸோ வ்ருணீதே ||",
        "mahavakya_meaning_english": "Both the Good (Shreyas) and the Pleasant (Preyas) approach a mortal. The wise one examines both and chooses the Eternal Good over fleeting pleasure.",
        "mahavakya_meaning_tamil": "நன்மையும் (ஸ்ரேயஸ்) இன்பமும் (ப்ரேயஸ்) மனிதனை வந்தடைகின்றன. அறிவுடைய தீரன் அவ்விரண்டையும் ஆராய்ந்து, நிலையற்ற இன்பத்தை விடுத்து நிலையான ஆத்ம நன்மையையே தேர்ந்தெடுக்கிறான்.",
        "philosophical_theme": "Unshakeable Shraddha (Faith), Vairagya (Dispassion toward worldly wealth and longevity), and choosing Shreyas (Spiritual Liberation) over Preyas (Sensory Pleasure).",
        "setting_specifics": "Vajashravasa's grand Yajnashala with aged barren cows, transitioning to the solemn, monumental black-granite portals of Vaivasvata Yama's abode.",
        "metaphor_highlight": "Peetodakaagdha-dugdha (Aged cows that have drunk their last water and eaten their last grass), and Shreyas vs. Preyas (The two diverging paths of liberation and pleasure).",
        "scenes": [
            {
                "camera": "Wide tracking shot across a grand Vedic Yajnashala filled with smoke and priests; camera pans to weak, aged cows being led toward the dakshina gate.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene at an ancient Vedic Vishvajit sacrifice in a forest clearing. Priests chant beside blazing brick fire altars while a wealthy sage (Vajashravasa) gives away frail, elderly white cows as ritual gifts. Standing in the foreground, a bright-eyed twelve-year-old Vedic boy (Nachiketa) in white dhoti and sacred thread watches with deep concern and pure devotion, no text, no borders.",
                "narration_en": "Desiring heaven, the sage Vajashravasa performed the Vishvajit sacrifice, where a giver must offer all his true wealth. Yet as young Nachiketa watched the cows being led forward as gifts to the priests, his heart was pierced with sorrow—for they were old, barren cows that had drunk their last water and yielded their last milk. Pure faith—Shraddha—entered the boy's heart.",
                "narration_ta": "விஸ்வஜித் என்னும் மாபெரும் யாகத்தைச் செய்த வாஜஸ்ரவஸர், தனது செல்வங்கள் அனைத்தையும் தானமாக வழங்கத் தொடங்கினார். ஆனால் தட்சிணையாக வழங்கப்பட்ட பசுக்களோ, புல்லும் உண்ண முடியாத, பாலும் சுரக்காத முதிய பசுக்களாக இருந்தன! அதைக் கண்ட அவரது புதல்வனான பாலகன் நசிகேதனின் இதயத்தில் 'ஸ்ரத்தை' என்னும் சத்திய உணர்வு பொங்கியெழுந்தது.",
                "subtitle_cue": "கட உபநிடதம்: நசிகேதனின் இதயத்தில் எழுந்த தூய சத்திய உணர்வு (ஸ்ரத்தை)!",
                "sound_cue": "Solemn Krishna Yajur Veda chanting, crackling sacrificial fire, distant lowing of cattle."
            },
            {
                "camera": "Medium two-shot pushing in on Nachiketa standing calmly before his angry father beside the sacrificial fire.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 dramatic medium shot inside a Vedic yajnashala. The young boy Nachiketa stands with folded hands before his stern, bearded father Vajashravasa, who points his hand in sudden anger while flames flare in the Homa pit behind them. Warm firelight and dramatic shadows, authentic ancient Indian attire, zero modern items, zero text, zero borders.",
                "narration_en": "Wishing to save his father from the sin of an insincere offering, Nachiketa stepped forward and asked: 'Father, since you are giving away all you possess, to whom will you give me?' He asked a second time, and a third! Blinded by anger, Vajashravasa cried out: 'Mrityave tva dadami—Unto Death, to Yama, I give you!' Without a trace of fear, Nachiketa bowed to fulfill his father's word.",
                "narration_ta": "தந்தை தகுதியற்ற தானம் செய்து பாவத்திற்கு ஆளாகக் கூடாதே என்ற பரிவோடு நசிகேதன், 'தந்தையே! என்னையும் ஒரு பொருளாகக் கருதி யாருக்குத் தானமாகக் கொடுக்கப் போகிறீர்கள்?' என்று இரண்டு மூன்று முறை கேட்டான். சினம் கொண்ட தந்தை, 'உன்னை எமனுக்குக் கொடுக்கிறேன்!' என்று கூறிவிட்டார். தந்தையின் வாக்கைக் காப்பாற்ற சிறிதும் அச்சமின்றி எமலோகத்திற்குப் புறப்பட்டான் நசிகேதன்.",
                "subtitle_cue": "'தந்தையே! என்னை யாருக்குக் கொடுப்பீர்கள்?' — 'உன்னை எமனுக்குக் கொடுக்கிறேன்!'",
                "sound_cue": "Dramatic Pakhawaj drum roll followed by a resolute, calm Veena chord."
            },
            {
                "camera": "Atmospheric wide crane shot of Nachiketa sitting in meditation for three days and nights on the colossal carved black-granite threshold of Yama's palace.",
                "veo_prompt": "16:9 8K 24fps photorealistic cinematic wide shot of the monumental black-granite gateway of Yama Dharmaraja's palace shrouded in twilight mist and glowing brass torches. Young Nachiketa sits motionless in Padmasana on the stone steps for three nights without food or water, radiating a soft golden aura of austerity while Lord Yama approaches in majestic dark-gold royal robes, no text, no borders.",
                "narration_en": "Arriving at the threshold of Death, Nachiketa found that Lord Yama was away. For three days and three nights, the young boy sat fasting in serene meditation at the gates of Yamaloka. When Yama returned and saw a Brahmana guest waiting unhonored, he bowed to the boy and said: 'O revered guest, because you waited three nights at my door without food, choose three boons—one for each night!'",
                "narration_ta": "எமதர்மராஜனின் மாளிகையை அடைந்த நசிகேதன், எமன் வெளியில் சென்றிருந்ததால் மூன்று பகலும் மூன்று இரவும் உணவும் நீருமின்றி வாசலிலேயே தியானத்தில் அமர்ந்திருந்தான். திரும்பி வந்த எமதர்மன், விருந்தினனான பிரம்மச்சாரி மூன்று இரவுகள் பட்டினியாய் இருந்ததைக் கண்டு பதறிப்போய் வணங்கி, 'குழந்தாய்! மூன்று இரவுகள் என் வாசலில் காத்திருந்ததற்காக, மூன்று வரங்களைக் கேள்!' என்றார்.",
                "subtitle_cue": "மூன்று இரவுகள் உணவின்றி தவம் இருந்த நசிகேதனுக்கு எமதர்மன் அளித்த மூன்று வரங்கள்!",
                "sound_cue": "Deep resonant conch shell and low temple gong echoing across a vast stone hall."
            },
            {
                "camera": "Medium shot of Yama seated on his dharma-throne blessing Nachiketa with golden sacred fire in a copper kunda between them.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot inside Yama's grand pillared stone hall. Lord Yama, dignified and compassionate in dark silk dhoti and golden crown, blesses young Nachiketa beside a glowing three-tiered brick fire altar (Nachiketa Agni). Golden sparks rise peacefully, authentic Vedic aesthetic, no text, no subtitles, no borders.",
                "narration_en": "For his first boon, Nachiketa asked only for his father's peace of mind and forgiveness when he returned home. For his second boon, he asked to learn the sacred celestial Fire-sacrifice that leads to immortality in heaven. Pleased by the boy's photographic memory and devotion, Yama granted both and blessed the sacred altar forever with the boy's own name: the Nachiketa Fire!",
                "narration_ta": "முதல் வரமாக, தன் தந்தையின் சினம் தணிந்து அமைதி பெற வேண்டும் என்றும், தான் திரும்பிச் செல்லும்போது அவர் தன்னை அன்புடன் ஏற்க வேண்டும் என்றும் கேட்டான் நசிகேதன். இரண்டாவது வரமாக, சுவர்க்க லோகத்து அமரத்துவத்தைத் தரும் அக்னி வித்தையைக் கேட்டான். சிறுவனின் கூர்மதியைக் கண்டு மகிழ்ந்த எமதர்மன், அந்த வேள்வித் தீக்கு 'நாசிகேத அக்னி' என்றே பெயர் சூட்டி ஆசீர்வதித்தார்.",
                "subtitle_cue": "முதல் வரம் தந்தையின் மன அமைதி; இரண்டாம் வரம் நாசிகேத அக்னி வித்தை!",
                "sound_cue": "Warm uplifting Bansuri and Veena harmony with sacred fire crackle."
            },
            {
                "camera": "Tight dramatic close-up of Nachiketa looking straight into the eyes of Death; cut to Yama conjuring visions of golden chariots, elephants, and vast kingdoms.",
                "veo_prompt": "16:9 8K 24fps photorealistic shot inside the hall of Yama. Young Nachiketa looks with unwavering clarity at Lord Yama. Around them, shimmering golden visions of royal chariots, caparisoned elephants, heaps of gold coins, and celestial musicians appear as a test of temptation, yet the boy keeps his hands folded in calm refusal, no text, no borders.",
                "narration_en": "Then came the third boon. Nachiketa asked the ultimate question: 'When a man dies, this doubt arises: some say he still exists, and some say he exists not. Teach me this truth, O Yama!' Yama tested him fiercely: 'Even the gods doubted this of old! Ask instead for sons and grandsons living a hundred years, herds of cattle, elephants, gold, horses, and empire over the whole earth—but do not ask me of Death!'",
                "narration_ta": "மூன்றாவது வரத்தில் நசிகேதன் கேட்டான்: 'மனிதன் இறந்த பிறகு ஆத்மா இருக்கிறதா இல்லையா என்ற ஐயம் நிலவுகிறது; மரணத்திற்குப் பின் உள்ள அந்த உண்மையை எனக்கு உபதேசியுங்கள்!' எமதர்மன் அவனைச் சோதிக்க எண்ணி, 'நூறாண்டு வாழும் புதல்வர்கள், யானைகள், குதிரைகள், பொன், பூமி முழுவதையும் ஆளும் சாம்ராஜ்யம், தேவலோக போகங்கள் அனைத்தையும் தருகிறேன்; ஆனால் மரண ரகசியத்தை மட்டும் கேட்காதே!' என்றார்.",
                "subtitle_cue": "சாம்ராஜ்யங்களையும் தேவலோக போகங்களையும் தருகிறேன்; மரண ரகசியத்தை மட்டும் கேட்காதே!",
                "sound_cue": "Rich orchestral Mridangam and Vina crescendo building tension, then pausing on a single high note."
            },
            {
                "camera": "Slow dolly push-in on Nachiketa standing tall as the illusory golden treasures dissolve into mist around him.",
                "veo_prompt": "Cinematic 8K 24fps 16:9 medium close-up of young Nachiketa standing serene and unshakeable as the illusory visions of gold and chariots dissolve into thin golden mist. His face glows with spiritual resolve and Vairagya while Lord Yama smiles with profound respect and joy at finding a true disciple, no text, no subtitles, no borders.",
                "narration_en": "Nachiketa uttered the roar of supreme renunciation: 'Svobhava martyasya yadantakaitat—O Death, all these pleasures last only until tomorrow, and they wear out the vigor of all the senses! Even the longest life is but a fleeting moment. Keep your horses, keep your dances and songs! What mortal who has met the Undying would delight in mere wealth? Tell me that Supreme Secret alone!'",
                "narration_ta": "நசிகேதன் சிங்கமென முழங்கினான்: 'எமதர்மராஜனே! இன்பங்கள் அனைத்தும் நாளை அழிந்துபோகக் கூடியவை; அவை புலன்களின் வலிமையை உருக்கிவிடுபவை! மிக நீண்ட ஆயுளும் கூட ஒரு கணப்பொழுதே. உமது தேர்களும் நாட்டியமும் கீதமும் உமக்கே இருக்கட்டும்! செல்வத்தால் மனிதனைத் திருப்திப்படுத்த முடியாது. எனக்கு அந்தப் பரம ரகசியத்தை மட்டுமே அருளுங்கள்!'",
                "subtitle_cue": "நாளை அழியும் சிற்றின்பங்கள் வேண்டாம்; அழியாத ஆத்ம ஞானத்தையே அருளுங்கள்!",
                "sound_cue": "Powerful Tanpura resonance and a triumphant, pure flute melody in Raga Hindolam."
            },
            {
                "camera": "Wide symmetrical shot of Yama stepping down from his throne to embrace and seat Nachiketa beside him as an equal seeker of Brahmavidya.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic shot of Lord Yama placing a blessing hand on the head of young Nachiketa seated beside the sacred Nachiketa fire altar. Warm golden light fills the ancient stone hall, symbolizing the victory of Shreyas (eternal wisdom) over Preyas (worldly pleasure), no modern objects, no text, no borders.",
                "narration_en": "Overjoyed to find a disciple of such diamond-like discrimination, Lord Yama proclaimed: 'Shreyascha preyascha manushyametah—Both the Eternal Good and the Fleeting Pleasant approach every human being. The fool chooses pleasure for the sake of greed; the wise one chooses the Eternal Good! You, O Nachiketa, have cast aside all desires. Now hear from me the immortal truth of the Atman!'",
                "narration_ta": "வைரத்தைப் போன்ற உறுதி கொண்ட சீடனைக் கண்டு மகிழ்ந்த எமதர்மன் போற்றினார்: 'ஸ்ரேயஸ் என்னும் ஆத்ம நன்மையும், ப்ரேயஸ் என்னும் உலக இன்பமும் ஒவ்வொரு மனிதனையும் அணுகுகின்றன. அறிவிலி பேராசையால் இன்பத்தைத் தேர்ந்தெடுக்கிறான்; தீரனோ ஆத்ம நன்மையையே தேர்ந்தெடுக்கிறான்! நசிகேதா, நீ ஆசைகளை உதறித் தள்ளிவிட்டாய்; இதோ உனக்கு ஆத்ம தத்துவத்தை உபதேசிக்கிறேன்!'",
                "subtitle_cue": "ஸ்ரேயஸ்ச ப்ரேயஸ்ச — தீரன் நிலையற்ற இன்பத்தை விடுத்து ஆத்ம நன்மையையே தேர்ந்தெடுக்கிறான்!",
                "sound_cue": "Full Vedic Shanti invocation 'Om Saha Navavatu' chanted by Guru and Shishya in unison."
            }
        ]
    },
    {
        "story_id": "MUKHYA_04_KATHA_02",
        "muktika_number": 3,
        "upanishad_sanskrit": "कठोपनिषद्",
        "upanishad_iast": "Kaṭhopaniṣad",
        "upanishad_tamil": "கட உபநிடதம் (பாகம் 2)",
        "upanishad_english": "Katha Upanishad (Part 2)",
        "veda": "Krishna Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "The Chariot of the Self & The Razor's Edge: Yama's Supreme Teaching to Nachiketa",
        "story_title_tamil": "ரத உருவகமும் கத்தி முனைப் பாதையும்: நசிகேதனுக்கு எமதர்மன் அருளிய ஆத்ம உபதேசம்",
        "characters": [
            "Yama Dharmaraja (The Supreme Teacher of the Immortal Atman)",
            "Nachiketa (The awakened young seeker receiving the Chariot Allegory and Ashvattha teaching)",
            "The Charioteer & Chariot Lord (Visual allegory of Buddhi/Intellect and Atman/Self)"
        ],
        "mahavakya_sanskrit": "उत्तिष्ठत जाग्रत प्राप्य वरान्निबोधत । क्षुरस्य धारा निशिता दुरत्यया दुर्गं पथस्तत्कवयो वदन्ति ॥",
        "mahavakya_tamil_translit": "உத்திஷ்டத ஜாக்ரத ப்ராப்ய வரான் நிபோதத | க்ஷுரஸ்ய தாரா நிஸிதா துரத்யயா துர்கம் பதஸ்தத் கவயோ வதந்தி ||",
        "mahavakya_meaning_english": "Arise! Awake! Having approached the great illumined teachers, realize that Truth! Like the sharp edge of a razor is that path, difficult to cross and hard to tread, say the wise sages.",
        "mahavakya_meaning_tamil": "எழுந்திருங்கள்! விழித்துக்கொள்ளுங்கள்! சிறந்த ஞானிகளை அணுகி மெய்ப்பொருளை உணருங்கள்! கூர்மையான கத்தியின் முனை மேல் நடப்பது போல் அப்பாதை கடப்பதற்கு அரியது என்று முனிவர்கள் கூறுகின்றனர்.",
        "philosophical_theme": "The Unborn, Undying Atman (Na Jayate Mriyate Va), the Ratha Kalpana (Chariot Allegory of Body, Senses, Mind, Intellect, and Self), and the Inverted Cosmic Banyan Tree (Urdhvamulo Avakshakhah).",
        "setting_specifics": "The inner sanctum of Yama's wisdom hall opening onto a cosmic vision of a golden Vedic chariot and an inverted luminous Ashvattha tree.",
        "metaphor_highlight": "Ratha Kalpana (Body = Chariot, Senses = Horses, Mind = Reins, Intellect = Charioteer, Atman = Lord of the Chariot), Razor's Edge (Kshurasya Dhara), and the Inverted Ashvattha Tree.",
        "scenes": [
            {
                "camera": "Slow circular dolly shot around Yama and Nachiketa seated beside the sacred fire; golden light illuminating Nachiketa's serene face.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic shot inside a sacred ancient stone mandapam. Lord Yama in majestic dark-gold silk attire instructs young Nachiketa beside a glowing sacred fire pit. Behind them, subtle golden light forms the silhouette of an eternal, unchanging lotus in the sky, warm volumetric lighting, no modern items, no text, no borders.",
                "narration_en": "Seated before young Nachiketa, Lord Yama unveiled the immortal nature of the Self: 'Na jayate mriyate va vipashchin—The knowing Self is never born, nor does It ever die! It sprang from nothing, and nothing sprang from It. Unborn, eternal, everlasting, and ancient, It is never slain when this mortal body is slain!'",
                "narration_ta": "நசிகேதனின் முன் அமர்ந்த எமதர்மராஜன் ஆத்மாவின் அழிவற்ற இயல்பை உபதேசித்தார்: 'ந ஜாயதே ம்ரியதே வா விபஸ்சின் — பேரறிவுப் பொருளான ஆத்மா பிறப்பதுமில்லை, இறப்பதுமில்லை! அது எதிலிருந்தும் தோன்றவில்லை, அதிலிருந்து எதுவும் புதிதாகத் தோன்றவுமில்லை. பிறப்பற்றதும், நித்தியமானதும், பழமையானதுமான அந்த ஆத்மா, உடல் கொல்லப்படும்போது கொல்லப்படுவதில்லை!'",
                "subtitle_cue": "ந ஜாயதே ம்ரியதே வா — ஆத்மா பிறப்பதுமில்லை, உடல் அழியும்போது அழிவதுமில்லை!",
                "sound_cue": "Deep resonant Rudra Veena melody in Raga Todi, steady Tanpura drone."
            },
            {
                "camera": "Macro close-up of a tiny mustard seed on Nachiketa's palm, pulling back to a vast starry cosmos reflected in the sacred water pot.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 macro-to-wide shot. Close-up of young Nachiketa's palm holding a tiny golden mustard seed beside a glowing oil lamp; camera pulls back to reveal the vast starry night sky reflected inside a copper Purnakumbha water vessel and glowing softly within the boy's chest cave (Hridaya Guha), no text, no borders.",
                "narration_en": "'Anoraniyan mahato mahiyan—Smaller than the smallest atom, yet greater than the greatest cosmos, the Atman is hidden in the secret cave of the heart of every living creature! One who has become free from selfish desire and grief beholds that glory of the Self through the tranquil purity of the senses and mind.'",
                "narration_ta": "'அணோரணீயான் மஹதோ மஹீயான் — அணுவிற்கும் அணுவாகவும், மகத்தான பிரபஞ்சத்திற்கும் மகத்தானதாகவும் விளங்கும் ஆத்மா, ஒவ்வொரு உயிரின் இதயக் குகையிலும் உறைந்துள்ளது! ஆசைகளிலிருந்து விடுபட்டு, புலன்களும் மனமும் தெளிந்தவனே, துக்கமற்ற நிலையில் அந்த ஆத்ம மகிமையை நேரடியாகத் தரிசிக்கிறான்.'",
                "subtitle_cue": "அணோரணீயான் மஹதோ மஹீயான் — அணுவிற்கும் அணுவாய், பிரபஞ்சத்திற்கும் பெரிதாய் உறையும் ஆத்மா!",
                "sound_cue": "Delicate Jalatharangam water-bowl chimes blending with deep cosmic Bansuri notes."
            },
            {
                "camera": "Epic tracking shot alongside a carved golden Vedic wooden chariot pulled by five spirited white horses across a sunlit plain.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic tracking shot of a magnificent ancient Indian carved wooden chariot pulled by five spirited white horses along a golden sunlit forest path. A wise charioteer in saffron turban holds taut braided reins with focused calm, while a serene royal passenger sits effortlessly in the rear pavilion of the chariot, no text, no subtitles, no borders.",
                "narration_en": "Then Yama gave the immortal Chariot Allegory—the Ratha Kalpana: 'Know the Atman as the Lord seated within the chariot, and the body itself as the chariot! Know the awakened Intellect—Buddhi—as the charioteer, and the Mind as the reins. The five Senses, say the wise, are the five horses, and the objects of the world are the roads they travel!'",
                "narration_ta": "அடுத்து உலகப் புகழ்பெற்ற 'ரத கல்பனை' என்னும் தேர் உருவகத்தை எமதர்மன் அருளினார்: 'இவ்வுடம்பையே தேராக அறிந்துகொள்; ஆத்மாவே அத்தேரில் வீற்றிருக்கும் தலைவன்! புத்தியே தேரைச் செலுத்தும் சாரதி; மனமே கடிவாளம். ஐம்புலன்களே அத்தேரில் பூட்டப்பட்ட ஐந்து குதிரைகள்; புலன் நுகர் பொருட்களே அக்குதிரைகள் ஓடும் வீதிகள்!'",
                "subtitle_cue": "உடம்பே தேர், ஆத்மாவே தலைவன், புத்தியே சாரதி, மனமே கடிவாளம், புலன்களே குதிரைகள்!",
                "sound_cue": "Rhythmic galloping Mridangam talas synchronized with energetic Veena strumming."
            },
            {
                "camera": "Contrast sequence: wild horses pulling a chariot toward a cliff edge, transitioning to the calm charioteer steering steadily toward a tranquil river crossing.",
                "veo_prompt": "16:9 8K 24fps photorealistic cinematic shot showing the Vedic charioteer holding the reins with steady mastery as the five white horses glide smoothly in harmony toward a serene, glowing golden lotus lake at sunrise. Warm volumetric morning mist, rich dust particles in golden light, no modern objects, no text, no borders.",
                "narration_en": "'He who lacks discrimination and whose mind is ever unbridled—his senses become unruly like vicious horses of a bad charioteer; he never reaches the goal, but wanders back into Samsara. Yet he who has keen discrimination and holds the reins of the mind firm—his senses are gentle horses, and he reaches that Supreme Abode of Vishnu from which he is never born again!'",
                "narration_ta": "'எவனிடம் விவேகம் இல்லையோ, எவனது மனமாகிய கடிவாளம் கட்டுப்பாட்டில் இல்லையோ, அவனது புலன்கள் முரட்டுக் குதிரைகளைப் போல் அவனைப் பிறவிப் பெருங்கடலில் தள்ளுகின்றன. ஆனால் விவேகமுடைய புத்தியால் மனக்கடிவாளத்தை உறுதியுடன் பிடிப்பவனின் புலன்கள் நற்குதிரைகளாகி, மீண்டும் பிறவாத பரந்தாமனான விஷ்ணுவின் மேலான பதத்தை அடைவிக்கின்றன!'",
                "subtitle_cue": "விவேகமுடைய புத்தியால் மனக்கடிவாளத்தை உறுதியாகப் பிடிப்பவனே பரமபதத்தை அடைகிறான்!",
                "sound_cue": "Turbulent percussion resolving into a majestic, peaceful Raga Shanmukhapriya flute melody."
            },
            {
                "camera": "Dramatic low-angle crane shot of a glowing razor-sharp sword edge bridge over a misty chasm, leading to a radiant temple peak.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 symbolic spiritual shot in the Himalayas. Young Nachiketa and the Vedic sages look upward toward a narrow, luminous mountain ridge gleaming like a polished silver razor's edge amidst golden clouds, leading to a radiant sun-crowned peak. Inspiring, awe-inspiring atmosphere, no text, no subtitles, no borders.",
                "narration_en": "Here rings the thunderous clarion call of the Katha Upanishad to all humanity: 'Uttishthata jagrata prapya varan nibodhata! Arise! Awake! Approach the illumined Masters and realize the Truth! For the sages declare that this path is narrow and difficult to tread, like walking upon the sharp edge of a razor!'",
                "narration_ta": "மனித குலம் முழுவதற்கும் கட உபநிடதம் விடுக்கும் சிம்ம கர்ஜனை இதோ ஒலிக்கிறது: 'உத்திஷ்டத ஜாக்ரத ப்ராப்ய வரான் நிபோதத! எழுந்திருங்கள்! விழித்துக்கொள்ளுங்கள்! சிறந்த ஞானிகளை அணுகிப் பரம்பொருளை உணருங்கள்! கூர்மையான கத்தியின் முனை மேல் நடப்பது போல் அப்பாதை கடப்பதற்கு அரியது என்று ஞானிகள் கூறுகின்றனர்!'",
                "subtitle_cue": "உத்திஷ்டத ஜாக்ரத ப்ராப்ய வரான் நிபோதத — எழுந்திருங்கள்! விழித்துக்கொள்ளுங்கள்!",
                "sound_cue": "Resonant Shankha (conch) blast and uplifting chorus chanting 'Uttishthata Jagrata'."
            },
            {
                "camera": "Vertical tilt-up revealing a colossal cosmic Banyan tree with roots shining in the heavens above and branches cascading downward into the material world.",
                "veo_prompt": "16:9 8K 24fps photorealistic cosmic vision of the eternal Ashvattha tree (Urdhvamulo Avakshakhah): its luminous golden roots anchored high in the starry heavens above, and its branches and aerial roots hanging downward toward a serene ancient Indian river below. Nachiketa meditates in Padmasana with a thumb-sized golden light (Angushtha-matra Purusha) glowing in his heart, no text, no borders.",
                "narration_en": "Finally, Yama revealed the Cosmic Ashvattha Tree whose roots are above in Brahman and whose branches spread below as this universe. And within the heart sits the Purusha, of the measure of a thumb—Angushtha-matra—like a smokeless flame! Drawing that inner Self delicately from the body, just as one draws the tender pith from a reed of Munja grass, Nachiketa realized his own immortality.",
                "narration_ta": "இறுதியாக, மேலே பிரம்மத்தில் வேர்களையும் கீழே பிரபஞ்சமாகக் கிளைகளையும் கொண்ட சம்சார அஸ்வத்த மரத்தின் ரகசியத்தை எமதர்மன் விளக்கினார். இதயக் குகையில் கட்டைவிரல் அளவினனாய் (அங்குஷ்ட மாத்ர புருஷன்), புகையற்ற ஜோதியாய் உறையும் ஆத்மாவை, முஞ்சைப் புல்லிலிருந்து அதன் உட்குருத்தை மென்மையாகப் பிரித்தெடுப்பது போல் உடலிலிருந்து வேறாகப் பிரித்துணர்ந்தான் நசிகேதன்.",
                "subtitle_cue": "முஞ்சைப் புல்லிலிருந்து உட்குருத்தைப் பிரிப்பது போல், உடலிலிருந்து ஆத்மாவைப் பிரித்துணர்வாயாக!",
                "sound_cue": "Ethereal Swarmandal, deep Tanpura, and serene Bansuri sustained note."
            },
            {
                "camera": "Warm sunlit wide shot of Nachiketa returning to his father's ashram, bowing at Vajashravasa's feet while the whole Gurukulam rejoices.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic shot of an ancient Indian forest ashram in golden morning light. Young Nachiketa, radiating divine peace and wisdom, bows at the feet of his overjoyed father Vajashravasa beside the sacred fire altar. Sages and disciples look on with reverence, lotus flowers blooming in the foreground, no text, no borders.",
                "narration_en": "Having received this supreme Brahmavidya and the whole discipline of Yoga from Death himself, Nachiketa became free from all impurity and mortality, and attained Brahman. Returning to his father's hermitage in radiant peace, he left this eternal assurance: whoever thus knows the inner Self becomes forever free and immortal!",
                "narration_ta": "எமதர்மராஜனிடமிருந்து இந்தப் பிரம்ம வித்தையையும் யோக நெறியையும் முழுமையாகப் பெற்ற நசிகேதன், பாபமும் மரண பயமும் நீங்கிப் பிரம்ம நிலையை அடைந்தான். தந்தையின் ஆசிரமத்திற்குப் பேரொளியுடன் திரும்பிய நசிகேதனின் வரலாறு, இவ்வுண்மையை உணரும் எவரும் பிறப்பு-இறப்பற்ற அமரத்துவத்தை அடைவர் என்று வாழ்த்துகிறது!",
                "subtitle_cue": "நசிகேதன் பெற்ற பிரம்ம வித்தையை உணரும் எவரும் மரணமற்ற அமரத்துவத்தை அடைவர்!",
                "sound_cue": "Joyful Vedic Mangalam chant 'Om Saha Navavatu... Om Shantih Shantih Shantih'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_05_PRASHNA_01",
        "muktika_number": 4,
        "upanishad_sanskrit": "प्रश्नोपनिषद्",
        "upanishad_iast": "Praśnopaniṣad",
        "upanishad_tamil": "பிரஸ்ன உபநிடதம்",
        "upanishad_english": "Prashna Upanishad",
        "veda": "Atharva Veda",
        "category": "Mukhya",
        "story_title_english": "Sage Pippalada & The Six Seekers: Six Cosmic Questions on Prana, Dreams & Om",
        "story_title_tamil": "பிப்பலாத முனிவரும் ஆறு சாதகர்களும்: பிராணன், கனவு மற்றும் ஓங்காரத்தின் ஆறு ரகசியங்கள்",
        "characters": [
            "Maharishi Pippalada (The illumined Guru of the Atharva Veda)",
            "Sukesha Bharadvaja, Satyakama Shaibya, Gargya, Kausalya Ashvalayana, Bhargava Vaidarbhi, and Kabandhi Katyayana (The Six Devoted Seekers of Brahman)"
        ],
        "mahavakya_sanskrit": "प्राणस्येदं वशे सर्वं त्रिदिवे यत्प्रतिष्ठितम् । मातेव पुत्रान् रक्षस्व श्रीश्च प्रज्ञां च विधेहि न इति ॥",
        "mahavakya_tamil_translit": "ப்ராணஸ்யேதம் வசே ஸர்வம் த்ரிதிவே யத்ப்ரதிஷ்டிதம் | மாதேவ புத்ரான் ரக்ஷஸ்வ ஸ்ரீஸ்ச ப்ரஜ்ஞாம் ச விதேஹி ந இதி ||",
        "mahavakya_meaning_english": "All that exists in the three worlds is under the control of Prana. O Prana, protect us as a mother protects her children, and grant us spiritual splendor and wisdom!",
        "mahavakya_meaning_tamil": "மூவுலகங்களிலும் நிலைபெற்றுள்ள அனைத்தும் பிராணனின் வசத்திலேயே உள்ளன. தாய் தன் குழந்தைகளைக் காப்பது போல் பிராணனே எங்களைக் காத்து, அருட்செல்வத்தையும் பேரறிவையும் தந்தருள்வாயாக!",
        "philosophical_theme": "One full year of Tapas and Brahmacharya as qualification for knowledge; the progressive inquiry from Creation (Rayi & Prana) to Vital Breath, Dream/Deep Sleep, Omkara, and the Sixteen-Part Purusha (Shodasha-Kala).",
        "setting_specifics": "Maharishi Pippalada's forest hermitage deep in the Narmada valley, featuring six thatched kutirs, a bird-catcher's net metaphor, and rivers flowing into the eastern ocean.",
        "metaphor_highlight": "Queen Bee and the Swarm (Madhukara-raja), Bird tied by a string returning to its perch, and Sixteen Rivers losing their names and forms upon merging into the Ocean.",
        "scenes": [
            {
                "camera": "Wide tracking shot of six Vedic scholars walking single-file through a misty ancient forest carrying bundles of Samit (sacred firewood) in their hands.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in a lush ancient Indian forest at dawn. Six earnest Vedic scholars of varying ages, dressed in saffron and white cotton dhotis with Rudraksha malas, walk humbly carrying bundles of dry sacrificial twigs (samit) in their hands toward the serene hermitage of aged Maharishi Pippalada seated beneath a giant peepal tree, no text, no borders.",
                "narration_en": "Six great scholars—Kabandhi, Bhargava, Kausalya, Gargya, Satyakama, and Sukesha—were already deeply learned in the Vedas, yet they thirsted for direct knowledge of the Supreme Brahman. Carrying bundles of sacred firewood in their hands as the token of humility, they approached the venerable Maharishi Pippalada in his forest hermitage.",
                "narration_ta": "சுகேஷன், சத்யகாமன், கார்கியன், கௌசல்யன், பார்கவன், கபந்தி ஆகிய ஆறு சிறந்த வேத விற்பன்னர்கள், பரம்பொருளை நேரில் உணரும் தாகத்தோடு சமித்துக்களைக் கையில் ஏந்தி (ஸமித்பாணிகளாய்), மகரிஷி பிப்பலாதரின் வன ஆசிரமத்தை வந்தடைந்தனர்.",
                "subtitle_cue": "பிரஸ்ன உபநிடதம்: பிரம்ம ஞானம் வேண்டி பிப்பலாத முனிவரை அணுகிய ஆறு சாதகர்கள்!",
                "sound_cue": "Morning forest birdsong, gentle stream water, and Atharva Veda peace invocation."
            },
            {
                "camera": "Montage-style slow pan across the ashram through changing seasons—monsoon rain, autumn leaves, and winter mist—showing the six seekers in silent meditation and service.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 wide shot of an ancient Vedic ashram courtyard. The six disciples sit in disciplined silence tending the sacred Agnihotra fire and meditating under the watchful, compassionate gaze of Maharishi Pippalada. Golden sunlight filters through monsoon-washed green foliage, copper water pots and palm leaves nearby, no text, no subtitles, no borders.",
                "narration_en": "Did Sage Pippalada answer their questions immediately? No! For supreme truth cannot be poured into a restless mind. The Sage said: 'भूय एव तपसा ब्रह्मचर्येण श्रद्धया संवत्सरं संवत्स्यथ—Dwell here for one full year more in austerity, celibacy, and unshakeable faith! Then ask whatever questions you wish, and if we know, we shall tell you all.'",
                "narration_ta": "மகரிஷி பிப்பலாதர் உடனே அவர்களின் கேள்விகளுக்கு விடையளிக்கவில்லை! அமைதியற்ற மனதில் ஆத்ம ஞானம் தங்காது என்பதால், 'இன்னும் ஓராண்டு காலம் தவத்துடனும், பிரம்மச்சரியத்துடனும், ஆழ்ந்த சிரத்தையுடனும் இங்கே வாழுங்கள்; அதன்பின் நீங்கள் விரும்பும் கேள்விகளைக் கேளுங்கள், நாங்கள் அறிந்த அனைத்தையும் உங்களுக்குக் கூறுவோம்!' என்று பணித்தார்.",
                "subtitle_cue": "ஞானத்தைப் பெறுவதற்கு முன் ஓராண்டு காலம் தவம், பிரம்மச்சரியம் மற்றும் சிரத்தை!",
                "sound_cue": "Meditative Tanpura and slow, rhythmic Pakhawaj beats marking the passage of a sacred year."
            },
            {
                "camera": "Close-up of a golden honeycomb in a forest tree where hundreds of bees rise together as the Queen Bee lifts off.",
                "veo_prompt": "16:9 8K 24fps photorealistic macro-to-medium shot in the sunlit forest outside Pippalada's ashram. A natural golden honeycomb hangs from a banyan branch; as the royal queen bee rises into the golden morning air, all the worker bees rise in unison with her. In the background, Sage Pippalada instructs Kabandhi and Bhargava, no text, no borders.",
                "narration_en": "After a year of silence, Kabandhi asked the First Question: 'Whence are all creatures born?' Pippalada revealed Prajapati's twin cosmic principles: Rayi (Matter, the Moon) and Prana (Life-Force, the Sun). And to Bhargava's Second Question on which power is supreme in the body, he gave the parable of the Queen Bee: 'Just as all bees rise when the Queen Bee rises, and settle when she settles, so speech, mind, eye, and ear depend wholly upon Prana!'",
                "narration_ta": "ஓராண்டு தவத்திற்குப் பின் கபந்தி முதல் கேள்வியைக் கேட்டார்: 'உயிர்கள் எங்கிருந்து தோன்றுகின்றன?' பிரஜாபதி படைத்த 'ரயி' (பொருள்/சந்திரன்) மற்றும் 'பிராணன்' (உயிர்/சூரியன்) ஆகிய இரு தத்துவங்களை முனிவர் விளக்கினார். இரண்டாவது கேள்விக்கு விடையளித்த அவர், 'இராணித் தேனீ எழுந்தால் எல்லாத் தேனீக்களும் உடன் எழுவது போலவும், அது அமர்ந்தால் அனைத்தும் அமர்வது போலவும், வாக்கும் மனமும் கண்ணும் காதும் பிராணனையே சார்ந்து நிற்கின்றன!' என்றார்.",
                "subtitle_cue": "இராணித் தேனீயை மற்ற தேனீக்கள் பின்பற்றுவது போல், புலன்கள் அனைத்தும் பிராணனையே சார்ந்துள்ளன!",
                "sound_cue": "Gentle natural humming of bees blending seamlessly into a warm Veena and flute raga."
            },
            {
                "camera": "Sunset shot over the ashram: birds flying from all directions to rest upon a single great tree as golden solar rays merge back into the setting sun.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic sunset shot over a tranquil Vedic forest hermitage. Flocks of white and golden birds fly across the twilight sky to settle peacefully upon the branches of one ancient banyan tree, while golden sunbeams draw back into the setting sun disk. Sage Pippalada speaks to Kausalya and Gargya, no text, no borders.",
                "narration_en": "To Kausalya's Third Question on how Prana enters and divides within the body, Pippalada explained how the five vital airs—Prana, Apana, Samana, Vyana, and Udana—govern the 72,000 subtle nadis radiating from the heart. And to Gargya's Fourth Question on sleep and dreams: 'Just as birds return to their resting tree at sunset, so in deep sleep all senses merge back into the serene Mind and rest in the Supreme Atman!'",
                "narration_ta": "மூன்றாவது கேள்வியில், இதயத்திலிருந்து பிரியும் நாடிகளில் பிராணன், அபானன், சமானன், வியானன், உதானன் ஆகிய பஞ்ச பிராணன்கள் செயல்படும் விதத்தை முனிவர் விளக்கினார். நான்காவது கேள்வியான உறக்கம் மற்றும் கனவு பற்றி விளக்கும்போது, 'மாலை வேளையில் பறவைகள் அனைத்தும் தம் கூட்டு மரத்தை நோக்கித் திரும்புவது போல், ஆழ்ந்த உறக்கத்தில் புலன்கள் அனைத்தும் மனதில் ஒடுங்கிப் பரமாத்மாவில் இளைப்பாறுகின்றன!' என்றார்.",
                "subtitle_cue": "பறவைகள் மாலையில் கூட்டு மரத்தில் ஒடுங்குவது போல், உறக்கத்தில் புலன்கள் ஆத்மாவில் ஒடுங்குகின்றன!",
                "sound_cue": "Tranquil evening Raga Neelambari on Bansuri, fluttering wings settling into calm silence."
            },
            {
                "camera": "Glowing close-up of Satyakama Shaibya and Pippalada chanting Om; visual resonance ripples through the air like golden concentric circles.",
                "veo_prompt": "16:9 8K 24fps photorealistic spiritual close-up in the candle-lit ashram hall. Sage Pippalada and disciple Satyakama chant the sacred syllable Om in unison; subtle golden sound-wave ripples of light emanate from the sacred Homa fire toward the starry night sky above, Rudraksha beads and vibhuti clearly visible, no text, no subtitles, no borders.",
                "narration_en": "Satyakama asked the Fifth Question: 'What world does a seeker win who meditates on the syllable OM until death?' Pippalada answered: 'O Satyakama, this very syllable OM is both the Higher and the Lower Brahman! Through Its three matras—A, U, M—covering waking, dream, and deep sleep, the wise sage sheds all sins just as a snake sheds its old skin, and rises to the supreme realm of Brahman!'",
                "narration_ta": "சத்யகாமன் ஐந்தாவது கேள்வியைக் கேட்டார்: 'வாழ்நாள் முழுவதும் ஓங்காரத்தைத் தியானிப்பவன் அடையும் நிலை யாது?' பிப்பலாதர் அருளினார்: 'சத்யகாமா! இந்த ஓங்காரமே பர பிரம்மமும் அபர பிரம்மமும் ஆகும்! அ, உ, ம என்னும் அதன் மூன்று மாத்திரைகளைத் தியானிக்கும் ஞானி, பாம்பு தன் பழைய தோலை உரித்துப் போடுவது போல் பாவங்களை உதறிப் பிரம்ம லோகத்தை அடைகிறான்!'",
                "subtitle_cue": "ஏதத் வை சத்யகாம பரம் சாபரம் ச ப்ரஹ்ம யத் ஓங்காரஃ — இந்த ஓங்காரமே பரம்பொருள்!",
                "sound_cue": "Deep, harmonic three-part chanting of 'A-U-M' resonating with temple bronze bells."
            },
            {
                "camera": "Epic aerial crane shot following multiple winding rivers through forests and valleys as they pour into the vast, shoreless golden ocean at sunrise.",
                "veo_prompt": "Breathtaking 16:9 8K 24fps photorealistic aerial landscape shot of ancient India at sunrise. Multiple winding rivers flow out of emerald forests and mountain valleys to merge into a vast, boundless golden ocean. Once the river waters meet the sea, they become one continuous, shimmering expanse of light, no text, no watermarks, no borders.",
                "narration_en": "Finally, Sukesha asked the Sixth Question about the Purusha of Sixteen Parts—Shodasha-Kala Purusha. Pippalada pointed within: 'That Purusha is right here inside your body! Just as a wheel's spokes are fastened to its hub, so the sixteen parts depend upon the Self. And just as flowing rivers aiming for the ocean lose their separate names and forms upon reaching the sea, and are called simply the Ocean, so the sixteen parts merge into the Immortal Purusha!'",
                "narration_ta": "சுகேஷன் கேட்ட ஆறாவது கேள்விக்கு, பதினாறு கலைகள் கொண்ட புருஷன் நம் உடலுக்குள்ளேயே உறைவதை முனிவர் காட்டினார்: 'சக்கரத்தின் ஆரக்கால்கள் அதன் மையக் குமிழில் நிலைத்திருப்பது போல், பதினாறு கலைகளும் ஆத்மாவில் நிலைத்துள்ளன. கடலை நோக்கிப் பாயும் நதிகள் சமுத்திரத்தில் கலந்தவுடன் தம் பெயரையும் உருவத்தையும் இழந்து கடல் என்றே அழைக்கப்படுவது போல், ஞானியின் கலைகள் அனைத்தும் அமர புருஷனில் ஒன்றாகக் கலக்கின்றன!'",
                "subtitle_cue": "நதிகள் சமுத்திரத்தில் கலந்து பெயரும் உருவமும் அழிவது போல், ஆத்மாவில் அனைத்தும் ஒன்றாகின்றன!",
                "sound_cue": "Majestic ocean waves blending with soaring Veena and Violin symphony."
            },
            {
                "camera": "Symmetrical wide shot of the six illumined seekers bowing at Maharishi Pippalada's feet and scattering lotus petals at his seat.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot in Pippalada's forest hermitage. The six illumined sages bow in deep gratitude at the feet of Maharishi Pippalada, offering fresh pink lotus flowers around his wooden seat under the sunlit peepal tree. Sacred fire burning brightly, serene Vedic atmosphere, zero text, zero borders.",
                "narration_en": "With their doubts dissolved like mist before the morning sun, the six sages worshiped Maharishi Pippalada and declared: 'Tvam hi nah pita योऽस्माकमविद्यायाः परं पारं तारयसि—You indeed are our true Father, for you have carried us across to the further shore beyond ignorance! Salutations to the supreme Rishis! Salutations to the supreme Rishis!'",
                "narration_ta": "ஐயங்கள் அனைத்தும் கதிரவனைக் கண்ட பனிபோல் விலக, ஆறு முனிவர்களும் பிப்பலாதரின் திருவடிகளில் பணிந்து போற்றினர்: 'அறியாமை என்னும் பெருங்கடலின் மறுகரைக்கு எங்களைக் கரையேற்றிய நீரே எங்கள் உண்மையான தந்தை! பரம ரிஷிகளுக்கு நமஸ்காரம்! பரம ரிஷிகளுக்கு நமஸ்காரம்!'",
                "subtitle_cue": "அறியாமைக் கடலின் மறுகரைக்கு எங்களைக் கரையேற்றிய நீரே எங்கள் உண்மையான தந்தை! நமஃ பரம ரிஷிப்யஃ!",
                "sound_cue": "Atharva Veda Shanti Mantra 'Om Bhadram Karnebhih Shrinuyama Devah' in full chorus."
            }
        ]
    }
]


MUKHYA_PART2 = [
    {
        "story_id": "MUKHYA_06_MUNDAKA_01",
        "muktika_number": 5,
        "upanishad_sanskrit": "मुण्डकोपनिषद्",
        "upanishad_iast": "Muṇḍakopaniṣad",
        "upanishad_tamil": "முண்டக உபநிடதம்",
        "upanishad_english": "Mundaka Upanishad",
        "veda": "Atharva Veda",
        "category": "Mukhya",
        "story_title_english": "Shaunaka's Question & The Two Birds on One Tree: Knowing That by Which All Is Known",
        "story_title_tamil": "ஒரே மரத்தில் இரண்டு பறவைகள்: எதை அறிந்தால் அனைத்தும் அறியப்படுமோ அந்தப் பிரம்ம வித்தை",
        "characters": [
            "Shaunaka (The great householder Mahashala seeking the ultimate synthesis of knowledge)",
            "Maharishi Angiras (The sage in the lineage of Brahma, Atharva, and Satyavaha)",
            "Dva Suparna (The Two Golden Birds perched upon the single Fig Tree of the Body)"
        ],
        "mahavakya_sanskrit": "सत्यमेव जयते नानृतं सत्येन पन्था विततो देवयानः । द्वा सुपर्णा सयुजा सखाया समानं वृक्षं परिषस्वजाते ॥",
        "mahavakya_tamil_translit": "ஸத்யமேவ ஜயதே நான்ருதம் ஸத்யேன பந்தா விததோ தேவயானஃ | த்வா ஸுபர்ணா ஸயுஜா ஸகாயா ஸமானம் வ்ருக்ஷம் பரிஷஸ்வஜாதே ||",
        "mahavakya_meaning_english": "Truth alone triumphs, never untruth! By Truth is laid out the divine path of Devayana. Two birds of golden plumage, inseparable companions, cling to the selfsame tree.",
        "mahavakya_meaning_tamil": "வாய்மையே வெல்லும், பொய்மையன்று! சத்தியத்தினாலேயே தேவயானப் பாதை விரிந்துள்ளது. பிரியாத தோழர்களான இரு அழகிய பறவைகள் ஒரே மரத்தைத் தழுவி அமர்ந்துள்ளன.",
        "philosophical_theme": "Para Vidya (Supreme Direct Realization of the Imperishable Akshara) vs. Apara Vidya (Lower ritual/intellectual learning); the Spider and Web, Fire and Sparks, Bow of Om, and the Two Birds on a Tree.",
        "setting_specifics": "Maharishi Angiras's Himalayan forest ashram with a massive fruit-laden Peepal tree where two golden-feathered birds sit on lower and upper branches.",
        "metaphor_highlight": "Dva Suparna (Two Birds on One Tree), Spider spinning and withdrawing its web (Urnanabhi), Thousands of sparks flying from a blazing fire, Frail Leaky Boats (Plava Hyete Adridhah), and Bow of Omkara.",
        "scenes": [
            {
                "camera": "Regal tracking shot of the great householder Shaunaka approaching Maharishi Angiras with ceremonial firewood in his hands.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in an ancient Vedic forest hermitage. The dignified householder sage Shaunaka, dressed in fine white cotton dhoti and golden angavastram, approaches the venerable white-bearded Maharishi Angiras seated before a sacred fire altar, carrying samit firewood humbly in both hands, golden morning light, no text, no borders.",
                "narration_en": "In the lineage descending from Brahma himself, the great householder Shaunaka approached Maharishi Angiras according to sacred rite and asked the question that echoes through eternity: 'Kasmin nu bhagavo vijnate sarvamidam vijnatam bhavati—Revered Master, what is That, by knowing which all this universe becomes known?'",
                "narration_ta": "பிரம்ம தேவரின் குரு பரம்பரையில் வந்த மகரிஷி அங்கிரஸரை, மகாசாலரான சௌனகர் முறைப்படி அணுகிப் பணிந்து கேட்டார்: 'கஸ்மின் நு பகவோ விஜ்ஞாதே ஸர்வமிதம் விஜ்ஞாதம் பவதி — பகவானே! எதை அறிந்தால் இவ்வுலகில் உள்ள அனைத்தும் அறியப்பட்டதாக ஆகுமோ, அந்த மூலப் பொருள் யாது?'",
                "subtitle_cue": "முண்டக உபநிடதம்: எதை அறிந்தால் இவ்வுலகம் அனைத்தும் அறியப்பட்டதாகும்?",
                "sound_cue": "Resonant Atharva Veda invocation, deep Tanpura drone, gentle forest breeze."
            },
            {
                "camera": "Medium shot of Angiras gesturing toward stacks of palm-leaf manuscripts on one side and the silent, infinite sky on the other.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot inside a thatched gurukulam pavilion. Maharishi Angiras points with one hand toward neatly stacked palm-leaf manuscripts (Olai Chuvadi) and ritual copper vessels, while raising his other hand in Chinmudra toward the vast sunlit sky. Shaunaka listens with intense devotion, no text, no subtitles, no borders.",
                "narration_en": "Angiras replied: 'Two kinds of knowledge must be known, say the knowers of Brahman: Para Vidya, the Supreme, and Apara Vidya, the Lower. The lower consists of the four Vedas, phonetics, ritual, grammar, etymology, metrics, and astronomy. But Para Vidya—the Supreme Wisdom—is that by which the Imperishable Akshara is directly realized!'",
                "narration_ta": "மகரிஷி அங்கிரஸர் அருளினார்: 'பிரம்மத்தை அறிந்த பெரியோர்கள், அறிய வேண்டிய வித்தை இரண்டு வகைப்படும் என்பர் — அவை பர வித்தை (மேலான ஞானம்) மற்றும் அபர வித்தை (சாதாரணக் கல்வி). நான்கு வேதங்கள், உச்சரிப்பு, இலக்கணம், ஜோதிடம் உள்ளிட்ட அனைத்தும் அபர வித்தையே! ஆனால் எதனால் அழியாத அக்ஷரப் பரம்பொருள் நேரடியாக உணரப்படுகிறதோ, அதுவே பர வித்தை!'",
                "subtitle_cue": "எதனால் அழியாத அக்ஷரப் பரம்பொருள் நேரில் உணரப்படுகிறதோ, அதுவே பர வித்தை!",
                "sound_cue": "Clear Veena melody contrasting rhythmic recitation with a sustained, timeless harmonic note."
            },
            {
                "camera": "Macro nature montage: a spider spinning a glistening dew-covered web, and thousands of golden sparks rising from a roaring Homa fire.",
                "veo_prompt": "16:9 8K 24fps photorealistic split-sequence shot in an ancient forest ashram: a delicate golden spider weaving a dewy web on a lotus leaf in morning sunlight, transitioning to a blazing sacred Homa fire sending thousands of glowing golden sparks upward into the twilight air. Pure natural beauty, no text, no borders.",
                "narration_en": "'Just as a spider sends forth and draws in its thread, just as herbs grow effortless upon the earth, and just as thousands of sparks fly forth from a blazing fire of like nature—so from that Imperishable Akshara does this entire universe arise, and into It alone does it return! Sacrifices performed without this wisdom are frail, leaky boats that cannot cross the ocean of birth and death.'",
                "narration_ta": "'சிலந்திப் பூச்சி தன்ுள்ளிருந்தே வலையைப் பின்னி மீண்டும் தன்னுள்ளே இழுத்துக்கொள்வது போலவும், பூமியில் செடிகொடிகள் முளைப்பது போலவும், நன்கு கொழுந்துவிட்டு எரியும் நெருப்பிலிருந்து ஆயிரக்கணக்கான தீப்பொறிகள் தோன்றுவது போலவும், அந்த அழியாத பரம்பொருளிலிருந்தே இப்பிரபஞ்சம் தோன்றி அதிலேயே ஒடுங்குகிறது! இந்த ஞானமில்லாத வெறும் சடங்குகள், பிறவிக் கடலைக் கடக்க உதவாத ஓட்டைப் படகுகளே ஆகும்.'",
                "subtitle_cue": "சிலந்தி தன்ுள்ளிருந்தே வலையைப் பின்னுவது போல், பரம்பொருளிலிருந்தே பிரபஞ்சம் தோன்றுகிறது!",
                "sound_cue": "Crackling fire sparks and delicate harp arpeggios in Raga Mohanam."
            },
            {
                "camera": "Metaphorical visual shot: a radiant golden bow of light (Omkara), with the focused soul as a sharpened arrow aimed at the luminous target of Brahman.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic spiritual visualization in a Vedic forest clearing. A young yogi in saffron dhoti meditates in Padmasana while a translucent golden bow of light forms around him, aiming a single glowing arrow of pure concentration toward a radiant solar target in the heart of the cosmos, no text, no subtitles, no borders.",
                "narration_en": "How then is that Imperishable Target pierced? Angiras gave the great Archery Metaphor: 'Pranavo dhanuh sharo hyatma brahma tallakshyam uchyate—The sacred syllable OM is the bow; one's own soul, purified by meditation, is the arrow; and Brahman is the supreme target! With an undistracted mind, shoot that arrow so that it becomes completely one with the Target!'",
                "narration_ta": "அந்த அழியாத இலக்கை அடைவது எப்படி? அங்கிரஸர் வில்-அம்பு உவமையைக் கூறினார்: 'ப்ரணவோ தனுஃ சரோ ஹ்யாத்மா ப்ரஹ்ம தல்லக்ஷ்யம் உச்யதே — ஓங்காரமே வில்; தியானத்தால் கூர்மையாக்கப்பட்ட ஜீவாத்மாவே அம்பு; பிரம்மமே அதன் இலக்கு! சிதறாத மனதுடன் அந்த அம்பை எய்து, அம்பு இலக்கோடு ஒன்றாவது போல் பிரம்மத்தோடு ஒன்றாகிவிடு!'",
                "subtitle_cue": "ப்ரணவோ தனுஃ சரோ ஹ்யாத்மா ப்ரஹ்ம தல்லக்ஷ்யம் — ஓங்காரமே வில், ஆத்மாவே அம்பு, பிரம்மமே இலக்கு!",
                "sound_cue": "Taut tambura string pluck followed by a soaring, unerring Bansuri glide."
            },
            {
                "camera": "Iconic slow tilt-up along the trunk of a majestic Peepal tree: on a lower branch, one bird pecks anxiously at sweet and bitter fruits; on the highest branch sits an identical golden bird in serene stillness.",
                "veo_prompt": "Masterpiece 16:9 8K 24fps photorealistic shot of an ancient sacred Peepal tree bathed in golden sunlight. On a lower shadowed branch, a colourful bird pecks restlessly at red and dark fig fruits, looking anxious; on the highest sunlit branch sits a magnificent, serene golden-plumaged bird watching calmly without eating, glowing with divine peace, no text, no borders.",
                "narration_en": "Then Maharishi Angiras unveiled the most celebrated parable of Vedanta—the Two Birds upon One Tree: 'Dva suparna sayuja sakhaya—Two birds of golden plumage, inseparable companions, cling to the selfsame tree of this body. One of them—the Jiva—eats the sweet and bitter fruits of karma and weeps in helplessness; the other—the Supreme Witness—looks on in majestic silence without eating!'",
                "narration_ta": "அடுத்து வேதாந்தத்தின் மிகப் புகழ்பெற்ற 'இரு பறவைகள்' உவமையை முனிவர் அருளினார்: 'த்வா ஸுபர்ணா ஸயுஜா ஸகாயா — பிரியாத தோழர்களான இரு அழகிய பறவைகள், உடலாகிய ஒரே மரத்தைத் தழுவி அமர்ந்துள்ளன. அவற்றுள் கீழ்க்கிளையில் உள்ள ஜீவாத்மா என்னும் பறவை, இன்ப-துன்ப கனிகளை உண்டு மயங்கி வருந்துகிறது; உச்சிக் கிளையில் உள்ள பரமாத்மா என்னும் பறவையோ, எதையும் உண்ணாமல் சாட்சியாகப் பேரொளியுடன் வீற்றிருக்கிறது!'",
                "subtitle_cue": "த்வா ஸுபர்ணா ஸயுஜா ஸகாயா — ஒரே மரத்தில் அமர்ந்திருக்கும் ஜீவாத்மா-பரமாத்மா என்னும் இரு பறவைகள்!",
                "sound_cue": "Expressive Violin solo portraying sorrow and restlessness on the lower notes, rising to serene high octave peace."
            },
            {
                "camera": "The lower bird hops upward branch by branch into the golden light, merging into the radiant upper bird as Shaunaka enters Samadhi.",
                "veo_prompt": "16:9 8K 24fps photorealistic cinematic sequence: the lower bird on the sacred Peepal tree gazes upward, spreads its wings, and ascends through shafts of golden sunlight to merge into the serene golden bird on the top branch. Below the tree, Shaunaka and Maharishi Angiras sit in radiant meditation as golden light fills the forest, no text, no borders.",
                "narration_en": "As the lower bird tastes bitter sorrow, it turns its gaze upward. Each time it beholds the serene, self-luminous glory of the Lord perched above, it hops one branch higher—until at last its grief vanishes, and it realizes that there were never two birds at all! The Jiva was always the Golden Witness, casting merely a reflection in the tree of life.",
                "narration_ta": "கசப்பான கனிகளை உண்டு துன்புற்ற கீழ்ப்பறவை, ஒருகட்டத்தில் மேலே நோக்குகிறது. உச்சியில் பேரமைதியுடன் ஒளிரும் பரமாத்ம பறவையைத் தரிசிக்கத் தரிசிக்க, தன் துயரம் நீங்கி ஒவ்வொரு கிளையாக மேலேறுகிறது. இறுதியில் அருகில் சென்றதும், இரண்டு பறவைகள் என்பதே மாயை என்றும், அந்தப் பொன்மயமான சாட்சிப் பறவையே தான் என்றும் உணர்ந்து பிரம்மத்தோடு ஒன்றாகிறது!",
                "subtitle_cue": "மேலே வீற்றிருக்கும் ஈசனைத் தரிசித்த மாத்திரத்தில் ஜீவனின் துயரங்கள் அனைத்தும் மறைகின்றன!",
                "sound_cue": "Triumphant Shankha blow and celestial Veena-Flute-Mridangam crescendo."
            },
            {
                "camera": "Wide heroic shot of the Gurukulam bathed in golden sunlight as the eternal maxim 'Satyameva Jayate' resounds across the mountains.",
                "veo_prompt": "Epic 16:9 8K 24fps photorealistic wide landscape of an ancient Indian Himalayan ashram at golden sunrise. Sages and disciples stand facing the snow-clad peaks along a sunlit mountain path leading into the heavens. Sacred fire burning in the foreground, pure timeless Vedic grandeur, zero modern elements, zero text, zero borders.",
                "narration_en": "Thus rings the immortal proclamation of the Mundaka Upanishad, enshrined as the eternal motto of Bharata: 'Satyameva jayate nanritam—Truth alone triumphs, never untruth! By Truth is laid out the divine path of Devayana, by which the sages who are free from desire reach that Supreme Treasure-House of Truth, and become Brahman itself—Brahmaveda Brahmaiva Bhavati!'",
                "narration_ta": "இவ்வாறு பாரத நாட்டின் தாரக மந்திரமாகத் திகழும் முண்டக உபநிடதத்தின் சத்திய முழக்கம் ஒலிக்கிறது: 'ஸத்யமேவ ஜயதே நான்ருதம் — வாய்மையே வெல்லும், பொய்மையன்று! சத்தியத்தினாலேயே தேவயானப் பாதை விரிந்துள்ளது. ஆசைகள் அற்ற முனிவர்கள் அப்பாதை வழியே சத்தியத்தின் பரம இருப்பிடத்தை அடைகின்றனர். பிரம்மத்தை அறிபவன் பிரம்மமாகவே ஆகிறான் — ப்ரஹ்மவேத ப்ரஹ்மைவ பவதி!'",
                "subtitle_cue": "ஸத்யமேவ ஜயதே நான்ருதம் — வாய்மையே வெல்லும்! பிரம்மத்தை அறிபவன் பிரம்மமாகவே ஆகிறான்!",
                "sound_cue": "Grand Vedic chorus chanting 'Satyameva Jayate Nanritam... Om Bhadram Karnebhih'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_07_MANDUKYA_01",
        "muktika_number": 6,
        "upanishad_sanskrit": "माण्डूक्योपनिषद्",
        "upanishad_iast": "Māṇḍūkyopaniṣad",
        "upanishad_tamil": "மாண்டூக்ய உபநிடதம்",
        "upanishad_english": "Mandukya Upanishad",
        "veda": "Atharva Veda",
        "category": "Mukhya",
        "story_title_english": "Rishi Manduka & The Four Quarters of the Soul: From Waking, Dream & Sleep to Turiya",
        "story_title_tamil": "மாண்டூக ரிஷியும் ஆத்மாவின் நான்கு நிலைகளும்: விழிப்பு, கனவு, உறக்கம் கடந்து ஒளிரும் துரீயம்!",
        "characters": [
            "Maharishi Manduka (The Seer of the Four-Quartered Atman and Omkara)",
            "Gaudapada / The Ideal Advaita Seeker (Contemplating the three states of consciousness and the Fourth)"
        ],
        "mahavakya_sanskrit": "सर्वं ह्येतद् ब्रह्मायमात्मा ब्रह्म सोऽयमात्मा चतुष्पात् । शान्तं शिवमद्वैतं चतुर्थं मन्यन्ते स आत्मा स विज्ञेयः ॥",
        "mahavakya_tamil_translit": "ஸர்வம் ஹ்யேதத் ப்ரஹ்மாயமாத்மா ப்ரஹ்ம ஸோऽயமாத்மா சதுஷ்பாத் | ஸாந்தம் ஸிவமத்வைதம் சதுர்தம் மன்யந்தே ஸ ஆத்மா ஸ விஜ்ஞேயஃ ||",
        "mahavakya_meaning_english": "All this universe is verily Brahman; this Self is Brahman, and this Self has four quarters. Peaceful, auspicious, and non-dual is the Fourth (Turiya)—That is the Atman, and That alone is to be known!",
        "mahavakya_meaning_tamil": "இங்குள்ள அனைத்தும் பிரம்மமே; இந்த ஆத்மாவே பிரம்மம் (அயமாத்மா பிரம்மம்). சாந்தமானதும், மங்கலமானதும், இரண்டற்றதுமான நான்காவது நிலையே (துரீயம்) ஆத்மா; அதுவே அறியத்தக்கது!",
        "philosophical_theme": "Avastha-Traya Viveka (Inquiry into Waking/Vishva, Dream/Taijasa, and Deep Sleep/Prajna) mapped to A-U-M, culminating in the Silence of Turiya—the non-dual Fourth.",
        "setting_specifics": "A tranquil lotus-ringed hermitage pond on the banks of the Narmada at twilight, night, and dawn, mirroring the four states of consciousness.",
        "metaphor_highlight": "Chatushpat (Four-quartered coin/cow where smaller quarters merge into the whole), and A-U-M + Amatra (The three audible syllables merging into the Measureless Silence after Om).",
        "scenes": [
            {
                "camera": "Wide symmetrical twilight shot of Maharishi Manduka seated by a still lotus pond reflecting both the setting sun and the rising stars.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic shot of an ancient Vedic hermitage by a mirror-still lotus pond at twilight. Maharishi Manduka sits in serene Padmasana on a granite slab, surrounded by four brass oil lamps. The water reflects the golden sky and early stars with crystal clarity, authentic ancient Bharata setting, no text, no borders.",
                "narration_en": "Of all the hundred and eight Upanishads, the Muktika canon declares that the Mandukya alone is sufficient for liberation! In just twelve condensed mantras, Maharishi Manduka revealed the supreme equation: 'Om! This Imperishable Sound is the whole universe. All that was, all that is, and all that ever shall be is OM—and whatever transcends the three times is also OM!'",
                "narration_ta": "நூற்றியெட்டு உபநிடதங்களில், முக்தி அடைய மாண்டூக்ய உபநிடதம் ஒன்றே போதுமானது என்று முக்திக உபநிடதம் போற்றுகிறது! வெறும் பன்னிரண்டு மந்திரங்களில் மகரிஷி மாண்டூகர் மாபெரும் சத்தியத்தை வெளியிட்டார்: 'ஓம்! இந்த அழியாத ஓங்காரமே இப்பிரபஞ்சம் அனைத்தும் ஆகும். கடந்த காலம், நிகழ்காலம், எதிர்காலம் ஆகிய மூன்றும் ஓங்காரமே; முக்காலத்தையும் கடந்த பரம்பொருளும் ஓங்காரமே!'",
                "subtitle_cue": "மாண்டூக்ய உபநிடதம்: அயமாத்மா பிரம்மம் — இந்த ஆத்மாவே பிரம்மம்!",
                "sound_cue": "Deep, sustained resonant Omkaram on Tanpura and Tibetan/Vedic bronze bell."
            },
            {
                "camera": "Bright sunlit tracking shot through a bustling ancient Vedic village and ashram garden—Representing Jagrat (Waking State / Vaishvanara).",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 sunlit scene in an ancient Vedic ashram courtyard during the waking day (Jagrat). Disciples gather fruits, tend the sacred fire, and listen to Vedic recitation, experiencing sights, sounds, and fragrances of the external world. Warm, vivid natural colors, authentic cotton dhotis, no modern objects, no text, no borders.",
                "narration_en": "Declaring the Mahavakya 'Ayamatma Brahma—This Self is Brahman', the Sage examined its four quarters through our own daily experience. The First Quarter is Vaishvanara, the Waking State (Jagrat), whose consciousness turns outward through seven limbs and nineteen mouths to enjoy the gross physical world. In the syllable OM, this waking world is the first sound: 'A' (Akara)!",
                "narration_ta": "'அயமாத்மா பிரம்மம் — இந்த ஆத்மாவே பிரம்மம்' என்ற மகா வாக்கியத்தை முழங்கிய முனிவர், நம் அன்றாட அனுபவத்தின் நான்கு நிலைகளை ஆராய்ந்தார். முதல் பாதம் 'வைஸ்வானரன்' எனப்படும் விழிப்பு நிலை (ஜாக்ரத்). இதில் அறிவு வெளிமுகமாகத் திரும்பி, பருப்பொருள் உலகை அனுபவிக்கிறது. ஓங்காரத்தில் இந்த விழிப்பு நிலையே 'அ' (அகாரம்) என்னும் முதல் ஒலியாகும்!",
                "subtitle_cue": "முதல் பாதம் விழிப்பு நிலை (வைஸ்வானரன்) — ஓங்காரத்தின் 'அ' என்னும் முதல் மாத்திரை!",
                "sound_cue": "Lively morning Veena and Mridangam rhythm with birdsong and ashram activity."
            },
            {
                "camera": "Dreamlike slow-motion pan inside a lamp-lit kutir at night: a sleeping seeker's subtle mind projects shimmering golden palaces and rivers in the air.",
                "veo_prompt": "16:9 8K 24fps photorealistic atmospheric night scene inside a quiet Vedic hut lit by a single clay lamp. A young disciple sleeps peacefully on a kusha-grass mat while above him, translucent golden dream-visions of celestial chariots, rivers, and lotus gardens shimmer softly in the air (Svapna / Taijasa state), no text, no subtitles, no borders.",
                "narration_en": "When the eyes close and the senses withdraw, we enter the Second Quarter: Taijasa, the Dream State (Svapna). Here consciousness turns inward, shining by its own light to project an entire subtle universe of mountains, chariots, joys, and fears out of mental impressions. In the syllable OM, this luminous dream state is the second sound: 'U' (Ukara)!",
                "narration_ta": "கண்கள் மூடிப் புறப் புலன்கள் ஒடுங்கும்போது, நாம் இரண்டாம் பாதமான 'தைஜஸன்' எனப்படும் கனவு நிலைக்குள் (ஸ்வப்னம்) நுழைகிறோம். இங்கே அறிவு உள்முகமாகத் திரும்பி, மனதின் வாசனைகளால் மலைகளையும் தேர்களையும் இன்ப-துன்பங்களையும் கொண்ட நுண்ணிய உலகைப் படைத்து அனுபவிக்கிறது. ஓங்காரத்தில் இக்கனவு நிலையே 'உ' (உகாரம்) என்னும் இரண்டாம் ஒலியாகும்!",
                "subtitle_cue": "இரண்டாம் பாதம் கனவு நிலை (தைஜஸன்) — ஓங்காரத்தின் 'உ' என்னும் இரண்டாம் மாத்திரை!",
                "sound_cue": "Mystical, echoing Bansuri flute with soft harp glissandos."
            },
            {
                "camera": "Deep indigo night sky over the ashram where all ripples on the pond cease and all dream-visions fold into undivided, restful stillness.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic night shot of the Vedic ashram under a canopy of deep indigo stars. All lamps are dim, the lotus pond is completely motionless like dark polished glass, and the sleeping seeker rests in profound, dreamless peace (Sushupti / Prajna state). Serene cosmic stillness, no text, no borders.",
                "narration_en": "Then comes the Third Quarter: Prajna, the State of Deep, Dreamless Sleep (Sushupti), where the sleeper desires no desire and sees no dream! All multiplicity of waking and dream folds into a single unified mass of consciousness filled with bliss—Anandamaya. This is the Lord of All, the womb from which all thoughts arise and into which they dissolve. In OM, this is the third sound: 'M' (Makara)!",
                "narration_ta": "அடுத்து மூன்றாம் பாதமான 'ப்ராஜ்ஞன்' எனப்படும் ஆழ்ந்த உறக்க நிலை (ஸுஷுப்தி) வருகிறது. இங்கே எந்த ஆசையும் இல்லை, எந்தக் கனவும் இல்லை! விழிப்பு மற்றும் கனவின் பன்முகக் காட்சிகள் அனைத்தும் ஒன்றாக ஒடுங்கி, ஆனந்தமயமான பேரமைதி மட்டுமே நிலவுகிறது. அனைத்து எண்ணங்களும் தோன்றி ஒடுங்கும் மூலம் இதுவே. ஓங்காரத்தில் இது 'ம' (மகாரம்) என்னும் மூன்றாம் ஒலியாகும்!",
                "subtitle_cue": "மூன்றாம் பாதம் ஆழ்ந்த உறக்கம் (ப்ராஜ்ஞன்) — ஓங்காரத்தின் 'ம' என்னும் மூன்றாம் மாத்திரை!",
                "sound_cue": "Low, warm, enveloping bass Tanpura hum with zero percussion."
            },
            {
                "camera": "Slow push-in on Maharishi Manduka's face as dawn light breaks; the three flames of three oil lamps merge into the boundless golden sunlight filling the entire sky.",
                "veo_prompt": "16:9 8K 24fps photorealistic spiritual climax shot at Brahmamuhurtham dawn. Maharishi Manduka sits in radiant Samadhi by the lotus pond. Three small oil lamps in the foreground are outshone by the vast, infinite golden-white radiance of the rising sun illuminating the entire sky and water—symbolizing Turiya, the Fourth state, no text, no borders.",
                "narration_en": "Yet who witnesses Waking come and go, Dream come and go, and even Deep Sleep come and go? Maharishi Manduka revealed the supreme secret—Turiya, the Fourth! 'Shantam shivam advaitam chaturtham manyante sa atma sa vijneyah—Neither inward-turned nor outward-turned, unseen, beyond empirical dealings, peaceful, auspicious, and non-dual is the Fourth! That is the Atman, and That alone is to be realized!'",
                "narration_ta": "ஆனால் விழிப்பு வருவதையும் போவதையும், கனவு தோன்றுவதையும் மறைவதையும், ஆழ்ந்த உறக்கத்தையும் சாட்சியாகப் பார்த்துக்கொண்டிருக்கும் அந்தப் பேரறிவு யாது? அதுவே நான்காவது நிலையான 'துரீயம்'! 'ஸாந்தம் ஸிவமத்வைதம் சதுர்தம் மன்யந்தே ஸ ஆத்மா ஸ விஜ்ஞேயஃ — சாந்தமானதும், மங்கலமானதும், இரண்டற்றதுமான அந்த நான்காவது நிலையே ஆத்மா; அதுவே அறியத்தக்கது!'",
                "subtitle_cue": "ஸாந்தம் ஸிவமத்வைதம் சதுர்தம் — சாந்தமும் மங்கலமும் இரண்டற்றதுமான துரீயமே ஆத்மா!",
                "sound_cue": "Three distinct A-U-M tones resolving into a breathtaking, crystal-clear silence (Amatra) with a faint harmonic overtone."
            },
            {
                "camera": "Visual resonance of A, U, and M sound waves on the water surface dissolving into pure, mirror-like stillness reflecting the infinite sky.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 overhead-to-eye-level shot of concentric golden ripples on a sacred lotus pond gradually settling into absolute, mirror-like stillness that reflects the infinite blue-gold cosmos above. Maharishi Manduka and his disciple sit in silent non-dual realization, no text, no subtitles, no borders.",
                "narration_en": "In the meditation on OM, when 'A', 'U', and 'M' subside, there remains the Amatra—the Measureless Silence that follows the chant! That Silence is Turiya itself. The seeker who meditates upon the three states as identical with the three letters of OM, and finally abides in the Silent Fourth, enters the Self by the Self alone.",
                "narration_ta": "ஓங்கார தியானத்தில் 'அ', 'உ', 'ம' ஆகிய மூன்று ஒலிகளும் அடங்கிய பின் எஞ்சியிருக்கும் அளவற்ற மௌனமே 'அமாத்ரம்' எனப்படும் துரீய நிலையாகும்! மூன்று நிலைகளையும் ஓங்காரத்தின் மூன்று எழுத்துக்களோடு இணைத்துத் தியானித்து, இறுதியில் அந்த மௌனமான துரீயத்தில் நிலைபெறும் ஞானி, ஆத்மாவால் ஆத்மாவிற்குள்ளேயே பிரவேசிக்கிறான்.",
                "subtitle_cue": "ஓங்காரத்தின் மூன்று மாத்திரைகளும் அடங்கும் எல்லையற்ற மௌனமே துரீயப் பரம்பொருள்!",
                "sound_cue": "Pure resonant bronze bell chime decaying slowly into peaceful natural dawn ambience."
            },
            {
                "camera": "Wide serene closing shot of the Narmada ashram in full golden morning light, white swans gliding effortlessly across the water.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing tableau of the Narmada river hermitage at sunrise. Maharishi Manduka and his disciples sit in tranquil meditation as white swans glide across the golden lotus pond. Pure Advaita Vedanta serenity, authentic ancient India, zero modern elements, zero text, zero borders.",
                "narration_en": "'Samvishatyatmana'tmanam ya evam veda—He who knows thus enters his own eternal Self through the Self!' There is no birth, no dissolution, no bondage, and no seeker in that non-dual Reality. May this Mandukya wisdom awaken the Turiya consciousness within all beings!",
                "narration_ta": "'ஸம்விஸத்யாத்மனாத்மானம் ய ஏவம் வேத — இவ்வுண்மையை உணர்பவன் தன் ஆத்மாவால் ஆத்மாவிற்குள்ளேயே நிலைபெறுகிறான்!' இரண்டற்ற அந்த அத்வைதப் பெருவெளியில் பிறப்புமில்லை, இறப்புமில்லை, பந்தமுமில்லை, துக்கமுமில்லை. மாண்டூக்ய உபநிடதத்தின் இந்த மகா ஞானம் அனைவர் உள்ளத்திலும் துரீய விழிப்பை அருளட்டும்!",
                "subtitle_cue": "அயமாத்மா பிரம்மம் — இரண்டற்ற அத்வைத ஆத்மாவே நாம்! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!",
                "sound_cue": "Atharva Veda Shanti Mantra 'Om Bhadram Karnebhih... Om Shantih Shantih Shantih'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_08_TAITTIRIYA_01",
        "muktika_number": 7,
        "upanishad_sanskrit": "तैत्तिरीयोपनिषद्",
        "upanishad_iast": "Taittirīyopaniṣad",
        "upanishad_tamil": "தைத்திரீய உபநிடதம் (சிக்ஷாவல்லி & ஆனந்தவல்லி)",
        "upanishad_english": "Taittiriya Upanishad (Part 1: Shikshavalli & Anandavalli)",
        "veda": "Krishna Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "The Gurukulam Convocation & The Calculus of Cosmic Bliss: From Matru Devo Bhava to Fearless Ananda",
        "story_title_tamil": "மாதா பிதா குரு தெய்வம் & பிரம்ம ஆனந்தத்தின் அளவுகோல்: தைத்திரீய குருகுலப் பட்டமளிப்பு!",
        "characters": [
            "The Kulapati Acharya of the Taittiriya Gurukulam (Delivering the eternal convocation address)",
            "Snataka Graduates (Young Vedic scholars completing 12 years of Brahmacharya and preparing to enter the world)"
        ],
        "mahavakya_sanskrit": "सत्यं वद । धर्मं चर । मातृदेवो भव । पितृदेवो भव । आचार्यदेवो भव । सत्यं ज्ञानमनन्तं ब्रह्म ॥",
        "mahavakya_tamil_translit": "ஸத்யம் வத | தர்மம் சர | மாத்ருதேவோ பவ | பித்ருதேவோ பவ | ஆசார்யதேவோ பவ | ஸத்யம் ஜ்ஞானமனந்தம் ப்ரஹ்ம ||",
        "mahavakya_meaning_english": "Speak the Truth. Practice Dharma. Revere Mother, Father, and Acharya as God. Brahman is Truth, Consciousness, and Infinity (Satyam Jnanam Anantam Brahma).",
        "mahavakya_meaning_tamil": "உண்மையையே பேசு; தர்மத்தையே கடைப்பிடி; தாயையும் தந்தையையும் குருவையும் தெய்வமாகப் போற்று! பிரம்மம் என்பது சத்தியம், ஞானம் மற்றும் எல்லையற்ற ஆனந்தம் ஆகும்!",
        "philosophical_theme": "The Ethical Foundation of Dharmic Life (Shikshavalli Convocation), the Definition of Brahman (Satyam Jnanam Anantam), the Five Sheaths (Panchakosha), and the 100-fold Calculus of Bliss (Ananda Mimamsa).",
        "setting_specifics": "A grand South Indian/Vedic forest Gurukulam convocation courtyard decorated with mango leaves, brass lamps, and lotus altars.",
        "metaphor_highlight": "Panchakosha (Five concentric birds/sheaths from Food to Bliss) and the Ananda Mimamsa (100x multiplication ladder of joy from a healthy youth-emperor up to Hiranyagarbha and the Shrotriya).",
        "scenes": [
            {
                "camera": "Majestic wide crane shot of a Vedic Gurukulam convocation ceremony at sunrise; graduating Brahmacharis in fresh white cotton dhotis stand with folded hands before their Acharya.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene of an ancient Indian Gurukulam graduation ceremony (Samavartana) at dawn. Dozens of young Vedic graduates in pure white cotton dhotis and sacred threads stand reverently before their venerable white-bearded Kulapati Acharya seated on a carved stone dais under a banyan tree. Mango leaf toranas and glowing brass lamps, no text, no borders.",
                "narration_en": "After twelve years of sacred study in the forest Gurukulam, the young graduates stood ready to return home and enter householder life. Before bidding them farewell, the Kulapati Acharya delivered the immortal Convocation Address of the Taittiriya Upanishad—the ethical charter of Bharata!",
                "narration_ta": "பன்னிரண்டு ஆண்டுகள் வன குருகுலத்தில் வேதங்களைக் கற்றுத் தேர்ந்த இளம் பட்டதாரிகள் (ஸ்நாதகர்கள்), இல்லற வாழ்வில் நுழையத் தயாராக நின்றனர். அவர்களை வழியனுப்பும் முன், குலபதி ஆச்சாரியர் தைத்திரீய உபநிடதத்தின் உலகப் புகழ்பெற்ற பட்டமளிப்புப் பேருரையை (சிக்ஷாவல்லி உபதேசம்) வழங்கினார்!",
                "subtitle_cue": "தைத்திரீய உபநிடதம்: குருகுலப் பட்டமளிப்பு உபதேசம் — சத்யம் வத, தர்மம் சர!",
                "sound_cue": "Resonant Krishna Yajur Veda Taittiriya chorus chanting with auspicious Nagaswaram notes."
            },
            {
                "camera": "Slow tracking shot across the faces of the young graduates as the Acharya blesses each with sandalwood paste and palm-leaf scrolls.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium tracking shot in the Vedic gurukulam courtyard. The elderly Acharya applies sandalwood tilaka to the foreheads of graduating disciples and hands them etched palm-leaf manuscripts. In the background, parents and villagers wait with joyful reverence, warm golden morning light, no modern items, no text, no borders.",
                "narration_en": "The Acharya commanded: 'Satyam vada, Dharmam chara, Svadhyayan ma pramadah! Speak the truth! Walk in righteousness! Never neglect your daily study of wisdom! Matru Devo Bhava—let your Mother be your God! Pitru Devo Bhava—let your Father be your God! Acharya Devo Bhava—let your Teacher be your God! Atithi Devo Bhava—let the Guest be your God! Give with faith, give with humility, give with sympathy!'",
                "narration_ta": "ஆச்சாரியர் ஆணையிட்டார்: 'ஸத்யம் வத, தர்மம் சர, ஸ்வாத்யாயான் மா ப்ரமதஃ! உண்மையையே பேசு! தர்ம வழியிலேயே நட! கற்றலை ஒருபோதும் கைவிடாதே! மாத்ரு தேவோ பவ — தாயைத் தெய்வமாகப் போற்று! பித்ரு தேவோ பவ — தந்தையைத் தெய்வமாகப் போற்று! ஆசார்ய தேவோ பவ — குருவைத் தெய்வமாகப் போற்று! அதிதி தேவோ பவ — விருந்தினரைத் தெய்வமாகப் போற்று! சிரத்தையோடும் பணிவோடும் கருணையோடும் தானம் செய்!'",
                "subtitle_cue": "மாத்ரு தேவோ பவ | பித்ரு தேவோ பவ | ஆசார்ய தேவோ பவ | அதிதி தேவோ பவ ||",
                "sound_cue": "Rhythmic Vedic swara recitation accompanied by soft Mridangam and temple bells."
            },
            {
                "camera": "Transition to the inner meditation mandapam: the Acharya traces five concentric golden circles on a sandalwood-strewn floor representing the Panchakosha.",
                "veo_prompt": "16:9 8K 24fps photorealistic overhead-to-medium shot inside a quiet granite temple mandapam. A meditating yogi sits in Padmasana at the center of five subtle, concentric glowing golden rings on the stone floor, symbolizing the five sheaths of existence (Annamaya, Pranamaya, Manomaya, Vijnanamaya, Anandamaya), warm oil lamp lighting, no text, no borders.",
                "narration_en": "Then, in the Anandavalli, the Upanishad unveiled the supreme definition of Reality: 'Satyam Jnanam Anantam Brahma—Brahman is Existence, Consciousness, and Infinity!' Hidden within the cave of the heart, this Infinite Self is veiled by five concentric sheaths—the sheaths of Food, Vital Breath, Mind, Intellect, and Bliss. Peeling back each outer sheath as a bird formed of light, the seeker arrives at the core of pure Ananda!",
                "narration_ta": "தொடர்ந்து ஆனந்தவல்லியில், பரம்பொருளின் இலக்கணத்தை உபநிடதம் வரையறுத்தது: 'ஸத்யம் ஜ்ஞானமனந்தம் ப்ரஹ்ம — பிரம்மம் என்பது சத்தியம், பேரறிவு மற்றும் எல்லையற்ற தன்மை ஆகும்!' நம் இதயக் குகைக்குள் உறையும் அந்தப் பரம்பொருள் அன்னமய, பிராணமய, மனோமய, விஞ்ஞானமய, ஆனந்தமய என்னும் ஐந்து கோசங்களால் (உறைகளால்) சூழப்பட்டுள்ளது. ஒவ்வொரு உறையையும் கடந்து உள்ளே செல்லும்போது ஆத்ம பேரானந்தம் வெளிப்படுகிறது!",
                "subtitle_cue": "ஸத்யம் ஜ்ஞானமனந்தம் ப்ரஹ்ம — சத்தியம், ஞானம், அனந்தமே பிரம்மம்!",
                "sound_cue": "Five ascending harmonic notes on the Veena, each deeper and more luminous than the last."
            },
            {
                "camera": "Cinematic upward crane shot from a noble young emperor in a sunlit palace up through the clouds to celestial realms and back to a serene, desireless sage under a tree.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic visual comparison in ancient India: in the distance, a noble young king stands in a grand sunlit sandstone palace courtyard; in the foreground under a quiet banyan tree by a river, a serene, desireless Vedic sage (Shrotriya Avrijina Akamahata) sits in blissful meditation, glowing with infinitely greater peace, no text, no borders.",
                "narration_en": "How great is the Bliss of Brahman? The Upanishad performs the famous Calculus of Bliss—Ananda Mimamsa! Imagine a youth in the prime of health, noble, learned, and ruler of the entire wealth-filled earth: that is one unit of human bliss. Multiply it by a hundred for the Gandharvas, a hundred again for the Pitris, Devas, Indra, Brihaspati, and Prajapati! Yet every single level of that cosmic bliss belongs right now to the sage who is free from all selfish desire!",
                "narration_ta": "பிரம்ம ஆனந்தத்தின் அளவு எத்தகையது? உபநிடதம் 'ஆனந்த மீமாம்சை' என்னும் ஆனந்தக் கணக்கீட்டைச் செய்கிறது! நற்கல்வியும் உடல்வளமும் கொண்ட ஓர் இளைஞன் இவ்வுலகம் முழுவதற்கும் சக்கரவர்த்தியாக இருந்தால் அவனது மகிழ்ச்சி 'ஒரு மனித ஆனந்தம்' ஆகும். அதை நூறால் பெருக்கினால் கந்தர்வர் ஆனந்தம்; மீண்டும் நூறு நூறாகப் பெருக்கினால் தேவர்கள், இந்திரன், பிரகஸ்பதி, பிரஜாபதியின் ஆனந்தம்! ஆனால் ஆசைகளற்ற ஞானிக்கோ (அகாமஹத श्रोत्रिय) இவை அனைத்தும் இயல்பாகவே சொந்தமாகின்றன!",
                "subtitle_cue": "ஆசைகளற்ற ஞானி (அகாமஹதன்), பிரஜாபதியின் பேரானந்தத்தையும் தன்னுள்ளேயே அனுபவிக்கிறான்!",
                "sound_cue": "Soaring Violin and Bansuri crescendo reaching a peak of pure, effortless bliss."
            },
            {
                "camera": "Macro shot of the wind stirring trees, the sun rising in the east, and fire blazing on the altar—all operating in cosmic harmony.",
                "veo_prompt": "16:9 8K 24fps photorealistic nature-and-cosmos shot in ancient India: the golden sun rising majestically over mountain peaks, wind rippling across a lotus lake, and sacred fire blazing on a stone altar, all unified in grand cosmic order under the invisible presence of Brahman, no text, no subtitles, no borders.",
                "narration_en": "Out of awe for that Supreme Reality, the Wind blows; out of awe for It, the Sun rises; out of awe for It, Agni, Indra, and Death himself perform their cosmic duties! He who realizes that the Spirit within a human being and the Spirit within the Sun are one and the same—Sa yashchayam purushe yashchasavaditye sa ekah—transcends all five sheaths!",
                "narration_ta": "அந்தப் பரம்பொருளின் ஆணையாலேயே காற்று வீசுகிறது; சூரியன் உதிக்கிறான்; அக்னியும் இந்திரனும் காலனும் தத்தம் கடமைகளைச் செய்கின்றனர்! 'ஸ யஸ்சாயம் புருஷே யஸ்சாஸாவாதித்யே ஸ ஏகஃ' — மனிதனுக்குள் உறையும் ஆத்மாவும், சூரியனுக்குள் ஒளிரும் பரம்பொருளும் ஒன்றே என்று உணர்பவன் ஐந்து கோசங்களையும் கடந்து பிரம்மத்தில் நிலைபெறுகிறான்!",
                "subtitle_cue": "மனிதனுக்குள் உறையும் ஆத்மாவும் சூரியனுக்குள் ஒளிரும் பரம்பொருளும் ஒன்றே!",
                "sound_cue": "Majestic Mridangam and Shankha resonance with cosmic wind ambience."
            },
            {
                "camera": "Close-up of the Acharya in Samadhi as words and thoughts fall back like gentle rain before the silent mountain of Self-bliss.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 close-up of the venerable Taittiriya Acharya in deep blissful meditation. Golden morning light bathes his serene countenance adorned with vibhuti and Rudraksha, while lotus petals float on still water beside him, conveying absolute fearlessness (Abhayam), no text, no borders.",
                "narration_en": "Here shines the immortal verse of the Anandavalli: 'Yato vacho nivartante aprapya manasa saha, anandam brahmano vidvan na bibheti kutashchana! From Where words return along with the mind, unable to grasp It—he who knows that Bliss of Brahman fears nothing whatsoever in this universe!'",
                "narration_ta": "இங்கே ஆனந்தவல்லியின் அமர மந்திரம் ஒலிக்கிறது: 'யதோ வாசோ நிவர்த்தந்தே அப்ராப்ய மனஸா ஸஹ, ஆனந்தம் ப்ரஹ்மணோ வித்வான் ந பிபேதி குதஸ்சன! மனதுடன் கூட வாக்கும் எதனை எட்டிப் பிடிக்க முடியாமல் திரும்பிவிடுகிறதோ, அந்தப் பிரம்ம ஆனந்தத்தை நேரடியாக உணர்ந்தவன் இவ்வுலகில் எதற்குமே அஞ்சுவதில்லை!'",
                "subtitle_cue": "யதோ வாசோ நிவர்த்தந்தே... பிரம்ம ஆனந்தத்தை உணர்ந்தவன் எதற்குமே அஞ்சுவதில்லை!",
                "sound_cue": "Deep, fearless Vedic chant of 'Yato Vacho Nivartante' echoing in a granite hall."
            },
            {
                "camera": "Wide celebratory pull-back of the graduates departing along sunlit forest paths while the Gurukulam chants 'Om Sham No Mitrah'.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot of the Taittiriya Gurukulam. Graduating disciples walk forth in peaceful confidence along a sunlit forest path lined with blooming lotuses and banyan trees, while the Acharya raises his hand in eternal benediction. Pure ancient Bharata splendour, zero text, zero borders.",
                "narration_en": "Why does the wise one never fear? Because fear arises only when one sees a second thing separate from oneself! Established in non-dual Bliss, the graduate walks through the world practicing Dharma while resting forever in the Fearless Brahman!",
                "narration_ta": "ஞானி ஏன் எதற்கும் அஞ்சுவதில்லை? ஏனெனில், தன்னைத் தவிர இரண்டாவது பொருள் உண்டு என எண்ணும்போது மட்டுமே பயம் தோன்றும்! இரண்டற்ற பிரம்ம ஆனந்தத்தில் நிலைபெற்றவன், தர்ம வழியில் உலகில் வாழ்ந்துகொண்டே அபய நிலையான மோட்ச சுகத்தை அனுபவிக்கிறான்!",
                "subtitle_cue": "இரண்டாவது பொருள் உண்டு என எண்ணும்போதே பயம் தோன்றும்; அத்வைத ஞானிக்கு என்றும் அபயமே!",
                "sound_cue": "Unison Shanti Mantra 'Om Sham No Mitrah Sham Varunah... Om Shantih Shantih Shantih'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_09_TAITTIRIYA_02",
        "muktika_number": 7,
        "upanishad_sanskrit": "तैत्तिरीयोपनिषद् (भृगुवल्ली)",
        "upanishad_iast": "Taittirīyopaniṣad (Bhṛguvallī)",
        "upanishad_tamil": "தைத்திரீய உபநிடதம் (பிருகுவல்லி)",
        "upanishad_english": "Taittiriya Upanishad (Part 2: Bhriguvalli)",
        "veda": "Krishna Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "Bhrigu & Varuna's Fivefold Tapas: Peeling the Five Sheaths to Discover 'Anando Brahma'",
        "story_title_tamil": "பிருகு முனிவரும் வருண பகவானும்: பஞ்ச கோசங்களைத் துளைத்து ஆனந்தமே பிரம்மம் என உணர்ந்த தவம்!",
        "characters": [
            "Bhrigu Varuni (The devoted son and seeker who performs five successive stages of Tapas)",
            "Lord Varuna (Bhrigu's father and Guru, who never spoon-feeds the answer but guides through Tapas)"
        ],
        "mahavakya_sanskrit": "यतो वा इमानि भूतानि जायन्ते । येन जातानि जीवन्ति । यत्प्रयन्त्यभिसंविशन्ति । तद्विजिज्ञासस्व । तद्ब्रह्मेति । आनन्दो ब्रह्मेति व्यजानात् ॥",
        "mahavakya_tamil_translit": "யதோ வா இமானி பூதானி ஜாயந்தே | யேன ஜாதானி ஜீவந்தி | யத்ப்ரயந்த்யபிஸம்விஸந்தி | தத்விஜிஜ்ஞாஸஸ்வ | தத்ப்ரஹ்மேதி | ஆனந்தோ ப்ரஹ்மேதி வ்யஜானாத் ||",
        "mahavakya_meaning_english": "That from which all these beings are born, by which once born they live, and into which they return and dissolve—seek to know That! That is Brahman! And Bhrigu realized: Bliss indeed is Brahman!",
        "mahavakya_meaning_tamil": "எதிலிருந்து இவ்வுயிர்கள் அனைத்தும் பிறக்கின்றனவோ, எதனால் வாழ்கின்றனவோ, எதில் மீண்டும் ஒடுங்குகின்றனவோ, அதனை அறிய விரும்புவாயாக; அதுவே பிரம்மம்! ஆனந்தமே பிரம்மம் என்று பிருகு உணர்ந்தார்!",
        "philosophical_theme": "Self-Inquiry through progressive Tapas (Tapasa Brahma Vijijnasasva); never stopping at partial truths (Food, Breath, Mind, Intellect) until realizing the Supreme Bliss (Ananda).",
        "setting_specifics": "Lord Varuna's serene coastal/riverine hermitage surrounded by sacred lotus groves, rock meditation caves, and sacrificial fire altars.",
        "metaphor_highlight": "Fivefold Tapas Ladder (Annam -> Prana -> Manas -> Vijnana -> Ananda) and the Sacred Law of Hospitality (Annam Na Nindyat, Annam Bahu Kurvita—Never scorn food, multiply food for all).",
        "scenes": [
            {
                "camera": "Slow dolly shot along a coastal Vedic hermitage where young Bhrigu bows before his majestic father Varuna.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in an ancient Vedic hermitage overlooking calm golden waters at dawn. The young sage Bhrigu in white dhoti and Rudraksha beads bows with folded hands before his dignified father and guru Varuna, who sits on a carved stone seat beside a sacred fire pit, warm sunrise glow, no text, no borders.",
                "narration_en": "Bhrigu, the illustrious son of Varuna, approached his father with deep reverence and said: 'Adhihi bhagavo brahmeti—Revered Father, teach me Brahman!' Instead of giving a ready-made answer to memorize, Varuna gave his son a cosmic compass by which he could discover the Truth for himself!",
                "narration_ta": "வருண பகவானின் புதல்வரான பிருகு முனிவர், தன் தந்தையை அணுகிப் பணிந்து, 'அதீஹி பகவோ ப்ரஹ்மேதி — பகவானே! எனக்குப் பிரம்மத்தை உபதேசியுங்கள்!' என்று வேண்டினார். தந்தை வருணனோ, விடையை உடனே சொல்லிவிடாமல், மகனே சுயமாகத் தவம் செய்து உண்மையைக் கண்டறியும் வண்ணம் பிரம்மத்தின் அடையாளத்தை மட்டும் சுட்டிக்காட்டினார்!",
                "subtitle_cue": "பிருகுவல்லி: 'பகவானே! எனக்குப் பிரம்மத்தை உபதேசியுங்கள்!' — பிருகுவின் விண்ணப்பம்.",
                "sound_cue": "Gentle ocean waves and Tanpura drone with a noble Veena opening in Raga Shankarabharanam."
            },
            {
                "camera": "Medium close-up of Varuna pointing to sprouting grain, breathing deer, and the boundless sky.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot of Sage Varuna instructing his son Bhrigu under a giant banyan tree. In the foreground, green sprouts rise from rich earth, spotted deer breathe peacefully in the morning mist, and golden sunlight bathes the hermitage. Authentic ancient Bharata aesthetic, no modern items, no text, no borders.",
                "narration_en": "Varuna declared the foundational sutra of Vedanta: 'Yato va imani bhutani jayante, yena jatani jivanti, yat prayantyabhisamvishanti—That from which all these beings are born, by which once born they live, and into which at the end they re-enter—seek to know That! That is Brahman! Go and perform Tapas—for Tapas itself is Brahman!'",
                "narration_ta": "வருண பகவான் வேதாந்தத்தின் மூல சூத்திரத்தை அருளினார்: 'யதோ வா இமானி பூதானி ஜாயந்தே... எதிலிருந்து இவ்வுயிர்கள் அனைத்தும் தோன்றுகின்றனவோ, தோன்றிய பின் எதனால் உயிர் வாழ்கின்றனவோ, இறுதியில் எதில் சென்று ஒடுங்குகின்றனவோ, அதனை அறியத் தவம் செய்வாயாக! அதுவே பிரம்மம்! தபஸா ப்ரஹ்ம விஜிஜ்ஞாஸஸ்வ — தவத்தினால் பிரம்மத்தை ஆராய்ந்து அறி!'",
                "subtitle_cue": "எதிலிருந்து உயிர்கள் தோன்றி, வாழ்ந்து, ஒடுங்குகின்றனவோ அதுவே பிரம்மம் — தவத்தால் அதனை அறி!",
                "sound_cue": "Deep Vedic chanting of 'Yato Va Imani Bhutani Jayante', accompanied by soft Mridangam."
            },
            {
                "camera": "Two-part montage of Bhrigu meditating in a quiet forest cave, contemplating first harvested grain (Annam) and then the rhythmic vital breath (Prana).",
                "veo_prompt": "16:9 8K 24fps photorealistic shot inside a serene mossy rock cave in an ancient Indian forest. Young sage Bhrigu sits in deep Padmasana meditation as shafts of golden sunlight illuminate golden ears of paddy grain and a glowing vital aura of breath around him, returning repeatedly to his father Varuna for deeper guidance, no text, no borders.",
                "narration_en": "Bhrigu went into solitude and meditated deeply. At first he saw that all bodies are born from Food, live by Food, and return to earth as Food—Annam Brahma! Yet when he returned to his father, he saw that dead matter cannot be the ultimate Source, and asked again: 'Teach me further, Father!' Each time, Varuna smiled and said only: 'Perform deeper Tapas!' Thus Bhrigu rose from Food to Vital Breath—Prano Brahma!",
                "narration_ta": "பிருகு தனிமையில் அமர்ந்து ஆழ்ந்த தவம் இயற்றினார். முதலில், எல்லா உடல்களும் அன்னத்திலிருந்து தோன்றி, அன்னத்தால் வளர்ந்து, மண்ணில் அன்னமாகவே ஒடுங்குவதைக் கண்டு 'அன்னமே பிரம்மம்' என உணர்ந்தார். ஆயினும் மனம் நிறைவடையாமல் மீண்டும் தந்தையிடம் சென்று கேட்டபோது, வருணன் 'மேலும் தவம் செய்!' என்றே அனுப்பினார். மீண்டும் தவம் செய்த பிருகு, உடலை இயக்கும் 'பிராணனே பிரம்மம்' என்ற இரண்டாம் படியை அடைந்தார்!",
                "subtitle_cue": "'மேலும் தவம் செய்!' — அன்னமய, பிராணமய கோசங்களைக் கடந்து உள்முகமாகச் சென்ற பிருகு!",
                "sound_cue": "Ascending Bansuri flute phrases symbolizing each higher rung of meditative inquiry."
            },
            {
                "camera": "Close-up of Bhrigu in deeper contemplation under starlight, passing beyond the restless waves of Mind (Manas) to the luminous lamp of Intellect (Vijnana).",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic night shot on a quiet stone terrace under a starry sky. Sage Bhrigu sits in motionless meditation beside a steady brass oil lamp whose flame does not flicker in the breeze, symbolizing the transition from restless Mind (Manas) to steady Intellect (Vijnana), no text, no subtitles, no borders.",
                "narration_en": "Still unsatisfied, for Breath itself is unconscious without a guiding thought, Bhrigu plunged into a third and fourth Tapas. He discovered first that Mind—Mano Brahma—drives all living beings; and going deeper still, he saw that determinative Intelligence—Vijnanam Brahma—directs every thought and action! Yet even the intellect is subject to change and fatigue. Once more he bowed before Varuna.",
                "narration_ta": "பிராணனும் அறிவற்ற சக்தியே என்பதை உணர்ந்த பிருகு, மூன்றாவது மற்றும் நான்காவது முறை ஆழ்ந்த தவத்தில் மூழ்கினார். முதலில் எண்ணங்களின் ஊற்றான 'மனமே பிரம்மம்' என்றும், அதற்கும் உள்ளே நிச்சயிக்கும் அறிவான 'விஞ்ஞானமே (புத்தியே) பிரம்மம்' என்றும் கண்டார்! ஆனால் புத்தியும் மாறுதலுக்கு உட்பட்டதே என்பதை உணர்ந்து, ஐந்தாவது முறையாகத் தந்தையை வணங்கினார்.",
                "subtitle_cue": "மனோமய மற்றும் விஞ்ஞானமய கோசங்களையும் கடந்து ஐந்தாம் முறை தவத்தில் ஆழ்ந்த பிருகு!",
                "sound_cue": "Sustained Rudra Veena meditation notes building toward a luminous resolution."
            },
            {
                "camera": "Breathtaking sunrise crane shot: Bhrigu's eyes shine with tears of pure ecstasy as golden light floods the cave and forest.",
                "veo_prompt": "16:9 8K 24fps photorealistic spiritual realization shot at golden sunrise. Sage Bhrigu sits in Padmasana with a radiant, blissful smile as warm golden sunrise rays flood the forest clearing and lotus pond. His father Varuna stands nearby with a look of supreme fulfilment, no text, no watermarks, no borders.",
                "narration_en": "Entering his fifth and final Tapas, Bhrigu pierced through all four outer sheaths and rested in the causeless, boundless ocean of the Self. There he realized the final truth: 'Anando Brahmeti Vyajanat—Bliss indeed is Brahman!' For from Bliss alone are all beings born; by Bliss, once born, do they live; and into Bliss do they return and merge! This is the supreme Bhargavi-Varuni Vidya, established in the highest heaven of the heart!",
                "narration_ta": "ஐந்தாவது முறையாக ஆழ்ந்த தவத்தில் நிலைபெற்ற பிருகு, நான்கு உறைகளையும் கடந்து ஆத்மாவின் எல்லையற்ற பேரானந்தக் கடலில் மூழ்கினார்! அங்கே இறுதிச் சத்தியத்தை நேரில் உணர்ந்தார்: 'ஆனந்தோ ப்ரஹ்மேதி வ்யஜானாத் — ஆனந்தமே பிரம்மம்!' ஏனெனில் ஆனந்தத்திலிருந்தே எல்லா உயிர்களும் தோன்றுகின்றன; ஆனந்தத்தாலேயே வாழ்கின்றன; இறுதியில் ஆனந்தத்திலேயே ஒடுங்குகின்றன! இதய ஆகாயத்தில் நிலைபெற்ற இந்த 'பார்கவீ வாருணீ வித்தை' பிறப்பற்ற பெருநிலையை அருளியது!",
                "subtitle_cue": "ஆனந்தோ ப்ரஹ்மேதி வ்யஜானாத் — ஆனந்தமே பிரம்மம் என்று நேரில் உணர்ந்தார் பிருகு முனிவர்!",
                "sound_cue": "Joyous, soaring flute and Veena duet in Raga Aanandabhairavi with temple bells."
            },
            {
                "camera": "Warm tracking shot of the Gurukulam Annadanam hall where sages and guests share sacred food in joyful reverence.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 wide shot of an ancient Vedic ashram Annadanam (sacred food sharing) pavilion. Disciples and sages serve wholesome steaming rice and fruits on fresh green banana leaves to visiting ascetics and villagers with folded hands and reverent smiles, warm golden sunlight, no modern objects, no text, no borders.",
                "narration_en": "Having reached the pinnacle of Bliss, did Bhrigu despise the physical world? Never! Instead, he beheld all five sheaths as sacred manifestations of the one Brahman. Thus the Upanishad proclaims the great vows of Annam: 'Annam na nindyat—Never speak ill of food! Annam na parichakshita—Never waste food! Annam bahu kurvita—Multiply food in abundance, and never turn away any guest who comes to your door!'",
                "narration_ta": "ஆனந்தப் பரம்பொருளை உணர்ந்த பின் பிருகு இவ்வுலகைப் புறக்கணித்தாரா? இல்லை! மாறாக, அன்னம் முதல் ஆனந்தம் வரை அனைத்துமே பிரம்மத்தின் வடிவங்கள் எனக் கண்டு போற்றினார். அதனாலேயே உபநிடதம் அன்னதான விரதத்தை முழங்குகிறது: 'அன்னம் ந நிந்த்யாத் — உணவை ஒருபோதும் பழிக்காதே! உணவை வீணாக்காதே! அன்னத்தை மிகுதியாகப் பெருக்குவாயாக; இல்லம் தேடி வரும் எந்த விருந்தினரையும் உணவின்றித் திருப்பி அனுப்பாதே!'",
                "subtitle_cue": "அன்னம் ந நிந்த்யாத் | அன்னம் பஹு குர்வீத — உணவைப் பழிக்காதே; அன்னதானத்தைப் பெருக்குவாயாக!",
                "sound_cue": "Warm, celebratory Mridangam and Veena harmony evoking gratitude and abundance."
            },
            {
                "camera": "Epic wide crane shot rising into the golden clouds above the ocean as Bhrigu chants the ecstatic song 'Ha Vu! Ha Vu! Ha Vu!'.",
                "veo_prompt": "Epic 16:9 8K 24fps photorealistic wide shot of Sage Bhrigu standing with raised arms on a sunlit cliff overlooking the vast golden ocean and green forests of ancient Bharata, radiating cosmic joy and oneness with all creation. Golden sunbeams pierce the clouds, zero modern items, zero text, zero borders.",
                "narration_en": "And the Taittiriya Upanishad closes with the ecstatic song of cosmic unity—the Sama of the liberated soul: 'Ha vu! Ha vu! Ha vu! Aham annam aham annadah—Oh, wonder of wonders! I am the food, and I am the eater of food! I am the poet who unites them both! I am the firstborn of Cosmic Order, earlier than the gods, the navel of Immortality, shining like the glorious Sun!'",
                "narration_ta": "தைத்திரீய உபநிடதம் ஜீவன்முக்தனின் ஆனந்த கானத்தோடு நிறைவடைகிறது: 'ஹா வு! ஹா வு! ஹா வு! ஆச்சரியம்! ஆச்சரியம்! நானே அன்னமாகவும் இருக்கிறேன், அன்னத்தை உண்பவனாகவும் இருக்கிறேன்! இரண்டையும் இணைக்கும் கவிஞனும் நானே! தேவர்களுக்கும் முற்பட்ட அமிர்தத்தின் மையமாகவும், சூரியனைப் போல் பேரொளி வீசும் பரம்பொருளாகவும் நானே திகழ்கிறேன்!'",
                "subtitle_cue": "ஹா வு! ஹா வு! ஹா வு! நானே உலகனைத்தும், நானே அமிர்தத்தின் பேரொளி! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!",
                "sound_cue": "Ecstatic Vedic Sama chant 'Ha Vu Ha Vu Ha Vu' concluding with 'Om Sham No Mitrah'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_10_AITAREYA_01",
        "muktika_number": 8,
        "upanishad_sanskrit": "ऐतरेयोपनिषद्",
        "upanishad_iast": "Aitareyopaniṣad",
        "upanishad_tamil": "ஐதரேய உபநிடதம்",
        "upanishad_english": "Aitareya Upanishad",
        "veda": "Rig Veda",
        "category": "Mukhya",
        "story_title_english": "Mahidasa Aitareya, Vamadeva in the Womb & The Cosmic Devas Choosing the Human Body",
        "story_title_tamil": "மனித உடலைத் தேர்ந்தெடுத்த தேவர்களும் கருவிலேயே ஞானம் பெற்ற வாமதேவரும்:ப்ரஜ்ஞானம் பிரம்மம்!",
        "characters": [
            "Mahidasa Aitareya (Son of Itara, the Rig Vedic Seer of the Upanishad)",
            "Atman / The Cosmic Creator (Who fashions the worlds and enters through the crown of the head)",
            "The Cosmic Devas (Agni, Vayu, Aditya, etc., seeking an abode and rejoicing at the Human Form)",
            "Rishi Vamadeva (Who realized the Immortal Self while still resting in his mother's womb)"
        ],
        "mahavakya_sanskrit": "सर्वं तत्प्रज्ञानेत्रं प्रज्ञाने प्रतिष्ठितं प्रज्ञानेत्रो लोकः प्रज्ञा प्रतिष्ठा प्रज्ञानं ब्रह्म ॥",
        "mahavakya_tamil_translit": "ஸர்வம் தத்ப்ரஜ்ஞானேத்ரம் ப்ரஜ்ஞானே ப்ரதிஷ்டிதம் ப்ரஜ்ஞானேத்ரோ லோகஃ ப்ரஜ்ஞா ப்ரதிஷ்டா ப்ரஜ்ஞானம் ப்ரஹ்ம ||",
        "mahavakya_meaning_english": "All this is guided by Consciousness and grounded in Consciousness; the world has Consciousness for its eye, and Consciousness is its foundation. Prajnanam Brahma—Consciousness is Brahman!",
        "mahavakya_meaning_tamil": "இவையனைத்தும் பேரறிவாலேயே (பிரக்ஞையால்) வழிநடத்தப்படுகின்றன; பேரறிவே உலகின் ஆதாரம். ப்ரஜ்ஞானம் பிரம்மம் — தூய பேரறிவே பிரம்மம்!",
        "philosophical_theme": "The Rig Veda Mahavakya 'Prajnanam Brahma' (Consciousness is Brahman); the preciousness of the Human Body ('Sukritam') as the temple chosen by all Devas; and Rishi Vamadeva breaking free from the hundred iron citadels of birth.",
        "setting_specifics": "Mahidasa Aitareya's Rig Vedic forest ashram transitioning into the primordial cosmic waters and the luminous entry of the Atman through the crown of the head (Vidriti).",
        "metaphor_highlight": "'Purusho vava sukritam' (The human form alone is truly well-made), Entry through the Crown (Vidriti), and the Falcon (Shyena) bursting out of a hundred iron cages (Shata Ayasih Purah).",
        "scenes": [
            {
                "camera": "Sweeping crane shot over primordial misty waters at dawn, pulling into Mahidasa Aitareya seated before the Rig Vedic fire altar.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene of an ancient Rig Vedic ashram beside a misty, boundless river at sunrise. Sage Mahidasa Aitareya, adorned in ochre cotton dhoti, sacred thread, and Rudraksha, sits in deep contemplation before a glowing Homa fire while golden light reflects across the primordial-looking waters, no text, no borders.",
                "narration_en": "In the sacred Rig Veda stands the Aitareya Upanishad, revealed to Mahidasa, son of the humble mother Itara. Contemplating the origin of all existence, the Rishi beheld the primordial truth: 'Atma va idameka evagra asit—In the beginning, all this was the One Atman alone; nothing else whatsoever winked!' That One looked within and resolved: 'Lokannu srija—Let Me now create the worlds!'",
                "narration_ta": "ரிக் வேதத்தின் மகுடமாகத் திகழும் ஐதரேய உபநிடதம், இதரா தேவியின் புதல்வரான மஹிதாஸ ஐதரேயரால் அருளப்பட்டது. படைப்பின் ஆதியைத் தியானித்த முனிவர் கண்ட சத்தியம் இதுவே: 'ஆத்மா வா இதமேக ஏவாக்ர ஆஸீத் — ஆதியில் ஆத்மா ஒன்றே தனித்திருந்தது; வேறு எதுவுமே இயங்கவில்லை!' அந்த ஏகப் பரம்பொருள் திருவுள்ளம் கொண்டு, 'இப்போது உலகங்களைப் படைப்போம்!' என்று சங்கல்பித்தது.",
                "subtitle_cue": "ஐதரேய உபநிடதம்: ஆதியில் ஆத்மா ஒன்றே தனித்திருந்தது; அதுவே உலகங்களைப் படைத்தது!",
                "sound_cue": "Deep Rig Vedic udhaatta-anudhaatta-svarita chanting over primordial water and Tanpura."
            },
            {
                "camera": "Cosmic visual sequence: luminous Devas (Fire, Wind, Sun) descending across the vast ocean of creation, looking at a cow and a horse, then rejoicing upon beholding a serene human form.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic scene in an ancient Vedic forest clearing bathed in celestial golden light. A white cow and a noble horse stand peacefully in the background, while in the center a serene human yogi sits in Padmasana. Subtle golden rays representing Agni, Vayu, and Surya descend joyful into the human figure's eyes, breath, and speech, no text, no borders.",
                "narration_en": "Having created the cosmic waters, light, earth, and the presiding Devas, the Creator fashioned first the form of a cow, and then a horse. But the Devas said: 'Not yet! These forms are not enough for us to realize the Truth.' Then the Creator brought forth the Human Form! Seeing it, the Devas cried out in joy: 'Sukritam bateti—Oh, well made indeed! Truly, the human body is a masterpiece!' Agni became Speech and entered the mouth; Vayu became Breath and entered the nostrils; the Sun became Sight and entered the eyes!",
                "narration_ta": "உலகங்களையும் தேவர்களையும் படைத்த இறைவன், தேவர்கள் தங்குவதற்காக முதலில் பசுவின் உருவத்தையும், பின்னர் குதிரையின் உருவத்தையும் காட்டினார். தேவர்கள், 'இவ்வுடல்கள் எங்களுக்குப் போதாது!' என்றனர். உடனே இறைவன் மனித உருவத்தைப் படைத்துக் காட்டினார்! அதைக் கண்ட தேவர்கள் பேருவகையுடன், 'ஸுக்ருதம் பதேதி — ஆஹா! இதுவன்றோ மிகச் சிறந்த படைப்பு!' என்று போற்றினர். அக்னி வாக்காகி வாயிலும், வாயு பிராணனாகி நாசியிலும், சூரியன் பார்வையாகிக் கண்களிலும் புகுந்தனர்!",
                "subtitle_cue": "புருஷோ வாவ ஸுக்ருதம் — மனிதப் பிறவியே இறைவனின் மிகச் சிறந்த படைப்பு எனப் போற்றிய தேவர்கள்!",
                "sound_cue": "Uplifting Veena and Bansuri fanfare celebrating the sacredness of the human temple."
            },
            {
                "camera": "Macro-to-medium shot of a golden ray of consciousness entering through the crown of the head (Brahmarandhra / Vidriti) and illuminating the heart.",
                "veo_prompt": "16:9 8K 24fps photorealistic spiritual close-up of a meditating Vedic sage in Padmasana. A single, pure beam of golden-white light descends from above and enters gently through the crown of his head (Sahasrara / Vidriti), illuminating three subtle lotus centers inside his head and heart cave, warm sacred lighting, no text, no subtitles, no borders.",
                "narration_en": "Then the Supreme Creator reflected: 'How can this body live without Me?' Cleaving open the very crown of the head—that sacred portal called Vidriti or Nandana, the Gate of Bliss—the Infinite Atman Himself entered into the human heart! Once inside, looking around at the elements, senses, and mind, did He see anything other than Brahman? No! He beheld everywhere the supreme Purusha alone and exclaimed: 'Idam adarsham—I have seen THIS!' Therefore He is called Idandra—Indra by mystic name!",
                "narration_ta": "அப்போது இறைவன் எண்ணினார்: 'நான் இன்றி இவ்வுடல் எவ்வாறு இயங்கும்?' உடனே உச்சந்தலையான பிரம்மரந்திரத்தை (வித்ருதி என்னும் ஆனந்த வாசலை) திறந்துகொண்டு, பரமாத்மாவே மனித இதயத்திற்குள் பிரவேசித்தார்! உள்ளே புகுந்த இறைவன் எங்கும் திரும்பிப் பார்த்தபோது, பிரம்மத்தைத் தவிர வேறு எதையுமே காணவில்லை! 'இதம் அதர்ஸம் — இதோ அந்தப் பூரணப் பரம்பொருளை நேரில் கண்டேன்!' என்று கூறி மகிழ்ந்ததால் அவருக்கு 'இதந்த்ரன்' (இந்திரன்) என்ற திருப்பெயர் ஏற்பட்டது!",
                "subtitle_cue": "உச்சந்தலை வழியாக மனித உடலுக்குள் புகுந்து இதயத்தில் வீற்றிருக்கும் பரமாத்மா!",
                "sound_cue": "Shimmering Swarmandal glissando and deep, resonant Shankha tone."
            },
            {
                "camera": "Dramatic metaphorical shot: a majestic white falcon (Shyena) bursting forth from dark iron bars to soar freely into the boundless golden sky.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 dramatic cinematic shot in ancient India: a magnificent white-and-gold falcon (Shyena) breaks free from an ancient dark iron cage and soars powerfully upward into the boundless golden morning sky above snow-capped mountains. Below, Sage Vamadeva meditates in radiant peace, no text, no borders.",
                "narration_en": "In the second chapter, the Upanishad reveals the three births of the soul and the glorious awakening of Rishi Vamadeva! Even while resting in his mother's womb, Vamadeva realized the Immortal Self and sang: 'For hundreds of births I was held within a hundred iron citadels of bodies; now, knowing the Self, I have burst forth with the speed of a royal falcon—Shyena—into eternal freedom!' Leaving the body later, he ascended in immortality.",
                "narration_ta": "இரண்டாம் பகுதியில், தாயின் கருவறையிலேயே பிரம்ம ஞானம் பெற்ற வாமதேவ ரிஷியின் வரலாற்றை உபநிடதம் போற்றுகிறது! கருவில் இருக்கும்போதே ஆத்மாவை உணர்ந்த வாமதேவர் பாடினார்: 'நூற்றுக்கணக்கான இரும்புக் கோட்டைகள் போன்ற உடல்களில் இத்தனை காலம் அடைபட்டிருந்தேன்; இப்போது ஆத்ம ஞானத்தால் வல்லூறுப் பறவையைப் போல் (ஷ்யேன) அக்கோட்டைகளை உடைத்துக்கொண்டு சுதந்திர வானில் பறந்துவிட்டேன்!'",
                "subtitle_cue": "நூறு இரும்புக் கோட்டைகளை உடைத்துப் பறக்கும் வல்லூறு போல் கருவிலேயே முக்தி பெற்ற வாமதேவர்!",
                "sound_cue": "Powerful percussion crescendo giving way to a soaring, liberated flute melody."
            },
            {
                "camera": "Circle of Rig Vedic disciples asking the ultimate question before Mahidasa Aitareya as the sacred fire blazes high.",
                "veo_prompt": "16:9 8K 24fps photorealistic scene in the Rig Vedic gurukulam courtyard. Disciples sit in a semicircle around Sage Mahidasa Aitareya beside a blazing Agnihotra fire pit. The sage raises his right hand in Chinmudra, his eyes shining with supreme clarity and wisdom, golden sunlight filtering through banyan leaves, no text, no borders.",
                "narration_en": "Now opens the third chapter with the ultimate inquiry: 'Ko'yam atmeti vayam upasmahe—Who is this Self whom we worship? Which of the two is the true Atman?' Is it the instrument by which one sees, hears, smells, speaks, and tastes sweet and bitter? No! Understanding, command, memory, resolve, insight, and impulse—all these are merely varying names of one underlying Reality: Prajnanam, Pure Consciousness!",
                "narration_ta": "மூன்றாம் பகுதியில் முனிவர்கள் இறுதி விசாரணையைத் தொடங்கினர்: 'கோऽயம் ஆத்மேதி வயம் உபாஸ்மஹே — நாம் வழிபடும் இந்த ஆத்மா யார்? எதனால் காண்கிறோமோ, கேட்கிறோமோ, பேசுகிறோமோ அந்தக் கருவியா?' இல்லை! புத்தி, நினைவு, சங்கல்பம், சிந்தனை, ஊக்கம் ஆகிய அனைத்துமே 'பிரக்ஞானம்' என்னும் ஒரே தூய பேரறிவின் வெவ்வேறு பெயர்களே ஆகும்!",
                "subtitle_cue": "மனம், புத்தி, நினைவு, சங்கல்பம் அனைத்திற்கும் ஆதாரமாக விளங்கும் தூய பேரறிவே ஆத்மா!",
                "sound_cue": "Deep, contemplative Rudra Veena alapana building toward the Mahavakya."
            },
            {
                "camera": "Slow crane rise from Mahidasa Aitareya's serene face to a panoramic vision of Brahma, Indra, all creatures, and the starry cosmos united in golden light.",
                "veo_prompt": "Epic 16:9 8K 24fps photorealistic crane shot rising above the Rig Vedic ashram into a golden-lit panorama of ancient rivers, forests, birds, deer, and sages—all connected by a subtle, luminous golden web of pure Consciousness (Prajnanam Brahma). Breathtaking spiritual cinematography, no text, no subtitles, no borders.",
                "narration_en": "Then Mahidasa Aitareya thundered the great Mahavakya of the Rig Veda: 'Prajnanam Brahma—Consciousness is Brahman!' This very Consciousness is Lord Brahma, Indra, Prajapati, and all the gods; It is the five great elements; It is all creatures born from eggs, wombs, sweat, and sprouts—horses, cattle, humans, and elephants, everything that breathes and walks and flies! All this is guided by Consciousness and grounded in Consciousness!",
                "narration_ta": "அப்போது மஹிதாஸ ஐதரேயர் ரிக் வேதத்தின் மகா வாக்கியத்தை முழங்கினார்: 'ப்ரஜ்ஞானம் பிரம்மம் — தூய பேரறிவே பிரம்மம்!' இந்தப் பேரறிவே பிரம்ம தேவனும், இந்திரனும், பிரஜாபதியும், தேவர்களும், பஞ்ச பூதங்களும் ஆகும்! அண்டஜம், ஜராயுஜம், ஸ்வேதஜம், உத்பிஜ்ஜம் என நால்வகைப் பிறவிகளும், குதிரைகளும், பசுக்களும், யானைகளும், மனிதர்களும், பறப்பனவும் நடப்பனவும் என அனைத்திற்கும் கண்ணாகவும் ஆதாரமாகவும் விளங்கும் இந்தப் பிரக்ஞானமே பிரம்மம்!",
                "subtitle_cue": "ப்ரஜ்ஞானம் பிரம்மம் — உலகம் அனைத்திற்கும் ஆதாரமாக விளங்கும் தூய பேரறிவே பிரம்மம்!",
                "sound_cue": "Full Vedic chorus proclaiming 'Prajnanam Brahma' with conch shell and temple gongs."
            },
            {
                "camera": "Tranquil wide final tableau of the Rig Veda Gurukulam by the river, white lotuses blooming in the golden morning light.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot of the Rig Vedic ashram along the sunlit river. Sage Mahidasa Aitareya and his disciples sit in peaceful meditation surrounded by blooming white lotuses and sacred fire smoke rising into the clear blue sky, zero modern items, zero text, zero borders.",
                "narration_en": "Riding upon this supreme vehicle of Prajnana—Pure Consciousness—Rishi Vamadeva transcended the mortal realm, fulfilled all desires in the heavenly expanse of the Self, and became immortal: 'Amritah samabhavat, amritah samabhavat!' May that sovereign Consciousness shine forever in our hearts!",
                "narration_ta": "இந்தப் பிரக்ஞானம் என்னும் பேரறிவின் துணையால் வாமதேவ முனிவர் இவ்வுலக மாயையைக் கடந்து, ஆத்ம பெருவெளியில் அனைத்து விருப்பங்களும் நிறைவேறி, மரணமற்ற அமரத்துவத்தை அடைந்தார் — 'அம்ருதஃ ஸமபவத்! அம்ருதஃ ஸமபவத்!' அந்தப் ப்ரஜ்ஞான பிரம்மம் நம் அனைவர் உள்ளத்திலும் என்றென்றும் சுடர்விடட்டும்!",
                "subtitle_cue": "ப்ரஜ்ஞானம் பிரம்மம் — பேரறிவே பிரம்மம் என உணர்ந்தவர் அமரத்துவத்தை அடைகிறார்! ஓம் சாந்திஃ!",
                "sound_cue": "Rig Veda Shanti Mantra 'Om Vang Me Manasi Pratishthita... Om Shantih Shantih Shantih'."
            }
        ]
    }
]


MUKHYA_PART3 = [
    {
        "story_id": "MUKHYA_11_CHANDOGYA_01",
        "muktika_number": 9,
        "upanishad_sanskrit": "छान्दोग्योपनिषद् (सत्यकामजाबालविद्या)",
        "upanishad_iast": "Chāndogyopaniṣad (Satyakāma Jābāla Vidyā)",
        "upanishad_tamil": "சாந்தோக்ய உபநிடதம் (சத்யகாம ஜாபாலன் கதை)",
        "upanishad_english": "Chandogya Upanishad (Story 1: Satyakama Jabala)",
        "veda": "Sama Veda",
        "category": "Mukhya",
        "story_title_english": "Satyakama Jabala & The Four-Quartered Brahman: How Fearless Truthfulness Made a True Brahmana",
        "story_title_tamil": "சத்யகாம ஜாபாலனின் உண்மை விரதம்: காளையரும் நெருப்பும் அன்னமும் உபதேசித்த பிரம்ம வித்தை!",
        "characters": [
            "Satyakama Jabala (The young seeker whose fearless honesty proved his highest spiritual qualification)",
            "Jabala (Satyakama's humble mother who served in many households during her youth)",
            "Acharya Haridrumata Gautama (The great Vedic Guru who revered truth above lineage)",
            "The Bull (Rishabha), The Sacred Fire (Agni), The White Swan (Hamsa), and The Diving Water-Bird (Madgu)"
        ],
        "mahavakya_sanskrit": "नैतदब्राह्मणो विवक्तुमर्हति समिधं सोम्याहर उप त्वा नेष्ये न सत्यादगा इति ॥",
        "mahavakya_tamil_translit": "நைததப்ராஹ்மணோ விவக்துமரஹதி ஸமிதம் ஸோம்யாஹர உப த்வா நேஷ்யே ந ஸத்யாதகா இதி ||",
        "mahavakya_meaning_english": "None but a true Brahmana could speak such fearless truth! Fetch the sacred fuel, dear boy, I shall initiate you, for you have not swerved from Truth!",
        "mahavakya_meaning_tamil": "உண்மையான பிராமணன் அன்றி வேறெவராலும் இத்தகைய ஒளிவுமறைவற்ற சத்தியத்தைப் பேச முடியாது! சமித்துக்களைக் கொண்டு வா குழந்தாய், சத்தியத்திலிருந்து நீ விலகவில்லை!",
        "philosophical_theme": "Satya (Uncompromising Truthfulness) as the supreme criterion of a Brahmana; Nature itself (Bull, Fire, Swan, Water-bird) becoming the teacher of the sixteen-part Brahman (Shodasha-Kala).",
        "setting_specifics": "Jabala's humble village cottage, Acharya Haridrumata Gautama's Gurukulam, and the wild forest pastures where Satyakama tends four hundred cows until they become a thousand.",
        "metaphor_highlight": "400 frail cows growing into 1,000 flourishing cattle, and the Four Quarters of Brahman (Prakashavan, Anantavan, Jyotishman, Ayatanavan) taught by the Bull, Fire, Swan, and Diving Bird.",
        "scenes": [
            {
                "camera": "Warm intimate shot inside a humble mud-and-thatch cottage lit by a clay lamp; young Satyakama kneels before his hardworking mother Jabala.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene inside a humble ancient Indian village hut at dawn. Young boy Satyakama in simple unstitched white cotton dhoti kneels with folded hands before his mother Jabala near a clay hearth. Morning light streams through a wooden doorway, copper pot and broom nearby, deeply moving emotional authenticity, no text, no borders.",
                "narration_en": "Desiring to live the sacred life of a Brahmachari in the Gurukulam, young Satyakama approached his mother Jabala and asked: 'Mother, what is my family lineage—my Gotra—so that I may declare it to the Acharya?' With tearful honesty, Jabala replied: 'My child, in my youth I was poor and served guests in many households when I conceived you; I do not know your Gotra. My name is Jabala, and your name is Satyakama—say simply that you are Satyakama Jabala!'",
                "narration_ta": "குருகுலத்தில் பிரம்மச்சாரியாகச் சேர்ந்து வேதம் பயில விரும்பிய சிறுவன் சத்யகாமன், தன் தாய் ஜாபாலாவிடம் சென்று, 'அம்மா! ஆச்சாரியரிடம் கூறுவதற்கு நமது கோத்திரம் எது என்று சொல்!' என்று கேட்டான். தாய் ஜாபாலா உண்மையே பேசினாள்: 'மகனே! என் இளமைக் காலத்தில் பல இடங்களில் பணிவிடை செய்து கொண்டிருந்தபோது உன்னைப் பெற்றேன்; உன் கோத்திரம் எதுவென்று எனக்குத் தெரியாது. என் பெயர் ஜாபாலா, உன் பெயர் சத்யகாமன்; ஆதலால் சத்யகாம ஜாபாலன் என்றே கூறுவாயாக!'",
                "subtitle_cue": "சாந்தோக்ய உபநிடதம்: 'என் பெயர் ஜாபாலா, உன் பெயர் சத்யகாமன்; சத்யகாம ஜாபாலன் என்றே கூறு!'",
                "sound_cue": "Tender Bansuri melody in Raga Yaman with soft Tanpura drone."
            },
            {
                "camera": "Wide tracking shot in Acharya Haridrumata Gautama's grand Gurukulam assembly; all scholars fall silent as young Satyakama speaks without hesitation.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 shot in an ancient Vedic gurukulam courtyard. Young Satyakama stands tall with folded hands before the venerable Acharya Haridrumata Gautama seated on a stone dais surrounded by many disciples. The Acharya's face beams with profound admiration and compassion as he blesses the boy, golden sunlight, no text, no borders.",
                "narration_en": "Approaching the great Acharya Haridrumata Gautama, the boy bowed and asked for initiation. When the Guru asked, 'Of what Gotra are you, my dear boy?', Satyakama did not invent a noble lie. Before the entire assembly, he repeated word for word what his mother had told him! Deeply moved, Acharya Gautama proclaimed: 'None but a true Brahmana could speak such fearless truth! Fetch the sacred fuel, my child—for you have not swerved from Satya!'",
                "narration_ta": "ஆச்சாரிய ஹரித்ருமத கௌதமரின் குருகுலத்தை அடைந்த சத்யகாமனிடம், 'குழந்தாய், உன் கோத்திரம் யாது?' என்று குரு கேட்டார். சத்யகாமன் தன் பெருமைக்காக எந்தப் பொய்யையும் புனையாமல், சபையின் நடுவே தன் தாய் கூறியதை வார்த்தை மாறாமல் அப்படியே கூறினான்! வியந்து மகிழ்ந்த ஆச்சாரியர், 'உண்மையான பிராமணன் அன்றி வேறெவராலும் இத்தகைய சத்தியத்தைப் பேச முடியாது! சத்தியத்திலிருந்து நீ வழுவவில்லை; சமித்துக்களைக் கொண்டு வா, உனக்கு உபநயனம் செய்விக்கிறேன்!' என்று போற்றினார்.",
                "subtitle_cue": "ந ஸத்யாதகா இதி — சத்தியத்திலிருந்து விலகாதவனே உண்மையான பிராமணன்!",
                "sound_cue": "Resonant Sama Veda chant and uplifting Veena chords."
            },
            {
                "camera": "Sweeping pastoral shot of Satyakama leading four hundred thin cows into a lush, sunlit Himalayan forest valley, vowing not to return until they number a thousand.",
                "veo_prompt": "16:9 8K 24fps photorealistic landscape shot in ancient India. Young Satyakama Jabala in saffron-bordered dhoti and carrying a wooden staff leads a herd of white Vedic cattle into a lush emerald forest valley beside a sparkling mountain river. Golden morning mist rises over the trees, no text, no subtitles, no borders.",
                "narration_en": "After initiating him, the Guru entrusted four hundred lean, weak cows to Satyakama's care. Filled with devotion, the youth led them into the deep forest and made a solemn vow: 'I shall not return to the Gurukulam until these four hundred cows have multiplied and flourished into a full thousand!' For years he lived in the wilderness, serving the cattle with love and meditating in silence.",
                "narration_ta": "உபநயனத்திற்குப் பின், மெலிந்த நானூறு பசுக்களைச் சத்யகாமனிடம் ஒப்படைத்தார் குருதேவர். அவற்றைப் பராமரிக்கக் காட்டிற்குள் ஓட்டிச் சென்ற சத்யகாமன், 'இந்த நானூறு பசுக்களும் செழித்துப் பெருகி ஆயிரம் பசுக்களாக ஆகும் வரை நான் திரும்ப மாட்டேன்!' என்று சபதம் ஏற்றான். பல ஆண்டுகள் காட்டிலேயே தங்கி, பசுக்களை அன்புடன் பேணி, தனிமையில் ஆழ்ந்த தவம் இயற்றினான்.",
                "subtitle_cue": "நானூறு பசுக்கள் ஆயிரமாகப் பெருகும் வரை காட்டிலேயே தங்கித் தவம் இயற்றிய சத்யகாமன்!",
                "sound_cue": "Peaceful pastoral flute melody, cowbells chiming softly, flowing forest stream."
            },
            {
                "camera": "Majestic golden hour shot: when the herd reaches a thousand, the great white Bull (Rishabha) steps forward at sunset, followed by the blazing night campfire (Agni).",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic twilight shot in a forest clearing. A magnificent white Vedic Bull (Rishabha) with curved horns stands before young Satyakama beside a blazing night campfire under a starry sky. Golden firelight illuminates Satyakama's reverent face as nature itself reveals cosmic wisdom, no text, no borders.",
                "narration_en": "When the cows had grown to a thousand, the cosmos itself came forward to initiate the truthful youth! First, the mighty Bull of the herd called out: 'Satyakama! We have reached a thousand; lead us home. Let me teach you the First Quarter of Brahman—Prakashavan, the Shining! East, West, South, and North are its four parts.' That night by the campfire, Agni himself taught the Second Quarter—Anantavan, the Endless—comprising Earth, Sky, Heaven, and the Ocean!",
                "narration_ta": "பசுக்கள் ஆயிரமாகப் பெருகிய நன்னாளில், இயற்கையே குருவாக வந்து சத்யகாமனுக்கு உபதேசித்தது! முதலில் மந்தையின் கம்பீரமான காளை (ரிஷபம்) அழைத்து, 'சத்யகாமா! கிழக்கு, மேற்கு, தெற்கு, வடக்கு ஆகிய நான்கு திசைகளைக் கொண்ட ப்ரகாசவான் (ஒளிமயமானது) என்னும் பிரம்மத்தின் முதல் பாதத்தை உனக்குக் கூறுகிறேன்!' என்றது. அன்றிரவு அக்னி பகவான் தோன்றி, பூமி, அந்தரிக்ஷம், சுவர்க்கம், சமுத்திரம் ஆகிய நான்கு கலைகள் கொண்ட 'அனந்தவான்' என்னும் இரண்டாம் பாதத்தை உபதேசித்தார்!",
                "subtitle_cue": "காளை 'ப்ரகாசவான்' பாதத்தையும், அக்னி 'அனந்தவான்' பாதத்தையும் சத்யகாமனுக்கு உபதேசித்தன!",
                "sound_cue": "Deep resonant horn tone, crackling sacred fire, and mystical Veena arpeggios."
            },
            {
                "camera": "Dawn on the forest river: a radiant white Swan (Hamsa) alights by the fire, followed by a Diving Water-Bird (Madgu) skimming across the sunlit water.",
                "veo_prompt": "16:9 8K 24fps photorealistic dawn shot by a forest river. A luminous white swan (Hamsa) and a diving water-bird (Madgu) rest near young Satyakama as golden sunrise rays illuminate his eyes, nostrils, and heart with subtle golden light. Pure spiritual harmony with nature, no text, no subtitles, no borders.",
                "narration_en": "On the third evening, a radiant white Swan—Hamsa—flew down and revealed the Third Quarter of Brahman: Jyotishman, the Effulgent, consisting of Fire, Sun, Moon, and Lightning! And on the fourth day, a diving water-bird—Madgu—revealed the Fourth Quarter right within his own body: Ayatanavan, the Abode-Possessing, consisting of Breath, Eye, Ear, and Mind!",
                "narration_ta": "மூன்றாம் நாள் மாலையில் வெண்ணிற அன்னப் பறவை (ஹம்ஸம்) பறந்து வந்து, அக்னி, சூரியன், சந்திரன், மின்னல் ஆகிய நான்கு கலைகள் கொண்ட 'ஜ்யோதிஷ்மான்' என்னும் மூன்றாம் பாதத்தை உபதேசித்தது! நான்காம் நாள் நீர்க்கோழி (மத்கு) தோன்றி, நம் உடலுக்குள்ளேயே பிராணன், கண், காது, மனம் ஆகிய நான்கிலும் உறைகின்ற 'ஆயதனவான்' என்னும் நான்காம் பாதத்தை உபதேசித்தது!",
                "subtitle_cue": "அன்னப் பறவை 'ஜ்யோதிஷ்மான்' பாதத்தையும், நீர்க்கோழி 'ஆயதனவான்' பாதத்தையும் உபதேசித்தன!",
                "sound_cue": "Graceful wing-flutters, rippling river water, and soaring Bansuri in Raga Hamsadhvani."
            },
            {
                "camera": "Dramatic close-up as Satyakama returns to the Gurukulam with a thousand cows; Acharya Gautama gazes in awe at the golden Brahma-Tejas shining on the youth's face.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium close-up at the entrance of the Vedic gurukulam. Young Satyakama returns leading a thousand healthy white cows; his face glows with unmistakable golden spiritual effulgence (Brahma-Tejas). Acharya Haridrumata Gautama looks at him in joyful wonder and clasps his shoulders, no text, no borders.",
                "narration_en": "When Satyakama returned to the Gurukulam with a thousand cattle, Acharya Gautama took one look at his radiant face and exclaimed: 'Brahma-vid iva vai somya भासि, ko nu tva anushashasa—My dear boy, your face shines like one who already knows Brahman! Who has taught you?' Satyakama replied humbly: 'Beings other than men have taught me, revered Master; yet I desire that you yourself speak this truth to me, for knowledge received from the Guru alone reaches perfection!'",
                "narration_ta": "ஆயிரம் பசுக்களுடன் குருகுலத்திற்குத் திரும்பிய சத்யகாமனின் முகத்தில் வீசிய பிரம்ம தேஜஸைக் கண்ட ஆச்சாரியர், 'ப்ரஹ்மவித் இவ வை ஸோம்ய பாஸி — குழந்தாய்! பிரம்மத்தை அறிந்தவனைப் போல் உன் முகம் ஒளிவீசுகிறதே! உனக்கு உபதேசித்தது யார்?' என்று வியந்து கேட்டார். சத்யகாமன் பணிவுடன், 'மனிதர்கள் அல்லாத இயற்கை சக்திகள் எனக்கு உபதேசித்தன; ஆயினும் ஆச்சாரியரின் திருவாக்கால் கேட்கும் வித்தையே முழுமையடையும் என்பதால், நீங்களே எனக்கு அருள வேண்டும்!' என்று வேண்டினான்.",
                "subtitle_cue": "'பிரம்மத்தை அறிந்தவன் போல் உன் முகம் ஒளிவீசுகிறதே!' — குருவின் திருவாக்கால் முழுமை பெற்ற ஞானம்!",
                "sound_cue": "Rich Violin and Veena unison celebrating Guru-Bhakti and Brahma-Tejas."
            },
            {
                "camera": "Wide sunlit tableau of Acharya Gautama formally initiating Satyakama into the highest mystery of the Sixteen-Part Brahman before the entire Gurukulam.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot in the Sama Veda gurukulam. Acharya Gautama sits beside the blazing sacred fire, formally imparting the final Upadesha to the radiant Satyakama Jabala while disciples and white cattle rest peacefully in the golden morning light, zero modern items, zero text, zero borders.",
                "narration_en": "Then Acharya Gautama taught him that very same Sixteen-Part Brahman, leaving nothing out—'Na kinchana vicyavayam chakara!' Thus Satyakama Jabala, born of a humble mother, became one of the greatest Brahma-Rishis of the Upanishads, proving forever that Truthfulness and Devotion are the true lineage of the Soul!",
                "narration_ta": "அப்போது ஆச்சாரிய கௌதமர், பதினாறு கலைகள் கொண்ட அந்தப் பிரம்ம வித்தையை எதுவும் விடுபடாமல் முழுமையாகச் சத்யகாமனுக்கு உபதேசித்தார்! எளிய தாய்க்குப் பிறந்த சத்யகாம ஜாபாலன், தன் சத்திய விரதத்தாலும் குரு பக்தியாலும் உபநிடத காலத்தின் மாபெரும் பிரம்மரிஷியாக உயர்ந்தார்!",
                "subtitle_cue": "சத்திய விரதமும் குரு பக்தியுமே பிரம்ம ஞானத்தின் உண்மையான தகுதி! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!",
                "sound_cue": "Sama Veda Shanti Mantra 'Om Apyayantu Mamangani' in full resonant chorus."
            }
        ]
    },
    {
        "story_id": "MUKHYA_12_CHANDOGYA_02",
        "muktika_number": 9,
        "upanishad_sanskrit": "छान्दोग्योपनिषद् (उद्दालक-श्वेतकेतु संवादः)",
        "upanishad_iast": "Chāndogyopaniṣad (Uddālaka-Śvetaketu Saṃvādaḥ)",
        "upanishad_tamil": "சாந்தோக்ய உபநிடதம் (உத்தாலகர் - சுவேதகேது: தத் த்வம் அஸி)",
        "upanishad_english": "Chandogya Upanishad (Story 2: Svetaketu & Uddalaka Aruni)",
        "veda": "Sama Veda",
        "category": "Mukhya",
        "story_title_english": "Svetaketu, the Banyan Seed & the Salt in Water: The Ninefold Revelation of 'Tat Tvam Asi'",
        "story_title_tamil": "ஆலமர விதையும் நீரில் கரைந்த உப்பும்: சுவேதகேதுவுக்கு அருளப்பட்ட 'தத் த்வம் அஸி' மகா வாக்கியம்!",
        "characters": [
            "Uddalaka Aruni (The illumined father and Guru of the Sama Veda)",
            "Svetaketu Aruneya (His 24-year-old son who returned from 12 years of study proud and stiff-necked, then humbled himself)"
        ],
        "mahavakya_sanskrit": "स य एषोऽणिमैतदात्म्यमिदं सर्वं तत्सत्यं स आत्मा तत्त्वमसि श्वेतकेतो इति ॥",
        "mahavakya_tamil_translit": "ஸ ய ஏஷோऽணிமைததாத்ம்யமிதம் ஸர்வம் தத்ஸத்யம் ஸ ஆத்மா தத்த்வமஸி ஸ்வேதகேதோ இதி ||",
        "mahavakya_meaning_english": "That which is this subtle essence—in That has all this universe its Self; That is the Truth; That is the Atman; Tat Tvam Asi—Thou Art That, O Svetaketu!",
        "mahavakya_meaning_tamil": "இந்த நுண்ணிய சாரப் பொருள் எதுவோ, அதுவே இப்பிரபஞ்சம் அனைத்திற்கும் ஆதாரமான ஆத்மா; அதுவே சத்தியம்; சுவேதகேதுவே, தத் த்வம் அஸி — அதுவே நீயாக இருக்கிறாய்!",
        "philosophical_theme": "The Sama Veda Mahavakya 'Tat Tvam Asi' (Thou Art That) repeated nine times; Cause and Effect non-difference (Clay & Pots, Gold & Ornaments); the Invisible Essence in the Banyan Seed and Salt in Water.",
        "setting_specifics": "Sage Uddalaka Aruni's shady hermitage courtyard with a giant Nyagrodha (Banyan) tree, clay pots, copper water bowls, and rock salt.",
        "metaphor_highlight": "One lump of clay knowing all clay pots (Mrittika), Splitting the tiny Banyan seed (Nyagrodha Phala), and Rock salt dissolved in water (Lavana Udaka).",
        "scenes": [
            {
                "camera": "Medium tracking shot of 24-year-old Svetaketu walking into his father's ashram with an arrogant, scholarly stride, carrying stacks of palm leaves.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in an ancient Indian forest ashram. Twenty-four-year-old Svetaketu, dressed in crisp white cotton dhoti and carrying palm-leaf manuscripts, walks in with a proud, scholarly posture. His wise father Sage Uddalaka Aruni sits calmly on a wooden seat by the porch, observing his son with gentle compassion, no text, no borders.",
                "narration_en": "Sent to the Gurukulam at age twelve, Svetaketu studied all the Vedas for twelve years and returned home at twenty-four—proud, stiff-necked, and fancying himself supremely learned! Seeing his son's intellectual arrogance, his father Sage Uddalaka Aruni asked gently: 'Svetaketu, my dear, since you are so proud and consider yourself so learned, did you ask your teachers for that Instruction—Adesha—by which the unheard becomes heard, the unthought becomes thought, and the unknown becomes known?'",
                "narration_ta": "பன்னிரண்டு வயதில் குருகுலம் சென்ற சுவேதகேது, பன்னிரண்டு ஆண்டுகள் அனைத்து வேதங்களையும் கற்றுத் தேர்ந்து இருபத்து நான்கு வயதில் வீடு திரும்பினான். தான் எல்லாம் அறிந்த பண்டிதன் என்ற கல்விச் செருக்கு அவனிடம் நிறைந்திருந்தது! அதைக் கண்ட தந்தை உத்தாலக ஆருணி, 'சுவேதகேது! இவ்வளவு கர்வத்துடன் இருக்கிறாயே, எதைக் கேட்டால் கேட்காத அனைத்தும் கேட்டதாகவும், அறியாத அனைத்தும் அறிந்ததாகவும் ஆகுமோ, அந்த ஆதேச உபதேசத்தைக் கேட்டாயா?' என்று வினவினார்.",
                "subtitle_cue": "சாந்தோக்ய உபநிடதம்: 'எதை அறிந்தால் அறியாத அனைத்தும் அறிந்ததாகுமோ, அதைக் கேட்டாயா?'",
                "sound_cue": "Proud, brisk Veena rhythm suddenly pausing on an inquiring, open Tanpura note."
            },
            {
                "camera": "Close-up of clay pots, gold ornaments, and iron tools arranged on a stone table before Uddalaka and the now-humbled Svetaketu.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot in the ashram courtyard. Sage Uddalaka Aruni holds a single lump of raw wet river clay in one hand while pointing to various baked earthen pots, golden ornaments, and iron implements on a stone slab. Young Svetaketu sits humbly on the ground listening intently, warm morning light, no text, no borders.",
                "narration_en": "Humbled, Svetaketu asked: 'How can there be such an instruction, Father?' Uddalaka explained with three immortal examples: 'Yatha somya ekena mritpindena sarvam mrinmayam vijnatam syat—Just as by knowing one lump of clay, all pots made of clay are known! For the modification—the pot—is merely a name arising from speech (Vacharambhanam vikaro namadheyam); the truth is that it is Clay alone! So too with one nugget of gold and one piece of iron!'",
                "narration_ta": "திகைத்துப்போன சுவேதகேது, 'அப்படியொரு உபதேசம் எப்படி இருக்க முடியும் தந்தையே? நீங்களே எனக்குக் கூறுங்கள்!' என்று பணிந்தான். உத்தாலகர் மூன்று உவமைகளால் விளக்கினார்: 'குழந்தாய்! ஒரேயொரு களிமண் கட்டியை அறிந்தால், மண்ணால் செய்யப்பட்ட குடம், சட்டி என அனைத்துப் பாத்திரங்களின் உண்மையும் அறியப்பட்டுவிடும்! ஏனெனில் குடம், சட்டி என்பவை வாக்கினால் சொல்லப்படும் வெறும் பெயர்களும் வடிவங்களுமே (வாசாரம்பணம் விகாரோ நாமதேயம்); மண் என்பது மட்டுமே சத்தியம்!'",
                "subtitle_cue": "வாசாரம்பணம் விகாரோ நாமதேயம் — வடிவங்கள் வெறும் பெயர்களே; மூலப் பொருளான சத்தே உண்மை!",
                "sound_cue": "Gentle clay-pot Ghatam percussion interweaving with melodic Veena notes."
            },
            {
                "camera": "Wide shot of the towering Nyagrodha (Banyan) tree; Svetaketu brings a single red banyan fig and splits its tiny seed with a copper needle.",
                "veo_prompt": "16:9 8K 24fps photorealistic macro-to-wide shot under a colossal, centuries-old Indian Banyan tree (Nyagrodha) with aerial roots. Young Svetaketu kneels before his father Uddalaka, holding a split red banyan fig and using a fine copper pin to divide a single microscopic seed on his palm. Golden sunlight streams through the canopy, no text, no borders.",
                "narration_en": "Then Uddalaka pointed to the towering Banyan tree above them: 'Bring me a fruit from that Nyagrodha tree.' 'Here it is, Father.' 'Break it open. What do you see?' 'Tiny seeds, Father.' 'Break open one of those tiny seeds. Now what do you see inside?' Svetaketu peered closely and said: 'Na kinchana, Bhagavah—I see nothing at all inside, Revered Sir!'",
                "narration_ta": "பின்னர் அங்கிருந்த பிரம்மாண்டமான ஆலமரத்தைக் காட்டி உத்தாலகர் கூறினார்: 'அந்த ஆலமரத்திலிருந்து ஒரு பழத்தைக் கொண்டு வா.' சுவேதகேது கொண்டு வந்தான். 'அதைப் பிளந்து பார், என்ன தெரிகிறது?' 'மிகச் சிறிய விதைகள் தெரிகின்றன தந்தையே.' 'அதில் ஒரு சிறிய விதையை இரண்டாகப் பிளந்து பார்; இப்போது உள்ளே என்ன தெரிகிறது?' சுவேதகேது உற்றுப் பார்த்துவிட்டு, 'ந கிஞ்சன பகவஃ — உள்ளே ஒன்றுமே தெரியவில்லை தந்தையே!' என்றான்.",
                "subtitle_cue": "'ஆலமரத்தின் நுண்ணிய விதையைப் பிளந்து பார்; உள்ளே என்ன தெரிகிறது?' — 'ஒன்றுமே தெரியவில்லை தந்தையே!'",
                "sound_cue": "Delicate rustling of banyan leaves and a quiet, suspenseful Bansuri solo."
            },
            {
                "camera": "Tilt-up from the invisible center of the split seed on Svetaketu's palm to the massive, sky-filling canopy of the ancient Banyan tree.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic tilt-up shot from a tiny split banyan seed glowing faintly on Svetaketu's open palm up into the colossal, sun-drenched trunk and sprawling branches of the ancient banyan tree. Sage Uddalaka raises his hand in Chinmudra, proclaiming Tat Tvam Asi, no text, no subtitles, no borders.",
                "narration_en": "Uddalaka spoke words that shake the very foundations of materialism: 'My dear child, that subtle essence inside the seed which your eyes cannot see—from that very invisible subtle essence stands this gigantic Banyan tree! Have faith, my child! In that subtle essence has all this universe its Self; That is the Truth; That is the Atman; Tat Tvam Asi, Svetaketo—Thou Art That, O Svetaketu!'",
                "narration_ta": "அப்போது உத்தாலகர் மெய்ம்மறக்கச் செய்யும் சத்தியத்தை வெளியிட்டார்: 'குழந்தாய்! எந்த நுண்ணிய சாரத்தை உன் கண்களால் பார்க்க முடியவில்லையோ, அந்தக் கண்ணுக்குத் தெரியாத நுண்ணிய சக்தியிலிருந்துதான் இத்தனை பெரிய ஆலமரம் எழுந்து நிற்கிறது! சிரத்தை கொள் மகனே! அந்த நுண்ணிய சாரமே இப்பிரபஞ்சம் அனைத்திற்கும் ஆத்மா; அதுவே சத்தியம்; சுவேதகேதுவே, தத் த்வம் அஸி — அதுவே நீயாக இருக்கிறாய்!'",
                "subtitle_cue": "கண்ணுக்குத் தெரியாத அந்த நுண்ணிய சாரமே இப்பெரிய ஆலமரம் — தத் த்வம் அஸி (அதுவே நீ)!",
                "sound_cue": "Majestic Sama Veda proclamation of 'Tat Tvam Asi' with resonant Tanpura and temple bell."
            },
            {
                "camera": "Evening to morning sequence: Svetaketu drops a crystal of rock salt into a bowl of water at night; at dawn the water is clear, and he sips from top, middle, and bottom.",
                "veo_prompt": "16:9 8K 24fps photorealistic close-up sequence in the Vedic ashram. Svetaketu holds a copper bowl of crystal-clear water into which rock salt has completely dissolved overnight. Under his father's guidance, he sips a drop from the surface, the middle, and the bottom, his eyes widening in realization as the invisible salt pervades every drop, no text, no borders.",
                "narration_en": "Still Svetaketu asked: 'If that Pure Being is everywhere, why do I not see It?' Uddalaka told him: 'Place this crystal of salt in water and come to me tomorrow morning.' At dawn, the Guru said: 'Bring me the salt you put in the water.' Svetaketu reached in, but it had vanished! 'Sip from the top—how does it taste?' 'Salty!' 'Sip from the middle!' 'Salty!' 'Sip from the bottom!' 'Salty!' 'Just so, my child, though you do not see Sat with your eyes, It pervades every atom of your being—Tat Tvam Asi!'",
                "narration_ta": "சுவேதகேது மீண்டும் கேட்டான்: 'பரம்பொருள் எங்கும் நிறைந்திருந்தால் என் கண்ணுக்கு ஏன் தெரிவதில்லை?' உத்தாலகர் ஒரு கல் உப்பை நீரில் போட்டு மறுநாள் காலையில் வரச் சொன்னார். காலையில், 'நீரில் போட்ட உப்பை எடுத்து வா' என்றார். உப்பு கரைந்து மறைந்திருந்தது! 'மேலேயுள்ள நீரைச் சுவைத்துப் பார், எப்படியிருக்கிறது?' 'உப்பாக இருக்கிறது!' 'நடுவிலும் அடியிலும் சுவைத்துப் பார்!' 'எங்கும் உப்பாகவே இருக்கிறது!' 'அதுபோலவே மகனே, கண்ணுக்குத் தெரியாவிட்டாலும் சத் என்னும் பரம்பொருள் எங்கும் நிறைந்துள்ளது — தத் த்வம் அஸி!'",
                "subtitle_cue": "நீரில் கரைந்த உப்பு கண்ணுக்குத் தெரியாவிட்டாலும் எங்கும் நிறைந்திருப்பது போல் உள்ள ஆத்மா — தத் த்வம் அஸி!",
                "sound_cue": "Rippling water sounds and luminous Violin melody in Raga Kalyani."
            },
            {
                "camera": "Dramatic tracking shot in a dense forest: a compassionate sage unties the blindfold from a lost traveler from Gandhara and points him toward home.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 cinematic scene in an ancient Indian forest. A compassionate Vedic Acharya gently unties a cloth blindfold from the eyes of a weary traveler who had been left bound in the woods, pointing him toward a sunlit highway leading to Gandhara. Immediate relief and joy on the traveler's face, no text, no borders.",
                "narration_en": "How then does a soul bound in ignorance find its way back to that Self? Uddalaka gave the parable of the Man from Gandhara: 'Suppose robbers blindfold a man from Gandhara and leave him in a desolate forest; he cries out until a compassionate knower unties his blindfold and points the way home! Asking from village to village, he reaches Gandhara. Even so, a seeker who finds an illumined Acharya has the blindfold of ignorance removed—Acharyavan purusho veda!'",
                "narration_ta": "அறியாமையில் கட்டுண்ட ஜீவன் எவ்வாறு தன் சுய நிலையை அடைவது? உத்தாலகர் 'காந்தார தேசத்து மனிதன்' உவமையைக் கூறினார்: 'கள்வர்களால் கண்கள் கட்டப்பட்டுக் காட்டில் விடப்பட்ட காந்தார தேசத்து மனிதன் தவிக்கும்போது, கருணையுள்ள ஒருவர் அவனது கண்கட்டை அவிழ்த்து வழிகாட்டுவது போல், ஆச்சாரியனை அடைந்தவனின் அறியாமைக் கட்டு அவிழ்க்கப்பட்டு அவன் ஆத்ம வீட்டை அடைகிறான் — ஆசார்யவான் புருஷோ வேத!'",
                "subtitle_cue": "ஆசார்யவான் புருஷோ வேத — சற்குருவை அடைந்தவனே அறியாமைக் கட்டு நீங்கி மெய்ப்பொருளை அறிகிறான்!",
                "sound_cue": "Moving Bansuri melody transitioning from minor-key longing to joyous major-key liberation."
            },
            {
                "camera": "Wide golden-hour shot under the Banyan tree: Svetaketu bows at his father's feet as the ninefold refrain 'Tat Tvam Asi' echoes across the forest.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot under the giant Banyan tree at golden hour. Svetaketu, now completely free of pride and glowing with non-dual realization, bows at the feet of his father Sage Uddalaka Aruni. Sacred fire smoke rises gently into the golden canopy, zero modern elements, zero text, zero borders.",
                "narration_en": "Nine times Sage Uddalaka repeated the supreme Mahavakya of the Sama Veda—'Tat Tvam Asi, Svetaketo—Thou Art That!'—and nine times he removed every layer of doubt until young Svetaketu realized: 'Vijnatam, Bhagavah—I have realized It, Revered Father!'",
                "narration_ta": "ஒன்பது முறை வெவ்வேறு உவமைகளின் வழியே 'தத் த்வம் அஸி ஸ்வேதகேதோ — சுவேதகேதுவே, அந்தப் பரம்பொருளே நீ!' என்ற சாம வேத மகா வாக்கியத்தை தந்தை உத்தாலகர் உபதேசித்தார். இறுதியில் கல்விச் செருக்கு அழிந்து, 'தந்தையே, அந்தப் பரம்பொருளை முழுமையாக உணர்ந்துகொண்டேன்!' என்று பேரானந்தத்தில் நிலைபெற்றான் சுவேதகேது!",
                "subtitle_cue": "தத் த்வம் அஸி ஸ்வேதகேதோ — சுவேதகேதுவே, அந்தப் பரம்பொருளே நீ! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!",
                "sound_cue": "Nine-fold harmonic chime and Sama Veda chorus chanting 'Tat Tvam Asi'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_13_CHANDOGYA_03",
        "muktika_number": 9,
        "upanishad_sanskrit": "छान्दोग्योपनिषद् (सनत्कुमार-नारद भूमाविद्या)",
        "upanishad_iast": "Chāndogyopaniṣad (Sanatkumāra-Nārada Bhūmāvidyā)",
        "upanishad_tamil": "சாந்தோக்ய உபநிடதம் (நாரதர் - சனத்குமாரர்: பூமா வித்தை)",
        "upanishad_english": "Chandogya Upanishad (Story 3: Narada & Sanatkumara - Bhuma Vidya)",
        "veda": "Sama Veda",
        "category": "Mukhya",
        "story_title_english": "Narada's Sorrow & Sanatkumara's Bhuma Vidya: Why Only the Infinite Brings True Joy",
        "story_title_tamil": "மந்திரங்களை மட்டுமே அறிந்த நாரதரும் சனத்குமாரரின் பூமா வித்தையும்: எல்லையற்றதே பேரின்பம்!",
        "characters": [
            "Devarishi Narada (Master of 64 arts and all Vedas, yet still afflicted by sorrow)",
            "Bhagavan Sanatkumara / Skanda (The eternally youthful Lord of Wisdom who teaches Bhuma Vidya)"
        ],
        "mahavakya_sanskrit": "यो वै भूमा तत्सुखं नाल्पे सुखमस्ति भूमैव सुखं भूमा त्वेव विजिज्ञासितव्य इति ॥",
        "mahavakya_tamil_translit": "யோ வை பூமா தத்ஸுகம் நால்பே ஸுகமஸ்தி பூமைவ ஸுகம் பூமா த்வேவ விஜிஜ்ஞாஸிதவ்ய இதி ||",
        "mahavakya_meaning_english": "That which is the Infinite (Bhuma) is true Bliss; there is no bliss in the finite (Alpa). The Infinite alone is Bliss, and the Infinite alone must be sought and realized!",
        "mahavakya_meaning_tamil": "எது எல்லையற்ற பூரணமோ (பூமாவோ) அதுவே பேரின்பம்; அற்பமான சிற்றெல்லையில் இன்பமில்லை. பூமாவே ஆனந்தம்; அந்தப் பூமாவையே ஆராய்ந்து அறிய வேண்டும்!",
        "philosophical_theme": "Transcending mere encyclopedic scholarship ('Mantravid eväsmi natmavit') to reach Atma-Vidya; climbing the 15 rungs from Name (Nama) to Vital Breath (Prana) and finally to Bhuma (The Infinite).",
        "setting_specifics": "A radiant celestial-forest tapovanam near Mount Kailasa/Ganga where Devarishi Narada holding his Mahati Veena bows before the youthful sage Sanatkumara.",
        "metaphor_highlight": "'Mantravid eväsmi natmavit' (Knowing only words/mantras, not the Self), the 15-step ladder of contemplation, and Bhuma vs. Alpa (The Infinite vs. the Finite).",
        "scenes": [
            {
                "camera": "Poignant dolly shot of Devarishi Narada carrying his Mahati Veena, walking with bowed head toward the luminous forest seat of Bhagavan Sanatkumara.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in a sacred Himalayan lotus grove at sunrise. Devarishi Narada, dressed in white silk dhoti with Rudraksha malas and holding his carved wooden Mahati Veena, bows humbly before the eternally youthful, radiant sage Sanatkumara seated on a white lotus rock platform, golden morning mist, no text, no borders.",
                "narration_en": "Even the greatest celestial sage, Devarishi Narada, once approached Bhagavan Sanatkumara in deep humility and cried: 'Adhihi Bhagavah—Teach me, O Lord!' Sanatkumara asked: 'First tell me what you already know, and then I shall teach you what lies beyond.' Narada recited a staggering catalog of sixty-four sciences—the four Vedas, Itihasa-Purana, mathematics, astronomy, music, and logic!",
                "narration_ta": "தேவரிஷி நாரதர் ஒருமுறை பகவான் சனத்குமாரரை அணுகிப் பணிந்து, 'பகவானே! எனக்கு ஆத்ம உபதேசம் அருளுங்கள்!' என்று வேண்டினார். சனத்குமாரர், 'நீ இதுவரை அறிந்தவற்றை முதலில் கூறு; அதன் பின் அதற்கு மேலானதை உனக்குக் கூறுகிறேன்' என்றார். நாரதர் தான் கற்ற ரிக், யஜுர், சாம, அதர்வண வேதங்கள், இதிகாச புராணங்கள், கணிதம், வானியல், இசை என அறுபத்து நான்கு கலைகளையும் பட்டியலிட்டார்!",
                "subtitle_cue": "சாந்தோக்ய உபநிடதம்: அறுபத்து நான்கு கலைகளையும் கற்ற நாரதர் சனத்குமாரரைச் சரணடைந்த கதை!",
                "sound_cue": "Melancholic yet noble Mahati Veena solo played by Narada over a deep Tanpura."
            },
            {
                "camera": "Close-up of Narada's tear-filled eyes as he confesses the limitation of mere book-learning.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 close-up of Devarishi Narada kneeling with folded hands beside his Veena. A single tear of spiritual longing glistens on his cheek as he looks up at the serene, compassionate face of youthful Sage Sanatkumara. Warm golden morning light, authentic Vedic aesthetic, no text, no subtitles, no borders.",
                "narration_en": "Then Narada uttered the confession that pierces every scholar's heart: 'So'ham bhagavo mantravid evasmi natmavit—Revered Lord, with all this vast learning, I am merely a knower of words and mantras, NOT a knower of the Atman! I have heard from great sages like you that only the knower of the Self crosses beyond sorrow (Tarati shokam atmavit). Yet I am still afflicted by sorrow! Pray, carry me across to the further shore of grief!'",
                "narration_ta": "அத்தனை கல்வியையும் கூறிவிட்டு நாரதர் கண்கலங்கி உரைத்த வார்த்தை ஒவ்வொரு பண்டிதரின் உள்ளத்தையும் உலுக்குவதாகும்: 'ஸோऽஹம் பகவோ மந்த்ரவித் ஏவாஸ்மி நாத்மவித் — பகவானே! இத்தனை சாஸ்திரங்களைக் கற்றும் நான் வெறும் வார்த்தைகளையும் மந்திரங்களையும் அறிந்தவனாகவே இருக்கிறேன்; ஆத்மாவை அறிந்தவனாக இல்லை! ஆத்மாவை அறிந்தவனே துக்கத்தைக் கடக்கிறான் (தரதி சோகமாத்மவித்) என்று கேள்விப்பட்டிருக்கிறேன்; என் துயரத்தைக் களைந்து என்னைக் கரையேற்றுங்கள்!'",
                "subtitle_cue": "மந்த்ரவித் ஏவாஸ்மி நாத்மவித் — நான் மந்திரங்களை மட்டுமே அறிந்தவன், ஆத்மாவை அறிந்தவனல்லன்!",
                "sound_cue": "Deep, emotional Violin phrase in Raga Subhapantuvarali."
            },
            {
                "camera": "Upward tracking shot along fifteen carved granite steps leading up a sunlit mountain terrace as Sanatkumara guides Narada step by step.",
                "veo_prompt": "16:9 8K 24fps photorealistic tracking shot of Sage Sanatkumara and Narada ascending a monumental flight of fifteen ancient carved granite steps bathed in golden sunlight amidst Himalayan pines. At each step, golden light intensifies, symbolizing the ascent from Name (Nama) and Speech (Vak) to Mind (Manas) and Prana, no text, no borders.",
                "narration_en": "Sanatkumara replied: 'Whatever you have studied so far is Nama—mere Name! Meditate on Name, yet know that Speech is greater than Name; Mind is greater than Speech; Resolve (Sankalpa) is greater than Mind; Intelligence (Chitta), Meditation (Dhyana), Understanding (Vijnana), Strength, Food, Water, Fire, Space, Memory, and Hope are each greater than the last—until you reach Prana, the Vital Life-Breath upon which all is strung like a gem upon a thread!'",
                "narration_ta": "சனத்குமாரர் கூறினார்: 'நாரதா! நீ இதுவரை கற்றவையனைத்தும் வெறும் பெயரே (நாமம்)! பெயரை விட வாக்கு பெரியது; வாக்கை விட மனம் பெரியது; மனதை விட சங்கல்பம் பெரியது; அதனை விட சித்தம், தியானம், விஞ்ஞானம், வலிமை, அன்னம், நீர், தேஜஸ், ஆகாயம், நினைவு, நம்பிக்கை எனப் படிப்படியாக உயர்ந்து, இவையனைத்தையும் நூலில் மணிகள் போல் தாங்கி நிற்கும் பிராணனே பெரியது!' என்று பதினைந்து படிகளில் நாரதரின் அறிவை உயர்த்தினார்.",
                "subtitle_cue": "நாமம் முதல் பிராணன் வரை பதினைந்து படிகளில் நாரதரின் சிந்தனையை உயர்த்திய சனத்குமாரர்!",
                "sound_cue": "Fifteen ascending swara steps on Veena and Bansuri, rising in pitch and grandeur."
            },
            {
                "camera": "Dramatic pause at the fifteenth step: Narada bows again and asks what lies even beyond Prana, opening the door to Satya and Bhuma.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic medium shot at the summit of the granite terrace. Devarishi Narada pauses and looks with keen inquiry at Bhagavan Sanatkumara, asking for the ultimate truth beyond even Prana. Behind them, the clouds part to reveal an infinite, shoreless golden sky, no text, no subtitles, no borders.",
                "narration_en": "Any ordinary student would have stopped at Prana, satisfied. But Sanatkumara saw that Narada longed for the Ultimate, and declared: 'He alone speaks the highest truth—Ativadi—who declares the Supreme Satya! To know Truth, one must reflect; to reflect, one must have faith; to have faith, one must have single-pointed devotion; and to act, one must experience true Bliss—Sukham!'",
                "narration_ta": "பிராணனோடு நின்றுவிடாமல், அதற்கும் மேலான 'சத்தியப் பரம்பொருளை' உரைப்பவனே உண்மையான அதிவாதி என்று சனத்குமாரர் வழிகாட்டினார்! 'சத்தியத்தை அறிய விஞ்ஞானம் வேண்டும்; அதற்குச் சிந்தனை வேண்டும்; சிந்தனைக்குச் சிரத்தை வேண்டும்; சிரத்தைக்கு நிஷ்டை வேண்டும்; நிஷ்டைக்குச் செயல் வேண்டும்; எவன் பேரின்பத்தை (சுகத்தை) அனுபவிக்கிறானோ அவனே செயல்படுகிறான்!' என்றார்.",
                "subtitle_cue": "பிராணனையும் கடந்து நிற்கும் பரம சத்தியம் மற்றும் பேரின்பத்தை (சுகத்தை) நோக்கிய பயணம்!",
                "sound_cue": "Rhythmic Mridangam crescendo resolving into an expansive, serene drone."
            },
            {
                "camera": "Epic panoramic crane shot expanding from a tiny puddle of water in a cow's hoofprint to the boundless, horizonless golden ocean and sky.",
                "veo_prompt": "Breathtaking 16:9 8K 24fps photorealistic crane shot starting on a tiny puddle of water in a rock depression, then rising rapidly to reveal a boundless, infinite golden ocean meeting the endless sky at sunrise. Sanatkumara and Narada sit on the cliff edge in radiant stillness, symbolizing Alpa (finite) vs Bhuma (Infinite), no text, no borders.",
                "narration_en": "Narada asked: 'What then is that true Bliss, O Lord?' Sanatkumara proclaimed the immortal Mahavakya of Bhuma Vidya: 'Yo vai bhuma tat sukham, nalpe sukham asti, bhumaiva sukham! That which is the Infinite—Bhuma—is true Bliss! There is no real happiness in the finite, the small, the limited! The Infinite alone is Bliss, for the finite is mortal, whereas the Infinite is forever Immortal!'",
                "narration_ta": "'பகவானே! அந்த உண்மையான பேரின்பம் (சுகம்) எது?' என்று நாரதர் கேட்டார். சனத்குமாரர் பூமா வித்தையின் அமர வாக்கியத்தை முழங்கினார்: 'யோ வை பூமா தத் ஸுகம், நால்பே ஸுகமஸ்தி, பூமைவ ஸுகம்! எது எல்லையற்ற பூரணமோ (பூமாவோ) அதுவே பேரின்பம்! அற்பமான சிற்றெல்லையில் (அல்பத்தில்) உண்மையான இன்பம் ஒருபோதும் இல்லை! ஏனெனில் அற்பமானது அழியக்கூடியது; எல்லையற்ற பூமாவோ அழியாத அமிர்தம்!'",
                "subtitle_cue": "யோ வை பூமா தத் ஸுகம் நால்பே ஸுகமஸ்தி — எல்லையற்ற பூமாவே பேரின்பம்; அற்பத்தில் இன்பமில்லை!",
                "sound_cue": "Full-throated Vedic chant of 'Yo Vai Bhuma Tat Sukham' with conch and temple bells."
            },
            {
                "camera": "360-degree slow rotation around Narada and Sanatkumara as golden light fills below, above, behind, before, right, and left.",
                "veo_prompt": "16:9 8K 24fps photorealistic 360-degree spiritual realization shot on a Himalayan peak. Golden-white light radiates equally below, above, behind, in front, to the right, and to the left of Devarishi Narada as he enters non-dual Samadhi, seeing nothing other than the Infinite Self anywhere, no text, no subtitles, no borders.",
                "narration_en": "'And what is the mark of that Bhuma?' asked Narada. Sanatkumara answered: 'Yatra nanyat pashyati, nanyachchhrinoti, nanyad vijanati sa bhuma! Where one sees nothing else, hears nothing else, understands nothing else separate from the Self—that is Bhuma, the Infinite! And upon what does that Infinite rest? Sve mahimni—upon Its own glory, or rather, not even upon glory! For the Self is below, the Self is above, the Self is behind and before—the Self alone is all this universe!'",
                "narration_ta": "'அந்தப் பூமாவின் இலக்கணம் யாது?' என்று நாரதர் கேட்டார். சனத்குமாரர் அருளினார்: 'யத்ர நான்யத் பஸ்யதி, நான்யச் ச்ருணோதி, நான்யத் விஜானாதி ஸ பூமா! எங்கே ஒருவன் தன்னிலிருந்து வேறாக எதையும் காண்பதில்லையோ, கேட்பதில்லையோ, அறிவதில்லையோ அதுவே பூமா! அது எதன் மேல் நிற்கிறது? தன்னுடைய சொந்த மகிமையிலேயே நிற்கிறது! கீழேயும் ஆத்மாவே, மேலேயும் ஆத்மாவே, முன்னும் பின்னும் வலமும் இடமும் எங்கும் நிறைந்திருப்பது இந்த ஆத்மா ஒன்றே!'",
                "subtitle_cue": "யத்ர நான்யத் பஸ்யதி... எங்கே இரண்டாவதாக எதையும் காண்பதில்லையோ அதுவே எல்லையற்ற பூமா!",
                "sound_cue": "Celestial Mahati Veena and Bansuri duet in Raga Bhairavi, boundless and serene."
            },
            {
                "camera": "Wide closing shot of Devarishi Narada standing liberated and radiant, strumming his Veena as Bhagavan Sanatkumara — known as Skanda — blesses him.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot of Devarishi Narada bowing in ecstatic gratitude before Bhagavan Sanatkumara (Skanda) in the sunlit Himalayan grove. All knots of sorrow in Narada's heart have dissolved into radiant golden peace, zero modern elements, zero text, zero borders.",
                "narration_en": "'Ahara-shuddhau sattva-shuddhih—When nourishment of the senses is pure, the heart becomes pure; when the heart is pure, memory of the Self becomes steady; and when memory is steady, all the knots of the heart are untied!' Thus Bhagavan Sanatkumara—whom the wise call Lord Skanda—carried pure-hearted Narada across to the further shore beyond all darkness!",
                "narration_ta": "'ஆஹார சுத்தௌ ஸத்த்வ சுத்திஃ — புலன் நுகர்வான ஆகாரம் தூய்மையடையும்போது சித்தம் தூய்மையடைகிறது; சித்தம் தூய்மையடைந்தால் ஆத்ம நினைவு நிலைபெறுகிறது; அப்போது இதயத்தின் அறியாமை முடிச்சுகள் அனைத்தும் அவிழ்ந்துவிடுகின்றன!' இவ்வாறு குமாரக் கடவுளான பகவான் சனத்குமாரர் (ஸ்கந்தன்), நாரதரை இருளின் மறுகரைக்குக் கரையேற்றினார்!",
                "subtitle_cue": "சித்தம் தூய்மையடைந்தால் இதயத்தின் முடிச்சுகள் அனைத்தும் அவிழ்ந்து பிறவித் துயர் நீங்கும்!",
                "sound_cue": "Joyful Sama Veda Shanti Mantra and Narada's Veena fading into eternal peace."
            }
        ]
    },
    {
        "story_id": "MUKHYA_14_CHANDOGYA_04",
        "muktika_number": 9,
        "upanishad_sanskrit": "छान्दोग्योपनिषद् (इन्द्र-विरोचन प्रजापतिविद्या)",
        "upanishad_iast": "Chāndogyopaniṣad (Indra-Virocana Prajāpatividyā)",
        "upanishad_tamil": "சாந்தோக்ய உபநிடதம் (இந்திரன் - விரோசனன்: பிரஜாபதியின் ஆத்ம உபதேசம்)",
        "upanishad_english": "Chandogya Upanishad (Story 4: Indra & Virochana before Prajapati)",
        "veda": "Sama Veda",
        "category": "Mukhya",
        "story_title_english": "Indra, Virochana & The Reflection in the Water Pan: 101 Years of Inquiry into the Immortal Self",
        "story_title_tamil": "இந்திரனும் விரோசனனும் நீரில் கண்ட பிரதிபலிப்பும்: 101 ஆண்டுகள் தவம் செய்து ஆத்மாவை உணர்ந்த கதை!",
        "characters": [
            "Lord Prajapati (The Creator and Supreme Preceptor of Devas and Asuras)",
            "Indra (King of the Devas, who refused to settle for partial truths and completed 101 years of Tapas)",
            "Virochana (King of the Asuras, who mistook the physical body's reflection for the Atman)"
        ],
        "mahavakya_sanskrit": "य आत्मापहतपाप्मा विजरो विमृत्युर्विशोको विजिघत्सोऽपिपासः सत्यकामः सत्यसङ्कल्पः सोऽन्वेष्टव्यः स विजिज्ञासितव्यः ॥",
        "mahavakya_tamil_translit": "ய ஆத்மாபஹதபாப்மா விஜரோ விம்ருத்யுர் விஸோகோ விஜிஹத்ஸோऽபிபாஸஃ ஸத்யகாமஃ ஸத்யஸங்கல்பஃ ஸோऽன்வேஷ்டவ்யஃ ஸ விஜிஜ்ஞாஸிதவ்யஃ ||",
        "mahavakya_meaning_english": "The Self which is free from sin, free from old age, death, and grief, free from hunger and thirst, whose desires and resolves are ever true—That Self must be sought out and realized!",
        "mahavakya_meaning_tamil": "பாவமற்றதும், மூப்பும் மரணமும் துக்கமும் அற்றதும், பசியும் தாகமும் அற்றதும், சத்திய காமமும் சத்திய சங்கல்பமும் கொண்டதுமான அந்த ஆத்மாவையே தேடி அறிய வேண்டும்!",
        "philosophical_theme": "The Danger of Dehatma-Buddhi (Materialism/Body-worship practiced by Virochana) vs. Persevering Viveka (Indra's 32 + 32 + 32 + 5 = 101 years of inquiry through Waking, Dream, Deep Sleep, and the Bodiless Immortal Self).",
        "setting_specifics": "Lord Prajapati's grand celestial-forest hermitage featuring a wide brass pan filled with still water (Udaka-Sharava) where Indra and Virochana gaze at their reflections.",
        "metaphor_highlight": "Reflection in a pan of water (Udaka-Sharava), Blind/Crippled reflection when the body is blind/crippled, and the Chariot-horse / Mortal Body as merely the temporary seat of the Bodiless Immortal Spirit.",
        "scenes": [
            {
                "camera": "Wide symmetrical shot of Lord Prajapati's ashram: Indra (king of Devas) and Virochana (king of Asuras) arrive simultaneously carrying firewood in their hands.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in an ancient celestial Vedic ashram. Two royal seekers—Indra in serene golden silk dhoti and Virochana in rich crimson silk—arrive carrying bundles of samit firewood humbly before the venerable four-headed/sage-like Lord Prajapati seated beside a sacred fire altar, golden morning light, no text, no borders.",
                "narration_en": "Once, Lord Prajapati proclaimed the supreme glory of the Self: 'The Atman, which is free from sin, free from old age, death, sorrow, hunger, and thirst—he who realizes that Self obtains all worlds and all desires!' Hearing this, both the Devas and the Asuras longed for that Self. Indra, King of the Gods, and Virochana, King of the Asuras, approached Prajapati with firewood in their hands and lived thirty-two years in silent Brahmacharya!",
                "narration_ta": "ஒருமுறை பிரஜாபதி முழங்கினார்: 'பாவமற்றதும், மூப்பு, மரணம், துக்கம், பசி, தாகம் அற்றதுமான ஆத்மாவை எவன் அறிகிறானோ, அவன் எல்லா உலகங்களையும் எல்லா விருப்பங்களையும் அடைகிறான்!' இதைக் கேட்ட தேவர்களும் அசுரர்களும் அந்த ஆத்மாவை அறிய விரும்பினர். தேவர்களின் தலைவன் இந்திரனும், அசுரர்களின் தலைவன் விரோசனனும் சமித்துக்களைக் கையில் ஏந்தி பிரஜாபதியிடம் வந்து முப்பத்திரண்டு ஆண்டுகள் பிரம்மச்சரிய விரதம் பூண்டு வாழ்ந்தனர்!",
                "subtitle_cue": "சாந்தோக்ய உபநிடதம்: ஆத்மாவை அறிய பிரஜாபதியிடம் 32 ஆண்டுகள் தவம் இருந்த இந்திரனும் விரோசனனும்!",
                "sound_cue": "Grand Sama Veda opening chant with dual Veena harmonies."
            },
            {
                "camera": "Overhead and eye-level shot of Indra and Virochana richly adorned in royal crowns and garlands, peering into a wide brass pan of still water.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot in Prajapati's sunlit courtyard. Indra and Virochana, adorned in fine silk garments, gold necklaces, and flower garlands, kneel on opposite sides of a wide polished brass pan filled with still water (Udaka-Sharava), gazing down at their reflections while Sage Prajapati watches them closely, no text, no borders.",
                "narration_en": "After thirty-two years, Prajapati tested their discrimination. He pointed to the person seen inside the eye and in a mirror, and told them: 'Go, adorn yourselves in your finest ornaments, shave and dress well, and look into a pan of water!' When they looked into the water-pan, Prajapati asked: 'What do you see?' Both cried out: 'We see our entire self reflected right down to the hair and nails!' Prajapati said: 'That is the Immortal, Fearless Brahman!'",
                "narration_ta": "முப்பத்திரண்டு ஆண்டுகளுக்குப் பின் பிரஜாபதி அவர்களின் விவேகத்தைச் சோதிக்க எண்ணி, 'கண்ணுக்குள்ளும் நீரிலும் தெரியும் புருஷனே ஆத்மா! நீங்கள் சிறந்த ஆபரணங்களையும் ஆடைகளையும் அணிந்துகொண்டு, ஒரு பாத்திரத்தில் உள்ள நீரில் உங்கள் உருவத்தைப் பாருங்கள்!' என்றார். இருவரும் நீரில் பார்த்துவிட்டு, 'நகக்கண் முதல் தலைமுடி வரை எங்கள் உருவம் முழுமையாகத் தெரிகிறது!' என்றனர். 'அதுவே அபயமான அமிர்தப் பிரம்மம்!' என்று கூறி அவர்களை அனுப்பினார் பிரஜாபதி.",
                "subtitle_cue": "நீர்ப் பாத்திரத்தில் தெரிந்த உடலின் பிரதிபலிப்பையே ஆத்மா எனக் காட்டிய பிரஜாபதியின் சோதனை!",
                "sound_cue": "Shimmering water chimes with a subtle, questioning undertone on the Rudra Veena."
            },
            {
                "camera": "Split path shot: Virochana marches arrogantly back to the Asuras praising the physical body, while Indra stops under a banyan tree on the forest road, deep in thought.",
                "veo_prompt": "16:9 8K 24fps photorealistic cinematic frame along an ancient forest road. In the distance, Virochana strides away proudly toward his city; in the foreground, Indra stops beneath a banyan tree, looking at his reflection in a forest pool and examining his own mortal hands in deep philosophical reflection, turning back toward the ashram, no text, no borders.",
                "narration_en": "Watching them depart without questioning, Prajapati sighed: 'Alas, they go without having realized the true Self!' Virochana returned to the Asuras with a satisfied heart and preached materialism: 'The physical body alone is to be worshiped and pampered here!'—and thus even today, one without faith or charity is called Asuric. But before Indra reached the Devas, he stopped on the road and reflected: 'Wait! If this reflection is the Self, then when the body goes blind, lame, or dies, this reflection also perishes! I see no joy in this!'",
                "narration_ta": "விசாரணையின்றிச் செல்லும் அவர்களைப் பார்த்து பிரஜாபதி, 'உண்மையான ஆத்மாவை உணராமலேயே செல்கிறார்களே!' என்று வருந்தினார். விரோசனன் அசுரர்களிடம் சென்று, 'இந்தப் பருவுடலே ஆத்மா! உடலை அலங்கரித்து இன்பம் நுகர்வதே முக்தி!' என்று தேகாத்ம வாதத்தைப் போதித்தான். ஆனால் இந்திரனோ வழியிலேயே நின்று சிந்தித்தான்: 'இவ்வுடல் குருடானால் பிரதிபலிப்பும் குருடாகிறது; உடல் அழிந்தால் இதுவும் அழிந்துவிடுமே! இதில் எனக்கு எந்த நன்மையும் தெரியவில்லையே!' என்று கூறி மீண்டும் பிரஜாபதியிடம் திரும்பினான்.",
                "subtitle_cue": "விரோசனன் உடலையே ஆத்மா என மயங்கினான்; இந்திரனோ உண்மையைத் தேடி மீண்டும் குருவிடம் திரும்பினான்!",
                "sound_cue": "Heavy, pompous drums fading away into a thoughtful, clear Bansuri solo as Indra turns back."
            },
            {
                "camera": "Montage of Indra spending a second 32 years and a third 32 years in Prajapati's ashram, examining the Dream state (Svapna) and Deep Sleep (Sushupti).",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic shot inside Prajapati's ashram over decades of austerity. Indra, now dressed as a humble tapasvi in simple white cotton dhoti without royal ornaments, sits before Sage Prajapati by the sacred fire, contemplating the states of dream and deep sleep with unwavering perseverance, no text, no borders.",
                "narration_en": "Returning with firewood in hand, Indra lived a second thirty-two years with Prajapati! First Prajapati pointed to the Dreaming Self, which moves freely even if the body is lame. Yet Indra reflected again: 'Even in dreams one weeps, feels chased, and suffers pain!' Returning for a third thirty-two years—ninety-six years in all!—Prajapati pointed to Deep Dreamless Sleep. Again Indra paused: 'In deep sleep, one does not even know 'I am this', nor any beings; it is like utter annihilation! I see no joy here either!'",
                "narration_ta": "மீண்டும் சமித்து ஏந்தி வந்த இந்திரனை மேலும் முப்பத்திரண்டு ஆண்டுகள் தவம் இருக்கச் செய்த பிரஜாபதி, கனவில் உலவும் புருஷனே ஆத்மா என்றார். ஆனால் கனவிலும் அழுகையும் பயமும் துன்பமும் இருப்பதை உணர்ந்த இந்திரன், மூன்றாவது முறையாக முப்பத்திரண்டு ஆண்டுகள் தவம் இருந்தான்! அப்போது ஆழ்ந்த உறக்க நிலையைக் காட்டினார் பிரஜாபதி. அதிலும், 'நான் யார் என்றே அறியாத சூன்யம்போல் தோன்றுகிறதே!' என்று உணர்ந்து, மீண்டும் பிரஜாபதியின் திருவடிகளைச் சரணடைந்தான்.",
                "subtitle_cue": "விழிப்பு, கனவு, ஆழ்ந்த உறக்கம் ஆகிய மூன்று நிலைகளையும் ஆராய்ந்து 96 ஆண்டுகள் தவம் செய்த இந்திரன்!",
                "sound_cue": "Deep meditative progression of Tanpura, Veena, and slow Pakhawaj rhythms across the decades."
            },
            {
                "camera": "Luminous sunrise shot: after five final years (101 years total), Prajapati reveals the Bodiless Immortal Self using the metaphor of Wind, Lightning, and Space.",
                "veo_prompt": "16:9 8K 24fps photorealistic spiritual climax shot in Prajapati's ashram at sunrise. After 101 years of austerity, Sage Prajapati places his hand on Indra's heart as the sky above blazes with golden sunlight dissolving dark clouds and lightning. Indra's entire being radiates pure, bodiless light, no text, no subtitles, no borders.",
                "narration_en": "Seeing Indra's unyielding quest for Truth, Prajapati kept him for five final years—making a hundred and one years of Tapas—and unveiled the supreme Siddhanta: 'Maghavan, martyam va idam shariram—O Indra, mortal indeed is this physical body, held by death; yet it is the dwelling-place of that Immortal, Bodiless Atman! As long as one identifies with the body, there is no freedom from pleasure and pain; but for the Bodiless Witness, pleasure and pain cannot touch It at all!'",
                "narration_ta": "இந்திரனின் தளராத சத்திய தாகத்தைக் கண்ட பிரஜாபதி, மேலும் ஐந்தாண்டுகள் — மொத்தம் நூற்றியோரு ஆண்டுகள் — தவத்திற்குப் பின் பரம ரகசியத்தை உபதேசித்தார்: 'மகவானே! இந்தப் பருவுடல் மரணத்திற்கு உட்பட்டது; ஆனால் அழிவற்றதும் உடலற்றதுமான (அசரீர) அமிர்த ஆத்மா தங்கியிருக்கும் இருப்பிடம் இதுவே! உடலோடு தன்னை இணைத்துக்கொள்பவனுக்கே இன்ப-துன்பங்கள் உண்டு; உடலற்ற சாட்சியாய் ஒளிரும் ஆத்மாவை இன்பமும் துன்பமும் ஒருபோதும் தீண்டுவதில்லை!'",
                "subtitle_cue": "நூற்றியோரு ஆண்டுகள் தவத்திற்குப் பின் 'உடலற்ற அமிர்த ஆத்மா'வின் ரகசியத்தை உபதேசித்த பிரஜாபதி!",
                "sound_cue": "Triumphant Shankha blow and soaring Violin-Flute symphony in Raga Hamsanadam."
            },
            {
                "camera": "Macro focus on Indra's serene eye, showing that the eye is merely the instrument for the Unseen Seer behind it.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 extreme close-up of Indra's serene, awakened eye reflecting the golden morning sun and the sacred fire, pulling back slowly to show him seated in blissful Samadhi beside Lord Prajapati. Pure divine light, no text, no watermarks, no borders.",
                "narration_en": "'Just as the wind is bodiless, and clouds, lightning, and thunder are bodiless until they rise into the supreme light of the sun and appear in their own radiance—so this Serene Being, rising above identification with the mortal body, reaches the Supreme Light and appears in Its own true form! He who knows 'Let me smell this' is the Atman; the nose is only the instrument! He who knows 'Let me think this' is the Atman; the mind is only His divine eye!'",
                "narration_ta": "'காற்றும், மேகமும், மின்னலும், இடியும் உடலற்றவையாய் இருந்து, சூரிய ஒளியில் சேரும்போது தத்தம் சுய ஒளியுடன் பரிணமிப்பது போல், இவ்வுடல் அபிமானத்தைக் கடந்த சம்பிரசாதன் என்னும் ஆத்மா, பரஞ்ஜோதியை அடைந்து தன் சுயரூபத்தில் ஒளிர்கிறான்! முகர்வதும், பேசுவதும், கேட்பதும், மனமாகிய தெய்வீகக் கண்ணால் சிந்திப்பதும் அந்த ஆத்மாவே; புலன்கள் வெறும் கருவிகளே!'",
                "subtitle_cue": "புலன்கள் வெறும் கருவிகளே; அவற்றின் பின்னால் நின்று அறியும் உடலற்ற பேரொளியே ஆத்மா!",
                "sound_cue": "Crystal-clear Swarmandal harp and sustained high-octave Bansuri note."
            },
            {
                "camera": "Wide celestial-forest closing tableau: Indra teaching the Devas and Rishis as the entire universe rejoices in the peace of the Atman.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot of the Vedic ashram bathed in golden morning light. Illumined Indra bows to Sage Prajapati and shares the wisdom of the Immortal Self with assembled sages and Devas, while white lotuses bloom in the tranquil water pan, zero modern items, zero text, zero borders.",
                "narration_en": "Thus Indra brought this supreme Brahmavidya to the Devas and the Rishis. And the Chandogya Upanishad concludes its final verse with the eternal vow of Ahimsa and Self-realization: 'He who establishes all his senses in the Self, practices non-injury toward all living beings, and beholds the Immortal Atman, attains the Supreme World of Brahman and never returns again—Na cha punar avartate, na cha punar avartate!'",
                "narration_ta": "இவ்வாறு நூற்றியோரு ஆண்டுகள் தவம் செய்து பெற்ற இந்த ஆத்ம வித்தையைத் தேவர்களுக்கும் முனிவர்களுக்கும் வழங்கினார் இந்திரன். சாந்தோக்ய உபநிடதம் இறுதி மந்திரத்தில் வாழ்த்துகிறது: 'புலன்களை ஆத்மாவில் நிலைநிறுத்தி, எவ்வுயிருக்கும் தீங்கு செய்யாத அஹிம்சை விரதத்துடன் ஆத்மாவை உணர்பவன், பிரம்ம லோகத்தை அடைந்து மீண்டும் பிறவிச் சுழலில் திரும்புவதே இல்லை — ந ச புனராவர்த்ததே! ந ச புனராவர்த்ததே!'",
                "subtitle_cue": "ந ச புனராவர்த்ததே — ஆத்மாவை உணர்ந்தவன் மீண்டும் பிறவிச் சுழலில் திரும்புவதே இல்லை! ஓம் சாந்திஃ!",
                "sound_cue": "Grand Sama Veda finale 'Na Cha Punar Avartate... Om Apyayantu Mamangani'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_15_CHANDOGYA_05",
        "muktika_number": 9,
        "upanishad_sanskrit": "छान्दोग्योपनिषद् (रैक्व-जानश्रुति संवर्गविद्या)",
        "upanishad_iast": "Chāndogyopaniṣad (Raikva-Jānaśruti Saṃvargavidyā)",
        "upanishad_tamil": "சாந்தோக்ய உபநிடதம் (வண்டி இழுக்கும் ரைக்கவரும் மன்னன் ஜானஸ்ருதியும்)",
        "upanishad_english": "Chandogya Upanishad (Story 5: Raikva the Cart-Driver & King Janashruti)",
        "veda": "Sama Veda",
        "category": "Mukhya",
        "story_title_english": "Raikva under the Bullock Cart & King Janashruti: Why Two Flying Swans Praised a Humble Sage Above an Emperor",
        "story_title_tamil": "மாட்டு வண்டியின் கீழ் அமர்ந்திருந்த ரைக்கவரும் மன்னன் ஜானஸ்ருதியும்: இரண்டு அன்னப் பறவைகள் புகழ்ந்த பிரம்ம ஞானி!",
        "characters": [
            "King Janashruti Pautrayana (A generous emperor who built rest-houses everywhere, yet realized charity without Self-knowledge is incomplete)",
            "Two Celestial Swans (Hamsas flying across the night sky comparing Janashruti and Raikva to the dice throws Krita and Traya)",
            "Kshattri (The King's royal charioteer/chamberlain who searched for Raikva)",
            "Sage Raikva with the Cart (Sayugva Raikva, resting contentedly beneath his wooden bullock cart)"
        ],
        "mahavakya_sanskrit": "वायुर्वाव संवर्गो यदा वा अग्निरुद्वायति वायुमेवाप्येति । प्राणो वाव संवर्गः स यदा स्वपिति प्राणमेव वागप्येति ॥",
        "mahavakya_tamil_translit": "வாயுர்வாவ ஸம்வர்கோ யதா வா அக்னிருத்வாயதி வாயுமேவாப்யேதி | ப்ராணோ வாவ ஸம்வர்கஃ ஸ யதா ஸ்வபிதி ப்ராணமேவ வாகப்யேதி ||",
        "mahavakya_meaning_english": "Vayu (the Cosmic Wind) is indeed the Great Absorber outside, into which Fire, Sun, Moon, and Water merge; and Prana (the Vital Breath) is the Great Absorber within, into which Speech, Eye, Ear, and Mind merge!",
        "mahavakya_meaning_tamil": "அண்டத்தில் வாயுவே அனைத்தையும் தன்னுள் ஒடுக்கும் 'ஸம்வர்கன்' (அக்னி, சூரியன், சந்திரன், நீர் வாயுவில் ஒடுங்குகின்றன); பிண்டத்தில் பிராணனே வாக்கு, கண், காது, மனம் அனைத்தையும் தன்னுள் ஒடுக்கும் ஸம்வர்கன்!",
        "philosophical_theme": "Philanthropy (Dana) alone is subordinate to Brahmavidya; a realized sage sitting under a dusty bullock cart encompasses all the merit of the universe, just as the winning throw of four (Krita) absorbs all smaller numbers.",
        "setting_specifics": "King Janashruti's moonlit palace roof, giant Annachathram rest-houses, and the dusty village roadside where Sage Raikva sits beneath a wooden bullock cart.",
        "metaphor_highlight": "Two Swans conversing in the moonlight, the Winning Dice Throw 'Krita' (4) absorbing smaller throws (3, 2, 1), and Samvarga Vidya (Cosmic Wind and Vital Breath as the Great Absorbers).",
        "scenes": [
            {
                "camera": "Wide moonlit shot of King Janashruti resting on the open marble terrace of his palace while two luminous white swans fly overhead across the starry sky.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic night scene on an ancient Indian royal sandstone palace terrace bathed in silver moonlight. King Janashruti in fine royal silk dhoti rests on a carved couch, looking up in astonishment as two luminous white swans (Hamsas) fly gracefully across the starry sky above, conversing in the night air, no text, no borders.",
                "narration_en": "King Janashruti Pautrayana was a ruler of immense charity and faith. He built vast rest-houses—Annachathrams—in every direction, declaring: 'Everywhere people shall eat of my food!' One night, as the King rested on his moonlit palace roof, two celestial swans flew overhead. One swan warned the other: 'Hey Bhallaksha! Fly carefully! Do not touch the fiery glory of King Janashruti, which spreads wide like the sky!'",
                "narration_ta": "ஜானஸ்ருதி பௌத்ராயணன் என்னும் மன்னன் மாபெரும் தர்மவான்; எங்கும் அன்னதான சத்திரங்களைக் கட்டி, 'எல்லா திசைகளிலும் மக்கள் என் உணவை உண்ணட்டும்!' என்று வாரி வழங்கினான். ஓர் இரவு நிலவொளியில் தன் அரண்மனை மாடத்தில் மன்னன் படுத்திருந்தபோது, வானில் பறந்து சென்ற இரண்டு அன்னப் பறவைகளில் ஒன்று மற்றொன்றைப் பார்த்து, 'பல்லாக்ஷா! மன்னன் ஜானஸ்ருதியின் தர்ம தேஜஸ் வானம் வரை பரவியுள்ளது, அதன் மேல் பட்டுவிடாமல் எச்சரிக்கையாகப் பறந்து வா!' என்றது.",
                "subtitle_cue": "சாந்தோக்ய உபநிடதம்: அன்னதான மன்னன் ஜானஸ்ருதியும் வானில் பறந்த இரு அன்னப் பறவைகளும்!",
                "sound_cue": "Serene night Raga Chandrakauns on Bansuri, fluttering swan wings in the moonlight."
            },
            {
                "camera": "Close-up of the second swan turning in mid-air and King Janashruti rising from his couch in deep humility and curiosity.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium close-up on the moonlit palace terrace. King Janashruti rises from his royal couch with folded hands, deeply humbled and awakened as he listens to the two white swans disappearing into the starlit horizon. Brass oil lamps flicker gently in the night breeze, no text, no subtitles, no borders.",
                "narration_en": "The second swan laughed gently and replied: 'Kam vara enam etat santam sayugvanam iva Raikvam attha—How can you speak of this mere king as though he were equal to Sage Raikva with the bullock cart? Why, just as in the game of dice the winning throw of Krita absorbs all smaller throws, so all the good deeds performed by every creature in this world are absorbed into the supreme wisdom of Raikva!' Hearing this, the King could not sleep a wink all night!",
                "narration_ta": "உடனே இரண்டாவது அன்னம் சிரித்துக்கொண்டே கேட்டது: 'ஏன் இம்மன்னனை மாட்டு வண்டிக்காரரான பிரம்ம ஞானி ரைக்கவருக்கு இணையாகப் பேசுகிறாய்? பகடை ஆட்டத்தில் கிருதம் (நான்கு) என்ற வெற்றி எண் விழுந்தால் மற்ற சிறிய எண்கள் அனைத்தும் அதில் அடங்கிவிடுவது போல், உலகில் எல்லா உயிர்களும் செய்யும் புண்ணியங்கள் அனைத்தும் ரைக்கவரின் பிரம்ம ஞானத்திற்குள்ளேயே அடங்கிவிடுகின்றனவே!' இதைக் கேட்ட மன்னன் இரவு முழுவதும் உறங்காமல் ரைக்கவரைப் பற்றியே சிந்தித்தான்!",
                "subtitle_cue": "'மாட்டு வண்டிக்காரரான பிரம்ம ஞானி ரைக்கவருக்கு இம்மன்னன் ஈடாவானா?' — இரண்டாம் அன்னத்தின் மொழி!",
                "sound_cue": "Expressive Veena glissando and gentle night breeze."
            },
            {
                "camera": "Sunlit tracking shot of the royal chamberlain searching Gurukulams in vain, then finding Sage Raikva sitting peacefully in the shade beneath a dusty wooden bullock cart.",
                "veo_prompt": "16:9 8K 24fps photorealistic sunlit scene on the outskirts of an ancient Indian village. A royal messenger in ornate attire stops in amazement before a humble wooden bullock cart. Seated on the ground in the shade underneath the cart is Sage Raikva—a rugged, serene ascetic in a simple loincloth, radiating immense inner peace and detachment, no text, no borders.",
                "narration_en": "At dawn, the King sent his chamberlain to find Sage Raikva. At first the servant searched all the famous Gurukulams and returned empty-handed. The King said: 'Do not look where ordinary scholars gather—search where a true knower of Brahman hides from the world!' Going back to the village outskirts, the servant found a man sitting in the shade beneath a dusty bullock cart, calmly scratching his sun-parched skin. Stepping close, he asked: 'Revered Sir, are you Raikva with the Cart?' 'Hmm, here I am!' replied the Sage.",
                "narration_ta": "பொழுது விடிந்ததும் மன்னன் தன் தேர்ப்பாகனை அனுப்பி ரைக்கவரைத் தேடச் சொன்னான். அவன் புகழ்பெற்ற இடங்களிலெல்லாம் தேடியும் காணாமல் திரும்பியபோது, மன்னன் 'பிரம்ம ஞானிகள் புகழை விரும்பாமல் எங்கேனும் மறைந்திருப்பார்கள், அங்கே தேடு!' என்றான். மீண்டும் சென்று தேடியபோது, ஓர் ஊரின் ஒதுக்குப்புறத்தில் மாட்டு வண்டியின் நிழலில் அமர்ந்து தன் உடலைச் சொறிந்துகொண்டிருந்த எளிய முனிவரைக் கண்டு, 'ஐயா, நீங்கள்தான் வண்டிக்கார ரைக்கவரா?' என்று கேட்டான். 'ஆம், நான்தான்!' என்றார் முனிவர்.",
                "subtitle_cue": "மாட்டு வண்டியின் அடியில் நிழலில் அமர்ந்திருந்த பிரம்ம ஞானி ரைக்கவரைக் கண்டடைந்த தேர்ப்பாகன்!",
                "sound_cue": "Rustic village ambience giving way to a deep, grounding Tanpura drone."
            },
            {
                "camera": "Dramatic scene by the bullock cart: King Janashruti arrives with 600 cows, a golden necklace, and a mule-chariot, which Raikva initially waves away until the King bows with complete surrender.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 dramatic shot beside the wooden bullock cart. King Janashruti kneels humbly in the dust before Sage Raikva, offering six hundred white cows, a heavy gold necklace, and a chariot drawn by mules, then bowing his head in complete disciple-surrender at the sage's feet, warm golden sunlight, no text, no borders.",
                "narration_en": "First King Janashruti came offering six hundred cows, a golden necklace, and a chariot drawn by mules, saying: 'Revered Sir, teach me the Deity upon whom you meditate!' Seeing that the King still approached like a wealthy patron buying knowledge, Raikva spurned the gifts! Humbled to the core, Janashruti returned with a thousand cows, his royal lands, and complete surrender of his own lineage, bowing his face directly at the Sage's feet. Seeing his ego dissolved, Raikva smiled and began the Upadesha!",
                "narration_ta": "முதலில் மன்னன் ஜானஸ்ருதி அறுநூறு பசுக்களும், பொன் மாலையும், கோவேறு கழுதை பூட்டிய தேரும் கொண்டு வந்து, 'சுவாமி, தாங்கள் உபாசிக்கும் தெய்வத்தை எனக்கு உபதேசியுங்கள்!' என்றான். செல்வக் கர்வத்தோடு விலைக்கு ஞானம் வாங்குவது போல் வந்த மன்னனின் பரிசுகளை ரைக்கவர் நிராகரித்தார்! தன் அகந்தை முழுமையாக அழியப்பெற்ற மன்னன், மீண்டும் ஆயிரம் பசுக்களுடனும் கிராமங்களுடனும் வந்து ரைக்கவரின் திருவடிகளில் சரணடைந்தான். மன்னனின் பணிவைக் கண்ட ரைக்கவர் புன்னகைத்து உபதேசத்தைத் தொடங்கினார்!",
                "subtitle_cue": "செல்வத்தால் ஞானத்தை வாங்க முடியாது — அகந்தை அழிந்து சரணடைந்த மன்னனுக்கு இரங்கிய ரைக்கவர்!",
                "sound_cue": "Dramatic Mridangam pause followed by a warm, compassionate Veena melody in Raga Sahana."
            },
            {
                "camera": "Cosmic nature visualization: a dying campfire merging into the wind, the setting sun and moon merging into the atmosphere, and drying water evaporating into the air.",
                "veo_prompt": "16:9 8K 24fps photorealistic nature-and-cosmos shot over the plains of ancient India at sunset. A campfire's dying embers, the setting golden sun, the pale moon, and evaporating river mist all stream visibly into the vast, invisible currents of the cosmic Wind (Vayu) sweeping across the sky, no text, no subtitles, no borders.",
                "narration_en": "Sage Raikva revealed the grand Samvarga Vidya—the Wisdom of the Great Absorber! 'Vayur vava samvargah—Among the cosmic powers outside, the Wind (Vayu) is indeed the Great Absorber! For when Fire goes out, it merges into the Wind; when the Sun sets, it merges into the Wind; when the Moon sets, it merges into the Wind; and when Water dries up, it merges into the Wind! For Vayu alone absorbs them all!'",
                "narration_ta": "ரைக்கவர் புகழ்பெற்ற 'ஸம்வர்க வித்தை'யை (அனைத்தையும் தன்னுள் ஒடுக்கும் தத்துவத்தை) உபதேசித்தார்: 'வாயுர்வாவ ஸம்வர்கஃ — புற உலகில் தேவர்களுள் வாயுவே அனைத்தையும் தன்னுள் ஈர்த்து ஒடுக்கும் ஸம்வர்கன் ஆகும்! ஏனெனில் நெருப்பு அணையும்போது வாயுவிலேயே ஒடுங்குகிறது; சூரியன் மறையும்போதும், சந்திரன் மறையும்போதும் வாயுவிலேயே ஒடுங்குகின்றன; நீர் வற்றும்போதும் வாயுவிலேயே கலக்கிறது!'",
                "subtitle_cue": "வாயுர்வாவ ஸம்வர்கஃ — அண்டத்தில் அக்னி, சூரியன், சந்திரன், நீர் அனைத்தையும் தன்னுள் ஒடுக்கும் வாயு!",
                "sound_cue": "Swirling wind soundscape blended with harmonic Bansuri and Tanpura resonance."
            },
            {
                "camera": "Intimate close-up of King Janashruti meditating by the cart as his speech, sight, hearing, and mind fold inward into the rhythmic golden glow of Prana in his heart.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 spiritual close-up of King Janashruti meditating in Padmasana beside Sage Raikva under the bullock cart. Subtle golden streams of light from his eyes, ears, mouth, and forehead draw inward into the glowing lotus of Prana in his chest, realizing the unity of macrocosm and microcosm, no text, no borders.",
                "narration_en": "'And now, O King, look within yourself! Prano vava samvargah—Within the body, Prana, the Vital Life-Breath, is the Great Absorber! When a person sleeps, Speech merges into Prana, Sight merges into Prana, Hearing merges into Prana, and Mind merges into Prana; for Prana alone absorbs them all! These two—Cosmic Wind without and Vital Breath within—are the two grand portals of the One Infinite Viraj!'",
                "narration_ta": "'இப்போது உன் உடலுக்குள்ளே பார் மன்னா! ப்ராணோ வாவ ஸம்வர்கஃ — உடலுக்குள் பிராணனே அனைத்தையும் தன்னுள் ஒடுக்கும் ஸம்வர்கன் ஆகும்! மனிதன் உறங்கும்போது வாக்கு பிராணனில் ஒடுங்குகிறது; பார்வையும், செவியும், மனமும் பிராணனிலேயே ஒடுங்குகின்றன! வெளியேயுள்ள வாயுவும் உள்ளேயுள்ள பிராணனும் விராட் புருஷனான ஒரே பரம்பொருளின் இரு வடிவங்களே ஆகும்!'",
                "subtitle_cue": "ப்ராணோ வாவ ஸம்வர்கஃ — உடலுக்குள் வாக்கு, கண், காது, மனம் அனைத்தையும் தன்னுள் ஒடுக்கும் பிராணன்!",
                "sound_cue": "Deep, rhythmic breathing pulse synchronized with Rudra Veena and soft temple bell."
            },
            {
                "camera": "Wide golden-hour closing shot of King Janashruti and Sage Raikva sharing sacred food with a humble Brahmachari guest in the village called Raikvaparna.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot in the sunlit Panchala countryside (Raikvaparna village). King Janashruti and Sage Raikva sit together in peaceful equality beside the bullock cart and sacred fire, serving food to a humble Vedic brahmachari mendicant, seeing the Supreme Viraj in every living breath, no text, no borders.",
                "narration_en": "Illumined by this Samvarga Vidya, King Janashruti realized that when we feed a hungry seeker, we are offering directly into the cosmic Prana that sustains the universe! The lands he gave to the Sage became known forever as Raikvaparna—reminding the world that an emperor's crown bows before the cart of a realized soul!",
                "narration_ta": "இந்த ஸம்வர்க வித்தையால் ஞானம் பெற்ற மன்னன் ஜானஸ்ருதி, பசித்த ஓர் உயிருக்கு அன்னமிடுவது பிரபஞ்சத்தை இயக்கும் பிராண அக்னியிலேயே இடப்படும் ஆஹுதி என்பதை உணர்ந்தான்! அன்று முதல் ரைக்கவர் தங்கியிருந்த அப்பகுதி 'ரைக்வபர்ணா' என்று பெயர் பெற்றது; சக்கரவர்த்தியின் மணிமகுடமும் ஆத்ம ஞானியின் மாட்டு வண்டிக்கு முன் தலைவணங்கும் என்பதை இக்கதை உலகுக்கு உணர்த்துகிறது!",
                "subtitle_cue": "எளிய மாட்டு வண்டியின் கீழ் அமர்ந்திருந்த பிரம்ம ஞானியின் முன் தலைவணங்கிய சக்கரவர்த்தியின் மகுடம்!",
                "sound_cue": "Sama Veda Shanti Mantra 'Om Apyayantu Mamangani' in joyous unison."
            }
        ]
    }
]


MUKHYA_PART4 = [
    {
        "story_id": "MUKHYA_16_BRIHADARANYAKA_01",
        "muktika_number": 10,
        "upanishad_sanskrit": "बृहदारण्यकोपनिषद् (याज्ञवल्क्य-मैत्रेयी संवादः)",
        "upanishad_iast": "Bṛhadāraṇyakopaniṣad (Yājñavalkya-Maitreyī Saṃvādaḥ)",
        "upanishad_tamil": "பிருஹதாரண்யக உபநிடதம் (யாக்ஞவல்கியர் - மைத்ரேயி: அமிர்தத்வ உபதேசம்)",
        "upanishad_english": "Brihadaranyaka Upanishad (Story 1: Yajnavalkya & Maitreyi)",
        "veda": "Shukla Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "Maitreyi's Immortal Question & Yajnavalkya's Teaching: 'What Shall I Do with That Which Makes Me Not Immortal?'",
        "story_title_tamil": "யாக்ஞவல்கியரும் மைத்ரேயியும்: 'எனக்கு அமரத்துவம் தராத செல்வத்தைக் கொண்டு நான் என்ன செய்வேன்?'",
        "characters": [
            "Maharishi Yajnavalkya (The peerless sage of the Shukla Yajur Veda preparing to enter Sannyasa)",
            "Brahmavadini Maitreyi (Yajnavalkya's philosophical wife who spurned earthly wealth for Atma-Vidya)",
            "Katyayani (Yajnavalkya's second wife, skilled in household affairs)"
        ],
        "mahavakya_sanskrit": "येनाहं नामृता स्यां किमहं तेन कुर्याम् । आत्मा वा अरे द्रष्टव्यः श्रोतव्यो मन्तव्यो निदिध्यासितव्यो मैत्रेयि ॥",
        "mahavakya_tamil_translit": "யேநாஹம் நாம்ருதா ஸ்யாம் கிமஹம் தேன குர்யாம் | ஆத்மா வா அரே த்ரஷ்டவ்யஃ ஸ்ரோதவ்யோ மந்தவ்யோ நிதித்யாஸிதவ்யோ மைத்ரேயி ||",
        "mahavakya_meaning_english": "What shall I do with that wealth by which I cannot become immortal? Verily, O Maitreyi, the Self is to be seen, heard of, reflected upon, and meditated upon!",
        "mahavakya_meaning_tamil": "எதனால் நான் மரணமற்ற அமரத்துவத்தை அடைய முடியாதோ, அந்தச் செல்வத்தைக் கொண்டு நான் என்ன செய்வேன்? மைத்ரேயி! ஆத்மாவையே தரிசிக்க வேண்டும், கேட்க வேண்டும், சிந்திக்க வேண்டும், தியானிக்க வேண்டும்!",
        "philosophical_theme": "Amritattva (Immortality cannot be won through wealth—Amritattvasya tu nashasti vittena); all love in the world is for the sake of the Atman (Atmanastu kamaya sarvam priyam bhavati); Shravana, Manana, and Nididhyasana.",
        "setting_specifics": "Maharishi Yajnavalkya's tranquil Mithila forest ashram at the threshold of his departure for Sannyasa, surrounded by cows, gold, and the sacred river.",
        "metaphor_highlight": "A lump of salt dissolved in the ocean (Saindhava-Khilya), Sounds of a drum, conch, and Veena (Dundubhi, Shankha, Vina), and the Threefold Path of Shravana-Manana-Nididhyasana.",
        "scenes": [
            {
                "camera": "Warm golden morning shot in Yajnavalkya's ashram courtyard; the sage prepares to divide his cattle and gold between his wives Maitreyi and Katyayani.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in an ancient Vedic forest hermitage in Mithila. The venerable sage Yajnavalkya in saffron-ochre robes stands beside herds of white cows and brass vessels of gold, addressing his noble wife Maitreyi, who wears a simple pure white cotton saree and Rudraksha beads, golden morning light, no text, no borders.",
                "narration_en": "Having lived the full life of a householder and royal teacher, the great sage Yajnavalkya resolved to embrace Sannyasa and enter the forest. Calling his beloved wife Maitreyi, he said: 'Maitreyi, I am about to renounce this householder life and go forth. Let me make a final division of all my wealth and cattle between you and Katyayani.'",
                "narration_ta": "இல்லற தர்மத்தை நிறைவு செய்த மகரிஷி யாக்ஞவல்கியர், துறவறம் பூண்டு வனத்திற்குச் செல்லத் திருவுள்ளம் கொண்டார். தன் பத்தினியான மைத்ரேயியை அழைத்து, 'மைத்ரேயி! நான் இவ்விடத்தை விட்டுத் துறவறம் ஏற்கப் போகிறேன்; அதற்கு முன் என் செல்வங்கள் அனைத்தையும் உனக்கும் காத்யாயனிக்கும் பகிர்ந்து கொடுத்துவிட விரும்புகிறேன்' என்றார்.",
                "subtitle_cue": "பிருஹதாரண்யக உபநிடதம்: துறவறம் ஏற்கும் முன் செல்வத்தைப் பகிர்ந்தளிக்க முன்வந்த யாக்ஞவல்கியர்!",
                "sound_cue": "Calm Shukla Yajur Veda recitation over a gentle Tanpura and morning Veena melody."
            },
            {
                "camera": "Dramatic close-up of Maitreyi looking past the heaps of gold and cattle straight into Yajnavalkya's eyes.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 close-up of Brahmavadini Maitreyi standing with folded hands before Sage Yajnavalkya. Her eyes shine with profound spiritual fire and detachment as she waves aside the golden vessels and cattle in the background, asking for the secret of immortality alone, no text, no subtitles, no borders.",
                "narration_en": "Maitreyi asked a question that has echoed down the millennia: 'Yannu ma iyam bhagavah sarva prithivi vittena purna syat, katham tenamrita syam—My Lord, if this whole earth filled to the brim with wealth were to belong to me alone, would I become immortal through it?' Yajnavalkya answered truthfully: 'Neti—No! Your life would merely be like the life of the rich; there is no hope of immortality through wealth!' Then Maitreyi uttered her immortal cry: 'Yenaham namrita syam, kim aham tena kuryam—What shall I do with that by which I cannot become immortal? Tell me instead what you know of Immortality!'",
                "narration_ta": "மைத்ரேயி கேட்ட கேள்வி யுகங்கள் தோறும் எதிரொலித்துக் கொண்டிருக்கிறது: 'பகவானே! செல்வத்தால் நிரம்பிய இந்தப் பூமி முழுவதும் எனக்கே சொந்தமானால், அதனால் நான் மரணமற்ற அமரத்துவத்தை அடைந்துவிடுவேனா?' யாக்ஞவல்கியர் உண்மையைக் கூறினார்: 'இல்லை! செல்வந்தர்களின் வாழ்க்கையைப் போல் உன் வாழ்க்கையும் இருக்குமே தவிர, செல்வத்தால் அமரத்துவம் கிடைக்கவே கிடைக்காது!' உடனே மைத்ரேயி முழங்கினார்: 'யேநாஹம் நாம்ருதா ஸ்யாம் கிமஹம் தேன குர்யாம் — எதனால் நான் அமரத்துவம் அடைய முடியாதோ, அதைக் கொண்டு நான் என்ன செய்வேன்? தாங்கள் அறிந்த அமிர்த தத்துவத்தையே எனக்கு அருளுங்கள்!'",
                "subtitle_cue": "'எதனால் நான் அமரத்துவம் அடைய முடியாதோ, அந்தச் செல்வத்தைக் கொண்டு நான் என்ன செய்வேன்?' — மைத்ரேயி.",
                "sound_cue": "Stirring Violin solo rising with spiritual intensity in Raga Bhairavi."
            },
            {
                "camera": "Heartwarming two-shot as Yajnavalkya seats Maitreyi beside him by the sacred Homa fire, overjoyed by her question.",
                "veo_prompt": "16:9 8K 24fps photorealistic medium shot inside the ashram pavilion. Sage Yajnavalkya, beaming with spiritual joy and affection, invites Maitreyi to sit beside the sacred Homa fire altar. Golden sunlight illuminates both figures as he raises his hand in Chinmudra to impart the highest wisdom, no text, no borders.",
                "narration_en": "Overjoyed, Yajnavalkya said: 'Priya batare nah सती priyam भाषसे—Dear as you have always been to me, O Maitreyi, you have now spoken words that make you dearer still! Come, sit down, and I will explain to you the secret of all love: Verily, not for the sake of the husband is the husband dear, but for the sake of the Atman is the husband dear! Not for the sake of wife, children, wealth, or gods are they dear, but for the sake of the Self—Atmanastu kamaya sarvam priyam bhavati!'",
                "narration_ta": "மகிழ்ச்சியில் திளைத்த யாக்ஞவல்கியர், 'மைத்ரேயி! ஏற்கனவே என் அன்புக்குரிய நீ, இப்போது என் உள்ளத்திற்கு மிகவும் இனிய வார்த்தையைக் கூறினாய்! அருகில் அமர்ந்து கேள்' என்று கூறி அன்பின் ரகசியத்தை உபதேசித்தார்: 'கணவனின் பொருட்டுக் கணவன் பிரியமானவன் அல்லன், ஆத்மாவின் பொருட்டே கணவன் பிரியமானவன் ஆகிறான்! மனைவி, மக்கள், செல்வம், தேவர்கள், உலகங்கள் அனைத்துமே ஆத்மாவின் பொருட்டே பிரியமானவையாகத் தோன்றுகின்றன — ஆத்மனஸ்து காமாய ஸர்வம் ப்ரியம் பவதி!'",
                "subtitle_cue": "ஆத்மனஸ்து காமாய ஸர்வம் ப்ரியம் பவதி — ஆத்மாவின் பொருட்டே அனைத்தும் பிரியமானவையாகின்றன!",
                "sound_cue": "Warm, tender Bansuri and Veena harmony celebrating divine love."
            },
            {
                "camera": "Visual contemplation of the three pillars of Vedanta: Shravana (listening to the Guru), Manana (deep reflection), and Nididhyasana (unbroken meditation).",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic shot of Brahmavadini Maitreyi listening with rapt attention (Shravana), reflecting deeply by a lotus pond (Manana), and sitting in unbroken meditative absorption (Nididhyasana) under a sunlit banyan tree as Sage Yajnavalkya guides her, no text, no subtitles, no borders.",
                "narration_en": "Then Yajnavalkya gave the golden royal highway of Vedantic sadhana: 'Atma va are drashtavyah, shrotavyo mantavyo nididhyasitavyo Maitreyi! Verily, O Maitreyi, it is the Self that must be seen! It must be heard of from the Guru (Shravana), reflected upon through reason (Manana), and meditated upon with one-pointed absorption (Nididhyasana)! For by seeing, hearing, reflecting, and realizing the Atman, all this universe is known!'",
                "narration_ta": "தொடர்ந்து வேதாந்த சாதனையின் மும்மணிகளை யாக்ஞவல்கியர் அருளினார்: 'ஆத்மா வா அரே த்ரஷ்டவ்யஃ ஸ்ரோதவ்யோ மந்தவ்யோ நிதித்யாஸிதவ்யோ மைத்ரேயி! மைத்ரேயி, ஆத்மாவையே நேரில் தரிசிக்க வேண்டும்! அதனை சற்குருவிடம் கேட்க வேண்டும் (ஸ்ரவணம்), கேட்டதை ஆழ்ந்து சிந்திக்க வேண்டும் (மனனம்), சிந்தித்துத் தெளிந்ததில் இடைவிடாது தியானிக்க வேண்டும் (நிதித்யாஸனம்)! ஆத்மாவைத் தரிசிப்பதால் இவ்வுலகம் அனைத்தும் அறியப்பட்டுவிடுகிறது!'",
                "subtitle_cue": "ஆத்மாவையே தரிசிக்க வேண்டும் — ஸ்ரவணம், மனனம், நிதித்யாஸனம் ஆகிய மூன்று படிகள்!",
                "sound_cue": "Resonant Vedic chant of 'Atma Va Are Drashtavyah' with three distinct temple bell chimes."
            },
            {
                "camera": "Close-up of temple musicians playing a Dundubhi (drum), blowing a Shankha (conch), and plucking a Veena; showing that individual notes cannot be grasped apart from the instrument.",
                "veo_prompt": "16:9 8K 24fps photorealistic scene in the ashram courtyard showing an ancient Indian wooden Dundubhi drum being beaten, a white Shankha conch being blown, and a carved Veena being plucked. Golden sound vibrations fill the air while Yajnavalkya and Maitreyi observe how all sounds are inseparable from their source, no text, no borders.",
                "narration_en": "To illustrate how the universe cannot exist apart from the Self, Yajnavalkya gave three musical metaphors: 'Just as when a drum is beaten, one cannot grasp its external sounds separately, but by grasping the drum or the drummer the sound is grasped; just as with the blowing of a conch and the playing of a Veena—and just as a lump of salt dropped into the ocean dissolves completely so that wherever one tastes there is only salt—even so is this Infinite Being a boundless mass of Pure Consciousness (Vijnanaghana)!'",
                "narration_ta": "ஆத்மாவைத் தவிர உலகம் வேறல்ல என்பதை விளக்க மூன்று இசை உவமைகளைக் கூறினார் முனிவர்: 'முரசு கொட்டப்படும்போது அதன் ஒலிகளைத் தனித்தனியே பிடிக்க முடியாது, முரசைப் பிடித்தாலே ஒலிகள் அனைத்தும் பிடிபடும்; சங்கு ஊதப்படும்போதும் வீணை மீட்டப்படும்போதும் அதுவே நியதி! கடலில் விழுந்த உப்புக்கட்டி கரைந்து எங்கு சுவைத்தாலும் உப்பாகவே இருப்பது போல், இந்த ஆத்மா எல்லையற்ற தூய ஞானப் பிழம்பாக (விஞ்ஞானகனமாக) நிறைந்துள்ளது!'",
                "subtitle_cue": "கடலில் கரைந்த உப்புக்கட்டி போல் எல்லையற்ற தூய ஞானப் பிழம்பாக (விஞ்ஞானகனமாக) ஒளிரும் ஆத்மா!",
                "sound_cue": "Dundubhi drum, Shankha conch, and Veena playing in succession and merging into one harmonic chord."
            },
            {
                "camera": "Cosmic realization shot: Maitreyi asks how there is no separate consciousness after liberation, and Yajnavalkya reveals the non-dual unity beyond subject and object.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 spiritual realization shot. Brahmavadini Maitreyi sits in radiant Padmasana as the boundary between seer and seen dissolves in golden sunrise light over the river. Sage Yajnavalkya stands beside her in blessing posture, pure Advaita stillness, no text, no subtitles, no borders.",
                "narration_en": "When Yajnavalkya said that in liberation there is no separate individual consciousness, Maitreyi asked in wonder: 'Here you have bewildered me, Lord!' Yajnavalkya smiled and uttered the ultimate peak of Advaita: 'Yatra hi dvaitam iva bhavati, tad itara itaram pashyati... yatra tvasya sarvam atmaivabhut, tat kena kam pashyet? Where there seems to be duality, there one sees another, smells another, hears another; but where ALL has become one's own Self, by what and whom could one see? How could one know the Knower Himself—Vijnataram are kena vijaniyat?'",
                "narration_ta": "முக்தி நிலையில் தனிப்பட்ட சிற்றறிவு இருப்பதில்லை என்று முனிவர் கூறியபோது மைத்ரேயி வியப்புற்றுக் கேட்டதற்கு, அத்வைதத்தின் சிகரமான விடையை அருளினார் யாக்ஞவல்கியர்: 'யத்ர ஹி த்வைதமிவ பவதி ததிதர இதரம் பஸ்யதி... எங்கே இருமை (துவைதம்) உள்ளது போல் தோன்றுகிறதோ, அங்கேதான் ஒருவன் மற்றொன்றைப் பார்க்கிறான், கேட்கிறான்; ஆனால் எங்கே எல்லாமே தன் ஆத்மாவாகவே ஆகிவிட்டதோ, அங்கே எதனால் எதைப் பார்ப்பது? அனைத்தையும் அறியும் அந்த அறிபவனையே (விஞ்ஞாதாரம்) எதனால் அறிய முடியும்?'",
                "subtitle_cue": "எங்கே எல்லாமே ஆத்மாவாக ஆகிவிட்டதோ, அங்கே அறிபவனையே (விஞ்ஞாதாரம்) எதனால் அறிய முடியும்?",
                "sound_cue": "Sublime, breathless Bansuri note suspended over an infinite Tanpura drone."
            },
            {
                "camera": "Wide closing shot of Maharishi Yajnavalkya walking peacefully into the sunlit forest as an ascetic, while Maitreyi sits enthroned in Immortal Self-Knowledge.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot at the edge of the Mithila forest at sunrise. Brahmavadini Maitreyi sits in luminous, immortal peace by the ashram altar while Maharishi Yajnavalkya, carrying his wooden danda and kamandalu, walks serenely into the golden forest path. Zero modern items, zero text, zero borders.",
                "narration_en": "'Etavad are khalu amritattvam—Thus far indeed, O Maitreyi, goes Immortality!' Having bestowed upon Maitreyi the treasure that outshines all the gold of the earth, Maharishi Yajnavalkya went forth into the forest as a liberated Sannyasin!",
                "narration_ta": "'ஏதாவதரே கலு அம்ருதத்வம் — மைத்ரேயி! மரணமற்ற அமரத்துவம் என்பது இதுவேயாகும்!' உலகின் பொன்னையும் பொருளையும் விட மேலான ஆத்ம அமிர்தத்தை மைத்ரேயிக்கு அருளிவிட்டு, மகரிஷி யாக்ஞவல்கியர் பரிவ்ராஜகத் துறவியாக வனத்திற்குள் புறப்பட்டார்!",
                "subtitle_cue": "ஏதாவதரே கலு அம்ருதத்வம் — மைத்ரேயி! மரணமற்ற அமரத்துவம் என்பது இந்த ஆத்ம ஞானமே! ஓம் சாந்திஃ!",
                "sound_cue": "Shukla Yajur Veda Shanti Mantra 'Om Purnamadah Purnamidam' in resonant harmony."
            }
        ]
    },
    {
        "story_id": "MUKHYA_17_BRIHADARANYAKA_02",
        "muktika_number": 10,
        "upanishad_sanskrit": "बृहदारण्यकोपनिषद् (जनकसभायां गार्गी-याज्ञवल्क्य संवादः)",
        "upanishad_iast": "Bṛhadāraṇyakopaniṣad (Janakasabhāyāṃ Gārgī-Yājñavalkya Saṃvādaḥ)",
        "upanishad_tamil": "பிருஹதாரண்யக உபநிடதம் (ஜனகர் சபையில் கார்கி - யாக்ஞவல்கியர் வாதம்)",
        "upanishad_english": "Brihadaranyaka Upanishad (Story 2: Gargi Vachaknavi & Yajnavalkya in King Janaka's Court)",
        "veda": "Shukla Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "Gargi's Two Unerring Arrows in King Janaka's Court: Who Holds Space and Time Together?",
        "story_title_tamil": "ஜனகர் சபையில் கார்கி தொடுத்த இரண்டு கூர்மையான கணைகள்: ஆகாயத்தையும் காலத்தையும் தாங்கும் அக்ஷரப் பரம்பொருள்!",
        "characters": [
            "Rajarishi Janaka of Videha (Emperor of Mithila hosting the grand Bahudakshina philosophical assembly)",
            "Maharishi Yajnavalkya (Who claimed the 1,000 cows with golden horns as the supreme knower of Brahman)",
            "Brahmavadini Gargi Vachaknavi (Daughter of Vachaknu, the fearless woman philosopher who questioned Yajnavalkya twice)",
            "Somi / Sages of Kuru-Panchala (Ashvala, Artabhaga, Bhujyu, Ushasta, Kahola, Uddalaka, Vidagdha Shakalya)"
        ],
        "mahavakya_sanskrit": "एतस्य वा अक्षरस्य प्रशासने गार्गि सूर्याचन्द्रमसौ विधृतौ तिष्ठतः । अदृष्टो द्रष्टाश्रुतः श्रोतामतो मन्ताविज्ञातो विज्ञाता ॥",
        "mahavakya_tamil_translit": "ஏதஸ்ய வா அக்ஷரஸ்ய ப்ரஸாஸனே கார்கி ஸூர்யாசந்த்ரமஸௌ வித்ருதௌ திஷ்டதஃ | அத்ருஷ்டோ த்ரஷ்டாஸ்ருதஃ ஸ்ரோதாமதோ மந்தாவிஜ்ஞாதோ விஜ்ஞாதா ||",
        "mahavakya_meaning_english": "Under the mighty rule of this Imperishable Akshara, O Gargi, the sun and moon are held in their courses! It is the Unseen Seer, the Unheard Hearer, the Unthought Thinker, the Unknown Knower!",
        "mahavakya_meaning_tamil": "கார்கி! இந்த அழியாத அக்ஷரப் பரம்பொருளின் ஆணையாலேயே சூரியனும் சந்திரனும் தத்தம் பாதையில் நிலைநிறுத்தப்பட்டுள்ளன! அது காணப்படாத பார்ப்பவன், அறியப்படாத அறிபவன்!",
        "philosophical_theme": "The Warp and Woof of Cosmic Space (Ota-Prota in Akasha) resting upon the Imperishable Akshara; the Cosmic Governance (Prashasana) of Brahman over sun, moon, rivers, and time.",
        "setting_specifics": "Emperor Janaka's magnificent pillared granite Sabha in Mithila, with 1,000 white cows standing in the courtyard, ten gold coins tied to each pair of horns.",
        "metaphor_highlight": "1,000 Cows with Gold-Adorned Horns, Warp and Woof of a Woven Cloth (Ota-Prota), and a Warrior of Kashi or Videha stringing his bow with two bamboo-tipped arrows.",
        "scenes": [
            {
                "camera": "Grand sweeping crane shot across Emperor Janaka's royal Sabha in Mithila; in the outer courtyard stand 1,000 white cows with gold coins gleaming on their horns.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in the grand royal pillared granite court of Emperor Janaka in ancient Mithila. Hundreds of Vedic sages from Kuru and Panchala sit in the hall, while through the archway stand a thousand white cows with golden coins tied to their horns. Maharishi Yajnavalkya stands calmly at the center, no text, no borders.",
                "narration_en": "Emperor Janaka of Videha once performed a grand sacrifice and gathered all the foremost Vedic scholars of Kuru and Panchala. Wishing to know who among them was the greatest knower of Brahman—Brahmishtha—he enclosed a thousand cows in the courtyard, with ten gold coins tied to the horns of each cow, and announced: 'Revered Brahmanas, let him who is the greatest knower of Brahman among you drive home these thousand cows!'",
                "narration_ta": "விதேக நாட்டு மன்னரான ராஜரிஷி ஜனகர் மாபெரும் வேள்வியை நடத்தி, குரு-பாஞ்சால தேசத்து வேத விற்பன்னர்கள் அனைவரையும் தன் சபைக்கு அழைத்தார். அவர்களுள் சிறந்த பிரம்ம ஞானி (பிரம்மிஷ்டன்) யார் என்பதை அறிய, கொம்புகளின் நடுவே பத்துப் பொற்காசுகள் கட்டப்பட்ட ஆயிரம் பசுக்களை நிறுத்தி, 'உங்களில் யார் சிறந்த பிரம்ம ஞானியோ அவர் இப்பசுக்களை ஓட்டிச் செல்லலாம்!' என்று அறிவித்தார்.",
                "subtitle_cue": "பிருஹதாரண்யக உபநிடதம்: ஜனகர் சபையில் ஆயிரம் பசுக்களும் பிரம்ம ஞானிகளின் சபையும்!",
                "sound_cue": "Majestic Nagaswaram and Mridangam court fanfare settling into tense, expectant silence."
            },
            {
                "camera": "Medium tracking shot as Yajnavalkya calmly tells his disciple Samashravas to lead the cows away, sparking questions from the assembled sages.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot in King Janaka's court. Maharishi Yajnavalkya gestures calmly to his young disciple Samashravas to drive away the gold-horned cows, while the surrounding scholars rise in challenge. In the front row sits the dignified woman philosopher Gargi Vachaknavi in white silk saree and Rudraksha, watching keenly, no text, no borders.",
                "narration_en": "While the other sages hesitated, Maharishi Yajnavalkya called his disciple: 'Samashravas, my boy, drive home these cows!' Immediately the scholars rose in protest: 'Do you claim to be the greatest knower of Brahman among us, Yajnavalkya?' Yajnavalkya replied with witty humility: 'We bow to the greatest knower of Brahman; we just want the cows!' One by one—Ashvala, Artabhaga, Bhujyu, Ushasta, and Kahola—questioned him and were answered.",
                "narration_ta": "மற்ற முனிவர்கள் தயங்கி நின்றபோது, மகரிஷி யாக்ஞவல்கியர் தன் சீடனை அழைத்து, 'சாமஸ்ரவஸ்! இந்தப் பசுக்களை நம் ஆசிரமத்திற்கு ஓட்டிச் செல்!' என்றார். சபையிலிருந்த பண்டிதர்கள் கொதித்தெழுந்து, 'யாக்ஞவல்கியரே! நீர்தான் எங்களுள் சிறந்த பிரம்ம ஞானியா?' என்று கேட்டனர். யாக்ஞவல்கியர் புன்னகையுடன், 'சிறந்த பிரம்ம ஞானிக்கு எங்கள் நமஸ்காரம்; இப்போது பசுக்கள் தேவை என்பதால் ஓட்டிச் செல்கிறோம்!' என்றார். தொடர்ந்து அஸ்வலர், ஆர்த்தபாகர், உஷஸ்தர், கஹோலர் ஆகியோரின் கேள்விகளுக்கு விடையளித்தார்.",
                "subtitle_cue": "'சிறந்த பிரம்ம ஞானிக்கு நமஸ்காரம்!' — சபையின் கேள்விகளை எதிர்கொண்ட யாக்ஞவல்கியர்!",
                "sound_cue": "Lively rhythmic Veena and Pakhawaj interplay representing philosophical debate."
            },
            {
                "camera": "Dramatic push-in on Brahmavadini Gargi Vachaknavi rising in the assembly, using the metaphor of threads woven warp and woof (Ota-Prota).",
                "veo_prompt": "16:9 8K 24fps photorealistic shot inside the royal Sabha. The noble woman philosopher Gargi Vachaknavi stands fearless and serene before Maharishi Yajnavalkya and King Janaka, gesturing with her hands like the warp and woof of a woven loom to question the foundation of the cosmos, warm golden lighting, no text, no borders.",
                "narration_en": "Then rose the fearless woman philosopher Gargi Vachaknavi! In her first round of inquiry, she wove a cosmic ladder: 'Yajnavalkya, since all this earth is woven warp and woof—Ota-Prota—upon water, upon what is water woven?' Step by step Yajnavalkya traced the cosmic tapestry from Water to Wind, Sky, the Gandharva worlds, Sun, Moon, Stars, Devas, Indra, Prajapati, and finally the World of Brahma! When Gargi tried to ask through mere logic what lies beyond Brahma, Yajnavalkya cautioned her that ultimate Reality must be approached through direct inquiry, not dry speculation.",
                "narration_ta": "அப்போது வாசக்னு முனிவரின் புதல்வியான பிரம்மவாதினி கார்கி எழுந்தார்! துணியின் பாவும் ஊடையும் போல் (ஓத-ப்ரோதமாக) இவ்வுலகம் நீரிலும், நீர் வாயுவிலும், வாயு ஆகாயத்திலும், ஆகாயம் கந்தர்வ லோகம், சூரிய, சந்திர, நட்சத்திர, தேவ, இந்திர, பிரஜாபதி, பிரம்ம லோகங்களிலும் நெய்யப்பட்டுள்ளதை அடுக்கடுக்காகக் கேட்டார்! வெறும் தர்க்க வாதத்தால் பிரம்மத்தைக் கடந்து கேள்வி கேட்டபோது, அது நேரில் உணர வேண்டிய சத்தியம் என்று யாக்ஞவல்கியர் எச்சரித்தார்.",
                "subtitle_cue": "பாவும் ஊடையும் போல் (ஓத-ப்ரோதமாக) உலகங்கள் எதன் மேல் நெய்யப்பட்டுள்ளன? — கார்கியின் விசாரணை!",
                "sound_cue": "Intricate, fast-paced Veena tanam building in complexity and pausing dramatically."
            },
            {
                "camera": "Heroic low-angle shot as Gargi rises a second time, addressing the entire assembly of Brahmanas and comparing her two questions to two unerring arrows of a Kashi warrior.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic heroic shot in King Janaka's court. Brahmavadini Gargi addresses the venerable assembly of sages with commanding dignity, holding up two fingers like a royal warrior of Kashi or Videha stringing a mighty bow with two bamboo-tipped arrows to test Maharishi Yajnavalkya, no text, no subtitles, no borders.",
                "narration_en": "Later in the debate, Gargi rose a second time and addressed the entire assembly: 'Venerable Brahmanas, listen! I shall now ask Yajnavalkya just two questions. If he answers them, not one of you will ever defeat him in any discussion of Brahman!' Turning to the sage, she declared: 'Yajnavalkya! Just as a heroic prince of Kashi or Videha strings his unstrung bow and stands ready with two bamboo-tipped arrows in his hand, so have I risen with two questions! Answer me!' 'Ask, O Gargi!' said Yajnavalkya.",
                "narration_ta": "சிறிது நேரத்திற்குப் பின் கார்கி இரண்டாவது முறையாக எழுந்து சபையோரைப் பார்த்து முழங்கினார்: 'பூஜ்ய பிராமணர்களே! நான் இப்போது யாக்ஞவல்கியரிடம் இரண்டே இரண்டு கேள்விகளைக் கேட்கப் போகிறேன்; இவற்றிற்கு மட்டும் அவர் விடையளித்துவிட்டால், பிரம்ம விவாதத்தில் உங்களில் ஒருவராலும் அவரை வெல்ல முடியாது!' யாக்ஞவல்கியரை நோக்கி, 'காசி அல்லது விதேக நாட்டு மாவீரன் தன் வில்லை வளைத்துக் கூர்மையான இரண்டு அம்புகளை ஏந்தி நிற்பது போல், இரு கேள்விகளுடன் நிற்கிறேன்!' என்றார். 'கேள் கார்கி!' என்றார் முனிவர்.",
                "subtitle_cue": "காசி அல்லது விதேக நாட்டு வீரனின் இரு கூர்மையான கணைகளைப் போன்ற கார்கியின் இரண்டு கேள்விகள்!",
                "sound_cue": "Resonant bow-string twang effect on the Rudra Veena and commanding Mridangam beat."
            },
            {
                "camera": "Cosmic vision above the Mithila Sabha: past, present, and future woven into Unmanifest Space (Akasha), which itself rests upon the Imperishable Akshara.",
                "veo_prompt": "16:9 8K 24fps photorealistic cosmic vision above the royal court of Mithila. The stone ceiling seems to open into the vast starry cosmos where Sun, Moon, Earth, Heaven, and flowing rivers move in perfect harmony under the invisible command of the Imperishable Light (Akshara). Yajnavalkya speaks to Gargi in awe-inspiring reverence, no text, no borders.",
                "narration_en": "Gargi shot both arrows: 'That which is above heaven, below the earth, and between heaven and earth—past, present, and future—upon what is all that woven warp and woof?' Yajnavalkya answered the first arrow: 'Upon Space—Akasha!' Immediately Gargi loosed the second arrow: 'And upon what, pray, is Space itself woven warp and woof?' Then Yajnavalkya unveiled the supreme Akshara Vidya: 'Etad vai tad aksharam Gargi brahmana abhivadanti—That, O Gargi, the knowers of Brahman call AKSHARA, the Imperishable! It is neither coarse nor fine, neither short nor long, neither fire nor air, without shadow, without darkness, without eyes or ears, without measure, having no inside and no outside!'",
                "narration_ta": "கார்கி தன் இரு கணைகளையும் தொடுத்தார்: 'விண்ணுக்கு மேலும், மண்ணுக்குக் கீழும், இடையே உள்ள முக்காலப் பிரபஞ்சமும் எதன் மேல் நெய்யப்பட்டுள்ளன?' 'ஆகாயத்தின் மேல்!' என்றார் யாக்ஞவல்கியர். 'அப்படியானால் அந்த ஆகாயம் எதன் மேல் நெய்யப்பட்டுள்ளது?' என்று இரண்டாம் கணையைத் தொடுத்தார் கார்கி! உடனே யாக்ஞவல்கியர் அக்ஷர வித்தையை வெளியிட்டார்: 'கார்கி! பிரம்ம ஞானிகள் அதனை அக்ஷரம் (அழியாத பரம்பொருள்) என்று அழைக்கின்றனர்! அது பருமையானதும் அல்ல, அணுவும் அல்ல; குட்டையும் அல்ல, நெட்டையும் அல்ல; நிழலற்றது, இருளற்றது, அளவற்றது, உள்ளும் புறமும் அற்றது!'",
                "subtitle_cue": "ஆகாயத்திற்கும் ஆதாரமாக விளங்கும் அந்த அழியாத பரம்பொருளே 'அக்ஷரம்' எனப்படுகிறது!",
                "sound_cue": "Deep, awe-inspiring Shukla Yajur Veda chant of 'Etad Vai Tad Aksharam Gargi'."
            },
            {
                "camera": "Sweeping montage of the sun and moon in orbit, snowy Himalayan rivers flowing east and west, and seasons turning under the silent rule (Prashasana) of Akshara.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 epic montage of cosmic order: the golden sun and silver moon holding their courses in the sky, mighty rivers flowing from snowy white Himalayan peaks toward the eastern and western seas, and seasons turning in harmony—all governed by the unseen Imperishable Self, no text, no subtitles, no borders.",
                "narration_en": "'Etasya va aksharasya prashasane Gargi surya-chandramasau vidhritau tishthatah! Under the mighty command of this Imperishable Akshara, O Gargi, the sun and moon are held in their orbits! Under Its command, heaven and earth stand firm; moments, hours, days, nights, months, and years roll on; and rivers flow from the snowy mountains to the east and to the west! Whosoever departs from this world without knowing this Imperishable Akshara is pitiable indeed; but he who departs knowing It is a true Brahmana! It is the Unseen Seer, the Unheard Hearer, the Unthought Thinker, the Unknown Knower!'",
                "narration_ta": "'ஏதஸ்ய வா அக்ஷரஸ்ய ப்ரஸாஸனே கார்கி ஸூர்யாசந்த்ரமஸௌ வித்ருதௌ திஷ்டதஃ! கார்கி! இந்த அழியாத அக்ஷரத்தின் ஆணையாலேயே சூரியனும் சந்திரனும் தத்தம் பாதையில் நிலைநிறுத்தப்பட்டுள்ளன! அதன் ஆணையாலேயே விண்ணும் மண்ணும் நிற்கின்றன; நிமிடங்களும் நாட்களும் ஆண்டுகளும் சுழல்கின்றன; வெண்பனி மலைகளிலிருந்து நதிகள் கிழக்கிலும் மேற்கிலும் பாய்கின்றன! இந்த அக்ஷரத்தை அறியாமல் இவ்வுலகை விட்டுச் செல்பவன் கிருபணன் (ஏழை); இதனை உணர்ந்து செல்பவனே உண்மையான பிராமணன்! அது காணப்படாத பார்ப்பவன், கேட்கப்படாத கேட்பவன், அறியப்படாத அறிபவன்!'",
                "subtitle_cue": "அந்த அக்ஷரத்தின் ஆணையாலேயே சூரியனும் சந்திரனும் தத்தம் பாதையில் நிலைநிறுத்தப்பட்டுள்ளன!",
                "sound_cue": "Soaring cosmic symphony of Veena, Bansuri, Shankha, and Mridangam."
            },
            {
                "camera": "Wide triumphant closing shot in King Janaka's Sabha: Gargi turns to the assembly with folded hands and proclaims Yajnavalkya's peerless wisdom.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot in Emperor Janaka's grand Sabha. Brahmavadini Gargi bows with folded hands to Maharishi Yajnavalkya and addresses the entire assembly of sages in joyful reverence. Golden sunlight floods the pillared hall, zero modern objects, zero text, zero borders.",
                "narration_en": "Hearing this supreme revelation, Brahmavadini Gargi bowed and proclaimed to the assembly: 'Venerable Brahmanas! Consider yourselves fortunate if you can take your leave by merely bowing to him! Never shall any one of you defeat Yajnavalkya in any discussion of Brahman!' Thus shines forever the immortal dialogue of Gargi and Yajnavalkya!",
                "narration_ta": "இந்தப் பரம உபதேசத்தைக் கேட்ட பிரம்மவாதினி கார்கி சபையோரை நோக்கி முழங்கினார்: 'பூஜ்ய பிராமணர்களே! இவரை நமஸ்கரித்துவிட்டு விடைபெற்றாலே நீங்கள் பெரும் பேறு பெற்றவர்கள் ஆவீர்கள்! பிரம்ம விவாதத்தில் இவரை உங்களில் ஒருவராலும் ஒருபோதும் வெல்ல முடியாது!' இவ்வாறு கார்கி மற்றும் யாக்ஞவல்கியரின் அக்ஷர வித்தை வரலாற்றில் அழியாப் புகழ் பெற்றது!",
                "subtitle_cue": "'பிரம்ம விவாதத்தில் யாக்ஞவல்கியரை எவராலும் வெல்ல முடியாது!' — கார்கியின் பிரகடனம்! ஓம் சாந்திஃ!",
                "sound_cue": "Resonant applause of Vedic blessings and 'Om Purnamadah Purnamidam'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_18_BRIHADARANYAKA_03",
        "muktika_number": 10,
        "upanishad_sanskrit": "बृहदारण्यकोपनिषद् (जनक-याज्ञवल्क्य ज्योतिर्ब्राह्मणम्)",
        "upanishad_iast": "Bṛhadāraṇyakopaniṣad (Janaka-Yājñavalkya Jyotirbrāhmaṇam)",
        "upanishad_tamil": "பிருஹதாரண்யக உபநிடதம் (ஜனகர் - யாக்ஞவல்கியர்: ஆத்ம ஜோதி உபதேசம்)",
        "upanishad_english": "Brihadaranyaka Upanishad (Story 3: Emperor Janaka & Yajnavalkya - The Inner Light)",
        "veda": "Shukla Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "When Sun, Moon & Fire Go Out: Emperor Janaka & Yajnavalkya on the Self-Luminous Atman",
        "story_title_tamil": "சூரியனும் சந்திரனும் நெருப்பும் அணைந்த பின் எது ஒளிர்கிறது? ஜனகருக்கு யாக்ஞவல்கியர் அருளிய ஆத்ம ஜோதி!",
        "characters": [
            "Emperor Janaka of Videha (The royal philosopher-king who stepped down from his throne to become a disciple)",
            "Maharishi Yajnavalkya (Revealer of the Jyotir-Brahmana, the Self-Luminous Atman)"
        ],
        "mahavakya_sanskrit": "अस्तमित आदित्ये याज्ञवल्क्य चन्द्रमस्यस्तमिते शान्तेऽग्नौ शांतये वाचि किंज्योतिरेवायं पुरुष इति । आत्मैवास्य ज्योतिर्भवति ॥",
        "mahavakya_tamil_translit": "அஸ்தமித ஆதித்யே யாக்ஞவல்க்ய சந்த்ரமஸ்யஸ்தமிதே ஸாந்தேऽக்னௌ ஸாந்தாயாம் வாசி கிம்ஜ்யோதிரேவாயம் புருஷ இதி | ஆத்மைவாஸ்ய ஜ்யோதிர்பவதி ||",
        "mahavakya_meaning_english": "When the Sun has set, O Yajnavalkya, when the Moon has set, when the Fire has gone out, and when Speech is hushed, what is the light of this human being? The Atman alone is his Light!",
        "mahavakya_meaning_tamil": "யாக்ஞவல்கியரே! சூரியனும் மறைந்து, சந்திரனும் மறைந்து, நெருப்பும் அணைந்து, பேச்சும் அடங்கிவிட்ட இருளில் மனிதனுக்கு ஒளியாக இருப்பது எது? ஆத்மாவே அவனுக்கு ஒளியாகத் திகழ்கிறது!",
        "philosophical_theme": "Svayam-Jyotih (Self-Luminosity of the Atman); the Golden Swan (Hamsa) moving between waking and dream; and attaining absolute Fearlessness (Abhayam vai Janaka prapto'si).",
        "setting_specifics": "Emperor Janaka's private royal contemplation chamber transitioning from blazing daylight to sunset, moonset, extinguished fire, and the inner radiance of the heart.",
        "metaphor_highlight": "Sun -> Moon -> Fire -> Speech -> Atman as the Fivefold Light, the Great Fish (Mahamatsya) swimming effortlessly between two riverbanks, and the Caterpillar (Trinajalayuka) moving from one blade of grass to another.",
        "scenes": [
            {
                "camera": "Regal dolly shot inside Emperor Janaka's private audience hall as Maharishi Yajnavalkya arrives; Janaka rises immediately from his golden throne.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in the serene sandstone contemplation hall of Emperor Janaka in Mithila. As Maharishi Yajnavalkya enters in saffron robes, King Janaka steps down respectfully from his royal seat with folded hands to welcome the sage. Warm morning sunlight through carved stone lattices, no text, no borders.",
                "narration_en": "One day Maharishi Yajnavalkya visited the court of Emperor Janaka of Videha, intending at first not to speak at length. Yet years earlier, when they had conversed on the Agnihotra sacrifice, Yajnavalkya had granted Janaka a boon: to ask whatever question he wished whenever they met! Remembering that boon, Emperor Janaka bowed and asked the first profound question: 'Yajnavalkya, what serves as the light—Jyotih—for a human being here?'",
                "narration_ta": "ஒருநாள் விதேக மன்னர் ஜனகரின் அரசவைக்கு மகரிஷி யாக்ஞவல்கியர் வருகை தந்தார். முன்னொரு காலத்தில் அக்னிஹோத்ர வேள்வி குறித்த உரையாடலின்போது, 'நீ விரும்பும் எந்தக் கேள்வியையும் எப்போது வேண்டுமானாலும் கேட்கலாம்' என்ற வரத்தை ஜனகருக்கு யாக்ஞவல்கியர் அளித்திருந்தார். அந்த வரத்தை நினைவூட்டிய மன்னர் ஜனகர் பணிந்து முதல் கேள்வியைக் கேட்டார்: 'யாக்ஞவல்கியரே! இம்மனிதனுக்கு இவ்வுலகில் எது ஒளியாக (ஜோதியாக) இருந்து வழிகாட்டுகிறது?'",
                "subtitle_cue": "பிருஹதாரண்யக உபநிடதம்: 'மனிதனுக்கு எது ஒளியாகத் திகழ்கிறது?' — ஜனகரின் முதல் கேள்வி!",
                "sound_cue": "Regal Veena and Tanpura opening in Raga Darbari Kanada."
            },
            {
                "camera": "Time-lapse lighting transition across the Mithila courtyard: bright golden sunlight fades into crimson sunset, then silver moonlight, then glowing firelight.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic lighting transition across an ancient Indian palace courtyard overlooking a river: golden afternoon sunlight sets behind the horizon, replaced by silver moonlight, which then clouds over, leaving only a blazing brass fire brazier illuminating King Janaka and Sage Yajnavalkya, no text, no borders.",
                "narration_en": "Yajnavalkya answered first from the outer world: 'Adityo ज्योतिः, सम्राट्—The Sun is his light, O Emperor! For by the light of the Sun he sits, goes out, does his work, and returns.' Janaka asked: 'When the Sun has set, O Yajnavalkya, what serves as his light?' 'The Moon is his light!' 'And when both the Sun and the Moon have set?' 'Then Fire—Agni—is his light!' 'And when the Sun has set, the Moon has set, and the Fire has gone out?' 'Then Speech—Vak—is his light, for in pitch darkness one follows a voice!'",
                "narration_ta": "யாக்ஞவல்கியர் முதலில் புற உலகத்திலிருந்து தொடங்கினார்: 'மன்னா! சூரியனே மனிதனுக்கு ஒளியாக இருக்கிறான்; சூரிய ஒளியாலேயே அவன் அமர்கிறான், செல்கிறான், தன் பணிகளைச் செய்கிறான்!' ஜனகர் விடாமல் கேட்டார்: 'சூரியன் மறைந்த பின் எது ஒளியாக இருக்கிறது?' 'சந்திரனே ஒளியாக இருக்கிறான்!' 'சூரியனும் மறைந்து சந்திரனும் மறைந்த பின்?' 'நெருப்பே (அக்னியே) ஒளியாக இருக்கிறது!' 'சூரியனும் சந்திரனும் மறைந்து நெருப்பும் அணைந்த இருளில் எது வழிகாட்டுகிறது?' 'வாக்கே (குரல் ஒலியே) ஒளியாக இருந்து வழிகாட்டுகிறது!'",
                "subtitle_cue": "சூரியன் -> சந்திரன் -> அக்னி -> வாக்கு எனப் புற ஒளிகளைப் படிப்படியாகக் கடந்த விசாரணை!",
                "sound_cue": "Four distinct tonal shifts on Bansuri and Veena as each outer light fades into deeper stillness."
            },
            {
                "camera": "Complete darkness in the chamber except for a soft, warm inner golden radiance illuminating Yajnavalkya and Janaka's faces from within.",
                "veo_prompt": "16:9 8K 24fps photorealistic dramatic low-key shot inside the dark stone chamber after the fire brazier has gone out. Both Sun and Moon have set outside, yet a serene, warm golden spiritual light radiates from the hearts of Maharishi Yajnavalkya and King Janaka seated in meditation, no text, no subtitles, no borders.",
                "narration_en": "Then Emperor Janaka asked the ultimate question: 'Astamita aditye Yajnavalkya, chandramasy astamite, shante'gnau, shantayam vachi, kim-jyotir evayam purushah—When the Sun has set, when the Moon has set, when the Fire has gone out, and when all Speech is hushed in absolute silence, what then is the Light of this human being?' Yajnavalkya proclaimed the immortal answer: 'Atmaivasya jyotir bhavati—The Atman alone is his Light! By the self-luminous Light of the Self alone does he sit, move, know, and exist!'",
                "narration_ta": "அப்போது ஜனகர் இறுதிக் கேள்வியைக் கேட்டார்: 'யாக்ஞவல்கியரே! சூரியனும் மறைந்து, சந்திரனும் மறைந்து, நெருப்பும் அணைந்து, பேச்சும் அடங்கிவிட்ட நிசப்தமான இருளில் மனிதனுக்கு ஒளியாக இருப்பது எது?' யாக்ஞவல்கியர் அமர வாக்கியத்தை முழங்கினார்: 'ஆத்மைவாஸ்ய ஜ்யோதிர்பவதி — ஆத்மாவே அவனுக்கு ஒளியாகத் திகழ்கிறது! சுயமாக ஒளிரும் அந்த ஆத்ம ஜோதியினாலேயே சூரியனும் சந்திரனும் கூட ஒளி பெறுகின்றன!'",
                "subtitle_cue": "ஆத்மைவாஸ்ய ஜ்யோதிர்பவதி — எல்லா ஒளிகளும் அணைந்த பின்பும் சுயமாக ஒளிர்வது ஆத்ம ஜோதியே!",
                "sound_cue": "Deep, breathtaking silence pierced by a single pure, radiant Veena harmonic and temple bell."
            },
            {
                "camera": "Metaphorical shot of a great golden fish (Mahamatsya) gliding effortlessly between the eastern and western banks of a crystal river.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 underwater-and-surface shot of a crystal-clear sacred Indian river in golden light. A majestic golden fish (Mahamatsya) glides effortlessly between the sunlit right riverbank and the shaded moonlit left riverbank without being touched or obstructed by the currents, no text, no borders.",
                "narration_en": "'Which is that Atman?' asked Janaka. Yajnavalkya replied: 'Yo'yam विज्ञानमयः प्राणेषु हृद्यन्तर्ज्योतिः पुरुषः—This Purusha consisting of pure Consciousness, shining as the inner Light within the heart amidst the vital breaths! Remaining ever the same, It wanders through both worlds as if thinking, as if moving! Just as a great fish—Mahamatsya—swims effortlessly between both banks of a river, the eastern and the western, so does this Self glide unattached between Waking and Dream!'",
                "narration_ta": "'அந்த ஆத்மா எது?' என்று ஜனகர் கேட்டார். யாக்ஞவல்கியர் விளக்கினார்: 'பிராணன்களுக்கு நடுவே, இதயத்திற்குள் சுய ஒளியாகத் திகழும் விஞ்ஞானமய புருஷனே அந்த ஆத்மா! ஆற்றின் இரு கரைகளுக்கும் (கிழக்கு மற்றும் மேற்குக் கரைகளுக்கு) இடையே ஒரு பெரிய மீன் (மஹாமத்ஸ்ய) எவ்விதத் தடையுமின்றி நீந்திச் செல்வது போல், இந்த ஆத்மா விழிப்பு நிலைக்கும் கனவு நிலைக்கும் இடையே சற்றும் ஒட்டாமல் சாட்சியாக உலவுகிறது!'",
                "subtitle_cue": "ஆற்றின் இரு கரைகளுக்கும் இடையே நீந்தும் பெரிய மீனைப் போல் விழிப்பிற்கும் கனவிற்கும் இடையே உலவும் ஆத்மா!",
                "sound_cue": "Fluid, gliding Bansuri melody over gentle river water acoustics."
            },
            {
                "camera": "Skyward crane shot of a majestic Falcon (Shyena) folding its wings after flying all day to rest serenely in its nest—representing Deep Sleep (Sushupti).",
                "veo_prompt": "16:9 8K 24fps photorealistic twilight shot high in the Himalayas. A noble falcon (Shyena), having soared effortlessly across the vast golden sky, folds its wings peacefully and settles into its quiet mountain nest, symbolizing the soul entering the fearless bliss of deep sleep and Samadhi, no text, no borders.",
                "narration_en": "'And just as a falcon or an eagle, having flown across the vast sky, folds its wings and is borne down to its nest to rest—even so does this Spirit hasten to that state where, asleep, It desires no desire and sees no dream! There a father becomes no father, a mother no mother, the worlds no worlds, a thief no thief, a monk no monk; for It is untouched by good or evil, having passed beyond all the sorrows of the heart!'",
                "narration_ta": "'வான வெளியில் நெடுநேரம் பறந்து களைத்த வல்லூறு அல்லது கழுகு (ஷ்யேன), தன் சிறகுகளை மடக்கிக்கொண்டு அமைதியாகத் தன் கூட்டை நோக்கிச் செல்வது போல், இந்த ஜீவன் எந்த ஆசையும் எந்தக் கனவும் அற்ற ஆழ்ந்த உறக்கப் பெருநிலைக்குச் செல்கிறான்! அங்கே தந்தை தந்தையல்ல, தாய் தாயல்ல, உலகங்கள் உலகங்களல்ல; புண்ணியமும் பாவமும் அவனைத் தீண்டுவதில்லை; ஏனெனில் அப்போது அவன் இதயத்தின் எல்லாத் துயரங்களையும் கடந்த நிலையில் இருக்கிறான்!'",
                "subtitle_cue": "சிறகுகளை மடக்கிக் கூட்டில் இளைப்பாறும் கழுகைப் போல் இதயத் துயரங்களைக் கடந்த ஆத்ம நிலை!",
                "sound_cue": "Serene, weightless Violin and Tanpura sustain in Raga Neelambari."
            },
            {
                "camera": "Macro shot of a green caterpillar reaching the tip of a blade of grass and extending itself onto a fresh blade, followed by a goldsmith fashioning a newer, fairer ornament.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 macro shot in a sunlit ashram garden: a delicate green caterpillar reaches the tip of one blade of darbha grass and reaches across to grasp a fresh sunlit blade before letting go of the old one. In the background, Emperor Janaka bows his head at Yajnavalkya's feet, offering his entire kingdom and himself, no text, no borders.",
                "narration_en": "Explaining how the unliberated soul transmigrates like a caterpillar reaching for a new blade of grass before leaving the old, Yajnavalkya then declared how the desireless sage never transmigrates at all: 'Na tasya prana utkramanti, brahmaiva san brahmapyeti—His vital breaths do not depart; being Brahman already, he merges into Brahman! Just as the lifeless slough of a snake lies cast off on an anthill, so lies this mortal body, while the Immortal Spirit shines as Brahman, as Pure Light!'",
                "narration_ta": "அறியாமையில் உள்ள ஜீவன், புழு ஒரு புல்லின் நுனியிலிருந்து மற்றொரு புல்லைப் பிடித்த பிறகே பழைய புல்லை விடுவது போல் மறுபிறவி எடுக்கிறான்; ஆனால் ஆசைகளற்ற ஞானியின் பிராணன்களோ எங்கும் வெளியேறுவதில்லை! 'ப்ரஹ்மைவ ஸன் ப்ரஹ்மாப்யேதி — அவன் இங்கேயே பிரம்மமாக இருந்து பிரம்மத்திலேயே லயிக்கிறான்!' பாம்பு உரித்துப் போட்ட சட்டை புற்றின் மேல் கிடப்பது போல் இவ்வுடல் கிடக்க, உடலற்ற ஆத்மா பிரம்மமாகவே, பேரொளியாகவே திகழ்கிறது!",
                "subtitle_cue": "ப்ரஹ்மைவ ஸன் ப்ரஹ்மாப்யேதி — பிரம்மமாகவே இருப்பவன் இங்கேயே பிரம்மத்தோடு ஒன்றாகிறான்!",
                "sound_cue": "Triumphant Shankha and full Vedic swara chorus."
            },
            {
                "camera": "Wide golden-hour closing shot: Emperor Janaka lays his royal crown and entire Videha empire at Yajnavalkya's feet as the Guru blesses him with 'Abhayam'.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot in the royal court of Mithila bathed in golden sunrise light. Emperor Janaka kneels with folded hands before Maharishi Yajnavalkya, offering the entire kingdom of Videha and himself in complete surrender. Yajnavalkya raises his right hand in Abhaya mudra (Fearlessness), zero modern items, zero text, zero borders.",
                "narration_en": "Overwhelmed with realization, Emperor Janaka stepped forward and declared: 'So'ham bhagavate Videhan dadami, mam chapi saha दास्याय—Revered Master, I give you the entire empire of Videha, and myself also to be your humble servant!' And Maharishi Yajnavalkya blessed him with the supreme benediction: 'Abhayam vai Janaka prapto'si—Verily, O Janaka, you have attained Fearlessness!'",
                "narration_ta": "மெய்ஞ்ஞானப் பேரொளியில் திளைத்த மன்னர் ஜனகர், யாக்ஞவல்கியரின் திருவடிகளில் வீழ்ந்து வணங்கி, 'பகவானே! இந்த விதேக சாம்ராஜ்யம் முழுவதையும், உங்களுக்குத் தொண்டு செய்ய என்னையும் சேர்த்துத் தங்களுக்கு அர்ப்பணிக்கிறேன்!' என்றார். மகரிஷி யாக்ஞவல்கியர் வலக்கரம் உயர்த்தி வாழ்த்தினார்: 'அபயம் வை ஜனக ப்ராப்தோऽஸி — ஜனகா! நீ அச்சமற்ற அபய நிலையான மோட்சத்தை அடைந்துவிட்டாய்!'",
                "subtitle_cue": "அபயம் வை ஜனக ப்ராப்தோऽஸி — ஜனகா! நீ அச்சமற்ற அபயப் பெருநிலையை அடைந்துவிட்டாய்! ஓம் சாந்திஃ!",
                "sound_cue": "Shukla Yajur Veda Shanti Mantra 'Om Purnamadah Purnamidam' in majestic chorus."
            }
        ]
    },
    {
        "story_id": "MUKHYA_19_BRIHADARANYAKA_04",
        "muktika_number": 10,
        "upanishad_sanskrit": "बृहदारण्यकोपनिषद् (प्रजापतेः द-द-द उपदेशः)",
        "upanishad_iast": "Bṛhadāraṇyakopaniṣad (Prajāpateḥ Da-Da-Da Upadeśaḥ)",
        "upanishad_tamil": "பிருஹதாரண்யக உபநிடதம் (பிரஜாபதியின் 'த-த-த' இடி முழக்க உபதேசம்)",
        "upanishad_english": "Brihadaranyaka Upanishad (Story 4: Prajapati's Threefold Thunder - Damyata, Datta, Dayadhvam)",
        "veda": "Shukla Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "The Voice of the Thunder: How Gods, Humans & Asuras Heard One Syllable 'DA' in Three Ways",
        "story_title_tamil": "இடி முழங்கிய 'த - த - த' என்னும் ஒற்றை எழுத்து: புலனடக்கம், ஈகை மற்றும் கருணை!",
        "characters": [
            "Lord Prajapati (The Creator and Father of Devas, Manushyas, and Asuras)",
            "The Devas / Gods (Abundant in pleasures, needing Damyata—Self-Restraint)",
            "The Manushyas / Humans (Prone to hoarding, needing Datta—Charity/Giving)",
            "The Asuras / Titans (Fierce and powerful, needing Dayadhvam—Compassion)"
        ],
        "mahavakya_sanskrit": "तदेतत्त्रयं शिक्षेद् दमं दानं दयामिति । ॐ शान्तिः शान्तिः शान्तिः ॥",
        "mahavakya_tamil_translit": "ததேதத் த்ரயம் ஸிக்ஷேத் தமம் தானம் தயாமிதி | ஓம் ஸாந்திஃ ஸாந்திஃ ஸாந்திஃ ||",
        "mahavakya_meaning_english": "Therefore one should practice this threefold triad taught by the divine Thunder: Damam (Self-Control), Danam (Charity), and Dayam (Compassion)!",
        "mahavakya_meaning_tamil": "ஆகவே இடி முழக்கத்தின் வாயிலாக இறைவன் அருளிய தமம் (புலனடக்கம்), தானம் (ஈகை), தயை (கருணை) ஆகிய இம்மூன்றையும் ஒவ்வொருவரும் பயில வேண்டும்!",
        "philosophical_theme": "Psychological precision of Vedic ethics: the same teaching ('DA') is understood by each seeker according to their inner flaw (restless indulgence -> Damyata; greed -> Datta; cruelty/anger -> Dayadhvam).",
        "setting_specifics": "Lord Prajapati's cosmic hermitage beneath towering monsoon thunderclouds flashing over the Himalayan peaks.",
        "metaphor_highlight": "Da-Da-Da (The roaring sound of the Monsoon Thundercloud—Stanayitnu—reminding humanity of Damyata, Datta, Dayadhvam).",
        "scenes": [
            {
                "camera": "Wide epic shot of Lord Prajapati's mountain ashram where three distinct groups of disciples—Devas, Manushyas, and Asuras—complete their Brahmacharya.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in a grand Himalayan ashram. Three groups of disciples sit in respectful rows before the venerable sage-like Lord Prajapati by the sacred fire: radiant celestial Devas on the right, earnest human seekers in the center, and mighty, muscular Asura warriors on the left, golden morning light, no text, no borders.",
                "narration_en": "In the fifth chapter of the Brihadaranyaka Upanishad unfolds the timeless parable of the Threefold Offspring of Prajapati: the Devas (gods), the Manushyas (humans), and the Asuras (demons). All three lived as Brahmachari disciples with their Father Prajapati, serving him and purifying their minds.",
                "narration_ta": "பிருஹதாரண்யக உபநிடதத்தின் ஐந்தாம் அத்தியாயத்தில், பிரஜாபதியின் மூன்று வகைப் புதல்வர்களான தேவர்கள், மனிதர்கள் மற்றும் அசுரர்களின் அற்புதக் கதை இடம்பெறுகிறது. இம்மூவரும் தங்கள் தந்தையான பிரஜாபதியிடம் பிரம்மச்சரிய விரதம் பூண்டு குருகுல வாசம் செய்தனர்.",
                "subtitle_cue": "பிருஹதாரண்யக உபநிடதம்: பிரஜாபதியிடம் குருகுல வாசம் செய்த தேவர்கள், மனிதர்கள் மற்றும் அசுரர்கள்!",
                "sound_cue": "Deep, rumbling distant thunder blended with Tanpura and Shukla Yajur Veda swaras."
            },
            {
                "camera": "Medium shot of the radiant Devas bowing before Prajapati; he utters the single resonant syllable 'DA!' as lightning flashes on the horizon.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot in Prajapati's ashram. The radiant Devas in golden silk attire kneel with folded hands before Lord Prajapati, asking for their final instruction. Prajapati raises one finger and utters a single resonant syllable while a golden flash of lightning illuminates the distant clouds, no text, no borders.",
                "narration_en": "Having completed their study, the Devas approached him first and said: 'Bravitu no Bhagavan—Speak to us, O Lord! Give us our final instruction!' Unto them Prajapati uttered just a single syllable: 'DA!' Then he asked: 'Have you understood?' Looking within their own nature—which is abundant in pleasures and prone to sensory indulgence—the Devas answered: 'We have understood! You say to us: DAMYATA—Be self-restrained! Master your senses!' 'Om! Yes, you have understood!' said Prajapati.",
                "narration_ta": "முதலில் தேவர்கள் பிரஜாபதியை அணுகி, 'பகவானே! எங்களுக்கு இறுதி உபதேசம் அருளுங்கள்!' என்று வேண்டினர். பிரஜாபதி அவர்களிடம் 'த' (Da) என்ற ஒரேயொரு எழுத்தை மட்டும் உச்சரித்துவிட்டு, 'புரிந்ததா?' என்று கேட்டார்! போக இன்பங்களில் திளைத்துப் புலனடக்கம் இழக்கும் இயல்புடைய தேவர்கள் தங்களை உள்நோக்கிப் பார்த்து, 'புரிந்தது பகவானே! தம்யத (Damyata) — புலன்களை அடக்குங்கள் என்று எங்களுக்குக் கூறுகிறீர்கள்!' என்றனர். 'ஓம்! நன்கு புரிந்துகொண்டீர்கள்!' என்றார் பிரஜாபதி.",
                "subtitle_cue": "தேவர்களுக்கு 'த' (தம்யத) — போகங்களில் மயங்காமல் புலன்களை அடக்குங்கள்!",
                "sound_cue": "Sharp thunder-clap followed by a disciplined, steady Veena rhythm."
            },
            {
                "camera": "Medium shot of the human disciples (Manushyas) approaching Prajapati; again he utters only 'DA!' and they reflect upon their tendency to hoard.",
                "veo_prompt": "16:9 8K 24fps photorealistic shot in the Vedic ashram. The human disciples (Manushyas) in simple white cotton dhotis bow before Lord Prajapati by the sacred fire. As Prajapati utters the single syllable 'DA', the humans look at their own hands with realization, opening their palms in the gesture of generous charity (Datta), no text, no borders.",
                "narration_en": "Next, the human disciples—Manushyas—approached him and prayed: 'Speak to us, O Lord!' Unto them also Prajapati uttered that selfsame syllable: 'DA!' 'Have you understood?' Looking honestly into the human heart—which is ever anxious for tomorrow and prone to greed and hoarding—they replied: 'We have understood! You say to us: DATTA—Give! Share generously in charity!' 'Om! Yes, you have understood!' said Prajapati.",
                "narration_ta": "அடுத்து மனிதர்கள் பிரஜாபதியை அணுகி, 'பகவானே! எங்களுக்கும் உபதேசியுங்கள்!' என்று வேண்டினர். அவர்களிடமும் பிரஜாபதி 'த' (Da) என்ற அதே ஒற்றை எழுத்தை உச்சரித்து, 'புரிந்ததா?' என்று கேட்டார்! நாளைக்காகச் சேர்த்து வைக்கும் பேராசையும் கருமித்தனமும் கொண்ட மனித இயல்பை உணர்ந்த அவர்கள், 'புரிந்தது பகவானே! தத்த (Datta) — வாரி வழங்குங்கள், ஈகை செய்யுங்கள் என்று எங்களுக்குக் கூறுகிறீர்கள்!' என்றனர். 'ஓம்! நன்கு புரிந்துகொண்டீர்கள்!' என்றார் பிரஜாபதி.",
                "subtitle_cue": "மனிதர்களுக்கு 'த' (தத்த) — பேராசையை விடுத்து எல்லோருக்கும் பகிர்ந்து கொடுங்கள்!",
                "sound_cue": "Second thunder roll resolving into a warm, generous Bansuri melody in Raga Kalyani."
            },
            {
                "camera": "Medium shot of the powerful Asuras bowing before Prajapati; hearing 'DA!', they soften their fierce gaze in compassion (Dayadhvam).",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic shot in the ashram. The mighty Asura disciples kneel before Lord Prajapati. Hearing the syllable 'DA', their stern, fierce expressions melt into gentle compassion and mercy as they bow their heads toward a fragile forest deer nearby, warm golden lighting, no text, no subtitles, no borders.",
                "narration_en": "Third, the Asuras approached him and asked: 'Speak to us, O Lord!' Unto them too Prajapati uttered that single syllable: 'DA!' 'Have you understood?' Looking at their own fierce strength—which is prone to anger, cruelty, and harming others—the Asuras answered: 'We have understood! You say to us: DAYADHVAM—Be compassionate! Show mercy to all living beings!' 'Om! Yes, you have understood!' declared Prajapati.",
                "narration_ta": "மூன்றாவதாக அசுரர்கள் பிரஜாபதியை அணுகி, 'பகவானே! எங்களுக்கும் உபதேசியுங்கள்!' என்றனர். அவர்களிடமும் பிரஜாபதி 'த' (Da) என்ற அதே எழுத்தை உச்சரித்து, 'புரிந்ததா?' என்று கேட்டார்! வலிமையால் பிறரைத் துன்புறுத்தும் குரூர சுபாவம் கொண்ட அசுரர்கள், 'புரிந்தது பகவானே! தயத்வம் (Dayadhvam) — எல்லா உயிர்களிடத்தும் தயை காட்டுங்கள், கருணையோடு இருங்கள் என்று எங்களுக்குக் கூறுகிறீர்கள்!' என்றனர். 'ஓம்! நன்கு புரிந்துகொண்டீர்கள்!' என்றார் பிரஜாபதி.",
                "subtitle_cue": "அசுரர்களுக்கு 'த' (தயத்வம்) — வன்முறையை விடுத்து எல்லா உயிர்களிடத்தும் கருணை காட்டுங்கள்!",
                "sound_cue": "Third deep thunder rumble melting into a tender, compassionate Violin phrase."
            },
            {
                "camera": "Sweeping crane shot up into dark monsoon clouds rolling over the Himalayas, flashing golden lightning and roaring 'DA! DA! DA!'.",
                "veo_prompt": "Epic 16:9 8K 24fps photorealistic nature shot over the Himalayan peaks and green valleys of ancient India. Towering monsoon clouds flash with golden lightning and send gentle, life-giving rain over rivers and forests, visually echoing the cosmic thunder voice 'Da - Da - Da'. Below, sages look up in reverence, no text, no borders.",
                "narration_en": "And the Upanishad reveals that even today, whenever the heavenly Thundercloud—Daivi Vak, the Divine Voice of the Sky—roars across the heavens with the sound 'DA! DA! DA!', it is repeating Prajapati's eternal instruction to all humanity: 'Damyata! Datta! Dayadhvam! Restrain yourselves! Give generously! Be compassionate!'",
                "narration_ta": "இன்றும் கூட வானில் இடி முழங்கும்போது 'த! த! த!' என்று ஒலிக்கும் அந்தத் தெய்வீகக் குரல் (தைவீ வாக்), பிரஜாபதியின் அதே உபதேசத்தைத்தான் நமக்கு நினைவூட்டுகிறது என்கிறது உபநிடதம்: 'தம்யத! தத்த! தயத்வம்! புலன்களை அடக்குங்கள்! வாரி வழங்குங்கள்! கருணை காட்டுங்கள்!'",
                "subtitle_cue": "வானில் முழங்கும் இடியோசை இன்றும் நினைவூட்டும் மந்திரம்: தம்யத! தத்த! தயத்வம்!",
                "sound_cue": "Three majestic thunderclaps synchronized with full Vedic chorus chanting 'Da! Da! Da!'."
            },
            {
                "camera": "Montage inside a single human seeker's day: practicing self-restraint in meditation, giving food to a guest, and protecting a wounded bird.",
                "veo_prompt": "16:9 8K 24fps photorealistic harmonious scene in a Vedic ashram showing all three virtues in one seeker's life: meditating with calm self-control by the fire (Dama), offering food on a banana leaf to a traveler (Dana), and gently cradling a small dove in his palms (Daya), warm golden sunlight, no text, no borders.",
                "narration_en": "As Acharya Adi Shankara explains in his great commentary, there are no separate gods or demons outside us—all three tendencies dwell within every human heart! When we are swept away by desire and restlessness, we are like Devas and need Dama (Self-Control). When we cling selfishly to wealth, we need Dana (Charity). And when anger or harshness rises within us, we are like Asuras and need Daya (Compassion)!",
                "narration_ta": "ஆதிசங்கர பகவத்பாதர் தன் பாஷ்யத்தில் விளக்குவது போல், தேவர்களும் அசுரர்களும் நமக்கு வெளியே எங்கோ இல்லை — மனித மனத்திற்குள்ளேயே இம்மூன்று குணங்களும் உள்ளன! ஆசைகளால் புலன்கள் அலைபாயும்போது நமக்கு 'தமம்' (புலனடக்கம்) தேவை; சுயநலமும் பேராசையும் எழும்போது 'தானம்' (ஈகை) தேவை; சினமும் வன்மமும் எழும்போது 'தயை' (கருணை) தேவை!",
                "subtitle_cue": "ஒவ்வொரு மனித உள்ளத்திற்கும் தேவையான மூன்று அருமருந்துகள்: தமம், தானம், தயை!",
                "sound_cue": "Harmonious trio of Veena, Bansuri, and Mridangam playing in serene balance."
            },
            {
                "camera": "Wide sunlit closing shot of the ashram after the rain, with a shimmering rainbow arch in the sky and sages chanting 'Om Purnamadah Purnamidam'.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot of the Himalayan Vedic ashram after a refreshing monsoon shower. Golden sunlight breaks through the clouds, illuminating lush green trees, lotus ponds, and sages chanting around the sacred fire altar. Pure ancient Bharata peace, zero modern objects, zero text, zero borders.",
                "narration_en": "'Tad etat trayam shikshed damam danam dayam iti—Therefore let every seeker practice this sacred triad: Self-Control, Charity, and Compassion!' For where Dama, Dana, and Daya blossom together, the heart becomes a spotless mirror reflecting the Infinite Brahman!",
                "narration_ta": "'ததேதத் த்ரயம் ஸிக்ஷேத் தமம் தானம் தயாமிதி — ஆகவே தமம் (புலனடக்கம்), தானம் (ஈகை), தயை (கருணை) ஆகிய இம்மூன்றையும் ஒவ்வொருவரும் பயில வேண்டும்!' இம்மூன்றும் மலரும் தூய இதயத்தில் பூரணப் பரம்பொருள் தானாகவே பிரதிபலிக்கிறது!",
                "subtitle_cue": "ததேதத் த்ரயம் ஸிக்ஷேத் தமம் தானம் தயாமிதி — புலனடக்கம், ஈகை, கருணை! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!",
                "sound_cue": "Shukla Yajur Veda Shanti Mantra 'Om Purnamadah Purnamidam' fading into peaceful rain-washed birdsong."
            }
        ]
    }
]


MUKHYA_PART5 = [
    {
        "story_id": "MUKHYA_20_SHVETASHVATARA_01",
        "muktika_number": 14,
        "upanishad_sanskrit": "श्वेताश्वतरोपनिषद्",
        "upanishad_iast": "Śvetāśvataropaniṣad",
        "upanishad_tamil": "சுவேதாஸ்வதர உபநிடதம்",
        "upanishad_english": "Shvetashvatara Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "Sage Shvetashvatara's Brahma-Chakra & The Churning of Fire: How Dhyana-Yoga Reveals Mahesvara",
        "story_title_tamil": "சுவேதாஸ்வதர முனிவரின் பிரம்ம சக்கரமும் தியான யோகமும்: அரணிக் கட்டையைக் கடைந்து அக்னியைக் காண்பது போல் ஈசனைத் தரிசித்தல்!",
        "characters": [
            "Maharishi Shvetashvatara (The sage of pure white senses who realized the Supreme through Tapas and Guru-grace)",
            "Assembly of Brahma-Vadin Rishis (Debating whether Time, Nature, Fate, Chance, or Elements are the First Cause)",
            "Rudra / Mahesvara (The One Supreme Lord ruling the Brahma-Chakra through His Devatma-Shakti)"
        ],
        "mahavakya_sanskrit": "तिलेषु तैलं दधिनीव सर्पिरापः स्रोतःस्वरणीषु चाग्निः । एवमात्मात्मनि गृह्यतेऽसौ सत्येनैनं तपसा योऽनुपश्यति ॥",
        "mahavakya_tamil_translit": "திலேஷு தைலம் ததினீவ ஸர்பிராபஃ ஸ்ரோதஃஸ்வரணீஷு சாக்னிஃ | ஏவமாத்மாத்மனி க்ருஹ்யதேऽஸௌ ஸத்யேனைனம் தபஸா யோऽனுபஸ்யதி ||",
        "mahavakya_meaning_english": "As oil in sesame seeds, as butter in curds, as water in underground riverbeds, and as fire in friction-sticks (Arani), so is that Supreme Self realized within oneself through Truth and Austerity!",
        "mahavakya_meaning_tamil": "எள்ளில் எண்ணெய் போலவும், தயிரில் வெண்ணெய் போலவும், ஆற்று மணலில் ஊற்று நீர் போலவும், அரணிக் கட்டையில் நெருப்பு போலவும், சத்தியத்தாலும் தவத்தாலும் தேடுபவனுக்கு ஆத்மா உள்ளத்திலேயே வெளிப்படுகிறது!",
        "philosophical_theme": "Refutation of Materialism/Fatalism (Kala, Svabhava, Niyati, Yadrichchha); Dhyana-Yoga (Body as lower Arani stick, Om as upper stick, Meditation as churning); and Para-Bhakti (Yasya deve para bhaktih yatha deve tatha gurau).",
        "setting_specifics": "A grand Himalayan forest assembly of Brahma-vadins gathered around Maharishi Shvetashvatara, with a carved stone wheel, sesame press, butter churn, and Vedic Arani fire-sticks.",
        "metaphor_highlight": "Brahma-Chakra (The Cosmic Wheel), Arani Fire-Churning (Body = lower stick, Pranava = upper stick), Oil in Sesame / Butter in Curds, and Rolling up the Sky like a Leather Scroll (Charmavad Akasham).",
        "scenes": [
            {
                "camera": "Wide tracking shot across a misty Himalayan cedar grove where dozens of Vedic sages sit in circular inquiry around a blazing fire.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in a misty Himalayan deodar cedar forest at dawn. A circle of venerable Vedic sages (Brahma-vadins) in ochre and white cotton robes sit around a blazing Agnihotra altar, engaged in deep philosophical inquiry into the Ultimate Cause of the universe, golden sunbeams piercing the mist, no text, no borders.",
                "narration_en": "In the sacred assembly that opens the Shvetashvatara Upanishad, the great Brahma-vadins sat inquiring into the ultimate mystery: 'Kim karanam Brahma? Kutah smajatah? What is the First Cause? Is it Brahman? Whence are we born, by what do we live, and where do we rest at last? O knowers of Brahman, tell us by whom governed we walk through pleasure and pain!'",
                "narration_ta": "சுவேதாஸ்வதர உபநிடதத்தின் தொடக்கத்தில் பிரம்மவாதிகளான மகரிஷிகள் ஒன்றுகூடி ஆழ்ந்த விசாரணையில் ஈடுபட்டனர்: 'கிம் காரணம் பிரம்ம? குதஃ ஸ்ம ஜாதா? இப்பிரபஞ்சத்தின் மூல காரணம் எது? நாம் எங்கிருந்து பிறந்தோம்? எதனால் வாழ்கிறோம்? இறுதியில் எங்கே நிலைபெறுகிறோம்? இன்ப-துன்பச் சுழலில் யாரால் இயக்கப்படுகிறோம்?'",
                "subtitle_cue": "சுவேதாஸ்வதர உபநிடதம்: 'கிம் காரணம் பிரம்ம?' — பிரபஞ்சத்தின் மூல காரணம் எது?",
                "sound_cue": "Deep Krishna Yajur Veda opening chant with resonant Tanpura and mountain wind."
            },
            {
                "camera": "Visual montage of partial theories: a sundial shadow (Time/Kala), growing plants (Nature/Svabhava), rolling dice (Chance/Yadrichchha), and the five elements—all shown revolving on a giant cosmic wheel.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 symbolic shot in an ancient Vedic ashram showing a stone sundial, sprouting plants, water, fire, and wind, while behind them a colossal translucent golden wheel (Brahma-Chakra) with fifty spokes revolves silently in the sky. Maharishi Shvetashvatara sits in deep meditation at the center, no text, no borders.",
                "narration_en": "The thinkers examined every worldly theory: 'Should Time (Kala), or inherent Nature (Svabhava), or Destiny (Niyati), or blind Chance (Yadrichchha), or the five Elements, or the individual Jiva be considered the Ultimate Cause?' No! For all of these are non-intelligent or bound by karma! Plunging into Dhyana-Yoga, the sages beheld the self-luminous Power of the Supreme Lord—Devatma-Shakti—hidden behind His own Gunas, turning the vast Brahma-Chakra in which the soul flutters like a swan!",
                "narration_ta": "'காலம் (Kala), இயற்கை சுபாவம் (Svabhava), விதி (Niyati), தற்செயல் நிகழ்வு (Yadrichchha), பஞ்ச பூதங்கள் அல்லது ஜீவன் — இவற்றுள் எது மூல காரணம்?' என்று ஆராய்ந்தனர். இவை எதுவுமே தனித்து இயங்கும் ஆற்றல் கொண்டவையல்ல! அப்போது தியான யோகத்தில் ஆழ்ந்த முனிவர்கள், முக்குணங்களால் மறைக்கப்பட்ட இறைவனின் 'தேவாத்ம சக்தி'யை நேரில் தரிசித்தனர்! அந்த ஏகப் பரம்பொருளே பிரம்ம சக்கரத்தை இயக்குகிறது!",
                "subtitle_cue": "காலமும் விதியும் காரணமல்ல — தியான யோகத்தால் வெளிப்பட்ட இறைவனின் தேவாத்ம சக்தி!",
                "sound_cue": "Revolving rhythmic Mridangam cycle resolving into a majesticRudra Veena chord."
            },
            {
                "camera": "Macro sequence in the ashram: pressing golden oil from sesame seeds, churning white butter from curds, digging water in a dry riverbed, and rubbing wooden Arani sticks to spark fire.",
                "veo_prompt": "16:9 8K 24fps photorealistic four-part detail shot in a Vedic gurukulam: golden oil pressed from sesame seeds, white butter churned in an earthen pot, clear spring water welling up in sandy riverbeds, and a priest twirling a wooden Arani fire-stick to kindle a bright flame. Warm natural lighting, zero text, zero borders.",
                "narration_en": "How can that unseen Lord be perceived within oneself? Maharishi Shvetashvatara gave four unforgettable illustrations: 'Tileshu tailam dadhiniva sarpih, apah srotahsu aranishu chagnih! Just as oil is hidden in sesame seeds, butter in curds, underground water in dry riverbeds, and fire in two wooden Arani sticks—even so is that Supreme Atman grasped within one's own heart by him who seeks It with Truth and Austerity!'",
                "narration_ta": "கண்ணுக்குத் தெரியாத அந்த ஈசனை நம்முள்ளேயே காண்பது எப்படி? சுவேதாஸ்வதர முனிவர் நான்கு அற்புத உவமைகளைக் கூறினார்: 'திலேஷு தைலம் ததினீவ ஸர்பிஃ... எள்ளுக்குள் எண்ணெய் மறைந்திருப்பது போலவும், தயிருக்குள் வெண்ணெய் உறைந்திருப்பது போலவும், ஆற்று மணலுக்குள் ஊற்று நீர் இருப்பது போலவும், அரணிக் கட்டைக்குள் நெருப்பு மறைந்திருப்பது போலவும், சத்தியத்தாலும் தவத்தாலும் தேடுபவனுக்கு ஆத்மா தன் உள்ளத்திலேயே பிடிபடுகிறது!'",
                "subtitle_cue": "எள்ளில் எண்ணெயும் தயிரில் வெண்ணெயும் அரணியில் நெருப்பும் போல் உள்ளத்தில் உறையும் ஆத்மா!",
                "sound_cue": "Rhythmic churning sound of the wooden Arani drill igniting into a bright Bansuri flourish."
            },
            {
                "camera": "Close-up of Maharishi Shvetashvatara seated in flawless Yoga posture by a serene mountain brook, head, neck, and chest held erect in one straight line.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot of Maharishi Shvetashvatara meditating in a sheltered, level mountain cave beside a gentle pebble-strewn stream. His body—chest, neck, and head—is held perfectly erect (Trirunnatam), with a dusty mirror being polished into a blazing golden disc beside him, no text, no subtitles, no borders.",
                "narration_en": "Then the Upanishad teaches the exact science of Dhyana-Yoga: 'Make your own body the lower Arani fire-stick, and make the sacred syllable Pranava (OM) the upper stick! By practising the friction of continuous Meditation (Dhyana-nirmathanabhyasat), behold the hidden God like fire blazing forth! Holding the body erect in three parts—chest, neck, and head—in a quiet spot sheltered from wind, withdraw the senses into the heart with the raft of Brahman! Just as a dusty metal mirror shines like the sun once polished, so the embodied soul beholds the Self and becomes sorrowless!'",
                "narration_ta": "அடுத்து தியான யோகத்தின் செய்முறையை உபநிடதம் போதிக்கிறது: 'உன் உடலையே கீழ் அரணிக் கட்டையாகவும், பிரணவ மந்திரமான ஓங்காரத்தையே மேல் அரணிக் கட்டையாகவும் கொள்! தியானம் என்னும் கடைதலால் உள்ளே மறைந்திருக்கும் இறைவனை நெருப்பைப் போல் நேரில் தரிசிப்பாயாக! மார்பு, கழுத்து, தலை ஆகிய மூன்றையும் நேராக வைத்து (த்ரிருன்னதம்), மனதால் புலன்களை இதயத்தில் ஒடுக்கிப் பிரம்மம் என்னும் தெப்பத்தால் பிறவிக் கடலைக் கடப்பாயாக! மண் படிந்த கண்ணாடி துடைக்கப்பட்டவுடன் சுடர்விடுவது போல் ஆத்மாவைத் தரிசித்தவன் துக்கமற்றவனாகிறான்!'",
                "subtitle_cue": "உடலைக் கீழ் அரணியாகவும் ஓங்காரத்தை மேல் அரணியாகவும் கொண்டு தியானத்தால் ஈசனைக் கடைந்தெடு!",
                "sound_cue": "Deep, steady Pranayama breath cadence with soaring Veena and Tambura harmonics."
            },
            {
                "camera": "Cosmic vision of Rudra-Mahesvara as the One Architect pervading every face, every neck, and every heart in the universe.",
                "veo_prompt": "16:9 8K 24fps photorealistic spiritual vision: above the Himalayan peaks shines the serene, auspicious cosmic presence of Mahesvara (Shiva-Vishvamurti) in golden light, reflected in every man, woman, youth, maiden,elderly person with a staff, blue bee, green parrot, and ocean wave below, no text, no borders.",
                "narration_en": "Beholding that One Reality, Shvetashvatara sang the cosmic hymn of oneness: 'Eko hi Rudro na dvitiyaya tasthur—Rudra is truly One; the wise admit no second! Tvam stri tvam puman asi, tvam kumara uta va kumari, tvam jirno dandena வञ्चसि—Thou art the woman, Thou art the man; Thou art the youth and the maiden too; Thou art the old man tottering with a staff! Thou art the dark-blue bee, the green parrot with red eyes, the thundercloud, the seasons, and the oceans!'",
                "narration_ta": "அந்த ஏகப் பரம்பொருளைத் தரிசித்த முனிவர் பாடினார்: 'ஏகோ ஹி ருத்ரோ ந த்விதீயாய தஸ்துஃ — ருத்ரன் ஒருவனே, இரண்டாவது பொருள் இல்லை! த்வம் ஸ்த்ரீ த்வம் புமான் அஸி... நீயே பெண், நீயே ஆண்! நீயே பாலகன், நீயே கன்னிப் பெண்! நீயே கோலூன்றி நடக்கும் முதியவனும் ஆகிறாய்! நீயே கருநீல வண்டு, செங்கண் பச்சைக் கிளி, மின்னல் மேகம், பருவங்கள் மற்றும் சமுத்திரங்கள் அனைத்தும் நீயே!'",
                "subtitle_cue": "த்வம் ஸ்த்ரீ த்வம் புமான் அஸி — ஆணும் பெண்ணும் பாலகனும் முதியவனும் இயற்கையும் நீயே!",
                "sound_cue": "Ecstatic Vedic hymn in Raga Hamsadhvani with temple bells, conch, and Mridangam."
            },
            {
                "camera": "Dramatic visual metaphor: a man attempting to roll up the vast starry sky like a leather mat, contrasted with effortless realization through Guru-Kripa.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 cinematic shot on a mountain ridge at twilight. The vast starry night sky above seems impossible to roll up like a scroll of leather, yet below, Maharishi Shvetashvatara sits in effortless liberation before the sacred fire, radiating supreme peace and devotion, no text, no subtitles, no borders.",
                "narration_en": "Here thunders the supreme warning against trying to end sorrow without Self-knowledge: 'Yada charmavad akasham veshtayishyanti manavah, tada devam avijnaya duhkhasyanto bhavishyati! Only when human beings can roll up the boundless sky like a piece of leather will there ever be an end to sorrow without realizing the Effulgent God within!'",
                "narration_ta": "ஆத்ம ஞானமின்றித் துக்கத்தை நீக்க முடியாது என்பதை ஓர் அற்புத உவமையால் முழங்குகிறது உபநிடதம்: 'யதா சர்மவத் ஆகாஸம் வேஷ்டயிஷ்யந்தி மானவாஃ, ததா தேவமவிஜ்ஞாய துக்கஸ்யாந்தோ பவிஷ்யதி! மனிதர்களால் எப்போது எல்லையற்ற ஆகாயத்தை ஒரு தோல் பாயைப் போல் சுருட்டி மடிக்க முடியுமோ, அப்போதுதான் இறைவனை அறியாமல் துக்கத்திற்கு முடிவு ஏற்படும்! ஆகவே ஈசனை அறிவதால் மட்டுமே பிறவித் துயர் நீங்கும்!'",
                "subtitle_cue": "ஆகாயத்தைத் தோல் பாய் போல் சுருட்ட முடிந்தால் மட்டுமே, இறைவனை அறியாமல் துக்கம் நீங்கும்!",
                "sound_cue": "Powerful dramatic pause followed by a serene, resolute Bansuri melody."
            },
            {
                "camera": "Wide closing shot of Maharishi Shvetashvatara blessing the highest ascetics (Atyashraminah) as they bow to God and Guru as One.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing tableau in the Himalayan deodar forest at golden sunrise. Ascetics and disciples bow with folded hands in Para-Bhakti before Maharishi Shvetashvatara beside the sacred fire. Golden light floods the valley, pure Vedic devotion, zero modern items, zero text, zero borders.",
                "narration_en": "By the power of his Tapas and the grace of the Lord, Sage Shvetashvatara imparted this supreme Brahman to the highest ascetics. And the Upanishad seals its teaching with the immortal verse of Guru-Bhakti: 'Yasya deve para bhaktih, yatha deve tatha gurau, tasyaite kathita hyarthah prakashante mahatmanah! Unto that great soul who has supreme devotion to God, and the very same devotion to his Guru as to God, do all these truths shine forth in full splendor!'",
                "narration_ta": "தன் தவ வலிமையாலும் இறைவனின் திருவருளாலும் பிரம்மத்தை நேரில் உணர்ந்த சுவேதாஸ்வதர முனிவர், பரமஹம்ச சந்நியாசிகளுக்கு இவ்வுபதேசத்தை வழங்கினார். உபநிடதம் குரு பக்தியின் மகுட வாக்கியத்தோடு நிறைவடைகிறது: 'யஸ்ய தேவே பரா பக்திஃ யதா தேவே ததா குரௌ, தஸ்யைதே கதிதா ஹ்யர்த்தாஃ ப்ரகாஸந்தே மஹாத்மனஃ! எவனுக்கு இறைவனிடத்தில் பரம பக்தி உள்ளதோ, இறைவனிடத்தில் உள்ளது போலவே குருவிடத்திலும் பக்தி உள்ளதோ, அந்த மகாத்மாவிற்கே இந்த உபநிடத ரகசியங்கள் அனைத்தும் உள்ளங்கை நெல்லிக்கனி போல் விளங்கும்!'",
                "subtitle_cue": "யஸ்ய தேவே பரா பக்திஃ யதா தேவே ததா குரௌ — தெய்வத்திடமும் குருவிடமும் பரம பக்தி கொண்டவர்க்கே ஞானம் ஒளிரும்!",
                "sound_cue": "Krishna Yajur Veda Shanti Mantra 'Om Saha Navavatu... Om Shantih Shantih Shantih'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_21_KAUSHITAKI_01",
        "muktika_number": 25,
        "upanishad_sanskrit": "कौषीतकिब्राह्मणोपनिषद्",
        "upanishad_iast": "Kauṣītakibrāhmaṇopaniṣad",
        "upanishad_tamil": "கௌஷீதகி உபநிடதம்",
        "upanishad_english": "Kaushitaki Upanishad",
        "veda": "Rig Veda",
        "category": "Mukhya",
        "story_title_english": "King Pratardana & Indra's Boon, Balaki & King Ajatashatru: The Chariot Wheel of Prana & Prajna",
        "story_title_tamil": "பிரதர்தனனுக்கு இந்திரன் அருளிய வரமும் அஜாதசத்ருவின் உபதேசமும்: பிராணனும் பிரக்ஞையும் ஒன்றே!",
        "characters": [
            "King Pratardana Daivodasi (Heroic king who reached Indra's abode and asked Indra to choose the highest boon for mankind)",
            "Indra (Revealer of Prana-Prajnatman: 'Know Me alone as the Conscious Life-Breath')",
            "Dripta-Balaki Gargya (A proud Vedic scholar who knew 12 partial meditations on Brahman)",
            "Rajarishi Ajatashatru of Kashi (Philosopher-king of Varanasi who awakened a sleeping man to reveal the Atman)"
        ],
        "mahavakya_sanskrit": "प्राणोऽस्मि प्रज्ञात्मा तं मामायुरमृतमित्युपास्स्व । तद्यथा रथस्यारेषु नेमिरर्पिता नाभावरा अर्पिता एवमेवैता भूतमात्राः प्रज्ञामात्रास्वपितः ॥",
        "mahavakya_tamil_translit": "ப்ராணோऽஸ்மி ப்ரஜ்ஞாத்மா தம் மாமாயுரமிருதமித்யுபாஸ்ஸ்வ | தத்யதா ரதஸ்யாரேஷு நேமிரர்பிதா நாபாவரா அர்பிதா ஏவமேவைதா பூதமாத்ராஃ ப்ரஜ்ஞாமாத்ராஸ்வர்பிதாஃ ||",
        "mahavakya_meaning_english": "I am Prana, the Conscious Self (Prajnatman); meditate on Me as Life and Immortality! Just as the rim of a chariot wheel is fixed on the spokes and the spokes on the hub, so the elements are fixed in Consciousness and Consciousness in Prana!",
        "mahavakya_meaning_tamil": "நானே பேரறிவு வடிவான பிராணன் (ப்ரஜ்ஞாத்மா); என்னையே ஆயுளாகவும் அமிர்தமாகவும் தியானிப்பாயாக! தேர்ச்சக்கரத்தின் விளிம்பு ஆரக்கால்களிலும், ஆரக்கால்கள் குமிழிலும் நிலைத்திருப்பது போல் அனைத்தும் பிரக்ஞையிலும் பிராணனிலும் நிலைத்துள்ளன!",
        "philosophical_theme": "Unity of Prana (Vital Life) and Prajna (Pure Consciousness); the River Vijara (Ageless River) on the path to Brahman; and King Ajatashatru waking a sleeping man to show where consciousness rests.",
        "setting_specifics": "King Ajatashatru's sacred court in Kashi (Varanasi) along the Ganga, and Indra's luminous hall where King Pratardana receives the supreme boon.",
        "metaphor_highlight": "Chariot Wheel Rim, Spokes, and Hub (Nemi, Ara, Nabhi); Sparks from a Blazing Fire; Razor inside a Razor-case (Kshura-dhana); and the Ageless River Vijara.",
        "scenes": [
            {
                "camera": "Majestic tracking shot through the sacred ghats and royal hall of Kashi (Varanasi), where proud scholar Balaki Gargya approaches Rajarishi Ajatashatru.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in the ancient sandstone royal hall of Kashi (Varanasi) overlooking the sacred Ganga river at dawn. The proud Vedic scholar Balaki Gargya stands before Philosopher-King Ajatashatru seated on a simple royal seat, offering to teach him Brahman, warm golden morning light, no text, no borders.",
                "narration_en": "Belonging to the Rig Veda and standing at #25 in the Muktika canon, the Kaushitaki Upanishad weaves together three luminous narratives of Self-knowledge! In the ancient city of Kashi, the proud scholar Balaki Gargya once approached Rajarishi Ajatashatru and declared boastfully: 'O King, I will teach you Brahman!' Ajatashatru replied with royal generosity: 'For that single word alone I offer you a thousand cows! People rush to King Janaka of Videha crying 'Janaka! Janaka!'—let me hear your wisdom!'",
                "narration_ta": "ரிக் வேதத்தைச் சேர்ந்ததும் முக்திக வரிசையில் 25-ஆவது உபநிடதமாகத் திகழ்வதுமான கௌஷீதகி உபநிடதம், ஆத்ம ஞானத்தின் அற்புத வரலாறுகளைக் கூறுகிறது! ஒருமுறை காசி நகரத்து அரசரான ராஜரிஷி அஜாதசத்ருவிடம் சென்ற பண்டிதர் பாலாகி கார்கியர், 'மன்னா! உமக்கு நான் பிரம்மத்தை உபதேசிக்கிறேன்!' என்று கர்வத்துடன் கூறினார். மன்னரோ, 'இந்த ஒரு வார்த்தைக்காகவே உமக்கு ஆயிரம் பசுக்களைத் தருகிறேன், கூறுங்கள்!' என்றார்.",
                "subtitle_cue": "கௌஷீதகி உபநிடதம்: காசி மன்னர் அஜாதசத்ருவிடம் பிரம்மத்தை உபதேசிக்க வந்த பாலாகி!",
                "sound_cue": "Regal Rig Vedic chant with Varanasi temple bells and Ganga water ambience."
            },
            {
                "camera": "Medium shot in the Kashi palace corridor: after Balaki falls silent, King Ajatashatru leads him by the hand to a man sleeping deeply on a stone bench.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot in a quiet pillared corridor of the Kashi palace. After the scholar Balaki stands silent with bowed head, King Ajatashatru leads him to a man sleeping deeply on a stone couch. The King calls the sleeper by mystic names of Prana, then gently touches him with his staff until the man wakes up, no text, no borders.",
                "narration_en": "Balaki recited twelve meditations—on the Person in the Sun, Moon, Lightning, Thunder, Wind, Space, Fire, Water, Mirror, Echo, Shadow, and Body! Each time, King Ajatashatru showed that these are only conditioned attributes, until Balaki fell completely silent! Then the humble scholar bowed and asked the King to become his Guru. Ajatashatru took Balaki by the hand and walked to a man who was fast asleep! First the King called out: 'O Great One clad in white! O Soma King!'—yet the sleeper did not stir. Only when the King touched him with his staff did the man wake up!",
                "narration_ta": "பாலாகி சூரியன், சந்திரன், மின்னல், இடி, காற்று, ஆகாயம், நெருப்பு, நீர், கண்ணாடி, எதிரொலி, நிழல், உடல் ஆகிய பன்னிரண்டு இடங்களில் உள்ள புருஷனைப் பிரம்மம் என்று கூறினார். அவை அனைத்தும் பிரம்மத்தின் சிறு அம்சங்களே என்று மன்னர் விளக்கியதும் பாலாகி மௌனமாகி, மன்னரையே குருவாகச் சரணடைந்தார்! அஜாதசத்ரு அவரை அழைத்துக்கொண்டு ஆழ்ந்த உறக்கத்தில் இருந்த ஒரு மனிதனிடம் சென்றார். பெயர் சொல்லி அழைத்தும் எழாத அம்மனிதனை, கோலால் தொட்டு எழுப்பியபோது அவன் விழித்தெழுந்தான்!",
                "subtitle_cue": "ஆழ்ந்த உறக்கத்திலிருந்த மனிதனை எழுப்பி ஆத்மாவின் இருப்பிடத்தைக் காட்டிய அஜாதசத்ரு!",
                "sound_cue": "Quiet rhythmic breathing in sleep interrupted by a gentle wooden staff tap and awakening flute."
            },
            {
                "camera": "Close-up of a carved wooden razor-case holding a gleaming blade, and sparks flying from a blazing fire, illustrating how the senses rest in the heart.",
                "veo_prompt": "16:9 8K 24fps photorealistic macro-to-medium shot in the Kashi hall: a gleaming bronze razor resting snugly inside its carved wooden case (Kshura-dhana), and glowing sparks radiating from a sacred fire altar. King Ajatashatru explains to Balaki how the Atman pervades the body right to the tips of the fingernails, no text, no borders.",
                "narration_en": "King Ajatashatru asked: 'Where did this man rest while asleep, and whence did he just return?' Explaining the secret of the heart's subtle nadis—Hita—finer than a hair split a thousand times, the King declared: 'In deep sleep all speech, sight, hearing, and mind merge into Prana alone! And when he wakes, just as sparks fly forth in all directions from a blazing fire, so the vital powers issue from this Atman! Just as a razor rests in a razor-case, this Conscious Self enters the body right down to the tips of the fingernails!'",
                "narration_ta": "அஜாதசத்ரு கேட்டார்: 'உறங்கும்போது இம்மனிதன் எங்கே தங்கியிருந்தான்? விழித்தவுடன் எங்கிருந்து திரும்பி வந்தான்?' முடியை ஆயிரம் கூறாகப் பிளந்தது போன்ற நுண்ணிய 'ஹிதா' நாடிகளின் வழியே ஆழ்ந்த உறக்கத்தில் புலன்கள் அனைத்தும் பிராணனில் ஒடுங்குவதை மன்னர் விளக்கினார்: 'எரியும் நெருப்பிலிருந்து தீப்பொறிகள் கிளம்புவது போல் விழிப்பு நிலையில் ஆத்மாவிலிருந்து புலன்களும் உலகங்களும் வெளிப்படுகின்றன! சவரக் கத்தி தன் உறைக்குள் பொருந்தியிருப்பது போல், தலைமுடி முதல் நகக்கண் வரை இவ்வுடலுக்குள் ஆத்மா நிறைந்துள்ளது!'",
                "subtitle_cue": "கத்தி உறைக்குள் இருப்பது போல் நகக்கண் வரை உடலுக்குள் நிறைந்திருக்கும் பிரக்ஞாத்மா!",
                "sound_cue": "Crisp Veena harmonics and crackling fire sparks."
            },
            {
                "camera": "Transition to Indra's celestial abode: heroic King Pratardana stands before Indra and asks Indra to choose the single highest boon for humanity.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic scene in a radiant celestial-mountain hall. Heroic King Pratardana in warrior-sage attire bows before Lord Indra and asks him to choose whatever boon is most beneficial for all humankind (Manushyaya Hitam). Golden morning light, authentic Vedic aesthetic, no text, no subtitles, no borders.",
                "narration_en": "In the third chapter, the heroic King Pratardana reached the beloved abode of Indra through valor and austerity. When Indra offered him a boon, Pratardana gave the noblest reply: 'Tvam eva me वृणीष्व यं त्वं मनुष्याय हिततमं मन्यसे—O Indra, do you yourself choose for me that boon which you deem most beneficial for all humankind!' Indra answered: 'Know Me alone! This indeed I deem the supreme good for humanity—that one should realize the Conscious Self within!'",
                "narration_ta": "மூன்றாம் அத்தியாயத்தில், மாவீரனான மன்னன் பிரதர்தனன் தன் வீரத்தாலும் தவத்தாலும் இந்திர லோகத்தை அடைந்தான். இந்திரன் அவனை ஒரு வரம் கேட்கச் சொன்னபோது, பிரதர்தனன், 'இந்திரனே! மனித குலத்திற்கு எது மிகச் சிறந்த நன்மையோ (மனுஷ்யாய ஹிததமம்), அந்த வரத்தை நீரே எனக்காகத் தேர்ந்தெடுத்து அருளுங்கள்!' என்றான். மகிழ்ந்த இந்திரன், 'மனித குலத்திற்கு மிகச் சிறந்த நன்மை ஆத்ம ஞானமே! என்னையே அந்த ஆத்மாவாக அறிந்துகொள்!' என்று உபதேசித்தான்.",
                "subtitle_cue": "'மனித குலத்திற்கு எது மிகச் சிறந்த நன்மையோ அதையே வரமாகத் தாருங்கள்!' — பிரதர்தனனின் விண்ணப்பம்!",
                "sound_cue": "Heroic Shankha and Bansuri duet in Raga Bilahari."
            },
            {
                "camera": "Macro rotating shot of a carved wooden Vedic chariot wheel: the outer rim (Nemi) resting on the spokes (Ara), and the spokes converging into the central hub (Nabhi).",
                "veo_prompt": "16:9 8K 24fps photorealistic close-up of a beautifully carved ancient Indian wooden chariot wheel illuminated by golden sunlight. Camera focuses on the outer rim (Nemi) fixed upon the carved spokes (Ara), and all the spokes converging into the central bronze-bound hub (Nabhi), symbolizing Elements, Consciousness, and Prana, no text, no borders.",
                "narration_en": "Then Indra uttered the great Mahavakya of the Kaushitaki Upanishad: 'Prano'smi Prajnatma tam mam ayur amritam ity upassva—I am Prana, the Conscious Self! Meditate upon Me as Life and Immortality! For without Prajna (Consciousness), no thought can be known; and without Prana (Life), no faculty can act. Just as the outer rim of a chariot wheel is fixed upon the spokes, and the spokes are fixed upon the central hub—even so are all elements of the world fixed upon elements of Consciousness, and Consciousness itself is one with Immortal Prana!'",
                "narration_ta": "அப்போது இந்திரன் கௌஷீதகி உபநிடதத்தின் மகா வாக்கியத்தை முழங்கினான்: 'ப்ராணோऽஸ்மி ப்ரஜ்ஞாத்மா — நானே பேரறிவு வடிவான பிராணன்! என்னையே ஆயுளாகவும் அமிர்தமாகவும் தியானிப்பாயாக! பிராணனும் பிரக்ஞையும் ஒன்றை விட்டு ஒன்று பிரிவதில்லை. தேர்ச்சக்கரத்தின் வெளி விளிம்பு (நேமி) ஆரக்கால்களிலும், ஆரக்கால்கள் மையக் குமிழிலும் (நாபியிலும்) பொருந்தியிருப்பது போல், உலகப் பொருட்கள் அனைத்தும் பிரக்ஞையிலும், பிரக்ஞை அமிர்தப் பிராணனிலும் நிலைபெற்றுள்ளன!'",
                "subtitle_cue": "தேர்ச்சக்கரத்தின் விளிம்பும் ஆரக்கால்களும் குமிழில் நிலைத்திருப்பது போல் பிரக்ஞையில் நிலைத்த பிரபஞ்சம்!",
                "sound_cue": "Rhythmic revolving tala on Mridangam with soaring Veena melody."
            },
            {
                "camera": "Breathtaking cosmic vision from Chapter 1: the liberated soul crossing the Ageless River Vijara by the power of mind alone, shaking off good and evil karma.",
                "veo_prompt": "Epic 16:9 8K 24fps photorealistic spiritual vision of the Devayana path: a radiant liberated sage crosses the shimmering golden Ageless River (Vijara Nadi) effortlessly by thought alone, beneath the fragrant celestial Ilya tree, entering the vast luminous expanse of Satya-Brahman, no text, no subtitles, no borders.",
                "narration_en": "And what awaits the seeker on the supreme path of Devayana described in the first chapter? Passing through the realms of Agni, Vayu, Varuna, Indra, and Prajapati, the liberated soul reaches the Ageless River—Vijara Nadi—and crosses it by the mere resolve of the mind! There he shakes off both good and evil karma just as a charioteer looks down upon the revolving wheels without being touched by them, and declares before Brahma: 'Tvam atma'si yas tvam asi so'ham asmi—Thou art the Self of every being; what Thou art, That am I!'",
                "narration_ta": "முதல் அத்தியாயத்தில் கூறப்படும் தேவயானப் பாதையில் செல்லும் ஞானி, அக்னி, வாயு, வருணன், இந்திரன், பிரஜாபதி உலகங்களைக் கடந்து 'விஜரா' என்னும் மூப்பற்ற நதியை மனச் சங்கல்பத்தாலேயே கடக்கிறான்! தேரின் மேல் நிற்பவன் கீழே சுழலும் சக்கரங்களைப் பார்ப்பது போல், புண்ணிய-பாவ இருவினைகளையும் உதறித் தள்ளிவிட்டு பிரம்மனிடம் முழங்குகிறான்: 'த்வம் ஆத்மாஸி யஸ்த்வமஸி ஸோऽஹமஸ்மி — அனைத்து உயிர்களின் ஆத்மாவான நீ எதுவோ, அதுவே நான்!'",
                "subtitle_cue": "'விஜரா' நதியைக் கடந்து, 'நீ எதுவோ அதுவே நான் (யஸ்த்வமஸி ஸோஹமஸ்மி)' என உணரும் முக்தி நிலை!",
                "sound_cue": "Celestial Swarmandal, Shankha, and Rig Vedic chorus chanting 'Yas Tvam Asi So'ham Asmi'."
            },
            {
                "camera": "Wide sunlit closing shot of Kashi's sacred Ganga ghat as sages and kings meditate together on the one Conscious Self.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot of the ancient stone ghats of Kashi along the sunlit Ganga river. Rajarishi Ajatashatru, scholar Balaki, and Vedic disciples sit in serene meditation as morning sunlight sparkles on the water, zero modern elements, zero text, zero borders.",
                "narration_en": "Thus the Kaushitaki Upanishad unites king and scholar, breath and consciousness, action and stillness in the one Immortal Prajnatman. He who knows this becomes the Lord of all beings, untouched by sorrow forevermore!",
                "narration_ta": "இவ்வாறு கௌஷீதகி உபநிடதம் மன்னனையும் பண்டிதனையும், பிராணனையும் பேரறிவையும் ஒன்றாக இணைத்துப் 'பிரக்ஞாத்மா'வைப் போற்றுகிறது. இவ்வுண்மையை உணர்பவன் அனைத்து உயிர்களுக்கும் தலைவனாகி, பிறவித் துயர் நீங்கி அமரத்துவத்தில் நிலைபெறுகிறான்!",
                "subtitle_cue": "ப்ராணோऽஸ்மி ப்ரஜ்ஞாத்மா — பிராணனும் பேரறிவும் ஒன்றே! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!",
                "sound_cue": "Rig Veda Shanti Mantra 'Om Vang Me Manasi Pratishthita... Om Shantih Shantih Shantih'."
            }
        ]
    },
    {
        "story_id": "MUKHYA_22_MAITRAYANIYA_01",
        "muktika_number": 24,
        "upanishad_sanskrit": "मैत्रायण्युपनिषद् (मैत्री उपनिषद्)",
        "upanishad_iast": "Maitrāyaṇyupaniṣad (Maitrī Upaniṣad)",
        "upanishad_tamil": "மைத்ராயணீய உபநிடதம் (மைத்ரீ உபநிடதம்)",
        "upanishad_english": "Maitrayaniya (Maitri) Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Mukhya",
        "story_title_english": "King Brihadratha's Renunciation & Sage Shakayanya: The Frog in a Dry Well & The Mind as the Key to Liberation",
        "story_title_tamil": "மன்னன் பிருஹத்ரதனின் துறவும் சாகாயன்ய முனிவரும்: வற்றிய கிணற்றுத் தவளையும் மனமே முக்திக்குத் திறவுகோல் என்ற உபதேசமும்!",
        "characters": [
            "King Brihadratha of the Ikshvaku Dynasty (Who renounced his kingdom and stood 1,000 days gazing at the Sun in forest austerity)",
            "Maharishi Shakayanya (The knower of the Atman who burned like a smokeless fire and rescued Brihadratha)",
            "Maharishi Maitri (Teacher of the sixfold Yoga and the Sound-Brahman / Non-Sound Brahman)"
        ],
        "mahavakya_sanskrit": "मन एव मनुष्याणां कारणं बन्धमोक्षयोः । बन्धाय विषयासङ्गि मुक्त्यै निर्विषयं स्मृतम् ॥",
        "mahavakya_tamil_translit": "மன ஏவ மனுஷ்யாணாம் காரணம் பந்தமோக்ஷயோஃ | பந்தாய விஷயாஸங்கி முக்த்யை நிர்விஷயம் ஸ்ம்ருதம் ||",
        "mahavakya_meaning_english": "The Mind alone is the cause of both bondage and liberation for human beings! Attached to sense-objects it leads to bondage; freed from sense-objects, that very mind leads to Liberation!",
        "mahavakya_meaning_tamil": "மனிதர்களுக்குப் பந்தத்திற்கும் (கட்டுப்பாட்டிற்கும்) மோட்சத்திற்கும் (விடுதலைக்கும்) மனமே காரணம்! விஷயங்களில் பற்றுக் கொண்ட மனம் பந்தத்திற்கும், பற்றற்ற தூய மனம் முக்திக்கும் வழிகாட்டுகிறது!",
        "philosophical_theme": "Intense Vairagya (King Brihadratha's contemplation on the impermanence of bodies, oceans, mountains, and emperors); Shadanga Yoga (Six-limbed Yoga); and the Mind as the pivot of Bondage and Moksha.",
        "setting_specifics": "A sunlit Ikshvaku forest tapovanam where King Brihadratha stands with arms raised gazing at the Sun for a thousand days before Sage Shakayanya arrives.",
        "metaphor_highlight": "A Frog at the bottom of a dry well (Andodapana-stho Bhekah), an Iron Ball glowing in fire hammered into many shapes, the Potter's Wheel (Kulala-Chakra), and a Spider climbing up its thread into free space.",
        "scenes": [
            {
                "camera": "Dramatic tracking shot of King Brihadratha placing his royal crown on his son's head, then standing in a forest clearing with arms raised toward the blazing Sun.",
                "veo_prompt": "16:9 widescreen 8K 24fps photorealistic scene in an ancient Indian forest clearing. Former King Brihadratha, now dressed in simple bark-cloth and matted hair as a forest tapasvi, stands motionless with raised arms gazing toward the blazing golden morning sun after renouncing his throne. Deer and birds watch peacefully, no text, no borders.",
                "narration_en": "Standing at #24 in the Muktika canon and revered among both the Mukhya and Samanya Vedanta Upanishads, the Maitrayaniya Upanishad opens with the intense renunciation of King Brihadratha! Realizing that this physical body is transient and impure, he installed his son upon the throne, entered the forest, and performed supreme austerity—standing for a thousand days with arms raised, gazing into the blazing Sun!",
                "narration_ta": "முக்திக வரிசையில் 24-ஆவது இடத்திலும், முக்கிய மற்றும் சாமான்ய வேதாந்த உபநிடதங்கள் இரண்டிலும் போற்றப்படும் மைத்ராயணீய உபநிடதம், மன்னன் பிருஹத்ரதனின் தீவிர வைராக்கியத்தோடு தொடங்குகிறது! இவ்வுடல் நிலையற்றது என்பதை உணர்ந்த மன்னன், தன் மகனுக்கு முடிசூட்டிவிட்டு வனத்திற்குச் சென்று, கைகளை உயர்த்திச் சூரியனை நோக்கியவாறு ஆயிரம் நாட்கள் கடும் தவம் இயற்றினான்!",
                "subtitle_cue": "மைத்ராயணீய உபநிடதம்: அரசைத் துறந்து வனத்தில் ஆயிரம் நாட்கள் கடும் தவம் இயற்றிய மன்னன் பிருஹத்ரதன்!",
                "sound_cue": "Solemn Krishna Yajur Veda chant over a deep, austere Rudra Veena alapana."
            },
            {
                "camera": "Medium shot as Maharishi Shakayanya, glowing like a smokeless fire, approaches King Brihadratha and offers him a boon; Brihadratha weeps for liberation.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 medium shot in the forest clearing. Maharishi Shakayanya, radiating a serene golden aura like a smokeless fire (Adhumaka Agni), approaches King Brihadratha and touches his chest in blessing. The King falls at the sage's feet with folded hands, pleading for Self-knowledge, no text, no borders.",
                "narration_en": "At the end of the thousandth day, the knower of the Atman—Maharishi Shakayanya, shining like a smokeless fire—appeared before the King and said: 'Arise, O King! Choose a boon!' Brihadratha bowed at his feet and asked: 'O Bhagavan, I know not the Atman! Teach me!' When the Sage tested his resolve by saying how rare this inquiry is, the King burst forth with the great song of Vairagya: 'O Lord! In this body made of bones, skin, sinews, marrow, and flesh, what good is the enjoyment of desires?'",
                "narration_ta": "ஆயிரமாவது நாள் முடிவில், புகையற்ற நெருப்பைப் போல் (அதூமக அக்னி) ஒளிவீசும் ஆத்ம ஞானியான மகரிஷி சாகாயன்யர் தோன்றி, 'மன்னா, எழுந்திரு! வரம் கேள்!' என்றார். பிருஹத்ரதன் முனிவரின் திருவடிகளில் வீழ்ந்து, 'பகவானே! நான் ஆத்மாவை அறியாதவன்; எனக்கு ஆத்ம ஞானம் அருளுங்கள்!' என்று வேண்டினான். முனிவர் அவனது வைராக்கியத்தைச் சோதித்தபோது, மன்னன் தன் ஆழ்ந்த துறவு உள்ளத்தை வெளிப்படுத்தினான்: 'சுவாமி! எலும்பு, தோல், நரம்பு, சதை ஆகியவற்றால் ஆன இந்த அழியும் உடலில் சிற்றின்பங்களை நுகர்வதால் என்ன பயன்?'",
                "subtitle_cue": "'அழியும் இவ்வுடலில் சிற்றின்பங்களை நுகர்வதால் என்ன பயன்? எனக்கு ஆத்ம ஞானம் அருளுங்கள்!'",
                "sound_cue": "Passionate, soulful Violin solo expressing deep Vairagya and longing for truth."
            },
            {
                "camera": "Poignant visual metaphor: a helpless frog at the bottom of a dark, dry stone well looking up at a compassionate hand reaching down with light and water.",
                "veo_prompt": "16:9 8K 24fps photorealistic symbolic shot in an ancient stone courtyard: looking down into a deep, dry stone well where a small frog sits at the bottom looking upward toward a brilliant shaft of golden sunlight and a sage's compassionate hand lowering a copper pot of water. Cut to King Brihadratha kneeling before Sage Shakayanya, no text, no borders.",
                "narration_en": "Brihadratha cried out: 'Even the greatest oceans dry up! Mighty mountain peaks crumble! The Pole Star itself shifts from its place! Great emperors like Sudyumna, Bhuridyumna, and Bharata had to leave their vast kingdoms before the eyes of their families! Therefore, O Revered Master, in this whirlpool of Samsara I am like a frog trapped at the bottom of a dry well—Andodapana-stho Bhekah! You alone are my refuge; lift me out!'",
                "narration_ta": "பிருஹத்ரதன் கதறினான்: 'பகவானே! மகா சமுத்திரங்களும் வற்றிப் போகின்றன! உயர்ந்த சிகரங்களும் சரிந்து விழுகின்றன! துருவ நட்சத்திரமும் தன் நிலையிலிருந்து பெயர்கிறது! பாரதன் முதலான சக்கரவர்த்திகளும் தம் செல்வங்களை விட்டுப் பிரிந்தனர்! ஆகவே இந்தச் சம்சாரச் சுழலில், நீர் வற்றிய பாழும் கிணற்றுக்குள் விழுந்த தவளையைப் போல் (அந்தோதபானஸ்தோ பேகஃ) நான் தவிக்கிறேன்! நீங்களே எனக்குப் புகலிடம், என்னைக் கரையேற்றுங்கள்!'",
                "subtitle_cue": "'வற்றிய கிணற்றுக்குள் விழுந்த தவளை போல் சம்சாரத்தில் தவிக்கும் என்னைக் கரையேற்றுங்கள்!' — பிருஹத்ரதன்.",
                "sound_cue": "Echoing acoustic depth transitioning into a warm, rescuing Bansuri melody."
            },
            {
                "camera": "Close-up of a potter spinning his clay wheel (Kulala-Chakra) and a blacksmith hammering a glowing red-hot iron ball (Ayopinda), illustrating the Self and the empirical Jiva.",
                "veo_prompt": "Cinematic 16:9 8K 24fps photorealistic two-part scene in an ancient Indian village near the ashram: a traditional potter setting a clay wheel (Kulala-Chakra) spinning with his hand, and a smith hammering a glowing red-hot iron ball on an anvil where the fire itself remains completely unharmed by the hammer blows, no text, no borders.",
                "narration_en": "Pleased by his supreme dispassion, Sage Shakayanya revealed how the Pure Self sets the body in motion without being touched by it, just as a potter spins his wheel! And why does the soul seem bound as the Bhutatman? 'Just as a ball of iron placed in fire is hammered by the smith into many shapes, yet the fire itself is never hurt by the hammer—even so the three Gunas hammer only the psycho-physical mind, while the Immortal Witness within remains forever pure and untouched!'",
                "narration_ta": "மன்னனின் வைராக்கியத்தைக் கண்டு மகிழ்ந்த சாகாயன்ய முனிவர், குயவன் சக்கரத்தைச் சுழற்றுவது போல் ஆத்மா உடலோடு ஒட்டாமல் அதனை இயக்குவதை விளக்கினார்! மேலும், 'நெருப்பில் பழுக்கக் காய்ச்சிய இரும்புக் குண்டை சம்மட்டியால் அடிக்கும்போது இரும்பு பல வடிவங்களாக மாறினாலும், உள்ளேயுள்ள நெருப்பு சம்மட்டி அடியால் சிறிதும் பாதிக்கப்படுவதில்லை; அதுபோலவே முக்குணங்களின் விகாரங்கள் மனதை மட்டுமே தாக்குகின்றன, உள்ளேயுள்ள சாட்சி ஆத்மா என்றும் தூய்மையாகவே உள்ளது!' என்றார்.",
                "subtitle_cue": "காய்ச்சிய இரும்பை அடிக்கும்போது உள்ளேயுள்ள நெருப்பு பாதிக்கப்படாதது போல் என்றும் தூயதான ஆத்மா!",
                "sound_cue": "Rhythmic anvil chime and spinning wheel hum resolving into serene Veena harmonics."
            },
            {
                "camera": "Macro shot of a water drop trembling on a lotus leaf, transitioning to a quiet mind where all ripples of thought subside like fire when its fuel is spent.",
                "veo_prompt": "16:9 8K 24fps photorealistic macro-to-medium shot: a crystal water drop resting unattached on a green lotus leaf in golden morning light, transitioning to King Brihadratha meditating beside a dying sacred fire whose flames subside peacefully into glowing embers as its firewood is consumed (Nirindhana Vahni), no text, no borders.",
                "narration_en": "Then rings forth the most famous psychological verse in all of Vedanta: 'Mana eva manushyanam karanam bandha-mokshayoh! Bandhaya vishayasangi muktyai nirvishayam smritam! The Mind alone is the cause of both bondage and liberation for human beings! Attached to sense-objects it binds; freed from sense-objects, that very mind liberates! Just as fire without fuel subsides into its own source, so the mind, when its thought-waves cease, dissolves into the Supreme Self!'",
                "narration_ta": "இங்கே வேதாந்த உலகின் மிகப் புகழ்பெற்ற மகா வாக்கியம் ஒலிக்கிறது: 'மன ஏவ மனுஷ்யாணாம் காரணம் பந்தமோக்ஷயோஃ! பந்தாய விஷயாஸங்கி முக்த்யை நிர்விஷயம் ஸ்ம்ருதம்! மனிதர்களுக்குப் பந்தத்திற்கும் மோட்சத்திற்கும் மனமே காரணம்! உலகப் பொருட்களில் பற்றுக் கொண்ட மனம் பந்தத்திற்கும், பற்றற்ற தூய மனம் முக்திக்கும் காரணமாகிறது! விறகு தீர்ந்த நெருப்பு தன் பிறப்பிடத்திலேயே அடங்கிவிடுவது போல், எண்ணங்கள் அற்ற மனம் ஆத்மாவிலேயே ஒடுங்கிவிடுகிறது!'",
                "subtitle_cue": "மன ஏவ மனுஷ்யாணாம் காரணம் பந்தமோக்ஷயோஃ — மனிதர்களுக்குப் பந்தத்திற்கும் மோட்சத்திற்கும் மனமே காரணம்!",
                "sound_cue": "Resonant Vedic chant of 'Mana Eva Manushyanam' with crystal-clear temple bell chimes."
            },
            {
                "camera": "Upward tracking shot of a golden spider climbing up its own silken thread toward the sunlit canopy, symbolizing the Yogi ascending through Pranava via Sixfold Yoga.",
                "veo_prompt": "Photorealistic 8K 24fps 16:9 shot in the sunlit forest: a tiny golden spider climbs steadily upward along its single silken thread into the boundless golden sunlight above the trees, while below, King Brihadratha practices the six-limbed Yoga (Pranayama, Pratyahara, Dhyana, Dharana, Tarka, Samadhi), glowing with inner peace, no text, no borders.",
                "narration_en": "Through the Sixfold Yoga—Pranayama, Pratyahara, Dhyana, Dharana, Tarka, and Samadhi—the seeker ascends from the Sound-Brahman (Shabda-Brahman, OM) into the Soundless Supreme (Ashabda-Brahman)! 'Just as a spider climbs upward along its thread into free space, so the Yogi climbs upward along the thread of Pranava through the Sushumna into supreme independence!' That Bliss cannot be described in words to one who has not tasted it, just as one cannot describe the distinct sweetness of milk, ghee, and honey!",
                "narration_ta": "பிராணாயாமம், பிரத்யாகாரம், தியானம், தாரணை, தர்க்கம், சமாதி ஆகிய ஆறு அங்க யோகத்தினால் (ஷடங்க யோகம்), சாதகன் சப்த பிரம்மமான ஓங்காரத்தின் வழியே அசப்த பிரம்மமான பரம்பொருளை அடைகிறான்! 'சிலந்திப் பூச்சி தன் நூலின் வழியே மேலேறிச் சுதந்திர வெளியை அடைவது போல், யோகி பிரணவத்தின் வழியே மேலேறி மோட்ச சுதந்திரத்தை அடைகிறான்!' நெய், பால், தேன் ஆகியவற்றின் சுவை வேறுபாட்டை வார்த்தையால் விவரிக்க முடியாதது போல், அந்த ஆத்ம ஆனந்தத்தை அனுபவித்தவனே அறிவான்!",
                "subtitle_cue": "சிலந்தி தன் நூலின் வழியே மேலேறுவது போல் பிரணவ தியானத்தால் சுதந்திர வெளியை அடையும் யோகி!",
                "sound_cue": "Ascending Swarmandal and Bansuri notes dissolving into sublime, wordless stillness."
            },
            {
                "camera": "Wide golden-hour closing shot: King Brihadratha attains the Solar Portal of Brahman and bows in eternal gratitude to Maharishi Shakayanya.",
                "veo_prompt": "Wide 16:9 8K 24fps photorealistic closing shot of the Ikshvaku forest tapovanam at golden sunrise. Illumined King Brihadratha and Maharishi Shakayanya sit in radiant Samadhi facing the rising sun along the Marichipatha (Path of Light). Serene ancient Bharata atmosphere, zero modern elements, zero text, zero borders.",
                "narration_en": "Having purified his mind until it became as clear as the autumn sky, King Brihadratha bowed to Maharishi Shakayanya and entered the Marichipatha—the Solar Path of the Immortal Self, whence no soul ever returns to sorrow!",
                "narration_ta": "தன் மனதைச் சரத் காலத்து வானம் போல் நிர்மலமாக்கிய மன்னன் பிருஹத்ரதன், மகரிஷி சாகாயன்யரை வணங்கி, மீண்டும் பிறவித் துயருக்குத் திரும்பாத ஆத்ம ஜோதிப் பாதையில் (மரீசி பதத்தில்) நிலைபெற்றான்!",
                "subtitle_cue": "தூய மனதால் ஆத்ம ஜோதியில் கலந்த பிருஹத்ரதன்! ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!",
                "sound_cue": "Krishna Yajur Veda Shanti Mantra 'Om Saha Navavatu... Om Shantih Shantih Shantih'."
            }
        ]
    }
]


SAMANYA_SPECS = [
    {
        "story_id": "SAMANYA_01_KAIVALYA_12",
        "muktika_number": 12,
        "upanishad_sanskrit": "कैवल्योपनिषद्",
        "upanishad_iast": "Kaivalyopaniṣad",
        "upanishad_tamil": "கைவல்ய உபநிடதம்",
        "upanishad_english": "Kaivalya Upanishad",
        "veda": "Atharva Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Sage Ashvalayana & Lord Brahma: Churning the Heart-Lotus for Kaivalya Liberation",
        "story_title_tamil": "அஸ்வலாயன முனிவரும் பிரம்ம தேவரும்: இதயத் தாமரையில் உமையொருபாகனைத் தியானித்துக் கைவல்ய முக்தி அடைதல்!",
        "characters": [
            "Maharishi Ashvalayana (The devoted Vedic sage seeking the supreme science of Brahmavidya)",
            "Lord Pitamaha Brahma (The Creator and Grand-Preceptor of the Universe)",
            "Uma-Sahaya Paramesvara / Nilakantha (The Three-Eyed Supreme Lord shining in the heart-lotus)"
        ],
        "mahavakya_sanskrit": "श्रद्धाभक्तिध्यानयोगादवेहि । मय्येव सकलं जातं मयि सर्वं प्रतिष्ठितम् । मयि सर्वं लयं याति तद्ब्रह्माद्वयमस्म्यहम् ॥",
        "mahavakya_tamil_translit": "ஸ்ரத்தாபக்தி த்யானயோகாதவேஹி | மய்யேவ ஸகலம் ஜாதம் மயி ஸர்வம் ப்ரதிஷ்டிதம் | மயி ஸர்வம் லயம் யாதி தத்ப்ரஹ்மாத்வயமஸ்ம்யஹம் ||",
        "mahavakya_meaning_english": "Realize Through Faith, Devotion, and Meditation! In Me alone all is born, in Me all rests, and in Me all dissolves—I am that Non-Dual Brahman!",
        "mahavakya_meaning_tamil": "சிரத்தை, பக்தி, தியான யோகத்தால் அறிந்துகொள்! என்னிலேயே அனைத்தும் தோன்றின, என்னிலேயே நிலைபெற்றுள்ளன, என்னிலேயே ஒடுங்குகின்றன — அந்த இரண்டற்ற பிரம்மமே நான்!",
        "philosophical_theme": "Shraddha-Bhakti-Dhyana Yoga; meditating on Uma-Sahaya Nilakantha in the pure Dahara heart-lotus; rising to non-dual Kaivalya ('Aham eva avashishye').",
        "setting_specifics": "Lord Brahma's radiant lotus assembly in Satyaloka/Himalayan Tapovanam where Sage Ashvalayana sits before the sacred fire.",
        "metaphor_highlight": "Atman as lower Arani stick and Om as upper Arani stick burning the bonds of ignorance, and the Blind/Lame sleeper experiencing joy before returning to Turiya.",
        "s1_en": "In the sacred Kaivalya Upanishad (#12 in the Muktika canon, revered in both Shaiva and Samanya Vedanta), Maharishi Ashvalayana approached the Grand-Sire Lord Brahma with folded hands and prayed: 'Adhihi Bhagavan Brahmavidyam varishtham—O Lord, teach me that supreme Science of Brahman, ever cherished by the wise, by which a seeker swiftly sheds all sins and attains the Purusha higher than the highest!'",
        "s1_ta": "முக்திக வரிசையில் 12-ஆவது உபநிடதமாகத் திகழும் கைவல்ய உபநிடதத்தில், மகரிஷி அஸ்வலாயனர் பிதாமகரான பிரம்ம தேவரை அணுகிப் பணிந்து, 'பகவானே! மறைபொருளானதும், ஞானிகளால் போற்றப்படுவதுமான பரம பிரம்ம வித்தையை எனக்கு உபதேசியுங்கள்; அதனால் பாவங்கள் அனைத்தும் நீங்கிப் பராத்பர புருஷனை அடைய வழிகாட்டுங்கள்!' என்று வேண்டினார்.",
        "s2_en": "Pitamaha Brahma answered with the golden triad of spiritual practice: 'Shraddha-bhakti-dhyana-yogad avehi! Know That through unshakeable Faith (Shraddha), supreme Devotion (Bhakti), and deep Meditation (Dhyana)! Not by work, nor by progeny, nor by wealth, but by Renunciation (Tyaga) alone did the immortals attain liberation! Higher than heaven, seated in the cave of the heart, shines that Reality.'",
        "s2_ta": "பிரம்ம தேவர் ஆத்ம சாதனையின் மும்மணிகளை அருளினார்: 'ஸ்ரத்தா பக்தி த்யான யோகாதவேஹி! சிரத்தை, பக்தி மற்றும் தியான யோகத்தினால் அந்தப் பரம்பொருளை அறிந்துகொள்! கர்மத்தினாலோ, சந்ததியினாலோ, செல்வத்தினாலோ அன்று; தியாகத்தினால் (துறவினால்) மட்டுமே அமரத்துவம் கிட்டுகிறது! விண்ணுக்கும் மேலாய் இதயக் குகையில் ஒளிரும் சத்தியம் அதுவே.'",
        "s3_en": "How should the Yogi meditate? Brahma instructed: 'Seated in a solitary, pure place in Sukhasana, with neck, head, and body held erect, subduing all the senses and bowing in devotion to one's Guru, contemplate the spotless Lotus of the Heart—Virajam Padmam! At its luminous center, behold the Supreme Lord: Uma-Sahaya, Consort of Uma, Paramesvara, the Three-Eyed Nilakantha of boundless peace!'",
        "s3_ta": "யோகி எவ்வாறு தியானிக்க வேண்டும்? பிரம்ம தேவர் வழிகாட்டினார்: 'தூய தனிமையான இடத்தில் சுகாசனத்தில் அமர்ந்து, தலை, கழுத்து, உடலை நேராக நிறுத்தி, புலன்களை அடக்கித் தன் குருவை பக்தியுடன் வணங்கி, இதயத்தில் உள்ள மாசற்ற தாமரையைத் தியானிக்க வேண்டும்! அதன் நடுவே உமா தேவியுடன் கூடிய பரமேஸ்வரனை, முக்கண்ணனை, நீலகண்டனை, சாந்த சொரூபனைத் தரிசிக்க வேண்டும்!'",
        "s4_en": "Then Brahma gave the sacred Fire-Drill experiment of the soul: 'Atmanam aranim kritva pranavam chottararanim—Making your own mind-self the lower Arani wood, and the sacred syllable OM (Pranava) the upper friction-rod, churn them again and again through the discipline of Knowledge! That inner fire of Jnana will burn to ashes every rope of karmic bondage (Pasha)!'",
        "s4_ta": "அடுத்து ஆத்ம அரணிக் கடைதல் உவமையை பிரம்மன் அருளினார்: 'ஆத்மானம் அரணிம் க்ருத்வா ப்ரணவம் சோத்தராரணிம் — உன் ஆத்மாவையே கீழ் அரணிக் கட்டையாகவும், பிரணவமான ஓங்காரத்தையே மேல் அரணிக் கட்டையாகவும் கொண்டு, ஞானம் என்னும் கடைதலால் இடைவிடாது கடைவாயாக! அதிலிருந்து எழும் ஞான அக்னி பாசக் கட்டுகள் அனைத்தையும் எரித்துச் சாம்பலாக்கும்!'",
        "s5_en": "Showing how the One Consciousness appears as the Jiva in waking, dream, and deep sleep, Brahma uttered the thunderous Advaita realization: 'Mayyeva sakalam jatam, mayi sarvam pratishthitam, mayi sarvam layam yati, tad brahmadvayam asmy aham! In Me alone is everything born; in Me alone does everything rest; and into Me alone does everything dissolve—I am that Non-Dual Brahman!'",
        "s5_ta": "விழிப்பு, கனவு, ஆழ்ந்த உறக்கம் ஆகிய மூன்றிற்கும் சாட்சியாய் நின்ற முனிவர் அத்வைதப் பேருண்மையை முழங்கினார்: 'மய்யேவ ஸகலம் ஜாதம் மயி ஸர்வம் ப்ரதிஷ்டிதம் மயி ஸர்வம் லயம் யாதி தத்ப்ரஹ்மாத்வயமஸ்ம்யஹம்! என்னிலேயே அனைத்தும் தோன்றின; என்னிலேயே அனைத்தும் நிலைபெற்றுள்ளன; என்னிலேயே அனைத்தும் ஒடுங்குகின்றன — அந்த இரண்டற்ற அத்வைதப் பிரம்மமே நான்!'",
        "s6_en": "Entering direct Aparoksha Anubhuti, Sage Ashvalayana sang in ecstasy: 'I am smaller than the smallest atom, and yet I am the vast universe! I am the ancient Purusha, the Effulgent Lord! Having no hands or feet, my power is inconceivable; I see without eyes, I hear without ears; I know all, yet none can objectify Me—for I am forever Pure Consciousness, Chidananda!'",
        "s6_ta": "நேரடி அனுபூதியில் திளைத்த அஸ்வலாயனர் பாடினார்: 'நான் அணுவிற்கும் அணுவானவன், விசித்திரமான இப்பிரபஞ்சம் அனைத்தும் நானே! கைகளும் கால்களும் அற்றவன், ஆயினும் எல்லையற்ற சக்தி கொண்டவன்; கண்களின்றிப் பார்ப்பவன், செவிகளின்றி கேட்பவன்; அனைத்தையும் அறிபவன், எப்போதும் தூய சிதானந்தப் பேரறிவாய் விளங்குபவன் நானே!'",
        "s7_en": "Thus the Kaivalya Upanishad bestows its eternal Phala-Sruti: he who studies and meditates upon this supreme secret of Kaivalya burns away the sins of a thousand births and attains Kaivalya Moksha—aloneness in the Absolute—whence there is no return!",
        "s7_ta": "இவ்வாறு கைவல்ய உபநிடதம் வாழ்த்துகிறது: இந்தப் பரம ரகசியத்தை சிரத்தையோடு பயின்று தியானிப்பவன் எல்லாப் பாவங்களிலிருந்தும் விடுபட்டு, இரண்டற்ற 'கைவல்ய முக்தி'யை அடைந்து பிறவாப் பேரின்பத்தில் நிலைபெறுகிறான்!"
    },
    {
        "story_id": "SAMANYA_02_SUBALA_30",
        "muktika_number": 30,
        "upanishad_sanskrit": "सुबालोपनिषद्",
        "upanishad_iast": "Subālopaniṣad",
        "upanishad_tamil": "சுபால உபநிடதம்",
        "upanishad_english": "Subala Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Maharishi Raikva & Subala: The Cosmic Birth from Narayana & The Childlike State of Balya",
        "story_title_tamil": "ரைக்கவ முனிவரும் சுபாலரும்: நாராயண தத்துவமும் குழந்தையைப் போன்ற 'பால்ய' நிர்மல நிலையும்!",
        "characters": [
            "Maharishi Subala / Raikva (Questioning Lord Brahma on the origin and dissolution of the cosmos)",
            "Lord Pitamaha Brahma (Revealer of the Cosmic Purusha Narayana and the state of Balya)"
        ],
        "mahavakya_sanskrit": "असद्वा इदमग्र आसीत् । अजातमेकमजरमمرंमभयं शुभम् । बाल्येन तिष्ठासेत् निर्वेदं गच्छेत् ॥",
        "mahavakya_tamil_translit": "அஸத்வா இதமக்ர ஆஸீத் | அஜாதமேகமஜரமமரமபயம் ஸுபம் | பால்யேன திஷ்டாஸேத் நிர்வேதம் கச்சேத் ||",
        "mahavakya_meaning_english": "In the beginning this was unmanifest; unborn, one, ageless, immortal, fearless, and auspicious is Narayana! Let the wise sage abide in childlike innocence (Balya) beyond all duality!",
        "mahavakya_meaning_tamil": "ஆதியில் இது அவ்யக்தமாய் இருந்தது; பிறப்பற்றதும், மூப்பற்றதும், மரணமற்றதும், அபயமானதுமான நாராயணனே ஆத்மா! ஞானி குழந்தையைப் போன்ற கள்ளங்கபடமற்ற 'பால்ய' நிலையில் நிலைபெறுவானாக!",
        "philosophical_theme": "Cosmogenesis from the Unmanifest through Mahat and Ahankara to the Virat Purusha; Laya-Chintana (Reverse Dissolution of Earth into Water, Water into Fire, up to Niranjana Narayana); and the Childlike State (Balya).",
        "setting_specifics": "A serene Shukla Yajur Veda hermitage by a crystal mountain lake where Sage Raikva and Subala receive the sixteen-chapter teaching of Lord Brahma.",
        "metaphor_highlight": "Laya-Krama (Progressive dissolving of Earth in Water, Water in Fire, Fire in Air, Air in Space, Space in Indriya, Tanmatra, Bhutadi, Mahat, Avyakta, Akshara, and Tamas into Niranjana Deva) and the Innocent Child (Balya).",
        "s1_en": "In the Subala Upanishad (#30 in the Muktika canon, a cornerstone of Samanya Vedanta cited extensively by both Shankara and Ramanuja), Sage Raikva asked Lord Brahma: 'Kim tad asit—What existed in the very beginning before creation?' Brahma answered: 'Neither non-being nor manifest being existed first, nor both together; from the subtle Unmanifest arose Darkness (Tamas), from Tamas the Imperishable Akshara, from Akshara the Unmanifest Avyakta, and from Avyakta the Cosmic Mind Mahat!'",
        "s1_ta": "முக்திக வரிசையில் 30-ஆவது உபநிடதமான சுபால உபநிடதத்தில், ரைக்கவ முனிவர் பிரம்ம தேவரிடம், 'பகவானே! படைப்பின் ஆதியில் என்ன இருந்தது?' என்று கேட்டார். பிரம்மன் அருளினார்: 'ஆதியில் இது வெளிப்படாத அவ்யக்த நிலையில் இருந்தது; பரம்பொருளின் சங்கல்பத்தால் அக்ஷரமும், அவ்யக்தமும், மஹத் தத்துவமும், அகங்காரமும், பஞ்ச பூதங்களும் படிப்படியாகத் தோன்றின!'",
        "s2_en": "From that golden cosmic egg arose the Divine Purusha—Narayana—whose eyes became the Sun, whose breath became the Wind, whose mind became the Moon, and whose feet became the Earth! Dividing His own radiance, He entered into every living body as the Indwelling Ruler—Antaryamin—seated within the Dahara lotus of the heart alongside the ten vital nadis!",
        "s2_ta": "அந்தப் பொன்மயமான பிரம்மாண்டத்திலிருந்து திவ்ய புருஷனான நாராயணன் வெளிப்பட்டார்! அவரது கண்களிலிருந்து சூரியனும், பிராணனிலிருந்து வாயுவும், மனதிலிருந்து சந்திரனும் தோன்றின. அவரே ஒவ்வொரு உயிரின் இதயத் தாமரையிலும் அந்தர்யாமியாகப் புகுந்து, பத்து நாடிகளின் நடுவே ஆத்மாவாக வீற்றிருக்கிறார்!",
        "s3_en": "Sage Raikva asked: 'When the Yogi prepares to leave the body or enter Samadhi, how does this vast universe dissolve back into the One?' Brahma taught the grand Laya-Chintana—the Meditation of Reverse Dissolution! 'Earth dissolves into Water; Water dissolves into Fire; Fire dissolves into Air; Air dissolves into Space; Space dissolves into the Senses; Senses into Subtle Elements (Tanmatras); Tanmatras into Bhutadi (Ego); Bhutadi into Mahat; Mahat into Avyakta; and Avyakta into the Imperishable Akshara!'",
        "s3_ta": "'இப்பிரபஞ்சம் மீண்டும் எவ்வாறு பரம்பொருளில் ஒடுங்குகிறது?' என்று ரைக்கவர் கேட்டார். பிரம்மன் 'லய சிந்தனை' என்னும் ஒடுக்க முறையை உபதேசித்தார்: 'பிருதிவி நீரிலும், நீர் அக்னியிலும், அக்னி வாயுவிலும், வாயு ஆகாயத்திலும், ஆகாயம் இந்திரியங்களிலும், தன்மாத்திரைகளிலும், அகங்காரத்திலும், மஹத் தத்துவத்திலும், அவ்யக்தத்திலும், அக்ஷரத்திலும் படிப்படியாக ஒடுங்குகின்றன!'",
        "s4_en": "'And where does the Imperishable Akshara itself dissolve?' asked the Sage. Brahma replied: 'Akshara merges into causal Tamas, and that Tamas becomes one with the Supreme Lord (Ekibhavati Parasmim Deve); beyond that there is no dissolution, only the Spotless, Partless, Unborn Niranjana Narayana!'",
        "s4_ta": "'அந்த அக்ஷரமும் எங்கே ஒடுங்குகிறது?' என்ற கேள்விக்கு பிரம்மன் அருளினார்: 'அக்ஷரம் மூலப் பிரகிருதியில் ஒடுங்க, அது பரம தேவனான நாராயணனோடு ஒன்றாகிவிடுகிறது! அதற்கு மேல் தோற்றமோ ஒடுக்கமோ இல்லை; களங்கமற்ற, அவயவங்களற்ற, பிறப்பற்ற நிரஞ்சனப் பரம்பொருள் மட்டுமே எஞ்சியிருக்கிறது!'",
        "s5_en": "Then rings the supreme ethical and mystical instruction of the Subala Upanishad on how the liberated sage lives in the world: 'Balyena tishthaset—Let the knower of Brahman abide in Balya, the state of a pure, guileless child! Without pride of scholarship, without anger, without possession, truthful, forgiving, practicing non-injury and serene silence!'",
        "s5_ta": "அடுத்து பிரம்ம ஞானி உலகில் வாழும் 'பால்ய' நிலையை சுபால உபநிடதம் போதிக்கிறது: 'பால்யேன திஷ்டாஸேத் — ஞானி கள்ளங்கபடமற்ற குழந்தையைப் போன்ற தூய நிலையில் நிலைபெறுவானாக! கல்விச் செருக்கின்றி, கோபமின்றி, உடைமைகளின்றி, சத்தியம், பொறுமை, அஹிம்சை, புலனடக்கம் ஆகியவற்றோடு சாந்தமாய் வாழ்வானாக!'",
        "s6_en": "For such an illumined soul who has attained Nirveda—complete freedom from worldly craving—there is neither day nor night, neither east nor west, neither inside nor outside; his own Self shines as the spotless canopy of Consciousness!",
        "s6_ta": "இவ்வாறு உலகப் பற்றுகள் அனைத்தும் நீங்கிய அந்த மகாத்மாவிற்குப் பகலுமில்லை, இரவுமில்லை; உள்ளுமில்லை, புறமுமில்லை; அவனது ஆத்மாவே எங்கும் நிறைந்த நிரஞ்சன ஜோதியாக ஒளிர்கிறது!",
        "s7_en": "This sacred Subala Upanishad should be imparted only to a disciple whose senses are subdued, who has deep devotion to his Guru, and who seeks liberation alone. Whoever meditates upon this truth at the three sandhyas burns away all karmic bonds and merges into the Immortal Narayana!",
        "s7_ta": "புலன்களை அடக்கியவனும், குரு பக்தி கொண்டவனுமான நன்மாணாக்கனுக்கு மட்டுமே இந்தச் சுபால உபநிடத ரகசியத்தை உபதேசிக்க வேண்டும். இதனைத் தியானிப்பவன் கர்ம பந்தங்கள் அனைத்தும் நீங்கி அமரத்துவமான நாராயணப் பரம்பொருளில் கலக்கிறான்!"
    },
    {
        "story_id": "SAMANYA_03_MANTRIKA_32",
        "muktika_number": 32,
        "upanishad_sanskrit": "मन्त्रिकोपनिषद् (चूलिकोपनिषद्)",
        "upanishad_iast": "Mantrikopaniṣad",
        "upanishad_tamil": "மந்திரிகா உபநிடதம்",
        "upanishad_english": "Mantrika Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Eight-Petaled Lotus & The Swan of Eight Feet: Piercing the Curtain of Maya",
        "story_title_tamil": "எட்டு இதழ் தாமரையும் எட்டுக் கால் அன்னப் பறவையும்: மாயைத் திரையை விலக்கும் மந்திரிகா உபநிடதம்!",
        "characters": [
            "The Shukla Yajur Veda Acharya (Revealer of the Swan and the Curtain of Maya)",
            "Brahma-vadins / Disciples (Contemplating how the One Unborn Purusha drinks the waters of Prakriti without being stained)"
        ],
        "mahavakya_sanskrit": "अष्टपादं शुचिं हंसं त्रिसूत्रमणुमव्ययम् । पश्यन्त्येवमहात्मानो दिव्येन चक्षुषा सदा ॥",
        "mahavakya_tamil_translit": "அஷ்டபாதம் ஸுசிம் ஹம்ஸம் த்ரிஸூத்ரமணுமவ்யயம் | பஸ்யந்த்யேவமஹாத்மானோ திவ்யேன சக்ஷுஷா ஸதா ||",
        "mahavakya_meaning_english": "That pure Swan (Hamsa) of eight feet, three threads, subtle and imperishable—the great souls ever behold Him with the divine eye of wisdom!",
        "mahavakya_meaning_tamil": "எட்டுப் பாதங்களும், மூன்று இழைகளும் கொண்ட தூய, நுண்ணிய, அழியாத அந்த அன்னப் பறவையை (ஹம்ஸத்தை) மகாத்மாக்கள் ஞானக் கண்ணால் எப்போதும் தரிசிக்கின்றனர்!",
        "philosophical_theme": "The Mystic Hamsa (Swan of the Self) with Eight Feet and Three Threads (Sattva, Rajas, Tamas); Maya as a multi-colored curtain (Patam) rolled up when the Self is known.",
        "setting_specifics": "A sunlit lotus-lake Gurukulam where a radiant white Swan glides effortlessly across red, white, and dark lotus reflections.",
        "metaphor_highlight": "Ashtapada Hamsa (Eight-footed Swan with Three Threads), Red-White-Black Prakriti (Lohita-Shukla-Krishna), and the Magician rolling up his painted curtain of Maya.",
        "s1_en": "In the Mantrika Upanishad (#32 in the Muktika canon, belonging to the Shukla Yajur Veda), the Vedic sages gathered around their Acharya beside a sacred lotus lake and asked: 'Who is that effulgent Swan that glides across the waters of birth and death without ever wetting its wings?'",
        "s1_ta": "முக்திக வரிசையில் 32-ஆவது உபநிடதமாகத் திகழும் சுக்ல யஜுர் வேதத்தின் மந்திரிகா உபநிடதத்தில், தாமரைத் தடாகத்தின் கரையில் அமர்ந்திருந்த ஆச்சாரியரிடம் முனிவர்கள் கேட்டனர்: 'பிறப்பு-இறப்பு என்னும் நீரில் தன் சிறகுகள் நனையாமல் நீந்திச் செல்லும் அந்தத் தூய அன்னப் பறவை (ஹம்ஸம்) யார்?'",
        "s2_en": "The Acharya unveiled the riddle of the Cosmic Swan: 'Ashtapadam shuchim hamsam trisutram anum avyayam! Behold that pure Swan endowed with eight feet—the five elements, mind, intellect, and ego—and bound seemingly by three threads: Sattva, Rajas, and Tamas! Though subtler than an atom and imperishable, the deluded world sees Him not, though He shines in every eye!'",
        "s2_ta": "ஆச்சாரியர் அந்தப் புதிரை விடுவித்தார்: 'அஷ்டபாதம் ஸுசிம் ஹம்ஸம் த்ரிஸூத்ரமணுமவ்யயம்! எட்டுப் பாதங்களும் (எட்டு பிரகிருதிகளும்), சத்வம்-ரஜஸ்-தமஸ் என்னும் மூன்று நூல் இழைகளும் கொண்ட அந்தத் தூய ஹம்ஸத்தைக் காணுங்கள்! அணுவை விட நுண்ணியதாய் எல்லார் கண்களிலும் ஒளிர்ந்தாலும், அறியாமையால் உலகம் அதனைக் காண்பதில்லை!'",
        "s3_en": "Describing the Unborn Mother of the material world—Prakriti—the Upanishad speaks in vivid colors: 'She is one, unborn, painted in three hues: red (Rajas), white (Sattva), and black (Tamas), bringing forth countless offspring like herself! The ignorant Jiva clings to her in infatuation, while the wise Atman abandons her once her illusion is seen through!'",
        "s3_ta": "மூலப் பிரகிருதியை மூன்று வண்ணங்களில் உபநிடதம் வர்ணிக்கிறது: 'செம்மை (ரஜஸ்), வெண்மை (சத்வம்), கருமை (தமஸ்) ஆகிய மூன்று வண்ணங்கள் கொண்ட அந்தப் பிரகிருதி, தன்னைப் போன்றே எண்ணற்ற படைப்புகளை ஈன்றெடுக்கிறாள்! அज्ञானி அவளில் மயங்கிக் கிடக்கிறான்; ஞானியோ அவளது மாயையை உணர்ந்து விடுபடுகிறான்!'",
        "s4_en": "Then the Acharya gave the unforgettable metaphor of the Curtain of Maya: 'Just as a master artist unfolds a painted scroll or curtain displaying mountains, palaces, and battles, and then rolls that curtain back into himself so nothing else remains—even so the Supreme Lord unfolds this universe of Ignorance and rolls it away when Self-Knowledge dawns!'",
        "s4_ta": "அடுத்து மாயைத் திரை உவமையை ஆச்சாரியர் கூறினார்: 'ஓர் ஓவியன் பல காட்சிகள் வரையப்பட்ட திரைச்சீலையை விரித்துக் காட்டிவிட்டு, பின்னர் அதனைச் சுருட்டித் தன்னிடமே வைத்துக்கொள்வது போல், ஈசன் அறியாமைக் காட்சியை விரித்து, ஆத்ம ஞானம் உதயமானவுடன் அத்திரையைச் சுருட்டி மறைத்துவிடுகிறான்!'",
        "s5_en": "The ancient sages—Bhrigu, Angiras, and Atharvan—searched the Vedas, the Agnihotra, the Gayatri, and the sixty-four sciences, and proclaimed with one voice: 'All these point to that One Purusha alone! He is the thread upon which the worlds are strung; He is the Swan who drinks the Soma of immortality!'",
        "s5_ta": "பிருகு, அங்கிரஸ், அதர்வா முதலான மகரிஷிகள் வேதங்கள், அக்னிஹோத்ரம், காயத்ரி அனைத்திலும் தேடி, 'அனைத்தும் அந்த ஏக புருஷனையே சுட்டிக்காட்டுகின்றன! உலகங்களைத் தாங்கும் சூத்திரமும் அவனே, அமிர்த சோமத்தைப் பருகும் ஹம்ஸமும் அவனே!' என்று முழங்கினர்.",
        "s6_en": "Beholding that Eight-Footed Swan with the divine eye ofJnana, the disciples saw the three threads of the Gunas dissolve into pure golden light, leaving only the Immortal Witness!",
        "s6_ta": "ஞானக் கண்ணால் அந்த அன்னப் பறவையைத் தரிசித்த சீடர்கள், முக்குணக் கயிறுகள் அறுந்து விழ, இரண்டற்ற ஆத்ம ஜோதியைத் தம் இதயத்திலேயே நேரில் உணர்ந்தனர்!",
        "s7_en": "He who recites and contemplates this Mantrika Upanishad—the crest-jewel of the Brahmanas—becomes forever pure, crosses beyond the three Gunas, and merges into the Supreme Brahman!",
        "s7_ta": "வேதங்களின் சிகாமணியான இந்த மந்திரிகா உபநிடதத்தை ஓதித் தியானிப்பவன், முக்குண மாயையைக் கடந்து என்றும் தூய பிரம்ம சொரூபத்தில் நிலைபெறுகிறான்!"
    },
    {
        "story_id": "SAMANYA_04_SARVASARA_33",
        "muktika_number": 33,
        "upanishad_sanskrit": "सर्वसारोपनिषद्",
        "upanishad_iast": "Sarvasāropaniṣad",
        "upanishad_tamil": "சர்வசூர உபநிடதம் (சர்வசார உபநிடதம்)",
        "upanishad_english": "Sarvasara Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The 23 Ultimate Definitions of Vedanta: The Diamond Glossary of Self-Inquiry",
        "story_title_tamil": "வேதாந்தத்தின் 23 மூலக் கேள்விகளும் வைரத் தெளிவான விடைகளும்: சர்வசார உபநிடதம்!",
        "characters": [
            "Assembly of Mumukshu Disciples (Asking 23 fundamental questions of Vedantic terminology)",
            "The Advaita Kulapati Acharya (Defining Bandha, Moksha, Avidya, Turiya, Kutastha, Jiva, Ishvara, and Maya with razor precision)"
        ],
        "mahavakya_sanskrit": "सत्यं ज्ञानमनन्तमानन्दं ब्रह्म । अहं ब्रह्मास्मीति यावत्स्वानुभूतिर्न जायते तावन्माया ॥",
        "mahavakya_tamil_translit": "ஸத்யம் ஜ்ஞானமனந்தமானந்தம் ப்ரஹ்ம | அஹம் ப்ரஹ்மாஸ்மீதி யாவத் ஸ்வானுபூதிர்ந ஜாயதே தாவன்மாயா ||",
        "mahavakya_meaning_english": "Brahman is Existence, Consciousness, Infinity, and Bliss! Until the direct realization 'Aham Brahmasmi—I am Brahman' dawns, Maya appears to exist; once realized, Maya is non-existent!",
        "mahavakya_meaning_tamil": "சத்தியம், ஞானம், அனந்தம், ஆனந்தமே பிரம்மம்! 'அஹம் பிரம்மாஸ்மி — நானே பிரம்மம்' என்ற நேரடி அனுபூதி உதிக்கும் வரையில்தான் மாயை தோன்றும்; ஞானம் உதித்த கணமே மாயை மறைந்துவிடும்!",
        "philosophical_theme": "Systematic Viveka through exact definitions of the 23 core concepts of Advaita Vedanta (Bandha, Moksha, Avastha-traya, Panchakosha, Kutastha, Jiva, Ishvara, Adhyaropa-Apavada, Maya).",
        "setting_specifics": "A grand granite Vedanta Pathashala mandapam where the Acharya etches the 23 golden definitions on palm leaves while demonstrating with a crystal prism, a rope, and an anvil.",
        "metaphor_highlight": "Kutastha (The Immovable Blacksmith's Anvil), Rope mistaken for a Snake (Rajju-Sarpa), and Crystal reflecting a red hibiscus flower (Sphatika).",
        "s1_en": "In the Sarvasara Upanishad (#33 in the Muktika canon, the 'Essence of All Upanishads' from the Krishna Yajur Veda), earnest seekers gathered in the Vedanta mandapam and asked twenty-three foundational questions: 'Revered Master! What is Bondage (Bandha)? What is Liberation (Moksha)? What is Avidya? What are the four states, the five sheaths, the Kutastha, the Jiva, the Kshetrajna, the Sakshi, and Maya?'",
        "s1_ta": "முக்திக வரிசையில் 33-ஆவது உபநிடதமாகத் திகழும் கிருஷ்ண யஜுர் வேதத்தின் 'சர்வசார உபநிடதம்' (அனைத்து உபநிடதங்களின் சாரம்), இருபத்து மூன்று மூலக் கேள்விகளுடன் தொடங்குகிறது: 'குருதேவா! பந்தம் என்றால் என்ன? மோட்சம் என்றால் என்ன? அவித்தை, நான்கு அவஸ்தைகள், பஞ்ச கோசங்கள், கூடஸ்தன், ஜீவன், ஈஸ்வரன், சாக்ஷி, மாயை ஆகியவற்றின் துல்லியமான இலக்கணம் யாது?'",
        "s2_en": "The Acharya answered the first pair with crystal clarity: 'Superimposing the qualities of the non-Self—body, senses, and ego—upon the Pure Self is Bandha, Bondage! And the complete cessation of that false identification through knowledge of the Self is Moksha, Liberation! Just as a crystal appears red when a hibiscus flower is placed near it, the spotless Atman seems bound only through proximity to the mind!'",
        "s2_ta": "ஆச்சாரியர் முதல் கேள்விகளுக்குத் தெளிவான விடையளித்தார்: 'ஆத்மா அல்லாத உடல், புலன், அகங்காரங்களை ஆத்மாவின் மேல் ஏற்றிப் பார்ப்பதே பந்தம் (கட்டு)! அந்தக் கற்பனைத் தொடர்பு ஞானத்தால் அழிவதே மோட்சம் (விடுதலை)! செம்பருத்திப் பூவின் அருகில் வைக்கப்பட்ட பளிங்குக் கல் சிவப்பாகத் தோன்றுவது போல், மனதின் தொடர்பால் மட்டுமே ஆத்மா கட்டுண்டது போல் தோன்றுகிறது!'",
        "s3_en": "Examining the three states of Waking, Dream, and Deep Sleep, and the five sheaths from Food to Bliss, the Acharya asked: 'Who stands unchanged behind them all?' He pointed to an iron anvil: 'Just as a blacksmith's anvil—Kuta—remains unmoved while countless pieces of iron are hammered upon it, the Witness Consciousness that stands unmoved behind all changing thoughts is called KUTASTHA!'",
        "s3_ta": "விழிப்பு, கனவு, உறக்கம் ஆகிய மூன்று நிலைகளையும், ஐந்து கோசங்களையும் விளக்கிய குருதேவர், கொல்லனின் பட்டறையைச் சுட்டிக்காட்டினார்: 'இரும்புத் துண்டுகள் அடித்து வளைக்கப்படும்போது அடியில் உள்ள பட்டடைக் கல் (கூடம்) அசையாமல் நிற்பது போல், மாறும் எண்ணங்களுக்குப் பின்னால் மாறாமல் நிற்கும் சாட்சி சைதன்யமே கூடஸ்தன் எனப்படுகிறான்!'",
        "s4_en": "Then the Acharya demonstrated Adhyaropa (False Superimposition) and Apavada (De-superimposition) with a coiled rope in twilight: 'Mistaking this rope for a snake in dim light is Adhyaropa—the projection of the world upon Brahman! Bringing the lamp of inquiry and seeing that there was never a snake, only the rope, is Apavada!'",
        "s4_ta": "மங்கலான ஒளியில் கிடந்த கயிற்றைக் காட்டி 'அத்யாரோபம்' மற்றும் 'அபவாதம்' ஆகியவற்றை விளக்கினார்: 'மங்கலான வெளிச்சத்தில் கயிற்றைப் பாம்பென்று மயங்குவது போல், பிரம்மத்தின் மேல் உலகை ஏற்றிப் பார்ப்பது அத்யாரோபம்! ஞான விளக்கைக் கொண்டு பார்த்தவுடன் பாம்பு இல்லவே இல்லை, கயிறு மட்டுமே உள்ளது எனத் தெளிவதே அபவாதம்!'",
        "s5_en": "When Consciousness reflects in the individual mind-mirror, it is called Jiva; when it reflects in cosmic Maya, it is called Ishvara. Yet when both mirrors are transcended in the Mahavakya, what remains? 'Satyam Jnanam Anantam Anandam Brahma—Existence, Consciousness, Infinity, and Bliss is the One Brahman without a second!'",
        "s5_ta": "அந்தச் சைதன்யம் அந்தக்கரணத்தில் பிரதிபலிக்கும்போது 'ஜீவன்' என்றும், மாயையில் பிரதிபலிக்கும்போது 'ஈஸ்வரன்' என்றும் அழைக்கப்படுகிறது. உபாதிகளைக் கடந்து நோக்கும்போது, 'ஸத்யம் ஜ்ஞானமனந்தமானந்தம் ப்ரஹ்ம — சத்தியம், ஞானம், அனந்தம், ஆனந்தமே இரண்டற்ற பிரம்மம்!' என்ற சத்தியம் மட்டுமே ஒளிர்கிறது.",
        "s6_en": "Finally, the Acharya gave the most famous definition of Maya: 'Beginingless, indescribable as either real or unreal, vanishing the instant 'Aham Brahmasmi' is realized, like the horn of a hare—that is called Maya!'",
        "s6_ta": "இறுதியாக மாயையின் இலக்கணத்தைக் கூறினார்: 'ஆதியற்றதாய், உள்பொருள் என்றோ இல்பொருள் என்றோ கூற முடியாததாய், அஹம் பிரம்மாஸ்மி என்ற சுய அனுபூதி உதித்த கணமே முயற்கொம்பைப் போல் இல்லாமல் போவது எதுவோ, அதுவே மாயை!'",
        "s7_en": "Armed with these twenty-three diamond definitions of the Sarvasara Upanishad, the seeker is never again confused by words, and rests forever in the Kutastha-Brahman!",
        "s7_ta": "சர்வசார உபநிடதத்தின் இந்த இருபத்து மூன்று வைரத் தெளிவான விளக்கங்களை உணர்ந்த சாதகன், இனி ஒருபோதும் மயங்காமல் கூடஸ்த பிரம்மத்திலேயே நிலைபெறுகிறான்!"
    },
    {
        "story_id": "SAMANYA_05_NIRALAMBA_34",
        "muktika_number": 34,
        "upanishad_sanskrit": "निरालम्बोपनिषद्",
        "upanishad_iast": "Nirālambopaniṣad",
        "upanishad_tamil": "நிராலம்ப உபநிடதம்",
        "upanishad_english": "Niralamba Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Supportless Freedom: How the True Sannyasin Transcends Caste, Ego & Worldly Crutches",
        "story_title_tamil": "நிராலம்ப ஞானம்: குலம், கோத்திரம் மற்றும் அகங்காரக் கட்டுகளைக் கடந்த சுதந்திரப் பெருநிலை!",
        "characters": [
            "The Avadhuta / Niralamba Rishi (Revealer of the Supportless Absolute)",
            "Assembly of Seekers (Inquiring into the true meaning of Varna, Ashrama, Guru, Shishya, Heaven, Hell, and Liberation)"
        ],
        "mahavakya_sanskrit": "जातिर्न च कुलं तात गोत्रं दूरगतानि च । अहं ममेति सन्त्यज्य निरालम्बो भवेन्नरः ॥",
        "mahavakya_tamil_translit": "ஜாதிர்ந ச குலம் தாத கோத்ரம் தூரகதானி ச | அஹம் மமேதி ஸந்த்யஜ்ய நிராலம்போ பவேந்நரஃ ||",
        "mahavakya_meaning_english": "Neither caste nor family nor lineage belongs to the Self, O child! Abandoning 'I' and 'mine', let a person become Niralamba—resting without any external support in Brahman alone!",
        "mahavakya_meaning_tamil": "ஆத்மாவிற்குச் சாதியுமில்லை, குலமுமில்லை, கோத்திரமுமில்லை! 'நான்', 'எனது' என்ற அகங்கார-மமகாரங்களைத் துறந்து, எந்தப் புறப் பற்றுக்கோடும் அற்ற 'நிராலம்ப' பிரம்ம நிலையில் நிலைபெறுவாயாக!",
        "philosophical_theme": "Niralamba-Jnana (Supportless Absolute Consciousness); redefining Caste (Varna), Guru, Disciple, Pilgrimage (Tirtha), Heaven, and Hell purely in terms of Self-Knowledge vs. Ignorance.",
        "setting_specifics": "An open skyward Himalayan plateau where an Avadhuta sage sits beneath the boundless canopy of space without roof or walls.",
        "metaphor_highlight": "Niralamba Akasha (Boundless sky needing no pillar to hold it up), Skin/Blood/Flesh vs. Spotless Consciousness, and Crushing the Poison-Creeper of Worldly Craving.",
        "s1_en": "In the Niralamba Upanishad (#34 in the Muktika canon, belonging to the Shukla Yajur Veda), a circle of seekers bowed before a liberated Avadhuta sage seated under the open sky and asked: 'O Master! How do creatures come into bondage, and how do they attain Niralamba—supreme, supportless Liberation?'",
        "s1_ta": "முக்திக வரிசையில் 34-ஆவது உபநிடதமான சுக்ல யஜுர் வேதத்தின் நிராலம்ப உபநிடதத்தில், திறந்த வெளியில் அமர்ந்திருந்த அவதூத முனிவரை வணங்கிய சாதகர்கள், 'குருதேவா! ஜீவர்கள் எவ்வாறு பந்தத்தில் வீழ்கின்றனர்? எந்தப் புறப் பற்றுக்கோடும் அற்ற நிராலம்ப முக்தியை எவ்வாறு அடைகின்றனர்?' என்று கேட்டனர்.",
        "s2_en": "Invocation to Lord Skanda-Sanatkumara opened the teaching: 'What is Brahman? It is the Infinite Consciousness free from all gunas and stains! And who are Brahma, Vishnu, Rudra, Indra, and Yama? That very Consciousness acting through cosmic functions! Outside of the One Atman, there is no separate world at all!'",
        "s2_ta": "குமாரக் கடவுளான சனத்குமாரரைப் போற்றி உபதேசம் தொடங்கியது: 'பிரம்மம் என்பது யாது? முக்குணங்களும் களங்கமும் அற்ற எல்லையற்ற சைதன்யமே பிரம்மம்! பிரம்மா, விஷ்ணு, ருத்ரன், இந்திரன், எமன் அனைவரும் அந்த ஒரே சைதன்யத்தின் செயல்பாடுகளே! ஆத்மாவைத் தவிர வேறொரு உலகம் தனியாக இல்லவே இல்லை!'",
        "s3_en": "Then the Upanishad shattered false social pride with fearless clarity: 'What is Jati—caste? Caste does not belong to the skin, nor to the blood, nor to the flesh, nor to the bones, nor to the spotless Atman! It is merely a convention built on outward habits! Before the Self, neither caste nor clan nor lineage has any reality!'",
        "s3_ta": "தொடர்ந்து சாதி மற்றும் குலப் பெருமைகளின் மாயையை உபநிடதம் உடைத்தெறிந்தது: 'ஜாதி என்பது யாது? அது தோலுக்கும் கிடையாது, இரத்தத்திற்கும் கிடையாது, தசைக்கும் எலும்புக்கும் கிடையாது; நிர்மலமான ஆத்மாவிற்கோ சாதியே கிடையாது! அது வெறும் புற வழக்கமே! ஆத்ம பார்வையில் சாதி, குலம், கோத்திரம் அனைத்தும் பொருளற்றவை!'",
        "s4_en": "'Who then is the true Guru, and who is the true Shishya?' asked the seekers. The Sage replied: 'The Guru is he who reveals the truth that the empirical ego is unreal and the Supreme Brahman alone is real! And the Shishya is that pure Consciousness which remains when all multiplicity of the universe has been negated through wisdom!'",
        "s4_ta": "'உண்மையான குரு யார்? உண்மையான சீடன் யார்?' என்ற கேள்விக்கு முனிவர் அருளினார்: 'ஜீவ பாவம் பொய், பிரம்மமே சத்தியம் என்ற பேருண்மையை உணர்த்தும் ஆச்சாரியரே குரு! பிரபஞ்சப் பன்முக மாயை நீங்கிய பின் எஞ்சி நிற்கும் தூய பிரம்ம அறிவே சீடன்!'",
        "s5_en": "'And what are Svarga (Heaven) and Naraka (Hell)?' 'Abiding in the bliss of the Self—Sat-Chit-Ananda—is the true Heaven! Wandering in the dark alleys of selfish worldly cravings (Asat-Samsara) is Hell! And who is the true Sannyasin? He who has abandoned the two words 'I' and 'mine' (Aham-Mama) and rests without any external crutch—Niralamba!'",
        "s5_ta": "'சுவர்க்கம் எது? நரகம் எது?' 'சச்சிதானந்த பிரம்மத்தில் நிலைபெறுவதே உண்மையான சுவர்க்கம்! நிலையற்ற உலக ஆசைகளில் உழல்வதே நரகம்! உண்மையான சந்நியாசி யார்? நான், எனது என்ற இரு சொற்களையும் துறந்து, எந்தப் பற்றுக்கோடும் இன்றி நிராலம்பமாய் நிற்பவனே சந்நியாசி!'",
        "s6_en": "Like the boundless sky that needs no pillar to hold it up, the Niralamba Yogi beholds his own Consciousness pervading every atom, free from fear, doubt, and sorrow.",
        "s6_ta": "தன்னைத் தாங்க எந்தத் தூணும் தேவைப்படாத எல்லையற்ற ஆகாயத்தைப் போல், நிராலம்ப யோகி எங்கும் நிறைந்த சுய ஒளியாகத் தன்னை உணர்ந்து அச்சமும் துயரமும் இன்றித் திகழ்கிறான்.",
        "s7_en": "Whoever contemplates this Niralamba Upanishad becomes purer than fire, freer than the wind, and never again returns to the cycle of birth and death!",
        "s7_ta": "இந்த நிராலம்ப உபநிடதத்தைத் தியானிப்பவன் நெருப்பை விடத் தூய்மையானவனாகவும், காற்றை விடச் சுதந்திரமானவனாகவும் ஆகி, பிறவிச் சுழலில் மீண்டும் சிக்காமல் முக்தி அடைகிறான்!"
    },
    {
        "story_id": "SAMANYA_06_SHUKARAHASYA_35",
        "muktika_number": 35,
        "upanishad_sanskrit": "शुकरहस्योपनिषद् (रहस्योपनिषद्)",
        "upanishad_iast": "Śukarahasyopaniṣad",
        "upanishad_tamil": "சுகரகசிய உபநிடதம்",
        "upanishad_english": "Shukarahasya Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Vyasa, Young Shuka & Lord Shiva: The Secret Initiation into the Four Mahavakyas",
        "story_title_tamil": "வியாசர், சுக பிரம்மரிஷி மற்றும் சிவபெருமான்: நான்கு மகா வாக்கியங்களின் ரகசிய உபதேசம்!",
        "characters": [
            "Maharishi Krishna Dvaipayana Vyasa (Who prayed to Lord Shiva for his son Shuka's direct illumination)",
            "Brahmarishi Shuka (The radiant young ascetic who received the six-limbed Rahasya Upanishad)",
            "Lord सदाशिव / Mahesvara (Who appeared before Vyasa and Shuka to expound the Four Mahavakyas)"
        ],
        "mahavakya_sanskrit": "प्रज्ञानं ब्रह्म । अहं ब्रह्मास्मि । तत्त्वमसि । अयमात्मा ब्रह्म । शुको முक्तो बभूव ॥",
        "mahavakya_tamil_translit": "ப்ரஜ்ஞானம் ப்ரஹ்ம | அஹம் ப்ரஹ்மாஸ்மி | தத்த்வமஸி | அயமாத்மா ப்ரஹ்ம | ஸுகோ முக்தோ பபூவ ||",
        "mahavakya_meaning_english": "Prajnanam Brahma, Aham Brahmasmi, Tat Tvam Asi, Ayamatma Brahma—hearing these four Mahavakyas, young Shuka abided in Nirvikalpa Samadhi and became eternally free!",
        "mahavakya_meaning_tamil": "ப்ரஜ்ஞானம் பிரம்மம், அஹம் பிரம்மாஸ்மி, தத் த்வம் அஸி, அயமாத்மா பிரம்மம் ஆகிய நான்கு மகா வாக்கியங்களின் பொருளை உணர்ந்த சுக முனிவர் நிர்விகல்ப சமாதியில் ஆழ்ந்து ஜீவன்முக்தரானார்!",
        "philosophical_theme": "The Canonical Synthesis of the Four Great Mahavakyas across the Four Vedas (Prajnanam Brahma, Aham Brahmasmi, Tat Tvam Asi, Ayamatma Brahma) and the Six-Word Pranava Rahasya.",
        "setting_specifics": "Badarikashrama in the snow-clad Himalayas where Maharishi Vyasa and young Shuka stand before Lord Sadashiva.",
        "metaphor_highlight": "A drop of water merging into the boundless ocean, and the Four Mahavakyas as the four pillars of the temple of Liberation.",
        "s1_en": "In the Shukarahasya Upanishad (#35 in the Muktika canon, from the Krishna Yajur Veda), the sages asked: 'How did young Shuka—son of Maharishi Vyasa—attain supreme Brahmavidya?' Long ago in the Himalayas, Maharishi Vyasa performed intense Tapas to Lord Sadashiva and prayed: 'O Mahesvara! Pray impart directly to my son Shuka that secret wisdom by which he may attain instantaneous liberation!'",
        "s1_ta": "முக்திக வரிசையில் 35-ஆவது உபநிடதமான சுகரகசிய உபநிடதத்தில், வியாச முனிவரின் புதல்வரான சுகர் எவ்வாறு பிரம்ம ஞானம் பெற்றார் என்ற வரலாறு கூறப்படுகிறது! இமயமலையில் மகரிஷி வியாசர் சிவபெருமானை நோக்கித் தவம் இயற்றி, 'மகேஸ்வரா! என் புதல்வன் சுகனுக்கு உடனடியாக முக்தி அளிக்கும் பரம ரகசிய வித்தையை நீரே நேரில் உபதேசித்தருள வேண்டும்!' என்று வேண்டினார்.",
        "s2_en": "Appearing in golden-white effulgence, Lord Shiva initiated young Shuka into the Sixfold Rahasya of Pranava—Om Namah Shivaya / Om Namo Narayanaya—and declared: 'O Shuka! The entire wisdom of the four Vedas is distilled into Four Great Sentences—the Chatur-Mahavakyas! Hear their inner meaning with a one-pointed mind!'",
        "s2_ta": "வெள்ளியங்கிரிப் பேரொளியாய் நேரில் தோன்றிய சிவபெருமான், இளம் சுகருக்குப் பிரணவத்தின் ஆறங்க ரகசியத்தை அருளி, 'சுகா! நான்கு வேதங்களின் ஒட்டுமொத்த சாரமும் நான்கு மகா வாக்கியங்களில் அடங்கியுள்ளது; அவற்றின் உட்பொருளை ஒருமுகப்பட்ட மனதுடன் கேள்!' என்று உபதேசிக்கத் தொடங்கினார்.",
        "s3_en": "First, Lord Shiva expounded the Rig Veda Mahavakya from the Aitareya Upanishad: 'PRAJNANAM BRAHMA—Consciousness is Brahman!' That pure awareness by which one sees, hears, smells, speaks, and knows is not a limited product of the body; stripped of mental conditioning, that Witness-Consciousness itself is the Infinite Brahman! Second, the Yajur Veda Mahavakya: 'AHAM BRAHMASMI—I am Brahman!'",
        "s3_ta": "முதலில் ரிக் வேதத்தின் மகா வாக்கியத்தை சிவபெருமான் விளக்கினார்: 'ப்ரஜ்ஞானம் பிரம்மம் — தூய பேரறிவே பிரம்மம்!' எதனால் நாம் காண்கிறோமோ, கேட்கிறோமோ, அறிகிறோமோ அந்தச் சாக்ஷி அறிவே பிரம்மம்! இரண்டாவதாக யஜுர் வேத மகா வாக்கியமான 'அஹம் பிரம்மாஸ்மி — நானே பூரணப் பிரம்மம்!' என்பதன் பொருளை அருளினார்.",
        "s4_en": "Third, the Sama Veda Mahavakya: 'TAT TVAM ASI—Thou Art That!' By discarding the apparent difference between the Cosmic Ruler (Tat) and the individual soul (Tvam)—just as one recognizes that 'This is that very Devadatta I saw yesterday' (Soyam Devadattah)—one realizes their indivisible identity! And fourth, the Atharva Veda Mahavakya: 'AYAM ATMA BRAHMA—This very Self shining directly within the heart is Brahman!'",
        "s4_ta": "மூன்றாவதாக சாம வேத மகா வாக்கியமான 'தத் த்வம் அஸி — அதுவே நீ!' என்பதை 'நேற்று பார்த்த தேவதத்தனே இவன் (ஸோऽயம் தேவதத்தஃ)' என்ற ஜஹத்-அஜஹத் லக்ஷணையால் விளக்கினார்! நான்காவதாக அதர்வண வேத மகா வாக்கியமான 'அயமாத்மா பிரம்மம் — இதயத்தில் நேரில் ஒளிரும் இந்த ஆத்மாவே பிரம்மம்!' என்று முத்தாய்ப்பு வைத்தார்.",
        "s5_en": "Hearing these four Mahavakyas directly from the lips of Mahesvara, young Shuka's mind dissolved in Nirvikalpa Samadhi! Like a drop of water falling into the shoreless ocean, or like space inside a jar merging with cosmic space when the jar is broken, Shuka realized: 'I am that spotless, non-dual Brahman!'",
        "s5_ta": "சிவபெருமானின் திருவாக்கால் இந்த நான்கு மகா வாக்கியங்களையும் கேட்ட மாத்திரத்தில், இளம் சுகர் நிர்விகல்ப சமாதியில் ஆழ்ந்தார்! கடலில் விழுந்த நீர்த்துளி கடலோடு ஒன்றாவது போலவும், குடம் உடைந்தவுடன் குட ஆகாயம் மகா ஆகாயத்தோடு கலப்பது போலவும், 'நானே அந்த இரண்டற்ற பிரம்மம்!' என்று நேரில் உணர்ந்தார்.",
        "s6_en": "Rising from Samadhi as a Jivanmukta—radiant, fearless, and free from every attachment—young Shuka bowed to his father Vyasa and to Lord Shiva, and walked forth into the vast universe, seeing the entire creation as his own Self!",
        "s6_ta": "சமாதியிலிருந்து எழுந்த சுக பிரம்மரிஷி, அனைத்துப் பற்றுகளிலிருந்தும் விடுபட்ட ஜீவன்முக்தராய் ஒளிவீசினார்; தந்தை வியாசரையும் சிவபெருமானையும் வணங்கி, பிரபஞ்சம் முழுவதையும் தன் ஆத்மாவாகவே தரிசித்தபடி புறப்பட்டார்!",
        "s7_en": "Seeing young Shuka walk away in supreme freedom, Maharishi Vyasa followed calling 'O my son!', and the very trees and mountains echoed back on Shuka's behalf, for Shuka had become the Soul of All! Whoever meditates on this Shukarahasya Upanishad attains that same liberation of Shuka!",
        "s7_ta": "சுகர் சுதந்திரமாய்ச் செல்வதைக் கண்டு தந்தை வியாசர் 'மகனே!' என்று அழைத்தபோது, சுகர் எல்லா உயிர்களின் ஆத்மாவாக ஆகிவிட்டதால் காட்டு மரங்களே எதிரொலித்துப் பதிலளித்தன! இந்தச் சுகரகசிய உபநிடதத்தைத் தியானிப்பவர் சுகர் அடைந்த அதே பரம முக்தியை அடைகிறார்!"
    },
    {
        "story_id": "SAMANYA_07_VAJRASUCHIKA_36",
        "muktika_number": 36,
        "upanishad_sanskrit": "वज्रसूचिकोपनिषद्",
        "upanishad_iast": "Vajrasūcikopaniṣad",
        "upanishad_tamil": "வஜ்ரசூசிகா உபநிடதம்",
        "upanishad_english": "Vajrasuchika Upanishad",
        "veda": "Sama Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Diamond Needle of Inquiry: Who Is a True Brahmana? Not by Birth, Body, or Wealth, Only by Self-Realization!",
        "story_title_tamil": "வஜ்ர ஊசியின் விசாரணை: உண்மையான பிராமணன் யார்? பிறப்பாலோ உடலாலோ அன்று, பிரம்ம ஞானத்தாலேயே!",
        "characters": [
            "The Sama Veda Acharya (Wielding the Vajrasuchi—the Diamond Needle that pierces ignorance)",
            "Rishyasringa (Son of a deer), Kaushika/Vishvamitra (Son of Kusha/Kshatriya), Jambuka (Son of a jackal), Valmiki (From an anthill), Vyasa (Son of a fisherwoman), Gautama (From a hare's back), Vasishtha (Born of Urvashi), Agastya (Born from a pitcher)",
            "Assembly of Vedic Scholars (Learning that direct realization of the Non-Dual Atman alone makes a Brahmana)"
        ],
        "mahavakya_sanskrit": "तर्हि को वा नाम ब्राह्मणो नाम । यः कश्चिदात्मानमद्वितीयं जातिगुणक्रियाहीनं... परमात्मन्येव सदावस्थितः स एव ब्राह्मण इति ॥",
        "mahavakya_tamil_translit": "தர்ஹி கோ வா நாம ப்ராஹ்மணோ நாம | யஃ கஸ்சிதாத்மானமத்விதீயம் ஜாதிகுணக்ரியாஹீனம்... பரமாத்மன்யேவ ஸதாவஸ்திதஃ ஸ ஏவ ப்ராஹ்மண இதி ||",
        "mahavakya_meaning_english": "Who then is truly a Brahmana? Whoever directly realizes the Non-Dual Self—free from caste, gunas, and actions—and abides free from desire, delusion, pride, and malice, he alone is a Brahmana!",
        "mahavakya_meaning_tamil": "அப்படியானால் உண்மையான பிராமணன் யார்? சாதி, குணம், செயல் அற்ற இரண்டற்ற ஆத்மாவை நேரில் உணர்ந்து, காமம், குரோதம், அகங்காரம், பொறாமை நீங்கிப் பரமாத்மாவில் நிலைபெற்ற எவரோ அவரே பிராமணன்!",
        "philosophical_theme": "Refuting the claim that Brahminhood comes from Jiva, Body, Birth (Jati), Scholarship (Jnana), Action (Karma), or Charity (Dharma); proving through the lineage of great Rishis that direct Brahmajnana alone makes a Brahmana.",
        "setting_specifics": "A grand Sama Veda assembly hall where the Acharya holds up a diamond-tipped stylus (Vajrasuchi) and systematically examines every false claim.",
        "metaphor_highlight": "Vajrasuchi (The Diamond Needle that pierces the pride of ignorant scholars and serves as the ornament of the wise), and the Eight Great Rishis born outside conventional Brahmin parentage.",
        "s1_en": "In the celebrated Vajrasuchika Upanishad (#36 in the Muktika canon, from the Sama Veda, commented upon by Adi Shankaracharya), the Acharya held aloft the Vajrasuchi—the Diamond Needle of Discrimination that pierces the ignorance of the proud and adorns the wise—and asked the assembly: 'Of the four Varnas, the scriptures call the Brahmana foremost; tell me, WHO or WHAT is truly the Brahmana?'",
        "s1_ta": "முக்திக வரிசையில் 36-ஆவது உபநிடதமாகத் திகழ்வதும், ஆதிசங்கரரால் உரை எழுதப்பட்டதுமான சாம வேதத்தின் 'வஜ்ரசூசிகா உபநிடதத்தில்', அறியாமையைத் துளைக்கும் வைர ஊசி போன்ற விசாரணையை ஆச்சாரியர் தொடங்கினார்: 'நான்கு வர்ணங்களில் பிராமணன் முதன்மையானவன் என்று சாஸ்திரங்கள் கூறுகின்றனவே; உண்மையில் பிராமணன் என்பது யார்? எது?'",
        "s2_en": "First the Acharya examined the Jiva (Soul) and the Deha (Body): 'Is the Jiva the Brahmana? No! For the same one Jiva takes countless bodies across past and future births—as gods, humans, and animals—while remaining unchanged in nature! Is the physical Body the Brahmana? No! For every human body—from emperor to outcaste—is made of the same five elements, undergoes childhood, old age, and death, and shows no difference in flesh or bone! Besides, if the body were the Brahmana, then cremating a father's body after death would incur the sin of Brahmahatya!'",
        "s2_ta": "முதலில் ஜீவனையும் உடலையும் ஆராய்ந்தார் ஆச்சாரியர்: 'ஜீவன்தான் பிராமணனா? இல்லை! ஏனெனில் அதே ஜீவன் பல பிறவிகளில் வெவ்வேறு உடல்களை எடுத்தாலும் ஜீவ சொரூபம் ஒன்றே! அப்படியானால் உடல்தான் பிராமணனா? இல்லை! எல்லா மனிதர்களின் உடலும் பஞ்ச பூதங்களால் ஆனதே; மூப்பு, மரணம், தசை, இரத்தம் அனைவருக்கும் பொதுவானதே! மேலும் உடலே பிராமணன் என்றால், இறந்த தந்தையின் உடலைத் தகனம் செய்யும் மகனுக்குப் பிரம்மஹத்தி தோஷம் ஏற்படுமே!'",
        "s3_en": "Then came the decisive refutation of Birth (Jati): 'Does mere birth—Jati—make one a Brahmana? No! Look at our own most revered Maharishis! Rishyasringa was born of a doe; Kaushika (Vishvamitra) of a Kshatriya lineage; Jambuka of a jackal; Valmiki from an anthill; Vyasa from a fisherman's daughter (Satyavati); Gautama from a hare's back; Vasishtha from the celestial nymph Urvashi; and Agastya from a clay pitcher! Yet all of them were supreme Brahma-Rishis without traditional birth!'",
        "s3_ta": "அடுத்து 'பிறப்பினால் (ஜாதியினால்) ஒருவன் பிராமணன் ஆகிறானா?' என்ற வாதத்தை ஆணித்தரமாக மறுத்தார்: 'பிறப்பினால் மட்டும் ஒருவன் பிராமணன் ஆவதில்லை! நம் மகரிஷிகளின் வரலாற்றைப் பாருங்கள்: ரிஷ்யசிருங்கர் மானின் வயிற்றிலும், கௌசிகர் (விஸ்வாமித்திரர்) க்ஷத்திரிய குலத்திலும், ஜம்புகர் நரியிடத்தும், வால்மீகி புற்றிலிருந்தும், வியாசர் மீனவப் பெண் சத்யவதியிடத்தும், வசிஷ்டர் ஊர்வசியிடத்தும், அகத்தியர் கலசத்திலிருந்தும் தோன்றினர்! ஆயினும் இவர்கள் அனைவரும் மாபெரும் பிரம்மரிஷிகளாகப் போற்றப்பட்டனரே!'",
        "s4_en": "Next the Acharya examined Scholarship, Ritual Action, and Charity: 'Does mere book-learning make a Brahmana? No! For many Kshatriyas and others are also masters of the Vedas and sciences! Does performing Karma make a Brahmana? No, for all beings perform actions driven by past impressions! Does giving gold in charity make a Brahmana? No, for many noble kings and householders of all backgrounds give away heaps of gold!'",
        "s4_ta": "தொடர்ந்து கல்வி, கர்மம், தர்மம் ஆகியவற்றையும் ஆராய்ந்தார்: 'ஏட்டுக் கல்வியால் மட்டும் ஒருவன் பிராமணன் ஆவானா? இல்லை! க்ஷத்திரியர் முதலான பலரும் வேத சாஸ்திரங்களை நன்கு அறிந்தவர்களாக உள்ளனர்! கர்மம் செய்வதாலோ, பொன்னும் பொருளும் தானம் செய்வதாலோ மட்டும் பிராமணன் ஆக முடியாது; ஏனெனில் எல்லா வகுப்பினரும் நற்செயல்களையும் தான தர்மங்களையும் செய்கின்றனர்!'",
        "s5_en": "Then rang forth the Diamond Siddhanta of the Vajrasuchika Upanishad: 'Tarhi ko va nama Brahmano nama? Who then is truly a Brahmana? Yah kashchid atmanam advitiyam... sakshad aparokshataya பश्यति! Whoever—regardless of birth—directly and immediately realizes the Non-Dual Atman, which is free from caste, gunas, and actions, free from the six infirmities of hunger, thirst, grief, delusion, old age, and death, and who is Sat-Chit-Ananda, the Indwelling Witness of all!'",
        "s5_ta": "அப்போது வஜ்ரசூசிகா உபநிடதத்தின் வைரத் தீர்ப்பு முழங்கியது: 'தர்ஹி கோ வா நாம ப்ராஹ்மணோ நாம? அப்படியானால் உண்மையான பிராமணன் யார்? யஃ கஸ்சிதாத்மானமத்விதீயம்... எவரொருவர் சாதி, குணம், செயல் அற்றதும், பசி-தாகம்-துக்கம்-மயக்கம்-மூப்பு-மரணம் என்னும் ஆறு ஊர்மிகள் அற்றதும், சச்சிதானந்த சொரூபமானதுமான இரண்டற்ற ஆத்மாவைத் தன் உள்ளத்திலேயே நேருக்கு நேர் (அபரோக்ஷமாக) உணர்கிறாரோ, அவரே பிராமணன்!'",
        "s6_en": "'He whose mind is completely free from desire, attachment, envy, greed, delusion, and pride—who lives with a serene, spotless heart as the very embodiment of Truth—he alone is recognized by Sruti, Smriti, Purana, and Itihasa as a true Brahmana! There is no other way to Brahminhood whatsoever!'",
        "s6_ta": "'காமம், ராகம், மாற்சரியம் (பொறாமை), ஆசை, மயக்கம், ஆணவம் ஆகிய குற்றங்கள் நீங்கி, எவன் தன் ஆத்மாவிலேயே எப்போதும் நிலைபெற்றுள்ளானோ, அவனே உண்மையான பிராமணன் என்பதே சுருதி, ஸ்மிருதி, இதிகாச புராணங்களின் முடிவான துணிபு! பிரம்ம ஞானம் அன்றிப் பிராமணத் தன்மை வேறு எதனாலும் கிடையாது!'",
        "s7_en": "Bow in reverence to that Non-Dual Atman! Whoever meditates upon this Vajrasuchika Upanishad drops all false pride of birth and form, and shines with the diamond radiance of Brahmajnana!",
        "s7_ta": "இரண்டற்ற அந்த ஆத்மாவையே தியானிப்போம்! இந்த வஜ்ரசூசிகா உபநிடதத்தை உணர்பவன் பிறப்பு மற்றும் உடல் பற்றிய போலி கர்வங்களைத் துறந்து, பிரம்ம ஞான வைரம் போல் சுடர்விடுகிறான்!"
    }
]


SAMANYA_SPECS.extend([
    {
        "story_id": "SAMANYA_08_ATMAPRABODHA_42",
        "muktika_number": 42,
        "upanishad_sanskrit": "आत्मप्रबोधोपनिषद्",
        "upanishad_iast": "Ātmaprabodhopaniṣad",
        "upanishad_tamil": "ஆத்மபிரபோத உபநிடதம்",
        "upanishad_english": "Atmaprabodha Upanishad",
        "veda": "Rig Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Awakening to the Inner Narayana: The Lamp that Dissolves the Dream of Samsara",
        "story_title_tamil": "ஆத்ம விழிப்புணர்வு: உள்ளிருக்கும் நாராயண ஜோதியால் சம்சாரக் கனவை நீக்கும் ஆத்மபிரபோத உபநிடதம்!",
        "characters": [
            "The Rig Vedic Rishi of Atmaprabodha (Singing the hymn of Self-Awakening)",
            "Dahara-Narayana (The Eight-Syllabled Supreme Self shining in the lotus of the heart)"
        ],
        "mahavakya_sanskrit": "प्रत्यगानन्दं ब्रह्मपुरुषं प्रणवस्वरूपम् । अकारउकारमकार इति त्रेधा हितं प्रणवेन द्योतितम् ॥",
        "mahavakya_tamil_translit": "ப்ரத்யகானந்தம் ப்ரஹ்மபுருஷம் ப்ரணவஸ்வரூபம் | அகாரஉகாரமகார இதி த்ரேதா ஹிதம் ப்ரணவேன த்யோதிதம் ||",
        "mahavakya_meaning_english": "The Inner Bliss, the Brahma-Purusha, is of the very form of Pranava (OM) shining as A-U-M; He alone is the Witness of the three states!",
        "mahavakya_meaning_tamil": "உள்ளிருக்கும் ஆனந்த சொரூபமான பிரம்ம புருஷனே அ-உ-ம என ஒளிரும் பிரணவ வடிவினன்; மூன்று நிலைகளுக்கும் சாட்சியான அந்த நாராயணனே நாம்!",
        "philosophical_theme": "Integration of Rig Vedic Pranava and Ashtakshara meditation with Advaita Self-Awakening (Atma-Prabodha); comparing Samsara to a dream palace and a mirage that vanishes upon waking.",
        "setting_specifics": "A lotus-filled Rig Vedic ashram at dawn where a golden brass lamp illuminates the inner sanctum of the heart.",
        "metaphor_highlight": "A Lamp inside a Pot shining out through all apertures, Ghee hidden within Milk, and a Dream Palace vanishing the moment one wakes up.",
        "s1_en": "In the Atmaprabodha Upanishad (#42 in the Muktika canon, belonging to the Rig Veda), the Rishi opens with a majestic meditation on the Inner Bliss—Pratyag-Ananda—shining as Pranava (A-U-M) and the Eight-Syllabled Mantra 'Om Namo Narayanaya' within the lotus of the heart!",
        "s1_ta": "முக்திக வரிசையில் 42-ஆவது உபநிடதமான ரிக் வேதத்தின் ஆத்மபிரபோத உபநிடதம், நம் உள்ளத்தின் ஆழத்தில் பிரத்யக் ஆனந்தமாய், அ-உ-ம என்னும் பிரணவ சொரூபமாய், அஷ்டாக்ஷர நாராயணனாய் ஒளிரும் ஆத்ம தியானத்தோடு தொடங்குகிறது!",
        "s2_en": "Though that Supreme Narayana has no form, no birth, and no division, He shines inside the body just like a bright lamp placed inside a perforated clay pot, sending rays of awareness through the eyes, ears, and speech! Like golden ghee hidden within every drop of milk, Consciousness pervades every cell of existence.",
        "s2_ta": "உருவமும் பிறப்பும் அற்ற அந்த நாராயணப் பரம்பொருள், துளைகள் உள்ள குடத்திற்குள் வைக்கப்பட்ட தீபம் போல் உடலுக்குள் ஒளிர்ந்து, கண், காது, வாக்கு ஆகிய துவாரங்கள் வழியே அறிவொளியை வீசுகிறது! பாலுக்குள் நெய் மறைந்திருப்பது போல் பிரபஞ்சம் எங்கும் சைதன்யம் நிறைந்துள்ளது.",
        "s3_en": "How does the seeker awaken from the illusion of limitation? By beholding how a dreamer builds an entire city of pleasures and terrors inside his own mind, and the instant he wakes up, realizes that neither the dream-tiger nor the dream-treasure ever touched him! Even so, waking from Avidya is Atma-Prabodha!",
        "s3_ta": "சிறுமை மயக்கத்திலிருந்து சாதகன் விழித்தெழுவது எப்படி? கனவில் ஒருவன் பல நகரங்களையும் இன்ப-துன்பங்களையும் கண்டு மயங்கி, விழித்தவுடன் அவை எதுவும் தன்னைத் தீண்டவில்லை என உணர்வது போல், அறியாமைத் தூக்கத்திலிருந்து விழிப்பதே 'ஆத்ம பிரபோதம்' ஆகும்!",
        "s4_en": "Just as clouds gather in the sky and dissolve back into the sky without ever staining the sky's blue vastness, and just as ornaments of bracelets and crowns are nothing but pure gold, all beings from Brahma down to a blade of grass are waves in the ocean of my own Consciousness!",
        "s4_ta": "ஆகாயத்தில் மேகங்கள் தோன்றி மறைந்தாலும் ஆகாயம் எவ்வாறு கறையின்றி இருக்கிறதோ, வளையலும் மகுடமும் பொன்னன்றி வேறல்லவோ, அதுபோலவே பிரம்மா முதல் புல் வரை அனைத்து உயிர்களும் என் சைதன்ய சமுத்திரத்தில் எழும் அலைகளே!",
        "s5_en": "Then the awakened sage proclaims the fearless Siddhanta: 'I have neither birth nor death! I have neither bondage nor striving! I am neither the doer nor the enjoyer! I am the Witness of the three worlds, the Self-Luminous Sun of Consciousness that never sets!'",
        "s5_ta": "அப்போது விழிப்புணர்வு பெற்ற ஞானி முழங்குகிறான்: 'எனக்குப் பிறப்புமில்லை, இறப்புமில்லை! எனக்குப் பந்தமுமில்லை, சாதனையுமில்லை! நான் கர்த்தாவும் அல்லன், போக்தாவும் அல்லன்! மூவுலகிற்கும் சாட்சியாய், என்றும் அஸ்தமிக்காத ஞான சூரியனாய் ஒளிர்பவன் நானே!'",
        "s6_en": "Abiding in that Atma-Prabodha, the Yogi beholds the lotus-eyed Narayana not in a distant heaven, but as the very 'I-Consciousness' shining effortlessly in the cave of his own heart.",
        "s6_ta": "இந்த ஆத்ம பிரபோதத்தில் நிலைபெற்ற யோகி, வைகுண்டத்து நாராயணனை எங்கோ தொலைவில் தேடாமல், தன் இதயக் குகையில் சுயமாக ஒளிரும் 'நான்' என்னும் பிரக்ஞையாகவே நேரில் தரிசிக்கிறான்.",
        "s7_en": "Whoever meditates upon this Atmaprabodha Upanishad morning and evening wakes forever from the long night of ignorance and attains the supreme peace of Brahman!",
        "s7_ta": "இந்த ஆத்மபிரபோத உபநிடதத்தைக் காலையிலும் மாலையிலும் தியானிப்பவன், அறியாமை என்னும் நீண்ட உறக்கத்திலிருந்து விழித்தெழுந்து பரம சாந்தியை அடைகிறான்!"
    },
    {
        "story_id": "SAMANYA_09_SKANDA_41",
        "muktika_number": 41,
        "upanishad_sanskrit": "स्कन्दोपनिषद्",
        "upanishad_iast": "Skandopaniṣad",
        "upanishad_tamil": "ஸ்கந்த உபநிடதம்",
        "upanishad_english": "Skanda Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Lord Skanda's Teaching on Shiva-Vishnu Oneness: The Husk and the Rice Grain",
        "story_title_tamil": "ஸ்கந்தப் பெருமானின் உபதேசம்: 'சிவாய விஷ்ணு ரூபாய' — உமியை நீக்கிய அரிசி போல் ஒளிரும் சதாசிவம்!",
        "characters": [
            "Bhagavan Skanda / Kartikeya / Subrahmanya (Revealer of the non-dual unity of Consciousness and the Oneness of Shiva and Vishnu)",
            "Assembly of Devas and Rishis (Receiving the immortal verse 'Shivaya Vishnu-rupaya')"
        ],
        "mahavakya_sanskrit": "शिवाय विष्णुरूपाय शिवरूपाय विष्णवे । शिवस्य हृदयं विष्णुर्विष्णोश्च हृदयं शिवः ॥",
        "mahavakya_tamil_translit": "ஸிவாய விஷ்ணுரூபாய ஸிவரூபாய விஷ்ணவே | ஸிவஸ்ய ஹ்ருதயம் விஷ்ணுர் விஷ்ணோஸ்ச ஹ்ருதயம் ஸிவஃ ||",
        "mahavakya_meaning_english": "Salutations to Shiva who is of the form of Vishnu, and to Vishnu who is of the form of Shiva! Vishnu is the very heart of Shiva, and Shiva is the very heart of Vishnu!",
        "mahavakya_meaning_tamil": "விஷ்ணு வடிவான சிவனுக்கும், சிவ வடிவான விஷ்ணுவிற்கும் நமஸ்காரம்! சிவனின் இதயமே விஷ்ணு, விஷ்ணுவின் இதயமே சிவன்!",
        "philosophical_theme": "Absolute non-difference between Jiva and Shiva (Devo देवालयः प्रोक्तो जीवो देवः सनातनः) and the canonical harmony of Hari and Hara ('Shivaya Vishnu-rupaya').",
        "setting_specifics": "A majestic South Indian Dravidian granite hilltop temple mandapam (Swamimalai/Tiruvannamalai aesthetic) bathed in golden sunrise light.",
        "metaphor_highlight": "Deho Devalayah (The Body is the Temple and the Jiva within is the Eternal God Sadashiva), Husk removed from Paddy grain (Tusha-Tandula), and Copper scrubbed of verdigris turning into Gold (Tamra-Svarnatva).",
        "s1_en": "In the revered Skanda Upanishad (#41 in the Muktika canon, from the Krishna Yajur Veda), Bhagavan Skanda—Lord Subrahmanya, the Supreme Guru—addressed the sages and exclaimed: 'Aho mahatmyam! Through the grace of Lord Mahadeva, I am that Imperishable Consciousness! Why do mortals wander in sorrow when their own Self is the Eternal Shiva?'",
        "s1_ta": "முக்திக வரிசையில் 41-ஆவது உபநிடதமாகத் திகழும் கிருஷ்ண யஜுர் வேதத்தின் 'ஸ்கந்த உபநிடதத்தில்', ஞானபண்டிதனான முருகப்பெருமான் (ஸ்கந்தன்) முனிவர்களுக்கு உபதேசித்தார்: 'மகாதேவனின் திருவருளால் அழியாத ஞான சொரூபமாய் நான் திகழ்கிறேன்! தன் ஆத்மாவே சதாசிவன் என்பதை அறியாமல் மனிதர்கள் ஏன் துயரத்தில் உழல்கின்றனர்?'",
        "s2_en": "Lord Skanda revealed the secret of the Paddy Grain and the Husk: 'As long as a grain of rice is covered by its outer husk (Tusha), it is called paddy and sprouts again into birth when planted; once the husk is removed, it becomes pure white rice (Tandula) and never sprouts again! Even so, while covered by the husk of Vasana and Ego, the soul is called Jiva; when the husk is removed by Guru's grace, that very Jiva shines as Sadashiva!'",
        "s2_ta": "நெல்லும் அரிசியும் என்ற அற்புத உவமையை ஸ்கந்தப் பெருமான் அருளினார்: 'உமி (துஷம்) மூடியிருக்கும் வரை அது நெல் எனப்படுகிறது, மண்ணில் விதைத்தால் மீண்டும் முளைக்கிறது; உமி நீக்கப்பட்டவுடன் அது தூய அரிசியாகி (தண்டுலம்), மீண்டும் பிறவிப் பயிராக முளைப்பதில்லை! அதுபோலவே வாசனை என்னும் உமியால் மூடப்பட்டிருக்கும் வரை ஜீவன் எனப்படுகிறான்; குருவருளால் உமி நீங்கியவுடன் அவனே சதாசிவனாக ஒளிர்கிறான்!'",
        "s3_en": "Then Lord Skanda uttered the famous temple verse of Vedanta: 'Deho devalayah prokto jivo devah sanatanah! Tyajed ajnana-nirmalyam so'ham-bhavena pujayet! This human body itself is the sacred Temple; the Jiva dwelling within is the Eternal God! Cast away the faded flowers of ignorance, and worship Him with the non-dual realization: So'ham—I am He!'",
        "s3_ta": "தொடர்ந்து ஆலய வழிபாட்டின் பரம ரகசியத்தை முருகப்பெருமான் முழங்கினார்: 'தேஹோ தேவாலயஃ ப்ரோக்தோ ஜீவோ தேவஃ ஸனாதனஃ! த்யஜேத் அஜ்ஞான நிர்மால்யம் ஸோऽஹம் பாவேன பூஜயேத்! இந்த மனித உடம்பே திருக்கோயில்; உள்ளே உறையும் ஜீவனே சனாதன தெய்வம்! அறியாமை என்னும் பழைய பூக்களை (நிர்மால்யத்தை) அகற்றிவிட்டு, அவனே நான் (ஸோऽஹம்) என்ற பாவனையால் பூஜிப்பாயாக!'",
        "s4_en": "Next flows the immortal hymn of Hari-Hara unity that originates right here in the Skanda Upanishad: 'Shivaya Vishnu-rupaya, Shiva-rupaya Vishnave, Shivasya hridayam Vishnur, Vishnoshcha hridayam Shivah! Salutations to Shiva who is of the form of Vishnu, and to Vishnu who is of the form of Shiva! Vishnu is the very heart of Shiva, and Shiva is the very heart of Vishnu!'",
        "s4_ta": "அடுத்து கோயில்கள் தோறும் ஒலிக்கும் அரியும் சிவனும் ஒன்றே என்ற புகழ்பெற்ற சுலோகம் இந்த ஸ்கந்த உபநிடதத்திலேயே அருளப்படுகிறது: 'ஸிவாய விஷ்ணுரூபாய ஸிவரூபாய விஷ்ணவே, ஸிவஸ்ய ஹ்ருதயம் விஷ்ணுர் விஷ்ணோஸ்ச ஹ்ருதயம் ஸிவஃ! விஷ்ணுவின் வடிவான சிவனுக்கும், சிவனின் வடிவான விஷ்ணுவிற்கும் நமஸ்காரம்! சிவனின் இதயமே விஷ்ணு, விஷ்ணுவின் இதயமே சிவன்!'",
        "s5_en": "'Yatha Shivamayo Vishnur evam Vishnumayah Shivah, yathantaram na pashyami tatha me svastir ayushi! Just as Vishnu is wholly Shiva, so Shiva is wholly Vishnu; and as I behold no difference whatsoever between them, may auspiciousness and immortality abide in my life! Between Kesava and Sadasiva, and between the Jiva and Brahman, there is not a hair's breadth of division!'",
        "s5_ta": "'யதா ஸிவமயோ விஷ்ணுர் ஏவம் விஷ்ணுமயஃ ஸிவஃ! விஷ்ணு எவ்வாறு சிவமயமோ, அவ்வாறே சிவனும் விஷ்ணுமயமே! இவ்விருவருக்கும் இடையே எள்ளளவும் பேதத்தை நான் காணாததால் என் வாழ்வில் என்றும் மங்கலம் நிலவட்டும்! அரன், அரி மற்றும் ஆத்மா ஆகிய மூன்றும் ஒரே சச்சிதானந்தப் பரம்பொருளே!'",
        "s6_en": "Beholding the six-faced Lord Skanda shining as the non-dual light of both Shiva and Vishnu inside the heart-temple, the assembled sages transcended all sectarian dispute and rested in unbroken bliss.",
        "s6_ta": "இதயக் கோயிலுக்குள் சிவனும் விஷ்ணுவும் ஒன்றாய் ஒளிரும் கந்தப் பெருமானின் ஞான ஒளியைத் தரிசித்த முனிவர்கள், பேத புத்திகள் அனைத்தும் நீங்கிப் பேரானந்தத்தில் நிலைபெற்றனர்.",
        "s7_en": "Thus concludes the Skanda Upanishad with its triumphant promise: 'Samasta-veda-siddhantam—This is the final Siddhanta of all the Vedas! He who studies this is never born again!'",
        "s7_ta": "அனைத்து வேதங்களின் சித்தாந்த சாரமான இந்த ஸ்கந்த உபநிடதத்தை ஓதி உணர்பவன் மீண்டும் பிறவாமல் மோட்ச சாம்ராஜ்யத்தை அடைகிறான்!"
    },
    {
        "story_id": "SAMANYA_10_MUDGALA_57",
        "muktika_number": 57,
        "upanishad_sanskrit": "मुद्गलोपनिषद्",
        "upanishad_iast": "Mudgalopaniṣad",
        "upanishad_tamil": "முத்கல உபநிடதம்",
        "upanishad_english": "Mudgala Upanishad",
        "veda": "Rig Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Indra & Sage Mudgala on the Purusha Sukta: Why Three Quarters of God Transcend Creation",
        "story_title_tamil": "இந்திரனும் முத்கல முனிவரும்: புருஷ சூக்தத்தின் உட்பொருளும் பிரபஞ்சத்தைக் கடந்த முக்கால் பங்கு பரம்பொருளும்!",
        "characters": [
            "Maharishi Mudgala (Son of Bharmyasva, the Rig Vedic sage expounding the esoteric Vedantic meaning of the Purusha Sukta)",
            "Lord Indra (King of the Gods, coming as a humble student to learn the secret of the Purusha Sukta)"
        ],
        "mahavakya_sanskrit": "पादोऽस्य विश्वा भूतानि त्रिपादस्यामृतं दिवि । स भूमिं विश्वतो वृत्वाऽत्यतिष्ठद्दशाङ्गुलम् ॥",
        "mahavakya_tamil_translit": "பாதோऽஸ்ய விஸ்வா பூதானி த்ரிபாதஸ்யாம்ருதம் திவி | ஸ பூமிம் விஸ்வதோ வ்ருத்வாऽத்யதிஷ்டத் தஸாங்குலம் ||",
        "mahavakya_meaning_english": "All living beings and this entire cosmos are but one-fourth (one foot) of Him; three-fourths of Him abide in immortal radiance beyond! Enveloping all, He transcends by ten fingers' breadth!",
        "mahavakya_meaning_tamil": "இப்பிரபஞ்சமும் எல்லா உயிர்களும் அந்தப் பரம்பொருளின் கால் பங்கு (ஒரு பாதம்) மட்டுமே; அவரது முக்கால் பங்கு அமிர்த மயமாய் மேலே ஒளிர்கிறது! அனைத்தையும் சூழ்ந்து பத்து விரற்கடை கடந்து நிற்கிறார்!",
        "philosophical_theme": "The Esoteric Advaita Commentary on the Rig Vedic Purusha Sukta; how the Infinite Narayana performs the Cosmic Mental Sacrifice (Jnana-Yajna) without losing His transcendental fullness.",
        "setting_specifics": "Maharishi Mudgala's Rig Vedic hermitage where Lord Indra sits beside the sacrificial altar while the starry cosmic Purusha shines overhead.",
        "metaphor_highlight": "One Quarter (Pada) as the entire visible universe vs. Three Quarters (Tripad) as Immortal Transcendence, and the Bird catching a fish without getting trapped in the water.",
        "s1_en": "In the Mudgala Upanishad (#57 in the Muktika canon, belonging to the Rig Veda), Maharishi Mudgala—renowned for his supreme contentment and wisdom—imparted to Lord Indra the deepest Vedantic secret of the Rig Vedic Purusha Sukta ('Sahasrashirsha Purushah')!",
        "s1_ta": "முக்திக வரிசையில் 57-ஆவது உபநிடதமாகத் திகழும் ரிக் வேதத்தின் 'முத்கல உபநிடதத்தில்', மகரிஷி முத்கலர் தேவேந்திரனுக்கு ரிக் வேத புருஷ சூக்தத்தின் ('ஸஹஸ்ரஸீர்ஷா புருஷஃ') ஆழ்ந்த வேதாந்த ரகசியத்தை உபதேசித்தார்!",
        "s2_en": "Explaining the opening verses to Indra, Mudgala declared: 'When the Purusha Sukta says the Supreme Being has a thousand heads, eyes, and feet, the word Thousand signifies INFINITY (Ananta)! Though He pervades the entire universe inside and out, He still stands beyond it—Atyatishthad dashangulam—transcending all limits of space and time!'",
        "s2_ta": "புருஷ சூக்தத்தின் முதல் மந்திரங்களை விளக்கிய முத்கலர், 'புருஷனுக்கு ஆயிரம் தலைகள், ஆயிரம் கண்கள், ஆயிரம் பாதங்கள் உள்ளன என்று வேதம் கூறும்போது, ஆயிரம் என்ற சொல் அனந்தம் (எல்லையற்றது) என்பதையே குறிக்கிறது! இப்பிரபஞ்சம் அனைத்தையும் சூழ்ந்து நின்றாலும், அதனையும் கடந்து பத்து விரற்கடை மேலாக எல்லையற்று நிற்கிறார்!' என்றார்.",
        "s3_en": "Then Mudgala revealed the awe-inspiring proportion of the Absolute: 'Pado'sya vishva bhutani tripad asyamritam divi! All past, present, and future universes—all galaxies, gods, humans, and creatures—are merely ONE QUARTER of the Supreme Vasudeva! Three full quarters of His glory remain untouched in self-luminous Immortality!'",
        "s3_ta": "'பாதோऽஸ்ய விஸ்வா பூதானி த்ரிபாதஸ்யாம்ருதம் திவி!' — கடந்த காலம், நிகழ்காலம், எதிர்காலம் ஆகிய முக்காலப் பிரபஞ்சங்களும் அந்த வாசுதேவனின் கால் பங்கு (ஒரு பாதம்) மட்டுமே! அவரது முக்கால் பங்கு மகிமை எவ்வித மாற்றமுமின்றி அமிர்த சுய ஒளியில் நிலைபெற்றுள்ளது!",
        "s4_en": "Indra asked in wonder: 'How did that Unchanging One become the many?' Mudgala explained the Cosmic Jnana-Yajna: 'Out of compassion to liberate bound souls, the Supreme Hari entered His own Prakriti through a sacrifice of pure Knowledge—making Spring the clarified butter, Summer the fuel, and Autumn the offering—and entered every body from the crown down to the feet!'",
        "s4_ta": "'மாற்றமற்ற அந்த ஏகப் பரம்பொருள் எவ்வாறு பலவாகத் தோன்றியது?' என்று இந்திரன் கேட்டான். முத்கலர் விளக்கினார்: 'ஜீவர்களை உய்விக்கும் பெருங்கருணையால், பரம புருஷனே வசந்த காலத்தை நெய்யாகவும், கோடையை விறகாகவும், சரத் காலத்தை ஆஹுதியாகவும் கொண்டு ஞான யக்ஞம் நிகழ்த்தி, ஒவ்வொரு உடலுக்குள்ளும் ஆத்மாவாகப் பிரவேசித்தார்!'",
        "s5_en": "Yet does entering the mortal body bind the Supreme Lord? Mudgala gave the metaphor of the Diving Bird: 'Just as a swift water-bird dives into the deep river, catches its prey, and flies effortlessly back into the open sky without drowning, so the Supreme Purusha enters Jiva-hood and lifts the awakened soul back into Immortal Brahman!'",
        "s5_ta": "உடலுக்குள் புகுந்ததால் இறைவன் கட்டுப்பட்டு விடுவாரா? முத்கலர் நீர்ப்பறவை உவமையைக் கூறினார்: 'நீருக்குள் பாய்ந்து இரையைப் பிடிக்கும் பறவை நீரில் மூழ்கிவிடாமல் உடனே ஆகாயத்தில் பறந்து எழுவது போல், பரம புருஷன் ஜீவனாகப் புகுந்து தன்னை உணர்ந்தவனை உடனே அமிர்தப் பெருவெளிக்கு உயர்த்துகிறார்!'",
        "s6_en": "Hearing this secret of the Purusha Sukta—that the Jiva and Paramatman are one—Lord Indra bowed to Maharishi Mudgala as the sixfold afflictions of hunger, thirst, sorrow, delusion, old age, and death fell away.",
        "s6_ta": "புருஷ சூக்தத்தின் இந்தப் பரம ரகசியத்தைக் கேட்ட தேவேந்திரன், பசி, தாகம், சோக, மோக, ஜரா, மரணம் என்னும் ஆறு ஊர்மிகளும் நீங்கி முத்கல முனிவரின் திருவடிகளில் பணிந்தான்.",
        "s7_en": "This sacred Mudgala Upanishad must never be given to the envious or the faithless; imparted to a pure-hearted disciple at twilight, it bestows immediate realization of the Cosmic Purusha!",
        "s7_ta": "புனிதமான இந்த முத்கல உபநிடத ரகசியத்தை சிரத்தையும் புலனடக்கமும் கொண்ட சீடனுக்கு உபதேசிக்க, அவன் விராட் புருஷனான நாராயணப் பரம்பொருளோடு இரண்டறக் கலக்கிறான்!"
    },
    {
        "story_id": "SAMANYA_11_PAINGALA_59",
        "muktika_number": 59,
        "upanishad_sanskrit": "पैङ्गलोपनिषद्",
        "upanishad_iast": "Paiṅgalopaniṣad",
        "upanishad_tamil": "பைங்கல உபநிடதம்",
        "upanishad_english": "Paingala Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Sage Paingala's 12 Years of Service to Yajnavalkya: The Painted Cloth of the World & Jivanmukti",
        "story_title_tamil": "யாக்ஞவல்கியரிடம் 12 ஆண்டுகள் தொண்டு செய்த பைங்கலர்: சித்திரத் துணி உவமையும் ஜீவன்முக்தி ரகசியமும்!",
        "characters": [
            "Sage Paingala (Who served Maharishi Yajnavalkya for 12 years with single-pointed devotion)",
            "Maharishi Yajnavalkya (Expounding the four chapters of the Paingala Upanishad on Creation, Mahavakya, and Jivanmukti)"
        ],
        "mahavakya_sanskrit": "तत्त्वमसि त्वं तदसि... घटे नष्टे घटाकाशो महाकाश एव भवति । तोये शैत्यं यथाग्नौ औष्ण्यं तथा चिन्मात्रो भवति ॥",
        "mahavakya_tamil_translit": "தத்த்வமஸி த்வம் ததஸி... கடே நஷ்டே கடாகாஸோ மஹாகாஸ ஏவ பவதி | தோயே சைத்யம் யதாக்னௌ ஒளஷ்ண்யம் ததா சின்மாத்ரோ பவதி ||",
        "mahavakya_meaning_english": "Thou Art That, and That Art Thou! When the pot breaks, the pot-space is one with boundless cosmic space; as coolness in water and heat in fire, the liberated sage abides as Pure Consciousness alone!",
        "mahavakya_meaning_tamil": "அதுவே நீ, நீயே அது! குடம் உடைந்தவுடன் குட ஆகாயம் மகா ஆகாயமாவது போலவும், நீரில் குளிர்ச்சியும் நெருப்பில் வெப்பமும் போல் ஞானி தூய சின்மாத்திரமாய் நிலைபெறுகிறான்!",
        "philosophical_theme": "Comprehensive 4-chapter treatise on Advaita: Creation (Panchikarana), the Painted Canvas Metaphor (Citrapata), Meditation in the Five-Petaled Heart Lotus, and the state of Videhamukti beyond Kashi or sacred places.",
        "setting_specifics": "Maharishi Yajnavalkya's Mithila forest hermitage where disciple Paingala completes twelve years of humble guru-seva.",
        "metaphor_highlight": "Painted Canvas (Dhauta-Vastra / Citrapata—when the paint fades, only the white cloth remains), Reflections of the Sun in water bowls, and Iron turned to Gold by the Philosopher's Stone (Sparshamani).",
        "s1_en": "In the comprehensive Paingala Upanishad (#59 in the Muktika canon, from the Shukla Yajur Veda), Sage Paingala lived for twelve full years serving Maharishi Yajnavalkya with unwavering devotion, and then bowed at his feet asking: 'O Bhagavan! Pray reveal to me the supreme mystery of Kaivalya!'",
        "s1_ta": "முக்திக வரிசையில் 59-ஆவது உபநிடதமாகத் திகழும் சுக்ல யஜுர் வேதத்தின் 'பைங்கல உபநிடதத்தில்', மகரிஷி யாக்ஞவல்கியரிடம் பன்னிரண்டு ஆண்டுகள் தொண்டு செய்த பைங்கல முனிவர், 'பகவானே! கைவல்ய முக்தியின் பரம ரகசியத்தை எனக்கு அருளுங்கள்!' என்று வேண்டினார்.",
        "s2_en": "Yajnavalkya explained how in the beginning Sat alone existed—unborn, changeless, like a lump of gold before it is shaped into bracelets and crowns! Blending with Mulaprakriti and undergoing Fivefold Combination (Panchikarana), that One Consciousness constructed the cosmic egg and the subtle channels of the body, yet remained ever unstained!",
        "s2_ta": "யாக்ஞவல்கியர் உபதேசிக்கத் தொடங்கினார்: 'ஆதியில் சத் என்னும் பிரம்மம் மட்டுமே இரண்டற்று இருந்தது! ஆபரணங்களாக மாறுவதற்கு முன் உள்ள பசும்பொன் கட்டி போல் இருந்த அந்தப் பரம்பொருள், மாயையோடு கூடிப் பஞ்சீகரணத்தின் வழியே அண்ட-பிண்டங்களைப் படைத்து, உள்ளே சாட்சியாக வீற்றிருக்கிறது!'",
        "s3_en": "To show how the world-illusion disappears upon inquiry, Yajnavalkya gave the famous Painted Canvas metaphor (Citrapata): 'Look at a white cloth stiffened with starch and painted with vivid figures of kings, mountains, and chariots! When the starch and paint are washed away, what remains? Only the pure white cloth! Even so, when karmic impressions are washed away by Jnana, only the Pure Consciousness remains!'",
        "s3_ta": "உலக மாயை நீங்கும் விதத்தை விளக்க 'சித்திரத் துணி' (சித்ரபடம்) உவமையைக் கூறினார் யாக்ஞவல்கியர்: 'வெள்ளைத் துணியில் கஞ்சி பூசி அதன் மேல் பல வண்ண ஓவியங்களை வரைகிறார்கள்; அந்த வண்ணங்களும் கஞ்சியும் கழுவப்பட்டவுடன் தூய வெள்ளைத் துணி மட்டுமே எஞ்சி நிற்பது போல், ஞானத்தால் பிரபஞ்சக் கற்பனை நீங்கியவுடன் தூய ஆத்மா மட்டுமே ஒளிர்கிறது!'",
        "s4_en": "Yajnavalkya continued: 'Just as a traveler mistakes a mother-of-pearl shell for silver, or a desert mirage for a river, or a post for a man in the dark, the ignorant mistake this body of five sheaths for the Self! Meditate continuously inside the lotus of the heart: Tat Tvam Asi—Thou Art That; Tvam Tad Asi—That Art Thou; Aham Brahmasmi—I am Brahman!'",
        "s4_ta": "'சிப்பியை வெள்ளி என்றும், கானல் நீரை ஆறு என்றும், இருட்டில் நிற்கும் கட்டையை மனிதன் என்றும் மயங்குவது போலவே அज्ञானிகள் உடலை ஆத்மா என்கின்றனர்! தத் த்வம் அஸி (அதுவே நீ), த்வம் ததஸி (நீயே அது), அஹம் பிரம்மாஸ்மி (நானே பிரம்மம்) என்று இதயத் தாமரையில் இடைவிடாது தியானிப்பாயாக!'",
        "s5_en": "'Just as iron touched by the Philosopher's Stone (Sparshamani) immediately becomes pure gold, and just as space inside a pot becomes one with the boundless sky when the pot breaks, the Yogi who realizes his oneness with Brahman becomes spotless Consciousness—whether he casts off his body in a sacred shrine like Kashi or in an outcaste's hut!'",
        "s5_ta": "'ஸ்பரிசமணியால் தொடப்பட்ட இரும்பு உடனே தங்கமாவது போலவும், குடம் உடைந்தவுடன் குட ஆகாயம் மகா ஆகாயத்தோடு ஒன்றாவது போலவும், பிரம்ம ஞானம் பெற்ற யோகி தன் உடலைப் புண்ணியத் தலத்தில் விட்டாலும் சரி, எங்கே விட்டாலும் சரி, அப்போதே முக்தியடைகிறான்!'",
        "s6_en": "Paingala asked: 'Where go the winds, stars, and worlds of such a liberated sage?' Yajnavalkya answered: 'Just as Ghee poured into Ghee becomes one Ghee, and milk poured into milk becomes one milk, the Jivanmukta abides as coolness in water, heat in fire, and fragrance in earth—pure, indivisible Chinmatra!'",
        "s6_ta": "'நெய்யில் ஊற்றப்பட்ட நெய் நெய்யோடு ஒன்றாவது போலவும், பாலில் கலந்த பால் பாலோடு ஒன்றாவது போலவும், நீரில் குளிர்ச்சியும் நெருப்பில் வெப்பமும் போல் ஜீவன்முக்தன் சின்மாத்திரப் பிரம்மத்தோடு இரண்டறக் கலந்து நிற்கிறான்!' என்றார் யாக்ஞவல்கியர்.",
        "s7_en": "Hearing this four-chapter nectar of the Paingala Upanishad, Sage Paingala bowed at Yajnavalkya's feet and shone forth as an immortal Jivanmukta!",
        "s7_ta": "நான்கு அத்தியாயங்கள் கொண்ட இந்தப் பைங்கல உபநிடத அமிர்தத்தைப் பருகிய பைங்கல முனிவர், யாக்ஞவல்கியரின் திருவடிகளை வணங்கி ஜீவன்முக்தராகப் பிரகாசித்தார்!"
    },
    {
        "story_id": "SAMANYA_12_MAHAD_61",
        "muktika_number": 61,
        "upanishad_sanskrit": "महोपनिषद्",
        "upanishad_iast": "Mahopaniṣad",
        "upanishad_tamil": "மஹா உபநிடதம் (வசுதைவ குடும்பகம்)",
        "upanishad_english": "Maha Upanishad",
        "veda": "Sama Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Ribhu, Nidagha & Shuka-Janaka: 'Vasudhaiva Kutumbakam' & The Seven Stages of Wisdom",
        "story_title_tamil": "நிதாகர் - ரிபு மற்றும் சுகர் - ஜனகர்: 'வசுதைவ குடும்பகம்' பிறந்த மஹா உபநிடதமும் சப்த பூமிகைகளும்!",
        "characters": [
            "Lord Narayana (The Primeval Purusha from whose forehead-meditation Rudra and Brahma arose)",
            "Brahmarishi Shuka & Rajarishi Janaka (Dialogue on how Shuka attained peace through Janaka's confirmation)",
            "Sage Ribhu & Disciple Nidagha (The Guru who disguised himself as a village rustic to cure Nidagha's ritual attachment)"
        ],
        "mahavakya_sanskrit": "अयं बन्धुरयं नेति गणना लघुचेतसाम् । उदारचरितानां तु वसुधैव कुटुम्बकम् ॥",
        "mahavakya_tamil_translit": "அயம் பந்துரயம் நேதி கணனா லகுசேதஸாம் | உதாரசரிதானாம் து வஸுதைவ குடும்பகம் ||",
        "mahavakya_meaning_english": "'This one is my relative, and that one is a stranger'—such is the calculation of narrow-minded mortals. For the noble-hearted knowers of the Self, the entire Earth is one family (Vasudhaiva Kutumbakam)!",
        "mahavakya_meaning_tamil": "'இவன் என் உறவினன், இவன் அந்நியன்' என்று கணக்கிடுவது குறுகிய மனம் கொண்டவர்களின் இயல்பு; பரந்த உள்ளம் கொண்ட ஞானிகளுக்கோ இவ்வுலகம் முழுவதுமே ஒரே குடும்பம் (வசுதைவ குடும்பகம்)!",
        "philosophical_theme": "Source of the world-famous maxim 'Vasudhaiva Kutumbakam' (Chapter 6.71); dialogue of Shuka and Janaka; Ribhu and Nidagha; the Seven Jnana-Bhumikas (Stages of Wisdom) and Seven Ajnana-Bhumikas.",
        "setting_specifics": "Mithila's royal garden where young Shuka meets King Janaka, and the forested banks of the Devika river where Sage Ribhu visits Nidagha.",
        "metaphor_highlight": "Vasudhaiva Kutumbakam (The Whole Earth is One Family), A Boy imagining a Ghost in the dark (Vetala), and the Seven Rungs of Jnana-Bhumika (Subheccha, Vicharana, Tanumanasa, Sattvapatti, Asamsakti, Padarthabhavana, Turiya).",
        "s1_en": "The grand Maha Upanishad (#61 in the Muktika canon, from the Sama Veda) is a vast ocean of Advaita wisdom! Beginning with the primeval Narayana, its six chapters unfold the dialogues of Shuka with King Janaka, and Sage Ribhu with his disciple Nidagha—and give humanity the immortal mantra: 'Vasudhaiva Kutumbakam'!",
        "s1_ta": "முக்திக வரிசையில் 61-ஆவது உபநிடதமாகத் திகழும் சாம வேதத்தின் 'மஹா உபநிடதம்', அத்வைத ஞானத்தின் மகா சமுத்திரமாகும்! ஆதி நாராயண தத்துவத்தில் தொடங்கி, சுகர்-ஜனகர் உரையாடல், ரிபு-நிதாகர் வரலாறு மற்றும் உலகப் புகழ்பெற்ற 'வசுதைவ குடும்பகம்' என்னும் மகா மந்திரத்தை இவ்வுபநிடதம் வழங்குகிறது!",
        "s2_en": "In the second chapter, young Shuka—though taught by his father Vyasa on Mount Meru—sought complete inner peace and journeyed to Mithila to test Rajarishi Janaka! Janaka kept him waiting seven days at the palace gate, then surrounded him with royal luxuries; yet Shuka remained unmoved as a mountain! Bowing to Janaka, Shuka asked how the world arose, and Janaka replied: 'Just as a child imagines a ghost in the shadows and trembles at his own thought, the mind alone projects and dissolves this Samsara!'",
        "s2_ta": "இரண்டாம் அத்தியாயத்தில், வியாசரின் புதல்வரான சுகர் மனத் தெளிவு வேண்டி மிதிலை மன்னர் ஜனகரை நாடிச் சென்றார். வாசலில் ஏழு நாட்கள் காத்திருக்க வைத்தும், அரண்மனை போகங்களைக் காட்டியும் சோதித்தபோது சுகர் மலைபோல் அசையாமல் நின்றார்! ஜனகர் சுகருக்கு உபதேசித்தார்: 'குழந்தை இருட்டில் தன்னுடைய கற்பனையாலேயே பேயை எண்ணி அஞ்சுவது போல், மனமே சம்சாரத்தைக் கற்பனை செய்து கொள்கிறது; சங்கல்பம் அழிந்தால் முக்தி சித்திக்கும்!'",
        "s3_en": "Next unfolds the story of Sage Ribhu and his disciple Nidagha by the Devika river! Though learned, Nidagha still clung to ritualistic pride. When Ribhu visited him disguised as a rustic villager and was offered food, Ribhu rejected the first meal as 'impure with ego', and only when Nidagha humbly recognized his Guru did Ribhu teach him that all separation between 'sacred' and 'profane' is mental delusion!",
        "s3_ta": "தொடர்ந்து தேவிகா நதிக்கரையில் வாழ்ந்த நிதாகருக்கும் அவரது குருவான ரிபு முனிவருக்கும் நடந்த உரையாடல் விரிகிறது! சடங்குப் பற்றில் நின்ற நிதாகரைத் திருத்த, ரிபு முனிவர் ஒரு சாதாரணக் கிராமவாசி வேடத்தில் வந்து ஆத்ம விசாரத்தைத் தூண்டினார்; பேத புத்தியே அறியாமை என்றும், எங்கும் நிறைந்த சைதன்யமே சத்தியம் என்றும் நிதாகருக்கு உணர்த்தினார்.",
        "s4_en": "Then the Maha Upanishad maps the Seven Stages of Ignorance and the Seven Stages of Wisdom—Sapta Jnana-Bhumikas: 1) Subheccha (Noble aspiration for truth), 2) Vicharana (Philosophical inquiry), 3) Tanumanasa (Attenuation of mental vasanas), 4) Sattvapatti (Abiding in pure Sattva and realization), 5) Asamsakti (Complete non-attachment), 6) Padarthabhavana (Dissolution of objective multiplicity), and 7) Turiya (Eternal abidance in the Fourth)!",
        "s4_ta": "அடுத்து ஞானத்தின் ஏழு படிகளை (சப்த ஞான பூமிகைகளை) மஹா உபநிடதம் வரையறுக்கிறது: 1) சுபேச்சை (நல்விருப்பம்), 2) விசாரணை (ஆத்ம விசாரணை), 3) தனுமானஸா (வாசனைகள் மெலிதல்), 4) சத்வாபத்தி (சத்வ நிலையில் ஆத்ம தரிசனம்), 5) அஸம்ஸக்தி (பற்றற்ற நிலை), 6) பதார்த்த அபாவனை (வெளிப்பொருள் தோற்றம் மறைதல்), 7) துரீய நிலை (இரண்டற்ற பிரம்ம நிஷ்டை)!",
        "s5_en": "And in Chapter 6, Verse 71, describing the exalted character of the Jivanmukta who sees the One Self in all beings, the Maha Upanishad proclaims the verse inscribed in the Parliament of India: 'Ayam bandhur ayam neti ganana laghu-chetasam, udara-charitanam tu Vasudhaiva Kutumbakam! This one is my kinsman and that one is a stranger—so calculate the small-minded; for the magnanimous knowers of Truth, the entire Earth is One Family!'",
        "s5_ta": "ஆறாம் அத்தியாயத்தின் 71-ஆவது சுலோகத்தில், பாரத நாடாளுமன்றத்தில் பொறிக்கப்பட்டுள்ள உலகப் புகழ்பெற்ற மந்திரத்தை மஹா உபநிடதம் முழங்குகிறது: 'அயம் பந்துரயம் நேதி கணனா லகுசேதஸாம், உதாரசரிதானாம் து வஸுதைவ குடும்பகம்! இவன் என் உறவினன், இவன் அந்நியன் என்று கணக்கிடுவது குறுகிய மனம் கொண்டவர்களின் இயல்பு; பரந்த உள்ளம் கொண்ட மகாத்மாக்களுக்கோ இவ்வுலகம் முழுவதுமே ஒரே குடும்பம்!'",
        "s6_en": "Living in this cool, desireless coolness of the spirit—Shitalatva—the sage walks through the world like the sky: untouched by praise or blame, smiling gently at the play of the Gunas.",
        "s6_ta": "ஆசைத் தீ அணைந்த இந்தக் குளிர்ந்த ஞான நிலையில் (சீதளத்வம்) வீற்றிருக்கும் ஞானி, புகழ்ச்சிக்கும் இகழ்ச்சிக்கும் அப்பாற்பட்டு ஆகாயத்தைப் போல் நிர்மலமாய் உலவுகிறான்.",
        "s7_en": "Thus the Maha Upanishad concludes: 'Break the elephant-chain of Vasanas with the sword of non-attachment, behold the entire Earth as one divine family in the Atman, and rest forever in Turiya!'",
        "s7_ta": "வாசனை என்னும் விலங்கை வைராக்கிய வாளால் அறுத்து, உலகம் அனைத்தையும் ஒரே ஆத்ம குடும்பமாகத் தரிசித்து, துரீயப் பெருநிலையில் நிலைபெறுவோம்!"
    },
    {
        "story_id": "SAMANYA_13_SHARIRAKA_62",
        "muktika_number": 62,
        "upanishad_sanskrit": "शारीरकोपनिषद्",
        "upanishad_iast": "Śārīrakopaniṣad",
        "upanishad_tamil": "சாரீரக உபநிடதம்",
        "upanishad_english": "Shariraka Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Sacred Anatomy of the 36 Tattvas: Who Dwells Inside the Chariot of the Body?",
        "story_title_tamil": "உடலின் 36 தத்துவங்களும் அந்தக்கரண ரகசியமும்: சாரீரக உபநிடதம் காட்டும் பரமாத்மா!",
        "characters": [
            "The Krishna Yajur Veda Acharya (Analyzing the psycho-physical anatomy of the body to isolate the Pure Witness)",
            "Gurukulam Disciples (Learning how the 5 Elements, 25 qualities, 10 Indriyas, and 4 Antahkaranas differ from the Purusha)"
        ],
        "mahavakya_sanskrit": "जीवात्मपरमात्मनोर्भेदो हि... क्षेत्रज्ञः परमात्मा स एव सर्वभूतान्तरात्मा ॥",
        "mahavakya_tamil_translit": "ஜீவாத்ம பரமாத்மனோர் பேதோ ஹி... க்ஷேத்ரஜ்ஞஃ பரமாத்மா ஸ ஏவ ஸர்வபூதாந்தராத்மா ||",
        "mahavakya_meaning_english": "When the conditioning of the body and gunas is understood, the Kshetrajna—the Knower of the Field—shines forth as the Supreme Paramatman indwelling all beings!",
        "mahavakya_meaning_tamil": "பஞ்ச பூத உடலின் தத்துவங்களைப் பிரித்துணரும்போது, உடலாகிய க்ஷேத்திரத்தை அறியும் க்ஷேத்ரஜ்ஞனே எல்லா உயிர்களுக்கும் உள்ளுறையும் பரமாத்மா என்பது விளங்கும்!",
        "philosophical_theme": "Tattva-Viveka (Discrimination of the 5 Elements, 5 Tanmatras, 5 Jnanendriyas, 5 Karmendriyas, 4 Antahkaranas, 3 Gunas, and 3 States) from the Kshetrajna Purusha.",
        "setting_specifics": "An ancient Vedic Gurukulam science-and-philosophy pavilion with anatomical diagrams etched on palm leaves and five elemental vessels.",
        "metaphor_highlight": "Five Vessels of Earth, Water, Fire, Air, and Space; the Fourfold Inner Instrument (Manas, Buddhi, Ahankara, Chitta); and the Kshetrajna (Knower of the Field).",
        "s1_en": "In the Shariraka Upanishad (#62 in the Muktika canon, from the Krishna Yajur Veda—sharing its very name with the Brahma Sutras' Shariraka Mimamsa), the Acharya gathered his disciples around five sacred vessels representing Earth, Water, Fire, Air, and Space, and asked: 'What is this Sharira—this human body—and who is the Lord dwelling within it?'",
        "s1_ta": "முக்திக வரிசையில் 62-ஆவது உபநிடதமாகத் திகழும் கிருஷ்ண யஜுர் வேதத்தின் 'சாரீரக உபநிடதத்தில்', பிருதிவி, அப்பு, தேஜஸ், வாயு, ஆகாயம் ஆகிய பஞ்ச பூதக் கலசங்களை முன்வைத்து ஆச்சாரியர் கேட்டார்: 'இந்தச் சரீரம் எதனால் ஆனது? இதனுள் வீற்றிருக்கும் தலைவன் யார்?'",
        "s2_en": "With scientific precision, the Upanishad maps how the five elements form the body: 'What is hard in the body—bone, skin, nerves, hair, and flesh—belongs to Earth! What is fluid—blood, saliva, sweat, and vital fluids—belongs to Water! Hunger, thirst, warmth, glow, and sleep belong to Fire! Walking, breathing, expansion, and contraction belong to Air! And space, passion, anger, and fear arise within Akasha!'",
        "s2_ta": "உடலின் அமைப்பைத் துல்லியமாகப் பகுத்துக் காட்டுகிறது உபநிடதம்: 'எலும்பு, தோல், நரம்பு, தசை, மயிர் ஆகிய ஐந்தும் பூமியின் கூறுகள்! இரத்தம், வியர்வை உள்ளிட்ட திரவங்கள் நீரின் கூறுகள்! பசி, தாகம், உடல் வெப்பம், ஒளி ஆகியவை நெருப்பின் கூறுகள்! ஓடுதல், நடத்தல், மூச்சு விடுதல் ஆகியவை வாயுவின் கூறுகள்! இடம், காமம், குரோதம் ஆகியவை ஆகாயத்தின் கூறுகள்!'",
        "s3_en": "Next, the Acharya distinguished the ten external instruments—the five organs of knowledge (Ear, Skin, Eye, Tongue, Nose) and the five organs of action (Speech, Hands, Feet, Excretion, Generation)—and then turned to the Fourfold Inner Instrument, the Antahkarana!",
        "s3_ta": "தொடர்ந்து மெய், வாய், கண், மூக்கு, செவி ஆகிய ஐந்து ஞானேந்திரியங்களையும், வாக்கு, பாதம், பாணி முதலான ஐந்து கர்மேந்திரியங்களையும் விளக்கிவிட்டு, உள்ளேயுள்ள நான்கு அந்தக்கரணங்களின் பணிகளை விவரித்தார்!",
        "s4_en": "'Listen carefully to the four functions of the inner mind: MANAS is the faculty of संकल्प-विकल्प—doubting and deliberating! BUDDHI is the faculty of निश्चय—decisive certainty! AHANKARA is અભિमान—the ego-sense of 'I am the doer'! And CHITTA is the storehouse of memory and contemplation!'",
        "s4_ta": "'அந்தக்கரணத்தின் நான்கு பிரிவுகளைக் கேளுங்கள்: சங்கல்ப-விகல்பம் செய்வது மனம்! ஒன்றை உறுதியாக நிச்சயிப்பது புத்தி! நான் செய்கிறேன் என அபிமானம் கொள்வது அகங்காரம்! நினைவுகளைத் தொகுத்துச் சிந்திப்பது சித்தம்!'",
        "s5_en": "Mapping the three states—Jagrat (Waking), Svapna (Dream), and Sushupti (Deep Sleep)—and the three Gunas—Sattva (purity, kindness, wisdom), Rajas (desire, restlessness), and Tamas (delusion, sloth)—the Acharya proclaimed the climax: 'All these twenty-four cosmic principles are merely the Kshetra—the inert Field! The Consciousness that knows this entire Field without being any part of it is the KSHETRAJNA—and that Kshetrajna is none other than Paramatman!'",
        "s5_ta": "விழிப்பு, கனவு, உறக்கம் ஆகிய மூன்று அவஸ்தைகளையும், சத்வ, ரஜோ, தமோ குணங்களையும் விளக்கிய ஆச்சாரியர் முடிவான சத்தியத்தை முழங்கினார்: 'இருபத்து நான்கு தத்துவங்களைக் கொண்ட இவ்வுடல் வெறும் க்ஷேத்திரம் (வயல்) மட்டுமே! இவற்றில் எதுவாகவும் இல்லாமல், இவையனைத்தையும் சாட்சியாக அறிகின்ற க்ஷேத்ரஜ்ஞனே பரமாத்மா!'",
        "s6_en": "Seeing the body clearly as an assembly of elements and the self as the untouched Witness—Purusha—the disciples dropped all bodily anxiety and rested in pure awareness.",
        "s6_ta": "உடலைப் பஞ்ச பூதங்களின் சேர்க்கையாகவும், தன்னை அதனை அறியும் தூய க்ஷேத்ரஜ்ஞ புருஷனாகவும் நேரில் உணர்ந்த சீடர்கள் தேகாபிமானம் நீங்கிப் பேரமைதியில் ஆழ்ந்தனர்.",
        "s7_en": "Thus the Shariraka Upanishad provides the razor-sharp Tattva-Viveka by which the seeker separates the immortal Spirit from the mortal frame and attains liberation!",
        "s7_ta": "இவ்வாறு சாரீரக உபநிடதம், அழியும் உடலிலிருந்து அழியாத ஆத்மாவைப் பிரித்தறியும் தத்துவ விவேகத்தை அருளி மோட்சப் பெருவழியைக் காட்டுகிறது!"
    },
    {
        "story_id": "SAMANYA_14_EKAKSHARA_69",
        "muktika_number": 69,
        "upanishad_sanskrit": "एकाक्षरोपनिषद्",
        "upanishad_iast": "Ekākṣaropaniṣad",
        "upanishad_tamil": "ஏகாக்ஷர உபநிடதம்",
        "upanishad_english": "Ekakshara Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Hymn of the One Imperishable Syllable: The Cosmic Autobiography of the Self",
        "story_title_tamil": "ஓரெழுத்துப் பரம்பொருளின் விஸ்வரூப கீதம்: ஏகாக்ஷர உபநிடதம்!",
        "characters": [
            "The Ekakshara Purusha / Hiranyagarbha-Atman (Speaking in the first person as the One Imperishable Syllable pervading all creation)",
            "Contemplative Rishis of the Krishna Yajur Veda (Chanting the 13 cosmic verses around the altar)"
        ],
        "mahavakya_sanskrit": "एकस्त्वमेवासि न च द्वितीयस्तुर्यं पदं त्वं हि गुहाशयानाम् । त्वमेक्षरं परमं वेदितव्यं त्वमस्य विश्वस्य परं निधानम् ॥",
        "mahavakya_tamil_translit": "ஏகஸ்த்வமேவாஸி ந ச த்விதீயஸ்துர்யம் பதம் த்வம் ஹி குஹாஸயானாம் | த்வமக்ஷரம் பரமம் வேதிதவ்யம் த்வமஸ்ய விஸ்வஸ்ய பரம் நிதானம் ||",
        "mahavakya_meaning_english": "Thou alone art the One without a second; Thou art the Turiya state hidden in the cave of all hearts! Thou art the Supreme Imperishable Syllable (Ekakshara), the ultimate resting place of the universe!",
        "mahavakya_meaning_tamil": "இரண்டற்ற ஏகப் பரம்பொருள் நீயே; எல்லா உயிர்களின் இதயக் குகையிலும் உறையும் துரீயப் பதம் நீயே! அறியத்தக்க பரம ஏகாக்ஷரமும், பிரபஞ்சத்தின் இறுதிப் புகலிடமும் நீயே!",
        "philosophical_theme": "The thirteen-verse cosmic hymn to the Ekakshara (OM / The Imperishable Self) as the Womb of all elements, the Protector, the Rain-Cloud, the Sacrifice, and the Turiya Witness.",
        "setting_specifics": "A high mountain fire-altar at dawn where thirteen Vedic Rishis chant in unison as the golden solar orb rises.",
        "metaphor_highlight": "Ekakshara (The Single Imperishable Syllable OM), the Cosmic Rain-Cloud showering Soma, the Navel of Immortality, and the Unborn Calf supporting the heavens.",
        "s1_en": "In the poetic Ekakshara Upanishad (#69 in the Muktika canon, from the Krishna Yajur Veda), the Rishis behold the Supreme Reality not as a distant abstraction, but as the Ekakshara—the Single Imperishable Syllable OM—that speaks as the living Heart of the cosmos!",
        "s1_ta": "முக்திக வரிசையில் 69-ஆவது உபநிடதமாகத் திகழும் கிருஷ்ண யஜுர் வேதத்தின் 'ஏகாக்ஷர உபநிடதத்தில்', ஓரெழுத்துப் பரம்பொருளான ஓங்காரமே (ஏகாக்ஷரமே) பிரபஞ்சம் அனைத்தின் ஆத்மாவாக நின்று பேசும் ஞான கீதத்தை முனிவர்கள் தரிசிக்கின்றனர்!",
        "s2_en": "'Thou art the Imperishable Source in the Vital Breath! Thou art the Ancient One, the Protector of the world, Lord Brihaspati and King Soma! Thou art the Sacrifice, the Sacrificer, and the Sacred Fire that bears the offering to the gods!'",
        "s2_ta": "'பிராணனுக்குள் உறையும் அழியாத அக்ஷரம் நீயே! உலகைக் காக்கும் பழமையான தலைவனும், பிரகஸ்பதியும், சோமனும் நீயே! யக்ஞமும், யக்ஞம் செய்பவனும், தேவர்களுக்கு ஆஹுதியைச் சுமந்து செல்லும் அக்னியும் நீயே!'",
        "s3_en": "'Sitting in the chariot of the sun, Thou shinest across the heavens! As the dark rain-cloud filled with life-giving water, Thou roarst with thunder and showerest sweet rain upon the earth so that all herbs, grains, and creatures may live!'",
        "s3_ta": "'சூரியத் தேரில் அமர்ந்து விண்ணில் ஒளிர்பவன் நீயே! நீருண்ட கார்மேகமாய் இடி முழங்கி, பூமியில் அமுத மழையைப் பொழிந்து பயிர்களையும் உயிர்களையும் வாழ வைக்கும் தந்தையும் நீயே!'",
        "s4_en": "'From Thee were born the Rig, the Yajus, the Saman, and the Atharvan! Thou art the Golden Embryo—Hiranyagarbha—born before the worlds, the single hub in which all the spokes of the cosmic wheel are fastened!'",
        "s4_ta": "'ரிக், யஜுர், சாம, அதர்வண வேதங்கள் உன்னிடமிருந்தே தோன்றின! உலகங்களுக்கு முன்பே தோன்றிய ஹிரண்யகர்ப்பனும், பிரபஞ்சச் சக்கரத்தின் ஆரக்கால்கள் அனைத்தும் பொருந்தியிருக்கும் மையக் குமிழும் நீயே!'",
        "s5_en": "Then rings the supreme non-dual declaration of the Ekakshara Upanishad: 'Ekas tvam evasi na cha dvitiyah, turyam padam tvam hi guhashayanam! Thou alone art the One without a second! Thou art the Fourth State—Turiya—dwelling in the secret cave of every heart!'",
        "s5_ta": "அப்போது ஏகாக்ஷர உபநிடதத்தின் அத்வைத முழக்கம் ஒலிக்கிறது: 'ஏகஸ்த்வமேவாஸி ந ச த்விதீயஃ, துர்யம் பதம் த்வம் ஹி குஹாஸயானாம்! இரண்டற்ற ஏகப் பரம்பொருள் நீயே! எல்லா உயிர்களின் இதயக் குகையிலும் உறையும் நான்காவது துரீயப் பதமும் நீயே!'",
        "s6_en": "'Thou art the Mother, the Father, the Kinsman, and the Guru! Thou art the Witness free from old age and death; knowing Thee as one's own Self, the wise cut asunder the knot of ignorance!'",
        "s6_ta": "'தாயும், தந்தையும், உறவும், குருவும் நீயே! மூப்பும் மரணமும் அற்ற சாட்சியான உன்னைத் தன் ஆத்மாவாகவே உணரும் ஞானி, அறியாமை முடிச்சை அறுத்து முக்தி அடைகிறான்!'",
        "s7_en": "Whoever recites these thirteen sacred verses of the Ekakshara Upanishad merges his breath and mind into the One Imperishable Syllable and attains eternal peace!",
        "s7_ta": "பதின்மூன்று மந்திரங்கள் கொண்ட இந்த ஏகாக்ஷர உபநிடதத்தை ஓதித் தியானிப்பவன், அந்த ஓரெழுத்துப் பிரணவப் பரம்பொருளோடு ஒன்றாகி நித்திய சாந்தியை அடைகிறான்!"
    }
])


SAMANYA_SPECS.extend([
    {
        "story_id": "SAMANYA_15_AKSHI_72",
        "muktika_number": 72,
        "upanishad_sanskrit": "अक्ष्युपनिषद्",
        "upanishad_iast": "Akṣyupaniṣad",
        "upanishad_tamil": "அக்ஷி உபநிடதம்",
        "upanishad_english": "Akshi Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Sankriti & The Sun-God on Chakshushmati Vidya & The Seven Stages of Enlightenment",
        "story_title_tamil": "சங்கிருதி முனிவரும் சூரிய பகவானும்: நேத்திர வித்தையும் ஞானத்தின் ஏழு படிகளும் (அக்ஷி உபநிடதம்)!",
        "characters": [
            "Maharishi Sankriti (Worshiping Lord Surya with the Chakshushmati Vidya to heal both physical and spiritual sight)",
            "Bhagavan Surya Narayana (The Solar Deity who teaches both eye-healing light and the 7 Jnana-Bhumikas)"
        ],
        "mahavakya_sanskrit": "असतो मा सद्गमय तमसो मा ज्योतिर्गमय मृत्योर्मामृतं गमय । अहमेवाक्षरं ब्रह्म वासुदेवाख्यमद्वयम् ॥",
        "mahavakya_tamil_translit": "அஸதோ மா ஸத்கமய தமஸோ மா ஜ்யோதிர்கமய ம்ருத்யோர்மாம்ருதம் கமய | அஹமேவாக்ஷரம் ப்ரஹ்ம வாஸுதேவாக்யமத்வயம் ||",
        "mahavakya_meaning_english": "Lead me from the unreal to the Real, from darkness to Light, from death to Immortality! I alone am the Imperishable Non-Dual Brahman named Vasudeva!",
        "mahavakya_meaning_tamil": "பொய்மையிலிருந்து என்னை மெய்மைக்கு அழைத்துச் செல்; இருளிலிருந்து ஒளிக்கு அழைத்துச் செல்; மரணத்திலிருந்து அமரத்துவத்திற்கு அழைத்துச் செல்! இரண்டற்ற வாசுதேவப் பிரம்மம் நானே!",
        "philosophical_theme": "Part 1: Chakshushmati Vidya (The sacred solar invocation that purifies sight so none in one's lineage ever goes blind); Part 2: Ascent through the Seven Jnana-Bhumikas to non-dual Vasudeva.",
        "setting_specifics": "A sunlit river ghat at dawn where Sage Sankriti offers Arghya to the rising Sun and receives the vision of the Cosmic Eye.",
        "metaphor_highlight": "The Sun as the Eye of the Universe (Chakshuh Suryah), Two Warriors fighting on a battlefield, and Climbing the Seven Rungs of the Tower of Wisdom.",
        "s1_en": "In the Akshi Upanishad (#72 in the Muktika canon, from the Krishna Yajur Veda—'The Upanishad of the Eye'), Maharishi Sankriti stood waist-deep in the sacred river at dawn, worshiping Bhagavan Surya Narayana with the Chakshushmati Vidya: 'O Sun-God! Thou art the radiant Eye of all worlds! Lead me from the unreal to the Real, from darkness to Light, from death to Immortality!'",
        "s1_ta": "முக்திக வரிசையில் 72-ஆவது உபநிடதமாகத் திகழும் கிருஷ்ண யஜுர் வேதத்தின் 'அக்ஷி உபநிடதத்தில்' (நேத்திர உபநிடதம்), மகரிஷி சங்கிருதி உதய சூரியனை வணங்கி 'சாக்ஷுஷ்மதி வித்தை'யால் துதித்தார்: 'சூரிய பகவானே! உலகின் கண்ணாக ஒளிர்பவர் நீரே! பொய்மையிலிருந்து மெய்மைக்கும், இருளிலிருந்து ஒளிக்கும், மரணத்திலிருந்து அமிர்தத்திற்கும் என்னை அழைத்துச் செல்வீராக!'",
        "s2_en": "Pleased by his devotion, Lord Surya appeared in golden splendor and blessed the first part of the Upanishad: 'Whoever recites this Chakshushmati Vidya daily with purity shall be cured of all afflictions of the eyes, and in his family no one shall ever be born blind!' Then Surya added: 'Yet, O Sankriti, outer sight is only the beginning—now receive from Me the Eye of Supreme Brahmavidya!'",
        "s2_ta": "மகிழ்ந்த சூரிய பகவான் நேரில் தோன்றி வரமளித்தார்: 'இந்தச் சாக்ஷுஷ்மதி வித்தையை நித்தியம் ஓதுபவருக்குக் கண் நோய்கள் ஒருபோதும் அண்டாது; அவரது குலத்தில் எவரும் பார்வையற்றவராகப் பிறக்க மாட்டார்! ஆயினும் சங்கிருதி, புறக்கண் பார்வை தொடக்கம் மட்டுமே; இப்போது அகக்கண்ணைத் திறக்கும் பிரம்ம வித்தையைக் கேள்!'",
        "s3_en": "Lord Surya mapped the Seven Stages of Enlightenment—Sapta Yoga-Bhumikas: First is Subheccha, the dawning wish: 'Why do I stand steeped in ignorance? Let me study the scriptures and seek the wise!' Second is Vicharana, earnest inquiry into Truth alongside detachment and virtuous conduct! Third is Asamsanga (Tanumanasa), where the mind grows thin and transparent as attachment to sense-objects fades!",
        "s3_ta": "சூரிய பகவான் ஞானத்தின் ஏழு படிகளை (சப்த யோக பூமிகைகளை) உபதேசித்தார்: முதல் படி 'சுபேச்சை' — நான் ஏன் மூடனாய் இருக்கிறேன், சாஸ்திரங்களையும் மகாத்மாக்களையும் நாடுவேன் என்ற நல்விருப்பம்! இரண்டாம் படி 'விசாரணை' — வைராக்கியத்துடனும் சதாசாரத்துடனும் சத்தியத்தை ஆராய்தல்! மூன்றாம் படி 'அஸம்ஸங்கம்' — பொருட்களின் மேல் உள்ள பற்று நீங்கி மனம் மெலிதல்!",
        "s4_en": "Even if a seeker passes away while striving on the first three rungs—like a fearless warrior falling on the battlefield—he is reborn in a pure yogic home and swiftly climbs to the Fourth Stage: Sattvapatti, where the entire world is seen as a dream and the truth of non-duality dawns!",
        "s4_ta": "போர்க்களத்தில் வீரமரணம் அடைந்த வீரன் சுவர்க்கம் செல்வது போல், முதல் மூன்று படிகளில் முயலும் சாதகன் இடையில் உடலை விட்டாலும் அடுத்த பிறவியிலேயே யோக குலத்தில் பிறந்து நான்காம் படியான 'சத்வாபத்தி'யை அடைகிறான்; அங்கே உலகம் கனவு என்பதும் பிரம்மம் ஒன்றே சத்தியம் என்பதும் நேரில் விளங்குகிறது!",
        "s5_en": "Beyond the fourth lie the three stages of Jivanmukti: the Fifth (Asamsakti), the Sixth (Padarthabhavana, where one wakes only when nudged by others), and the Seventh—Turiya—where all distinction between waking and samadhi dissolves! There the Yogi proclaims: 'Aham evaksharam Brahma Vasudevakhyam advayam—I alone am the Imperishable Non-Dual Brahman named Vasudeva!'",
        "s5_ta": "நான்காம் படியைக் கடந்தவன் ஐந்தாம், ஆறாம் படிகளில் ஜீவன்முக்தனாய் உலவி, இறுதியில் ஏழாம் படியான 'துரீய' நிலையை அடைகிறான்! அங்கே யோகி முழங்குகிறான்: 'அஹமேவாக்ஷரம் ப்ரஹ்ம வாஸுதேவாக்யமத்வயம் — வாசுதேவன் எனப்படும் அழியாத இரண்டற்ற பிரம்மம் நானே!'",
        "s6_en": "Bathed in the golden light of the Rising Sun, Maharishi Sankriti beheld both his physical eyes and his inner eye of wisdom merged into the one self-luminous Aditya-Purusha.",
        "s6_ta": "உதய சூரியனின் பொன்னொளியில் நனைந்த சங்கிருதி முனிவர், புறக்கண்ணும் அகக்கண்ணும் ஒன்றாகி ஆதித்ய புருஷனான வாசுதேவ ஜோதியிலேயே இரண்டறக் கலந்தார்.",
        "s7_en": "Whoever studies this Akshi Upanishad receives both unfailing physical vision and the supreme Eye of Non-Dual Self-Knowledge!",
        "s7_ta": "இந்த அக்ஷி உபநிடதத்தை ஓதித் தியானிப்பவர், குறையாத புறக்கண் ஒளியையும், பிறவிப் பிணி தீர்க்கும் ஞானக் கண் ஒளியையும் ஒருங்கே பெறுகிறார்!"
    },
    {
        "story_id": "SAMANYA_16_ADHYATMA_73",
        "muktika_number": 73,
        "upanishad_sanskrit": "अध्यात्मोपनिषद्",
        "upanishad_iast": "Adhyātmopaniṣad",
        "upanishad_tamil": "அத்யாத்ம உபநிடதம்",
        "upanishad_english": "Adhyatma Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Apantaratamas & The Unborn Antaryamin: Dissolving the Pot into Clay",
        "story_title_tamil": "அபாந்தரதமஸ் முனிவரும் அந்தர்யாமி தத்துவமும்: குடத்தை மண்ணில் ஒடுக்கும் அத்யாத்ம உபநிடதம்!",
        "characters": [
            "Maharishi Apantaratamas (The ancient Vedic seer and precursor of Vyasa who revealed the Adhyatma Upanishad)",
            "Narayana / Antaryamin (The Unborn Inner Controller dwelling within the cave of the body)"
        ],
        "mahavakya_sanskrit": "अन्तर्यामी स एवात्मा... देहाभिमानंगलिते विज्ञाते परमात्मनि । यत्र यत्र मनो याति तत्र तत्र समाधयः ॥",
        "mahavakya_tamil_translit": "அந்தர்யாமீ ஸ ஏவாத்மா... தேஹாபிமானே கலிதே விஜ்ஞாதே பரமாத்மனி | யத்ர யத்ர மனோ யாதி தத்ர தத்ர ஸமாதயஃ ||",
        "mahavakya_meaning_english": "When identification with the body melts away and the Supreme Self is realized, wherever the mind goes, there itself is Samadhi!",
        "mahavakya_meaning_tamil": "தேகாபிமானம் கரைந்து பரமாத்மா அறியப்பட்ட பின், மனம் எங்கெல்லாம் செல்கிறதோ அங்கெல்லாம் சமாதியே நிலவுகிறது!",
        "philosophical_theme": "Adhyaropa-Apavada and Laya-Yoga (Dissolving the gross into the subtle); the famous verse 'Dehabhimane galite vijnate paramatmani, yatra yatra mano yati tatra tatra samadhayah'.",
        "setting_specifics": "A quiet Himalayan rock cave where Maharishi Apantaratamas meditates before a clay pot and a steady oil lamp.",
        "metaphor_highlight": "Pot and Clay (Ghata-Mrittika), Gold and Ear-rings (Kundala-Suvarna), Mother-of-Pearl and Silver (Shukti-Rajata), and 'Wherever the mind goes, there is Samadhi'.",
        "s1_en": "In the sublime Adhyatma Upanishad (#73 in the Muktika canon, belonging to the Shukla Yajur Veda and revealed by the ancient Rishi Apantaratamas), the teaching opens from within the very cave of the body: 'Antah sharire nihito guhayam ajah eko nityah—Hidden within the cave of the body dwells the One Unborn, Eternal Witness!'",
        "s1_ta": "முக்திக வரிசையில் 73-ஆவது உபநிடதமாகத் திகழும் சுக்ல யஜுர் வேதத்தின் 'அத்யாத்ம உபநிடதம்', அபாந்தரதமஸ் முனிவரால் அருளப்பட்டது! 'அந்தஃ சரீரே நிஹிதோ குஹாயாம் அஜ ஏகோ நித்யஃ — உடலின் இதயக் குகைக்குள் பிறப்பற்றதும் நித்தியமானதுமான அந்த ஏகப் பரம்பொருள் உறைகிறது!' என்று உபதேசம் தொடங்குகிறது.",
        "s2_en": "Earth is His body, yet Earth knows Him not; Water, Fire, Wind, Space, Mind, and Intellect are His bodies, yet none of them know Him—He alone rules them all from within as the Immortal Antaryamin! Why then does a human being suffer? Only because he foolishly superimposes 'I' and 'mine' upon this passing bundle of flesh and thoughts!",
        "s2_ta": "பூமி, நீர், நெருப்பு, காற்று, ஆகாயம், மனம், புத்தி ஆகிய அனைத்திற்கும் உள்ளே நின்று அவற்றை இயக்கும் அந்தர்யாமி அவரே! மனிதன் ஏன் துன்புறுகிறான்? நிலையற்ற இந்த உடலையும் மனதையும் 'நான்', 'எனது' என்று தவறாகக் கற்பனை செய்து கொள்வதாலேயே சம்சாரத் துயரில் உழல்கிறான்!",
        "s3_en": "How should the wise seeker dissolve this false superimposition? Maharishi Apantaratamas taught the practice of Pravipaka—merging the effect back into its cause: 'Just as a clay pot is seen to be nothing but clay, and golden earrings nothing but gold, and dream-elephants nothing but the dreamer's own mind, merge the gross world into Virat, Virat into Hiranyagarbha, Hiranyagarbha into Ishvara, and Ishvara into Pure Witness-Consciousness!'",
        "s3_ta": "இந்த மயக்கத்தை நீக்குவது எப்படி? காரியத்தைக் காரணத்தில் ஒடுக்கும் 'பிரவிலாபன' தியானத்தை முனிவர் போதித்தார்: 'மண் குடத்தை மண்ணாகவும், பொன் குண்டலங்களைப் பொன்னாகவும், சிப்பியில் தோன்றும் வெள்ளியைச் சிப்பியாகவும் காண்பது போல், ஸ்தூல உலகை விராட் புருஷனிலும், அதனை ஹிரண்யகர்ப்பனிலும், ஈஸ்வரனிலும், இறுதியில் தூய சாக்ஷி சைதன்யத்திலும் ஒடுக்குவாயாக!'",
        "s4_en": "Addressing the restless mind directly, the Sage commanded: 'Go, O mind, into the forest of sense-objects if you wish, or sit quiet in a cave—what is that to Me? For I am the Partless Consciousness! I have no birth, no old age, no sorrow, and no work to perform!'",
        "s4_ta": "அலைபாயும் மனதை நோக்கி ஞானி கூறுகிறான்: 'மனமே! நீ எங்கே வேண்டுமானாலும் ஓடு அல்லது அடங்கி இரு; அதனால் எனக்கு என்ன? நான் அவயவங்களற்ற தூய சைதன்யம்! எனக்குப் பிறப்புமில்லை, மூப்புமில்லை, துக்கமுமில்லை!'",
        "s5_en": "Then shines the most celebrated verse of the Adhyatma Upanishad: 'Dehabhimane galite vijnate paramatmani, yatra yatra mano yati tatra tatra samadhayah! When identification with the body melts away and the Supreme Self is realized, wherever the mind goes, there itself is Samadhi! Then the Knot of the Heart is broken, all doubts are cut asunder, and all karmas perish!'",
        "s5_ta": "அப்போது அத்யாத்ம உபநிடதத்தின் மகுட சுலோகம் ஒலிக்கிறது: 'தேஹாபிமானே கலிதே விஜ்ஞாதே பரமாத்மனி, யத்ர யத்ர மனோ யாதி தத்ர தத்ர ஸமாதயஃ! உடற்பற்று கரைந்து பரமாத்மா நேரில் உணரப்பட்ட பின், மனம் எங்கெல்லாம் செல்கிறதோ அங்கெல்லாம் சமாதியே நிலவுகிறது! அப்போது இதய முடிச்சு அவிழ்ந்து, ஐயங்கள் அனைத்தும் அறுபட்டு, கர்மங்கள் அனைத்தும் க்ஷயமாகின்றன!'",
        "s6_en": "For such a Jivanmukta, whether his body is worshiped with flowers by gods or pelted with stones by the ignorant, his inner sky remains as serene as the ocean depths.",
        "s6_ta": "அத்தகைய ஜீவன்முக்தனின் உடலை உலகோர் மலர் தூவிப் பூஜித்தாலும் சரி, நிந்தித்தாலும் சரி, அவனது அக ஆகாயம் சமுத்திரத்தின் ஆழம் போல் என்றும் சலனமின்றி அமைதியாகத் திகழ்கிறது.",
        "s7_en": "Passed down from Apantaratamas to Brahma, Ghora Angirasa, Raikva, and Rama, this Adhyatma Upanishad bestows immediate liberation in this very life!",
        "s7_ta": "அபாந்தரதமஸ் முனிவரிடமிருந்து பிரம்மா, கோர ஆங்கிரஸர், ரைக்கவர், ஸ்ரீராமர் வழியே வந்த இந்த அத்யாத்ம உபநிடதம், இப்பிறவியிலேயே ஜீவன்முக்திப் பேற்றினை அருள்கிறது!"
    },
    {
        "story_id": "SAMANYA_17_SAVITRI_75",
        "muktika_number": 75,
        "upanishad_sanskrit": "सावित्र्युपनिषद्",
        "upanishad_iast": "Sāvitryupaniṣad",
        "upanishad_tamil": "சாவித்ரி உபநிடதம்",
        "upanishad_english": "Savitri Upanishad",
        "veda": "Sama Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Cosmic Couplets of Savitar & Savitri: The Four Quarters of the Gayatri",
        "story_title_tamil": "சவிதாவும் சாவித்ரியும்: பிரபஞ்ச இரட்டைகளின் ஐக்கியமும் காயத்ரியின் நான்கு பாதங்களும்!",
        "characters": [
            "The Sama Veda Rishi of Savitri Vidya (Revealing the cosmic couples of Savitar and Savitri)",
            "Savitar & Savitri (The Cosmic Impeller and the Creative Power united in the Gayatri Mantra)"
        ],
        "mahavakya_sanskrit": "कः सविता का सावित्री... मन एव सविता वाक् सावित्री यत्र ह्येव मनस्तद्वै वाग्यत्र वै वाक्तन्मन इति ॥",
        "mahavakya_tamil_translit": "கஃ ஸவிதா கா ஸாவித்ரீ... மன ஏவ ஸவிதா வாக் ஸாவித்ரீ யத்ர ஹ்யேவ மனஸ்தத்வை வாக்யத்ர வை வாக்தன்மன இதி ||",
        "mahavakya_meaning_english": "Who is Savitar and who is Savitri? Mind indeed is Savitar and Speech is Savitri; where Mind is, there is Speech, and where Speech is, there is Mind—both are one in the Fourth Foot of Gayatri!",
        "mahavakya_meaning_tamil": "சவிதா யார்? சாவித்ரி யார்? மனமே சவிதா, வாக்கே சாவித்ரி; எங்கே மனம் உள்ளதோ அங்கே வாக்கு உள்ளது, எங்கே வாக்கு உள்ளதோ அங்கே மனம் உள்ளது — இரண்டும் காயத்ரியின் துரீய பாதத்தில் ஒன்றே!",
        "philosophical_theme": "The Nine Cosmic Dyads (Mithunas) of Savitar and Savitri (Mind & Speech, Fire & Earth, Wind & Sky, Sun & Heaven, Moon & Stars, Day & Night, Heat & Cold, Cloud & Rain, Prana & Food) culminating in the Turiya Pada of Gayatri.",
        "setting_specifics": "A sunlit Sama Veda river ghat at Sandhya-vandana where sages offer water to the golden solar orb.",
        "metaphor_highlight": "Nine Cosmic Couples (Savitar & Savitri Mithunas) and the Four-Footed Swan of Gayatri resting on the Transcendental Fourth Foot (Paroraja).",
        "s1_en": "In the luminous Savitri Upanishad (#75 in the Muktika canon, from the Sama Veda), the sages stood at dawn performing Sandhya-vandana and asked the foundational question of the Gayatri mystery: 'Kah Savita? Ka Savitri? Who truly is Savitar, the Cosmic Impeller, and who is Savitri, His divine creative power?'",
        "s1_ta": "முக்திக வரிசையில் 75-ஆவது உபநிடதமாகத் திகழும் சாம வேதத்தின் 'சாவித்ரி உபநிடதத்தில்', வைகறை சந்தியாவந்தன வேளையில் முனிவர்கள் கேட்டனர்: 'கஃ ஸவிதா? கா ஸாவித்ரீ? அனைத்தையும் தூண்டும் சவிதா யார்? அவரது தெய்வீக சக்தியான சாவித்ரி யார்?'",
        "s2_en": "The Acharya revealed the nine cosmic dyads—Mithunas—pervading both microcosm and macrocosm: 'First, Mind indeed is Savitar, and Speech is Savitri! Second, Agni (Fire) is Savitar, and Prithivi (Earth) is Savitri! Third, Vayu (Wind) is Savitar, and Antariksha (Sky) is Savitri! Where the one is, there unfailingly is the other!'",
        "s2_ta": "அண்டத்திலும் பிண்டத்திலும் இணைந்து நிற்கும் ஒன்பது தெய்வீக இரட்டைகளை (மிதுனங்களை) ஆச்சாரியர் விளக்கினார்: 'முதலில் மனமே சவிதா, வாக்கே சாவித்ரி! இரண்டாவது அக்னியே சவிதா, பூமியே சாவித்ரி! மூன்றாவது வாயுவே சவிதா, அந்தரிக்ஷமே சாவித்ரி! இவை ஒன்றை விட்டு ஒன்று பிரிவதில்லை!'",
        "s3_en": "'Fourth, Aditya (the Sun) is Savitar, and Dyaus (Heaven) is Savitri! Fifth, Chandramas (the Moon) is Savitar, and the Stars (Nakshatras) are Savitri! Sixth, Day is Savitar, and Night is Savitri! Seventh, Warmth is Savitar, and Coolness is Savitri! Eighth, the Cloud is Savitar, and Rain is Savitri! And ninth, within the body, Prana (Vital Breath) is Savitar, and Annam (Food) is Savitri!'",
        "s3_ta": "'நான்காவது சூரியனே சவிதா, சுவர்க்கமே சாவித்ரி! ஐந்தாவது சந்திரனே சவிதா, நட்சத்திரங்களே சாவித்ரி! ஆறாவது பகலே சவிதா, இரவே சாவித்ரி! ஏழாவது வெப்பமே சவிதா, குளிர்ச்சியே சாவித்ரி! எட்டாவது மேகமே சவிதா, மழையே சாவித்ரி! ஒன்பதாவது உடலுக்குள் பிராணனே சவிதா, அன்னமே சாவித்ரி!'",
        "s4_en": "Having shown how the entire dual universe of energy and matter is the dance of Savitar and Savitri, the Acharya united them into the three Vedic Gayatri padas: 'Bhur, Bhuvah, Suvah—Earth, Sky, and Heaven form the first three feet of Savitri!'",
        "s4_ta": "சக்தியும் பொருளும் இணைந்த இப்பிரபஞ்சம் அனைத்தும் சவிதா-சாவித்ரியின் திருநடனமே என்று காட்டிய ஆச்சாரியர், 'பூஃ, புவஃ, ஸுவஃ' என்னும் மூன்று உலகங்களையும் காயத்ரியின் மூன்று பாதங்களாக இணைத்துக் காட்டினார்!",
        "s5_en": "Then rings the supreme climax of the Savitri Upanishad: 'Beyond these three manifest worlds shines the Fourth Foot of Gayatri—Paroraja, transcendental, self-luminous, where Savitar and Savitri merge into the One Non-Dual Atman: Tat Savitur Varenyam Bhargo Devasya Dhimahi!'",
        "s5_ta": "அப்போது சாவித்ரி உபநிடதத்தின் சிகர மந்திரம் ஒலிக்கிறது: 'மூன்று உலகங்களையும் கடந்து, ரஜோ குணத்திற்கு அப்பாற்பட்டு (பரோரஜஸாய்) ஒளிரும் நான்காவது துரீய பாதத்தில் சவிதாவும் சாவித்ரியும் ஒன்றாகக் கலக்கின்றனர் — தத் ஸவிதுர் வரேண்யம் பர்கோ தேவஸ்ய தீமஹி!'",
        "s6_en": "Meditating upon the Bala, Atibala, and Savitri mantras with the Rishi Vishvamitra and Gayatri metre united in the heart, the seeker's mind is impelled directly into the Solar Brahman.",
        "s6_ta": "விஸ்வாமித்திர ரிஷியைச் சிரசிலும், காயத்ரி சந்தஸை நாவிலும், சவிதா தேவதையை இதயத்திலும் நிறுத்தித் தியானித்த சாதகர்கள், தம் அறிவை இயக்கும் சுய ஒளியே பிரம்மம் என உணர்ந்தனர்.",
        "s7_en": "Whoever contemplates this Savitri Upanishad becomes radiant with Brahma-Tejas, crosses beyond the pairs of opposites, and attains the immortal abode of Savitar!",
        "s7_ta": "இந்தச் சாவித்ரி உபநிடதத்தை ஓதித் தியானிப்பவன் பிரம்ம தேஜஸ் பெற்று, இருமைகளைக் கடந்து சவிதாவின் அமிர்தப் பெருவெளியில் நிலைபெறுகிறான்!"
    },
    {
        "story_id": "SAMANYA_18_ATMA_76",
        "muktika_number": 76,
        "upanishad_sanskrit": "आत्मोपनिषद्",
        "upanishad_iast": "Ātmopaniṣad",
        "upanishad_tamil": "ஆத்ம உபநிடதம்",
        "upanishad_english": "Atma Upanishad",
        "veda": "Atharva Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Maharishi Angiras on the Threefold Purusha: Atman, Antaratman & Paramatman",
        "story_title_tamil": "அங்கிரஸ முனிவர் அருளிய மூன்று புருஷர்கள்: ஆத்மா, அந்தராத்மா மற்றும் பரமாத்மா (ஆத்ம உபநிடதம்)!",
        "characters": [
            "Maharishi Angiras (The great Atharva Vedic sage expounding the threefold distinction of Atman, Antaratman, and Paramatman)",
            "Assembly of Yogis and Seekers (Learning how the Potter's Wheel and Space in Pots illustrate the Partless Paramatman)"
        ],
        "mahavakya_sanskrit": "अथाङ्गिरास्त्रिविधः पुरुषस्तद्यथा बाह्यात्मा अन्तरात्मा परमात्मा चेति । निष्कलंकः... स एव परमात्मा ॥",
        "mahavakya_tamil_translit": "அதாங்கிராஸ்த்ரிவிதஃ புருஷஸ்தத்யதா பாஹ்யாத்மா அந்தராத்மா பரமாத்மா சேதி | நிஷ்கலங்கஃ... ஸ ஏவ பரமாத்மா ||",
        "mahavakya_meaning_english": "Maharishi Angiras declared the Threefold Purusha: the Outer Self (Atman), the Inner Self (Antaratman), and the Supreme Self (Paramatman)—spotless, partless, non-dual Consciousness!",
        "mahavakya_meaning_tamil": "மகரிஷி அங்கிரஸர் புருஷனை மூன்று நிலைகளில் விளக்கினார்: பாஹ்யாத்மா (உடல்), அந்தராத்மா (ஜீவன்) மற்றும் பரமாத்மா (களங்கமற்ற, அவயவங்களற்ற தூய பிரம்மம்)!",
        "philosophical_theme": "Clear pedagogical triad of Atman (Gross Body), Antaratman (Subtle Jiva experiencing the states), and Paramatman (The Changeless Turiya Brahman), illustrated with thread in cloth and space in pots.",
        "setting_specifics": "Maharishi Angiras's Atharva Vedic forest ashram with a handloom weaving white cotton cloth and clay pots arranged by the fire.",
        "metaphor_highlight": "Threefold Purusha (Atman, Antaratman, Paramatman), Threads forming a Woven Cloth (Tantu-Pata), and Space inside broken Pots (Ghatakasha).",
        "s1_en": "In the lucid Atma Upanishad (#76 in the Muktika canon, belonging to the Atharva Veda), Maharishi Angiras addressed his disciples around the sacred fire and proclaimed: 'Trividhah Purushah—To guide the seeker from the gross to the supreme, the wise speak of the Purusha in three aspects: Atman (the Outer Self), Antaratman (the Inner Self), and Paramatman (the Supreme Self)!'",
        "s1_ta": "முக்திக வரிசையில் 76-ஆவது உபநிடதமாகத் திகழும் அதர்வண வேதத்தின் 'ஆத்ம உபநிடதத்தில்', மகரிஷி அங்கிரஸர் தன் சீடர்களுக்கு உபதேசித்தார்: 'த்ரிவிதஃ புருஷஃ — சாதகர்கள் எளிதில் உணர்வதற்காக புருஷன் மூன்று நிலைகளில் விளக்கப்படுகிறான்: ஆத்மா (புற ஆத்மா), அந்தராத்மா (உள் ஆத்மா) மற்றும் பரமாத்மா (மேலான ஆத்மா)!'",
        "s2_en": "'What is the first—the Outer Atman?' asked the disciples. Angiras replied: 'That which is born of parents, composed of skin, flesh, blood, bone, and hair, which sees, hears, speaks, walks, and perishes in time—this gross physical body that the ignorant call 'I' is the Outer Atman (Bahyatman)!'",
        "s2_ta": "'முதலாவதான புற ஆத்மா (பாஹ்யாத்மா) எது?' என்று சீடர்கள் கேட்டனர். அங்கிரஸர் விளக்கினார்: 'தோல், தசை, இரத்தம், எலும்பு, நகம், மயிர் ஆகியவற்றால் ஆகி, கண்-காது-வாக்கு முதலான கருவிகளுடன் பிறந்து வளர்ந்து மடியும் இந்தப் பருவுடலே (ஸ்தூல சரீரமே) அज्ञானிகளால் நான் எனப்படும் முதல் ஆத்மா!'",
        "s3_en": "'And what is the second—the Antaratman (Inner Self)?' 'That subtle entity which dwells inside the city of the five elements, tastes pleasure and pain, wanders through Waking, Dream, and Deep Sleep, and studies the scriptures, philosophy, music, and logic—that empirical Jiva or Kshetrajna is called the Antaratman!'",
        "s3_ta": "'இரண்டாவதான அந்தராத்மா (உள் ஆத்மா) எது?' 'பஞ்ச பூதங்களால் ஆன இந்த உடலுக்குள் தங்கி, இன்ப-துன்பங்களை நுகர்ந்து, விழிப்பு-கனவு-உறக்கம் ஆகிய நிலைகளில் சுழன்று, சாஸ்திரங்களையும் கலைகளையும் ஆராயும் அந்தச் சூட்சும ஜீவனே (க்ஷேத்ரஜ்ஞனே) அந்தராத்மா எனப்படுகிறான்!'",
        "s4_en": "Then Maharishi Angiras turned to the third and highest: 'And who is the PARAMATMAN—the Supreme Self? He who is worshiped through Pranava and Yoga, who is beyond breath, mind, and senses, unborn, unaging, deathless, fearless, without inside or outside! Just as when a clay pot is broken, the space inside the pot has neither gone anywhere nor come from anywhere, but is forever the boundless sky—so is Paramatman!'",
        "s4_ta": "அடுத்து மூன்றாவதான 'பரமாத்மா'வின் சொரூபத்தை அங்கிரஸர் அருளினார்: 'பிராணாயாமம், பிரத்யாகாரம், தாரணை, தியானம், சமாதி ஆகிய யோக அங்கங்களாலும் பிரணவத்தாலும் அறியப்படுபவன் எவனோ, குடம் உடைந்தவுடன் குட ஆகாயம் எங்கும் போகாமல் மகா ஆகாயமாகவே நிற்பது போல், பிறப்பு-இறப்பு-உள்-புறம் அற்றவன் எவனோ அவனே பரமாத்மா!'",
        "s5_en": "Pointing to a white cotton cloth on a handloom, Angiras gave a classic Advaita illustration: 'Just as a woven cloth is nothing other than the threads composing it, and yet the deluded world speaks of 'cloth' as if it were separate from the threads—even so, this entire universe of Jivas and elements is nothing other than the Non-Dual Paramatman!'",
        "s5_ta": "தறியில் நெய்யப்பட்ட வெள்ளைத் துணியைக் காட்டி முனிவர் விளக்கினார்: 'நூல் இழைகளைத் தவிர்த்துத் துணி என்றொரு பொருள் தனியாக இல்லாதபோதும் உலகம் அதனைத் துணி என்று அழைப்பது போல், பரமாத்மாவைத் தவிர்த்து ஜீவனோ உலகமோ தனியாக இல்லவே இல்லை!'",
        "s6_en": "'Just as the potter's wheel continues to spin for a little while by past momentum even after the pot is finished, the Jivanmukta's body moves peacefully through Prarabdha until it merges in Videhamukti—as pure and traceless as space!'",
        "s6_ta": "'குடம் செய்து முடித்த பின்பும் சக்கரம் பழைய வேகத்தால் சற்று நேரம் சுழன்று அடங்குவது போல், ஜீவன்முக்தன் பிராரப்த கர்மம் முடியும் வரை உலகில் சாந்தமாய் உலவி, விதேக முக்தியில் ஆகாயம் போல் இரண்டறக் கலக்கிறான்!'",
        "s7_en": "Thus concludes the Atma Upanishad of the Atharva Veda: realizing that the Outer Body is not I, and the restless Jiva is only a reflection, abide forever as the Spotless Paramatman!",
        "s7_ta": "அதர்வண வேதத்தின் இந்த ஆத்ம உபநிடதத்தை உணர்ந்து, அழியும் உடலும் மாறும் ஜீவ பாவமும் நீங்கி, நிர்மலமான பரமாத்மாவாகவே நிலைபெறுவோம்!"
    },
    {
        "story_id": "SAMANYA_19_SURYA_71",
        "muktika_number": 71,
        "upanishad_sanskrit": "सूर्योपनिषद्",
        "upanishad_iast": "Sūryopaniṣad",
        "upanishad_tamil": "சூரிய உபநிடதம்",
        "upanishad_english": "Surya Upanishad",
        "veda": "Atharva Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Lord Brahma & Atharvangiras on the Solar Brahman: 'Suryo Atma Jagatas Tasthushashcha'",
        "story_title_tamil": "பிரம்ம தேவரும் அதர்வாங்கிரஸரும்: அசையும் அசையாப் பொருட்களின் ஆத்மாவான சூரியப் பிரம்மம் (சூரிய உபநிடதம்)!",
        "characters": [
            "Lord Pitamaha Brahma (Revealing the Atharvangirasa Surya-Mantra to the Rishis)",
            "Maharishi Atharvangiras (Seer of the Solar Brahman and the Eight-Syllabled Aditya Vidya)",
            "Bhagavan Surya Narayana / Savitar (The Golden Purusha in the Solar Orb)"
        ],
        "mahavakya_sanskrit": "सूर्य आत्मा जगतस्तस्थुषश्च । सूर्याद्भवन्ति भूतानि सूर्येण पालितानि तु । सूर्ये लयं प्राप्नुवन्ति यः सूर्यः सोऽहमेव च ॥",
        "mahavakya_tamil_translit": "ஸூர்ய ஆத்மா ஜகதஸ்தஸ்துஷஸ்ச | ஸூர்யாத் பவந்தி பூதானி ஸூர்யேண பாலிதானி து | ஸூர்யே லயம் ப்ராப்னுவந்தி யஃ ஸூர்யஃ ஸோऽஹமேவ ச ||",
        "mahavakya_meaning_english": "The Sun is the Atman of all that moves and all that stands still! From Surya all beings are born, by Surya they are sustained, and into Surya they dissolve—He who is that Surya, That very One am I!",
        "mahavakya_meaning_tamil": "அசையும் மற்றும் அசையாப் பொருட்கள் அனைத்தின் ஆத்மாவும் சூரியனே! சூரியனிடமிருந்தே உயிர்கள் தோன்றி, சூரியனாலேயே காக்கப்பட்டு, சூரியனிலேயே ஒடுங்குகின்றன — அந்தச் சூரியன் எவனோ அவனே நான்!",
        "philosophical_theme": "Identity of the Cosmic Solar Purusha (Aditya-Antargata Purusha) with the Indwelling Atman ('Yah Suryah So'ham Eva Cha'); the Eight-Syllabled Solar Mantra ('Om Ghrinih Suryah Adityah').",
        "setting_specifics": "A grand Himalayan sunrise altar where Maharishi Atharvangiras and disciples face the rising four-armed golden Surya in his seven-horse chariot.",
        "metaphor_highlight": "The Seven-Horse Single-Wheel Chariot of Time, and the Golden Purusha in the Sun as identical with the Witness in the Heart ('Yah Suryah So'ham Eva Cha').",
        "s1_en": "In the radiant Surya Upanishad (#71 in the Muktika canon, belonging to the Atharva Veda), Lord Brahma imparted the supreme Atharvangirasa Mantra of the Solar Brahman: 'Surya atma jagatas tasthushashcha—The Sun is the very Soul of all that moves and all that stands still!'",
        "s1_ta": "முக்திக வரிசையில் 71-ஆவது உபநிடதமாகத் திகழும் அதர்வண வேதத்தின் 'சூரிய உபநிடதத்தில்', பிரம்ம தேவர் அதர்வாங்கிரஸ முனிவருக்குச் சூரிய பிரம்ம வித்தையை அருளினார்: 'ஸூர்ய ஆத்மா ஜகதஸ்தஸ்துஷஸ்ச — இயங்கும் மற்றும் இயங்காத இப்பிரபஞ்சம் அனைத்தின் ஆத்மாவும் சூரிய பகவானே!'",
        "s2_en": "Applying the canonical Vedantic definition of Brahman directly to the Solar Spirit, the Upanishad proclaims: 'Suryad bhavanti bhutani, Suryena palitani tu, Surye layam prapnuvanti, yah Suryah so'ham eva cha! From Surya all living beings are born; by Surya are they nourished and sustained; into Surya do they return and merge—and He who is that Supreme Surya, That very One am I!'",
        "s2_ta": "பிரம்மத்தின் இலக்கணத்தைச் சூரிய பகவானுக்கே பொருத்தி உபநிடதம் முழங்குகிறது: 'ஸூர்யாத் பவந்தி பூதானி, ஸூர்யேண பாலிதானி து, ஸூர்யே லயம் ப்ராப்னுவந்தி, யஃ ஸூர்யஃ ஸோऽஹமேவ ச! சூரியனிடமிருந்தே எல்லா உயிர்களும் தோன்றுகின்றன; சூரியனாலேயே காக்கப்படுகின்றன; சூரியனிலேயே ஒடுங்குகின்றன — அந்தச் சூரியப் பரம்பொருள் எவனோ, அவனே நான்!'",
        "s3_en": "From this Solar Purusha arise the sacrifice, the rain-clouds, the five elements, the seven vital breaths, and the division of Time—moments, hours, days, fortnights, months, seasons, and years—drawn across the sky by seven emerald horses yoked to a single-wheeled chariot of Cosmic Order!",
        "s3_ta": "அந்த ஆதித்ய புருஷனிடமிருந்தே யக்ஞமும், மழையும், பஞ்ச பூதங்களும், பிராணன்களும், நிமிடம் முதல் வருடம் வரையிலான காலச் சக்கரமும் தோன்றின! ஏழு குதிரைகள் பூட்டிய ஒற்றைச் சக்கரத் தேரில் பவனி வரும் அவரே பிரம்மா, விஷ்ணு, ருத்ரன் மற்றும் நான்கு வேதங்களின் வடிவமாவார்!",
        "s4_en": "How should the seeker meditate upon this Solar Brahman? In the golden orb of the rising Sun, behold the four-armed Golden Purusha holding two red lotuses, granting fearlessness (Abhaya) and boons (Varada), seated upon a red lotus and turning the wheel of Time!",
        "s4_ta": "சாதகன் எவ்வாறு தியானிக்க வேண்டும்? உதய சூரிய மண்டலத்தின் நடுவே, செந்தாமரை மீது அமர்ந்து, இரு கரங்களில் தாமரை ஏந்தி, அபய-வரத முத்திரையோடு காலச் சக்கரத்தை இயக்கும் பொன்மயமான நான்கு கர புருஷனாகத் தியானிக்க வேண்டும்!",
        "s5_en": "Then the Upanishad reveals the sacred Eight-Syllabled Aditya Mantra—Ashtakshara Surya Vidya: 'OM (1), GHRINIH (2-3), SURYAH (4-5), ADITYAH (6-7-8)!' Meditating upon the Gayatri and the Savitri with the conviction 'Adityo Brahma—The Sun is Brahman, and I am That!', the seeker's inner darkness vanishes like night before dawn!",
        "s5_ta": "அடுத்து எட்டெழுத்துச் சூரிய மந்திரமான 'ஓம் க்ருணிஃ ஸூர்ய ஆதித்யஃ' என்னும் அஷ்டாக்ஷர வித்தையை உபநிடதம் அருள்கிறது! 'ஆதித்யோ பிரம்ம — சூரியனே பிரம்மம், அந்தப் பேரொளியே நான்!' என்று தியானிப்பவனின் உள்ளத்து இருள் உதய சூரியனைக் கண்ட இரவு போல் மறைகிறது!",
        "s6_en": "Bathed in golden sunrise rays by the sacred river, Maharishi Atharvangiras and his disciples experienced the Sun in the sky and the Consciousness in the heart blazing as one undivided Jyotih.",
        "s6_ta": "வைகறைச் சூரிய ஒளியில் நனைந்த முனிவர்கள், விண்ணில் ஒளிரும் கதிரவனும் தம் இதயத்தில் ஒளிரும் ஆத்ம ஜோதியும் இரண்டற்ற ஒரே பிரம்மமே என்பதை நேரில் உணர்ந்தனர்.",
        "s7_en": "Whoever recites this Surya Upanishad at sunrise before the sacred fire or water crosses beyond all sin, poverty, disease, and mortality, and attains the Immortal Solar Brahman!",
        "s7_ta": "உதய காலத்தில் இந்தச் சூரிய உபநிடதத்தை ஓதித் தியானிப்பவன் பாவம், பிணி, வறுமை மற்றும் மரண பயம் நீங்கி, அழியாத ஆதித்ய பிரம்ம பதத்தை அடைகிறான்!"
    },
    {
        "story_id": "SAMANYA_20_PRANAGNIHOTRA_90",
        "muktika_number": 90,
        "upanishad_sanskrit": "प्राणाग्निहोत्रोपनिषद्",
        "upanishad_iast": "Prāṇāgnihotropaniṣad",
        "upanishad_tamil": "பிராணாக்னிஹோத்ர உபநிடதம்",
        "upanishad_english": "Pranagnihotra Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Inner Fire-Sacrifice of Breath & Food: Every Meal as a Cosmic Yajna in the Body-Temple",
        "story_title_tamil": "மூச்சும் உணவும் செய்யும் உள்முக வேள்வி: உடலையே யாகசாலையாக்கும் பிராணாக்னிஹோத்ர உபநிடதம்!",
        "characters": [
            "The Krishna Yajur Veda Acharya (Teaching how the seeker performs the eternal Agnihotra within his own body)",
            "Vaishvanara Agni & The Five Pranas (The Inner Fires receiving every morsel of food as an oblation to the Atman)"
        ],
        "mahavakya_sanskrit": "अथातः सर्वोपनिषत्सारं संसारतारकं प्राणाग्निहोत्रं... स्वशरीरे यज्ञं परिवर्तयामास ॥",
        "mahavakya_tamil_translit": "அதாதஃ ஸர்வோபநிஷத்ஸாரம் ஸம்ஸாரதாரகம் ப்ராணாக்னிஹோத்ரம்... ஸ்வசரீரே யஜ்ஞம் பரிவர்த்தயாமாஸ ||",
        "mahavakya_meaning_english": "Now is expounded the Pranagnihotra—the essence of all Upanishads that carries one across Samsara—whereby the wise turn their own body into the sacred Yajna!",
        "mahavakya_meaning_tamil": "அனைத்து உபநிடதங்களின் சாரமானதும், சம்சாரக் கடலைக் கடக்கச் செய்வதுமான 'பிராணாக்னிஹோத்ரம்' இதோ கூறப்படுகிறது — ஞானி தன் உடலையே புனித யாகசாலையாக மாற்றுகிறான்!",
        "philosophical_theme": "Internalization of Vedic Yajna (Pranagnihotra): Even without external fire or brick altars, offering food into the five Pranas ('Om Pranaya Svaha...') and mapping the entire Yajnashala onto the human body.",
        "setting_specifics": "A serene ashram pavilion where an Acharya and disciples sit before wholesome food on banana leaves, offering water and five prana-ahutis before eating.",
        "metaphor_highlight": "The Human Body as the Complete Yajnashala (Purusha = Sacrificer, Buddhi = Wife, Heart = Vedi Altar, Four Fires inside the Body, Five Prana Oblations with the Five Fingers).",
        "s1_en": "In the sacred Pranagnihotra Upanishad (#90 in the Muktika canon, from the Krishna Yajur Veda—the scripture that inspired the daily 'Om Pranaya Svaha' food-offering across all India!), the disciples asked: 'O Master! When a seeker renounces outer ritual fires, how is the eternal Agnihotra maintained within?'",
        "s1_ta": "முக்திக வரிசையில் 90-ஆவது உபநிடதமாகத் திகழ்வதும், பாரதம் முழுவதும் உணவு உண்ணும் முன் 'ஓம் பிராணாய ஸ்வாஹா' என்று ஆஹுதி இடும் மரபிற்கு மூலமானதுமான 'பிராணாக்னிஹோத்ர உபநிடதத்தில்', சீடர்கள் கேட்டனர்: 'குருதேவா! புற அக்னிஹோத்ர வேள்வியைச் செய்ய இயலாத நிலையில், உடலுக்குள்ளேயே நித்திய வேள்வியைச் செய்வது எப்படி?'",
        "s2_en": "The Acharya proclaimed: 'Listen to the essence of all Upanishads, which carries a mortal across Samsara! Even without kindling outer fires or reciting the Rig, Yajus, and Saman, the wise perform the supreme sacrifice within their own body through the Pranagnihotra—the Fire-Sacrifice of the Vital Breath!'",
        "s2_ta": "ஆச்சாரியர் அருளினார்: 'அனைத்து உபநிடதங்களின் சாரமான இந்தப் பிராணாக்னிஹோத்ரத்தைக் கேளுங்கள்! புறத்தே வேள்வித் தீயை வளர்க்காமலும், சடங்குகள் செய்யாமலும், நம் உடலுக்குள் உறையும் வைஸ்வானர அக்னியில் பிராண ஆஹுதி இடுவதே மிக உயர்ந்த உள்முக யக்ஞமாகும்!'",
        "s3_en": "How are the four Vedic fires present inside the human body? 'In the speech dwells the Sharira Agni; in the heart dwells the Garhapatya Fire; in the crescent of the navel dwells the Dakshinagni (digestive fire); and in the lotus of the face shines the Ahavaniya Fire! Mind is the ladle, and Knowledge is the sacred altar!'",
        "s3_ta": "நம் உடலுக்குள்ளேயே நான்கு வேள்வித் தீக்கள் எவ்வாறு உள்ளன? 'வாக்கில் சாரீர அக்னியும், இதயத்தில் கார்ஹபத்ய அக்னியும், நாபியில் (வயிற்றில்) தக்ஷிணாக்னியும், முக கமலத்தில் ஆஹவனீய அக்னியும் சுடர்விடுகின்றன! மனமே நெய் வார்க்கும் கரண்டி; ஞானமே யாக பீடம்!'",
        "s4_en": "Then the Upanishad teaches the exact ritual of every meal: 'Sipping water as an inner jacket of immortality for Prana (Amritopastaranam Asi), take food with the five sacred fingers as five oblations: with thumb and ring finger offer OM PRANAYA SVAHA! With thumb and middle finger, OM APANAYA SVAHA! With thumb and fourth finger, OM VYANAYA SVAHA! With thumb and little finger, OM UDANAYA SVAHA! And with all five fingers together, OM SAMANAYA SVAHA!'",
        "s4_ta": "உணவு உண்ணும் புனித வேள்வி முறையை உபநிடதம் போதிக்கிறது: 'முதலில் அம்ருதோபஸ்தரணமஸி என நீரைப் பருகி, ஐந்து விரல்களின் முத்திரைகளால் ஐந்து ஆஹுதிகளை இட வேண்டும்: ஓம் பிராணாய ஸ்வாஹா! ஓம் அபானாய ஸ்வாஹா! ஓம் வியானாய ஸ்வாஹா! ஓம் உதானாய ஸ்வாஹா! ஓம் சமானாய ஸ்வாஹா!'",
        "s5_en": "In the final chapter, the Upanishad maps the entire Ashvamedha and Agnihotra onto the living human temple: 'The Self (Atman) is the Yajamana (Sacrificer); the pure Intellect (Buddhi) is his consecrated Wife (Patni); the Heart is the Vedi altar; the Chest hairs are the Darbha grass; the Two Eyes are the clarified butter; the Tongue is the ladle; and Fearlessness and Non-Injury (Ahimsa) are the supreme Dakshina!'",
        "s5_ta": "நான்காம் பகுதியில் மனித உடலையே முழுமையான யாகசாலையாக உபநிடதம் காட்டுகிறது: 'ஆத்மாவே எஜமானன்; தூய புத்தியே தர்மபத்தினி; இதயமே வேதிகை; மார்பு ரோமங்களே தர்ப்பைப் புல்; இரு கண்களே ஆஜ்யம் (நெய்); நாக்கே ஸ்ருவம்; அஹிம்சையும் அபயமுமே மிகச் சிறந்த தட்சிணை!'",
        "s6_en": "Eating the remainder in silence while contemplating the Hamsa-So'ham mantra in the heart, and closing with 'Amritapidhänam Asi', every single breath and meal becomes an offering into the Supreme Brahman!",
        "s6_ta": "மௌனமாக உணவருந்தி இதயத்தில் ஹம்ஸ-ஸோऽஹம் தியானத்துடன் 'அம்ருதாபிதானமஸி' என்று நிறைவு செய்யும்போது, உண்ணும் ஒவ்வொரு கவளமும் விடும் ஒவ்வொரு மூச்சும் பிரம்ம வேள்வியாகவே மாறுகிறது!",
        "s7_en": "He who knows and practices this Pranagnihotra Upanishad—even if his body drops in an ordinary place—needs no outer rites, for he is already consecrated in the Eternal Fire of the Atman!",
        "s7_ta": "இந்தப் பிராணாக்னிஹோத்ர உபநிடதத்தை உணர்ந்து கடைப்பிடிப்பவன், தன் உடம்பையே நித்திய யாகசாலையாக்கி ஆத்ம ஜோதியில் இரண்டறக் கலக்கிறான்!"
    },
    {
        "story_id": "SAMANYA_21_GARBHA_17",
        "muktika_number": 17,
        "upanishad_sanskrit": "गर्भोपनिषद्",
        "upanishad_iast": "Garbhopaniṣad",
        "upanishad_tamil": "கர்ப்ப உபநிடதம்",
        "upanishad_english": "Garbha Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Sage Pippalada's Embryology & The Soul's Vow in the Womb: Awakening Before the Wind of Maya",
        "story_title_tamil": "பிப்பலாத முனிவரின் கருவறை அறிவியலும் ஜீவனின் சபதமும்: மாயைக் காற்றுத் தீண்டும் முன் விழித்தெழும் கர்ப்ப உபநிடதம்!",
        "characters": [
            "Maharishi Pippalada (Revealer of the Moksha-Shastra of Garbha Upanishad—ancient Vedic embryology and spiritual awakening)",
            "The Jiva in the Womb (Who remembers its past births in the 9th month and vows to worship Narayana/Shiva, before forgetting upon touching the Vaishnavayu at birth)"
        ],
        "mahavakya_sanskrit": "गर्भोपनिषदं व्याख्यास्यामः... योनिशतसहस्राणि दृष्ट्वा... बाह्यवायुना स्पृष्टः... नारायणं चिन्तयिष्यामि ॥",
        "mahavakya_tamil_translit": "கர்ப்போபநிஷதம் வ்யாக்யாஸ்யாமஃ... யோனிஸதஸஹஸ்ராணி த்ருஷ்ட்வா... பாஹ்யவாயுனா ஸ்ப்ருஷ்டஃ... நாராயணம் சிந்தயிஷ்யாமி ||",
        "mahavakya_meaning_english": "Remembering thousands of past births in the womb, the soul vows: 'Once born, I shall meditate on Mahesvara and Narayana and study Sankhya-Yoga!'—yet touched by the outer wind of Maya at birth, it forgets!",
        "mahavakya_meaning_tamil": "கருவறையில் ஒன்பதாம் மாதத்தில் பழைய பிறவிகளை நினைவுகூரும் ஜீவன், 'பிறந்தவுடன் மகேஸ்வரனையும் நாராயணனையும் தியானித்து உபநிடத ஞானத்தைப் பெறுவேன்!' என்று சபதம் எடுக்கிறான்; ஆனால் பிறந்தவுடன் மாயைக் காற்றுப் பட்டு மறந்துவிடுகிறான்!",
        "philosophical_theme": "Remarkably accurate ancient Vedic embryology (from 1 night, 7 nights, 1 month up to 9 months); the eight-fire sacrifice of the body; and the Soul's Womb-Prayer ('Stuti') before being touched by the Vaishnavayu.",
        "setting_specifics": "Maharishi Pippalada's Gurukulam pavilion where palm-leaf scrolls depict the nine months of embryonic development and the luminous soul within.",
        "metaphor_highlight": "Kalala (1 night) -> Budbuda (7 nights) -> Pinda (fortnight) -> Kathina (1 month) -> Head (2 months) -> Feet (3 months) -> Spine/Belly (4 months) -> Senses (7 months); and the Vaishnavayu (Wind of Maya at birth).",
        "s1_en": "In the extraordinary Garbha Upanishad (#17 in the Muktika canon, from the Krishna Yajur Veda, revealed by Maharishi Pippalada), ancient medical science and supreme Vedanta unite to answer: 'How is this five-element body formed in the mother's womb, and what does the conscious Jiva experience before birth?'",
        "s1_ta": "முக்திக வரிசையில் 17-ஆவது உபநிடதமாகத் திகழும் கிருஷ்ண யஜுர் வேதத்தின் 'கர்ப்ப உபநிடதத்தில்', மகரிஷி பிப்பலாதர் பண்டைய கருவறை அறிவியலையும் வேதாந்த ஞானத்தையும் இணைத்துக் கூறுகிறார்: 'பஞ்ச பூதங்களால் ஆன இவ்வுடல் தாயின் கருவறையில் எவ்வாறு உருவாகிறது? பிறப்பதற்கு முன் ஜீவன் என்ன சிந்திக்கிறான்?'",
        "s2_en": "Explaining first the five elements, the six tastes (sweet, sour, salty, pungent, bitter, astringent), the seven musical notes (Shadja, Rishabha, Gandhara, Madhyama, Panchama, Dhaivata, Nishada), and the seven bodily tissues (Dhatus), Pippalada traced the exact month-by-month growth of the human embryo!",
        "s2_ta": "முதலில் பஞ்ச பூதங்கள், அறுசுவைகள், சப்த ஸ்வரங்கள் (ஷட்ஜம், ரிஷபம், காந்தாரம், மத்யமம், பஞ்சமம், தைவதம், நிஷாதம்) மற்றும் ஏழு தாதுக்களை விளக்கிய பிப்பலாதர், கருவறையில் சிசு மாதம் தோறும் வளரும் விதத்தைத் துல்லியமாக விவரித்தார்!",
        "s3_en": "'After one night, the fertilized seed is a microscopic droplet (Kalala); after seven nights, a bubble (Budbuda); in fifteen days, a spherical mass (Pinda); in one month, firm; in two months, the head forms; in three months, the limb-buds; in four months, ankles, belly, and hips; in five months, the spine; in six months, mouth, nose, eyes, and ears; in seven months, the conscious Jiva-sense awakens; and in eight months, every organ is complete!'",
        "s3_ta": "'கருத்தரித்த ஓர் இரவில் கலலம் (சிறு துளி); ஏழு இரவுகளில் புத்புதம் (நீர்க்குமிழி); பதினைந்து நாட்களில் பிண்டம்; ஒரு மாதத்தில் கடினத் தன்மை; இரண்டாம் மாதத்தில் சிரசு; மூன்றாம் மாதத்தில் பாதங்கள்; நான்காம் மாதத்தில் வயிறு மற்றும் இடுப்பு; ஐந்தாம் மாதத்தில் முதுகெலும்பு; ஆறாம் மாதத்தில் வாய், மூக்கு, கண், காது; ஏழாம் மாதத்தில் ஜீவ உணர்வு; எட்டாம் மாதத்தில் முழு உடலும் நிறைவடைகிறது!'",
        "s4_en": "Then in the ninth month, endowed with full awareness and memory of thousands of previous births and karmas, the Jiva inside the womb offers a poignant prayer: 'I have seen thousands of wombs, eaten countless foods, and loved and lost countless relatives strictly for selfish gain, forgetting the Lord! Now, while resting in this womb, if only I am delivered safely—'",
        "s4_ta": "ஒன்பதாம் மாதத்தில், தன் முற்பிறவிகள் அனைத்தையும் நினைவுகூரும் ஜீவன் கருவறைக்குள்ளிருந்து உருக்கமாகப் பிரார்த்திக்கிறான்: 'ஆயிரக்கணக்கான பிறவிகளைக் கண்டேன்; சுயநலத்திற்காகப் பல கர்மங்களைச் செய்து இறைவனை மறந்தேன்! இப்போது இக்கருவறையிலிருந்து நான் வெளியே வந்தவுடன்—'",
        "s5_en": "The soul in the womb makes its solemn vow: 'Once born, I shall take refuge in Mahesvara and Narayana! I shall study Sankhya-Yoga and the Upanishads, meditate upon the Imperishable Brahman, and tear away the net of Samsara forever!' Yet the instant the child emerges from the womb and is touched by the outer wind of Maya—Vaishnavayu—it forgets its past births and cries out in delusion!",
        "s5_ta": "கருவறையில் உள்ள ஜீவன் சபதம் எடுக்கிறான்: 'நான் பிறந்தவுடன் மகேஸ்வரனையும் நாராயணனையும் சரணடைவேன்! சாங்கிய-யோகத்தையும் உபநிடத ஞானத்தையும் பயின்று பிரம்மத்தைத் தியானிப்பேன்!' ஆனால் கருவறையிலிருந்து வெளியே வந்து 'வைஷ்ணவ வாயு' (மாயைக் காற்று) பட்ட கணமே, தன் சபதத்தை மறந்து உலக மயக்கத்தில் அழத் தொடங்குகிறான்!",
        "s6_en": "Therefore Maharishi Pippalada taught how the wise awaken right now to that forgotten womb-vow: making the Mind the Yajamana, the Body the altar, and Knowledge the fire, they remember the Immortal Self before death arrives!",
        "s6_ta": "ஆகவே கருவறையில் நாம் எடுத்த அந்தப் புனித சபதத்தை இப்போதே நினைவூட்டுகிறார் பிப்பலாத முனிவர்: உடலை யாக பீடமாக்கி, ஞானத் தீயை மூட்டி, இப்பிறவியிலேயே பரம்பொருளை உணர வழிகாட்டுகிறார்!",
        "s7_en": "Thus concludes the Moksha-Shastra of Maharishi Pippalada—the Garbha Upanishad: whoever remembers the vow of the soul and meditates upon the Unborn Brahman never enters a mother's womb again!",
        "s7_ta": "பிப்பலாத முனிவர் அருளிய மோட்ச சாஸ்திரமான இந்தக் கர்ப்ப உபநிடதத்தை உணர்பவன், கருவறைச் சபதத்தை நிறைவேற்றி மீண்டும் தாயின் கருவில் புகாத பிறவாப் பெருநிலையை அடைகிறான்!"
    },
    {
        "story_id": "SAMANYA_22_MAITREYI_29",
        "muktika_number": 29,
        "upanishad_sanskrit": "मैत्रेय्युपनिषद्",
        "upanishad_iast": "Maitreyyupaniṣad",
        "upanishad_tamil": "மைத்ரேயி உபநிடதம்",
        "upanishad_english": "Maitreyi Upanishad",
        "veda": "Sama Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Lord Shiva to Goddess Maitreyi/Parvati: True Abhisheka of the Mind & The Song of 'I Am That'",
        "story_title_tamil": "மைத்ரேயி உபநிடதம்: மனதாலேயே செய்யும் உண்மையான சிவ பூஜையும் 'அதுவே நான்' என்ற அத்வைத கீதமும்!",
        "characters": [
            "King Brihadratha & Sage Shakayanya (Chapter 1 framing of Vairagya and Shadanga Yoga)",
            "Goddess Maitreyi / Parvati (Asking Lord Shiva in Chapter 2 for the secret of true worship and non-dual identity)",
            "Lord Paramesvara / Somaskanda Shiva (Teaching inner Abhisheka, Arghya, and the ecstatic Advaita Gatha)"
        ],
        "mahavakya_sanskrit": "अपांशुः शिवलिङ्गस्य... देहो देवालयः प्रोक्तः स जीवः केवलः शिवः । प्रज्ञानघन एवाहं... सोऽहमस्मि सनातनः ॥",
        "mahavakya_tamil_translit": "தேஹோ தேவாலயஃ ப்ரோக்தஃ ஸ ஜீவஃ கேவலஃ ஸிவஃ | ப்ரஜ்ஞானகன ஏவாஹம்... ஸோऽஹமஸ்மி ஸனாதனஃ ||",
        "mahavakya_meaning_english": "The body is the temple and the Jiva within is verily Kewala Shiva alone! I am a solid mass of Pure Consciousness; I am that Eternal One!",
        "mahavakya_meaning_tamil": "இவ்வுடம்பே திருக்கோயில்; உள்ளே உறையும் ஜீவனே கேவல சிவன்! நான் தூய ஞானப் பிழம்பு; அந்தச் சனாதனப் பரம்பொருளே நான்!",
        "philosophical_theme": "Internalization of Shiva-Puja (Bathing the mind in detachment is true Snana, holding Prana steady is Pratishtha,Samadhi is Abhisheka) and the ecstatic 27-verse Advaita Song of Chapter 3.",
        "setting_specifics": "Mount Kailasa / South Indian granite Shiva temple sanctum bathed in golden lamp-light where Goddess Maitreyi receives the inner Puja teaching from Lord Shiva.",
        "metaphor_highlight": "Manasa-Snana (Washing away mental dirt as the true sacred bath), Samadhi as Abhisheka, Space in a Jar, and 'Deho Devalayah Prokto Sa Jivah Kevalah Shivah'.",
        "s1_en": "In the luminous Maitreyi Upanishad (#29 in the Muktika canon, belonging to the Sama Veda), after recounting King Brihadratha's forest Tapas in the first chapter, the second chapter opens on the heights of Kailasa where Maitreyi bowed before Lord Paramesvara and asked: 'O Lord! Tell me the secret of that Turiya Reality by which the wise attain liberation without effort!'",
        "s1_ta": "முக்திக வரிசையில் 29-ஆவது உபநிடதமாகத் திகழும் சாம வேதத்தின் 'மைத்ரேயி உபநிடதத்தில்', முதல் பகுதியில் பிருஹத்ரதனின் தவத்தைக் கூறிவிட்டு, இரண்டாம் பகுதியில் கைலாய நாதனான பரமேஸ்வரனிடம் மைத்ரேயி தேவி கேட்டாள்: 'இறைவா! எதனை அறிந்தால் சிரமமின்றி மோட்சம் கிட்டுமோ, அந்தத் துரீய தத்துவத்தை எனக்கு உபதேசியுங்கள்!'",
        "s2_en": "Lord Shiva revealed the superiority of Inner Knowledge over mere external austerity: 'Without the mirror of Self-Knowledge, merely torturing the body or wandering to distant rivers cannot liberate! Look at a fish: it is born in sacred water and dies in water, yet it does not go to heaven because its mind is not purified! Washing away the dirt of mental delusion—Mano-malasya tyagah—is the only true sacred bath!'",
        "s2_ta": "புறச் சடங்குகளை விட அகத் தூய்மையே மேலானது என்று சிவபெருமான் அருளினார்: 'ஆத்ம ஞானம் இல்லாமல் வெறும் உடலை வருத்துவதால் முக்தி கிட்டாது! புண்ணிய நதி நீரிலேயே பிறந்து நீரிலேயே மடியும் மீன் சுவர்க்கம் செல்வதில்லையே, ஏனெனில் அதன் மனம் தூய்மையடையவில்லை! மனோமலத்தைக் கழுவுவதே உண்மையான புனித நீராடல் (தீர்த்த ஸ்நானம்)!'",
        "s3_en": "Then Lord Shiva taught the supreme Antar-Puja—the Inner Worship of the Self: 'Deho devalayah proktah, sa jivah kevalah Shivah! This body is the temple, and the Jiva within is none other than Pure Shiva! Discard the faded flowers of ignorance and worship with the conviction So'ham—I am He! Seeing non-duality is the true Avahana (invocation); steadiness of intellect is the true Asana (seat)!'",
        "s3_ta": "தொடர்ந்து ஆத்ம பூஜையின் ரகசியத்தை ஈசன் போதித்தார்: 'தேஹோ தேவாலயஃ ப்ரோக்தஃ ஸ ஜீவஃ கேவலஃ ஸிவஃ! இவ்வுடம்பே ஆலயம்; உள்ளே உறையும் ஜீவனே கேவல சிவன்! அறியாமை என்னும் பழைய மலர்களை நீக்கி ஸோऽஹம் பாவனையால் பூஜிப்பாயாக! பேதமற்ற பார்வையே ஆவாஹனம்; அசையாத புத்தியே ஆசனம்!'",
        "s4_en": "'Unclouded transparency of mind is the true Arghya and Padya! Continuous awareness of the Self-Luminous Consciousness is the true Abhisheka! Abiding in one's own natural stillness is the true Naivedya! And silence where not even a single vritti stirs is the true Pradakshina and Namaskara!'",
        "s4_ta": "'மனத் தெளிவே அர்க்கியமும் பாத்யமும்! சைதன்ய ஒளியில் தோய்வதே அபிஷேகம்! தன்னிலையில் நிறைந்திருப்பதே நைவேத்தியம்! எந்த விருத்தியும் அற்ற நிர்மல மௌனமே பிரதக்ஷிணமும் நமஸ்காரமும் ஆகும்!'",
        "s5_en": "In the third chapter, the Maitreyi Upanishad bursts into the twenty-seven-verse ecstatic Song of the Awakened Self: 'Aham eva परं ब्रह्म—I alone am the Supreme Brahman! I am the Lord of all, the Witness free from the three states! All universes appear in Me like silver in a mother-of-pearl shell, or water in a mirage, or a city in a mirror!'",
        "s5_ta": "மூன்றாம் அத்தியாயத்தில் ஞானியின் இருபத்தேழு சுலோகங்கள் கொண்ட ஆனந்த கீதம் பொங்கி வழிகிறது: 'அஹமேவ பரம் பிரம்ம — பரம்பொருள் நானே! மூன்று அவஸ்தைகளுக்கும் அப்பாற்பட்ட சாட்சி நானே! சிப்பியில் வெள்ளி போலவும், கானல் நீரில் ஆறு போலவும், கண்ணாடியில் தெரியும் நகரம் போலவும் என்னிலேயே உலகங்கள் தோன்றி மறைகின்றன!'",
        "s6_en": "'I have no Guru and no disciple, no duty and no sorrow, no birth and no death; I am spotless, changeless, self-luminous Prajnanaghana Shiva—One without a second!'",
        "s6_ta": "'நான் தூய பிரக்ஞானகன சிவன்; இரண்டற்ற ஏகப் பரம்பொருள் நானே! எனக்குப் பிறப்புமில்லை, இறப்புமில்லை, துக்கமுமில்லை; சனாதன சச்சிதானந்த சொரூபம் நானே!'",
        "s7_en": "Receiving this supreme wisdom from Lord Shiva, Maitreyi abided in effortless Advaita Samadhi. Whoever contemplates this Maitreyi Upanishad becomes Kewala Shiva Himself!",
        "s7_ta": "பரமேஸ்வரனிடமிருந்து இந்த ஞானத்தைப் பெற்ற மைத்ரேயி அத்வைத சமாதியில் நிலைபெற்றாள். இந்த மைத்ரேயி உபநிடதத்தைத் தியானிப்பவன் கேவல சிவ சொரூபமாகவே ஆகிறான்!"
    },
    {
        "story_id": "SAMANYA_23_GARUDA_BRIHAJJABALA_102",
        "muktika_number": 102,
        "upanishad_sanskrit": "गारुडोपनिषद् (बृहज्जाबाल-समन्वित)",
        "upanishad_iast": "Gāruḍopaniṣad",
        "upanishad_tamil": "காருட உபநிடதம் (#102) & சாமான்ய வேதாந்த நச்சு நீக்க வித்தை",
        "upanishad_english": "Garuda Upanishad (#102 in Muktika Canon)",
        "veda": "Atharva Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Brahma, Narada & Suparna Garuda: Destroying the Venom of Serpents & the Venom of Samsara",
        "story_title_tamil": "பிரம்மன், நாரதர் மற்றும் கருட பகவான்: நாக விஷத்தையும் சம்சார விஷத்தையும் அழிக்கும் காருட பிரம்ம வித்தை!",
        "characters": [
            "Lord Pitamaha Brahma (Revealer of the Garuda Brahmavidya to Devarishi Narada)",
            "Devarishi Narada (Who transmitted the Garuda Vidya to Brihatsena, Indra, Bharadvaja, and humanity)",
            "Vainateya Garuda / Suparna (The Golden-Winged Vehicle of Vishnu and Sovereign Destroyer of Poison and Ignorance)"
        ],
        "mahavakya_sanskrit": "गारुडब्रह्मविद्यां प्रवक्ष्यामि... हंसो हंसः परमहंसः सोऽहम् । निर्विषो भवति मुच्यते संसारविषबंधनात् ॥",
        "mahavakya_tamil_translit": "காருட ப்ரஹ்மவித்யாம் ப்ரவக்ஷ்யாமி... ஹம்ஸோ ஹம்ஸஃ பரமஹம்ஸஃ ஸோऽஹம் | நிர்விஷோ பவதி முச்யதே ஸம்ஸார விஷபந்தனாத் ||",
        "mahavakya_meaning_english": "I shall declare the Garuda Brahmavidya! By the power of Suparna-Atman, all physical venom and the deadly poison of Samsara-ignorance are destroyed instantly!",
        "mahavakya_meaning_tamil": "காருட பிரம்ம வித்தையை உரைக்கிறேன்! சுபர்ணனான ஆத்ம சக்தியால் கொடிய நாக விஷமும், சம்சாரம் என்னும் அறியாமை விஷமும் கணப்பொழுதில் நீங்கி முக்தி சித்திக்கிறது!",
        "philosophical_theme": "Canonical Muktika #102 (Garuda Upanishad of the Atharva Veda, paired with Brihajjabala #26 cross-reference): Sovereign mastery of Consciousness (Garuda/Suparna) over both physical serpent-venom and the fivefold poison of sensory attachment (Vishaya-Visha).",
        "setting_specifics": "Lord Brahma's lotus assembly where Devarishi Narada receives the Garuda Vidya as the golden-winged Suparna soars across the sky.",
        "metaphor_highlight": "Vainateya Garuda (whose wings are the Brihat and Rathantara Samans) neutralizing both Takshaka/Karkotaka serpent venom and the Deadly Venom of Sense-Objects (Vishaya-Visha).",
        "s1_en": "At #102 in the Muktika canon stands the Garuda Upanishad of the Atharva Veda (alongside the sacred Vibhuti-Agni wisdom of the Brihajjabala tradition). Approaching Lord Pitamaha Brahma, Devarishi Narada prayed: 'O Lord! Teach me that Garuda Brahmavidya which destroys both deadly serpent venom and the poison of worldly ignorance!'",
        "s1_ta": "முக்திக வரிசையில் 102-ஆவது உபநிடதமாகத் திகழும் அதர்வண வேதத்தின் 'காருட உபநிடதத்தில்', தேவரிஷி நாரதர் பிரம்ம தேவரிடம் வேண்டினார்: 'பகவானே! கொடிய நாகங்களின் விஷத்தையும், பிறவிப் பெருங்கடல் என்னும் சம்சார விஷத்தையும் ஒருங்கே அழிக்கும் காருட பிரம்ம வித்தையை எனக்கு உபதேசியுங்கள்!'",
        "s2_en": "Lord Brahma revealed the lineage of this sovereign wisdom: 'Listen, O Narada! What I teach you, impart to Brihatsena, who shall give it to Indra, Indra to Bharadvaja, and Bharadvaja to his disciples desiring the welfare of all creatures! For Vainateya Garuda—Suparna—is none other than the Vedic Person whose right wing is the Brihat Saman, whose left wing is the Rathantara Saman, and whose soul is the Immortal Atman!'",
        "s2_ta": "பிரம்ம தேவர் அருளினார்: 'நாரதா! நான் உனக்குக் கூறும் இந்த வித்தையை பிருஹத்சேனனுக்கும், அவன் இந்திரனுக்கும், இந்திரன் பரத்வாஜருக்கும் உலக நன்மைக்காக வழங்குவார்கள்! ஏனெனில் கருட பகவான் (சுபர்ணன்) வேத சொரூபமான பரமாத்மாவே! அவரது வலது சிறகு பிருஹத் சாமம், இடது சிறகு ரதந்தர சாமம், ஆத்மாவோ அழியாத பிரம்மம்!'",
        "s3_en": "When a seeker invokes the Suparna-Atman with the sacred Garuda Mala-Mantra—'Om Namo Bhagavate महागरुडाय पक्षिराजाय विष्णුවल्लभाय'—the fierce venom of Ananta, Vasuki, Takshaka, Karkotaka, Padma, Mahapadma, Shankha, and Kulika, as well as scorpions and spiders, dries up and perishes like mist before the blazing sun!",
        "s3_ta": "'ஓம் நமோ பகவதே மஹாகருடாய பக்ஷிராஜாய விஷ்ணுவல்லபாய' என்று ஆத்ம சக்தியோடு கருட மந்திரத்தை உச்சரிக்கும்போது, அனந்தன், வாசுகி, தக்ஷகன், கார்க்கோடகன், பத்மன், மஹாபத்மன், சங்கபாலன், குளிகன் ஆகிய நாகங்களின் விஷமும், தேள், சிலந்தி முதலான நஞ்சுகளும் கதிரவனைக் கண்ட பனி போல் உடனே அழிகின்றன!",
        "s4_en": "Yet the Upanishadic sages point to an even deadlier venom than the cobra's bite: VISHAYA-VISHA—the Poison of Sense-Objects! A serpent's bite kills only one physical body when touched, whereas the poison of greed, lust, and ego kills the deluded soul across a thousand births merely by being looked at or thought of!",
        "s4_ta": "ஆனால் நாக விஷத்தை விடக் கொடிய விஷம் ஒன்றை உபநிடத முனிவர்கள் சுட்டிக்காட்டுகின்றனர் — அதுவே 'விஷய விஷம்' எனப்படும் சிற்றின்ப நஞ்சு! பாம்பின் விஷம் கடித்தால் மட்டுமே ஒரு பிறவியின் உடலைக் கொல்லும்; ஆனால் காமம், குரோதம், பேராசை என்னும் விஷய விஷமோ நினைத்த மாத்திரத்திலேயே எண்ணற்ற பிறவிகளில் ஜீவனை வீழ்த்துகிறது!",
        "s5_en": "Just as a dry wooden post touched by the Garuda-Vidya bursts into green leaves and blossoms, the seeker who awakens the Golden-Winged Hamsa-Garuda of Pure Consciousness within his heart neutralizes every drop of karmic poison and proclaims: 'So'ham—I am the Immortal Witness untouched by any venom!'",
        "s5_ta": "காருட வித்தையால் தொடப்பட்ட பட்டமரம் தளிர்ப்பது போல், இதயத்தில் பொன் சிறகு கொண்ட ஆத்ம சுபர்ணனை (ஹம்ஸத்தை) விழிப்பிக்கச் செய்யும் சாதகன், கர்ம நஞ்சுகள் அனைத்தையும் நீக்கி 'நான் எந்த விஷத்தாலும் தீண்டப்படாத அமிர்த ஆத்மா!' என்று முழங்குகிறான்!",
        "s6_en": "Adorned with the sacred Bhasma of Shiva-Jnana and soaring on the wings of the Gayatri and Sama Veda, the Yogi looks down upon the serpents of fear and mortality as harmless ropes.",
        "s6_ta": "ஞான விபூதியைத் தரித்து, வேதச் சிறகுகளில் பறக்கும் யோகிக்கு, மரண பயம் என்னும் பாம்புகள் அனைத்தும் வெறும் கயிறாகவே தோன்றுகின்றன.",
        "s7_en": "Whoever studies this Garuda Upanishad on an auspicious constellation and meditates upon the Suparna-Brahman is forever protected from all earthly and cosmic poisons, attaining fearless Liberation!",
        "s7_ta": "இந்தக் காருட உபநிடதத்தை ஓதி ஆத்ம சுபர்ணனைத் தியானிப்பவன், புற விஷங்களிலிருந்தும் பிறவி விஷத்திலிருந்தும் முற்றிலும் விடுபட்டு அபய மோட்சத்தை அடைகிறான்!"
    },
    {
        "story_id": "SAMANYA_24_MUKTIKA_108",
        "muktika_number": 108,
        "upanishad_sanskrit": "मुक्तिकोपनिषद्",
        "upanishad_iast": "Muktikopaniṣad",
        "upanishad_tamil": "முக்திக உபநிடதம் (108 உபநிடதங்களின் மகுடம்)",
        "upanishad_english": "Muktika Upanishad (#108 Master Canon)",
        "veda": "Shukla Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "Sri Rama & Hanuman in Ayodhya: The Master Canon of 108 Upanishads & The Bird of Mind & Prana",
        "story_title_tamil": "அயோத்தியில் ஸ்ரீராமரும் ஆஞ்சநேயரும்: 108 உபநிடதங்களின் பட்டியலும் மனோநாச-வாசனா க்ஷய முக்தி ரகசியமும்!",
        "characters": [
            "Bhagavan Sri Ramachandra (The Supreme Parabrahman enthroned in Ayodhya alongside Sita, Lakshmana, Bharata, Shatrughna, and Vasishtha)",
            "Bhakta Hanuman / Maruti (The ideal devotee and Brahmajnani who asks Sri Rama for the canon of all Upanishads and the nature of Mukti)"
        ],
        "mahavakya_sanskrit": "माण्डूक्यमेवालं मुमुक्षूणां विमुक्तये । वासनाक्षयविज्ञानमनोनाशा महामते समकालं चिराभ्यस्ता भवन्ति फलदा मताः ॥",
        "mahavakya_tamil_translit": "மாண்டூக்யமேவாலம் முமுக்ஷூணாம் விமுக்தயே | வாஸனாக்ஷய விஜ்ஞான மனோநாஸா மஹாமதே ஸமகாலம் சிராப்யஸ்தா பவந்தி பலதா மதாஃ ||",
        "mahavakya_meaning_english": "The Mandukya alone is sufficient for the liberation of seekers; if not, study 10, 32, or all 108 Upanishads! Realization (Vijnana), destruction of Vasanas, and dissolution of the Mind practised together bestow Jivanmukti!",
        "mahavakya_meaning_tamil": "முமுக்ஷுக்களுக்கு முக்தி அளிக்க மாண்டூக்ய உபநிடதம் ஒன்றே போதும்; இல்லையேல் 10, 32 அல்லது 108 உபநிடதங்களையும் பயில்க! தத்துவ ஞானம், வாசனா க்ஷயம், மனோ நாசம் ஆகிய மூன்றும் கூடியே ஜீவன்முக்தி அளிக்கின்றன!",
        "philosophical_theme": "The Grand Culmination (#108): Sri Rama reveals to Hanuman the complete canonical list of 108 Upanishads across the Four Vedas, their Shanti Mantras, the Four Types of Mukti vs. Kaivalya, and the Twin Method of Prana-Rodha and Vasana-Kshaya.",
        "setting_specifics": "The jewel-studded royal court of Ayodhya where Lord Sri Rama sits on the Simhasana with Sita Devi and Maharishi Vasishtha while Hanuman kneels with folded hands.",
        "metaphor_highlight": "108 Upanishads as pearls on a necklace (Muktika), Tree trembling with both Wind and Sap (Mind vibrating with both Vasana and Prana), and Space in a Jar merging into Mahakasha (Videhamukti).",
        "s1_en": "Crowning the entire Vedic canon at #108 stands the glorious Muktika Upanishad of the Shukla Yajur Veda! In the resplendent city of Ayodhya, Lord Sri Ramachandra sat upon his jewel throne surrounded by Sita Devi, his brothers, and Maharishi Vasishtha. Bowing low at Sri Rama's lotus feet, mighty Hanuman asked: 'O Rama! Thou art Paramatman—Existence, Consciousness, and Bliss! Tell me how a soul crosses the ocean of Samsara and attains Mukti!'",
        "s1_ta": "108 உபநிடதங்களின் மகுடமாக 108-ஆவது இடத்தில் சுடர்விடுவது சுக்ல யஜுர் வேதத்தின் 'முக்திக உபநிடதம்'! அயோத்தி மாநகரில் சீதா தேவியோடும் வசிஷ்டಾದಿ முனிவர்களோடும் சிம்மாசனத்தில் வீற்றிருந்த பகவான் ஸ்ரீராமச்சந்திர மூர்த்தியின் திருவடிகளில் ஆஞ்சநேயர் பணிந்து, 'இராமா! சச்சிதானந்தப் பரம்பொருள் நீயே! சம்சாரக் கடலைக் கடந்து முக்தி அடையும் வழியை எனக்கு உபதேசித்தருள்வாயாக!' என்று வேண்டினார்.",
        "s2_en": "Sri Rama smiled with boundless grace and explained: 'Well asked, O Maruti! Wait—people speak of Salokya, Sarupya, Samipya, and Sayujya, yet even the world of Brahma is subject to time! The only eternal, fearless liberation by which even a worm or a human transcends rebirth is KAIVALYA MUKTI—realizing one's non-dual identity with Brahman through the Vedanta-Upanishads, which are My very breath!'",
        "s2_ta": "ஸ்ரீராமர் கருணையோடு அருளினார்: 'மாருதி! சாலோக்யம், சாரூப்யம், சாமீப்யம், சாயுஜ்யம் ஆகியவற்றையும் கடந்து, பிரம்ம லோகத்திற்கும் மேலான பிறப்பற்ற நித்திய விடுதலை என்பது கைவல்ய முக்தியே! என்னுடைய மூச்சுக் காற்றாக வெளிப்பட்ட வேதாந்த உபநிடத ஞானத்தாலேயே அந்தக் கைவல்ய முக்தி சித்திக்கும்!'",
        "s3_en": "Then Sri Rama gave the immortal graded prescription of the Muktika Canon: 'Mandukyam evalam mumukshunam vimuktaye! For a seeker of keenest maturity, the MANDUKYA UPANISHAD alone is enough for liberation! If knowledge does not dawn from that alone, study the TEN Mukhya Upanishads (Isha, Kena, Katha, Prashna, Mundaka, Mandukya, Taittiriya, Aitareya, Chandogya, Brihadaranyaka)! If still not steady, study THIRTY-TWO Upanishads; and if desiring Videhamukti, study all ONE HUNDRED AND EIGHT Upanishads!'",
        "s3_ta": "தொடர்ந்து உபநிடதப் பயிற்சியின் படிநிலைகளை ஸ்ரீராமர் அருளினார்: 'மாண்டூக்யமேவாலம் முமுக்ஷூணாம் விமுக்தயே! உத்தம அதிகாரியான சாதகனுக்கு முக்தி அளிக்க மாண்டூக்ய உபநிடதம் ஒன்றே போதுமானது! அதனால் மட்டும் ஞானம் நிலைபெறாவிட்டால் ஈசாவாஸ்யம் முதல் பிருஹதாரண்யகம் வரையிலான பத்து உபநிடதங்களைப் பயில்வாயாக! அதிலும் தெளிவு பிறக்காவிட்டால் முப்பத்திரண்டு உபநிடதங்களையும், விதேக முக்தி வேண்டுமெனில் நூற்றியெட்டு உபநிடதங்களையும் பயில்வாயாக!'",
        "s4_en": "Reciting by name all 108 Upanishads—10 of the Rig Veda, 19 of the Shukla Yajur Veda, 32 of the Krishna Yajur Veda, 16 of the Sama Veda, and 31 of the Atharva Veda, along with their five respective Shanti Mantras—Sri Rama handed Hanuman the complete jewel-necklace of Vedanta!",
        "s4_ta": "ரிக் வேதத்தின் 10 உபநிடதங்கள், சுக்ல யஜுர் வேதத்தின் 19 உபநிடதங்கள், கிருஷ்ண யஜுர் வேதத்தின் 32 உபநிடதங்கள், சாம வேதத்தின் 16 உபநிடதங்கள், அதர்வண வேதத்தின் 31 உபநிடதங்கள் என 108 உபநிடதங்களின் பெயர்களையும் அவற்றின் சாந்தி மந்திரங்களையும் ஆஞ்சநேயருக்கு வரிசையாக உபதேசித்தார் ஸ்ரீராமர்!",
        "s5_en": "In the second chapter, Sri Rama taught Hanuman the practical royal secret of Jivanmukti and Videhamukti: 'O Wise Maruti! The Tree of the Mind has two seeds that make it tremble: Prana-Spandana (pulsation of breath) and Dridha-Vasana (deep-rooted latent desires)! If either one is quieted, the other immediately subsides! Therefore practice Tattva-Jnana (Self-Knowledge), Vasana-Kshaya (dissolution of desires), and Mano-Nasha (stilling of the mind) together at the same time!'",
        "s5_ta": "இரண்டாம் அத்தியாயத்தில் ஜீவன்முக்தி மற்றும் விதேகமுக்தியின் செய்முறை ரகசியத்தை ஸ்ரீராமர் போதித்தார்: 'மாருதி! மனம் என்னும் விருக்ஷத்திற்கு இரண்டு விதைகள் உண்டு — ஒன்று பிராண சலனம் (மூச்சின் அசைவு), மற்றொன்று வாசனை (உள்ளிருக்கும் ஆசைப் பதிவுகள்)! இவற்றில் ஒன்றை அடக்கினால் மற்றொன்றும் தானாகவே அடங்கும்! ஆகவே தத்துவ ஞானம், வாசனா க்ஷயம், மனோ நாசம் ஆகிய மூன்றையும் ஒரே காலத்தில் இடைவிடாது பழகுவாயாக!'",
        "s6_en": "When the Sleeping Mind is awakened, and the Waking restless Mind is dissolved into the Heart—where there is neither gloom nor distraction—there shines the Turiya Ramachandra, the Witness of all worlds! Beholding Sri Rama as the non-dual Self within his own heart, Hanuman entered supreme Samadhi!",
        "s6_ta": "சோம்பலில் தூங்கும் மனதை விழிப்பிக்கச் செய்து, ஆசைகளில் ஓடும் மனதை இதயத்தில் ஒடுக்கும்போது, அங்கே துரீயப் பரம்பொருளான ஸ்ரீராம சைதன்யம் சுயமாக ஒளிர்கிறது! தன் இதயத்திற்குள்ளேயே ஸ்ரீராமரை இரண்டற்ற ஆத்மாவாகத் தரிசித்த ஆஞ்சநேயர் பரம சமாதியில் திளைத்தார்!",
        "s7_en": "Thus concludes the 108th and final jewel—the Muktika Upanishad—with the Shukla Yajur Veda benediction: 'Om Purnamadah Purnamidam Purnat Purnam Udachyate, Purnasya Purnam Adaya Purnamevavashishyate! Om Shantih Shantih Shantih!'",
        "s7_ta": "இவ்வாறு 108 உபநிடதங்களின் மணிமகுடமான முக்திக உபநிடதம் பூரண சாந்தி மந்திரத்தோடு நிறைவடைகிறது: 'ஓம் பூர்ணமதஃ பூர்ணமிதம் பூர்ணாத் பூர்ணமுதச்யதே | பூர்ணஸ்ய பூர்ணமாதாய பூர்ணமேவாவஸிஷ்யதே || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ!'"
    }
])


SAMANYA_SPECS.extend([
    {
        "story_id": "SAMANYA_25_NARAYANA_18",
        "muktika_number": 18,
        "upanishad_sanskrit": "नारायणोपनिषद्",
        "upanishad_iast": "Nārāyaṇopaniṣad",
        "upanishad_tamil": "நாராயண உபநிடதம்",
        "upanishad_english": "Narayana Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Primeval Will of Narayana & The Eight-Syllabled Mantra of Immortality",
        "story_title_tamil": "ஆதி நாராயணனின் சங்கல்பமும் எட்டெழுத்து மந்திரத்தின் அமரத்துவ மகிமையும் (நாராயண உபநிடதம்)!",
        "characters": [
            "Purusha Narayana (The Cosmic Source from whom Prana, Mind, Senses, Elements, Brahma, Rudra, and Indra arise)",
            "Vedic Rishis of the Krishna Yajur Veda (Chanting the Ashtakshara 'Om Namo Narayanaya')"
        ],
        "mahavakya_sanskrit": "अथ पुरुषो ह वै नारायणोऽकामयत प्रजाः सृजेयेति । ॐ नमो नारायणायेति मन्त्रोपाஸकः वैकुण्ठभुवनं गमिष्यति ॥",
        "mahavakya_tamil_translit": "அத புருஷோ ஹ வை நாராயணோऽகாமயத ப்ரஜாஃ ஸ்ருஜேயேதி | ஓம் நமோ நாராயணாயேதி மந்த்ரோபாஸகஃ வைகுண்டபுவனம் கமிஷ்யதி ||",
        "mahavakya_meaning_english": "Verily, Purusha Narayana willed to create all beings; from Narayana arose Brahma, Rudra, Indra, and the Twelve Adityas! The worshiper of 'Om Namo Narayanaya' attains Immortal Vaikuntha!",
        "mahavakya_meaning_tamil": "புருஷனான நாராயணன் உயிர்களைப் படைக்கத் திருவுள்ளம் கொண்டார்; நாராயணனிடமிருந்தே பிரம்மாவும், ருத்ரனும், இந்திரனும் தோன்றினர்! 'ஓம் நமோ நாராயணாய' என உபாசிப்பவர் அமரத்துவ வைகுண்ட பதத்தை அடைகிறார்!",
        "philosophical_theme": "Cosmogenesis from Narayana; the esoteric structure of the Ashtakshara Mantra ('Om' = 1 syllable, 'Namo' = 2 syllables, 'Narayanaya' = 5 syllables); and realization of the Lotus-Heart Purusha.",
        "setting_specifics": "A serene Krishna Yajur Veda Gurukulam beside a lotus lake at dawn, glowing with golden solar rays.",
        "metaphor_highlight": "Ashtakshara (1 + 2 + 5 = 8 syllables of 'Om Namo Narayanaya') and the Lightning-Bright Purusha inside the Heart Lotus.",
        "s1_en": "In the revered Narayana Upanishad (#18 in the Muktika canon, from the Krishna Yajur Veda), the sages contemplated the primeval dawn of creation: 'Atha Purusho ha vai Narayano'kamayata prajah srijeyeti—Verily, in the beginning the Cosmic Purusha Narayana willed: Let Me bring forth all living beings!'",
        "s1_ta": "முக்திக வரிசையில் 18-ஆவது உபநிடதமாகத் திகழும் கிருஷ்ண யஜுர் வேதத்தின் 'நாராயண உபநிடதம்', படைப்பின் ஆதி சங்கல்பத்தோடு தொடங்குகிறது: 'அத புருஷோ ஹ வை நாராயணோऽகாமயத ப்ரஜாஃ ஸ்ருஜேயேதி — ஆதியில் புருஷனான நாராயணன் உயிர்களைப் படைக்கத் திருவுள்ளம் கொண்டார்!'",
        "s2_en": "From Narayana is born Vital Breath (Prana), Mind, and all the Senses! From Narayana arise Space, Wind, Fire, Water, and Earth that supports the universe! From Narayana is born Brahma; from Narayana is born Rudra; from Narayana is born Indra, Prajapati, the twelve Adityas, the eleven Rudras, the eight Vasus, and all Vedic metres!",
        "s2_ta": "நாராயணனிடமிருந்தே பிராணனும் மனமும் புலன்களும் தோன்றின! ஆகாயம், காற்று, நெருப்பு, நீர், பூமி ஆகிய பஞ்ச பூதங்களும் நாராயணனிடமிருந்தே பிறந்தன! நாராயணனிடமிருந்தே பிரம்மாவும், ருத்ரனும், இந்திரனும், பிரஜாபதியும், பன்னிரண்டு ஆதித்யர்களும், பதினொரு ருத்ரர்களும், எட்டு வசுக்களும் தோன்றினர்; நாராயணனிலேயே அனைத்தும் ஒடுங்குகின்றன!",
        "s3_en": "Then the Upanishad declares the non-dual truth of the Eternal: 'Nityo Narayano, Brahma Narayano, Shivashcha Narayano, Shakrashcha Narayano, Kalashcha Narayano, Dishashcha Narayano, Adhashcha Narayano, Urdhvashcha Narayano, Antarbahishcha Narayana—Narayana is all that was, all that is, and all that ever shall be, spotless, stain-free, Niranjana, Nirvikalpa, without a second!'",
        "s3_ta": "தொடர்ந்து நாராயணனின் சர்வ வியாபகத் தன்மையை உபநிடதம் போற்றுகிறது: 'பிரம்மாவும் நாராயணனே, சிவனும் நாராயணனே, இந்திரனும் நாராயணனே, காலமும் திசைகளும் நாராயணனே, கீழும் மேலும் உள்ளும் புறமும் எங்கும் நிறைந்திருப்பவர் நாராயணன் ஒருவரே! அவரே களங்கமற்ற நிரஞ்சன, நிர்விகல்பப் பரம்பொருள்!'",
        "s4_en": "Next, the Rishi unveils the sacred science of the Eight-Syllabled Ashtakshara Mantra: 'OM is one syllable; NAMO is two syllables; NARAYANAYA is five syllables—together these eight syllables form the supreme Ashtakshara of Narayana! Whoever studies and chants this Ashtakshara infused with the Samaveda attains full longevity, wealth, and mastery over the senses!'",
        "s4_ta": "அடுத்து எட்டெழுத்து மந்திரமான 'அஷ்டாக்ஷர வித்தை'யின் ரகசியத்தை உபநிடதம் வெளியிடுகிறது: 'ஓம் என்ற ஓரெழுத்தும், நமோ என்ற இரண்டெழுத்தும், நாராயணாய என்ற ஐந்தெழுத்தும் இணைந்ததே எட்டெழுத்து மந்திரமான ஓம் நமோ நாராயணாய! இதனை சிரத்தையோடு ஜபிப்பவர் நீண்ட ஆயுளும் செல்வமும் புலனடக்கமும் பெறுகிறார்!'",
        "s5_en": "Then rings the supreme climax of meditation: 'Within the lotus of the heart dwells the Purusha born of Devaki, Madhusudana, shining like a streak of lightning—Pundarikaksha, the Lotus-Eyed, Achyuta, the Imperishable Narayana pervading all creatures as the One Causeless Self!'",
        "s5_ta": "இதயத் தாமரைக்குள் மின்னல் கொடி போல் ஒளிரும் புண்டரீகாக்ஷனான, தேவகி நந்தனனான, மதுசூதனனான நாராயணனே எல்லா உயிர்களிலும் காரணமற்ற ஏக ஆத்மாவாக வீற்றிருக்கிறார்!",
        "s6_en": "Chanting the Narayana Gayatri—'Narayanaya Vidmahe Vasudevaya Dhimahi Tanno Vishnuh Prachodayat'—the seeker's consciousness merges into the self-luminous Lotus of Vaikuntha.",
        "s6_ta": "'நாராயணாய வித்மஹே வாஸுதேவாய தீமஹி தந்நோ விஷ்ணுஃ ப்ரசோதயாத்' என்ற நாராயண காயத்ரியைத் தியானித்த முனிவர்கள், தம் உள்ளத்திலேயே சிதானந்த வைகுண்டப் பேரொளியைத் தரிசித்தனர்.",
        "s7_en": "Whoever recites this Narayana Upanishad in the morning destroys the sins of the night; reciting it in the evening destroys the sins of the day; and reciting it at midday facing the Sun attains the supreme abode of Narayana!",
        "s7_ta": "இந்த நாராயண உபநிடதத்தை ஓதித் தியானிப்பவர் சகல பாவங்களிலிருந்தும் விடுபட்டு, பிறப்பற்ற நாராயணப் பரம்பொருளின் சாயுஜ்ய முக்தியை அடைகிறார்!"
    },
    {
        "story_id": "SAMANYA_26_ATMAPUJA_49",
        "muktika_number": 49,
        "upanishad_sanskrit": "आत्मपूजोपनिषद् (आत्मबोध-समन्वित)",
        "upanishad_iast": "Ātmapūjopaniṣad",
        "upanishad_tamil": "ஆத்மபூஜா / ஆத்மபோத உபநிடதம் (#49)",
        "upanishad_english": "Atmapuja / Atmabodha Samanya Upanishad (#49)",
        "veda": "Rig Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Sixteen-Limbed Worship of the Self: Every State of Awareness as Sacred Puja",
        "story_title_tamil": "ஆத்மாவிற்கே செய்யும் சோடச உபசார பூஜை: நிர்மல மௌனமே நமஸ்காரம்!",
        "characters": [
            "The Advaita Acharya of Atmapuja (Teaching the sixteen-limbed internal worship of the Self)",
            "Illumined Seekers (Replacing outer flowers with non-dual awareness)"
        ],
        "mahavakya_sanskrit": "तस्य निश्चिन्तनं ध्यानम् । सर्वकर्मविसर्जनमावाहनम् । निश्चलज्ञानमासनम् । चिदानन्दमयी दृष्टिः पाद्यम् ॥",
        "mahavakya_tamil_translit": "தஸ்ய நிஸ்சிந்தனம் த்யானம் | ஸர்வகர்ம விஸர்ஜனமாவாஹனம் | நிஸ்சலஜ்ஞானமாஸனம் | சிதானந்தமயீ த்ருஷ்டிஃ பாத்யம் ||",
        "mahavakya_meaning_english": "Thought-free stillness is Meditation; relinquishing egoic karma is Invocation (Avahana); unshakeable Wisdom is the Seat (Asana); and beholding Chidananda everywhere is the Offering!",
        "mahavakya_meaning_tamil": "எண்ணமற்ற நிர்மல நிலையே தியானம்; கர்ம அகங்காரத்தை விடுவதே ஆவாஹனம்; அசையாத ஞானமே ஆசனம்; எங்கும் சிதானந்தத்தைக் காண்பதே பாத்யம்!",
        "philosophical_theme": "Transforming all 16 traditional temple Upacharas (Avahana, Asana, Padya, Arghya, Snana, Dhupa, Dipa, Naivedya, Pradakshina, Namaskara) into direct Advaita Self-Abidance.",
        "setting_specifics": "A serene granite sanctum where a single oil lamp burns steadily beside a meditating sage.",
        "metaphor_highlight": "Shodasha-Upachara (Sixteen Temple Offerings translated into sixteen stages of Nirvikalpa Samadhi) and Silence as the highest Stuti.",
        "s1_en": "In the luminous Samanya Vedanta tradition (#49 in the Muktika canon), the sages asked: 'How does the knower of Non-Duality perform the sixteen-limbed Shodasha-Upachara Puja to the Formless Atman?'",
        "s1_ta": "சாமான்ய வேதாந்த மரபின் (முக்திக எண் #49) 'ஆத்மபூஜா / ஆத்மபோத உபநிடதத்தில்', முனிவர்கள் கேட்டனர்: 'உருவமற்ற இரண்டற்ற ஆத்மாவிற்குப் பதினாறு வகையான சோடச உபசார பூஜைகளை ஞானி எவ்வாறு செய்கிறான்?'",
        "s2_en": "The Acharya revealed the first four inner offerings: 'Om! Freedom from anxious thought is Dhyana! Letting go of ego-driven actions is Avahana (Invocation)! Unshakeable Self-Knowledge is Asana (the Throne)! And a gaze filled with Chidananda is Padya and Arghya!'",
        "s2_ta": "ஆச்சாரியர் முதல் நான்கு உபசாரங்களை விளக்கினார்: 'ஓம்! எண்ணங்களற்ற நிர்மல நிலையே தியானம்! கர்ம அகங்காரத்தை விடுவதே ஆவாஹனம்! அசையாத ஆத்ம ஞானமே ஆசனம்! எங்கும் சிதானந்தத்தைக் காணும் பார்வையே பாத்யமும் அர்க்கியமும் ஆகும்!'",
        "s3_en": "'Resting in eternal luminescence is Achamaniya! Immersing oneself in one's own innate Bliss is Snana (the Sacred Bath)! Seeing the one Atman in all beings is Gandha (Sandalwood paste)! And remaining established in the Witness-Consciousness is Akshata (unbroken rice)!'",
        "s3_ta": "'என்றும் குறையாத சுய ஒளியில் நிலைப்பதே ஆசமனீயம்! ஆத்ம ஆனந்தத்தில் மூழ்குவதே புனித நீராடல் (ஸ்நானம்)! எல்லா உயிர்களிலும் ஆத்மாவைக் காண்பதே சந்தனம்! சாட்சி சைதன்யத்தில் நிலைத்து நிற்பதே அக்ஷதை!'",
        "s4_en": "'Rising into pure Consciousness is Pushpa (the Flower offering)! Burning away all latent mental vasanas in the fire of wisdom is Dhupa (Incense)! And shining as the Self-Luminous Sun of Awareness is Dipa (the Sacred Lamp)!'",
        "s4_ta": "'தூய சித் சொரூபத்தில் மலர்வதே புஷ்பம்! வாசனைகளை ஞானத் தீயில் சுட்டெரிப்பதே தூபம்! சுயப் பிரகாசமான சைதன்ய சூரியனாய் ஒளிர்வதே மங்கல தீபம்!'",
        "s5_en": "'Gathering the rays of the mind into the nectar of the Full Moon of the Heart is Naivedya (Food-offering)! Complete stillness where no impulse moves is নিवेद्य-समर्पण! And dissolving all distinctions of time and space is Pradakshina (Circumambulation)!'",
        "s5_ta": "'மனக் கதிர்களை ஒன்றுதிரட்டிப் பூரண அமிர்தத்தில் லயிப்பதே நைவேத்தியம்! சலனமற்ற நிಶ್ಚல நிலையே தாம்பூலம்! கால-தேச எல்லைகளைக் கடந்து நிற்பதே பிரதக்ஷிணம்!'",
        "s6_en": "'Realizing So'ham—I am That Non-Dual Brahman—is Namaskara (Prostration)! And abiding in absolute Silence where words cannot reach is the highest Stuti (Hymn of Praise)!'",
        "s6_ta": "'அந்தப் பரம்பொருளே நான் (ஸோऽஹம்) என்று உணர்வதே நமஸ்காரம்! வாக்கு எட்ட முடியாத பரம மௌனத்தில் நிலைத்திருப்பதே மிகச் சிறந்த தோத்திரம் (ஸ்துதி)!'",
        "s7_en": "Performing this ceaseless Atma-Puja in every breath, the sage becomes liberated while living—Sarva-Niramaya, forever free from all sorrow!",
        "s7_ta": "இத்தகைய ஆத்ம பூஜையை இடைவிடாது நிகழ்த்தும் ஞானி, இப்பிறவியிலேயே சகல துயரங்களிலிருந்தும் விடுபட்டு ஜீவன்முக்தனாகத் திகழ்கிறான்!"
    },
    {
        "story_id": "SAMANYA_27_NIRVANA_47",
        "muktika_number": 47,
        "upanishad_sanskrit": "निर्वाणोपनिषद् (सामान्य-परमहंस समन्वित)",
        "upanishad_iast": "Nirvāṇopaniṣad",
        "upanishad_tamil": "நிர்வாண / சாமான்ய வேதாந்த சூத்திர உபநிடதம்",
        "upanishad_english": "Nirvana / Samanya Vedanta Sutra Upanishad",
        "veda": "Rig Veda",
        "category": "Samanya Vedanta",
        "story_title_english": "The Sky-Clad Sutras of Supreme Freedom: Where the Sky Is the Robe & Silence Is the Scripture",
        "story_title_tamil": "ஆகாயமே ஆடையாய் மௌனமே மந்திரமாய் ஒளிரும் நிர்வாண பிரம்ம சூத்திரங்கள்!",
        "characters": [
            "The Paramahamsa Avadhuta Rishi (Reciting the condensed aphorisms of non-dual freedom)",
            "Assembly of Siddhas (Contemplating the inner monastery of the Self)"
        ],
        "mahavakya_sanskrit": "अथातो निर्वाणोपनिषदं व्याख्यास्यामः । गगनं सिंहासनम्... अजपा गायत्री... तारकब्रह्मणि प्रविष्टः ॥",
        "mahavakya_tamil_translit": "அதாதோ நிர்வாணோபநிஷதம் வ்யாக்யாஸ்யாமஃ | ககனம் ஸிம்ஹாஸனம்... அஜபா காயத்ரீ... தாரகப்ரஹ்மணி ப்ரவிஷ்டஃ ||",
        "mahavakya_meaning_english": "Now we expound the Nirvana Upanishad: Boundless Space is his throne, Discrimination is his loincloth, Compassion is his play, and the Unchanted Breath is his Gayatri!",
        "mahavakya_meaning_tamil": "இதோ நிர்வாண உபநிடதத்தை உரைக்கிறோம்: எல்லையற்ற ஆகாயமே சிம்மாசனம், விவேகமே ஆடை, கருணையே திருவிளையாடல், அஜபா மூச்சே காயத்ரி மந்திரம்!",
        "philosophical_theme": "Condensed poetic sutras describing the inner life of the liberated sage where every external ascetic insignia is replaced by an attribute of Non-Dual Consciousness.",
        "setting_specifics": "A sunlit Himalayan mountain crest above the clouds where an Avadhuta sage sits in royal ease upon a flat granite rock.",
        "metaphor_highlight": "Sky as Throne (Gaganam Simhasanam), Viveka as Kaupina, Kshama as Krodha-jaya, and Ajapa Hamsa as Gayatri.",
        "s1_en": "In the aphoristic Samanya-Nirvana Upanishadic tradition of the Rig Veda, the Rishi speaks in lightning-like sutras to portray the inner sovereignty of the liberated sage: 'Atha nirvanopanishadam vyakhyasyamah—Now we expound the secret of Supreme Nirvana!'",
        "s1_ta": "ரிக் வேத உபநிடத மரபின் மின்னல் போன்ற சூத்திரங்களால் ஜீவன்முக்தனின் அகப் பேரரசை விவரிக்கிறது இவ்வுபநிடதம்: 'அத நிர்வாணோபநிஷதம் வ்யாக்யாஸ்யாமஃ — இதோ பரம நிர்வாண முக்தியின் ரகசியத்தை உரைக்கிறோம்!'",
        "s2_en": "'For the awakened sage, what is his monastery and what is his throne? Boundless Space—Gagana—is his royal throne! Pure Consciousness within the Heart is his monastery! Joy in the Self is his garland, and inner contentment is his sandals!'",
        "s2_ta": "'விழிப்புணர்வு பெற்ற ஞானிக்கு மடம் எது? சிம்மாசனம் எது? எல்லையற்ற ஆகாயமே அவனது சிம்மாசனம்! இதயத்தில் ஒளிரும் தூய பிரக்ஞையே அவனது மடம்! ஆத்ம ஆனந்தமே மாலை, மன நிறைவே பாதுகைகள்!'",
        "s3_en": "'What is his garment and his sacred thread? Discrimination (Viveka) is his loincloth; the four directions of space are his robe; and unbroken awareness of the Non-Dual Brahman is his Upavita (sacred thread)!'",
        "s3_ta": "'அவனது ஆடை எது? பூணூல் எது? விவேகமே அவனது கௌபீனம்; திசைகளே அவனது ஆடை; இரண்டற்ற பிரம்ம சிந்தனையே அவனது புனித பூணூல்!'",
        "s4_en": "'How does he view the world? He sees the entire play of Maya as a grand illusion, yet his conduct toward all creatures is pure Compassion (Karuna)! Patience is his invincible armor, and the natural Ajapa-Hamsa breath is his eternal Gayatri!'",
        "s4_ta": "'அவன் உலகை எவ்வாறு காண்கிறான்? மாயையின் தோற்றங்களைக் கனவாகக் கண்டாலும், எல்லா உயிர்களிடத்தும் பெருங்கருணையே (கருணா) அவனது செயல்! பொறுமையே அவனது கவசம்; இயல்பாக நடைபெறும் அஜபா-ஹம்ஸ மூச்சே அவனது நித்திய காயத்ரி!'",
        "s5_en": "'With the Yoga-patta of Equanimity wrapped around his knees, and the Danda-staff of Self-Inquiry in his hand, he beholds neither birth nor death, neither bondage nor liberation, for all is Satchidananda!'",
        "s5_ta": "'சமத்துவம் என்னும் யோகப் பட்டையைக் கட்டிக்கொண்டு, ஆத்ம விசாரணை என்னும் தண்டத்தை ஏந்திய அவனுக்குப் பிறப்புமில்லை, இறப்புமில்லை; எங்கும் சச்சிதானந்தம் ஒன்றே!'",
        "s6_en": "Entering into the Taraka-Brahman that carries all souls across the ocean of existence, the sage rests in unbroken turiya stillness.",
        "s6_ta": "பிறவிக் கடலைக் கடக்கச் செய்யும் தாரகப் பிரம்மத்தில் பிரவேசித்த அந்த ஞானி, அசைவற்ற துரீய அமைதியில் நிலைபெறுகிறான்.",
        "s7_en": "Whoever contemplates these diamond sutras of the Upanishad attains immediate peace and abides as the Sovereign Emperor of the Self!",
        "s7_ta": "வைரத் துளிகள் போன்ற இந்த உபநிடத சூத்திரங்களைத் தியானிப்பவன், உடனடியாக மன அமைதி பெற்று ஆத்ம சாம்ராஜ்யத்தின் சக்கரவர்த்தியாய் விளங்குகிறான்!"
    }
])


SHANTI_MANTRAS_BY_VEDA = {
    "Rig Veda": {
        "sanskrit": "ॐ वाङ्मे मनसि प्रतिष्ठिता मनो मे वाचि प्रतिष्ठितमाविरावीर्म एधि ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் வாங் மே மனஸி ப்ரதிஷ்டிதா மனோ மே வாசி ப்ரதிஷ்டிதம் ஆவிராவீர்ம ஏதி | ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "May my speech be established in my mind, and my mind in my speech; O Self-Luminous Brahman, be revealed unto me!"
    },
    "Shukla Yajur Veda": {
        "sanskrit": "ॐ पूर्णमदः पूर्णमिदं पूर्णात्पूर्णमुदच्यते । पूर्णस्य पूर्णमादाय पूर्णमेवावशिष्यते ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் பூர்ணமதஃ பூர்ணமிதம் பூர்ணாத் பூர்ணமுதச்யதே | பூர்ணஸ்ய பூர்ணமாதாய பூர்ணமேவாவஸிஷ்யதே || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "That Supreme Brahman is Whole, and this visible universe is Whole; from the Whole comes forth the Whole, and the Whole alone remains!"
    },
    "Krishna Yajur Veda": {
        "sanskrit": "ॐ सह नाववतु । सह नौ भुनक्तु । सह वीर्यं करवावहै । तेजस्वि नावधीतमस्तु मा विद्विषावहै ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் ஸஹ நாவவது | ஸஹ நௌ புனக்து | ஸஹ வீர்யம் கரவாவஹை | தேஜஸ்வி நாவதீதமஸ்து மா வித்விஷாவஹை || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "May the Lord protect us both (Guru and Disciple) together; may our study be radiant with Brahma-Tejas; may we never harbor disharmony!"
    },
    "Sama Veda": {
        "sanskrit": "ॐ आप्यायन्तु ममाङ्गानि वाक्प्राणश्चक्षुः श्रोत्रमथो बलमिन्द्रियाणि च सर्वाणि । सर्वं ब्रहौपनिषदं माऽहं ब्रह्म निराकुर्यां मा मा ब्रह्म निराकरोदनिराकरणमस्त्वनिराकरणं मेऽस्तु ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் ஆப்யாயந்து மமாங்கானி வாக்ப்ராணஸ்சக்ஷுஃ ஸ்ரோத்ரமதோ பலமிந்த்ரியாணி ச ஸர்வாணி | ஸர்வம் ப்ரஹ்மௌபநிஷதம் || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "May my limbs, speech, vital breath, eye, ear, and all senses grow strong for Self-Knowledge; all is the Upanishadic Brahman!"
    },
    "Atharva Veda": {
        "sanskrit": "ॐ भद्रं कर्णेभिः शृणुयाम देवा भद्रं पश्येमाक्षभिर्यजत्राः । स्थिरैरङ्गैस्तुष्टुवांसस्तनूभिर्व्यशेम देवहितं यदायुः ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "tamil": "ஓம் பத்ரம் கர்ணேபிஃ ஸ்ருணுயாம தேவா பத்ரம் பஸ்யேமாக்ஷபிர்யஜத்ராஃ | ஸ்திரைரங்கைஸ்துஷ்டுவாம்ஸஸ்தனூபிர் வ்யஸேம தேவஹிதம் யதாயுஃ || ஓம் சாந்திஃ சாந்திஃ சாந்திஃ ||",
        "meaning": "O Gods, may we hear with our ears what is auspicious; may we behold with our eyes what is auspicious and dedicate our life to the Divine!"
    }
}


def expand_samanya_spec_to_story(spec: dict) -> dict:
    """Expands a Samanya Vedanta specification into a full 7-scene story record."""
    setting = spec["setting_specifics"]
    chars_str = ", ".join(spec["characters"])
    metaphor = spec["metaphor_highlight"]
    upan_en = spec["upanishad_english"]
    upan_ta = spec["upanishad_tamil"]

    scenes_raw = [
        (
            "Slow 35mm cinematic dolly push-in across the sacred ashram at Brahmamuhurtham dawn; warm golden sunrise rays and Agnihotra firelight.",
            f"Cinematic 16:9 widescreen 8K 24fps photorealistic shot of {setting}. Revered Vedic sages and seekers ({chars_str[:90]}) dressed in authentic unstitched saffron and white cotton dhotis, Rudraksha malas, and vibhuti gather around a glowing sacred Homa fire altar. Golden morning mist, etched palm-leaf manuscripts and copper kamandalu nearby, zero modern elements, zero text, zero subtitles, zero borders.",
            spec["s1_en"],
            spec["s1_ta"],
            f"{upan_ta}: பிரம்ம ஞானத்தின் புனிதத் தொடக்கம்!",
            f"Deep Tanpura drone in Shadjam, {spec['veda']} invocation, gentle river water and crackling sacred Homa fire."
        ),
        (
            "Low-angle medium orbit shot around the Guru and seeker; warm firelight illuminating etched palm leaves and sacred mudras.",
            f"Photorealistic 8K 24fps 16:9 medium shot inside {setting}. The illumined Guru raises his right hand in Chinmudra while testing and instructing the devoted disciple beside the sacred fire. Subtle golden light highlights {metaphor[:80]}, authentic ancient Bharata Gurukulam atmosphere, no modern objects, no text, no borders.",
            spec["s2_en"],
            spec["s2_ta"],
            f"{upan_ta}: ஆத்ம விசாரணையின் தகுதியும் சத்திய நெறியும்!",
            "Resonant Veena alapana in Raga Bhupalam with subtle temple bronze bell chimes."
        ),
        (
            "Dynamic tracking and rack-focus shot illustrating the Upanishadic metaphor and dismantling the outer layer of illusion (Purvapaksha).",
            f"16:9 8K 24fps photorealistic sequence in {setting} visually depicting the sacred metaphor of {metaphor}. Sages in traditional dhotis and Rudraksha beads observe with deep philosophical wonder as golden sunlight pierces the morning mist, pure Vedic aesthetic, no text, no watermarks, no borders.",
            spec["s3_en"],
            spec["s3_ta"],
            f"மாயையின் வெளித்திரையை விலக்கும் {upan_ta} உபதேசம்!",
            "Rhythmic Mridangam pulse steady and contemplative beneath melodic Bansuri flute phrases."
        ),
        (
            "Macro-to-wide contemplation shot revealing the deeper spiritual experiment and inner meditative alignment (Drishtanta).",
            f"Cinematic 8K 24fps 16:9 macro-to-wide shot in {setting}. Foreground shows sacred Vedic symbols and {metaphor[:75]} bathed in warm oil-lamp and sunrise glow; background reveals the Acharya and disciples seated in serene Padmasana meditation, zero modern items, zero text, zero borders.",
            spec["s4_en"],
            spec["s4_ta"],
            f"உவமை வழியே ஆத்ம சத்தியத்தை விளக்கும் திருष्टாந்தம்!",
            "Soaring Bansuri flute and Violin duet echoing across the tranquil hermitage."
        ),
        (
            "Majestic crane rise at the climax of Upadesha as the Mahavakya is proclaimed and golden light floods the sanctum (Siddhanta).",
            f"Epic 16:9 8K 24fps photorealistic crane shot at sunrise in {setting}. As the Guru proclaims the supreme Mahavakya, brilliant golden sunbeams pierce the canopy and illuminate the heart-lotus of the seeker in Anjali mudra. Sacred Homa flames rise peacefully, deeply spiritual Vedic grandeur, no text, no subtitles, no borders.",
            spec["s5_en"],
            spec["s5_ta"],
            f"மகா வாக்கிய முழக்கம்: {spec['mahavakya_meaning_tamil'][:78]}",
            "Full-voiced Vedic chanting of the Mahavakya, resonant Shankha (conch) blow and deep temple gong."
        ),
        (
            "Slow 360-degree ethereal push-in on the awakened seeker in Nirvikalpa Samadhi as microcosm and macrocosm unite (Aparoksha Anubhuti).",
            f"Photorealistic 8K 24fps 16:9 spiritual realization shot in {setting}. The awakened seeker sits in motionless Padmasana with a serene, blissful smile as subtle golden-white radiance unites the inner heart cave with the boundless sky and river outside, pure Advaita stillness, no text, no borders.",
            spec["s6_en"],
            spec["s6_ta"],
            "அபரோக்ஷ அனுபூதி — இரண்டற்ற ஆத்ம பேரானந்த அனுபவம்!",
            "Ethereal Swarmandal harp glissando, celestial Tanpura hum, and tranquil nature ambience."
        ),
        (
            "Wide symmetrical locked-off closing tableau of the Gurukulam bathed in golden morning light, crane slowly pulling back over blooming lotuses.",
            f"Wide 16:9 8K 24fps photorealistic final tableau of {setting} in full golden morning light. The Acharya and illumined disciples chant the Shanti Mantra in unison around the sacred fire while white swans and blooming lotuses grace the water nearby, zero modern elements, zero text, zero borders.",
            spec["s7_en"],
            spec["s7_ta"],
            f"{SHANTI_MANTRAS_BY_VEDA[spec['veda']]['tamil']}",
            f"Unison Gurukulam Vedic chorus chanting {spec['veda']} Shanti Mantra, fading out with Tanpura and temple bells."
        )
    ]

    scenes_built = []
    for idx, (cam, veo, n_en, n_ta, sub_cue, snd_cue) in enumerate(scenes_raw):
        scenes_built.append({
            "camera": cam,
            "veo_prompt": veo,
            "narration_en": n_en,
            "narration_ta": n_ta,
            "subtitle_cue": sub_cue,
            "sound_cue": snd_cue
        })

    out = dict(spec)
    out["scenes"] = scenes_built
    return out


def build_youtube_metadata(story: dict) -> dict:
    """Builds 16:9 YouTube Long-Form Metadata Block (< 4850 UTF-8 bytes)."""
    m_num = story["muktika_number"]
    u_en = story["upanishad_english"]
    u_ta = story["upanishad_tamil"]
    t_en = story["story_title_english"]
    t_ta = story["story_title_tamil"]
    veda = story["veda"]
    cat = story["category"]

    yt_title_ta = f"{u_ta} | {t_ta} | Muktika #{m_num:03d} | Guru Kula Desam"
    yt_title_en = f"{u_en} (#{m_num:03d}): {t_en} | 16:9 4K Vedanta Story | Guru Kula Desam"
    hook_en = story["scenes"][0]["narration_en"][:220] + "..."
    hook_ta = story["scenes"][0]["narration_ta"][:220] + "..."

    desc = (
        f"🔱 {u_ta} ({u_en} — Muktika Canon #{m_num:03d}) 🔱\n"
        f"📖 {t_ta}\n"
        f"🌍 {t_en}\n\n"
        f"🏛️ Veda: {veda} | Category: {cat} Upanishad\n"
        f"🕉️ Core Mahavakya:\n"
        f"{story['mahavakya_sanskrit']}\n"
        f"{story['mahavakya_tamil_translit']}\n\n"
        f"✨ Meaning (Tamil): {story['mahavakya_meaning_tamil']}\n"
        f"✨ Meaning (English): {story['mahavakya_meaning_english']}\n\n"
        f"⏱️ 7-Scene 16:9 Master Film Chapters:\n"
        f"00:00 - Scene 1: The Sacred Setting & The Seeker's Question (Upakrama)\n"
        f"00:45 - Scene 2: The Encounter / The Trial of Qualification (Adhikara & Pariksha)\n"
        f"01:30 - Scene 3: The First Teaching / The Outer Layer of Illusion (Purvapaksha)\n"
        f"02:15 - Scene 4: The Deeper Inquiry & Sacred Experiment / Metaphor (Drishtanta)\n"
        f"03:00 - Scene 5: The Climax of Upadesha / The Mahavakya Revelation (Siddhanta)\n"
        f"03:45 - Scene 6: Direct Realization & Cosmic Vision (Aparoksha Anubhuti)\n"
        f"04:30 - Scene 7: The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)\n\n"
        f"🔔 Subscribe to @guru-kula-desam for authentic 108 Upanishads, Thirukkural & South Indian Devotional Master Films.\n"
        f"#Upanishads #GuruKulaDesam #Vedanta #{u_en.replace(' ', '').replace('(', '').replace(')', '')} #TamilSpiritual #Mahavakya #SanatanaDharma"
    )
    # Ensure strict < 4850 UTF-8 bytes
    while len(desc.encode("utf-8")) > 4800:
        desc = desc[:-50]

    tags = [
        "Guru Kula Desam", "108 Upanishads", "Upanishad Stories Tamil", "Upanishad Stories English",
        u_en, u_ta, veda, cat, "Advaita Vedanta", "Mahavakya", f"Muktika {m_num}",
        "Vedic Gurukulam", "Adi Shankaracharya", "Brahmavidya"
    ]
    return {
        "youtube_title_tamil": yt_title_ta,
        "youtube_title_english": yt_title_en,
        "youtube_hook_tamil": hook_ta,
        "youtube_hook_english": hook_en,
        "youtube_description": desc,
        "youtube_description_utf8_bytes": len(desc.encode("utf-8")),
        "youtube_tags": tags
    }


def enrich_story_record(raw_story: dict) -> dict:
    """Enriches a story dictionary with full canonical scene structure and YouTube metadata."""
    shanti = SHANTI_MANTRAS_BY_VEDA[raw_story["veda"]]
    yt_meta = build_youtube_metadata(raw_story)

    enriched_scenes = []
    for idx, sc in enumerate(raw_story["scenes"]):
        sc_num, dur_win, sc_arc_title = SCENE_TEMPLATE_WINDOWS[idx]
        enriched_scenes.append({
            "scene_number": idx + 1,
            "scene_id": f"{raw_story['story_id']}_S0{idx + 1}",
            "scene_title": f"{sc_num} ({dur_win}): {sc_arc_title}",
            "duration_window": dur_win,
            "narrative_stage": sc_arc_title,
            "camera_and_cinematography": sc["camera"],
            "veo_16_9_video_prompt": sc["veo_prompt"],
            "voiceover_english": sc["narration_en"],
            "voiceover_tamil": sc["narration_ta"],
            "on_screen_subtitle_cue": sc["subtitle_cue"],
            "sound_design_and_sangeetham_cue": sc["sound_cue"]
        })

    visual_bible = dict(LOCKED_VISUAL_BIBLE_BASE)
    visual_bible["story_specific_setting"] = raw_story["setting_specifics"]
    visual_bible["signature_visual_metaphor"] = raw_story["metaphor_highlight"]

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
        "youtube_metadata": yt_meta,
        "locked_visual_continuity_bible": visual_bible,
        "scenes": enriched_scenes
    }


def render_markdown(story: dict) -> str:
    """Renders a complete, production-ready 7-Scene Markdown document for a story."""
    u = story["upanishad_names"]
    mv = story["core_mahavakya"]
    sm = story["shanti_mantra"]
    yt = story["youtube_metadata"]
    vb = story["locked_visual_continuity_bible"]
    chars_md = "\n".join(f"  - {c}" for c in story["key_characters"])
    tags_md = ", ".join(f"`{t}`" for t in yt["youtube_tags"])

    lines = [
        f"# {story['story_id']} — {u['english']} (Muktika #{story['muktika_number']:03d})",
        f"## {story['story_title']['english']}",
        f"### {story['story_title']['tamil']}",
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
        "## 2. Locked Visual Continuity Bible (16:9 8K 24fps)",
        "",
        f"- **Aspect Ratio & Cinema Spec**: {vb['aspect_ratio_and_format']}",
        f"- **Historical Epoch & Setting**: {vb['historical_epoch_and_setting']}",
        f"- **Story-Specific Sacred Setting**: {vb['story_specific_setting']}",
        f"- **Signature Visual Metaphor / Drishtanta**: {vb['signature_visual_metaphor']}",
        f"- **Lighting & Color Palette**: {vb['lighting_and_color_palette']}",
        f"- **Costume & Prop Continuity**: {vb['costume_and_prop_continuity']}",
        f"- **Hard Negative Exclusions**: {vb['hard_negative_exclusions']}",
        f"- **8-Layer Compositing Compatibility**: {vb['8_layer_compositing_note']}",
        "",
        "---",
        "",
        "## 3. Full 7-Scene Detailed Screenplay Breakdown (00:00 – 05:15)",
        ""
    ]

    for sc in story["scenes"]:
        lines.extend([
            f"### {sc['scene_title']}",
            "",
            f"- **Scene ID**: `{sc['scene_id']}`",
            f"- **Duration Window**: `{sc['duration_window']}` (45 seconds)",
            f"- **Camera & Cinematography**: {sc['camera_and_cinematography']}",
            f"- **Google Flow / Veo 16:9 Video Generation Prompt**:",
            f"  > `{sc['veo_16_9_video_prompt']}`",
            f"- **Voiceover / Narration Script (English)**:",
            f"  > {sc['voiceover_english']}",
            f"- **Voiceover / Narration Script (Tamil - செந்தமிழ் உரைநடை)**:",
            f"  > {sc['voiceover_tamil']}",
            f"- **On-Screen Subtitle / Verse Cue (Layer 8 WhisperX / ASS)**:",
            f"  > `{sc['on_screen_subtitle_cue']}`",
            f"- **Sound Design & Sangeetham Cue**:",
            f"  > {sc['sound_design_and_sangeetham_cue']}",
            ""
        ])

    return "\n".join(lines)


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return s[:65]


def main():
    MUKHYA_DIR.mkdir(parents=True, exist_ok=True)
    SAMANYA_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)

    raw_mukhya_all = MUKHYA_PART1 + MUKHYA_PART2 + MUKHYA_PART3 + MUKHYA_PART4 + MUKHYA_PART5
    raw_samanya_all = [expand_samanya_spec_to_story(sp) for sp in SAMANYA_SPECS]

    mukhya_enriched = []
    for st in raw_mukhya_all:
        enr = enrich_story_record(st)
        fname = f"{enr['story_id']}_Muktika{enr['muktika_number']:03d}_{slugify(enr['upanishad_names']['english'])}.md"
        fpath = MUKHYA_DIR / fname
        enr["markdown_file_path"] = str(fpath)
        fpath.write_text(render_markdown(enr), encoding="utf-8")
        mukhya_enriched.append(enr)

    samanya_enriched = []
    for st in raw_samanya_all:
        enr = enrich_story_record(st)
        fname = f"{enr['story_id']}_Muktika{enr['muktika_number']:03d}_{slugify(enr['upanishad_names']['english'])}.md"
        fpath = SAMANYA_DIR / fname
        enr["markdown_file_path"] = str(fpath)
        fpath.write_text(render_markdown(enr), encoding="utf-8")
        samanya_enriched.append(enr)

    all_stories = mukhya_enriched + samanya_enriched
    unique_muktika_nums = sorted(list({s["muktika_number"] for s in all_stories}))

    dataset = {
        "agent": "Agent 1: Mukhya & Samanya Vedanta Upanishads Story & 7-Scene Screenplay Architect",
        "channel": "@guru-kula-desam",
        "aspect_ratio": "16:9 Widescreen Long-Form (00:00 - 05:15 per 7-Scene Film)",
        "summary_counts": {
            "total_story_documents": len(all_stories),
            "mukhya_upanishad_stories_count": len(mukhya_enriched),
            "mukhya_distinct_upanishads_count": len({s["muktika_number"] for s in mukhya_enriched}),
            "samanya_vedanta_stories_count": len(samanya_enriched),
            "total_7_scene_prompts_generated": len(all_stories) * 7,
            "unique_muktika_numbers_covered": unique_muktika_nums
        },
        "mukhya_upanishad_stories": mukhya_enriched,
        "samanya_vedanta_upanishad_stories": samanya_enriched
    }

    JSON_OUT.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SUCCESS] Generated {len(mukhya_enriched)} Mukhya story .md files in {MUKHYA_DIR}")
    print(f"[SUCCESS] Generated {len(samanya_enriched)} Samanya Vedanta story .md files in {SAMANYA_DIR}")
    print(f"[SUCCESS] Generated master JSON dataset at {JSON_OUT} ({len(all_stories)} total stories, {len(all_stories)*7} total scenes)")


if __name__ == "__main__":
    main()
