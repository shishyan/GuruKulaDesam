#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 2: Sannyasa & Yoga Upanishads Story & 7-Scene Screenplay Architect
Generates:
- 19 Sannyasa Upanishads in /home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/03_sannyasa_upanishads/
- 20 Yoga Upanishads in /home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/04_yoga_upanishads/
- Comprehensive JSON dataset in /home/shishyan/GitHub/GuruKulaDesam/data/upanishads/agent2_sannyasa_yoga.json
"""

import os
import json
import re

BASE_DIR = "/home/shishyan/GitHub/GuruKulaDesam"
SANNYASA_DIR = os.path.join(BASE_DIR, "production", "upanishad_stories", "03_sannyasa_upanishads")
YOGA_DIR = os.path.join(BASE_DIR, "production", "upanishad_stories", "04_yoga_upanishads")
JSON_OUT = os.path.join(BASE_DIR, "data", "upanishads", "agent2_sannyasa_yoga.json")

LOCKED_VISUAL_BIBLE = {
    "aesthetic": "Authentic ancient Bharata / Himalayan & Kaveri forest hermitage / Yogic cave / South Indian granite mandapam aesthetic",
    "resolution_fps": "16:9 widescreen, 8K photorealistic cinema, 24fps",
    "lighting": "Sacred golden dawn rays, earthen oil-lamp glow, and subtle yogic prana golden-prismatic illumination",
    "costume_props": "Handwoven unbleached cotton, bark-cloth (valkala), rudraksha malas, sacred vibhuti, kamandalu, wooden danda, ancient palm-leaf manuscripts, sacred homa fire",
    "hard_exclusions": "Zero modern elements, zero synthetic fabrics, zero modern architecture, zero on-screen text, zero subtitles, zero watermarks, zero borders or frames, zero anatomical distortions"
}

UPANISHADS_DATA = []

UPANISHADS_DATA.extend([
    # 1. BRAHMA UPANISHAD (#11)
    {
        "story_id": "SANNYASA_01_BRAHMA",
        "muktika_number": 11,
        "name_sanskrit": "ब्रह्मोपनिषद्",
        "name_iast": "Brahmopaniṣad",
        "name_tamil": "பிரம்ம உபநிடதம்",
        "name_english": "Brahma Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "The Sacred Thread of Pure Consciousness: Pippalada & Shaunaka",
        "story_title_tamil": "தூய உணர்வின் பிரம்ம சூத்திரம்: பிப்பலாதர் மற்றும் சௌனகர்",
        "characters": "Maharishi Shaunaka (Great Householder Seeker), Sage Pippalada (Vedic Master of Angiras Gotra), The Four States of Consciousness (Jagarita, Svapna, Sushupti, Turiya)",
        "verse_sanskrit": "यಜ್ಞोपवीतं परमं पवित्रं प्रजापतेर्यत्सहजं पुरस्तात् । आयुष्यमग्र्यं प्रतिमुञ्च शुभ्रं यज्ञोपवीतं बलमस्तु तेजः ॥ सशिखं वपनं कृत्वा बहिःसूत्रं त्यजेद्बुधः । यदक्षरं परं ब्रह्म तत्सूत्रं धारयेत्सुधीः ॥",
        "verse_tamil_translit": "சஷிகம் வபனம் க்ருத்வா பஹி:ஸூத்ரம் த்யஜேத் புத: | யதக்ஷரம் பரம் ப்ரஹ்ம தத்ஸூத்ரம் தாரயேத் ஸுதீ: ||",
        "verse_meaning_english": "Having shaved the head along with the tuft of hair, the wise sage should cast away the external thread; instead, let the illumined one wear as his thread the Imperishable Supreme Brahman on which the entire universe is strung like pearls.",
        "verse_meaning_tamil": "சடையுடன் தலைமுடியை மழித்து, ஞானியானவன் புறப் பூணூலைத் துறக்க வேண்டும்; மாறாக, முத்துக்கள் கோர்க்கப்பட்ட கயிறு போல இப் பிரபஞ்சம் அனைத்தும் எதில் ஊடுருவி நிற்கிறதோ, அந்த அழிவற்ற பரம்பொருளையே தனது அகப் பூணூலாக தரிக்க வேண்டும்.",
        "theme": "Transition from ritualistic external symbols (Yajnopavita and Shikha) to direct realization of the four states of consciousness and the all-pervading Atman, culminating in churning the inner fire of Brahman.",
        "SettingVisual": "Ancient Kaveri riverbank hermitage beneath a towering sacred Banyan tree at golden dawn, thatched Vedic cottages and a glowing homa fire pit",
        "ProtagonistVisual": "Maharishi Shaunaka, an elderly dignified Vedic scholar with silver beard, rudraksha beads, white cotton dhoti, and prominent triple sacred cotton thread across his chest",
        "GuruVisual": "Sage Pippalada, radiant ascetic master seated on a kusha grass mat, luminous serene eyes, vibhuti on forehead, bare chest without external thread, radiating golden prana",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow cinematic dolly-in at 24fps from mist-covered Kaveri river waters toward the ancient Banyan tree hermitage, settling on a medium two-shot of Shaunaka bowing before Sage Pippalada.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of an ancient Bharata forest hermitage by the Kaveri river at golden dawn. Dignified elderly Vedic scholar Shaunaka with silver beard and white cotton dhoti bows humbly with folded hands before radiant Sage Pippalada seated on kusha grass under a grand banyan tree. Sacred homa fire smoke rises gently in golden morning sunlight. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the serene forest hermitage of ancient Bharata, the great householder Maharishi Shaunaka approached Sage Pippalada of the Angiras lineage. Having mastered every Vedic sacrifice, Shaunaka still hungered for the ultimate truth. Gently bowing, he asked: 'O Revered Master, how is this divine body structured as the city of Brahman, and how does the Self shine within it?'",
                "vo_ta": "பண்டைய பாரதத்தின் அமைதியான வன ஆசிரமத்தில், மகா கிருஹஸ்தரான சௌனக மகரிஷி ஆங்கிரச குலத்து முனிவரான பிப்பலாதரை அணுகினார். சகல வேத வேள்விகளிலும் கரைகண்டிருந்தும், சௌனகரின் உள்ளம் பரம சத்தியத்திற்காக ஏங்கியது. பணிவுடன் வணங்கிய அவர், 'பூஜ்ய குருவே! இந்த திவ்ய சரீரம் எவ்வாறு பிரம்மபுரியாக அமைந்துள்ளது? இதில் ஆத்ம ஜோதி எவ்வாறு பிரகாசிக்கிறது?' என்று கேட்டார்.",
                "sub_cue": "Shaunaka questions Pippalada: 'How does the Self shine within this divine city of Brahman?'",
                "sound": "Gentle Kaveri river water flow, morning koel birdsong, soft crackling of sacred homa fire, and a deep resonant Tanpura drone in Raga Bhupalam."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Slow orbital arc shot around Sage Pippalada and Shaunaka, transitioning to an intimate close-up of Shaunaka's hand touching his sacred cotton thread.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up cinematic shot inside an ancient Vedic ashram. Sage Pippalada gazes with compassionate intensity at elderly seeker Shaunaka, who looks down thoughtfully at the white cotton sacred thread across his chest. Warm golden morning light filters through banyan leaves, illuminating dust motes and rudraksha beads. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Pippalada beheld Shaunaka's readiness and tested his attachment to outer identity. 'O Shaunaka,' the Guru spoke, 'within this body dwell the sensory deities—fire, wind, sun, and moon—moving like breaths at the command of Prana. Yet can mere outer emblems of caste, ritual tuft, or cotton thread reveal the Witness of Prana?'",
                "vo_ta": "சௌனகரின் பக்குவத்தைக் கண்ட பிப்பலாதர், புற அடையாளங்களின் மீதான அவரது பற்றைச் சோதித்தார். 'சௌனகா! இந்த உடலினுள் அக்னி, வாயு, சூரியன், சந்திரன் ஆகிய தேவர்கள் பிராணனின் ஆணைக்குக் கட்டுப்பட்டு இயங்குகின்றனர். ஆனால், வெறும் புறச் சின்னங்களான குடுமியும் பருத்திப் பூணூலும் அந்தப் பிராணனின் சாட்சியைக் காட்டிடுமோ?' என்று வினவினார்.",
                "sub_cue": "Can external emblems of ritual reveal the Eternal Witness of Prana?",
                "sound": "Subtle bamboo flute motif entering over the Tanpura drone, accompanied by soft rustling of banyan leaves."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium tracking shot moving across four symbolic earthen lamps arranged before Pippalada, with subtle golden prana light glowing around the throat, heart, and crown of the meditating disciple.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of Sage Pippalada instructing Shaunaka beside four glowing earthen oil lamps in a stone-and-thatch hermitage. Subtle translucent golden yogic prana light glows softly at Shaunaka's eyes, throat, and heart lotus as he meditates deeply. Rich warm chiaroscuro lighting, ancient Indian aesthetic. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Pippalada revealed the four seats of the Purusha: in the eye during waking, in the throat during dream, in the heart Lotus during deep sleep, and in the crown of the head in the fourth transcendent state, Turiya. Because the Self unites with the Imperishable in deep stillness, that state is called Sandhya—the true sacred twilight meditation.",
                "vo_ta": "புருஷனின் நான்கு இருப்பிடங்களை பிப்பலாதர் விளக்கினார்: விழிப்பு நிலையில் கண்ணிலும், கனவு நிலையில் கண்டத்திலும், ஆழ்ந்த உறக்கத்தில் இதயத் தாமரையிலும், துரியம் எனும் நான்காவது நிலையில் சிரசின் உச்சியிலும் ஆத்மா உறைகிறது. ஆழ்ந்த மௌனத்தில் அழிவற்ற பரம்பொருளுடன் ஆத்மா இணையுமிடமே உண்மையான 'சந்தியா' கால தியானமாகும்.",
                "sub_cue": "Eye in Waking, Throat in Dream, Heart in Sleep, Crown in Turiya — the Four Seats of Atman.",
                "sound": "Deep Vedic Mridangam pulse at 60 BPM, layered with a meditative Veena melody in Raga Shankarabharanam."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Macro-to-medium cinematic transition showing a wooden churning rod igniting fire in arani wood, cross-dissolving to glowing golden light radiating like oil inside sesame seeds and ghee inside milk.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of ancient Vedic fire-churning arani wood sparking with golden flame beside an earthen bowl of pure white milk and sesame seeds, transitioning to Sage Pippalada and Shaunaka in deep dhyana with golden light radiating from their hearts. Warm sacred illumination, authentic ancient ashram. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "As oil is hidden within sesame seeds, as clarified butter pervades milk, as fragrance dwells in flowers, and as fire sleeps within arani wood—so does the Supreme Self pervade every limb of this body. By making one's own body the lower fire-stick and the sacred syllable Om the upper rod, one must churn the flame of Dhyana to behold the hidden Lord.",
                "vo_ta": "எள்ளில் எண்ணெய் போலவும், பாலில் நெய் போலவும், மலரில் நறுமணம் போலவும், அரணிக்கட்டையில் நெருப்பு போலவும் பரமாத்மா இவ்வுடலின் ஒவ்வொரு அணுவிலும் மறைந்துள்ளார். தன் உடலையே கீழ்க்கட்டையாகவும், ஓங்காரத்தையே மேல்கட்டையாகவும் கொண்டு, தியானம் எனும் கடைதலால் உள்ளிருக்கும் இறைச் சுடரைத் தரிசிக்க வேண்டும்.",
                "sub_cue": "As butter in milk and fire in wood, churn the body with Omkara to behold the hidden Self.",
                "sound": "Rhythmic friction sound of wooden arani churning, rising into a luminous harmonic chime and resonant Omkara chant."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic slow-motion 24fps close-up as a shaved-head sannyasin removes the outer cotton thread and offers it to the sacred river, while a brilliant golden thread of light illuminates his heart center.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic cinematic shot of an awakened ancient Indian sannyasin with shaven head standing waist-deep in the golden dawn waters of the Kaveri river, gently releasing his white cotton sacred thread into the flowing water while a luminous golden aura of pure consciousness shines from his heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then spoke Pippalada the thunderous command of Sannyasa: 'Shaving the head along with the ritual tuft, let the wise man cast off the external thread! That Imperishable Supreme Brahman on which this entire cosmos is woven like pearls upon a string—let the knower of Truth wear that alone as his eternal Upavita!'",
                "vo_ta": "அப்போது பிப்பலாதர் சந்நியாசத்தின் சிம்மநாத உபதேசத்தை அருளினார்: 'குடுமியுடன் தலைமுடியை மழித்து, ஞானியானவன் புறப் பூணூலைத் துறப்பானாக! முத்துக்கள் கோர்க்கப்பட்ட கயிறு போல இப் பிரபஞ்சம் அனைத்தும் எதில் ஊடுருவி நிற்கிறதோ, அந்த அழிவற்ற பரப்பிரம்மத்தையே தனது நித்திய பூணூலாக ஞானி தரிப்பானாக!'",
                "sub_cue": "सशिखं वपनं कृत्वा बहिःसूत्रं त्यजेद्बुधः — Cast off the outer thread; wear Supreme Brahman as your Sutra!",
                "sound": "Crescendo of temple conch (Shankha) and gentle river splash, resolving into an ethereal, spacious flute solo."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide crane shot rising above the banyan canopy as the ascetic walks serene and unattached, surrounded by a subtle golden cosmic web connecting trees, river, birds, and stars.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an illumined barefoot Indian ascetic in ochre valkala cloth sitting in nirvikalpa samadhi beneath a giant banyan tree. Subtle golden threads of light connect his heart to the river, trees, and morning sky, depicting the one Divine glowing in all beings. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Abiding in that realization, Shaunaka beheld the One Deva hidden in all beings, all-pervading, the inner soul of every creature, the witness, pure consciousness free of gunas. For such a Paramahamsa whose knowledge itself is his sacred tuft and whose nishtha in Brahman is his sacred thread, there is no longer any bondage or rebirth.",
                "vo_ta": "அந்த மெய்ஞ்ஞானத்தில் நிலைபெற்ற சௌனகர், எல்லா உயிர்களிலும் மறைந்திருக்கும் ஒரே தேவனையும், எங்கும் நிறைந்த உள்சாட்சியையும், முக்குணங்களற்ற தூய சைதன்யத்தையும் நேருக்கு நேர் தரிசித்தார். ஞானத்தையே தனது குடுமியாகவும், பிரம்ம நிஷ்டையையே தனது பூணூலாகவும் கொண்ட அத்தகைய பரமஹம்சருக்கு இனிப் பிறவித் தளையோ பந்தமோ இல்லை.",
                "sub_cue": "One God hidden in all beings, all-pervading, the Inner Witness free of all Gunas.",
                "sound": "Expansive celestial choir of Vedic voices humming 'Aum' in fifths, with gentle Saraswati Veena arpeggios."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow pull-back shot from the glowing hermitage out over the golden sunlit Kaveri valley as Pippalada raises his hand in abhaya mudra.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps serene pull-back shot of Sage Pippalada raising his right hand in abhaya blessing mudra beside the Kaveri river at sunrise, while Shaunaka sits in tranquil bliss. Golden sunlight bathes the ancient granite stones and forest canopy. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Brahma Upanishad: the true brahmin is not made by cotton threads or outer marks, but by weaving one's awareness into the seamless fabric of the Absolute. May our inner eye awaken to that one luminous thread of Consciousness that binds all existence in eternal peace. Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பிரம்ம உபநிடதம் நிறைவுறுகிறது: உண்மையான பிரம்மஞானி பருத்தி நூலாலோ புற அடையாளங்களாலோ உருவாவதில்லை; மாறாக தன் உணர்வை பரம்பொருளின் பிரிக்க முடியாத இழையோடு இணைப்பவனே ஞானி ஆவான். சகல உயிர்களையும் அன்பிலும் அமைதியிலும் பிணைக்கும் அந்த ஆத்ம சூத்திரத்தை நாம் அனைவரும் உணர்வோமாக. ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Weave your awareness into the seamless thread of Supreme Consciousness. Om Shanti.",
                "sound": "Resonant bronze temple bell chime, fading smoothly into the peaceful murmur of the Kaveri river and Tanpura resonance."
            }
        ]
    },
    # 2. JABALA UPANISHAD (#13)
    {
        "story_id": "SANNYASA_02_JABALA",
        "muktika_number": 13,
        "name_sanskrit": "जाबालोपनिषद्",
        "name_iast": "Jābālopaniṣad",
        "name_tamil": "ஜாபால உபநிடதம்",
        "name_english": "Jabala Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "The Day Detachment Dawns: Yajnavalkya, Janaka & Brihaspati",
        "story_title_tamil": "வைராக்கியம் பிறக்கும் கணமே சந்நியாசம்: யாக்ஞவல்கியர் மற்றும் ஜனகர்",
        "characters": "Maharishi Yajnavalkya (Illumined Sage), Deva Guru Brihaspati, King Janaka of Videha, Atri Maharishi",
        "verse_sanskrit": "ब्रह्मचर्यं समाप्य गृही भवेद्गृही भूत्वा वनी भवेद्वनी भूत्वा प्रव्रजेत् । यदि वेतरथा ब्रह्मचर्यादेव प्रव्रजेद्गृहाद्वा वनाद्वा । यदहरेव विरजेत्तदहरेव प्रव्रजेत् ॥",
        "verse_tamil_translit": "யதஹரேவ விரஜேத் ததஹரேவ ப்ரவ்ரஜேத் |",
        "verse_meaning_english": "Finishing studenthood, let one become a householder; after householding, a forest-dweller; after forest-dwelling, let one renounce. Or else, whether from studenthood, household, or forest—the very day detachment dawns, that very day let one embrace renunciation!",
        "verse_meaning_tamil": "பிரம்மச்சரியம் முடித்து இல்லறத்தானாகி, பின் வானப்பிரஸ்தனாகி, அதன்பின் துறவு பூணலாம். அல்லது பிரம்மச்சரியத்திலிருந்தோ, இல்லறத்திலிருந்தோ, வனத்திலிருந்தோ—எந்த நாளில் மனதில் முழுமையான வைராக்கியம் பிறக்கிறதோ, அன்றே, அக்கணமே சந்நியாசம் மேற்கொள்ளலாம்!",
        "theme": "The inner geographical discovery of Avimukta (Varanasi) between the eyebrows (Varana and Nasi), and the revolutionary declaration that true Sannyasa depends solely on inner Vairagya (detachment), transcending all external fires and emblems.",
        "SettingVisual": "Magnificent Videha stone mandapam overlooking the sacred Ganges and a tranquil forest ashram glowing with evening oil lamps",
        "ProtagonistVisual": "King Janaka of Videha and Sage Atri, earnest seekers in royal unstitched silk and bark-cloth respectively, bowing with humility",
        "GuruVisual": "Maharishi Yajnavalkya, towering Vedic sage with flowing white hair and beard, radiant golden aura, wearing simple unbleached ochre cloth",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide sweeping crane shot of an ancient carved stone mandapam at dusk, gliding inward as Brihaspati and King Janaka sit before Maharishi Yajnavalkya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic wide shot of an ancient Indian carved granite mandapam at golden sunset. Maharishi Yajnavalkya with flowing white beard sits on a raised stone seat surrounded by brass oil lamps, as Brihaspati and King Janaka bow reverently before him. Warm golden-amber light, sacred atmosphere. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the sacred assembly of Videha, Brihaspati Himself first questioned Maharishi Yajnavalkya: 'Tell me, O Sage, what is Kurukshetra, the true sacrificial field of the gods, and what is Avimukta, the place never forsaken by the Lord, where all beings attain liberation?'",
                "vo_ta": "விதேக நாட்டின் புனித சபையில், தேவகுரு பிரகஸ்பதியே முதலில் மகரிஷி யாக்ஞவல்கியரிடம் வினவினார்: 'முனிவரே! தேவர்களின் உண்மையான யாக பூமியான குருக்ஷேத்திரம் எது? சகல உயிர்களும் முக்தியடையும், இறைவனால் ஒருபோதும் கைவிடப்படாத அந்த அவிமுக்தத் தலம் எங்கே உள்ளது?'",
                "sub_cue": "Brihaspati asks Yajnavalkya: 'Where is Avimukta, the sacred seat never forsaken by the Supreme?'",
                "sound": "Deep temple gong resonance, gentle evening wind, and a solemn Rudra Veena alapana in Raga Yaman."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Extreme close-up on Yajnavalkya's serene eyes and the Ajna chakra point between his eyebrows, glowing with a subtle indigo-golden star of prana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps extreme close-up cinematic shot of Maharishi Yajnavalkya in deep meditation, a subtle luminous golden-indigo point of light glowing between his eyebrows at the Ajna center. Soft warm oil-lamp reflections dance in his eyes. Authentic ancient Vedic sage aesthetic. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Yajnavalkya smiled and turned the pilgrim's gaze inward: 'Why seek Avimukta only in external geography? That which wards off all sins of the senses is Varana, and that which destroys all ignorance is Nasi. Their sacred junction—Varanasi—lies right here, between the eyebrows and the bridge of the nose, the portal to the heavens and the Supreme Brahman!'",
                "vo_ta": "யாக்ஞவல்கியர் புன்னகைத்து தேடுதலை உள்முகமாகத் திருப்பினார்: 'புற பூமியில் மட்டும் ஏன் அவிமுக்தத்தைத் தேடுகிறீர்கள்? இந்திரிய தோஷங்களைத் தடுப்பது வரணா; அறியாமைப் பாவங்களை நாசம் செய்வது நாசி! இவ்விரண்டும் இணையும் புனித வாரணாசி, புருவ மத்திக்கும் மூக்கின் நுனிக்கும் இடையே உள்ள ஆக்ஞா சக்கரத்திலேயே அமைந்துள்ளது!'",
                "sub_cue": "Varana and Nasi meet between the eyebrows — the inner Varanasi where Brahman dwells!",
                "sound": "Crystalline harmonic overtone singing layered with soft tanpura and distant Ganges waves."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium dramatic shot of King Janaka stepping forward, removing his royal gold necklace and crown, asking Yajnavalkya about the true rule of Sannyasa.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of King Janaka of Videha kneeling on a stone floor, setting aside his ornate ancient gold crown before Maharishi Yajnavalkya. Flickering brass oil lamps cast warm golden highlights across their expressive faces. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Hearing this inner mystery, King Janaka of Videha stepped forward with folded hands: 'O Venerable Yajnavalkya, expound to me the law of Sannyasa! Must a seeker wait until old age, passing strictly through studenthood, household, and forest life before he is permitted to renounce?'",
                "vo_ta": "இந்த அக ரகசியத்தைக் கேட்ட விதேக மன்னன் ஜனகர் கைகூப்பி முன்வந்தார்: 'பூஜ்ய யாக்ஞவல்கியரே! சந்நியாசத்தின் தர்மத்தை எனக்கு உபதேசிப்பீராக! ஒரு சாதகன் பிரம்மச்சரியம், இல்லறம், வானப்பிரஸ்தம் ஆகிய நிலைகளைக் கடந்து முதுமை வரும் வரை துறவிற்காகக் காத்திருக்கத்தான் வேண்டுமா?'",
                "sub_cue": "King Janaka asks: 'Must one wait for old age to embrace Sannyasa?'",
                "sound": "Metallic clink of the royal crown being placed on stone, followed by a rising, expectant mridangam roll."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Dynamic slow-motion sequence showing a young brahmachari, a middle-aged householder by a sacred fire, and an elder forest hermit all awakening simultaneously to inner light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a Vedic householder offering final oblations into a blazing homa fire pit, inhaling the warm golden essence of the sacred fire into his own breath with closed eyes and serene expression. Ancient thatched ashram setting at dawn. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Yajnavalkya uttered the immortal Upanishadic proclamation: 'Yadahareva virajet, tadahareva pravrajet—the very day detachment dawns in the heart, that very day let him renounce!' Offering the Prajapatya sacrifice, the seeker merges the external sacrificial fire into his own vital breath, making his own Prana the eternal altar.",
                "vo_ta": "யாக்ஞவல்கியர் உபநிடதத்தின் அழியா மகா வாக்கியத்தை முழங்கினார்: 'யதஹரேவ விரஜேத் ததஹரேவ ப்ரவ்ரஜேத் — எந்த நாளில் உள்ளத்தில் முழுமையான வைராக்கியம் உதயமாகிறதோ, அன்றே, அக்கணமே துறவு பூணுக!' பிராஜாபத்ய இஷ்டியைச் செய்து, புற அக்னியைத் தன் பிராணனிலேயே ஒடுக்கி, தன் மூச்சையே நித்திய யாக குண்டமாக்குகிறான் துறவி.",
                "sub_cue": "यदहरेव विरजेत्तदहरेव प्रव्रजेत् — The very day detachment dawns, that very day renounce!",
                "sound": "Roaring sacred fire whoosh that gently dissolves into the rhythmic sound of deep yogic pranayama breathing."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Close-up of Sage Atri questioning Yajnavalkya, followed by Yajnavalkya touching his own radiant chest where a brilliant sun-like light glows.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium close-up of Sage Atri and Maharishi Yajnavalkya in a sunlit forest clearing. Yajnavalkya touches his bare chest with his right hand as a warm golden-white radiance emanates from his heart, symbolizing Atman as the only sacred thread. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Sage Atri asked: 'How can one without a sacred thread still be called a Brahmana?' Yajnavalkya replied: 'Idam evāsya tad yajñopavītam ya ātmā—the Self alone is his sacred thread! Rinsing his mouth with water and sipping Prana, he purifies the five vital airs within his own heart.'",
                "vo_ta": "அப்போது அத்ரி முனிவர், 'பூணூல் இல்லாத ஒருவன் எவ்வாறு பிராமணன் ஆவான்?' என்று கேட்டார். அதற்கு யாக்ஞவல்கியர், 'இதமேவாஸ்ய தத் யக்ஞோபவீதம் ய ஆத்மா — ஆத்மாவே அவனது உண்மையான பூணூல்! நீரால் ஆசமனம் செய்து பிராணனை உள்வாங்கி, தன் இதயத்திலேயே பஞ்ச பிராணன்களுக்கும் ஆஹுதி அளிக்கிறான்' என்றார்.",
                "sub_cue": "इदमेवास्य तद्यज्ञोपवीतं य आत्मा — The Supreme Self alone is his sacred thread!",
                "sound": "Clear, uplifting Bamboo Flute solo in Raga Hamsadhwani with gentle water chimes."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide tracking shot of a Paramahamsa ascetic walking freely through an abandoned temple ruin and a hollow tree trunk during a gentle monsoon rain, completely serene and joyous.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide tracking shot of a serene barefoot Paramahamsa ascetic walking peacefully past an ancient stone temple courtyard at dawn, holding neither staff nor bowl, his face glowing with bliss and equanimity. Golden sunlight breaks through morning clouds. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Behold the supreme Paramahamsa—like Samvartaka, Aruni, Shvetaketu, Durvasa, Ribhu, Nidagha, and Jada Bharata! Carrying no triple staff, no begging bowl, no outer emblem, wearing no fixed mark, appearing mad to the deluded world yet inwardly established in pure Advaita, he rests in deserted temples, beneath trees, or by flowing rivers, equal toward praise and blame.",
                "vo_ta": "சம்வர்த்தகர், ஆருணி, சுவேதகேது, துர்வாசர், ரிபு, நிதாகர், ஜடபரதர் போன்ற பரமஹம்சர்களைக் காணீர்! முக்கோலோ, கமண்டலமோ, புற அடையாளமோ இன்றி, உலகோருக்குப் பித்தனைப் போல் தோன்றினாலும் உள்ளே தூய அத்வைதத்தில் நிலைபெற்று, பாழடைந்த மண்டபங்களிலும் மரத்தடியிலும் நதிக்கரையிலும் விருப்பு வெறுப்பின்றி அவர்கள் உலாவுகின்றனர்.",
                "sub_cue": "Without outer marks or possessions, the Paramahamsa roams free in pure Advaita.",
                "sound": "Soaring violin and veena duet evoking boundless freedom, accompanied by gentle wind and birdsong."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane elevation over the confluence of river and forest at sunrise, fading on Yajnavalkya and Janaka seated in silent meditation.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial crane shot rising slowly over an ancient forest ashram and winding sacred river bathed in golden morning light, as Maharishi Yajnavalkya and King Janaka sit in silent meditation below. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "At the final hour within the inner Varanasi, Lord Rudra Himself whispers the Taraka Mantra of liberation, transporting the realized soul across mortality into immortality. May the fire of true Vairagya awaken within us today. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "அக வாரணாசியின் இறுதிப் பயணத்தில், சாட்சாத் ருத்ர பெருமானே தாரக மந்திரத்தை உபதேசித்து, அந்த ஆத்மாவை மரணத்திலிருந்து அமரத்துவத்திற்குக் கரையேற்றுகிறார். உண்மையான வைராக்கியச் சுடர் இன்றே நம் உள்ளத்தில் சுடர்விடுவதாக! ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "In the inner Varanasi, Rudra whispers the Taraka Mantra of Immortality. Om Shanti.",
                "sound": "Deep conch shell, Vedic peace invocation 'Om Purnamadah', and fading river resonance."
            }
        ]
    },
    # 3. ARUNI UPANISHAD (#15)
    {
        "story_id": "SANNYASA_03_ARUNI",
        "muktika_number": 15,
        "name_sanskrit": "आरुण्युपनिषद्",
        "name_iast": "Āruṇyupaniṣad",
        "name_tamil": "ஆருணி உபநிடதம்",
        "name_english": "Aruni Upanishad",
        "veda": "Sama Veda",
        "category": "Sannyasa",
        "story_title_english": "Aruni's Total Renunciation before Prajapati",
        "story_title_tamil": "பிரஜாபதியின் முன் ஆருணியின் பூரண துறவு",
        "characters": "Sage Aruni (Uddalaka Aruni, Seeker of Total Renunciation), Lord Prajapati (The Cosmic Creator & Adi Guru)",
        "verse_sanskrit": "अथ हैनं भगवन्तमरुणिः प्रजापतिं लोकं जगाम । कं भगवन् कर्मणामशेषतो विसृजानीति । तं होवाच प्रजापतिः । तव पुत्रान् भ्रातॄन् बन्धूवादीन् शिखां यज्ञोपवीतं च यागं च सूत्रं च स्वाध्यायं च भूर्भुवःस्वरिति लोकांश्च सर्वान् विसृज ॥",
        "verse_tamil_translit": "காம் பகவன் கர்மணாமஷேஷதோ விஸ்ருஜானீதி | தம் ஹோவாச ப்ரஜாபதி: ... ஸர்வான் விஸ்ருஜ ||",
        "verse_meaning_english": "Aruni went to the world of Lord Prajapati and asked: 'Lord, by what means may I relinquish karma completely without remainder?' Prajapati replied: 'Relinquish sons, brothers, relatives, tuft, sacred thread, sacrifice, ritual texts, and all worlds from Bhur, Bhuvar, and Svar!'",
        "verse_meaning_tamil": "ஆருணி பகவான் பிரஜாபதியின் உலகத்திற்குச் சென்று, 'இறைவா! கர்மங்களை எச்சமின்றி முழுமையாகத் துறப்பது எவ்வாறு?' என்று கேட்டார். அதற்குப் பிரஜாபதி, 'புதல்வர்கள், சகோதரர்கள், உறவினர்கள், குடுமி, பூணூல், யாகம், சாஸ்திரச் சடங்குகள் மற்றும் பூ:, புவ:, ஸுவ: முதலான அனைத்து உலக ஆசைகளையும் துறப்பாயாக!' என்றார்.",
        "theme": "Complete abandonment of karmic rituals, familial attachments, and cosmic ambitions, adopting the bamboo staff of self-restraint and chanting the thrilling ecstatic declaration 'Aham Anna, Aham Annadah' (I am the food and the eater of food).",
        "SettingVisual": "Celestial-earthly Himalayan cedar grove bathed in golden-amber light, overlooking a vast sea of clouds and mountain streams",
        "ProtagonistVisual": "Sage Aruni, earnest middle-aged Vedic rishi with intense eyes, wearing bark-cloth, approaching with a bamboo staff and earthen bowl",
        "GuruVisual": "Lord Prajapati, luminous patriarchal sage-deity seated on a white lotus-carved granite slab surrounded by golden radiance",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide crane shot ascending through Himalayan cedar trees and golden morning mist toward a luminous stone plateau where Aruni bows before Prajapati.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of a majestic Himalayan cedar grove bathed in golden dawn mist. Sage Aruni in bark-cloth kneels with folded hands before the radiant figure of Lord Prajapati seated on a carved stone throne. Ethereal golden sunbeams pierce the ancient trees. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Seeking freedom from the endless wheel of action and reaction, the great Sage Aruni ascended to the luminous realm of Lord Prajapati. Bowing at the Creator's feet, Aruni asked the piercing question of every true seeker: 'O Bhagavan! By what path may I cast off all karmic rituals completely, leaving not a single trace behind?'",
                "vo_ta": "வினைப்பயன்களின் முடிவற்ற சுழற்சியிலிருந்து விடுதலை வேண்டி, மகரிஷி ஆருணி பகவான் பிரஜாபதியின் ஒளிமயமான சந்நிதியை அடைந்தார். படைப்புக் கடவுளின் திருவடிகளில் பணிந்த ஆருணி, 'பகவானே! கர்ம வினைகளைத் துளியும் எச்சமின்றி முழுமையாகத் துறக்கும் வழி யாது?' என்று கேட்டார்.",
                "sub_cue": "Aruni asks Prajapati: 'How may I cast off all karma completely without remainder?'",
                "sound": "High-altitude Himalayan wind, deep resonant Sama Veda chant in the distance, and warm Tanpura drone."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium close-up of Prajapati's commanding yet compassionate face, cutting to Aruni's resolute eyes as he accepts the supreme demand of renunciation.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium close-up of Lord Prajapati with glowing white beard and serene eyes speaking to Sage Aruni in a sunlit Himalayan clearing. Golden dust motes float in the crisp mountain air around their rudraksha beads. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Prajapati tested the depth of Aruni's courage: 'O Aruni, partial renunciation binds the soul tighter! If you seek the Absolute, relinquish attachment to sons, brothers, friends, the ritual tuft, the sacred thread, sacrifices, and even the desire for the seven heavens from Bhurloka to Satyaloka!'",
                "vo_ta": "ஆருணியின் மன உறுதியைப் பிரஜாபதி சோதித்தார்: 'ஆருணி! அரைகுறையான துறவு ஆத்மாவை இன்னும் இறுக்கமாகக் கட்டிப்போடும்! பரம்பொருளை அடைய விரும்பினால், புதல்வர்கள், சகோதரர்கள், உறவினர்கள், குடுமி, பூணூல், வேள்விகள் மற்றும் பூலோகம் முதல் சத்தியலோகம் வரையிலான ஏழு உலகங்களின் ஆசையையும் ஒருங்கே துறப்பாயாக!'",
                "sub_cue": "Relinquish attachment to kin, ritual emblems, and all seven worlds from Bhur to Satya!",
                "sound": "Deep resonant pakhawaj strike followed by a contemplative Sarangi melody."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Slow tracking shot of Aruni standing beside a mountain stream, casting away his ritual implements while chanting the three thrilling cries of 'Chittam! Chittam! Chittam!'",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of Sage Aruni standing beside a crystal-clear Himalayan stream at dawn, releasing his ritual wooden ladles and cotton thread into the water while holding a single bamboo staff, his face lit with fearless spiritual joy. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Taking up a simple bamboo staff and a loincloth for covering the body, Aruni bathed at dawn, noon, and dusk in the waters of self-knowledge. Rejoicing in the inner Self, he proclaimed aloud three times: 'Truly it is cut! Truly the bond of ignorance is severed! Truly I am free!'",
                "vo_ta": "உடலை மறைக்கச் சிறிய ஆடையும், கையில் ஒரு மூங்கில் தண்டமும் ஏந்தி, முப்பொழுதும் ஆத்ம ஞான நீரில் நீராடினார் ஆருணி. தன் உள் ஆத்மாவில் மகிழ்ந்தவராய், 'அறுந்தது! அறியாமைத் தளை அறுந்தது! நான் முற்றிலும் விடுபட்டேன்!' என்று மும்முறை ஆனந்த முழக்கமிட்டார்.",
                "sub_cue": "Three times the sage proclaims: 'Severed is the bond of ignorance! I am free!'",
                "sound": "Rushing mountain stream waters, three clear bronze bell strikes, and joyous Sama Vedic vocal notes."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of Aruni accepting a small morsel of alms in his cupped hands as medicine, while his eyes remain fixed on the inward flame of Prana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian ascetic receiving a small handful of simple rice alms into his cupped palms outside a thatched cottage, viewing food purely as medicine while glowing with inner yogic serenity. Warm golden afternoon light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Prajapati instructed the discipline of the wandering Paramahamsa: 'Spend four months of the rains in one shelter and wander the remaining eight months alone or with a single companion. Partake of begged food strictly as medicine for the body, practicing brahmacharya, ahimsa, truthfulness, and total absence of anger.'",
                "vo_ta": "பரிவ்ராஜக சந்நியாசியின் சாதனையைப் பிரஜாபதி அருளினார்: 'மழைக்காலத்து நான்கு மாதங்கள் ஓரிடத்தில் தங்கி, எஞ்சிய எட்டு மாதங்கள் தனித்தோ இருவராகவோ சஞ்சரிப்பாயாக. பிட்சை உணவை உடற்பிணிக்குரிய மருந்தாக மட்டுமே ஏற்று, பிரம்மச்சரியம், அஹிம்சை, சத்தியம், சினமின்மை ஆகியவற்றில் நிலைத்திருப்பாயாக.'",
                "sub_cue": "Take alms as medicine for the body; abide in Ahimsa, Satya, and spotless Brahmacharya.",
                "sound": "Steady, peaceful rhythm of wooden khartal and a serene flute melody in Raga Kalyani."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Low-angle heroic shot of Aruni atop a windswept granite crag, arms raised toward the golden sun, vibrating with the Sama Veda chant 'Aham Annam'.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps low-angle cinematic shot of Sage Aruni standing atop a sunlit Himalayan granite peak above golden clouds, arms slightly open in ecstatic realization as golden prana light radiates from his heart into the sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Understanding the meaning of the Vedas before and after renunciation, Aruni realized that the syllabic mantra Om alone is his true Upanayana! Filled with cosmic ecstasy, he chanted the Sama hymn: 'I am the food, I am the eater of food! I am the unifier of both! I am the first-born of the cosmic order, shining like the glorious Sun!'",
                "vo_ta": "துறவிற்கு முன்னும் பின்னும் வேதத்தின் உட்பொருளை உணர்ந்த ஆருணி, பிரணவ மந்திரமான 'ஓம்' என்பதே தனது உண்மையான உபநயனம் என்பதை அறிந்தார்! பிரபஞ்சப் பேரின்பத்தில் திளைத்தவராய், 'நானே உணவு! நானே உண்பவன்! இருவரையும் இணைக்கும் சத்தியமும் நானே! ஆதித்யனைப் போல் ஒளிரும் பரம்பொருள் நானே!' என்று சாம கானம் பாடினார்.",
                "sub_cue": "अहमन्नमहमन्नमहमन्नादोऽहं — I am the Food, I am the Eater, I shine as the Cosmic Sun!",
                "sound": "Majestic Sama Veda choral chant 'Aham Annam Aham Annadoham' with soaring conch and mridangam."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Slow 360-degree pan around Aruni seated in lotus posture on a mountain ledge, where golden light merges his form with the sky and earth.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps orbital shot of Sage Aruni seated in padmasana on a high Himalayan rock ledge at sunset. His form is bathed in translucent golden-white light, seamlessly blending with the surrounding mountains and glowing sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Established in the Paramahamsa state beyond all dualities of merit and sin, Aruni needed no external staff or shelter. Having abandoned all worlds, he discovered that the entire universe rested effortlessly within his own infinite Consciousness.",
                "vo_ta": "புண்ணியம், பாவம் எனும் இருமைகளைக் கடந்த பரமஹம்ச நிலையில் நிலைபெற்ற ஆருணிக்கு, இனிப் புறக் கோலோ புகலிடமோ தேவைப்படவில்லை. அனைத்து உலக ஆசைகளையும் துறந்த அவர், பிரபஞ்சம் முழுவதுமே தனது எல்லையற்ற ஆத்ம உணர்விற்குள் அடங்கியிருப்பதைக் கண்டார்.",
                "sub_cue": "Having renounced all worlds, the Sage discovers the entire cosmos resting within his own Self.",
                "sound": "Deep, sustained Tanpura and ethereal Santoor ripples echoing across mountain valleys."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Wide pull-back shot of the glowing Himalayan peaks under twilight stars as Aruni's serene silhouette radiates golden peace.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide pull-back shot of Sage Aruni meditating on a peaceful Himalayan peak at twilight as the first stars appear above golden snow-capped mountains. Warm spiritual aura surrounds him. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus teaches the Aruni Upanishad: when we let go of the finite fragments we cling to, the Infinite reveals itself as our very nature. May that fearless detachment and luminous peace abide in every seeker's heart. Om Apyayantu Mamangani... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு ஆருணி உபநிடதம் உபதேசிக்கிறது: நாம் பற்றிக்கொண்டிருக்கும் அற்பமான எல்லைகளைக் கைவிடும்போது, எல்லையற்ற பரம்பொருள் நமது சொந்த இயல்பாகவே வெளிப்படுகிறது. அந்த அச்சமற்ற வைராக்கியமும் பேரமைதியும் நம் அனைவரின் உள்ளத்திலும் நிலைபெறுவதாக! ஓம் ஆப்யாயந்து மமாங்கானி... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Let go of the finite fragments; awaken to the Infinite Self. Om Shanti.",
                "sound": "Sama Veda Shanti Mantra 'Om Apyayantu Mamangani' fading into gentle mountain wind."
            }
        ]
    },
    # 4. PARAMAHAMSA UPANISHAD (#19)
    {
        "story_id": "SANNYASA_04_PARAMAHAMSA",
        "muktika_number": 19,
        "name_sanskrit": "परमहंसोपनिषद्",
        "name_iast": "Paramahaṃsopaniṣad",
        "name_tamil": "பரமஹம்ச உபநிடதம்",
        "name_english": "Paramahamsa Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "The Royal Swan Who Desires neither Gold nor Moksha: Narada & Bhagavan",
        "story_title_tamil": "பொன்னையும் வேண்டாம், மோட்ச விசாரமும் கடந்த பரமஹம்சன்: நாரதர் மற்றும் பகவான்",
        "characters": "Devarishi Narada (Celestial Sage with Mahati Veena), Bhagavan (The Supreme Lord & Primordial Teacher), The Rare Paramahamsa Yogi",
        "verse_sanskrit": "सुवर्णादीनां दानं न प्रतिगृह्णाति न ਲੋकते च । न चास्याहंकारो न च भविष्यति । यत्पूर्णानन्दैकबोधस्तद्ब्रह्माहमस्मीति कृतकृत्यो भवति ॥",
        "verse_tamil_translit": "ஸுவர்ணாதீனாம் தானம் ந ப்ரதிக்ருஹ்ணாதி ந லோகதே ச | யத் பூர்ணானந்தைகபோதஸ்தத் ப்ரஹ்மாஹமஸ்மீதி க்ருதக்ருத்யோ பவதி ||",
        "verse_meaning_english": "He neither accepts gold and wealth nor even looks at them with desire. Free from egoism now and forever, realizing 'I am that Brahman which is the one Pure Consciousness of Infinite Bliss,' he becomes completely fulfilled.",
        "verse_meaning_tamil": "பொன் முதலான செல்வங்களை அவன் ஏற்பதுமில்லை, ஆசையோடு பார்ப்பதுமில்லை. அகங்காரம் அற்றவனாய், 'பூரண ஆனந்தமே உருவான அந்த ஏக பிரம்மமே நான்' என்று உணர்ந்து, பிறவிப் பயனை முழுமையாக அடைந்த கிருதகிருத்தியன் ஆகிறான்.",
        "theme": "The distinction between the false hypocrite who carries a staff only for his belly (udara-nimittam) and the true Paramahamsa who wears the sky as his garment, rejects gold even in gaze, and abides in Purnananda.",
        "SettingVisual": "Luminous lotus lake surrounded by ancient white marble and granite steps at sunrise, with white swans gliding across mirror-still waters",
        "ProtagonistVisual": "Devarishi Narada, radiant celestial sage carrying a traditional carved wooden tampura/veena, rudraksha beads, and topknot, bowing with eager devotion",
        "GuruVisual": "Bhagavan, the Supreme Adi Guru seated on a lotus-carved granite seat beside the lake, radiating serene golden light",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Glide shot skimming over a tranquil lotus lake where white swans swim at dawn, rising to show Devarishi Narada bowing before Bhagavan.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic glide shot over a tranquil ancient Indian lotus lake at golden sunrise with white swans gliding on mirror-like water. Devarishi Narada holding a traditional wooden veena bows before the radiant Adi Guru seated on carved granite steps. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Beside the tranquil waters where royal swans glide untouched by mud, Devarishi Narada approached the Supreme Lord and asked: 'O Bhagavan! What is the path of the Paramahamsa—the supreme swan among yogis—and what is his inner state of being?'",
                "vo_ta": "சேற்றில் ஒட்டாது வெண் அன்னங்கள் நீந்தும் புனித தடாகக் கரையில், தேவரிஷி நாரதர் பகவானை அணுகி வினவினார்: 'பகவானே! யோகியரில் தலைசிறந்த பரமஹம்சரின் வழி யாது? அவரது அகநிலை எத்தகையது?'",
                "sub_cue": "Narada asks the Lord: 'What is the path and inner state of the Paramahamsa Yogi?'",
                "sound": "Gentle lapping of lake water, distant swan calls, and Narada's Mahati Veena playing a pure Shadja-Panchama drone."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Slow push-in on Bhagavan's face as he describes the rarity of the Paramahamsa, intercut with a solitary yogi walking along a misty mountain ridge.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a solitary barefoot Indian Paramahamsa yogi walking along a high misty mountain ridge at sunrise, bathed in golden light, serene and detached from the world below. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Lord replied: 'O Narada, this path of the Paramahamsa is exceedingly rare in the world; they are not found in crowds. Yet if even one such soul abides on earth, he is the eternal Purusha of the Vedas, whose mind rests unceasingly in Me, and therefore I Myself dwell forever within him!'",
                "vo_ta": "பகவான் அருளினார்: 'நாரதா! இந்தப் பரமஹம்ச மார்க்கம் உலகில் மிக மிக அரிதானது; கூட்டத்தில் அதனைக் காண முடியாது. ஆயினும் அத்தகைய மகாத்மா ஒருவர் இருந்தாலும், அவரே நித்திய வேத புருஷர் ஆவார்! அவரது மனம் என்னிலேயே லயித்திருப்பதால், நானும் அவருள்ளேயே என்றும் உறைகிறேன்!'",
                "sub_cue": "Exceedingly rare is the Paramahamsa; where his mind rests in Me, there I Myself abide.",
                "sound": "Deep flute melody in Raga Bhairavi with soft temple bell overtones."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of a serene ascetic walking unbothered through both winter frost and summer heat, while villagers offer praise on one side and scorn on the other.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium tracking shot of a tranquil ancient Indian ascetic walking barefoot down a dusty village path at dawn, utterly unmoved and smiling gently with equal compassion toward all beings, radiating inner peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Renouncing wife, sons, wealth, and relatives, casting aside tuft, thread, and ritual study, he accepts a loincloth and bamboo staff only for bodily maintenance—and even that is preliminary! The supreme Paramahamsa lives without staff, without tuft, clothed in the vast sky itself, untouched by cold or heat, pleasure or pain, respect or insult.",
                "vo_ta": "மனைவி, மக்கள், செல்வம், சுற்றம் ஆகியவற்றைத் துறந்து, குடுமியும் பூணூலும் நீக்கி, உடலின் பொருட்டு மட்டுமே கௌபீனமும் தண்டமும் ஏற்கிறான்—அதுவும் ஆரம்ப நிலையே! உத்தம பரமஹம்சனோ தண்டமும் இன்றி, திசைகளையே ஆடையாகக் கொண்டு, குளிர்-வெப்பம், இன்பம்-துன்பம், மானம்-அவமானம் ஆகிய இருமைகளைக் கடந்து நிற்கிறான்.",
                "sub_cue": "Untouched by cold or heat, honour or insult, the Paramahamsa abides beyond the six waves of existence.",
                "sound": "Rhythmic, steady mridangam beat symbolizing unwavering equanimity amidst shifting ambient winds."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of a pile of gleaming gold coins offered on a brass platter before the yogi's feet; the yogi's eyes remain peacefully closed, looking past the gold as if it were dust.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of a wealthy merchant placing a brass platter of ancient gold coins before the feet of a meditating Paramahamsa sage under a tree; the sage does not even glance at the gold, his face shining with pure inner bliss. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Beware the false renunciate who takes up the staff merely to fill his belly and hoards gold! The true Paramahamsa neither accepts gold nor even looks upon it with desire. Why? Because one who looks upon gold with longing becomes a killer of the Self! Free from the slightest stain of longing, he sees no difference between gold and a clod of earth.",
                "vo_ta": "வயிற்றுப் பிழைப்பிற்காகத் தண்டம் ஏந்திப் பொன்னைச் சேர்க்கும் போலித் துறவியைக் குறித்து எச்சரிக்கிறார் பகவான்! உண்மையான பரமஹம்சனோ பொன்னை ஏற்பதுமில்லை, ஆசையோடு பார்ப்பதுமில்லை. ஏனெனில் பொன்னை ஆசையோடு பார்ப்பவன் ஆத்மஹத்தி செய்தவனாகிறான்! ஆசையின் சுவடே இன்றி, பொன்னையும் மண்ணையும் சமமாகக் காண்கிறான் ஞானி.",
                "sub_cue": "सुवर्णादीनां दानं न प्रतिगृह्णाति न लोकते च — He neither accepts gold nor looks upon it with desire!",
                "sound": "Sharp metallic ring of gold coins fading instantly into a deep, pure, incorruptible Omkara resonance."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Slow zoom into the yogi's face as a golden-white aura of Jnanadanda (the Staff of Knowledge) illuminates his spine and crown.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of a Paramahamsa yogi seated in lotus posture at sunrise; along his spine shines a brilliant golden column of light representing the Jnanadanda, the inner staff of pure knowledge. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "He who carries a wooden staff is an ordinary mendicant; only he who holds the Jnanadanda—the one indivisible Staff of Self-Knowledge—is a true Ekadandi! When Narada asked if such a sage still seeks liberation, the Lord declared: 'For him, there is neither bondage nor any struggle for Moksha, for he already is the ever-free Brahman!'",
                "vo_ta": "மரத்தாலான தண்டத்தை ஏந்துபவன் சாதாரண துறவி; 'ஞானதண்டம்' எனும் அக அறிவுக் கோலைத் தாங்குபவனே உண்மையான ஏகதண்டி! 'அவருக்கு மோட்ச விசாரம் உண்டா?' என்று நாரதர் கேட்க, பகவான் கூறினார்: 'அவருக்குப் பந்தமும் இல்லை, முக்திக்கான ஏக்கமும் இல்லை; ஏனெனில் அவர் எப்போதும் சுதந்திரமான பிரம்மமே ஆவார்!'",
                "sub_cue": "He who holds the Jnanadanda—the Staff of Pure Knowledge—is the true Ekadandi!",
                "sound": "Triumphant Saraswati Veena and Bansuri unison crescendo in Raga Hindolam."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide cinematic shot of the Paramahamsa seated beside the lotus lake as his reflection in the water transforms into boundless starry sky and golden sunlight.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of the Paramahamsa sage meditating beside a mirror-like lotus lake at dawn; the water reflects golden cosmic light while white swans glide peacefully nearby. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Resting in the supreme realization—'I am that Brahman which is the one indivisible Consciousness of Fullness and Bliss'—the Paramahamsa becomes Kritakritya, one who has accomplished all that is to be accomplished in the universe.",
                "vo_ta": "'பூரண ஆனந்தமே உருவான அந்த ஏக பிரம்மமே நான்' என்ற பரம ஞானத்தில் நிலைபெற்று, பரமஹம்சர் கிருதகிருத்தியராக—பிறவிப் பயனை முழுமையாக அடைந்த பூரணராகத் திகழ்கிறார்.",
                "sub_cue": "यत्पूर्णानन्दैकबोधस्तद्ब्रह्माहमस्मि — I am that Brahman of Infinite Bliss and Pure Consciousness!",
                "sound": "Celestial Tanpura and harmonic bowls creating a sense of timeless fullness."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane lift over Narada bowing to Bhagavan as a white swan takes flight into the golden morning sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps crane shot of a pure white swan taking flight over a sunlit ancient Indian lotus lake while Devarishi Narada bows in gratitude before the radiant Adi Guru. Golden morning rays fill the sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Like the royal swan that separates pure milk from water and soars into the trackless sky, may our awareness rise above worldly greed and ego into the boundless ocean of Purnananda. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "நீரைப் பிரித்துப் பாலை மட்டும் அருந்தி வானில் சிறகடிக்கும் அன்னப் பறவையைப் போல, நம் உணர்வும் உலக ஆசைகளையும் அகங்காரத்தையும் கடந்து பூரண ஆனந்தப் பெருங்கடலில் சிறகடிக்கட்டும். ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Soar like the royal Paramahamsa into the boundless sky of Purnananda. Om Shanti.",
                "sound": "Gentle wingbeats of a swan, soft Veena cadence, and resonant Shanti chant."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 5. MAITREYI UPANISHAD (#29)
    {
        "story_id": "SANNYASA_05_MAITREYI",
        "muktika_number": 29,
        "name_sanskrit": "मैत्रेय्युपनिषद्",
        "name_iast": "Maitreyyupaniṣad",
        "name_tamil": "மைத்ரேயி உபநிடதம்",
        "name_english": "Maitreyi Upanishad",
        "veda": "Sama Veda",
        "category": "Sannyasa",
        "story_title_english": "The King Who Renounced an Empire & Shiva's Worship Without Flowers: Brihadratha & Maitreya",
        "story_title_tamil": "பேரரசைத் துறந்த பிருஹத்ரதனும் மலரில்லா சிவபூஜையும்: மைத்ரேயி உபநிடதம்",
        "characters": "King Brihadratha (Royal Renunciate), Sage Shakayanya (Illumined Master), Sage Maitreya, Lord Shiva & Goddess Maitreyi",
        "verse_sanskrit": "देहो देवालयः प्रोक्तः स जीवः केवलः शिवः । त्यजेदज्ञाननिर्माल्यं सोऽहंभावेन पूजयेत् ॥",
        "verse_tamil_translit": "தேஹோ தேவாலய: ப்ரோக்த: ஸ ஜீவ: கேவல: ஷிவ: | த்யஜேதக்ஞானநிர்மால்யம் ஸோஹம்பாவேன பூஜயேத் ||",
        "verse_meaning_english": "The body is declared to be the temple of God, and the individual indwelling soul is none other than Pure Shiva Himself. One should cast away the faded flowers of ignorance and worship Him with the non-dual realization 'He am I' (Soham)!",
        "verse_meaning_tamil": "இந்த உடலே திருக்கோயில் எனப்படுகிறது; இதனுள் உறையும் ஜீவனே கேவல சிவபெருமான் ஆவான்! அறியாமை எனும் வாடிய மலர்களை நீக்கிவிட்டு, 'அவனே நான்' (ஸோஹம்) என்ற அத்வைத பாவனையால் அவனைப் பூஜிக்க வேண்டும்!",
        "theme": "Dispassion toward the transient physical body (which is born of impurity and decays like an old house), the supremacy of Chitta-shuddhi, and the ultimate non-dual Shiva-puja where the body is the temple and non-dual awareness is the offering.",
        "SettingVisual": "Deep emerald forest penance grove leading to a sacred mountain shrine where golden sunlight illuminates an ancient stone Shiva Lingam and meditating sages",
        "ProtagonistVisual": "King Brihadratha in austere bark-cloth with arms raised toward the sun in penance, and Goddess Maitreyi / Sage Maitreya in serene contemplation",
        "GuruVisual": "Sage Shakayanya glowinglike a smokeless fire, and Lord Shiva in auspicious Dakshinamurti form under a banyan tree",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow cinematic tracking shot through an ancient forest grove at sunrise, revealing former King Brihadratha standing in austere penance with arms raised toward the sun as Sage Shakayanya approaches.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic tracking shot in an ancient Indian forest grove at dawn. Former King Brihadratha dressed in rough bark-cloth stands in deep tapasya gazing at the rising golden sun, as radiant Sage Shakayanya approaches like a smokeless fire. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Knowing this physical body to be impermanent, King Brihadratha installed his eldest son upon the throne and retired into the deep forest. Performing fierce penance for a thousand days with his gaze fixed upon the Sun, he beheld the great Sage Shakayanya—knower of the Self, shining like a smokeless fire at the end of time—and bowed at his feet.",
                "vo_ta": "இந்த உடல் நிலையற்றது என்பதை உணர்ந்த மன்னன் பிருஹத்ரதன், தன் மூத்த புதல்வனுக்கு முடிசூட்டிவிட்டு அடர்ந்த வனத்திற்குள் புகுந்தான். ஆயிரம் நாட்கள் சூரியனை நோக்கிக் கடும் தவம் புரிந்த அவனது முன், புகையில்லா அக்னியைப் போல் ஒளிரும் ஆத்ம ஞானியான சாகாயண்ய முனிவர் தோன்றினார்.",
                "sub_cue": "Renouncing his kingdom, King Brihadratha performs tapasya until Sage Shakayanya appears.",
                "sound": "Morning forest birdsong, solemn tanpura drone, and a deep resonant Rudra Veena glide."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Intimate medium close-up of Shakayanya offering a boon, and Brihadratha weeping with dispassion as he points to the decaying leaves and transient nature of the world.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium close-up of former King Brihadratha kneeling on forest earth with folded hands and tear-filled earnest eyes before luminous Sage Shakayanya, golden sunbeams filtering through ancient sal trees. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Shakayanya said: 'Arise, O King, choose a boon!' Brihadratha touched the sage's feet and cried: 'O Bhagavan, I am not the Self-knower! In this body built of bone, skin, sinew, marrow, and flesh, afflicted by hunger, thirst, anger, and decay, what joy is there in sense pleasures? Like a frog trapped at the bottom of a dry well, lift me out of this ocean of samsara!'",
                "vo_ta": "சாகாயண்யர், 'மன்னா, எழுந்திரும்! வரம் கேளும்!' என்றார். பிருஹத்ரதன் முனிவரின் பாதங்களைப் பற்றி, 'பகவானே! எலும்பு, தோல், நரம்பு, சதையால் ஆனதும், பசி, தாகம், சினம், மூப்பினால் வாடுவதுமான இவ்வுடலில் காம போகங்களால் என்ன பயன்? வறண்ட கிணற்றில் கிடக்கும் தவளையைப் போல் தவிக்கும் என்னை இச்சம்சாரக் கடலிலிருந்து கரையேற்றுங்கள்!' என வேண்டினான்.",
                "sub_cue": "Like a frog in a dry well, save me from this transient ocean of samsara!",
                "sound": "Poignant Esraj solo in Raga Todi expressing deep spiritual yearning and vairagya."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Cinematic montage of mighty rivers drying, giant banyan trees falling, and royal palaces crumbling into dust, while the inner witness remains untouched.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of Sage Shakayanya instructing Brihadratha beside a calm forest pond reflecting the sky; ripples in the water settle into mirror stillness, revealing the unshakeable golden light of the Witness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Shakayanya revealed the teaching of Sage Maitreya: 'Even great emperors, gandharvas, oceans, and mountains pass away; yet the mind alone is samsara! As your thought is, so you become. When the mind is purified of attachment and delusion, it merges like salt in water into the Supreme Self.'",
                "vo_ta": "மைத்ரேய முனிவரின் உபதேசத்தை சாகாயண்யர் அருளினார்: 'மகா சக்கரவர்த்திகளும், சமுத்திரங்களும், மலைகளும்கூடக் காலத்தால் அழிகின்றன! மனமே சம்சாரம்; எண்ணம் எதுவோ அதுவாகவே மனிதன் ஆகிறான். பற்றும் மயக்கமும் நீங்கி மனம் தூய்மையடையும்போது, நீரில் உப்பு கரைவது போல் பரமாத்மாவில் அது ஒடுங்குகிறது.'",
                "sub_cue": "चित्तमेव हि संसारः — The mind alone is Samsara; purify the mind to realize the Self.",
                "sound": "Gentle water ripples dissolving into a crystalline Santoor and Flute harmony."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Transition to a luminous Himalayan cave where Lord Shiva instructs Maitreyi on the supreme inner worship without external flowers or water.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a serene ascetic meditating inside a sunlit granite mandapam before a natural stone Shiva Lingam; instead of physical flowers, glowing golden lotus petals of pure awareness rise from his heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then unfolds the supreme dialogue where Lord Shiva reveals to Maitreyi the secret of Abhisheka and Puja of the Self: 'Deho devalayah proktah, sa jivah kevalah Shivah—this body itself is the temple, and the indwelling soul is none other than Pure Shiva! Cast away the faded flowers of ignorance and worship with the awareness: He am I!'",
                "vo_ta": "அதன்பின் சிவபெருமான் மைத்ரேயிக்கு அருளிய ஆத்ம பூஜை ரகசியம் விரிகிறது: 'தேஹோ தேவாலய: ப்ரோக்த: ஸ ஜீவ: கேவல: ஷிவ: — இந்த உடலே ஆலயம்; இதனுள் உறையும் ஜீவனே கேவல சிவன்! அறியாமை எனும் வாடிய மலர்களை எறிந்துவிட்டு, அவனே நான் என்ற ஸோஹம் பாவனையால் பூஜிப்பாயாக!'",
                "sub_cue": "देहो देवालयः प्रोक्तः स जीवः केवलः शिवः — The body is the Temple; the Jiva is Pure Shiva!",
                "sound": "Resonant Damaru pulse and deep Vedic chanting of 'Soham Shivoham'."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Slow-motion close-up of the meditating sage in nirvikalpa samadhi as golden light pours across his crown like a spiritual abhisheka.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an illumined yogi in deep samadhi; a gentle stream of golden-white prana light cascades over his crown chakra like a sacred abhisheka while his face glows with transcendent peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "What is true bathing? Washing away the dirt of mental impurities! What is true food? Resting in the nectar of Brahman! What is the supreme Asana? Abiding effortlessly in one's own innate Consciousness, where the knower, knowing, and known become One!",
                "vo_ta": "உண்மையான அபிஷேகம் எது? மன மாசுகளைக் கழுவுவதே! உண்மையான நைவேத்தியம் எது? பிரம்ம அமிர்தத்தில் திளைப்பதே! உத்தம ஆசனம் எது? அறிபவன், அறிவு, அறியப்படுபொருள் மூன்றும் ஒன்றாகும் தன் சொந்த ஆத்ம சொரூபத்தில் சலனமின்றி வீற்றிருப்பதே!",
                "sub_cue": "Washing mental impurities is the true bath; resting in Sahaja Samadhi is the supreme Puja.",
                "sound": "Soaring Saraswati Veena melody in Raga Shanmukhapriya with temple bell resonance."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide crane shot of Brihadratha and Maitreyi shining in golden self-effulgence, seeing the one Shiva-Atman pervading every tree, stone, and creature.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of King Brihadratha and Sage Shakayanya seated in luminous samadhi in the ancient forest, surrounded by a golden aura that unites the trees, deer, and sky into one seamless field of consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Awakened by this wisdom, he declares: 'I am timeless, partless, spotless! I am neither the body nor the senses nor the mind; I am Pure Consciousness, the Witness of the three states, the non-dual Shiva Himself!'",
                "vo_ta": "இந்த மெய்ஞ்ஞானத்தால் விழிப்படைந்த முனிவர் முழங்குகிறார்: 'நான் காலமற்றவன், கலைகளற்றவன், களங்கமற்றவன்! நான் உடலோ, இந்திரியங்களோ, மனமோ அல்ல; மூன்று அவஸ்தைகளுக்கும் சாட்சியான தூய சைதன்ய சிவனே நான்!'",
                "sub_cue": "I am neither body nor mind; I am the spotless Witness, the non-dual Shiva!",
                "sound": "Expansive choral 'Shivoham' chant with deep tanpura andbansuri harmonies."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Serene pull-back from the forest shrine at golden dusk as oil lamps flicker peacefully.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps serene pull-back shot of an ancient forest stone shrine lit by golden earthen oil lamps at twilight, radiating eternal peace across the quiet woodland. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Maitreyi Upanishad: do not search for God only in distant stone when the Living Lord shines within the sanctuary of your own heart. Worship Him every moment with the flower of non-dual awareness. Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு மைத்ரேயி உபநிடதம் நிறைவுறுகிறது: நம் இதயக் கருவறையிலேயே உயிருள்ள ஈசன் ஒளிரும்போது, அவனைப் புறத்தே மட்டும் தேடாதீர்கள். ஒவ்வொரு கணமும் அத்வைத விழிப்புணர்வு எனும் மலரால் அவனைப் பூஜிப்போமாக. ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Worship the Living Lord within the temple of your own heart with non-dual awareness. Om Shanti.",
                "sound": "Gentle temple bell chime and Sama Veda Shanti invocation fading into silence."
            }
        ]
    },
    # 6. NIRVANA UPANISHAD (#47)
    {
        "story_id": "SANNYASA_06_NIRVANA",
        "muktika_number": 47,
        "name_sanskrit": "निर्वाणोपनिषद्",
        "name_iast": "Nirvāṇopaniṣad",
        "name_tamil": "நிர்வாண உபநிடதம்",
        "name_english": "Nirvana Upanishad",
        "veda": "Rig Veda",
        "category": "Sannyasa",
        "story_title_english": "The Sky-Clad Sutra of the Avadhuta: The Secret Code of Nirvana",
        "story_title_tamil": "வானமே ஆடையான அவதூதரின் ரகசிய சூத்திரம்: நிர்வாண உபநிடதம்",
        "characters": "The Avadhuta Paramahamsa Master, The Circle of Illumined Dikshita Disciples in the Ajapa Matha",
        "verse_sanskrit": "अथ निर्वाणोपनिषदं व्याख्यास्यामः । परमहंसः सोऽहम् । परिव्राजकाः पश्चिमलिङ्गाः । मन्मथक्षेत्रपालः । गगनसिद्धान्तः । अमृतकल्लोलநदी । अक्षय्यनिरञ्जनः ॥",
        "verse_tamil_translit": "பரமஹம்ஸ: ஸோஹம் | ககனஸித்தாந்த: | அம்ருதகல்லோலநதீ | அக்ஷய்யநிரஞ்ஜன: ||",
        "verse_meaning_english": "Now we expound the Nirvana Upanishad: The Paramahamsa is 'Soham' (He am I). His doctrine is vast as the sky (Gagana-siddhanta); his sacred river is the surging wave of Immortal Bliss (Amrita-kallola-nadi); his state is the Imperishable and Spotless Absolute.",
        "verse_meaning_tamil": "இப்போது நிர்வாண உபநிடதத்தை விளக்குவோம்: பரமஹம்சர் 'ஸோஹம்' வடிவானவர். அவரது சித்தாந்தம் ஆகாயம் போல் எல்லையற்றது (ககன சித்தாந்தம்); அவரது புனித நதி அமிர்த அலைகள் பொங்கும் ஆனந்த நதி; அவரது நிலையோ அழிவற்ற, களங்கமற்ற பரம்பொருள்!",
        "theme": "The mystical cryptographic sutra-language (Sandhya-bhasha) of the Avadhutas, where every external monastery tool (matha, kantha, danda, kashaya, bhiksha) is re-defined as an inner state of non-dual Turiya consciousness.",
        "SettingVisual": "Vast open plateau under a boundless sunlit and star-kissed sky (Gagana-siddhanta) beside a crystal waterfall, with a natural rock cave hermitage",
        "ProtagonistVisual": "A circle of serene Avadhuta seekers seated in effortless stillness, wearing simple unbleached cloth and rudraksha",
        "GuruVisual": "The Supreme Avadhuta Master seated on a flat granite rock under the open sky, radiating boundless joy and freedom",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Expansive wide-angle pan across a high rock plateau where the earth meets the open sky at dawn, settling on the Avadhuta Master and his disciples.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of an ancient Indian rock plateau under a vast golden-blue morning sky. A serene Avadhuta master sits on a natural granite boulder surrounded by quiet ascetic disciples, with a crystal waterfall gleaming in the background. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Beneath the vast canopy of the infinite sky, where all boundaries of sect and monastery dissolve, the Rigvedic Nirvana Upanishad unfolds in aphoristic lightning flashes. The disciples asked the Avadhuta Master: 'What is the monastery, the robe, the staff, and the scripture of one who abides in Nirvana?'",
                "vo_ta": "சம்பிரதாய எல்லைகள் அனைத்தும் கரைந்துபோகும் எல்லையற்ற ஆகாயக் கூரையின் கீழ், ரிக் வேதத்தின் நிர்வாண உபநிடதம் மின்னல் போன்ற சூத்திரங்களாக வெளிப்படுகிறது. சீடர்கள் அவதூத குருவிடம் கேட்டனர்: 'நிர்வாண நிலையில் நிலைபெற்ற ஒருவரின் மடம் எது? ஆடை எது? தண்டம் எது? சாஸ்திரம் எது?'",
                "sub_cue": "What is the monastery, robe, and scripture of the Sage who abides in Nirvana?",
                "sound": "Vast open wind chime resonance, distant waterfall roar, and a deep, meditative Tanpura drone."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Slow push-in on the Master's eyes reflecting the open sky as he speaks the cryptic sutras of the Paramahamsa.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of the Avadhuta master's serene face bathed in golden dawn light, his eyes reflecting the vast sky above as he imparts secret Upanishadic sutras to his disciples. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Master answered in the secret code of the realized: 'Paramahamsah Soham—the Supreme Swan is the realization He am I! His doctrine is Gagana-siddhanta, boundless as the sky! His sacred river is the surging wave of Immortal Bliss, and his lineage is the Spotless Imperishable!'",
                "vo_ta": "ஞானிகளின் ரகசிய சூத்திர மொழியில் குரு பதிலளித்தார்: 'பரமஹம்ஸ: ஸோஹம் — அவனே நான் என்ற உணர்வே பரமஹம்சன்! அவரது சித்தாந்தம் ஆகாயம் போல் எல்லையற்ற ககன சித்தாந்தம்! அவரது புனித தீர்த்தம் அமிர்த அலைகள் பொங்கும் ஆனந்த நதி! அவரது குலம் களங்கமற்ற அக்ஷரப் பரம்பொருள்!'",
                "sub_cue": "परमहंसः सोऽहम् । गगनसिद्धान्तः — The Paramahamsa is Soham; his doctrine is the Boundless Sky!",
                "sound": "Resonant Rigvedic sutra recitation accompanied by ethereal bamboo flute notes."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Tracking shot across the disciples in deep pranayama, where their breath flows effortlessly as the Ajapa Gayatri.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium tracking shot of three ancient Indian ascetics seated in padmasana on a sunlit rock ledge, subtle golden prana light flowing rhythmically with their breath at the heart and nostrils. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "What is his monastery? The unuttered Ajapa Gayatri of the breath! Look at his virtues: cosmic consciousness is his patched garment (kantha), yoga is his seat, inner bliss is his garland, and mocking the delusions of the world with a compassionate smile is his sacred cave!",
                "vo_ta": "அவரது மடம் எது? உச்சரிக்கப்படாமல் இயங்கும் அஜபா காயத்ரி மூச்சே அவரது மடம்! விராட் சொரூபமே அவரது ஒட்டுப்போட்ட கந்தை ஆடை; யோகமே அவரது ஆசனம்; உள் ஆனந்தமே அவரது மாலை; உலக மயக்கங்களைக் கண்டு புன்னகைக்கும் கருணையே அவரது குகை!",
                "sub_cue": "Ajapa breath is his monastery; Cosmic Consciousness is his garment; Yoga is his seat.",
                "sound": "Rhythmic breath-like Bansuri phrasing over a gentle tabla tarang pulse."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Cinematic close-up of the Master's calm hands in jnana mudra, juxtaposed with golden sunlight piercing dark storm clouds over the valley.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of golden sunbeams breaking through dramatic morning clouds over a green Indian valley while the Avadhuta yogi sits motionless in jnana mudra in the foreground. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Compassion toward all beings is his begging bowl; patience and forgiveness are his shelter; unwavering discrimination is his loincloth; seeing the Self in all is his ochre dye; and fearless, unshakeable samadhi is his ascetic staff!",
                "vo_ta": "சகல உயிர்களிடத்தும் காட்டும் கருணையே அவரது பிட்சைப் பாத்திரம்; பொறுமையும் மன்னிப்புமே அவரது புகலிடம்; விவேகமே அவரது கௌபீனம்; எங்கும் ஆத்மாவைக் காண்பதே அவரது காவி நிறம்; அச்சமற்ற நிர்விகல்ப சமாதியே அவரது தண்டம்!",
                "sub_cue": "Compassion is his bowl, Discrimination his garment, and Fearless Samadhi his staff.",
                "sound": "Deep Rudra Veena chords building in majesty and spiritual resolve."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Orbital shot around the Avadhuta as the distinction between day and night, sun and moon, merges into one golden radiance around him.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps orbital cinematic shot of the Avadhuta master in deep meditation on the high plateau; warm golden sunlight and cool silvery moonlight blend harmoniously in the sky above him, symbolizing non-dual union. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In that state of Shiva-yoga sleep, there is neither confusion nor doubt, neither bondage nor liberation, neither virtue nor vice. By the path of the Western Sushumna channel, Kundalini unites with Paramashiva in the thousand-petalled lotus, and the yogi drinks the nectar of Sahaja Samadhi!",
                "vo_ta": "அந்த சிவயோக நித்திரையில் குழப்பமோ சந்தேகமோ இல்லை; பந்தமோ முக்தியோ இல்லை; புண்ணியமோ பாவமோ இல்லை! சுஷும்னா நாடி வழியாகக் குண்டலினி சகஸ்ராரத் தாமரையில் பரமசிவனுடன் இணைய, யோகி சஹஜ சமாதியின் அமிர்தத்தைப் பருகுகிறார்!",
                "sub_cue": "Through Sushumna into Sahasrara, the Yogi drinks the immortal nectar of Sahaja Samadhi.",
                "sound": "Harmonic overtone singing and high-register Saraswati Veena notes shimmering like starlight."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the Avadhuta standing serenely at the cliff edge, looking out over the boundless horizon as a liberated Jivanmukta.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide heroic shot of the barefoot Avadhuta sage standing peacefully at the edge of a sunlit mountain plateau gazing across an infinite sea of golden clouds, embodying absolute freedom. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Free from fear, free from sorrow, free from desire and ego, he moves through the world in Svecchachara—spontaneous divine harmony. Realizing Parabrahman as his own Self, he attains Nirvana—the blowing out of all false limitations in the blaze of Infinite Truth.",
                "vo_ta": "அச்சமின்றி, சோகமின்றி, ஆசையும் அகங்காரமும் இன்றி, இறை நியதியோடு இயைந்த தன்னிச்சையான சுதந்திரத்தில் அவர் உலாவுகிறார். பரப்பிரம்மமே தான் என உணர்ந்து, பொய்யான எல்லைகள் அனைத்தும் அழிந்துபோகும் பரிபூரண நிர்வாண நிலையை அவர் அடைகிறார்.",
                "sub_cue": "All false limitations vanish in the blaze of Parabrahman — this is true Nirvana.",
                "sound": "Majestic conch shell call echoing across the canyon, followed by serene bansuri peace notes."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane ascent into the golden morning sky above the plateau, leaving the circle of sages in silent bliss.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot rising into the golden-blue morning sky above the Himalayan plateau where the Avadhuta master and disciples sit in silent radiance. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "This secret Nirvana Upanishad is to be imparted only to the tranquil disciple whose heart is pure. May we too wear the boundless sky of pure awareness and rest in the spotless peace of the Self. Om Vang Me Manasi Pratishthita... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "மனம் தெளிந்த உத்தம சீடர்களுக்கு மட்டுமே அருளப்படும் ரகசிய உபநிடதம் இது. நாமும் தூய விழிப்புணர்வு எனும் ஆகாயத்தை ஆடையாகக் கொண்டு ஆத்ம சாந்தியில் நிலைபெறுவோமாக. ஓம் வாங் மே மனஸி ப்ரதிஷ்டிதா... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Abide in Gagana-Siddhanta—the boundless sky of Pure Awareness. Om Shanti.",
                "sound": "Rigvedic Shanti Mantra 'Om Vang Me Manasi' fading into open sky wind resonance."
            }
        ]
    },
    # 7. NARADAPARIVRAJAKA UPANISHAD (#43)
    {
        "story_id": "SANNYASA_07_NARADAPARIVRAJAKA",
        "muktika_number": 43,
        "name_sanskrit": "नारदपरिव्राजकोपनिषद्",
        "name_iast": "Nāradaparivrājakopaniṣad",
        "name_tamil": "நாரத பரிவ்ராஜக உபநிடதம்",
        "name_english": "Naradaparivrajaka Upanishad",
        "veda": "Atharva Veda",
        "category": "Sannyasa",
        "story_title_english": "The Six Rungs of Renunciation & The 16-Fold Omkara: Narada & Lord Brahma",
        "story_title_tamil": "துறவின் ஆறு படிகளும் பதினாறு கலை ஓங்காரமும்: நாரதர் மற்றும் சௌனகர்",
        "characters": "Devarishi Narada (The Cosmic Wanderer), Maharishi Shaunaka & the 88,000 Rishis of Naimisharanya, Pitamaha Brahma (Parameshthi)",
        "verse_sanskrit": "कुटीचको बहूदकः हंसश्च परमहंसश्च तुरीयातीतोऽवधूतश्चेति षड्विधाः संन्यासिनः । अहिंसा सत्यमस्तेयब्रह्मचर्यापरिग्रहाः । अनौद्धत्यमदीनत्वं प्रसादः स्थैर्यमार्जवम् ॥",
        "verse_tamil_translit": "குடீசகோ பஹூதக: ஹம்ஸஸ்ச பரமஹம்ஸஸ்ச துரீயாதீதோ அவதூதஸ்சேதி ஷட்விதா: ஸம்ந்யாஸின: ||",
        "verse_meaning_english": "Renunciates are of six kinds: Kutichaka, Bahudaka, Hamsa, Paramahamsa, Turiyatita, and Avadhuta. Their foundational vows are non-violence, truth, non-stealing, continence, non-possession, humility, fearlessness, serenity, steadiness, and rectitude.",
        "verse_meaning_tamil": "சந்நியாசிகள் ஆறு வகையினர்: குடீசகர், பஹூதகர், ஹம்சர், பரமஹம்சர், துரீயாதீதர் மற்றும் அவதூதர். அஹிம்சை, சத்தியம், திருடாமை, பிரம்மச்சரியம், உடமையின்மை, பணிவு, சோர்வின்மை, மனத்தெளிவு, உறுதி, நேர்மை ஆகியவையே அவர்களின் அடிப்படை விரதங்களாகும்.",
        "theme": "The encyclopedic blueprint of Sannyasa: who is qualified and disqualified to renounce, how the wandering ascetic must live like an ant, a bee, or a python without attachment, the six classes of Sannyasins, and meditation on the 16-kala Omkara.",
        "SettingVisual": "Vast Naimisharanya sacred forest congregation under ancient banyan and peepal trees with hundreds of oil lamps and a central stone dais",
        "ProtagonistVisual": "Maharishi Shaunaka and the assembled forest sages in white cotton and bark-cloth, listening with rapt devotion",
        "GuruVisual": "Devarishi Narada holding his Mahati Veena, radiating golden celestial wisdom, and Pitamaha Brahma in luminous meditation",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Sweeping crane shot over the grand Naimisharanya forest assembly at dawn as Devarishi Narada arrives holding his Veena, greeted by Shaunaka and the sages.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps sweeping crane shot of the sacred Naimisharanya forest at golden sunrise. Devarishi Narada holding a carved wooden veena stands at the center of an ancient clearing while Maharishi Shaunaka and venerable Vedic sages bow with folded hands. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Once, Devarishi Narada, wandering through the three worlds purifying every shrine, arrived at the sacred forest of Naimisharanya. There, Maharishi Shaunaka and a vast assembly of tapasvins bowed before him and asked: 'O Revered Son of Brahma, teach us the complete science of Parivrajya—the liberating path of the wandering renunciate!'",
                "vo_ta": "மூவுலகங்களிலும் சஞ்சரித்துப் புனிதத் தலங்களைப் புனிதப்படுத்தும் தேவரிஷி நாரதர், ஒருமுறை நைமிசாரண்ய வனத்திற்கு எழுந்தருளினார். அங்கே சௌனக மகரிஷியும் தவ சீலர்களும் அவரை வணங்கி, 'பிரம்ம புத்திரரே! பிறவிப் பிணியைப் போக்கும் பரிவ்ராஜக சந்நியாசத்தின் முழுமையான தர்மத்தை எங்களுக்கு உபதேசித்தருளுங்கள்!' என்று வேண்டினர்.",
                "sub_cue": "In Naimisharanya, Shaunaka and the sages ask Narada for the supreme science of Sannyasa.",
                "sound": "Melodious strumming of Narada's Mahati Veena, forest birdsong, and a warm Vedic choral murmur."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium shot of Narada recounting the teaching he received from his father Pitamaha Brahma, showing a seeker examined by a wise Guru.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of Devarishi Narada seated on a deer-skin mat under a giant peepal tree, speaking earnestly to Shaunaka and the forest rishis as golden sunbeams illuminate their faces. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Narada shared the supreme wisdom taught to him by Pitamaha Brahma Himself: 'Not everyone is ready for Sannyasa! The apostate, the mortal sinner, the deceitful, and the sense-bound cannot renounce—except in the hour of Atyatura, the final threshold of life. Only one endowed with discrimination, serene senses, and burning detachment is qualified!'",
                "vo_ta": "பிதாமகர் பிரம்மதேவரே தனக்கு உபதேசித்த ரகசியத்தை நாரதர் பகிர்ந்தார்: 'கடமை தவறியவன், வஞ்சகன், புலனடக்கம் இல்லாதவன் ஆகியோர் சந்நியாசத்திற்குத் தகுதியற்றவர்கள். விவேகமும், புலனடக்கமும், தீவிர வைராக்கியமும் கொண்ட பக்குவ ஆத்மாவே துறவு பூணத் தகுதியுடையவன்!'",
                "sub_cue": "Only the seeker endowed with Viveka, Sama, Dama, and burning Vairagya is qualified to renounce.",
                "sound": "Steady, authoritative Pakhawaj rhythm with a contemplative Veena melody in Raga Darbari Kanada."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Visual progression across six distinct ascetics seated in ascending tiers of a Himalayan granite staircase, from Kutichaka at the base to Avadhuta at the summit.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of six ancient Indian ascetics seated at ascending levels of a natural mountain stone terrace at sunrise, progressing from a triple-staff mendicant below to a radiant sky-clad Avadhuta in samadhi at the summit. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Narada revealed the six ascending orders of Sannyasa: the Kutichaka dwelling in a hermitage, the Bahudaka wandering to sacred rivers with a triple staff, the Hamsa with a single staff, the Paramahamsa without outer emblems, the Turiyatita who takes food like a cow without using hands, and the supreme Avadhuta who abides like a python in unbroken absorption!",
                "vo_ta": "சந்நியாசத்தின் ஆறு படிநிலைகளை நாரதர் விவரித்தார்: குடிலில் தங்கும் குடீசகர், முக்கோல் ஏந்தி புனித நதிகளில் நீராடும் பஹூதகர், ஏகதண்டம் ஏந்தும் ஹம்சர், புற அடையாளமற்ற பரமஹம்சர், பசுவைப் போல் உணவேற்கும் துரீயாதீதர், மற்றும் மலைப்பாம்பைப் போல் அசையாது பிரம்ம நிஷ்டையில் ஆழ்ந்திருக்கும் அவதூதர்!",
                "sub_cue": "Six Orders of Sannyasa: Kutichaka, Bahudaka, Hamsa, Paramahamsa, Turiyatita, and Avadhuta.",
                "sound": "Ascending six-note raga scale on the Bansuri and Saraswati Veena, rising in spiritual elevation."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Macro shot of a honeybee gathering nectar from a lotus without bruising a single petal, dissolving to a wandering monk accepting alms with utter humility.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic macro-to-medium shot of a golden honeybee gently resting on a pink lotus flower at dawn without disturbing a petal, transitioning to a serene barefoot Indian monk walking quietly along a forest path. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "How should the Parivrajaka move through the world? Like a honeybee gathering drops of nectar without hurting the flower—Madhukara vritti! He neither rejoices when praised nor grieves when insulted. Keeping no store for tomorrow, avoiding royal courts and crowds, he guards his senses like a tortoise withdrawing its limbs.",
                "vo_ta": "பரிவ்ராஜக துறவி உலகில் எவ்வாறு நடந்துகொள்ள வேண்டும்? மலரை நோகடிக்காமல் தேனை மட்டும் சேகரிக்கும் வண்டைப் போல 'மதுகர விருத்தி'யில் பிட்சை ஏற்க வேண்டும்! ஆமை தன் உறுப்புகளை உள்ளிழுத்துக் கொள்வது போல் புலன்களை அடக்கி, புகழ்ச்சிக்கு மயங்காமலும் இகழ்ச்சிக்குக் கலங்காமலும் சஞ்சரிக்க வேண்டும்.",
                "sub_cue": "Like a bee gathering nectar without hurting the flower, the monk practices Madhukara Vritti.",
                "sound": "Soft buzzing of nature blending into a tranquil bamboo flute solo."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of a meditating Paramahamsa surrounded by sixteen concentric rings of golden light representing the sixteen Kalas of Omkara.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic close-up of an illumined Indian sage in padmasana inside a dark stone cave; from his heart and crown radiate concentric rings of golden prana light representing the sixteen kalas of Omkara. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Narada unveiled the supreme Taraka Brahma: the sacred syllable Om possessing sixteen luminous Kalas—from A-kara, U-kara, Ma-kara, Ardhamatra, Nada, and Bindu up to Unmani and Para! Meditating upon this sixteen-petalled Omkara across the waking, dream, deep sleep, and Turiya states, the yogi burns away the causal seed of rebirth.",
                "vo_ta": "அதன்பின் பதினாறு கலைகள் கொண்ட தாரகப் பிரம்மமான ஓங்கார ரகசியத்தை நாரதர் வெளியிட்டார்! அகாரம், உகாரம், மகாரம், அர்த்தமாத்திரை, நாதம், விந்து முதல் உன்மனி வரை விரியும் பதினாறு கலை ஓங்காரத்தை நான்கு அவஸ்தைகளிலும் தியானிக்கும் யோகி, பிறவியின் காரண வித்தையே சுட்டெரிக்கிறான்!",
                "sub_cue": "Meditating on the 16-Kala Omkara, the Yogi burns away the seed of rebirth.",
                "sound": "Deep, multi-layered Omkara chant resonating across three octaves with temple bell harmonics."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the Avadhuta sage seated by a river confluence, his form glowing like pure crystal as the river flows into the ocean.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of an ancient Indian Avadhuta sage seated in samadhi at the confluence of a sacred river and the vast ocean at sunrise, golden light uniting water and sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Just as rivers flowing into the ocean lose their separate names and forms and become the ocean itself, so does the knower of Brahman, freed from name and form, attain the Supreme Divine Person beyond the higher and the lower!",
                "vo_ta": "கடலில் கலக்கும் நதிகள் தமது தனிப் பெயரையும் உருவத்தையும் இழந்து சமுத்திரமாகவே மாறுவது போல, நாம ரூபங்களிலிருந்து விடுபட்ட பிரம்மஞானி மேலானதற்கும் மேலான திவ்ய புருஷனோடு இரண்டறக் கலக்கிறான்!",
                "sub_cue": "As rivers merge into the ocean losing name and form, the knower merges into Supreme Brahman.",
                "sound": "Ocean waves blending with a majestic Veena and Violin symphony in Raga Sindhubhairavi."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow pull-back over the Naimisharanya forest assembly as Narada raises his Veena in blessing and the sages bow in unison.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide pull-back shot of Devarishi Narada raising his hand in blessing over Maharishi Shaunaka and the Naimisharanya forest sages bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Naradaparivrajaka Upanishad: whether in the forest or the heart of life, let humility, non-injury, and continuous remembrance of Omkara be our true pilgrimage. Om Bhadram Karnebhih Shrinuyama Devah... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு நாரத பரிவ்ராஜக உபநிடதம் நிறைவுறுகிறது: பணிவும், அஹிம்சையும், இடைவிடாத ஓங்கார ஸ்மரணையுமே நமது உண்மையான புனித யாத்திரையாக மலரட்டும். ஓம் பத்ரம் கர்ணேபி: ச்ருணுயாம தேவா:... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Let Ahimsa, Humility, and continuous Omkara awareness be your eternal pilgrimage. Om Shanti.",
                "sound": "Atharva Veda Shanti Mantra 'Om Bhadram Karnebhih' and fading Mahati Veena notes."
            }
        ]
    },
    # 8. BHIKSHUKA UPANISHAD (#60)
    {
        "story_id": "SANNYASA_08_BHIKSHUKA",
        "muktika_number": 60,
        "name_sanskrit": "भिक्षुकोपनिषद्",
        "name_iast": "Bhikṣukopaniṣad",
        "name_tamil": "பிக்ஷுக உபநிடதம்",
        "name_english": "Bhikshuka Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "The Four Mendicants on the Path of Liberation: Kutichaka to Paramahamsa",
        "story_title_tamil": "முக்திப் பாதையின் நான்கு பிட்சுக்கள்: குடீசகர் முதல் பரமஹம்சர் வரை",
        "characters": "The Assembly of Shukla Yajurvedic Sages, Representatives of the Four Orders: Kutichaka (Gautama, Bharadvaja), Bahudaka, Hamsa, and Paramahamsa (Samvartaka, Aruni, Shvetaketu, Jada Bharata)",
        "verse_sanskrit": "अथ भिक्षूणां मोक्षार्थिनां कुटीचकबहूदकहंसपरमहंसाश्चेति चत्वारः । परमहंसा नाम संवर्तकारुणिश्वेतकेतुजडभरतदत्तात्रेयशुकवामदेवहारीतकप्रभृतयोऽष्टौ ग्रासांश्चरन्तो योगमार्गेण मोक्षमेव प्रार्थयन्ते ॥",
        "verse_tamil_translit": "அத பிக்ஷூணாம் மோக்ஷார்த்தினாம் குடீசக பஹூதக ஹம்ஸ பரமஹம்ஸாஸ்சேதி சத்வார: | பரமஹம்ஸா நாம ஸம்வர்த்தகாருணி ஸ்வேதகேது ஜடபரத தத்தாத்ரேய சுக வாமதேவ ஹாரீதக ப்ரப்ருதய: ||",
        "verse_meaning_english": "Among mendicant monks who seek liberation, there are four classes: Kutichaka, Bahudaka, Hamsa, and Paramahamsa. The Paramahamsas—such as Samvartaka, Aruni, Shvetaketu, Jada Bharata, Dattatreya, Shuka, Vamadeva, and Haritaka—partake of eight morsels and seek Liberation alone through the path of Yoga.",
        "verse_meaning_tamil": "மோட்சத்தை நாடும் பிட்சுக்களில் குடீசகர், பஹூதகர், ஹம்சர், பரமஹம்சர் என நான்கு வகையினர் உள்ளனர். சம்வர்த்தகர், ஆருணி, சுவேதகேது, ஜடபரதர், தத்தாத்ரேயர், சுகர், வாமதேவர், ஹாரீதகர் போன்ற பரமஹம்சர்கள் எட்டு கவள உணவேற்று, யோக மார்க்கத்தால் மோட்சத்தை மட்டுமே நாடுகின்றனர்.",
        "theme": "The progressive distillation of ascetic life across the four orders of Bhikshus—from thirty-two morsels to eight morsels, from desiring heaven to desiring pure Moksha alone in the footsteps of Shuka, Dattatreya, and Jada Bharata.",
        "SettingVisual": "Ancient forest ashram pathway leading from thatched hermitage huts to sacred riverbanks and finally to a solitary sunlit banyan tree",
        "ProtagonistVisual": "Four distinct mendicant monks representing the four stages of Bhikshu discipline",
        "GuruVisual": "Luminous lineage of Paramahamsa masters (Dattatreya, Shuka, Jada Bharata) seated in radiant stillness",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow tracking shot along a golden sunlit forest path where four mendicant monks walk in quiet contemplation.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps tracking shot of an ancient Indian forest pathway at golden dawn. Four serene Vedic mendicants in varying stages of ascetic simplicity walk barefoot beneath towering sal trees as morning mist rises. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the sacred tradition of the Shukla Yajur Veda, the Bhikshuka Upanishad illuminates the four graduated ranks of mendicants who walk the path toward liberation: the Kutichaka, the Bahudaka, the Hamsa, and the supreme Paramahamsa.",
                "vo_ta": "சுக்ல யஜுர் வேதத்தின் புனித மரபில், முக்தியை நாடும் துறவிகளின் நான்கு படிநிலைகளை பிக்ஷுக உபநிடதம் படம் பிடித்துக் காட்டுகிறது: குடீசகர், பஹூதகர், ஹம்சர் மற்றும் உத்தம பரமஹம்சர்.",
                "sub_cue": "Four Orders of Mendicants on the Path of Liberation: Kutichaka, Bahudaka, Hamsa, and Paramahamsa.",
                "sound": "Calm morning birdsong, gentle footsteps on dry leaves, and a serene Tanpura and Bansuri introduction."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium shot of a Kutichaka ascetic outside a modest thatched hut, holding a triple staff and water pot, partaking of thirty-two small morsels.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of an elderly Kutichaka ascetic with topknot, sacred thread, triple bamboo staff, and kamandalu seated outside a simple thatched ashram hut at sunrise, calmly accepting alms in a leaf bowl. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "First are the Kutichakas—such as Gautama, Bharadvaja, Yajnavalkya, and Vasishtha—who live in quiet hermitages, carry the triple staff and water pot, and partake of thirty-two morsels of food while fixing their contemplation upon the philosophical truth.",
                "vo_ta": "முதலாமவர் குடீசகர்கள்—கௌதமர், பரத்வாஜர், யாக்ஞவல்கியர், வசிஷ்டர் போன்றோர்—ஆசிரமக் குடில்களில் தங்கி, முக்கோலும் கமண்டலமும் ஏந்தி, முப்பத்திரண்டு கவள உணவேற்று தத்துவ விசாரத்தில் ஈடுபடுபவர்கள்.",
                "sub_cue": "The Kutichaka: dwelling in quiet hermitages, practicing steady philosophical contemplation.",
                "sound": "Soft rhythmic mridangam pulse and gentle Saraswati Veena phrases."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Panning shot beside a sacred river confluence where a Bahudaka monk in ochre robe performs his morning bath and subsists on eight morsels gathered like a bee.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps panning shot of a Bahudaka ascetic in ochre cloth standing beside a sacred river temple ghat at dawn, holding a triple staff and rudraksha mala, radiating devotion and discipline. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Second are the Bahudakas, who leave behind fixed huts to wander from sacred river to sacred river. Wearing ochre robes and three lines of sacred ash, they gather just eight morsels of food like a honeybee from seven virtuous households, purifying their minds for higher knowledge.",
                "vo_ta": "இரண்டாமவர் பஹூதகர்கள்—குடிலைத் துறந்து புனித தீர்த்தங்கள் தோறும் சஞ்சரிப்பவர்கள். காவியாடையும் திருநீறும் அணிந்து, வண்டைப் போல ஏழு இல்லங்களில் எட்டு கவள உணவை மட்டுமே பிட்சையேற்று மனத்தூய்மை பெறுபவர்கள்.",
                "sub_cue": "The Bahudaka: wandering from sacred river to river, subsisting on eight morsels gathered like a bee.",
                "sound": "Flowing river water sound layered with a melodic Carnatic violin in Raga Kambhoji."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Tracking shot of a Hamsa ascetic walking continuously through village and forest, never staying more than one night in a village.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps tracking shot of a serene Hamsa monk carrying a single bamboo staff, walking past a quiet rural Indian village at sunrise without stopping, eyes fixed on the horizon in yogic detachment. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Third are the Hamsas: they stay no more than a single night in a village, five nights in a town, and seven nights at a sacred shrine! Practicing austere penance and purifying the body through natural elements, they soar ever higher above worldly attachment.",
                "vo_ta": "மூன்றாமவர் ஹம்சர்கள்: கிராமத்தில் ஒரு இரவும், நகரத்தில் ஐந்து இரவுகளும், புனிதத் தலத்தில் ஏழு இரவுகளுக்கும் மேல் தங்காதவர்கள்! கடும் தவத்தோடு அன்னப் பறவையைப் போல உலகப் பற்றுகளுக்கு மேலே சிறகடித்து உயர்வது இவர்களின் இயல்பு.",
                "sub_cue": "The Hamsa: staying never more than one night in a village, soaring free of attachment.",
                "sound": "Brisk, uplifting flute melody evoking continuous movement and detachment."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Majestic slow push-in on a Paramahamsa sage seated under a giant banyan tree, glowing with golden inner fire, surrounded by visions of Shuka, Dattatreya, and Jada Bharata.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps majestic push-in shot of a radiant Paramahamsa yogi seated in lotus posture beneath an ancient banyan tree at sunrise, his bare torso glowing with subtle golden yogic prana, embodying the lineage of Shuka and Dattatreya. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Fourth and highest are the Paramahamsas—the lineage of Samvartaka, Aruni, Shvetaketu, Jada Bharata, Dattatreya, Shuka, Vamadeva, and Haritaka! Seeking neither earthly comfort nor heavenly realms, they partake of eight morsels solely to sustain the yoga-body and seek Liberation alone!",
                "vo_ta": "நான்காமவரான உச்ச நிலையினர் பரமஹம்சர்கள்—சம்வர்த்தகர், ஆருணி, சுவேதகேது, ஜடபரதர், தத்தாத்ரேயர், சுகர், வாமதேவர், ஹாரீதகர் ஆகியோரின் ஞானப் பரம்பரை! இவ்வுலக சுகத்தையோ சொர்க்கத்தையோ நாடாமல், யோக மார்க்கத்தால் மோட்சத்தை மட்டுமே இலக்காகக் கொண்டவர்கள்!",
                "sub_cue": "The Paramahamsas—like Shuka, Dattatreya, and Jada Bharata—seek Liberation alone through Yoga!",
                "sound": "Deep conch shell, resonant Omkara chant, and majestic Rudra Veena chords."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the Paramahamsa resting serenely inside a hollow tree trunk and an abandoned temple courtyard, viewing a clod of earth, a stone, and gold as one.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of a serene Paramahamsa sage meditating inside an ancient unroofed stone temple courtyard overgrown with banyan roots at golden dawn, radiating supreme equanimity. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Dwelling at the foot of trees, in deserted houses, or in cremation grounds, clothed or unclothed, they transcend the pairs of dharma and adharma, truth and untruth. Seeing a clod of earth, a stone, and gold as equal, they behold the Self in all beings and merge into Brahman through pure Yoga!",
                "vo_ta": "மரத்தடியிலோ, பாழடைந்த மண்டபங்களிலோ தங்கி, தர்ம-அதர்ம இருமைகளைக் கடந்து அவர்கள் நிற்கின்றனர். மண்ணையும், கல்லையும், பொன்னையும் சமமாகக் கண்டு, சகல உயிர்களிலும் ஆத்மாவையே தரிசித்து, யோக மார்க்கத்தால் பரப்பிரம்மத்தில் லயிக்கின்றனர்!",
                "sub_cue": "Seeing earth, stone, and gold as equal, the Paramahamsa merges into Supreme Brahman.",
                "sound": "Expansive, serene Santoor and Bansuri duet in Raga Ahir Bhairav."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane elevation over the banyan tree and forest horizon bathed in golden morning light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over a sunlit ancient Indian banyan tree and forest river valley at dawn, radiating timeless peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Bhikshuka Upanishad: every step of simplicity brings the seeker closer to the supreme freedom of the Paramahamsa. May our hearts awaken to that equal vision which sees the One Divine in all. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பிக்ஷுக உபநிடதம் நிறைவுறுகிறது: எளிமையின் ஒவ்வொரு அடியும் சாதகனைப் பரமஹம்சரின் பரம சுதந்திரத்திற்கு இட்டுச் செல்கிறது. சகலத்திலும் ஒரே இறைவனைக் காணும் சமநோக்கு நம் உள்ளத்தில் மலர்வதாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Awaken to the equal vision that beholds the One Divine in all beings. Om Shanti.",
                "sound": "Shanti Mantra 'Om Purnamadah' with fading temple bell and river murmur."
            }
        ]
    },
    # 9. TURIYATITA AVADHUTA UPANISHAD (#64)
    {
        "story_id": "SANNYASA_09_TURIYATITA_AVADHUTA",
        "muktika_number": 64,
        "name_sanskrit": "तुरीयातीतावधूतोपनिषद्",
        "muktika_alt": "Turiyatitavadhuta Upanishad",
        "name_iast": "Turīyātītāvadhūtopaniṣad",
        "name_tamil": "துரீயாதீத அவதூத உபநிடதம்",
        "name_english": "Turiyatita Avadhuta Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "Beyond the Fourth State: Lord Narayana Reveals the Turiyatita to Brahma",
        "story_title_tamil": "துரியத்தையும் கடந்த அவதூத நிலை: பிரம்மனுக்கு நாராயணரின் உபதேசம்",
        "characters": "Lord Adinarayana (The Supreme Cosmic Guru), Pitamaha Brahma (The Creator Seeker), The Turiyatita Avadhuta Sage",
        "verse_sanskrit": "दुर्लभोऽयं तुरीयातीतावधूतमार्गः । यदि कश्चिदेको विद्यते स एव नित्यपूतः स एव वेदपुरुष इति विदुषो मन्यन्ते । यस्य चित्तं मय्यन्तर्हितं तस्याहं दास इति ॥",
        "verse_tamil_translit": "துர்லபோயம் துரீயாதீதாவதூதமார்க்க: | யதி கஸ்சிதேகோ வித்யதே ஸ ஏவ நித்யபூத: ஸ ஏவ வேதபுருஷ இதி ||",
        "verse_meaning_english": "Exceedingly rare is this path of the Turiyatita Avadhuta! If even a single such sage exists, the wise revere him as eternally pure and as the very Veda-Purusha Himself; he whose mind is absorbed in Me, in him I Myself abide!",
        "verse_meaning_tamil": "இந்தத் துரீயாதீத அவதூத மார்க்கம் உலகில் மிக மிக அரிதானது! அத்தகைய மகாத்மா ஒருவர் இருந்தாலும், அவரே நித்திய பரிசுத்தர், அவரே சாட்சாத் வேத புருஷர் என ஞானிகள் போற்றுகின்றனர்; எவரது சித்தம் என்னில் முழுமையாக ஒடுங்கியுள்ளதோ, அவருள் நானே உறைகிறேன்!",
        "theme": "The culmination of the ascetic ladder where a Kutichaka rises step-by-step to Bahudaka, Hamsa, Paramahamsa, and finally Turiyatita Avadhuta—living effortlessly like a child without dualistic thought, buried in the caves of non-dual Pranava.",
        "SettingVisual": "Luminous cosmic-earthly sanctuary where golden sunlight illuminates a solitary Himalayan cave and a crystal mountain lake",
        "ProtagonistVisual": "Pitamaha Brahma bowing in reverence, and the Turiyatita Avadhuta sage seated in childlike, utterly unselfconscious bliss",
        "GuruVisual": "Lord Adinarayana radiating warm golden-sapphire effulgence",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic slow dolly-in across a sunlit Himalayan lotus lake toward a radiant stone sanctuary where Brahma questions Lord Adinarayana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot across a high Himalayan lotus lake at golden dawn. Pitamaha Brahma with white beard bows with folded hands before the luminous golden-blue aura of Lord Narayana seated on a carved stone dais. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "At the dawn of creation, Pitamaha Brahma approached his own Father, Lord Adinarayana, and asked: 'O Bhagavan! Explain to me the mystery of the Turiyatita Avadhuta—those rare souls who have transcended even the fourth state of consciousness! What is their path and their state of being?'",
                "vo_ta": "படைப்பின் தொடக்கத்தில், பிதாமகர் பிரம்மதேவர் ஆதிநாராயணப் பெருமானை அணுகி வினவினார்: 'பகவானே! நான்காவது நிலையான துரியத்தையும் கடந்த துரீயாதீத அவதூதர்களின் ரகசியத்தை எனக்கு அருள்வீராக! அவர்களின் வழி யாது? அவர்களின் அகநிலை எத்தகையது?'",
                "sub_cue": "Brahma asks Lord Narayana: 'What is the state of the Turiyatita Avadhuta who transcends even Turiya?'",
                "sound": "Deep cosmic Shankha resonance, gentle mountain water ripples, and a serene Saraswati Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium close-up of a solitary Avadhuta sage seated on a mossy rock in the forest while deer graze fearlessly beside him.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a solitary barefoot Indian Avadhuta yogi seated in effortless stillness on a mossy forest boulder at sunrise while spotted deer graze peacefully right beside him, sensing his total harmlessness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Narayana replied: 'Rare indeed in the universe is the path of the Turiyatita Avadhuta; it is never crowded! If even one such soul walks the earth, he is eternally pure, the very incarnation of the Veda-Purusha. Because his mind rests unceasingly in Me, I Myself am bound to him in love!'",
                "vo_ta": "பகவான் நாராயணர் அருளினார்: 'பிரம்மா! இந்தத் துரீயாதீத அவதூத மார்க்கம் பிரபஞ்சத்தில் மிக மிக அரிதானது! அத்தகைய மகாத்மா ஒருவர் பூமியில் இருந்தாலும், அவரே நித்திய பரிசுத்தர்; அவரே சாட்சாத் வேத புருஷர்! அவரது சித்தம் என்னில் நிலைத்திருப்பதால், நானும் அவருள் அன்பால் கட்டுப்பட்டிருக்கிறேன்!'",
                "sub_cue": "If even one Turiyatita Avadhuta walks the earth, he is the living Veda-Purusha!",
                "sound": "Warm Bansuri flute melody in Raga Yaman with soft forest ambience."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Smooth visual dissolve showing the ascetic's step-by-step maturation from Kutichaka to Bahudaka, Hamsa, Paramahamsa, and finally Turiyatita.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of an ancient Indian yogi stepping out of a shadow-lit cave into blinding golden morning sunlight, leaving behind wooden staff, water pot, and ochre cloth to stand in pure natural simplicity. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "How does one reach this summit? First, the Kutichaka matures into a Bahudaka; the Bahudaka matures into a Hamsa; the Hamsa ripens into a Paramahamsa; and through deep contemplation of the Self, the Paramahamsa blossoms into a Turiyatita Avadhuta, abandoning staff, water pot, waist-cord, loincloth, and all outer rites!",
                "vo_ta": "இச்சிகரத்தை அடைவது எவ்வாறு? முதலில் குடீசகன் பஹூதகனாக முதிர்ச்சியடைகிறான்; பஹூதகன் ஹம்சனாகவும், ஹம்சன் பரமஹம்சனாகவும் உயர்கிறான்; ஆழ்ந்த ஆத்ம விசாரத்தால் பரமஹம்சன் தண்டம், கமண்டலம், ஆடை மற்றும் சகல புறச் சடங்குகளையும் விடுத்து துரீயாதீத அவதூதனாக மலர்கிறான்!",
                "sub_cue": "From Kutichaka to Bahudaka, Hamsa, and Paramahamsa — ripening at last into Turiyatita Avadhuta.",
                "sound": "Gradually simplifying musical arrangement, stripping away percussion until only pure Veena and Tanpura remain."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of the Avadhuta's serene, childlike face as he partakes of fruit fallen naturally on the ground without calculation or pride.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of a radiant ancient Indian Avadhuta sage with a childlike blissful smile seated under a fruit tree in the forest at dawn, utterly free of ego or anxiety. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "His way of life is Gopravartika—taking whatever sustenance comes unasked, like a gentle cow grazing in a meadow, viewing food solely as medicine! Like a newborn child, he knows neither pride nor resentment; he neither blesses nor curses, moving through the world in unbroken inner silence.",
                "vo_ta": "அவரது வாழ்க்கை முறை 'கோப்ரவர்த்திகம்'—பசு புல்லை மேய்வது போல, வலியச் சென்று கேட்காமல் தானாகக் கிடைக்கும் ஆகாரத்தை உடற்பிணிக்குரிய மருந்தாக மட்டுமே ஏற்கிறார்! பச்சிளம் குழந்தையைப் போல மான-அவமானம் இன்றி, யாரையும் சபிக்காமலும் புகழாமலும் ஆழ்ந்த மௌனத்தில் உலாவுகிறார்.",
                "sub_cue": "Like a child free of ego, he moves through the world in unbroken inner silence.",
                "sound": "Gentle wind chimes and a playful yet deeply peaceful bamboo flute motif."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Slow zoom into the Avadhuta's heart and crown inside a quiet mountain cave as the golden vibration of Pranava fills the entire space.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic cinematic shot inside a Himalayan granite cave where the Turiyatita Avadhuta sits in motionless samadhi; golden rings of Omkara light radiate from his heart, dissolving the cave walls into boundless light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Withdrawing all senses into the heart, he contemplates the non-dual essence where waking, dream, and deep sleep have ceased. All dualities of knowledge and ignorance disappear, and through the direct realization of Pranava, the Avadhuta becomes one with the Absolute!",
                "vo_ta": "புலன்கள் அனைத்தையும் இதயத்தில் ஒடுக்கி, விழிப்பு, கனவு, ஆழ்ந்த உறக்கம் ஆகிய மூன்றும் அற்ற அத்வைதப் பொருளை அவர் தியானிக்கிறார். ஞானம்-அஞ்ஞானம் எனும் இருமைகள் மறைந்து, பிரணவத்தின் நேரடி அனுபூதியால் அவதூதர் பரம்பொருளோடு இரண்டறக் கலக்கிறார்!",
                "sub_cue": "Where waking, dream, and sleep cease, the Avadhuta merges into the non-dual Pranava.",
                "sound": "Deep, all-encompassing Omkara resonance filling the entire stereo field."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide cosmic shot of the Avadhuta seated on the mountain peak as golden light unites his form with the sun and the infinite sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of the Avadhuta sage seated on a high Himalayan peak at sunrise, his form glowing like a second sun of pure consciousness above a sea of golden clouds. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Such a sage is an Avadhuta because he has shaken off (avadhuta) every trace of karmic bondage! Having accomplished all that is to be accomplished, he abides forever in the state of Purnananda—the indivisible fullness of Brahman.",
                "vo_ta": "கர்ம பந்தங்களின் சுவடுகளை எல்லாம் உதறித் தள்ளியதால் அவர் 'அவதூதர்' எனப்படுகிறார்! அடைய வேண்டிய அனைத்தையும் அடைந்த கிருதகிருத்தியராய், பிரம்மத்தின் பிரிக்க முடியாத பூரண ஆனந்தத்தில் அவர் என்றென்றும் திளைத்திருக்கிறார்.",
                "sub_cue": "Having shaken off all karmic bonds, the Avadhuta abides forever in Purnananda.",
                "sound": "Soaring Saraswati Veena and celestial vocal drone in Raga Hamsanadam."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Serene pull-back over the Himalayan lotus lake as Brahma bows in gratitude before the golden light of Narayana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps pull-back shot across the tranquil Himalayan lotus lake at sunrise as Pitamaha Brahma bows in serene gratitude toward the golden light of Lord Narayana. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Turiyatita Avadhuta Upanishad: beyond waking, beyond dream, beyond sleep, and beyond even effortful meditation shines our true Self. May we rest in that childlike, fearless purity of Consciousness. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு துரீயாதீத அவதூத உபநிடதம் நிறைவுறுகிறது: விழிப்பு, கனவு, உறக்கம் மற்றும் முயற்சிகளையும் கடந்து நமது உண்மையான ஆத்மா ஒளிர்கிறது. குழந்தையைப் போன்ற அந்தக் களங்கமற்ற தூய உணர்வில் நாம் இளைப்பாறுவோமாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Rest in the fearless, childlike purity of Turiyatita Consciousness. Om Shanti.",
                "sound": "Vedic Shanti invocation 'Om Purnamadah' fading into peaceful mountain wind."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 10. SANNYASA (BRIHAT-SANNYASA) UPANISHAD (#65)
    {
        "story_id": "SANNYASA_10_BRIHAT_SANNYASA",
        "muktika_number": 65,
        "name_sanskrit": "संन्यासोपनिषद् (बृहत्संन्यासोपनिषद्)",
        "name_iast": "Saṃnyāsopaniṣad (Bṛhat-Saṃnyāsopaniṣad)",
        "name_tamil": "சந்நியாச (பிருஹத் சந்நியாச) உபநிடதம்",
        "name_english": "Sannyasa (Brihat-Sannyasa) Upanishad",
        "veda": "Sama Veda",
        "category": "Sannyasa",
        "story_title_english": "The Ascetic Who Moves Like a Python & a Bee: The Code of Brihat-Sannyasa",
        "story_title_tamil": "மலைப்பாம்பும் மலர் வண்டும் காட்டும் துறவு நெறி: பிருஹத் சந்நியாச உபநிடதம்",
        "characters": "The Assembly of Sama Vedic Rishis, The Illumined Acharya of Sannyasa Dharma, The Six Classes of Renunciates",
        "verse_sanskrit": "अजगरवृत्तिमास्थितः शयानो वा लब्धमश्नाति । माधूकरमश्नन् वसेदेकत्र न वसेत् । बद्धमुक्तो महीधरवदप्रकम्प्यः ॥",
        "verse_tamil_translit": "அஜகரவ்ருத்திமாஸ்தித: ஷயானோ வா லப்தமஷ்னாதி | மாதுகரமஷ்னன் வஸேதேகத்ர ந வஸேத் ||",
        "verse_meaning_english": "Adopting the way of the python (Ajagara-vritti), lying peacefully in one spot, he partakes only of what comes of its own accord; or gathering food like a honeybee without hurting any household, he never clings to one place, unshakeable like a mountain.",
        "verse_meaning_tamil": "மலைப்பாம்பின் இயல்பைக் கைக்கொண்டு (அஜகர விருத்தி), அமைதியாகத் தங்கித் தானாகக் கிடைப்பதை மட்டுமே உண்பான்; அல்லது மலரை வருத்தாத வண்டைப் போலப் பிட்சையேற்று, ஓரிடத்தில் பற்றுக்கொள்ளாமல் மலைபோல் அசையாது நிலைத்திருப்பான்.",
        "theme": "Rigorous purification of the ascetic order: rejecting six spiritual pitfalls (attachment to shelter, precious bowls, hoarding staffs, gluttony), living by Madhukara and Ajagara vritti, and merging external sacrificial fires into the fire of Prana.",
        "SettingVisual": "Ancient Sama Vedic forest gurukulam beside a rocky mountain cave and a lotus-filled stream at golden sunrise",
        "ProtagonistVisual": "Earnest Sama Vedic forest ascetics holding earthen bowls and wooden staffs, listening to the Acharya",
        "GuruVisual": "Venerable Sama Vedic Acharya seated on a granite boulder beneath a peepal tree, radiating unshakeable mountain-like stillness",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide crane shot descending through a Sama Vedic forest hermitage at dawn as ascetics gather before the venerable Acharya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an ancient Indian forest ashram at golden sunrise. Ascetic seekers in ochre and bark-cloth bow before a venerable white-bearded Acharya seated on a flat granite rock under a sacred peepal tree. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the sacred Sama Veda tradition, the sages gathered to hear the Brihat-Sannyasa Upanishad. Bowing before the Master, they asked: 'O Bhagavan, how does a seeker properly enter the sacred order of renunciation, and what are the subtle traps that can cause even a monk to fall?'",
                "vo_ta": "சாம வேதத்தின் புனித மரபில், பிருஹத் சந்நியாச உபநிடதத்தைக் கேட்க முனிவர்கள் கூடினர். குருவை வணங்கிய அவர்கள், 'பகவானே! ஒரு சாதகன் முறைப்படி துறவறத்தில் புகுவது எவ்வாறு? துறவியையும் வீழ்த்தக்கூடிய நுட்பமான மாயைப் பொறிகள் யாவை?' என்று கேட்டனர்.",
                "sub_cue": "The sages ask: 'How does one enter true Sannyasa, and what subtle traps must a monk avoid?'",
                "sound": "Resonant Sama Veda chant, morning forest birdsong, and a deep Tanpura drone."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium shot of a householder performing the final Vaisvanara offering, inhaling the warm smoke of the sacred fire into his own chest.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of a Vedic seeker kneeling before a glowing homa fire pit at dawn, warming his palms over the sacred flames and drawing them to his heart to internalize the fire into his own prana. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Acharya explained the rite of passage: 'Having tested his detachment, the seeker offers the final oblation to Vaisvanara and inhales the sacred fire into his own Prana! From that moment, his breath is his altar, his inhalation and exhalation are the sacrificial ladles, and self-knowledge is the eternal flame.'",
                "vo_ta": "துறவு பூணும் முறையை ஆச்சாரியர் விளக்கினார்: 'வைராக்கியத்தை உறுதி செய்த சாதகன், வைஸ்வானர அக்னியில் இறுதி ஆஹுதி அளித்து, அந்தப் புனித நெருப்பைத் தன் பிராணனிலேயே உள்வாங்கிக் கொள்கிறான்! அக்கணம் முதல் அவனது மூச்சே யாக குண்டம்; ஆத்ம ஞானமே அணையா ஜோதி!'",
                "sub_cue": "Inhaling the sacred fire into his own breath, the monk makes Prana his eternal altar.",
                "sound": "Crackling homa fire smoothly transitioning into deep, rhythmic yogic breathing and Veena notes."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Close-up of clay, wooden, and gourd begging bowls beside simple patched cloth, contrasting with forbidden gold, silver, and copper vessels.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of a simple dried bottle-gourd kamandalu, a clay bowl, and a wooden bowl resting on kusha grass in morning sunlight, symbolizing pure ascetic non-possession. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Master warned against the subtle snares of pseudo-renunciation: 'A monk must never touch bowls of gold, silver, or copper—only clay, wood, or bottle-gourd! Even in asceticism, six things bind the soul: attachment to a fixed dwelling, coveting fine bowls, hoarding staffs, gluttony, gathering disciples for pride, and trading in mantras or medicine!'",
                "vo_ta": "போலித் துறவின் நுட்பமான பொறிகளைக் குறித்து குரு எச்சரித்தார்: 'துறவி பொன், வெள்ளி, செம்புப் பாத்திரங்களைத் தொடக்கூடாது; மண், மரம் அல்லது சுரைக்குடுக்கையையே பயன்படுத்த வேண்டும்! ஒரே இடத்தில் பற்று, விலையுயர்ந்த பாத்திரம், உணவுப் பேராசை, பெருமைக்காகச் சீடர்களைச் சேர்த்தல் ஆகியவை துறவியையும் கட்டிப்போடும்!'",
                "sub_cue": "Shun gold and silver vessels; avoid pride of scholarship and attachment to fixed dwellings.",
                "sound": "Firm, clear Pakhawaj beat underscoring the austerity of the rule."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Split nature metaphor: a giant python resting motionless on a sunlit rock in the forest, and a yogi seated in equally unshakeable stillness outside a mountain cave.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a serene Turiyatita Avadhuta yogi seated in motionless samadhi on a sun-warmed granite ledge in the forest, as calm and unshakeable as a mountain peak at dawn. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Behold the two supreme modes of sustenance: Madhukara-vritti, gathering small morsels like a honeybee without taxing any household; and for the highest Avadhuta, Ajagara-vritti—the way of the python, resting in unbroken samadhi without anxiety for food, accepting only what Providence brings of its own accord!",
                "vo_ta": "துறவியின் இரு உயர்ந்த வாழ்க்கை நெறிகளைக் காணீர்: எந்த இல்லத்தையும் வருத்தாமல் வண்டைப் போலச் சிறிதளவு உணவேற்கும் மதுகர விருத்தி; மற்றும் அவதூதருக்கான அஜகர விருத்தி—மலைப்பாம்பைப் போல உணவுக் கவலையின்றி சமாதி நிலையில் தங்கி, இறை நியதியால் தானாகக் கிடைப்பதை மட்டுமே ஏற்கும் பக்குவம்!",
                "sub_cue": "अजगरवृत्तिमास्थितः — Abiding like the python in unbroken stillness, free from anxiety.",
                "sound": "Deep, grounded Rudra Veena drone with slow, meditative Bansuri phrases."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Slow zoom into the Acharya's radiant face as he chants the six-syllable and single-syllable mantras, golden light illuminating the disciples' hearts.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of the venerable Acharya and his ascetic disciples meditating together at sunrise; golden prana light radiates from their heart centers as they contemplate the supreme Omkara. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Giving up worldly logic and contentious debates, the true Sannyasin reflects solely on Vedanta! Like an actor changing costumes on a stage without becoming the role, the illumined sage witnesses the body's actions while abiding as the unchangeable, partless Brahman!",
                "vo_ta": "வீண் வாதங்களையும் உலகியல் தர்க்கங்களையும் விடுத்து, உண்மையான சந்நியாசி வேதாந்த விசாரத்தில் மட்டுமே நிலைத்திருக்கிறான்! நாடக மேடையில் வேடங்களை மாற்றும் நடிகன் அவ்வேடமாகவே மாறிவிடாதது போல, ஞானி உடலின் செயல்களைச் சாட்சியாகப் பார்த்துக்கொண்டு மாறாத பிரம்மமாகவேத் திகழ்கிறான்!",
                "sub_cue": "Like an actor unaffected by his costume, the Sage witnesses the body while abiding as Brahman.",
                "sound": "Luminous Saraswati Veena and Violin harmony in Raga Kalyani."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the liberated yogi standing unshakeable like a Himalayan peak as clouds drift past below him.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide heroic shot of an ancient Indian Paramahamsa yogi seated like an unshakeable mountain peak on a granite cliff while golden morning clouds drift peacefully below him. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Unshakeable like Mount Meru, pure as the autumn sky, he swims across the ocean of samsara and helps all beings cross over through his silent presence.",
                "vo_ta": "மேரு மலையைப் போல் அசைக்க முடியாதவராய், शरत् கால ஆகாயம் போல் நிர்மலமானவராய், சம்சாரப் பெருங்கடலைக் கடந்து தன் மௌன சந்நிதியால் உலகோரையும் அவர் கரையேற்றுகிறார்.",
                "sub_cue": "Unshakeable like a mountain, pure as the sky, the Jivanmukta abides in eternal freedom.",
                "sound": "Expansive conch shell and celestial Vedic chorus."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Pull-back shot from the Sama Vedic forest ashram as golden sunlight fills the canopy.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps serene pull-back shot of the ancient Indian forest hermitage bathed in golden morning sunbeams as the Acharya and disciples sit in silent peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Brihat-Sannyasa Upanishad: true renunciation is not an outer profession, but total inner freedom from greed, pride, and fear. Om Apyayantu Mamangani... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பிருஹத் சந்நியாச உபநிடதம் நிறைவுறுகிறது: உண்மையான துறவு என்பது புற வேடமல்ல; பேராசை, கர்வம், அச்சம் ஆகியவற்றிலிருந்து பெறும் அக விடுதலையே ஆகும். ஓம் ஆப்யாயந்து மமாங்கானி... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "True renunciation is total inner freedom from greed, pride, and fear. Om Shanti.",
                "sound": "Sama Veda Shanti Mantra fading into tranquil forest ambience."
            }
        ]
    },
    # 11. PARAMAHAMSA PARIVRAJAKA UPANISHAD (#66)
    {
        "story_id": "SANNYASA_11_PARAMAHAMSA_PARIVRAJAKA",
        "muktika_number": 66,
        "name_sanskrit": "परमहंसपरिव्राजकोपनिषद्",
        "name_iast": "Paramahaṃsaparivrājakopaniṣad",
        "name_tamil": "பரமஹம்ச பரிவ்ராஜக உபநிடதம்",
        "name_english": "Paramahamsa Parivrajaka Upanishad",
        "veda": "Atharva Veda",
        "category": "Sannyasa",
        "story_title_english": "Lord Narayana Teaches Brahma the Eightfold Pranava of the Wandering Swan",
        "story_title_tamil": "பரிவ்ராஜக பரமஹம்சரின் அஷ்டாங்க பிரணவம்: பிரம்மனுக்கு நாராயணர் உபதேசம்",
        "characters": "Pitamaha Brahma (The Creator Seeker), Bhagavan Adinarayana (The Supreme Guru), The Wandering Paramahamsa Parivrajaka",
        "verse_sanskrit": "अहमेव परं ब्रह्म अहमेव परं पदम् । सर्वज्ञोऽहं सर्वगतोऽहं सर्वेश्वरोऽहम् अद्वितीयोऽहं मत्तोऽन्यन्न किञ्चिदस्तीति ॥",
        "verse_tamil_translit": "அஹமேவ பரம் ப்ரஹ்ம அஹமேவ பரம் பதம் | ஸர்வக்ஞோஹம் ஸர்வகதோஹம் ஸர்வேஷ்வரோஹம் அத்விதீயோஹம் ||",
        "verse_meaning_english": "'I alone am the Supreme Brahman! I alone am the Supreme Abode! I am omniscient, all-pervading, the Lord of all, the One without a second; other than Me there is nothing whatsoever!'",
        "verse_meaning_tamil": "'நானே பரப்பிரம்மம்! நானே பரம பதம்! நானே சர்வக்ஞன், எங்கும் நிறைந்தவன், சர்வேஸ்வரன், இரண்டற்ற ஏகப் பரம்பொருள்; என்னைத் தவிர வேறொன்றும் இப் பிரபஞ்சத்தில் இல்லை!'",
        "theme": "The awakening from the exhaustion of worldly pleasure into the Paramahamsa Parivrajaka state, mastering the Eightfold Pranava (Ashtanga Omkara) and roaring the fearless lion-cry of non-duality.",
        "SettingVisual": "Luminous sacred river terrace surrounded by ancient carved stone pillars and Himalayan peaks at golden dawn",
        "ProtagonistVisual": "Pitamaha Brahma bowing before Adinarayana, and a noble householder renouncing his attachments to become a radiant Paramahamsa Parivrajaka",
        "GuruVisual": "Lord Adinarayana glowing with golden-sapphire light, imparting the secret of Ashtanga Pranava",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide cinematic crane shot over a sacred mountain river terrace at dawn where Pitamaha Brahma questions Lord Adinarayana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of a sacred Himalayan river terrace at golden sunrise. Pitamaha Brahma bows with folded hands before the radiant golden-blue presence of Lord Adinarayana seated on a lotus stone pedestal. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the sacred Atharva Veda, Pitamaha Brahma approached his Father, Lord Adinarayana, and asked: 'O Bhagavan, how does a seeker who has fulfilled his worldly duties awaken to the path of the Paramahamsa Parivrajaka—the wandering royal swan of liberation?'",
                "vo_ta": "அதர்வ வேதத்தின் புனித மரபில், பிதாமகர் பிரம்மதேவர் ஆதிநாராயணப் பெருமானை அணுகி வினவினார்: 'பகவானே! உலகக் கடமைகளை முடித்த ஒரு சாதகன், முக்தியின் அரச அன்னமான பரமஹம்ச பரிவ்ராஜக நிலையை அடைவது எவ்வாறு?'",
                "sub_cue": "Brahma asks Lord Narayana: 'How does one awaken to the state of the Paramahamsa Parivrajaka?'",
                "sound": "Deep Shankha call, flowing mountain river, and a majestic Rudra Veena introduction."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium shot of a wise householder looking with deep dispassion upon his wealth and family, turning toward a serene Guru in the forest.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a noble ancient Indian householder standing at the threshold of his home at dawn, turning away from worldly wealth with serene detachment to bow before a forest Guru. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Narayana replied: 'Just as a man exhausted from sense-pleasures longs only for deep restful sleep, so does the mature soul grow weary of the endless cycle of birth and death! Equipped with the fourfold qualification—discrimination, dispassion, sixfold serenity, and burning longing for liberation—he approaches a realized Guru.'",
                "vo_ta": "பகவான் நாராயணர் அருளினார்: 'இந்திரிய போகங்களால் களைப்படைந்த ஒருவன் ஆழ்ந்த உறக்கத்தை மட்டுமே நாடுவது போல, பக்குவப்பட்ட ஆத்மா பிறப்பு-இறப்புச் சுழற்சியிலிருந்து விடுபட ஏங்குகிறது! விவேகம், வைராக்கியம், சம-தமாதி षट्सम्पत्ति, முமுக்ஷுத்வம் ஆகிய சாதன சதுஷ்டயத்துடன் அவன் சற்குருவை அடைகிறான்.'",
                "sub_cue": "Weary of samsara, the seeker armed with Sadhana Chatushtaya approaches the Guru.",
                "sound": "Contemplative Bansuri melody in Raga Yaman with soft tanpura."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Slow tracking shot of the newly initiated monk casting his wooden sacrificial vessels into the fire and water, stepping forward free and unburdened.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps tracking shot of an ancient Indian ascetic standing by a sacred river at sunrise, offering his ritual implements to the water and stepping onto the forest path clothed only in simple ochre cloth, radiating inner freedom. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Offering the Viraja homa, he bids farewell to sons, friends, and possessions, proclaiming the Abhaya Mantra: 'Let no creature in the three worlds fear me; from me comes total fearlessness to all beings!' Abandoning even external emblems, he becomes a wandering Paramahamsa.",
                "vo_ta": "விரஜா ஹோமம் செய்து, சுற்றமும் உடமையும் நீத்து, 'மூவுலகிலும் உள்ள எந்த உயிரும் என்னால் அஞ்சற்க! என்னிடமிருந்து சகல உயிர்களுக்கும் அபயம் உண்டாகட்டும்!' என அபய வாக்கு அளிக்கிறான். புறச் சின்னங்களையும் கடந்து அவன் பரமஹம்ச பரிவ்ராஜகனாகப் புறப்படுகிறான்.",
                "sub_cue": "अभयं सर्वभूतेभ्यः — From me comes total fearlessness to all living beings!",
                "sound": "Warm mridangam cadence and uplifting choral Vedic chant 'Abhayam Sarvabhutebhyah'."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of the meditating Paramahamsa as an eight-petalled golden lotus of Pranava (A, U, M, Bindu, Nada, Kala, Kalatita, Paratpara) blooms in his heart.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of a meditating Paramahamsa yogi in a sunlit granite cave; a luminous eight-petalled golden lotus of prana light glows softly at his heart center, symbolizing the Ashtanga Pranava. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "His staff is silence; his begging bowl is the sky; his meditation is the Ashtanga Pranava—the eightfold Omkara comprising A-kara, U-kara, Ma-kara, Ardhamatra, Nada, Bindu, Kala, and Taraka! Through this inner sound, he dissolves the waking, dream, and causal bodies.",
                "vo_ta": "மௌனமே அவரது தண்டம்; ஆகாயமே அவரது பாத்திரம்; அகாரம், உகாரம், மகாரம், அர்த்தமாத்திரை, நாதம், விந்து, கலை, தாரகம் எனும் அஷ்டாங்க பிரணவமே அவரது தியானம்! இந்த உள் நாதத்தால் ஸ்தூல, சூட்சும, காரண சரீரங்களை அவர் கரைக்கிறார்.",
                "sub_cue": "Meditating on the Eightfold Pranava, the Yogi dissolves the three bodies into Pure Light.",
                "sound": "Eight-layered harmonic Omkara chime ascending into pure high-frequency resonance."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Heroic low-angle shot of the Paramahamsa standing atop a sunlit boulder, eyes shining with the realization of 'Ahameva Param Brahma'.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps low-angle heroic shot of an illumined Indian Paramahamsa sage standing on a sunlit mountain boulder at dawn, golden light radiating from his form as he abides in fearless non-dual realization. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then bursts forth the thunderous lion-roar of Advaita: 'Ahameva Param Brahma! I alone am the Supreme Brahman! I alone am the Supreme Abode! I am all-knowing, all-pervading, the One without a second—other than Me, nothing whatsoever exists!'",
                "vo_ta": "அப்போது அத்வைதத்தின் சிம்ம கர்ஜனை வெடித்துக் கிளம்புகிறது: 'அஹமேவ பரம் ப்ரஹ்ம! நானே பரப்பிரம்மம்! நானே பரம பதம்! நானே சர்வக்ஞன், எங்கும் நிறைந்தவன், இரண்டற்ற ஏகப் பரம்பொருள்—என்னைத் தவிர வேறொன்றும் இப் பிரபஞ்சத்தில் இல்லை!'",
                "sub_cue": "अहमेव परं ब्रह्म — I alone am the Supreme Brahman, the One without a second!",
                "sound": "Majestic crescendo of Shankha, Mridangam, and Saraswati Veena in Raga Shankarabharanam."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the Paramahamsa walking serenely along the riverbank, his reflection merging with the golden sun on the water.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of a serene barefoot Paramahamsa walking along a golden sunlit riverbank at dawn, his reflection in the calm water merging with the rising sun. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Established in this non-dual vision, he wanders the earth as a Jivanmukta—free while living, sanctifying the very dust beneath his feet, until his prana merges effortlessly into the Infinite.",
                "vo_ta": "இந்த அத்வைத தரிசனத்தில் நிலைபெற்ற அவர், வாழும்போதே முக்தனான ஜீவன்முக்தராய், தன் பாதம் படும் பூமியையெல்லாம் புனிதப்படுத்தியவாறு சஞ்சரித்து, இறுதியில் எல்லையற்ற பரம்பொருளில் இரண்டறக் கலக்கிறார்.",
                "sub_cue": "Sanctifying the earth beneath his feet, the Jivanmukta abides in effortless freedom.",
                "sound": "Serene flute and violin duet with gentle river waves."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane rise over the Himalayan river terrace as Brahma bows before Narayana in golden morning light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the sacred Himalayan river terrace bathed in golden dawn light, where Brahma and Lord Narayana sit in eternal peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Paramahamsa Parivrajaka Upanishad: grant fearlessness to every creature, and discover that the Supreme Lord of the Universe is your own innermost Self. Om Bhadram Karnebhih... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பரமஹம்ச பரிவ்ராஜக உபநிடதம் நிறைவுறுகிறது: சகல உயிர்களுக்கும் அபயம் அளித்து, பிரபஞ்ச நாயகனே நமது உள் ஆத்மா என்பதை உணர்வோமாக. ஓம் பத்ரம் கர்ணேபி:... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Grant fearlessness to all beings; realize the Supreme Brahman within. Om Shanti.",
                "sound": "Atharva Veda Shanti invocation fading into tranquil river resonance."
            }
        ]
    },
    # 12. KUNDIKA UPANISHAD (#74)
    {
        "story_id": "SANNYASA_12_KUNDIKA",
        "muktika_number": 74,
        "name_sanskrit": "कुण्डिकोपनिषद्",
        "name_iast": "Kuṇḍikopaniṣad",
        "name_tamil": "குண்டிகா உபநிடதம்",
        "name_english": "Kundika Upanishad",
        "veda": "Sama Veda",
        "category": "Sannyasa",
        "story_title_english": "The Water-Pot of Pure Sky: From Forest Hermit to Sky-Clad Yogi",
        "story_title_tamil": "தூய ஆகாயக் கமண்டலம்: வானப்பிரஸ்தத்திலிருந்து ஆகாய சந்நியாசிக்கு",
        "characters": "The Venerable Vanaprastha Elder, The Illumined Sannyasa Guru, The Sky-Wandering Yogi",
        "verse_sanskrit": "आकाशमेकाकी विहरेत् । पवनवच्चरेत् । नित्यं शुद्धो बुद्धो मुक्तः स्वभावतः । अहमेव परं ब्रह्म ॥",
        "verse_tamil_translit": "ஆகாஷமேகாகீ விஹரேத் | பவனவச்சரேத் | நித்யம் ஷுத்தோ புத்தோ முக்த: ஸ்வபாவத: ||",
        "verse_meaning_english": "Let him roam alone like the boundless sky! Let him move freely like the wind! By his very nature he is eternally pure, awakened, and free—realizing 'I alone am the Supreme Brahman!'",
        "verse_meaning_tamil": "ஆகாயத்தைப் போல் தனித்து விரிந்திருப்பானாக! காற்றைப் போல் சுதந்திரமாக உலாவுவானாக! இயல்பாகவே நித்திய பரிசுத்தனாய், விழிப்புணர்வு பெற்றவனாய், முக்தனாய், 'நானே பரப்பிரம்மம்' என உணர்ந்து நிலைத்திருப்பானாக!",
        "theme": "The poetic transformation from carrying an external water-pot (Kundika) and sandals to realizing that the body is moved by Prana like a chariot, wandering freely like the wind (Pavanavat) and resting in the spotless sky of Consciousness.",
        "SettingVisual": "Sunlit mountain forest hermitage transitioning to a high windswept ridge overlooking an endless sea of clouds",
        "ProtagonistVisual": "An elderly forest hermit carrying a traditional gourd water-pot (kundika), wooden staff, and bark-cloth, awakening into a radiant yogi",
        "GuruVisual": "The Inner Guru / Illumined Master seated by a crystal mountain spring at sunrise",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly shot through a sunlit forest hermitage focusing on a gourd water-pot (kundika) resting beside a crystal spring as an elder hermit bows to his Guru.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot in an ancient Indian forest ashram at dawn. A traditional gourd water-pot (kundika) and bamboo staff rest beside a crystal spring while an elderly forest hermit bows before a radiant Guru. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Sama Veda's Kundika Upanishad, the seeker who has completed studenthood, household duties, and forest austerity stands at the threshold of supreme renunciation. Looking at his gourd water-pot—the Kundika—he asks: 'What is the final step from outer asceticism into boundless liberation?'",
                "vo_ta": "சாம வேதத்தின் குண்டிகா உபநிடதத்தில், பிரம்மச்சரியம், இல்லறம், வானப்பிரஸ்தம் ஆகிய நிலைகளைக் கடந்த சாதகன் பரம துறவின் வாசலில் நிற்கிறான். தன் கமண்டலமான குண்டிகையைப் பார்த்தவாறு, 'புறத் தவத்திலிருந்து எல்லையற்ற முக்திக்குச் செல்லும் இறுதிப் படி யாது?' என்று வினவுகிறான்.",
                "sub_cue": "At the threshold of renunciation, the seeker asks: 'What is the final step into boundless freedom?'",
                "sound": "Trickling mountain spring water, morning birdsong, and a gentle Tanpura and Veena prelude."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium shot of the seeker offering his ritual fires into his own breath and burying the wooden fire-sticks in the earth.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a Vedic forest hermit kneeling by a dying homa fire at sunrise, drawing the last warm breath of the sacred fire into his chest with serene devotion. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "First, the seeker consigns the external fires into his own vital breath and leaves behind wife, sons, and lands. Taking only an ochre robe, a staff, and the Kundika water-pot to guard purity, he steps out into the trackless forest of self-inquiry.",
                "vo_ta": "முதலில், சாதகன் புற அக்னியைத் தன் பிராணனிலேயே ஒடுக்கி, சுற்றமும் நிலமும் துறக்கிறான். தூய்மை காக்கக் காவியாடையும், தண்டமும், குண்டிகை எனும் கமண்டலமும் மட்டும் ஏந்தி ஆத்ம விசாரப் பாதையில் அடியெடுத்து வைக்கிறான்.",
                "sub_cue": "Merging the sacred fire into his breath, the seeker steps onto the path of self-inquiry.",
                "sound": "Soft crackling embers dissolving into a steady, rhythmic Bansuri melody."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Tracking shot of the monk sleeping peacefully on river sand under the stars, resting his head upon his own arm as a pillow.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a serene ancient Indian sannyasin resting peacefully on clean white river sand under a twilight sky, using his own folded arm as a pillow while a gentle breeze blows. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Look at the royal simplicity of the awakened monk: the earth itself is his couch, his own arm is his pillow, the open sky is his canopy, and his hands are his begging bowl! Rejoicing in whatever comes unasked, he fears neither heat nor cold.",
                "vo_ta": "விழிப்படைந்த துறவியின் அரச எளிமையைக் காணீர்: பூமியே அவரது படுக்கை; தன் கையே அவருக்குத் தலையணை; விரிந்த வானமே கூரை; தன் உள்ளங்கைகளே பிட்சைப் பாத்திரம்! கிடைப்பதில் மகிழ்ந்து, குளிர்-வெப்பம் கண்டு அஞ்சாமல் அவர் வாழ்கிறார்.",
                "sub_cue": "The Earth is his bed, his arm is his pillow, and the boundless sky is his roof!",
                "sound": "Gentle evening river breeze and a soothing Sarangi solo in Raga Behag."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Dynamic shot of wind moving through tall mountain grass and clouds sailing across the sky, cross-dissolving to the yogi walking effortlessly.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of golden morning wind sweeping across high mountain grass and white clouds, as a barefoot Indian yogi walks effortlessly along the ridge like the wind itself. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Pavanavac-charet—he moves like the wind, leaving no footprints of attachment anywhere! Just as water drops roll off a lotus leaf without wetting it, actions no longer cling to him. When someone strikes or insults the body, he knows: 'Who strikes whom? Only one Self pervades all!'",
                "vo_ta": "பவனவச்சரேத் — காற்றைப் போல் எங்கும் பற்றின் சுவடின்றி அவர் உலாவுகிறார்! தாமரை இலையில் நீர் ஒட்டாதது போல் கர்மங்கள் அவரைத் தீண்டுவதில்லை. உடலை எவரேனும் நிந்தித்தாலும், 'யார் யாரை அடிப்பது? எங்கும் நிறைந்திருப்பது ஒரே ஆத்மாவன்றோ!' என அமைதி காக்கிறார்.",
                "sub_cue": "पवनवच्चरेत् — Move freely like the wind, untouched like a lotus leaf in water!",
                "sound": "Swirling mountain breeze blending with airy, effortless flute arpeggios."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Close-up of the gourd water-pot left behind on a rock by the stream, while the yogi sits higher up the mountain in glowing samadhi.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a gourd kundika water-pot left behind on a mossy stone beside a stream, while in the sunlit background the yogi sits in radiant samadhi on a high rock ledge. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "At the summit of Yoga, even the external Kundika is transcended, for his own body has become the vessel filled to the brim with the immortal nectar of Chidakasha! Awakening from the dream of duality, he proclaims: 'I was never born, I never die; I am eternally pure, awakened, and free!'",
                "vo_ta": "யோகத்தின் உச்சியில் புறக் கமண்டலமும் கைவிடப்படுகிறது; ஏனெனில் சிதாகாச அமிர்தம் ததும்பும் கலசமாகவே அவரது உள்ளம் மாறிவிடுகிறது! இருமை எனும் கனவிலிருந்து விழித்தெழுந்து, 'நான் பிறந்ததுமில்லை, இறப்பதுமில்லை; இயல்பாகவே நான் நித்திய பரிசுத்தன், புத்தன், முக்தன்!' என்று முழங்குகிறார்.",
                "sub_cue": "नित्यं शुद्धो बुद्धो मुक्तः स्वभावतः — By nature I am eternally pure, awakened, and free!",
                "sound": "Resonant bronze bell chime and soaring Saraswati Veena crescendo."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide panoramic shot of the yogi seated on the mountain peak, his aura merging into the vast golden-blue dome of the sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps panoramic shot of the illumined yogi seated in padmasana on a mountain peak under a vast golden-blue sky, radiating serene light across the valley. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Seeing the entire cosmos as a mirage in the desert of Brahman, he rests in the fourth state, Turiya—the Witness of waking, dream, and deep sleep, shining in his own self-luminous glory.",
                "vo_ta": "பிரபஞ்சம் முழுவதையும் பிரம்மத்தில் தோன்றும் கானல் நீராகக் கண்டு, விழிப்பு, கனவு, உறக்கம் ஆகிய மூன்றிற்கும் சாட்சியான துரிய நிலையில் சுயம்பிரகாசமாய் அவர் வீற்றிருக்கிறார்.",
                "sub_cue": "Beholding the cosmos as a mirage in Brahman, the Yogi rests in self-luminous Turiya.",
                "sound": "Deep Tanpura and harmonic singing bowls in spacious resonance."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow pull-back into the golden morning clouds above the mountain ridge.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot rising into golden morning clouds above a serene Indian mountain ridge and crystal stream. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Kundika Upanishad: may our minds be like the lotus leaf untouched by sorrow, and may our spirit roam free like the wind in the sky of Consciousness. Om Apyayantu Mamangani... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு குண்டிகா உபநிடதம் நிறைவுறுகிறது: நம் மனம் துன்பம் ஒட்டாத தாமரை இலை போலவும், நம் ஆன்மா சிதாகாசத்தில் உலாவும் சுதந்திரக் காற்று போலவும் திகழ்வதாக. ஓம் ஆப்யாயந்து மமாங்கானி... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Be untouched like the lotus leaf; roam free in the sky of Consciousness. Om Shanti.",
                "sound": "Sama Veda Shanti invocation fading into gentle wind and stream sounds."
            }
        ]
    },
    # 13. PARABRAHMA UPANISHAD (#78)
    {
        "story_id": "SANNYASA_13_PARABRAHMA",
        "muktika_number": 78,
        "name_sanskrit": "परब्रह्मोपनिषद्",
        "name_iast": "Parabrahmapaniṣad",
        "name_tamil": "பரப்பிரம்ம உபநிடதம்",
        "name_english": "Parabrahma Upanishad",
        "veda": "Atharva Veda",
        "category": "Sannyasa",
        "story_title_english": "The Knot of the Heart & The Thread of Supreme Brahman: Shaunaka & Pippalada",
        "story_title_tamil": "இதய முடிச்சும் பரப்பிரம்ம பூணூலும்: சௌனகர் மற்றும் பிப்பலாதர்",
        "characters": "Maharishi Shaunaka (The Great Questioner), Sage Pippalada (Master of Brahmavidya), The True Brahmana Knower of Parabrahman",
        "verse_sanskrit": "शिखा ज्ञानमयी यस्य उपवीतं च तन्मयम् । ब्राह्मण्यं सकलं तस्य इति ब्रह्मविदो विदुः ॥ यदक्षरं परं ब्रह्म तत्सूत्रमिति धारयेत् ॥",
        "verse_tamil_translit": "ஷிகா க்ஞானமயீ யஸ்ய உபவீதம் ச தன்மயம் | ப்ராஹ்மண்யம் ஸகலம் தஸ்ய இதி ப்ரஹ்மவிதோ விது: ||",
        "verse_meaning_english": "He whose tuft is made of Pure Knowledge and whose sacred thread is also made of That—he possesses complete Brahminhood; so declare the knowers of Brahman! Let the wise wear that Imperishable Parabrahman as his true Sutra.",
        "verse_meaning_tamil": "எவருக்குத் தூய ஞானமே குடுமியாகவும், அப்பிரம்ம நிஷ்டையே பூணூலாகவும் உள்ளதோ, அவருக்கே பூரண பிரம்மத்துவம் உண்டு என பிரம்மஞானிகள் கூறுகின்றனர்! அழிவற்ற பரப்பிரம்மத்தையே தனது சூத்திரமாக ஞானி தரிக்க வேண்டும்.",
        "theme": "The inner anatomy of the four states in the ninety-six-finger-measured body, the ninety-six tattvas, and the revolutionary teaching that outward cotton threads and hair tufts are mere symbols—true Brahminhood belongs only to one whose Shikha and Upavita are Jnana itself.",
        "SettingVisual": "Ancient Atharva Vedic granite courtyard and banyan hermitage illuminated by golden morning sunlight and brass oil lamps",
        "ProtagonistVisual": "Maharishi Shaunaka seated with palm-leaf manuscripts, questioning with deep reverence",
        "GuruVisual": "Sage Pippalada radiating golden yogic prana, pointing to the inner lotus of the heart",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly-in across a sunlit granite courtyard under a banyan tree as Maharishi Shaunaka bows before Sage Pippalada.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot in an ancient Indian granite courtyard under a sacred banyan tree at dawn. Maharishi Shaunaka bows with folded hands before radiant Sage Pippalada seated on a kusha mat beside brass oil lamps. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Atharva Veda's Parabrahma Upanishad, the great seeker Maharishi Shaunaka approached Sage Pippalada and asked: 'O Bhagavan! What is the true Karmadhikara and Brahmavidya? How does the Supreme Brahman dwell within this ninety-six-finger-measured human body?'",
                "vo_ta": "அதர்வ வேதத்தின் பரப்பிரம்ம உபநிடதத்தில், மகா சாதகரான சௌனக மகரிஷி பிப்பலாத முனிவரை அணுகி வினவினார்: 'பகவானே! தொண்ணூற்றாறு அங்குல அளவுடைய இம்மனித உடலினுள் பரப்பிரம்மம் எவ்வாறு உறைகிறது? உண்மையான பிரம்மவித்தை யாது?'",
                "sub_cue": "Shaunaka asks Pippalada: 'How does Parabrahman dwell within this human temple?'",
                "sound": "Resonant temple bell, morning koel call, and a deep Tanpura drone in Raga Chakravakam."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Shaunaka's meditative face as four subtle golden lotus lights glow at the navel, heart, throat, and crown.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi in padmasana; subtle golden lotus lights glow at his navel, heart, throat, and crown chakra as Sage Pippalada instructs him. Warm golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Pippalada revealed the inner mystery: 'Within the wheel of the heart dwells the Purusha along with Prana! When he abides in the throat and eye, he experiences dream and waking; in the heart, deep sleep; and rising to the crown, he realizes the fourth transcendent state—Turiya, the spotless Parabrahman!'",
                "vo_ta": "பிப்பலாதர் அக ரகசியத்தை வெளியிட்டார்: 'இதயச் சக்கரத்தினுள் பிராணனுடன் புருஷன் உறைகிறான்! கண்ணிலும் கண்டத்திலும் விழிப்பு மற்றும் கனவையும், இதயத்தில் ஆழ்ந்த உறக்கத்தையும் கடந்து, சிரசின் உச்சியில் நான்காவது நிலையான களங்கமற்ற துரிய பரப்பிரம்மத்தை அவன் உணர்கிறான்!'",
                "sub_cue": "Rising beyond waking, dream, and deep sleep, the Purusha shines in the crown as Turiya.",
                "sound": "Ascending four-note Bansuri motif with subtle harmonic chimes."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of Pippalada holding up a strand of white cotton thread next to a glowing golden flame of camphor.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of Sage Pippalada holding a white cotton thread beside a blazing brass camphor lamp in a stone mandapam, teaching Shaunaka the difference between outer symbol and inner light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Pippalada contrasted outer ritual with inner realization: 'For those still bound to worldly action, the external tuft and cotton thread are prescribed as reminders. Yet a mere cotton thread spun from plant fibers does not make one a knower of Brahman! Only when the knot of ignorance in the heart is untied is the true Granthi formed!'",
                "vo_ta": "புறச் சடங்கிற்கும் அக ஞானத்திற்கும் உள்ள வேறுபாட்டை பிப்பலாதர் விளக்கினார்: 'கர்மத்தில் உழல்பவர்களுக்கு நினைவூட்டலாகவே புறக் குடுமியும் பருத்திப் பூணூலும் விதிக்கப்பட்டன. ஆனால் வெறும் பருத்தி நூல் ஒருவனைப் பிரம்மஞானி ஆக்கிவிடாது! இதயத்து அறியாமை முடிச்சு அவிழும் போதே உண்மையான பிரம்ம முடிச்சு ஏற்படுகிறது!'",
                "sub_cue": "Mere cotton fibers do not make a knower of Brahman; untie the knot of ignorance in the heart!",
                "sound": "Steady Pakhawaj beat and a probing Saraswati Veena melody."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Macro shot of white pearls strung upon a golden thread, dissolving into planets and stars strung upon a cosmic golden thread of Consciousness.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps macro-to-wide cinematic shot of luminous white pearls strung on a golden thread resting on a palm leaf, dissolving into a glowing golden thread of light connecting the heart of a meditating sage to the stars. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Why is the Supreme Self called Sutra? Because just as pearls are strung upon a single thread, this entire universe of beings is strung upon the Imperishable Parabrahman! And why is wisdom called Shikha? Because like the topmost peak of a flame, the realization 'I am Brahman' rises at the summit of awareness!",
                "vo_ta": "பரமாத்மா ஏன் 'சூத்திரம்' எனப்படுகிறார்? முத்துக்கள் ஒரே நூலில் கோர்க்கப்பட்டிருப்பது போல, இப் பிரபஞ்சத்து உயிர்கள் அனைத்தும் அழிவற்ற பரப்பிரம்மத்தில் கோர்க்கப்பட்டுள்ளன! தீபத்தின் உச்சிச் சுடரைப் போல 'நானே பிரம்மம்' என்ற ஞானம் உணர்வின் சிகரத்தில் ஒளிர்வதால் அதுவே உண்மையான 'சிகை' எனப்படுகிறது!",
                "sub_cue": "As pearls on a thread, the cosmos is strung on Parabrahman; Jnana is the flame-crest Shikha!",
                "sound": "Shimmering Santoor cascades and warm Violin sustain."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of an awakened Paramahamsa with shaven head and bare chest, radiating a golden crown-flame and heart-thread of light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of an awakened Indian Paramahamsa with shaven head and bare torso seated at dawn; a golden flame of light shines at his crown and a luminous golden thread of prana glows across his heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Pippalada declared the supreme verse: 'Shikha jnanamayi yasya, upavitam cha tanmayam—he whose tuft is made of Pure Knowledge and whose sacred thread is made of Brahman itself, he alone possesses complete Brahminhood! Casting off the outer thread, let the wise wear the Imperishable Parabrahman!'",
                "vo_ta": "பிப்பலாதர் பரம சுலோகத்தை முழங்கினார்: 'ஷிகா க்ஞானமயீ யஸ்ய உபவீதம் ச தன்மயம் — எவருக்குத் தூய ஞானமே குடுமியாகவும், பிரம்ம நிஷ்டையே பூணூலாகவும் உள்ளதோ, அவருக்கே பூரண பிரம்மத்துவம் உண்டு! புறப் பூணூலைத் துறந்து, அழிவற்ற பரப்பிரம்மத்தையே ஞானி தரிப்பானாக!'",
                "sub_cue": "शिखा ज्ञानमयी यस्य उपवीतं च तन्मयम् — Whose Shikha and Upavita are Pure Knowledge, he is the true Brahmana!",
                "sound": "Triumphant conch shell and resonant Vedic chorus chanting the verse."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide crane shot of Shaunaka and Pippalada seated in luminous stillness under the banyan tree as golden sunlight floods the courtyard.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of Sage Pippalada and Maharishi Shaunaka meditating in a sunlit granite courtyard beneath a giant banyan tree, enveloped in golden morning radiance. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "For such a knower of Parabrahman, there is no longer any ritual obligation, no impurity, and no fear of return—for he has become the seamless fabric of Consciousness itself.",
                "vo_ta": "அத்தகைய பரப்பிரம்ம ஞானிக்கு இனி எந்தச் சடங்கு நிர்ப்பந்தமும் இல்லை, களங்கமும் இல்லை, மறுபிறவி அச்சமும் இல்லை—ஏனெனில் அவர் பிரிக்க முடியாத தூய உணர்வாகவே மாறிவிட்டார்.",
                "sub_cue": "Free from ritual obligation and rebirth, the Knower becomes Parabrahman itself.",
                "sound": "Serene Bansuri and Tanpura harmony in Raga Bhupalam."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow pull-back from the banyan courtyard into the golden morning sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps pull-back shot from the ancient Indian banyan tree courtyard into the golden sunrise sky, radiating timeless wisdom and peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Parabrahma Upanishad: kindle the flame-crest of Self-Knowledge at your crown, and wear the thread of universal oneness in your heart. Om Bhadram Karnebhih... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பரப்பிரம்ம உபநிடதம் நிறைவுறுகிறது: நம் சிரசில் ஆத்ம ஞானச் சுடரை ஏற்றி, இதயத்தில் பிரபஞ்ச ஒருமைப்பாடு எனும் பிரம்ம சூத்திரத்தைத் தரிப்போமாக. ஓம் பத்ரம் கர்ணேபி:... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Kindle the flame of Self-Knowledge; wear the thread of Universal Oneness. Om Shanti.",
                "sound": "Atharva Veda Shanti Mantra fading into gentle morning birdsong."
            }
        ]
    },
    # 14. AVADHUTA UPANISHAD (#79)
    {
        "story_id": "SANNYASA_14_AVADHUTA",
        "muktika_number": 79,
        "name_sanskrit": "अवधूतोपनिषद्",
        "name_iast": "Avadhūtopaniṣad",
        "name_tamil": "அவதூத உபநிடதம்",
        "name_english": "Avadhuta Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "The Four Immortal Letters of A-Va-Dhu-Ta: Lord Dattatreya & Sage Sankriti",
        "story_title_tamil": "அ-வ-தூ-த எனும் நான்கு அழியா எழுத்துக்கள்: பகவான் தத்தாத்ரேயர் மற்றும் சான்கிருதி",
        "characters": "Lord Dattatreya (Adi-Guru of Avadhutas), Sage Sankriti (Devoted Vedic Seeker)",
        "verse_sanskrit": "अक्षरत्वाद्वरेण्यत्वाद्धूतसंसारबन्धनात् । तत्त्वमस्यादिलक्ष्यत्वाच्चावधूत इतीर्यते ॥ न निरोधो न चोत्पत्तिर्न बद्धो न च साधकः । न मुमुक्षुर्न वै मुक्त इत्येषा परमार्थता ॥",
        "verse_tamil_translit": "அக்ஷரத்வாத் வரேண்யத்வாத் தூதஸம்ஸாரபந்தனாத் | தத்வமஸ்யாதிலக்ஷ்யத்வாச்சாவதூத இதீர்யதே ||",
        "verse_meaning_english": "Because he is Imperishable (Akshara), because he is Supreme (Varenya), because he has shaken off the bonds of samsara (Dhuta-samsara-bandhana), and because he is the direct meaning of 'Tat Tvam Asi' (Ta)—he is called an Avadhuta!",
        "verse_meaning_tamil": "அழிவற்றவராக இருப்பதால் 'அ', போற்றத்தக்க உச்ச நிலையில் இருப்பதால் 'வ', சம்சார பந்தங்களை உதறித் தள்ளியதால் 'தூ', 'தத் த்வம் அஸி' எனும் மகாவாக்கியத்தின் உட்பொருளாகத் திகழ்வதால் 'த' — இ چهار எழுத்துக்களின் இணையானவரே 'அவதூதர்' எனப்படுகிறார்!",
        "theme": "Lord Dattatreya's breathtaking etymology of the four syllables A-Va-Dhu-Ta to Sage Sankriti, culminating in the ultimate Advaita realization that there is neither dissolution nor creation, neither bound nor seeker, neither aspirant nor liberated.",
        "SettingVisual": "Sacred Audumbara (cluster-fig) tree grove on the slopes of Mount Sahyadri/Girnar at golden sunrise, surrounded by misty valleys",
        "ProtagonistVisual": "Sage Sankriti in white bark-cloth and rudraksha, kneeling with folded hands and luminous devotion",
        "GuruVisual": "Lord Dattatreya, radiant young-eternal Avadhuta Guru with matted locks, serene blissful smile, seated beneath the sacred Audumbara tree",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly-in through a misty Sahyadri mountain grove at dawn toward a sacred Audumbara tree where Sage Sankriti bows before Lord Dattatreya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot in an ancient Indian mountain grove at golden sunrise. Sage Sankriti kneels with folded hands before the radiant, serene figure of Lord Dattatreya seated under a sacred Audumbara fig tree. Golden sunbeams pierce the morning mist. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Beneath the sacred Audumbara tree where silence itself sings the Vedas, Sage Sankriti approached Bhagavan Dattatreya—the primordial Master of Yogis—and asked: 'O Lord! Who is truly an Avadhuta? What is his definition, his state of consciousness, and his way of moving through the world?'",
                "vo_ta": "மௌனமே வேதமாய் ஒலிக்கும் புனித அத்தி மரத்தடியில், யோகியரின் ஆதிகுருவான பகவான் தத்தாத்ரேயரை அணுகிய சான்கிருதி முனிவர் பணிவுடன் கேட்டார்: 'பகவானே! உண்மையான அவதூதர் யார்? அவரது இலக்கணம் யாது? அவரது அகநிலையும் சஞ்சார முறையும் எத்தகையது?'",
                "sub_cue": "Sage Sankriti asks Lord Dattatreya: 'Who is an Avadhuta, and what is his state of being?'",
                "sound": "Gentle mountain wind, morning birdsong, and a divine Rudra Veena and Bansuri prelude in Raga Bhairav."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Lord Dattatreya's compassionate, radiant eyes as four subtle golden Sanskrit syllables (A - Va - Dhu - Ta) shimmer as light in the air.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Lord Dattatreya's serene, luminous face bathed in golden dawn light under the Audumbara tree, four subtle golden sparks of prana light glowing in the air as he instructs Sage Sankriti. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "With infinite compassion, Lord Dattatreya unveiled the four immortal syllables of the word Avadhuta: 'A stands for Akshara—he is Imperishable! Va stands for Varenya—he is the Supreme crest-jewel of existence! Dhu stands for Dhuta-samsara-bandhana—he has shaken off every bond of worldly delusion! And Ta stands for Tat Tvam Asi—he is the living truth of Thou Art That!'",
                "vo_ta": "அளவற்ற கருணையுடன் பகவான் தத்தாத்ரேயர் 'அவதூத' எனும் நான்கு அழியா எழுத்துக்களின் ரகசியத்தை அருளினார்: 'அ என்பது அக்ஷரம்—அவர் அழிவற்றவர்! வ என்பது வரேண்யம்—அவர் போற்றத்தக்க உச்ச நிலையினர்! தூ என்பது தூத-சம்சார-பந்தனம்—உலக மாயைத் தளைகளை உதறித் தள்ளியவர்! த என்பது தத் த்வம் அஸி—நீயே அது என்ற மகாவாக்கியத்தின் வடிவானவர்!'",
                "sub_cue": "A = Imperishable, Va = Supreme, Dhu = Shaken off Samsara, Ta = Tat Tvam Asi!",
                "sound": "Four resonant bronze bell strikes accompanying the four explanations, over a warm Tanpura drone."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium tracking shot of an Avadhuta walking effortlessly through forest and village, unconcerned with caste, stage of life, or social convention.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium tracking shot of a serene barefoot Avadhuta yogi walking peacefully along a sunlit forest trail, his gaze steady and inward, radiating supreme equanimity and joy. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Having transcended all stages of life and caste, remaining ever absorbed in the Self alone, he moves free like a great yogi! Just as a chariot moves on the road while its passenger sits unconcerned inside, the Avadhuta allows the body to be sustained by whatever comes while his mind never wavers from Brahman.",
                "vo_ta": "வர்ண-ஆசிரம எல்லைகளைக் கடந்து எப்போதும் ஆத்மாவிலேயே திளைத்திருக்கும் அவர், மகா யோகியாய்ச் சுதந்திரமாக உலாவுகிறார்! தேர் பாதையில் செல்லும்போது உள்ளே அமர்ந்திருப்பவன் சலனமின்றி இருப்பது போல, உடலின் இயக்கங்களைப் பிராரப்தத்திற்கு விட்டுவிட்டு அவதூதரின் மனம் பிரம்மத்திலேயே நிலைத்திருக்கிறது.",
                "sub_cue": "Transcending varna and ashrama, the Avadhuta abides unceasingly in the Self alone.",
                "sound": "Flowing Carnatic violin melody in Raga Anandabhairavi with gentle mridangam pulse."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Cinematic visual metaphor: the bright sun shining equally upon a sacred Ganges ghat and a humble village courtyard without ever being tainted.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of the golden morning sun shining brilliantly over both a sacred stone river ghat and a humble forest clearing, its rays pure and untainted everywhere, as Dattatreya teaches Sankriti. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Just as the Sun shines upon all places and consumes all moisture without ever losing its purity, so the Avadhuta yogi partakes of whatever comes without ever being stained! Even if he performs actions for the welfare of the world, knowing 'I do nothing at all,' no karma ever touches him.",
                "vo_ta": "சூரியன் எல்லா இடங்களிலும் ஒளிவீசி நீரைக் கவர்ந்தாலும் தன் தூய்மையை இழக்காதது போல, அவதூத யோகியை எந்த வினையும் களங்கப்படுத்துவதில்லை! உலக நன்மைக்காகச் செயல்கள் புரிந்தாலும், 'நான் எதையும் செய்பவனல்ல' என்ற ஞானத்தால் கர்மம் அவரைத் தீண்டுவதில்லை.",
                "sub_cue": "Pure as the all-illuminating Sun, the Avadhuta is never stained by action.",
                "sound": "Bright, luminous Santoor and Bansuri interplay."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic slow zoom into Dattatreya's eyes as he proclaims the pinnacle verse of Advaita ('Na nirodho na chotpattih'), golden light filling the screen.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of Lord Dattatreya in radiant samadhi under the Audumbara tree, golden cosmic light radiating from his heart and illuminating Sage Sankriti's awakened face. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Dattatreya spoke the ultimate thunderbolt of Supreme Truth: 'Na nirodho na chotpattir, na baddho na cha sadhakah, na mumukshur na vai mukta, ity esha paramarthata—there is neither destruction nor creation, none is bound and none is a struggling seeker, none is longing for liberation and none is newly liberated—this is the Supreme Absolute Truth!'",
                "vo_ta": "அப்போது தத்தாத்ரேயர் பரமார்த்த சத்தியத்தின் இடிமுழக்கத்தை வெளியிட்டார்: 'ந நிரோதோ ந சோத்பத்திர் ந பத்தோ ந ச சாதக: ந முமுக்ஷுர் ந வை முக்த இத்யேஷா பரமார்த்ததா — அழிவும் இல்லை, படைப்பும் இல்லை; கட்டுண்டவனும் இல்லை, சாதகனும் இல்லை; முக்தி தேடுபவனும் இல்லை, புதிதாக முக்தி அடைந்தவனும் இல்லை—இதுவே பரம சத்தியம்!'",
                "sub_cue": "न निरोधो न चोत्पत्तिर्न बद्धो न च साधकः — Neither creation nor destruction, neither bound nor seeker: this is the Supreme Truth!",
                "sound": "Deep conch shell and majestic Vedic choral chant of 'Na Nirodho Na Chotpattih'."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide orbital shot of Sankriti and Dattatreya seated in blissful silence as the entire mountain grove shimmers with one golden Consciousness.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps orbital wide shot of Lord Dattatreya and Sage Sankriti seated in deep samadhi beneath the Audumbara tree, surrounded by a luminous golden field of oneness uniting mountain, forest, and sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Hearing this, Sankriti's final veil of duality vanished. Resting in the fullness of the Self, he realized: 'How can I bow to myself? I am the One Indivisible Consciousness without parts or limits!'",
                "vo_ta": "இதைக் கேட்ட சான்கிருதி முனிவரின் இறுதி மாயைத் திரையும் விலகியது. ஆத்ம பூரணத்தில் திளைத்தவராய், 'எனக்கு நானே எவ்வாறு நமஸ்காரம் செய்வேன்? எல்லைகளற்ற அந்த ஏக சைதன்யப் பரம்பொருளே நான்!' என உணர்ந்தார்.",
                "sub_cue": "Resting in indivisible fullness, the Sage beholds the One Self without a second.",
                "sound": "Spacious Saraswati Veena and harmonic Tanpura resonance."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane rise above the Audumbara tree into the golden morning sky over Mount Sahyadri.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial crane shot rising above the sacred Audumbara tree and golden mountain peaks at sunrise, radiating eternal peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Avadhuta Upanishad: he who meditates upon this truth becomes Kritakritya—completely fulfilled, purified of all stains, abiding forever as Brahman. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு அவதூத உபநிடதம் நிறைவுறுகிறது: இச்சத்தியத்தைத் தியானிப்பவன் சகல மாசுகளிலிருந்தும் விடுபட்டு, பிறவிப் பயனை அடைந்த கிருதகிருத்தியனாய் என்றென்றும் பிரம்மமாகவேத் திகழ்கிறான். ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Realize the Supreme Truth beyond bondage and liberation. Om Shanti.",
                "sound": "Krishna Yajur Veda Shanti Mantra 'Om Saha Navavatu' fading into serene mountain wind."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 15. KATHARUDRA (KATHASHRUTI) UPANISHAD (#83)
    {
        "story_id": "SANNYASA_15_KATHARUDRA",
        "muktika_number": 83,
        "name_sanskrit": "कठरुद्रोपनिषद् (कठश्रुत्युपनिषद्)",
        "name_iast": "Kaṭharudropaniṣad (Kaṭhaśrutyupaniṣad)",
        "name_tamil": "கடருத்ர (கடஸ்ருதி) உபநிடதம்",
        "name_english": "Katharudra (Kathashruti) Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "The Gods Seek the Secret of Rudra-Atman from Prajapati",
        "story_title_tamil": "பிரஜாபதியிடம் தேவர்கள் கேட்ட ருத்ர-ஆத்ம ஞானமும் சந்நியாச விதியும்",
        "characters": "The Devas (Celestial Seekers), Bhagavan Prajapati (The Creator & Teacher), A Father & His Awakened Son",
        "verse_sanskrit": "प्रज्ञानं ब्रह्म । अहं ब्रह्मास्मि । तत्त्वमसि । अयमात्मा ब्रह्म । सोऽयमात्मा चतुष्पात् जागरितस्थानो बहिःप्रज्ञः ॥",
        "verse_tamil_translit": "ப்ரக்ஞானம் ப்ரஹ்ம | அஹம் ப்ரஹ்மாஸ்மி | தத் த்வம் அஸி | அயமாத்மா ப்ரஹ்ம ||",
        "verse_meaning_english": "Consciousness is Brahman. I am Brahman. Thou art That. This Self is Brahman. This very Self has four quarters, unified in the supreme non-dual Witness.",
        "verse_meaning_tamil": "தூய உணர்வே பிரம்மம். நானே பிரம்மம். நீயே அது. இந்த ஆத்மாவே பிரம்மம். இந்த ஆத்மாவே நான்கு பாதங்களையும் கடந்து நிற்கும் ஏக சாட்சியாகும்.",
        "theme": "The touching rite of a seeker taking loving leave of family and Vedic fires (Kathashruti) coupled with Prajapati's revelation to the Devas that the illusory world-appearance vanishes upon realizing the non-dual Atman.",
        "SettingVisual": "Ancient Krishna Yajurvedic fire-altar pavilion at dawn, transitioning to Lord Prajapati's luminous mountain assembly",
        "ProtagonistVisual": "A middle-aged Vedic seeker bidding loving farewell to his young son, and the Devas bowing before Prajapati",
        "GuruVisual": "Bhagavan Prajapati radiating golden-white effulgence on a carved stone throne",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly-in across an ancient Vedic fire pavilion at sunrise where the Devas and rishis bow before Lord Prajapati.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot in an ancient Indian granite pavilion at golden dawn. Celestial sages and Devas bow with folded hands before radiant Lord Prajapati seated beside a sacred homa fire. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's Katharudra Upanishad, the gods and sages approached Lord Prajapati and asked: 'O Bhagavan! Explain to us the supreme rule of Sannyasa and the direct knowledge of the Self by which all sorrow ceases!'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் கடருத்ர உபநிடதத்தில், தேவர்களும் முனிவர்களும் பகவான் பிரஜாபதியை அணுகி வினவினர்: 'பகவானே! சகல துன்பங்களையும் போக்கும் ஆத்ம ஞானத்தையும் சந்நியாச தர்மத்தையும் எங்களுக்கு உபதேசித்தருளுங்கள்!'",
                "sub_cue": "The Devas ask Prajapati: 'Teach us the path of Sannyasa and the knowledge that ends all sorrow!'",
                "sound": "Crackling sacred fire, morning birdsong, and a deep Tanpura and Rudra Veena prelude."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Poignant medium shot of a father placing his hands in blessing upon his son's head as he prepares to renounce, while the son responds without grief.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps poignant medium shot in an ancient Indian courtyard at sunrise. A serene Vedic father in white cotton places his hands in blessing on the head of his young son, both smiling with spiritual peace and detachment without a single tear. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Prajapati first described the sacred farewell of the Kathashruti: gathering family and priests, the seeker declares to his son: 'You are Brahma, you are the sacrifice, you are the world!' And the wise son, understanding the truth, sheds no tears as they part in mutual blessing.",
                "vo_ta": "கடஸ்ருதியின் புனித விடைபெறுதலைப் பிரஜாபதி முதலில் விவரித்தார்: உறவினர்களையும் புரோகிதர்களையும் அழைத்து, தந்தை தன் மகனிடம் 'நீயே பிரம்மா, நீயே வேள்வி, நீயே உலகம்!' என வாழ்த்துகிறார். உண்மையை உணர்ந்த மகனும் கண்ணீர் சிந்தாமல் அமைதியுடன் தந்தையை வழியனுப்புகிறான்.",
                "sub_cue": "'You are Brahma, you are the sacrifice!' — The father and son part in luminous peace without tears.",
                "sound": "Warm, tender Carnatic violin solo in Raga Sahana."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Tracking shot of the seeker offering his wooden sacrificial spoons into the fire, sipping water in achamana, and walking into the forest.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps tracking shot of a newly initiated ancient Indian sannyasin walking barefoot away from a smoking homa altar into a sunlit forest grove, his face glowing with fearless serenity. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Consigning his wooden ritual vessels to the fire and offering fearlessness to every creature, the monk vows: 'Just as I do not fear any being, let no being fear me!' Living free of possessions, he meditates solely on the Supreme Self.",
                "vo_ta": "யாகப் பாத்திரங்களை அக்னியில் சமர்ப்பித்து, சகல உயிர்களுக்கும் அபயம் அளித்துத் துறவி புறப்படுகிறான். உடமைகள் ஏதுமின்றி, பரமாத்மாவை மட்டுமே தியானிப்பவனாக அவன் வனத்தில் சஞ்சரிக்கிறான்.",
                "sub_cue": "Offering fearlessness to all beings, the monk walks free into the forest of contemplation.",
                "sound": "Steady mridangam cadence and serene Bansuri flute."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Visual metaphor: bubbles and foam rising on the surface of a golden sunlit river and dissolving back into the same water.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps macro-to-wide shot of golden sunlit water bubbles and foam rising on a crystal river and dissolving seamlessly back into the current, while a sage meditates on the bank. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Prajapati imparted the Brahmavidya to the Devas: 'Just as foam and waves rise from water, shine as water, and dissolve back into water, this entire universe of Prana and elements is projected by Maya upon the one Atman and has no existence apart from It!'",
                "vo_ta": "அதன்பின் தேவர்களுக்கு பிரஜாபதி பிரம்மவித்தையை உபதேசித்தார்: 'நீரிலிருந்து எழும் நுரையும் அலையும் நீராகவே இருந்து நீரிலேயே மறைவது போல, பிராணனும் பஞ்ச பூதங்களும் கொண்ட இப்பிரபஞ்சம் ஆத்மாவின் மீது தோன்றும் மாயா விலாசமே அன்றி ஆத்மாவைத் தவிர வேறில்லை!'",
                "sub_cue": "As waves and foam are nothing but water, the cosmos is nothing but the One Atman.",
                "sound": "Flowing river sounds blending with shimmering Santoor arpeggios."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the meditating sage as the four Mahavakyas resonate and golden light unites the four quarters of consciousness.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of an illumined Indian sage in padmasana inside a sunlit granite mandapam; a radiant golden sphere of light glows in his heart, uniting the four states of consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Realizing the four great declarations—Prajnanam Brahma, Aham Brahmasmi, Tat Tvam Asi, Ayam Atma Brahma—the yogi merges the waking Visva into Taijasa, Taijasa into Prajna, and Prajna into the spotless fourth state, Turiya, the Rudra-Atman who destroys all ignorance!",
                "vo_ta": "'பிரக்ஞானம் பிரம்ம, அஹம் பிரம்மாஸ்மி, தத் த்வம் அஸி, அயமாத்மா பிரம்ம' எனும் நான்கு மகாவாக்கியங்களின் பொருளை உணர்ந்து, விஸ்வன், தைஜசன், பிராஞன் ஆகிய மூன்றையும் கடந்து, அறியாமையை அழிக்கும் துரிய ருத்ர-ஆத்மாவில் யோகி நிலைபெறுகிறான்!",
                "sub_cue": "प्रज्ञानं ब्रह्म । अहं ब्रह्मास्मि । तत्त्वमसि । अयमात्मा ब्रह्म — The Four Mahavakyas converge in Turiya!",
                "sound": "Majestic four-part Vedic choral chant of the four Mahavakyas with conch and temple bells."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the Devas and the awakened sage shining in one seamless golden light of Satchidananda.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Lord Prajapati and the meditating sages bathed in a unified field of golden dawn light in the ancient pavilion, radiating Satchidananda. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In that non-dual vision, the knot of the heart is cleft asunder, all doubts are dispelled, and the sage abides as the self-effulgent Witness—secondless, blissful, and immortal.",
                "vo_ta": "அந்த அத்வைத தரிசனத்தில் இதய முடிச்சு அவிழ்கிறது; சகல ஐயங்களும் நீங்குகின்றன; இரண்டற்ற சச்சிதானந்த சுயம்பிரகாச சாட்சியாக முனிவர் அமரத்துவம் பெறுகிறார்.",
                "sub_cue": "The knot of the heart is untied; all doubts vanish in the self-effulgent Witness.",
                "sound": "Soaring Saraswati Veena and Bansuri duet in Raga Hamsadhwani."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the sunlit forest and granite pavilion.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian granite pavilion and green forest valley at sunrise, glowing with golden peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Katharudra Upanishad: behold the waves of life without forgetting the boundless ocean of Consciousness that you are. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு கடருத்ர உபநிடதம் நிறைவுறுகிறது: வாழ்க்கை எனும் அலைகளைக் காணும்போதும், நாம் எல்லையற்ற உணர்வுப் பெருங்கடலே என்பதை மறவாதிருப்போமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Behold the waves of life while abiding as the Ocean of Consciousness. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into peaceful morning air."
            }
        ]
    },
    # 16. YAJNAVALKYA UPANISHAD (#97)
    {
        "story_id": "SANNYASA_16_YAJNAVALKYA",
        "muktika_number": 97,
        "name_sanskrit": "याज्ञवल्क्योपनिषद्",
        "name_iast": "Yājñavalkyopaniṣad",
        "name_tamil": "யாக்ஞவல்கிய உபநிடதம்",
        "name_english": "Yajnavalkya Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "Conquering the Demon of Craving (Trishna): Yajnavalkya, Janaka & Priyavrata",
        "story_title_tamil": "तृष्णा எனும் ஆசைப் பேயை வெல்லும் வழி: யாக்ஞவல்கியர், ஜனகர் மற்றும் பிரியவிரதன்",
        "characters": "Maharishi Yajnavalkya (The Lion of Vedanta), King Janaka of Videha, Priyavrata (Disciple Who Questions about Equanimity)",
        "verse_sanskrit": "सर्वं खल्विदं ब्रह्म तज्जलानिति शान्त उपासीत । तृष्णां छिन्धि भज क्षान्तिं जहि मानंजरामयम् ॥",
        "verse_tamil_translit": "ஸர்வம் கல்விதம் ப்ரஹ்ம தஜ்ஜலானிதி ஷாந்த உபாஸீத | த்ருஷ்ணாம் சின்தி பஜ க்ஷாந்திம் ஜஹி மானம் ஜராமயம் ||",
        "verse_meaning_english": "All this universe is indeed Brahman; from That it is born, into That it dissolves, and in That it breathes—thus meditate in utter peace! Sever the creeper of craving (Trishna), embrace forgiveness, and cast off pride!",
        "verse_meaning_tamil": "இப் பிரபஞ்சம் அனைத்துமே பிரம்மம்; அதிலிருந்தே தோன்றி, அதிலேயே ஒடுங்கி, அதனாலேயே உயிர்க்கிறது—என அமைதியாகத் தியானிப்பாயாக! ஆசைக் கொடியை (த்ருஷ்ணா) அறுத்தெறிந்து, பொறுமையை மேற்கொண்டு, ஆணவத்தைக் கைவிடுவாயாக!",
        "theme": "After revealing the rules of Sannyasa to Janaka, Yajnavalkya answers Priyavrata on how to conquer the witch of Craving (Trishna)—which grows youthful even when the body grows old—and how the sage sleeps comfortably even in the battle of life.",
        "SettingVisual": "Grand Videha royal-philosophical courtyard and quiet river hermitage under golden sunrise light",
        "ProtagonistVisual": "King Janaka and ascetic disciple Priyavrata bowing before Maharishi Yajnavalkya",
        "GuruVisual": "Maharishi Yajnavalkya with luminous white beard, rudraksha, and fearless lion-like presence",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide crane shot of the Videha assembly hall opening onto a sacred river garden at dawn, where King Janaka and Priyavrata bow before Maharishi Yajnavalkya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an ancient Indian carved stone pavilion overlooking a river garden at sunrise. King Janaka and ascetic Priyavrata bow with folded hands before venerable Maharishi Yajnavalkya. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Shukla Yajur Veda's Yajnavalkya Upanishad, after King Janaka learned the sacred law of renunciation, the seeker Priyavrata stepped forward and asked Maharishi Yajnavalkya: 'O Bhagavan! Even when a man renounces outer possessions, how does he conquer the restless demon of inner craving, and how does he abide in unshakeable peace?'",
                "vo_ta": "சுக்ல யஜுர் வேதத்தின் யாக்ஞவல்கிய உபநிடதத்தில், மன்னன் ஜனகருக்குத் துறவு விதியை அருளிய பின், சீடர் பிரியவிரதன் முன்வந்து கேட்டார்: 'பகவானே! புறப் பொருட்களைத் துறந்த பின்பும், உள்ளே அலைபாயும் ஆசை எனும் பேயை வெல்வது எவ்வாறு? அசைக்க முடியாத அமைதியில் நிலைத்திருப்பது எப்படி?'",
                "sub_cue": "Priyavrata asks Yajnavalkya: 'How does one conquer the restless demon of inner craving?'",
                "sound": "Resonant temple gong, morning river breeze, and a majestic Rudra Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of an elderly worldly man clutching a golden vessel with trembling hands, contrasted with Yajnavalkya's serene, open-palmed fearlessness.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Maharishi Yajnavalkya's serene, open hands in abhaya mudra bathed in golden morning light, contrasting with dry twisted vines on a stone wall symbolizing worldly craving. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Yajnavalkya exposed the anatomy of Trishna—worldly craving: 'Look at this sorceress called Craving! The hair turns white, the teeth fall out, the limbs tremble with old age—yet Trishna alone remains ever young! Running faster than the wind across a hundred leagues in a wink, she binds even scholars unless severed by the sword of Self-Knowledge!'",
                "vo_ta": "'த்ருஷ்ணா' எனும் பேராசையின் இயல்பை யாக்ஞவல்கியர் தோலுரித்துக் காட்டினார்: 'தலைமுடி நரைக்கிறது, பற்கள் விழுகின்றன, உடல் முதுமையால் நடுங்குகிறது—ஆனால் ஆசை மட்டும் என்றும் இளமையாகவேத் துள்ளுகிறது! கண்ணிமைக்கும் நேரத்தில் நூறு யோஜனை தூரம் பாயும் இந்த ஆசைப் பேயை ஆத்ம ஞான வாளால் மட்டுமே வெட்ட முடியும்!'",
                "sub_cue": "The body grows old, yet Craving (Trishna) remains ever young—sever it with the sword of Wisdom!",
                "sound": "Dramatic Pakhawaj roll and urgent Sarangi phrases resolving into calm Veena chords."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of a false ascetic glancing angrily at someone while counting rudraksha beads, contrasted with a true Paramahamsa smiling in utter inward peace.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a true Paramahamsa sage seated calmly under a banyan tree at sunrise, his face glowing with genuine forgiveness and inward peace, free of hypocrisy. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Yajnavalkya warned against outward show: 'He whose fingers roll rudraksha beads while his heart boils with anger and greed is like a vessel copper-plated outside but rusty within! Only he who sees another's gold as a worthless pebble and guards his mind in forgiveness is a true Yati!'",
                "vo_ta": "போலி வேடத்தைக் குறித்து யாக்ஞவல்கியர் எச்சரித்தார்: 'கையில் ஜபமாலையை உருட்டிக்கொண்டு உள்ளத்தில் சினமும் பேராசையும் கொண்டவன், வெளியே செம்பு பூசிய களிமண் பாத்திரம் போன்றவன்! பிறர் பொன்னைக் கூழாங்கல்லாகக் கண்டு, பொறுமையில் நிலைத்திருப்பவனே உண்மையான யதி!'",
                "sub_cue": "Not rolling beads with a greedy heart, but seeing gold as a pebble makes a true Yati.",
                "sound": "Clear, purifying Bansuri melody in Raga Shuddha Saveri."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Striking visual metaphor: a serene yogi resting in deep peace even as storm winds blow and chariots pass in the distance.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of a serene ancient Indian yogi seated in unshakeable meditation on a granite hillock while dramatic wind sweeps through the trees around him, golden sunlight illuminating his calm face. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "How fearless is the knower of the Self! Even if the sky falls, even amidst flying arrows on a battlefield, or inside a blazing fire, the sage whose mind has dissolved in Brahman rests as peacefully as a child in its mother's lap—for he knows the Witness can never be wounded or burned!",
                "vo_ta": "ஆத்ம ஞானியின் அச்சமின்மை எத்தகையது! வானமே இடிந்து விழுந்தாலும், போர்க்களத்து அம்புகளுக்கு நடுவிலும், கொழுந்துவிட்டெரியும் நெருப்பிலும் பிரம்மத்தில் மனம் கரைந்த ஞானி தாயின் மடியில் உறங்கும் குழந்தையைப் போல் அமைதியாக இருக்கிறார்—ஏனெனில் ஆத்மாவை எதுவும் காயப்படுத்த முடியாது என்பதை அவர் அறிவார்!",
                "sub_cue": "Even amidst a storm or battlefield, the Knower of Atman rests in unshakeable peace.",
                "sound": "Swirling wind sound effects giving way to an unshakeable, crystalline Tanpura and Veena drone."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Slow zoom into Yajnavalkya's radiant eyes as golden light connects every leaf, river wave, and seeker in the pavilion.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Maharishi Yajnavalkya in luminous contemplation, golden threads of light radiating from his heart and uniting King Janaka, Priyavrata, and the surrounding nature. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Yajnavalkya imparted the supreme Upasana: 'Sarvam khalvidam Brahma, tajjalan iti shanta upasita—all this universe is verily Brahman; from That it arises, into That it dissolves, and in That it breathes! Knowing this, sever craving, embrace patience, and abide in Supreme Peace!'",
                "vo_ta": "அப்போது யாக்ஞவல்கியர் பரம உபாசனையை அருளினார்: 'ஸர்வம் கல்விதம் ப்ரஹ்ம தஜ்ஜலானிதி ஷாந்த உபாஸீத — இப் பிரபஞ்சம் அனைத்துமே பிரம்மம்; அதிலிருந்தே தோன்றி, அதிலேயே ஒடுங்கி, அதனாலேயே உயிர்க்கிறது! இதை உணர்ந்து ஆசையை அறுத்துப் பேரமைதியில் திளைப்பாயாக!'",
                "sub_cue": "सर्वं खल्विदं ब्रह्म तज्जलानिति शान्त उपासीत — All this is Brahman; meditate in utter peace!",
                "sound": "Majestic choral Vedic chant of 'Sarvam Khalvidam Brahma' with temple bells."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Janaka and Priyavrata in deep samadhi before Yajnavalkya as the morning sun rises over the Videha river.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Maharishi Yajnavalkya, King Janaka, and Priyavrata seated in silent samadhi in the sunlit stone pavilion overlooking the river at dawn. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "With the creeper of Trishna severed at its root, the mind becomes cool, luminous, and still like an ocean without waves, shining as the immortal Self.",
                "vo_ta": "ஆசைக் கொடி வேரோடு அறுபட்டதும், மனம் அலையில்லாப் பெருங்கடல் போல் குளிர்ந்து, தெளிந்து, அமரத்துவமான ஆத்மாவாகப் பிரகாசிக்கிறது.",
                "sub_cue": "With Craving severed at its root, the mind shines like a waveless ocean of Bliss.",
                "sound": "Tranquil Santoor and Bansuri harmony."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the sunlit river garden and pavilion.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Videha river pavilion bathed in golden sunrise light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Yajnavalkya Upanishad: conquer the aging-proof demon of greed with the eternal youth of Self-Knowledge, and rest in fearless peace. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு யாக்ஞவல்கிய உபநிடதம் நிறைவுறுகிறது: மூப்படையாத பேராசையை ஆத்ம ஞானத்தால் வென்று, அச்சமற்ற பேரமைதியில் நிலைபெறுவோமாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Conquer Craving with Self-Knowledge; rest in fearless peace. Om Shanti.",
                "sound": "Shanti Mantra 'Om Purnamadah' fading into gentle river breeze."
            }
        ]
    },
    # 17. VARAHA UPANISHAD (#98)
    {
        "story_id": "SANNYASA_17_VARAHA",
        "muktika_number": 98,
        "name_sanskrit": "वराहोपनिषद्",
        "name_iast": "Varāhopaniṣad",
        "name_tamil": "வராக உபநிடதம்",
        "name_english": "Varaha Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "Lord Varaha's 96 Tattvas & Ribhu's Awakening of Nidagha into Jivanmukti",
        "story_title_tamil": "பகவான் வராகமூர்த்தியின் உபதேசமும் ரிபு-நிதாகர் ஜீவன்முக்திச் சரிதமும்",
        "characters": "Lord Adi-Varaha (The Boar Incarnation of Vishnu), Maharishi Ribhu (Illumined Sage), Nidagha (Disciple Tested in the Royal Procession)",
        "verse_sanskrit": "अहमेव परं ब्रह्म வாसुदेवाख्यमव्ययम् । जीवन्मुक्तः सदा स्वच्छो नित्यतृप्तो निरञ्जनः ॥",
        "verse_tamil_translit": "அஹமேவ பரம் ப்ரஹ்ம வாஸுதேவாக்யமவ்யயம் | ஜீவன்முக்த: ஸதா ஸ்வச்சோ நித்யத்ருப்தோ நிரஞ்ஜன: ||",
        "verse_meaning_english": "'I alone am the Supreme Imperishable Brahman known as Vasudeva!' The Jivanmukta is ever pure, eternally contented, and spotless amidst all existence.",
        "verse_meaning_tamil": "'வாசுதேவன் எனப்படும் அழிவற்ற பரப்பிரம்மம் நானே!' ஜீவன்முக்தன் எப்போதும் தூயவனாய், நித்திய திருப்தியாளனாய், களங்கமற்றவனாய்த் திகழ்கிறான்.",
        "theme": "After meditating for twelve years, Sage Ribhu receives from Lord Varaha the science of the 96 Tattvas, the seven Bhumikas (stages of wisdom), the characteristics of the Jivanmukta, and tests his disciple Nidagha riding on a royal elephant.",
        "SettingVisual": "Sacred mountain cave glowing with golden Vishnu-Varaha radiance, transitioning to an ancient South Indian temple town procession and forest ashram",
        "ProtagonistVisual": "Maharishi Ribhu in deep tapasya, and his disciple Nidagha carrying firewood on the outskirts of a festive ancient city",
        "GuruVisual": "Lord Adi-Varaha shining with cosmic golden-sapphire light, and Maharishi Ribhu disguised as a humble village rustic",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic slow push-in inside a sunlit mountain cave where Maharishi Ribhu completes twelve years of penance and beholds the radiant form of Lord Varaha.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps majestic cinematic shot inside a sacred Indian mountain cave at dawn. Maharishi Ribhu kneels in awe with folded hands before the divine golden-blue effulgence of Lord Adi-Varaha. Warm celestial light fills the stone cavern. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "After performing austere penance for twelve celestial years, the great Sage Ribhu beheld Lord Adi-Varaha shining in cosmic splendor. When the Lord asked him to choose a boon, Ribhu rejected all worldly and heavenly wealth, asking: 'O Bhagavan! Teach me that supreme Brahmavidya which grants direct Jivanmukti!'",
                "vo_ta": "பன்னிரண்டு தேவ ஆண்டுகள் கடும் தவம் புரிந்த ரிபு மகரிஷியின் முன், ஆதிவராகப் பெருமான் திவ்ய தேஜஸுடன் தோன்றினார். வரம் கேட்கும்படி பகவான் பணிக்க, உலக போகங்கள் அனைத்தையும் உதறிய ரிபு, 'பகவானே! ஜீவன்முக்தியை நல்கும் பரம பிரம்மவித்தையை எனக்கு உபதேசித்தருளுங்கள்!' என்று வேண்டினார்.",
                "sub_cue": "Rejecting all worldly boons, Sage Ribhu asks Lord Varaha for the supreme science of Jivanmukti.",
                "sound": "Deep cosmic Shankha blast, temple bell resonance, and a majestic Rudra Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Cinematic visualization of the ninety-six Tattvas (elements, pranas, nadis, gunas) revolving like a cosmic wheel around the meditating sage, while the center remains still.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of Maharishi Ribhu meditating in lotus posture surrounded by subtle golden geometric rings of prana light representing the ninety-six tattvas, while his heart center shines in motionless peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Varaha first expounded the ninety-six Tattvas that constitute the phenomenal body and universe—the senses, vital airs, channels, gunas, and modifications. 'Only when the seeker discerns the changeless Witness distinct from all ninety-six Tattvas does he enter the portal of liberation!'",
                "vo_ta": "பகவான் வராகமூர்த்தி முதலில் உடலையும் பிரபஞ்சத்தையும் உருவாக்கும் தொண்ணூற்றாறு தத்துவங்களை விளக்கினார்: 'பஞ்ச பூதங்கள், பிராணன்கள், நாடிகள், முக்குணங்கள் ஆகிய தொண்ணூற்றாறு தத்துவங்களுக்கும் மேலான மாறாத சாட்சியைத் பிரித்தறியும் போதே சாதகன் முக்தி வாசலில் நுழைகிறான்!'",
                "sub_cue": "Discerning the changeless Witness beyond all 96 Tattvas opens the portal of Liberation.",
                "sound": "Rhythmic mridangam cycle in Adi Tala with an intricate Saraswati Veena melody."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Dramatic scene on the outskirts of an ancient temple city: Nidagha stands aside as a decorated royal elephant passes, and Ribhu (disguised as a rustic) questions him.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot on the outskirts of an ancient Indian stone city at golden morning. Young ascetic Nidagha holding a bundle of kusha grass speaks to elderly sage Ribhu disguised as a simple villager, while a caparisoned royal elephant passes in the sunlit distance. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "To illustrate this non-dual wisdom, Ribhu later visited his ritual-minded disciple Nidagha in disguise as a village rustic. When Nidagha pointed out the King riding atop a royal elephant, Ribhu leaped onto Nidagha's shoulders and asked: 'Tell me, O Brahmin—which of us is the King on top, and which is the elephant below? What do above and below mean in the One Indivisible Atman?'",
                "vo_ta": "இந்த அத்வைத ஞானத்தை உணர்த்த, ரிபு மகரிஷி ஒரு கிராமவாசி வேடத்தில் தன் சீடர் நிதாகரைச் சந்தித்தார். பட்டத்து யானை மேல் மன்னன் வருவதை நிதாகர் சுட்டிக்காட்ட, ரிபு உடனே நிதாகரின் தோள் மீது ஏறி அமர்ந்து, 'சொல் நிதாகா! நம் இருவரில் மேலே இருக்கும் மன்னன் யார்? கீழே இருக்கும் யானை யார்? எங்கும் நிறைந்த ஏக ஆத்மாவில் மேலும் கீழும் ஏது?' என்று கேட்டார்!",
                "sub_cue": "Ribhu asks Nidagha: 'In the One Indivisible Atman, who is the King above and who is the elephant below?'",
                "sound": "Distant festive temple drums fading into a sudden, piercing Bansuri note of awakening."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Seven ascending golden lotus steps (Sapta Jnana Bhumikas) glowing along a mountain pathway as the yogi practices Laya, Mantra, Hatha, and Raja Yoga.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of seven glowing golden stone steps ascending a Himalayan shrine at sunrise, as a serene Indian yogi sits at the summit in padmasana practicing deep pranayama and dhyana. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Varaha revealed the Seven Stages of Wisdom—Shubheccha, Vicharana, Tanumanasa, Sattvapatti, Asamsakti, Padarthabhavana, and Turiya—united with the fourfold Yoga and the eleven limbs of kundalini mastery! Like a salt doll diving into the ocean, the yogi's mind dissolves completely into Consciousness.",
                "vo_ta": "சுபேச்சை, விசாரணா, தனுமானஸா, சத்வாபத்தி, அஸம்ஸக்தி, பதார்த்தபாவனா, துரியகா எனும் ஏழு ஞான பூமிகளையும், அஷ்டாங்க யோக இரகசியங்களையும் வராகப் பெருமான் அருளினார்! கடலில் குதித்த உப்புப் பொம்மை கரைவது போல, யோகியின் மனம் சைதன்யப் பெருங்கடலில் முழுமையாகக் கரைகிறது.",
                "sub_cue": "Ascending the Seven Jnana-Bhumikas, the mind dissolves like a salt doll in the ocean of Brahman.",
                "sound": "Ascending seven-note raga progression on Veena and Flute."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Close-up of Nidagha bowing at Ribhu's feet in tears of joy as he abandons dualistic ritualism for pure Advaita.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps emotional close-up of disciple Nidagha bowing with tears of spiritual joy at the feet of Maharishi Ribhu under a sunlit banyan tree, a warm golden aura of realization enveloping both Guru and disciple. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Recognizing his Guru Ribhu by that fearless teaching, Nidagha fell at his feet! Lord Varaha proclaimed the summit of realization: 'Ahameva Param Brahma Vasudevakhyam avyayam—I alone am the Supreme Imperishable Brahman known as Vasudeva! For one who knows this, the entire world is Chinmatra—Pure Consciousness alone!'",
                "vo_ta": "அந்த அद्वैत வாக்கால் தன் குருவான ரிபுவை அடையாளம் கண்ட நிதாகர், அவர் பாதங்களில் வீழ்ந்து வணங்கினார்! வராகப் பெருமான் முழங்குகிறார்: 'அஹமேவ பரம் ப்ரஹ்ம வாஸுதேவாக்யமவ்யயம் — வாசுதேவன் எனப்படும் அழிவற்ற பரப்பிரம்மம் நானே! இவ்வுலகம் சின்மாத்திரம்—தூய உணர்வு மட்டுமே!'",
                "sub_cue": "अहमेव परं ब्रह्म वासुदेवाख्यमव्ययम् — I alone am the Imperishable Brahman, Vasudeva!",
                "sound": "Triumphant Shankha and Vedic chorus chanting 'Ahameva Param Brahma'."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Ribhu and Nidagha seated in Jivanmukti bliss, serene like the sky while golden light bathes the forest.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Maharishi Ribhu and Nidagha seated side by side in luminous samadhi in a sunlit forest clearing, radiating eternal contentment and peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Behold the Jivanmukta: even while acting in the world, he neither rejoices in pleasure nor grieves in pain; ever pure, eternally contented, he shines like the boundless sky untouched by passing clouds.",
                "vo_ta": "ஜீவன்முக்தரின் நிலையைக் காணீர்: உலகில் செயல்பட்டாலும் இன்பத்தில் மகிழ்வதுமில்லை, துன்பத்தில் துவள்வதுமில்லை; மேகங்களால் தீண்டப்படாத ஆகாயத்தைப் போல் நித்திய திருப்தியாளனாய் அவர் பிரகாசிக்கிறார்.",
                "sub_cue": "Ever pure, eternally contented, the Jivanmukta shines untouched like the boundless sky.",
                "sound": "Serene Carnatic violin and Tanpura in Raga Nilambari."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow pull-back from the mountain cave and forest into the golden sunrise sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the sacred mountain cave and forest hermitage bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Varaha Upanishad: transcend the illusion of high and low, and behold the One Vasudeva shining in every heart. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு வராக உபநிடதம் நிறைவுறுகிறது: உயர்வு-தாழ்வு எனும் மாயையைக் கடந்து, ஒவ்வொரு இதயத்திலும் ஒளிரும் ஏக வாசுதேவனைத் தரிசிப்போமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Transcend high and low; behold the One Vasudeva in every heart. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into peaceful morning resonance."
            }
        ]
    },
    # 18. SHATYAYANIYA UPANISHAD (#99)
    {
        "story_id": "SANNYASA_18_SHATYAYANIYA",
        "muktika_number": 99,
        "name_sanskrit": "शाट्यायनीयोपनिषद्",
        "name_iast": "Śāṭyāyanīyopaniṣad",
        "name_tamil": "சாட்யாயனீய உபநிடதம்",
        "name_english": "Shatyayaniya Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Sannyasa",
        "story_title_english": "The Fivefold Banner of Vishnu & The Mind as Cause of Bondage and Liberation",
        "story_title_tamil": "விஷ்ணுவின் பஞ்ச அங்கங்களும் மனமே பந்த-மோட்ச காரணம் என்பதும்: சாட்யாயனீய உபநிடதம்",
        "characters": "The Assembly of Shukla Yajurvedic Sages of the Shatyayana Shakha, The Vaishnava Paramahamsa Acharya",
        "verse_sanskrit": "मन एव मनुष्याणां कारणं बन्धमोक्षयोः । बन्धाय विषयासक्तं मुक्त्यै निर्विषयं स्मृतम् ॥",
        "verse_tamil_translit": "மன ஏவ மனுஷ்யாணாம் காரணம் பந்தமோக்ஷயோ: | பந்தாய விஷயாஸக்தம் முக்த்யை நிர்விஷயம் ஸ்ம்ருதம் ||",
        "verse_meaning_english": "The mind alone is the cause of bondage and liberation for human beings! Attached to sense-objects, it leads to bondage; freed from sense-objects, it leads to liberation!",
        "verse_meaning_tamil": "மனிதர்களுக்குப் பந்தத்திற்கும் முக்திக்கும் மனமே ஒரே காரணம்! புலன் நுகர்ச்சிகளில் பற்று வைக்கும்போது அது பந்தத்திற்கும், புலன் ஆசைகளிலிருந்து விடுபடும்போது அது முக்திக்கும் இட்டுச் செல்கிறது!",
        "theme": "The mind as the sole pivot of bondage and freedom, the sacred five emblems of the Vaishnava Sannyasin (triple staff, sacred thread, loincloth, sling, and water-pot as the five fierce forms of Vishnu), and how a single realized Sannyasin redeems sixty generations of ancestors.",
        "SettingVisual": "Ancient South Indian granite temple mandapam and Kaveri river ghat at golden sunrise, with sacred Tulasi and Peepal trees",
        "ProtagonistVisual": "Devoted Shukla Yajurvedic seekers and a serene Paramahamsa monk holding the sacred Tridanda",
        "GuruVisual": "Venerable Shatyayaniya Acharya seated on a carved stone dais beside a glowing brass lamp",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly shot along a sunlit South Indian granite mandapam beside the Kaveri river, where seekers bow before the Shatyayaniya Acharya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot in an ancient South Indian carved granite mandapam beside the Kaveri river at golden dawn. Vedic seekers bow with folded hands before a venerable Acharya seated beside a glowing brass oil lamp. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "By the sacred waters of the Kaveri, the Shukla Yajur Veda's Shatyayaniya Upanishad opens with the timeless psychological truth of Vedanta. The seekers asked the Master: 'O Bhagavan! What binds the immortal soul to samsara, and what is the unfailing key to its liberation?'",
                "vo_ta": "புனித காவிரிக் கரையில், சுக்ல யஜுர் வேதத்தின் சாட்யாயனீய உபநிடதம் வேதாந்தத்தின் உளவியல் பேருண்மையோடு தொடங்குகிறது. சீடர்கள் ஆச்சாரியரிடம் கேட்டனர்: 'பகவானே! அமரத்துவமான ஆத்மாவைச் சம்சாரத்தில் பிணிப்பது எது? அதனை விடுவிக்கும் திறவுகோல் யாது?'",
                "sub_cue": "What binds the immortal soul to samsara, and what is the key to its liberation?",
                "sound": "Gentle Kaveri river flow, temple bell chime, and a resonant Saraswati Veena prelude."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of a brass key turning an ancient iron lock both ways—locking and unlocking—dissolving to the Acharya pointing to the heart-mind.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of the venerable Acharya in the sunlit granite mandapam touching his heart and forehead as he teaches the secret of the mind to his attentive disciples. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Acharya proclaimed the immortal verse: 'Mana eva manushyanam karanam bandha-mokshayoh—the mind alone is the cause of both bondage and liberation for mankind! When stained with attachment to sense-objects, the mind is bondage; when emptied of sense-craving, that very mind becomes liberation!'",
                "vo_ta": "ஆச்சாரியர் அழியா சுலோகத்தை முழங்கினார்: 'மன ஏவ மனுஷ்யாணாம் காரணம் பந்தமோக்ஷயோ: — மனிதர்களுக்குப் பந்தத்திற்கும் முக்திக்கும் மனமே காரணம்! புலன் நுகர்ச்சிகளில் பற்று வைக்கும்போது அது பந்தமாகிறது; விடய வாசனையிலிருந்து விடுபடும்போது அதே மனம் முக்தியாகிறது!'",
                "sub_cue": "मन एव मनुष्याणां कारणं बन्धमोक्षयोः — The mind alone is the cause of bondage and liberation!",
                "sound": "Clear, memorable Bansuri motif in Raga Mohanam accompanied by soft mridangam."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of a Vaishnava Sannyasin holding the triple bamboo staff (Tridanda), kamandalu, and patched robe, glowing with golden light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a serene ancient Indian Vaishnava sannyasin standing on stone river steps at sunrise, holding a triple bamboo staff (tridanda) and gourd water-pot, bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Entering the order of Sannyasa, the monk carries the five sacred emblems as the very limbs of Lord Vishnu—the triple staff, the sacred thread, the loincloth, the sling, and the water-pot—guarding speech, mind, and body while meditating ceaselessly on Vasudeva.",
                "vo_ta": "சந்நியாச தர்மத்தில் புகும் துறவி, முக்கோல், பூணூல், கௌபீனம், உறிகயிறு, கமண்டலம் ஆகிய ஐந்து அங்கங்களையும் சாட்சாத் மகாவிஷ்ணுவின் வடிவமாகத் தரித்து, மனம்-மொழி-மெய்களை அடக்கி வாசுதேவனை இடைவிடாது தியானிக்கிறார்.",
                "sub_cue": "Guarding speech, mind, and body, the monk meditates ceaselessly on Lord Vasudeva.",
                "sound": "Devotional Tambura and Violin melody in Raga Harikambhoji."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Cinematic contrast: a warrior dying nobly on a battlefield vs. a Sannyasin steadfastly conquering the six inner enemies (lust, anger, greed, delusion, pride, envy) until his final breath.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a steadfast Indian ascetic meditating fearlessly under a banyan tree at dawn, surrounded by a protective golden aura that repels dark shadows of anger and greed. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Look at the heroism of the true monk: just as a valiant warrior never turns his back on the battlefield, the Sannyasin never retreats to worldly cravings! Conquering the six inner enemies—lust, anger, greed, delusion, arrogance, and envy—he views gold and stone, praise and blame, friend and foe with utter equality.",
                "vo_ta": "உண்மையான துறவியின் வீரத்தைக் காணீர்: போர்க்களத்தில் புறமுதுகிடாத மாவீரனைப் போல, சந்நியாசி ஒருபோதும் உலக ஆசைகளுக்குத் திரும்புவதில்லை! காமம், குரோதம், லோபம், மோகம், மதம், மாச்சரியம் எனும் ஆறு உட்பகைவர்களையும் வென்று, பொன்னையும் கல்லையும் சமமாகக் காண்கிறான்.",
                "sub_cue": "Like a fearless warrior who never retreats, the monk conquers the six inner enemies.",
                "sound": "Heroic Pakhawaj rhythm resolving into serene Veena harmonics."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Majestic upward tilt from the meditating Sannyasin toward the golden morning sky, where sixty luminous ancestral stars shine with joy.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps majestic upward tilt shot of an illumined Indian sannyasin meditating by the river at dawn while golden rays of light rise from his heart into the morning sky, blessing generations past and future. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then the Upanishad proclaims the glorious fruit of renunciation: 'The very moment a pure soul embraces true Sannyasa and realizes the Self, sixty generations of his ancestors before him and sixty generations after him are uplifted from darkness into the world of Brahman!'",
                "vo_ta": "துறவின் மகிமையை உபநிடதம் முழங்குகிறது: 'தூய ஆத்மா ஒருவன் உண்மையான சந்நியாசத்தை மேற்கொண்டு ஆத்மாவை உணரும் அக்கணமே, அவனுக்கு முன் சென்ற அறுபது தலைமுறை முன்னோர்களும் பின் வரும் சந்ததியினரும் பிறவி இருளிலிருந்து பிரம்மலோகத்திற்கு உயர்த்தப்படுகின்றனர்!'",
                "sub_cue": "A single realized Sannyasin uplifts sixty generations of ancestors into the light of Brahman!",
                "sound": "Soaring Shankha and celestial Vedic chorus."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the Sannyasin seated in nirvikalpa samadhi beside the Kaveri river, his mind completely still and luminous.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the illumined sannyasin seated in lotus posture on the Kaveri river ghat at sunrise, the water reflecting his golden aura in mirror stillness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Abiding in the secret cave of the heart, he realizes the Supreme Vishnu—spotless, partless, and all-pervading—and never returns to the whirlpool of birth and death.",
                "vo_ta": "இதயக் குகையில் உறையும் களங்கமற்ற, எங்கும் நிறைந்த பரம விஷ்ணுவைத் தன்னுள்ளேயே உணர்ந்து, பிறப்பு-இறப்புச் சுழலுக்கு அவர் மீண்டும் திரும்புவதில்லை.",
                "sub_cue": "Realizing the all-pervading Supreme within the heart, the Sage never returns to samsara.",
                "sound": "Peaceful Bansuri and Saraswati Veena duet."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the South Indian granite mandapam and Kaveri river at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient granite temple mandapam and golden Kaveri river at sunrise. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Shatyayaniya Upanishad: turn the key of your own mind away from fleeting cravings toward the Eternal Self, and unlock boundless freedom. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு சாட்யாயனீய உபநிடதம் நிறைவுறுகிறது: நம் மனம் எனும் திறவுகோலை அற்ப ஆசைகளிலிருந்து திருப்பி நித்திய ஆத்மாவை நோக்கித் திறந்து, எல்லையற்ற விடுதலையைப் பெறுவோமாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Turn the key of the mind from craving to Consciousness; unlock eternal freedom. Om Shanti.",
                "sound": "Shanti Mantra 'Om Purnamadah' fading into Kaveri river waves."
            }
        ]
    },
    # 19. LAGHU-SANNYASA (KUNDALIKA / ARUNEYA-SANNYASA) UPANISHAD (#16 / #65A)
    {
        "story_id": "SANNYASA_19_LAGHU_SANNYASA",
        "muktika_number": 65,
        "name_sanskrit": "लघुसंन्यासोपनिषद् (संन्यासोपनिषद् - सामवेद)",
        "name_iast": "Laghusaṃnyāsopaniṣad",
        "name_tamil": "லகு சந்நியாச உபநிடதம்",
        "name_english": "Laghu-Sannyasa Upanishad",
        "veda": "Sama Veda",
        "category": "Sannyasa",
        "story_title_english": "The Final Fire-Oblation of the Householder & The Ascetic's Inner Altar",
        "story_title_tamil": "இல்லறத்தானின் இறுதி அக்னி ஆஹுதியும் துறவியின் அக வேள்வியும்: லகு சந்நியாச உபநிடதம்",
        "characters": "The Virtuous Vedic Householder, The Circle of Sacrificial Priests, The Awakened Forest Sannyasin",
        "verse_sanskrit": "प्राणापानव्यानोदानसमाना मे शुध्यन्तां ज्योतिरमृतं विरजं விपाप्म ब्रह्म भूयासमिति । सशिखान् केशान् निकृत्य यज्ञोपवीतं विसृज्य आत्मनि संन्यसेत् ॥",
        "verse_tamil_translit": "ப்ராணாபானவ்யானோதானஸமானா மே ஷுத்யந்தாம் ஜ்யோதிரம்ருதம் விரஜம் விபாப்ம ப்ரஹ்ம பூயாஸமிதி ||",
        "verse_meaning_english": "'May my five vital airs—Prana, Apana, Vyana, Udana, and Samana—be purified! May I become the Immortal Light, spotless, sinless Brahman!' Shaving the hair with the tuft and casting away the sacred thread, let him repose solely in the Self!",
        "verse_meaning_tamil": "'எனது பிராணன், அபானன், வியானன், உதானன், சமானன் ஆகிய பஞ்ச பிராணன்களும் தூய்மையடையட்டும்! களங்கமற்ற, பாவமற்ற அமிர்த ஜோதியான பிரம்மமாக நான் ஆவேனாக!' குடுமியுடன் முடியை மழித்துப் பூணூலை நீக்கி ஆத்மாவில் மட்டுமே நிலைபெறுவானாக!",
        "theme": "The sacred transition of a householder who desires to renounce: purifying the five vital airs through the Viraja homa, handing over responsibilities without debt, and becoming a silent vessel of the Immortal Light.",
        "SettingVisual": "Ancient thatched Vedic agnihotra sala at dawn, leading out to a tranquil forest riverbank bathed in golden morning light",
        "ProtagonistVisual": "A serene Vedic householder offering final ghee oblations into the sacred fire before stepping forth as a radiant sannyasin",
        "GuruVisual": "Venerable Sama Vedic Guru blessing the transition at the forest threshold",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly shot into a thatched Vedic fire sanctuary (Agnihotra-sala) at dawn, where a mature householder sits before the sacred fire.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot into an ancient Indian thatched Vedic fire sanctuary at golden dawn. A serene middle-aged householder sits before three glowing sacred fire altars as morning sunbeams pierce the rising smoke. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Sama Veda's Laghu-Sannyasa Upanishad, the sacred path is laid out for the householder who has fulfilled his worldly duties and feels the call of the Infinite. Seated before the sacred fire he has tended for decades, he asks: 'How do I transform this outer ritual fire into the immortal flame of Self-Knowledge?'",
                "vo_ta": "சாம வேதத்தின் லகு சந்நியாச உபநிடதத்தில், இல்லறக் கடமைகளை நிறைவேற்றி எல்லையற்ற பரம்பொருளின் அழைப்பை உணரும் சாதகனுக்கான புனித நெறி கூறப்படுகிறது. பல ஆண்டுகளாகத் தான் வளர்த்த யாக அக்னியின் முன் அமர்ந்த அவன், 'இந்தப் புற வேள்வித் தீயை ஆத்ம ஞான அழியாச் சுடராக மாற்றுவது எவ்வாறு?' என்று வினவுகிறான்.",
                "sub_cue": "How does the seeker transform the outer ritual fire into the inner flame of Self-Knowledge?",
                "sound": "Crackling sacred fire, morning birdsong, and a serene Sama Veda Tanpura drone."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of the seeker pouring golden ghee from an earthen pot into the blazing fire while chanting the Viraja purification of the five Pranas.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian seeker pouring golden clarified butter into a blazing homa fire at sunrise, golden flames reflecting in his tear-filled, luminous eyes. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Cooking a sacred offering of milk and ghee, he offers the Viraja oblations to purify every layer of his being: 'May my Prana, Apana, Vyana, Udana, and Samana be purified! May I become the spotless, sinless, Immortal Light of Brahman!'",
                "vo_ta": "விரஜா ஹோமத்தில் நெய்யை ஆஹுதி அளித்துத் தன் உயிரின் ஒவ்வொரு அடுக்கையும் அவன் தூய்மைப்படுத்துகிறான்: 'எனது பிராணன், அபானன், வியானன், உதானன், சமானன் ஆகிய பஞ்ச வாயுக்களும் தூய்மையடையட்டும்! களங்கமற்ற அமிர்த ஜோதியான பிரம்மமாக நான் ஆவேனாக!'",
                "sub_cue": "प्राणापानव्यानोदानसमाना मे शुध्यन्ताम् — May my five Pranas be purified into the Immortal Light of Brahman!",
                "sound": "Blazing fire whoosh and resonant Vedic mantra recitation."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of the seeker inhaling the warm aroma of the fire, shaving his tuft, and releasing his sacred thread into the flowing river.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a newly shaven ancient Indian ascetic standing in golden river waters at dawn, releasing his cotton thread into the current while his heart glows with inner fire. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Inhaling the sacred fire into his own breath, shaving the hair along with the tuft, and relinquishing the outer thread, he entrusts his all to the Supreme Self. Walking northward without looking back, he enters the order of timeless freedom.",
                "vo_ta": "புனித அக்னியைத் தன் மூச்சினுள் வாங்கி, குடுமியுடன் முடியை மழித்துப் புறப் பூணூலை நீரில் விடுத்து, ஆத்மாவிலேயே தன் அனைத்தையும் ஒப்படைக்கிறான். திரும்பிப் பாராமல் வடதிசை நோக்கி நடந்து, காலமற்ற சுதந்திர நிலையில் அவன் புகுகிறான்.",
                "sub_cue": "Inhaling the fire into his breath and walking forward without looking back, he enters freedom.",
                "sound": "Gentle river splash and an uplifting Bansuri flute solo in Raga Bilahari."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Tracking shot of the monk walking through forest and village, accepting a few morsels after household cooking fires have died down.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps tracking shot of a serene barefoot Indian sannyasin in ochre valkala cloth walking quietly past thatched village cottages at noon when kitchen smoke has ceased, holding a simple clay bowl. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "When the pestle is set aside, when the hearth-coals have cooled, and when the household has finished eating, the monk approaches quietly for a few morsels to sustain the body. Equal toward getting or not getting, he guards his senses in unbroken brahmacharya and peace.",
                "vo_ta": "உலக்கை ஓய்ந்து, அடுப்பின் தணல் ஆறி, இல்லத்தார் உண்டு முடித்த பின்பே, உடலைக் காக்கச் சில கவள பிட்சைக்காகத் துறவி அமைதியாக இல்லம் அணுகுகிறார். கிடைத்தாலும் கிடைக்காவிட்டாலும் சமபுத்தியோடு புலனடக்கத்தில் நிலைத்திருக்கிறார்.",
                "sub_cue": "When hearth-coals have cooled, the monk accepts alms with utter equanimity.",
                "sound": "Calm noon ambience with a steady, peaceful Veena melody."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Close-up of the monk meditating in a forest cave at twilight, where his five Pranas shine like five sacred fires around the central altar of the Atman.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi meditating in a stone forest cave; five subtle golden flames of prana light glow within his torso around the radiant central sun of the heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Every breath becomes a cosmic sacrifice! Apana is the Garhapatya fire, Vyana is the Dakshinagni, Prana is the Ahavaniya, and the spotless Atman in the heart is the Supreme Yajamana and Brahman itself!",
                "vo_ta": "அவரது ஒவ்வொரு மூச்சுமே பிரபஞ்ச வேள்வியாக மாறுகிறது! அபானன் கார்ஹபத்ய அக்னி, வியானன் தக்ஷிணாக்னி, பிராணன் ஆஹவனீய அக்னி, இதயத்தில் ஒளிரும் களங்கமற்ற ஆத்மாவே பரப்பிரம்மம்!",
                "sub_cue": "Every breath is a cosmic sacrifice; the spotless Atman in the heart is Supreme Brahman!",
                "sound": "Deep harmonic Omkara chant with five-layered metallic chimes."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the sannyasin seated beneath a starry and sunlit sky on a mountain peak, shining as the Immortal Light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the illumined sannyasin seated in padmasana on a mountain peak at dawn, his form glowing with the spotless golden light of Brahman. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Freed from the triple debt and the triple guna, he shines as Jyotir Amritam—the Immortal Light of Consciousness that neither rises nor sets.",
                "vo_ta": "மூன்று கடன்களிலிருந்தும் முக்குணங்களிலிருந்தும் விடுபட்டு, உதயமும் அஸ்தமனமும் அற்ற 'ஜ்யோதிர் அம்ருதம்' எனும் அமிர்தப் பேரொளியாக அவர் பிரகாசிக்கிறார்.",
                "sub_cue": "ज्योतिरमृतं विरजं ब्रह्म — Shining as the spotless, Immortal Light of Brahman.",
                "sound": "Celestial Saraswati Veena and Tanpura sustain."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the forest hermitage and river bathed in golden morning light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian forest hermitage and golden river at sunrise. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the nineteenth Sannyasa Upanishad: purify every breath with awareness, and let your whole life become a silent oblation into the Immortal Light. Om Apyayantu Mamangani... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பத்தொன்பதாவது சந்நியாச உபநிடதம் நிறைவுறுகிறது: விழிப்புணர்வால் ஒவ்வொரு மூச்சையும் தூய்மையாக்கி, நம் வாழ்வையே அமிர்த ஜோதியில் இடும் மௌன ஆஹுதியாக்குவோமாக. ஓம் ஆப்யாயந்து மமாங்கானி... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Purify every breath with awareness; abide as the Immortal Light. Om Shanti.",
                "sound": "Sama Veda Shanti Mantra fading into tranquil morning breeze."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 20 (YOGA 1). SHWETASHVATARA UPANISHAD (#14)
    {
        "story_id": "YOGA_01_SHWETASHVATARA",
        "muktika_number": 14,
        "name_sanskrit": "श्वेताश्वतरोपनिषद्",
        "name_iast": "Śvetāśvataropaniṣad",
        "name_tamil": "சுவேதாஸ்வதர உபநிடதம்",
        "name_english": "Shwetashvatara Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Two Birds on the Cosmic Tree & The Fire of Dhyana-Yoga: Sage Shwetashvatara",
        "story_title_tamil": "ஒரே மரத்தின் இரு பறவைகளும் தியான யோக அக்னியும்: சுவேதாஸ்வதர மகரிஷி",
        "characters": "Maharishi Shwetashvatara ('He of the Pure White Senses'), The Assembly of Brahmavadin Rishis, The Two Birds (Jiva & Ishwara), Rudra-Shiva (The One Cosmic Lord)",
        "verse_sanskrit": "त्रिरुन्नतं स्थाप्य समं शरीरं हृदीन्द्रियाणि मनसा सन्निवेश्य । ब्रह्मोडुपेन प्रतरेत विद्वान् स्रोतांसि सर्वाणि भयावहानि ॥ यस्य देवे परा भक्तिर्यथा देवे तथा गुरौ । तस्यैते कथिता ह्यर्थाः प्रकाशन्ते महात्मनः ॥",
        "verse_tamil_translit": "த்ரிருன்னதம் ஸ்தாப்ய ஸமம் ஷரீரம் ஹ்ருதீந்த்ரியாணி மனஸா ஸன்னிவேஷ்ய | ப்ரஹ்மோடுபேன ப்ரதரேத வித்வான் ஸ்ரோதாம்ஸி ஸர்வாணி பயாவஹானி ||",
        "verse_meaning_english": "Holding the body steady with the three upper parts (chest, neck, and head) erect, drawing the senses with the mind into the heart, the wise yogi crosses over all terrifying currents of samsara in the boat of Brahman! Unto that great soul who has supreme devotion to God and equally to the Guru, these truths shine forth!",
        "verse_meaning_tamil": "மார்பு, கழுத்து, தலை ஆகிய மூன்றையும் நேராக நிறுத்தி, மனத்தால் புலன்களை இதயத்தில் ஒடுக்கி, பிரணவம் எனும் பிரம்மத் தோணியால் சம்சாரத்தின் அச்சமூட்டும் சுழல்களை ஞானி கடக்கிறான்! இறைவனிடத்தும் குருவிடத்தும் பரம பக்தி கொண்ட மகாத்மாவுக்கே இவ்வுண்மைகள் பிரகாசிக்கின்றன!",
        "theme": "The grand foundational synthesis of Dhyana-Yoga, Sankhya, Bhakti, and Advaita: the inquiry 'Kim karanam Brahma', the metaphor of the Two Birds on one fig tree, the nine-gated lotus cave of posture and pranayama, churning the body with Om, and Para-Bhakti to Deva and Guru.",
        "SettingVisual": "Quiet mist-free Himalayan cave shelter beside a crystal mountain stream and a giant Peepal tree where two birds perch at golden dawn",
        "ProtagonistVisual": "The Assembly of Brahmavadin Sages questioning the first cause of the cosmos",
        "GuruVisual": "Maharishi Shwetashvatara, radiant white-robed master of pure senses, seated in perfect tri-unnata erect yoga posture",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide crane shot over a Himalayan forest clearing at dawn as a circle of Brahmavadin sages sit around a sacred fire, questioning the ultimate cause of existence before Maharishi Shwetashvatara.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an ancient Himalayan forest clearing at golden sunrise. A circle of Vedic sages sit around a glowing homa fire questioning radiant Maharishi Shwetashvatara seated on a flat granite stone under a peepal tree. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the sacred assembly of the Krishna Yajur Veda, the Brahmavadins pondered the ultimate mystery of existence: 'Kim karanam Brahma? What is the First Cause? Is it Brahman? Whence are we born? By what do we live, and where do we finally rest? Is it Time, Nature, Fate, Chance, or the Elements?'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் புனித சபையில், பிரம்மவாதிகளான முனிவர்கள் பிரபஞ்சத்தின் மூல காரணத்தை ஆராய்ந்தனர்: 'கிம் காரணம் ப்ரஹ்ம? முதற்காரணம் எது? நாம் எங்கிருந்து பிறந்தோம்? எதனால் வாழ்கிறோம்? எதில் ஒடுங்குகிறோம்? காலம், இயற்கை, விதி, தற்செயல் அல்லது பஞ்ச பூதங்கள் காரணமா?'",
                "sub_cue": "किं कारणं ब्रह्म कुतः स्म जाताः — What is the First Cause? Whence are we born, and where do we rest?",
                "sound": "Deep Vedic chorus chanting 'Harih Om, Kim Karanam Brahma', crackling homa fire, and resonant Tanpura."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Slow dolly-in on Maharishi Shwetashvatara in deep Dhyana-Yoga, his chest, neck, and head perfectly aligned as a golden wheel of cosmic energy revolves and stills around him.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dolly-in shot of Maharishi Shwetashvatara seated in padmasana with chest, neck, and head held perfectly erect; a subtle golden cosmic wheel of light revolves around him and dissolves into his serene heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Entering the depths of Dhyana-Yoga, Maharishi Shwetashvatara—he who had mastered his senses like pure white horses—beheld the answer not in dry speculation, but in direct yogic vision! He saw the Devatma-Shakti—the Divine Conscious Power of the One Lord—hidden by its own gunas, ruling over Time and Soul alike.",
                "vo_ta": "தன் புலன்களை வெண் குதிரைகளைப் போல் அடக்கிய சுவேதாஸ்வதர மகரிஷி, வெறும் தர்க்கத்தால் அல்லாமல் 'தியான யோக' சமாதியில் விடையைத் தரிசித்தார்! முக்குணங்களால் மறைக்கப்பட்ட இறைவனின் 'தேவாத்ம சக்தி'யே காலம் முதலான அனைத்தையும் இயக்குவதை அவர் நேருக்கு நேர் கண்டார்.",
                "sub_cue": "ते ध्यानयोगानुगता अपश्यन् देवात्मशक्तिं — Through Dhyana-Yoga, the Sages beheld the Divine Power!",
                "sound": "Majestic Rudra Veena and Pakhawaj entering in a steady, meditative rhythm."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Poetic close-up of two birds perched on the same Peepal branch at sunrise: the lower bird pecking anxiously at bittersweet figs, while the upper bird shines in golden stillness without eating.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic close-up of two beautiful birds perched on the branch of an ancient sacred peepal tree at golden dawn. The lower bird pecks at red figs while the upper bird sits higher in serene golden radiance, watching calmly as a witness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Shwetashvatara sang the immortal parable of the Two Birds: 'Two birds of inseparable friendship cling to the selfsame tree! One eats the sweet and bitter fruits of karma, grieving in delusion; the other looks on as the silent Witness without eating! When the lower bird looks up and beholds the glorious Lord, all its sorrow vanishes at once!'",
                "vo_ta": "சுவேதாஸ்வதரர் இரு பறவைகளின் உவமையை அருளினார்: 'பிரியா நட்பு கொண்ட இரு பறவைகள் ஒரே மரத்தில் அமர்ந்துள்ளன! ஒன்று கர்மத்தின் இன்ப-துன்பக் கனிகளை உண்டு மயங்குகிறது; மற்றொன்றோ எதையும் உண்ணாமல் மௌன சாட்சியாகப் பிரகாசிக்கிறது! கீழே உள்ள ஜீவப் பறவை மேலே உள்ள ஈசனைத் திரும்பிப் பார்க்கும் கணமே அதன் சோகமெல்லாம் மறைகிறது!'",
                "sub_cue": "द्वा सुपर्णा सयुजा सखाया — Two birds on one tree: one eats the fruit, the other shines as the Witness!",
                "sound": "Expressive Bansuri duet where a restless lower flute phrase merges into a serene, sustained upper flute note."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Inside a shelter cave free of wind and dust beside a gentle stream: the yogi sits erect, and inner visions of mist, smoke, sun, fireflies, lightning, crystal, and the moon appear.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot inside a quiet, level Himalayan rock cave beside a gentle stream. A yogi sits with chest, neck, and head erect in pranayama; subtle luminous visions of golden fireflies, lightning, and a crystal moon shimmer softly in the air before his closed eyes. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Shwetashvatara taught the exact method of Yoga: 'In a level, pure cave free from pebbles, fire, and noise, soothing to the mind alongside gentle waters, hold the chest, neck, and head erect in a straight line! Restraining the breath and drawing the senses into the heart, cross the terrifying currents of samsara in the boat of Omkara! First appear visions of mist, smoke, sun, wind, fire, fireflies, lightning, crystal, and the moon—the heralds of Brahman!'",
                "vo_ta": "தியான யோகத்தின் செயல்முறையை மகரிஷி விவரித்தார்: 'கற்களோ இரைச்சலோ இல்லாத, நீர்நிலைக்கு அருகிலுள்ள சமமான குகையில், மார்பு, கழுத்து, தலை ஆகிய மூன்றையும் நேராக நிறுத்தி அமர்க! பிராணனை அடக்கிப் புலன்களை இதயத்தில் ஒடுக்கி, ஓங்காரத் தோணியால் சம்சாரக் கடலைக் கடப்பாயாக! மூடுபனி, புகை, சூரியன், மின்மினி, மின்னல், பளிங்கு, சந்திரன் ஆகிய உள் ஒளிகள் பிரம்ம தரிசனத்தின் முன்னோடிகளாகத் தோன்றும்!'",
                "sub_cue": "त्रिरुन्नतं स्थाप्य समं शरीरं — Hold chest, neck, and head erect; cross samsara in the boat of Brahman!",
                "sound": "Deep rhythmic pranayama breath, gentle stream murmur, and shimmering Santoor harmonics representing the nine inner lights."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi churning the inner flame with Omkara as his body glows with youthfulness, health, and golden Rudra-Shiva effulgence.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of Maharishi Shwetashvatara in deep samadhi; a brilliant golden-white sun of Consciousness blazes in his heart center, illuminating the entire cave with divine light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Making the body the lower fire-stick and Pranava the upper stick, churn with the drill of Dhyana until the hidden God shines forth! 'Vedaham etam purusham mahantam, adityavarnam tamasah parastat—I know that Great Purusha, luminous as the Sun beyond all darkness! By knowing Him alone does one conquer death; there is no other path to liberation!'",
                "vo_ta": "உடலைக் கீழ்க்கட்டையாகவும் பிரணவத்தை மேல்கட்டையாகவும் கொண்டு தியானத்தால் கடைந்தால் மறைந்திருக்கும் இறைவன் வெளிப்படுவான்! 'வேதாஹமேதம் புருஷம் மஹாந்தம் ஆதித்யவர்ணம் தமஸ: பரஸ்தாத் — இருளுக்கு அப்பால் சூரியனைப் போல் ஒளிரும் அந்த மகா புருஷனை நான் அறிவேன்! அவனை அறிவதால் மட்டுமே மரணத்தை வெல்ல முடியும்; முக்திக்கு வேறு வழியில்லை!'",
                "sub_cue": "वेदाहमेतं पुरुषं महान्तमादित्यवर्णं तमसः परस्तात् — I know that Great Purusha, luminous as the Sun beyond darkness!",
                "sound": "Triumphant Shankha blast, temple bells, and Vedic choral roar of 'Vedaham Etam Purusham Mahantam'."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide cosmic shot of the sages beholding the One Deva hidden in all beings, when the skyitself seems rolled up like a leather scroll.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of Maharishi Shwetashvatara and the sages seated on a Himalayan peak at sunrise as golden cosmic light arches across the sky, revealing the One Divine presence pervading mountains, trees, and sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Only when men can roll up the boundless sky like a piece of leather could sorrow end without knowing the luminous God within! Freed from all fetters, experiencing lightness, health, steadiness, and a melodious voice of yoga-siddhi, the sage realizes the One Rudra-Shiva who pervades every heart.",
                "vo_ta": "ஆகாயத்தைத் தோல் சுருளைப் போல் சுருட்ட முடிந்தால் மட்டுமே இறைவனை அறியாமல் துன்பம் நீங்கும்! யோக சித்தியால் உடல் இலகுவாகி, சகல பாசங்களிலிருந்தும் விடுபட்டு, எல்லா உயிர்களிலும் மறைந்திருக்கும் ஏக தேவனான ருத்ர-சிவனை முனிவர் தரிசிக்கிறார்.",
                "sub_cue": "एष देवो विश्वकर्मा महात्मा सदा जनानां हृदये सन्निविष्टः — This Great Lord ever dwells in the hearts of all!",
                "sound": "Soaring Saraswati Veena and Violin symphony in Raga Shankarabharanam."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Intimate two-shot of a disciple bowing in supreme devotion at the feet of Maharishi Shwetashvatara as golden sunlight bathes the hermitage.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps serene pull-back shot of Vedic disciples bowing with supreme devotion before Maharishi Shwetashvatara under the sacred peepal tree at golden sunrise. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Shwetashvatara Upanishad with its immortal seal: 'Yasya deve para bhaktir, yatha deve tatha gurau—unto that great soul who has supreme devotion to God, and as to God so to the Guru, all these truths shine forth of their own accord!' Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு சுவேதாஸ்வதர உபநிடதம் தன் அழியா முத்திரையோடு நிறைவுறுகிறது: 'யஸ்ய தேவே பரா பக்திர் யதா தேவே ததா குரௌ — இறைவனிடத்தில் பரம பக்தியும், இறைவனிடத்தில் எவ்வாறோ அவ்வாறே குருவிடத்திலும் பக்தி கொண்ட மகாத்மாவுக்கே இவ்வுண்மைகள் அனைத்தும் தாமாகவே பிரகாசிக்கும்!' ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "यस्य देवे परा भक्तिर्यथा देवे तथा गुरौ — To him who has supreme devotion to God and Guru, Truth shines forth! Om Shanti.",
                "sound": "Resonant chorus chanting 'Yasya Deve Para Bhaktih' and 'Om Saha Navavatu' fading into peaceful morning air."
            }
        ]
    },
    # 21 (YOGA 2). HAMSA UPANISHAD (#15)
    {
        "story_id": "YOGA_02_HAMSA",
        "muktika_number": 16,
        "name_sanskrit": "हंसोपनिषद्",
        "name_iast": "Haṃsopaniṣad",
        "name_tamil": "ஹம்ஸ உபநிடதம்",
        "name_english": "Hamsa Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The 21,600 Breaths of Ajapa Gayatri & The Ten Inner Nada Sounds: Gautama & Sanatkumara",
        "story_title_tamil": "21,600 அஜபா காயத்ரி மூச்சும் பத்து அனாஹத நாதங்களும்: கௌதமர் மற்றும் சனத்குமாரர்",
        "characters": "Maharishi Gautama (Earnest Seeker), Bhagavan Sanatkumara (Eternal Youth & Master of Hamsa-Vidya), Lord Shiva & Parvati (Originators of the Vidya)",
        "verse_sanskrit": "हकारेण बहिर्याति सकारेण विशेत्पुनः । हंस हंसेत्यमुं मन्त्रं जीवो जपति सर्वदा ॥ शतानि षट् दिवारात्रं सहस्राण्येकविंशतिः । एतत्संख्यान्वितं मन्त्रं जीवो जपति सर्वदा ॥",
        "verse_tamil_translit": "ஹகாரேண பஹிர்யாதி ஸகாரேண விஷேத் புன: | ஹம்ஸ ஹம்ஸேத்யமும் மந்த்ரம் ஜீவோ ஜபதி ஸர்வதா ||",
        "verse_meaning_english": "With the sound 'Ham' the breath goes out; with the sound 'Sa' it enters again! Every living being ceaselessly chants this mantra 'Hamsa, Hamsa' twenty-one thousand six hundred times every day and night!",
        "verse_meaning_tamil": "'ஹம்' என்ற ஒலியுடன் மூச்சு வெளியே செல்கிறது; 'ஸ' என்ற ஒலியுடன் மீண்டும் உள்ளே நுழைகிறது! இரவும் பகலும் இருபத்தோராயிரத்து அறுநூறு முறை ஒவ்வொரு ஜீவனும் 'ஹம்ஸ ஹம்ஸ' என்ற இம்மந்திரத்தை இடைவிடாது ஜபிக்கிறது!",
        "theme": "The secret of Hamsa-Vidya (Ajapa Gayatri) imparted by Sanatkumara to Gautama: the eight-petalled heart lotus where the Hamsa bird moves depending on one's mental states, reversing 'Hamsa' into 'Soham', and ascending through the ten unstruck Nada sounds from 'Chini' to the thundercloud, dissolving into Turiya.",
        "SettingVisual": "Luminous Kailasa-inspired Himalayan crystal lake and granite meditation pavilion at golden dawn with white swans",
        "ProtagonistVisual": "Maharishi Gautama with silver beard and rudraksha, bowing with folded hands",
        "GuruVisual": "Bhagavan Sanatkumara, the ever-radiant youth of supreme wisdom, glowing with golden-white yogic light",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow glide shot across a crystal Himalayan lake where a white swan floats at sunrise, rising to show Maharishi Gautama bowing before Bhagavan Sanatkumara.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic glide shot across a crystal Himalayan lake at golden dawn with a white swan on the water. Maharishi Gautama bows with folded hands before the radiant, youthful sage Bhagavan Sanatkumara seated on a granite lotus dais. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Shukla Yajur Veda's Hamsa Upanishad, Maharishi Gautama approached the eternal sage Sanatkumara and asked: 'O Bhagavan, you who know all truths! Teach me the supreme mystery of Brahmavidya by which the yogi attains immortality!'",
                "vo_ta": "சுக்ல யஜுர் வேதத்தின் ஹம்ஸ உபநிடதத்தில், கௌதம மகரிஷி நித்திய குமாரரான பகவான் சனத்குமாரரை அணுகி வினவினார்: 'பகவானே! சகல தத்துவங்களையும் அறிந்தவரே! யோகிக்கு அமரத்துவத்தை நல்கும் பிரம்மவித்தையின் பரம ரகசியத்தை எனக்கு உபதேசித்தருளுங்கள்!'",
                "sub_cue": "Gautama asks Sanatkumara: 'Teach me the supreme mystery of Hamsa-Brahmavidya!'",
                "sound": "Gentle lapping of crystal lake water, distant swan call, and a serene Bansuri prelude in Raga Hamsadhwani."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Sanatkumara's luminous eyes as he speaks of the treasure hidden like gold in the earth, taught originally by Shiva to Parvati.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Bhagavan Sanatkumara's serene, radiant face bathed in golden morning light, his right hand raised in jnana mudra as Maharishi Gautama listens with deep reverence. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Sanatkumara replied: 'Listen, O Gautama! This Hamsa-Vidya, which Lord Shiva once revealed to Parvati, is like a hidden treasure of gold beneath your very feet! It is revealed only to the self-controlled Brahmachari who is tranquil and devoted to the Guru.'",
                "vo_ta": "சனத்குமாரர் அருளினார்: 'கேளும் கௌதமரே! சிவபெருமான் பார்வதி தேவிக்கு அருளிய இந்த ஹம்ஸ வித்தை, நம் காலடியில் புதைந்திருக்கும் பொற்பुधையலைப் போன்றது! புலனடக்கமும், மன அமைதியும், குரு பக்தியும் கொண்ட சாதகனுக்கு மட்டுமே இது வெளிப்படுகிறது.'",
                "sub_cue": "Like a treasure hidden beneath one's feet, Hamsa-Vidya shines within every breath.",
                "sound": "Warm Tanpura drone with soft, mystical Saraswati Veena harmonics."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Macro-spiritual shot of the meditating yogi's breath: golden prana flowing out with 'Ham' and silvery-golden prana entering with 'Sa' 21,600 times a day.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi in padmasana at dawn; subtle golden and silver streams of prana light flow gently out and in with his breath from the heart lotus to the nostrils. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Sanatkumara unveiled the Ajapa Gayatri: 'As fire dwells in all wood and oil in all sesame seeds, the Hamsa pervades all bodies! With the sound Ham the breath goes out; with the sound Sa it enters again! Twenty-one thousand six hundred times every day and night, every living being chants this unuttered mantra! When reversed through awareness, Hamsa becomes Soham—I am He!'",
                "vo_ta": "அஜபா காயத்ரி ரகசியத்தை சனத்குமாரர் வெளியிட்டார்: 'ஹம் என்ற ஒலியுடன் மூச்சு வெளியேறுகிறது; ஸ என்ற ஒலியுடன் மீண்டும் உள்நுழைகிறது! இரவும் பகலும் இருபத்தோராயிரத்து அறுநூறு முறை ஒவ்வொரு உயிரும் இம்மந்திரத்தை உச்சரிக்காமலேயே ஜபிக்கிறது! விழிப்புணர்வால் இதனைத் திருப்பினால் ஹம்ஸ என்பது ஸோஹம்—அவனே நான் என்றாகிறது!'",
                "sub_cue": "हकारेण बहिर्याति सकारेण विशेत्पुनः — 21,600 times a day the breath chants Hamsa—Soham!",
                "sound": "Rhythmic breath-synchronized Bansuri and Tanpura pulsing gently between 'Ham' and 'Sa'."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Visualization of an eight-petalled golden lotus in the heart center: as the yogi's mind moves from the outer petals to the glowing pericarp and filament, the swan of awareness settles into stillness.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of a meditating yogi inside a granite mandapam; at his heart center shines a translucent eight-petalled golden lotus of light with a luminous white swan of prana resting in its center. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Within the heart blooms an eight-petalled lotus! When the Hamsa moves to the eastern petal, virtuous thoughts arise; on the southeastern, sleep and laziness; on the southern, cruelty; on the southwestern, sin; on the western, play; on the northwestern, restlessness; on the northern, love and peace; on the northeastern, charity! In the filament wakes the soul; in the pericarp shines Pure Consciousness; and when the Hamsa rises above the lotus, that is Turiya!",
                "vo_ta": "இதயத்தில் எட்டு இதழ்கள் கொண்ட தாமரை மலர்ந்துள்ளது! கிழக்கு இதழில் புண்ணிய எண்ணமும், வடக்கு இதழில் அன்பும் அமைதியும், நடுக்கேசரத்தில் விழிப்புணர்வும் தோன்றுகின்றன. தாமரையின் பொகுட்டில் தூய சைதன்யம் ஒளிர்கிறது; அத்தாமரைக்கும் மேலே ஹம்ஸம் உயரும்போது அதுவே துரிய நிலையாகும்!",
                "sub_cue": "Rising from the eight petals of the Heart Lotus into the center, the Hamsa ascends to Turiya.",
                "sound": "Delicate eight-note Santoor scale resolving into a pure, sustained Veena chord."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic auditory-visual sequence inside a mountain cave as the yogi listens to the Ten Unstruck Nada Sounds, culminating in the deep resonance of the Tenth Sound (Thundercloud).",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of Maharishi Gautama in deep samadhi inside a sunlit stone cave; concentric golden sound-waves of Anahata Nada ripple outward from his crown chakra like celestial music. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "As Hamsa dissolves into Nada, ten unstruck inner sounds arise: first 'Chini', second 'Chini-chini', third the bell, fourth the conch, fifth the tantri lute, sixth the cymbals, seventh the flute, eighth the bheri drum, ninth the mridanga, and tenth the majestic roar of the thundercloud! Shun the first nine sounds, O Gautama, and merge your mind into the Tenth Sound alone—there the mind dissolves into spotless Brahman!",
                "vo_ta": "ஹம்ஸம் நாதத்தில் ஒடுங்கும்போது பத்து அனாஹத ஒலிகள் எழுகின்றன: சினி, சினி-சினி, மணி, சங்கு, வீணை, தாளம், புல்லாங்குழல், பேரிகை, மிருதங்கம் மற்றும் பத்தாவதாக கார்மேகத்தின் இடி முழக்கம்! முதல் ஒன்பது ஒலிகளைக் கடந்து பத்தாவது மேக நாதத்தில் மனதைக் கரைப்பாயாக—அங்கே மனம் மறைந்து தூய பிரம்மம் மட்டுமே எஞ்சும்!",
                "sub_cue": "Ten Unstruck Nada Sounds arise: transcend the nine and merge into the Tenth Sound of Brahman!",
                "sound": "Extraordinary acoustic progression layering bell, conch, veena, cymbals, flute, and mridangam, culminating in a deep, sacred thunder-drone of Omkara."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Gautama and Sanatkumara glowing like ten million suns of pure consciousness beside the crystal lake.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Bhagavan Sanatkumara and Maharishi Gautama seated in nirvikalpa samadhi beside the Himalayan crystal lake at sunrise, bathed in golden-white effulgence. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "When the mind is dissolved in that tenth Nada, Sankalpa and Vikalpa vanish, virtues and sins are burned away, and the yogi shines as Sadashiva—pervading all things like the boundless sky, luminous as ten million suns!",
                "vo_ta": "அந்தப் பத்தாவது நாதத்தில் மனம் லயிக்கும்போது, சங்கல்ப-விகல்பங்கள் அழிந்து, புண்ணிய-பாவங்கள் எரிந்து, கோடி சூரியப் பிரகாசத்துடன் எங்கும் நிறைந்த சதாசிவனாகவே யோகி மிளிர்கிறார்!",
                "sub_cue": "When the mind dissolves in the Tenth Nada, the Yogi shines as the all-pervading Sadashiva!",
                "sound": "Celestial harmonic overtones and spacious Tanpura resonance."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane rise over the crystal lake as a white swan glides across the golden reflection of the rising sun.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the Himalayan crystal lake at dawn as a white swan glides peacefully across the golden reflection of the sun. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Hamsa Upanishad: every single breath you take is a sacred mantra calling you home to the Self. Listen to that inner swan and awaken to Soham. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு ஹம்ஸ உபநிடதம் நிறைவுறுகிறது: நாம் வாங்கும் ஒவ்வொரு மூச்சுமே நம்மை ஆத்ம வீட்டிற்கு அழைக்கும் புனித மந்திரமாகும். அந்த உள் அன்னத்தின் குரலைக் கேட்டு 'ஸோஹம்' என விழித்தெழுவோமாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Every breath chants Soham—listen to the inner Nada and awaken to the Self. Om Shanti.",
                "sound": "Shanti Mantra 'Om Purnamadah' with gentle swan wingbeats and fading flute."
            }
        ]
    },
    # 22 (YOGA 3). AMRITABINDU UPANISHAD (#20)
    {
        "story_id": "YOGA_03_AMRITABINDU",
        "muktika_number": 20,
        "name_sanskrit": "अमृतबिन्दूपनिषद्",
        "name_iast": "Amṛtabindūpaniṣad",
        "name_tamil": "அம்ருதபிந்து உபநிடதம்",
        "name_english": "Amritabindu Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Drop of Immortal Nectar: From Book-Learning to Silent Samadhi",
        "story_title_tamil": "அமிர்தத் துளி: ஏட்டுக் கல்வியைக் கடந்து மௌன சமாதிக்கு: அம்ருதபிந்து உபநிடதம்",
        "characters": "The Scholarly Vedic Seeker Burdened with Texts, The Illumined Yoga Master, The One Atman Shining in All Vessels",
        "verse_sanskrit": "ग्रन्थमभ्यस्य मेधावी ज्ञानविज्ञानतत्परः । पलालमिव धान्यार्थी त्यजेद्ग्रन्थमशेषतः ॥ गोअनेकवर्णां क्षीरस्य एकवर्णां यथा पयः । क्षीरवत्पश्यते ज्ञानं लिङ्गिनस्तु गवां यथा ॥",
        "verse_tamil_translit": "க்ரந்தமப்யஸ்ய மேதாவீ க்ஞானவிக்ஞானதத்பர: | பலாலமிவ தான்யார்த்தீ த்யஜேத் க்ரந்தமஷேஷத: ||",
        "verse_meaning_english": "Having studied the scriptures, the intelligent seeker intent on direct Knowledge and Realization should set aside the heap of books completely, just as a harvester seeking grain throws away the empty chaff! Though cows are of many colors, their milk is of one white color; look upon Consciousness as the one milk and bodies as the varied cows!",
        "verse_meaning_tamil": "சாஸ்திரங்களைக் கற்றறிந்த புத்திமான், நேரடி ஞானானுபவத்தில் நிலைபெற்று, நெல்மணியை எடுத்த பின் பதரை வீசி எறிவது போல ஏட்டுச் சுவடிகளின் சுமையை விட்டுவிட வேண்டும்! பசுக்கள் பல நிறத்தனவாயினும் பால் ஒரே வெண்மை நிறமானது போல, உடல்கள் பலவாயினும் உள்ளிருக்கும் ஆத்ம ஞானம் ஒன்றே!",
        "theme": "The two states of mind (impure with desire and pure without desire), transcending sound-Omkara into soundless Brahman, discarding bookish chaff after gathering the grain of wisdom, and beholding the one white milk of Consciousness in the many-colored cows of living beings.",
        "SettingVisual": "Ancient forest gurukulam courtyard at golden dawn with palm-leaf manuscripts, harvesting grain fields, cows, and a serene meditation hall",
        "ProtagonistVisual": "An earnest Vedic scholar setting down a heavy bundle of palm-leaf manuscripts to sit in silent meditation",
        "GuruVisual": "Luminous Yoga Acharya seated beside an earthen bowl of pure white milk and a brass oil lamp",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly shot into a sunlit forest gurukulam where a weary scholar carrying stacks of palm-leaf manuscripts bows before the silent Yoga Acharya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot in an ancient Indian forest gurukulam at golden sunrise. A Vedic scholar carrying bundles of palm-leaf manuscripts kneels humbly before a serene, luminous Yoga Acharya seated on a stone dais. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's Amritabindu Upanishad—the Upanishad of the Drop of Immortal Nectar—a seeker burdened by endless scriptural debates approached the Master and asked: 'O Bhagavan! How is the restless mind stilled so that one may taste the direct nectar of Brahman?'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் அம்ருதபிந்து உபநிடதத்தில், முடிவற்ற சாஸ்திர வாதங்களால் களைப்படைந்த சாதகன் குருவை அணுகிக் கேட்டான்: 'பகவானே! அலைபாயும் மனதை அடக்கி, பிரம்ம அமிர்தத்தின் நேரடித் துளியைச் சுவைப்பது எவ்வாறு?'",
                "sub_cue": "How is the restless mind stilled to taste the direct nectar of Brahman?",
                "sound": "Rustling of palm-leaf manuscripts giving way to a deep, calming Tanpura and Bansuri drone."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of the Acharya's calm eyes reflecting a still earthen water bowl beside a rippling bowl.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of two earthen water bowls before the Yoga Acharya at dawn—one rippling with wind, the other mirror-still reflecting the golden sun—as the Guru instructs his disciple. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Master began with the foundational secret of Yoga: 'The mind is declared to be of two kinds—impure and pure! Impure is that mind which is driven by desire-resolutions; pure is that mind which is completely free of desire! Therefore, restrain the mind within the heart until it reaches complete dissolution—that is both Knowledge and Liberation!'",
                "vo_ta": "யோகத்தின் அடிப்படை ரகசியத்தை குரு உபதேசித்தார்: 'மனம் சுத்தம், அசுத்தம் என இரு வகைப்படும்! காம சங்கல்பங்களால் அலைவது அசுத்த மனம்; ஆசையற்றது சுத்த மனம்! எனவே, இதயத்தில் மனதை நிறுத்தி அது முழுமையாக ஒடுங்கும் வரை பழகுவாயாக—அதுவே ஞானம், அதுவே முக்தி!'",
                "sub_cue": "मनो हि द्विविधं प्रोक्तं शुद्धं चाशुद्धमेव च — Pure is the mind free from desire!",
                "sound": "Gentle water ripples settling into a pure, crystalline Santoor chord."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of the yogi chanting Omkara aloud, then softly, then entering radiant silent stillness (Ashabda Brahman).",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of an ancient Indian yogi meditating in a sunlit stone pavilion, transitioning from chanting Omkara to sitting in radiant, soundless samadhi as golden light fills his aura. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "How should one meditate? 'First meditate upon Brahman through the sound-syllable Om; then transcend sound to enter the Soundless Supreme! For one who clings only to the outer sound without entering silence does not yet behold the Non-Being beyond manifestation. Only in soundless stillness does the Supreme Brahman shine!'",
                "vo_ta": "தியானிக்கும் முறை யாது? 'முதலில் ஓங்கார ஒலியால் பிரம்மத்தைத் தியானிக்க வேண்டும்; பின் ஒலியையும் கடந்து நிശബ്दமான அசப்தப் பிரம்மத்தில் புக வேண்டும்! புற ஒலியைக் கடந்து மௌனத்தில் நிலைபெறும்போது மட்டுமே சுயம்பிரகாசமான பரப்பிரம்மம் புலப்படும்!'",
                "sub_cue": "Meditate first with Omkara; then cross over into the Soundless Supreme!",
                "sound": "Resonant vocal 'Ommm' gradually fading into a luminous, high-register violin harmonic and silence."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Rich visual triptych of three iconic Upanishadic metaphors: (1) winnowing golden paddy grain from chaff, (2) cows of brown, black, and spotted colors yielding one pure white milk, and (3) churning butter from milk.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot in an ancient Indian ashram courtyard at sunrise showing golden paddy grain separated from chaff beside an earthen pot of pure white milk and peaceful ashram cows in the background. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then the Master gave three unforgettable metaphors: 'First, having studied the scriptures and grasped the truth, let the wise man set aside the heap of books, just as one seeking rice throws away the empty chaff! Second, though cows are of many colors, their milk is of one white color—look upon Consciousness as the one milk and bodies as the varied cows! Third, as butter is hidden in milk, churn the mind to bring forth the Self!'",
                "vo_ta": "குரு மூன்று அழியா உவமைகளை அருளினார்: 'முதலாவது, சாஸ்திரங்களைக் கற்று உண்மையை உணர்ந்த பின், நெல்மணியை எடுத்துக்கொண்டு பதரை வீசி எறிவது போல ஏட்டுச் சுமையை விட்டுவிடுக! இரண்டாவது, பசுக்கள் பல நிறத்தனவாயினும் பால் ஒரே வெண்மை நிறமானது போல, உடல்கள் பலவாயினும் உள்ளிருக்கும் ஆத்மா ஒன்றே! மூன்றாவது, பாலில் மறைந்திருக்கும் வெண்ணெயைக் கடைவது போல் தியானத்தால் ஆத்மாவை வெளிக்கொணர்க!'",
                "sub_cue": "Throw away the chaff of mere book-learning; behold the One White Milk of Consciousness in all beings!",
                "sound": "Warm, pastoral Bansuri and Mridangam melody in Raga Khamas."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the moon reflected in ten earthen pots of water; as a pot is removed, the sky-moon remains whole and unchanged.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of several earthen pots filled with crystal water reflecting the single golden sun in an ashram courtyard, while the yogi meditates in luminous realization behind them. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Just as the one Moon reflected in water appears both still and trembling, so the One Atman appears bound in the ignorant and free in the wise! And just as space inside a pot merges seamlessly with cosmic space when the pot breaks, the Atman is forever one and undivided!",
                "vo_ta": "நீரில் பிரதிபலிக்கும் ஒரே சந்திரன் அசைவது போலவும் அசையாதது போலவும் தோன்றுவது போல, ஒரே ஆத்மா அஞ்ஞானிக்குக் கட்டுண்டது போலவும் ஞானிக்கு முக்தனாகவும் தோன்றுகிறது! குடம் உடைந்தாலும் குடத்து ஆகாயம் மகா ஆகாயத்தோடு ஒன்றாகவே இருப்பது போல ஆத்மா என்றும் பிரிக்க முடியாத ஒன்றே!",
                "sub_cue": "एक एव हि भूतात्मा भूते भूते व्यवस्थितः — One alone is the Self abiding in every being, like the Moon in water!",
                "sound": "Majestic Saraswati Veena and choral chant of 'Eka Eva Hi Bhutatma'."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the awakened seeker and Guru seated in radiant silence as golden light unites every creature and tree in the gurukulam.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the Yoga Acharya and his awakened disciple seated in samadhi in the sunlit ashram courtyard, surrounded by a unified golden field of consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Tasting that drop of immortal nectar, the sage declares: 'I am Vasudeva, the abode of all beings! I dwell in all creatures, and all creatures dwell in Me!'",
                "vo_ta": "அந்த அமிர்தத் துளியைச் சுவைத்த முனிவர் முழங்குகிறார்: 'சகல உயிர்களின் உறைவிடமான வாசுதேவன் நானே! எல்லா உயிர்களிலும் நான் உறைகிறேன்; எல்லா உயிர்களும் என்னுள் உறைகின்றன!'",
                "sub_cue": "वासुदेवोऽहमोमिति — I am Vasudeva, the Indwelling Self of all beings!",
                "sound": "Expansive Shankha and serene Bansuri duet."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the forest gurukulam at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian forest gurukulam bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Amritabindu Upanishad: move beyond mere words into silent realization, and see the one pure Consciousness shining in every living form. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு அம்ருதபிந்து உபநிடதம் நிறைவுறுகிறது: வெறும் வார்த்தைகளைக் கடந்து மௌன அனுபூதியில் ஆழ்ந்து, ஒவ்வொரு உயிரிலும் ஒளிரும் ஒரே தூய உணர்வைக் காண்போமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Move beyond words into silent realization; see the One Consciousness in all. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into peaceful morning air."
            }
        ]
    },
    # 23 (YOGA 4). AMRITANADA UPANISHAD (#21)
    {
        "story_id": "YOGA_04_AMRITANADA",
        "muktika_number": 21,
        "name_sanskrit": "अमृतनादोपनिषद्",
        "name_iast": "Amṛtanādopaniṣad",
        "name_tamil": "அம்ருதநாத உபநிடதம்",
        "name_english": "Amritanada Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Chariot of Omkara & Six-Limbed Yoga: Abandoning the Torch at the Portal of Light",
        "story_title_tamil": "ஓங்காரத் தேரும் ஷடங்க யோகமும்: ஒளி வாசலில் தீவந்தியை விடுத்தல்: அம்ருதநாத உபநிடதம்",
        "characters": "The Wise Seeker Who Leaves Behind Mere Textual Study, The Master of Shadanga Yoga (Pratyahara, Dharana, Pranayama, Dhyana, Tarka, Samadhi)",
        "verse_sanskrit": "ओङ्कारं रथमारुह्य विष्णुं कृत्वा तु सारथिम् । ब्रह्मलोकपदान्वेषी रुद्राराधनतत्परः ॥ प्रत्याहारस्तथा ध्यानं प्राणायामोऽथ धारणा । तर्कश्चैव समाधिश्च षडङ्गो योग उच्यते ॥",
        "verse_tamil_translit": "ஓங்காரம் ரதமாருஹ்ய விஷ்ணும் க்ருத்வா து ஸாரதிம் | ப்ரஹ்மலோகபதான்வேஷீ ருத்ராராதனதத்பர: ||",
        "verse_meaning_english": "Mounting the chariot of Omkara and making Lord Vishnu the charioteer, the seeker of the Supreme Abode of Brahman, devoted to the worship of Rudra, travels as far as the chariot goes—and then, abandoning the chariot itself, enters the Infinite! Pratyahara, Dhyana, Pranayama, Dharana, Tarka, and Samadhi—this is called Six-Limbed Yoga!",
        "verse_meaning_tamil": "ஓங்காரம் எனும் தேரில் ஏறி, மகாவிஷ்ணுவைத் தேரோட்டியாகக் கொண்டு, ருத்ர ஆராதனையில் நிலைபெற்று பிரம்மலோகத்தை நாடும் யோகி, தேர் செல்லும் தூரம் வரை பயணித்து, பின் தேரையும் விடுத்து எல்லையற்ற பரம்பொருளில் புகுகிறான்! பிரத்யாஹாரம், தியானம், பிராணாயாமம், தாரணை, தர்க்கம், சமாதி ஆகிய ஆறும் ஷடங்க யோகம் எனப்படும்!",
        "theme": "Walking with a torch at night only to lay down the torch once the treasure is found; riding the Chariot of Omkara with Vishnu as charioteer; the unique Shadanga Yoga (including Tarka—illuminating discriminative inquiry); and opening the sealed heart-door through Pranayama into the Akasha-Hridaya.",
        "SettingVisual": "Ancient forest pathway lit by a flaming torch at pre-dawn, opening into a sun-drenched Himalayan granite cave and lotus terrace",
        "ProtagonistVisual": "A resolute yogi carrying a flaming torch to the cave entrance, setting it down to sit in luminous six-limbed yoga",
        "GuruVisual": "Venerable Krishna Yajurvedic Yoga Master seated on a kusha mat, glowing with the five elemental colors of Prana",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Dramatic tracking shot of a seeker walking with a flaming torch through a dark forest before dawn, arriving at a sunlit cave entrance where he extinguishes the torch and bows before the Yoga Master.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic tracking shot of an ancient Indian seeker walking with a flaming wooden torch at pre-dawn toward a sunlit mountain cave; reaching the golden sunrise light, he sets down the torch and bows before a radiant Yoga Master. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's Amritanada Upanishad—the Upanishad of the Immortal Sound—the Master opens with a vivid parable: 'Just as a man searching in the dark walks with a flaming torch in hand, and upon finding the treasure sets the torch aside, so the wise seeker studies the scriptures and then lays aside mere words to enter direct Yoga!'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் அம்ருதநாத உபநிடதம் ஓர் அற்புத உவமையோடு தொடங்குகிறது: 'இருட்டில் பொருளைத் தேடுபவன் கையில் தீவந்தியுடன் சென்று, புதையலைக் கண்டவுடன் தீவந்தியைக் கீழே வைத்துவிடுவது போல, சாஸ்திரங்களை ஆராய்ந்த அறிஞன் ஏட்டுச் சுமையை விடுத்து நேரடி யோகத்தில் புகுகிறான்!'",
                "sub_cue": "As one sets down the torch after finding the treasure, transcend mere words to enter direct Yoga!",
                "sound": "Crackling torch flame fading into the clear, golden resonance of a morning temple bell and Tanpura."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Visionary shot of the yogi seated in meditation as a luminous golden chariot of Omkara rises before his inner eye, dissolving into boundless light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a meditating Indian yogi in padmasana at dawn; a subtle translucent golden chariot of Omkara light shimmers around him and dissolves into pure boundless sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then follows the famous verse of the Chariot of Omkara: 'Omkaram ratham aruhya, Vishnum kritva tu sarathim—mounting the chariot of Omkara and making Lord Vishnu the charioteer, worshipping Rudra, the seeker travels to the threshold of Brahmaloka! And where the chariot road ends, abandoning even the chariot, he steps into the trackless Infinite!'",
                "vo_ta": "அதன்பின் ஓங்காரத் தேரின் புகழ்பெற்ற சுலோகம் ஒலிக்கிறது: 'ஓங்காரம் ரதமாருஹ்ய விஷ்ணும் க்ருத்வா து ஸாரதிம் — ஓங்காரம் எனும் தேரில் ஏறி, மகாவிஷ்ணுவைச் சாரதியாகக் கொண்டு, ருத்ரனை ஆராதித்து பிரம்மலோக வாசலை அடைகிறான் யோகி! தேர் செல்லும் பாதை முடியுமிடத்தில், தேரையும் விடுத்து எல்லையற்ற பரம்பொருளில் காலடியெடுத்து வைக்கிறான்!'",
                "sub_cue": "ओङ्कारं रथमारुह्य विष्णुं कृत्वा तु सारथिम् — Mount the Chariot of Omkara with Vishnu as Charioteer!",
                "sound": "Majestic Rudra Veena and Mridangam rhythm evoking a celestial chariot, resolving into spacious flute silence."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of the Master instructing the disciple in the Six Limbs of Yoga (Shadanga Yoga) in a peaceful forest grove.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of the Yoga Master and disciple seated on kusha grass in a peaceful, flower-filled ancient Indian forest grove devoid of thorns or noise, practicing deep yogic contemplation. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Master taught the ancient Shadanga Yoga—the Six-Limbed Yoga: 'Pratyahara (sense-withdrawal), Dhyana (meditation), Pranayama (breath-mastery), Dharana (concentration), Tarka (luminous discriminative reasoning aligned with scripture), and Samadhi (union)! Looking upon the five sense-objects as pleasant mirages, withdraw the rays of the mind back into the Self!'",
                "vo_ta": "பண்டைய 'ஷடங்க யோகம்' எனும் ஆறு அங்க யோகத்தை குரு போதித்தார்: 'பிரத்யாஹாரம் (புலன் ஒடுக்கம்), தியானம், பிராணாயாமம், தாரணை, தர்க்கம் (வேதத்திற்கு முரணில்லாத ஞான விசாரம்), மற்றும் சமாதி! ஐம்புல நுகர்ச்சிகளைக் கானல் நீராகக் கண்டு, மனக் கதிர்களை ஆத்மாவிற்குள் மீட்டுக்கொள்வாயாக!'",
                "sub_cue": "Six-Limbed Yoga (Shadanga): Pratyahara, Dhyana, Pranayama, Dharana, Tarka, and Samadhi.",
                "sound": "Six-beat Rupaka Tala pulse on Pakhawaj with a serene Saraswati Veena melody."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of a goldsmith's crucible where gold ore is heated in fire until all dross burns away and pure gold shines, cross-dissolving to the yogi performing Rechaka, Puraka, and Kumbhaka.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of molten pure gold glowing inside an ancient clay crucible over glowing coals, transitioning to a yogi in padmasana performing pranayama with a golden aura purifying his nadis. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Just as mountain ore smelted in fire casts off all impurity and shines as pure gold, so the yogi burns away the defects of the senses through Pranayama! Through Rechaka, Puraka, and Kumbhaka, contemplating the Gayatri with Vyahrities and Shirah in a single breath, he purifies the five elemental pranas—ruby-red Prana, crystal Apana, dark-blue Vyana, golden Samana, and milk-white Udana!",
                "vo_ta": "நெருப்பில் உருக்கப்படும் தாதுத் தன் மாசுகளை நீக்கித் தங்கமாக ஒளிர்வது போல, பிராணாயாமத்தால் யோகி புலன் தோஷங்களைச் சுட்டெரிக்கிறான்! ரேசகம், பூரகம், கும்பகம் வழியே பவள நிற பிராணன், படிக நிற அபானன், நீல நிற வியானன், பொன்னிற சமானன், பால் வெண்மை உதானன் ஆகிய பஞ்ச வாயுக்களையும் அவன் தூய்மையாக்குகிறான்!",
                "sub_cue": "As fire purifies gold ore of all dross, Pranayama purifies the senses and the five Pranas.",
                "sound": "Deep, rhythmic pranayama breath cycles accompanied by harmonic chimes."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic zoom into the yogi's heart-gate and crown-gate (Brahmarandhra) as the upward Udana breath opens the portal of Akasha-Hridaya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of an illumined Indian yogi in samadhi; a vertical column of milk-white and golden prana light rises from his heart through the crown portal (Brahmarandhra) into boundless light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Blocking the lower gates of mortality and opening the sealed portal of the heart, the yogi pierces the crown center—the Brahmarandhra! Chanting the immortal Nada of Omkara without movement of tongue or palate, he enters the fearless Akasha-Hridaya—the Sky of the Heart where there is no return!",
                "vo_ta": "கீழ் வாசல்களை அடைத்து இதயத்தின் முத்திரையிடப்பட்ட வாயிலைத் திறந்து, சிரசின் உச்சியிலுள்ள பிரம்மரந்திரத்தை யோகி ஊடுருவுகிறான்! நாவும் அண்ணமும் அசையாத உள் அமிர்த நாதத்தால், மறுபிறப்பற்ற அச்சமில்லாத இதய ஆகாயத்தில் (ஆகாச ஹ்ருதயம்) அவன் பிரவேசிக்கிறான்!",
                "sub_cue": "Opening the portal of the heart and piercing the Brahmarandhra, the Yogi enters the Immortal Sky!",
                "sound": "Soaring Amritanada Omkara resonance and triumphant conch shell."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogi seated in luminous stillness at the mountain summit, one with the Immortal Sound.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the awakened yogi seated in padmasana on a sunlit mountain peak, radiating golden-white peace across the sky and valley. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Having attained the state of the Immortal Sound—Amritanada—all doubts vanish, all karmic seeds are roasted, and the yogi abides forever in the supreme peace of Brahman.",
                "vo_ta": "அம்ருதநாத நிலையை அடைந்த யோகியின் சகல ஐயங்களும் நீங்கி, கர்ம விதைகள் வறுபட்டு, பரப்பிரம்மத்தின் பேரமைதியில் அவர் என்றென்றும் நிலைபெறுகிறார்.",
                "sub_cue": "In the state of Amritanada, all karmic seeds are roasted and the Yogi abides in Immortal Peace.",
                "sound": "Serene Bansuri and Tanpura sustain in Raga Amritavarshini."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the sunlit cave and forest grove.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian mountain cave and sunlit forest grove at dawn. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Amritanada Upanishad: mount the chariot of Omkara, purify your breath with the fire of Yoga, and step into the Immortal Light within your own heart. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு அம்ருதநாத உபநிடதம் நிறைவுறுகிறது: ஓங்காரத் தேரில் ஏறி, யோகத் தீயால் பிராணனைத் தூய்மையாக்கி, நம் இதயத்து அமிர்த ஒளியில் காலடியெடுத்து வைப்போமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Mount the Chariot of Omkara; step into the Immortal Light of the Heart. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into peaceful mountain wind."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 24 (YOGA 5). KSHURIKA UPANISHAD (#31)
    {
        "story_id": "YOGA_05_KSHURIKA",
        "muktika_number": 31,
        "name_sanskrit": "क्षुरिकोपनिषद्",
        "name_iast": "Kṣurikopaniṣad",
        "name_tamil": "க்ஷுரிகா உபநிடதம்",
        "name_english": "Kshurika Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Razor-Blade of Dharana: Severing the 72,000 Cords of Karmic Bondage",
        "story_title_tamil": "தாரணை எனும் கூரிய கத்தி: 72,000 கர்மக் கயிறுகளை அறுக்கும் யோகம்: க்ஷுரிகா உபநிடதம்",
        "characters": "The Master of Kshurika-Dharana, The Resolute Yogi Performing Marmasthana Prana-Retention, The Spider Climbing its Single Thread",
        "verse_sanskrit": "मनसश्चन्द्रमा जातः चक्षुषः सूर्य उच्यते । तयोर्मध्ये तु या नाडी सुषुम्ना नाम विश्रुता ॥ तां छित्त्वा क्षुरिकाध्यानैर्न भूयः संसरिष्यति ॥",
        "verse_tamil_translit": "மனஸஸ்சந்த்ரமா ஜாத: சக்ஷுஷ: ஸூர்ய உச்யதே | தாம் சித்வா க்ஷுரிகாத்யானைர் ந பூய: ஸம்ஸரிஷ்யதி ||",
        "verse_meaning_english": "Surrounding the central white Sushumna channel are seventy-two thousand nadis; severing all karmic bonds across them with the razor-blade of Dharana and Pranayama, the yogi never returns to samsara!",
        "verse_meaning_tamil": "வெண்ணிற சுஷும்னா நாடியைச் சூழ்ந்து எழுபத்திரண்டாயிரம் நாடிகள் உள்ளன; தாரணை மற்றும் பிராணாயாமம் எனும் கூரிய கத்தியால் கர்மக் கயிறுகள் அனைத்தையும் அறுத்தெறியும் யோகி, மீண்டும் சம்சாரத்தில் பிறப்பதில்லை!",
        "theme": "The surgical precision of Yoga: sharpening the razor-blade of Manas on the whetstone of Vairagya, ascending step-by-step from the big toes through the ankles, shins, knees, thighs, and navel into the 101 heart nadis, and climbing the single white thread of Sushumna like a spider into Moksha.",
        "SettingVisual": "Quiet rock-walled meditation sanctuary at dawn with a glowing oil lamp and a spider spinning a single luminous silk thread",
        "ProtagonistVisual": "A focused yogi seated in Siddhasana/Padmasana with eyes fixed on the vital marma points of the body",
        "GuruVisual": "Venerable Krishna Yajurvedic Yoga Acharya demonstrating the razor-sharp focus of Dharana",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly shot into a quiet stone meditation cell at dawn where a yogi sits before his Guru, asking for the surgical method to sever subtle karmic attachments.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot into a quiet ancient Indian stone meditation sanctuary at golden dawn. A focused yogi bows before a venerable Yoga Acharya seated on a white cotton mat beside a single brass oil lamp. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's Kshurika Upanishad—the Upanishad of the Razor's Edge—the Master reveals the surgical Yoga of Dharana. The disciple asked: 'O Bhagavan! How can the yogi sever the subtle cords that tie the vital breath to this mortal body and prevent rebirth forever?'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் க்ஷுரிகா உபநிடதத்தில்—கூரிய கத்தியின் உபநிடதத்தில்—தாரணை யோகத்தின் நுட்பத்தை குரு வெளியிடுகிறார். சீடன் கேட்டான்: 'பகவானே! பிராணனை இவ்வுடலோடு பிணித்திருக்கும் சூட்சுமக் கயிறுகளை அறுத்து, மறுபிறவியைத் தடுப்பது எவ்வாறு?'",
                "sub_cue": "How does the Yogi sever the subtle cords binding Prana to the mortal body?",
                "sound": "Pin-drop cave silence broken by a single crystalline bronze chime and deep Tanpura drone."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of the yogi assuming a rock-steady posture in a noiseless spot, withdrawing his senses like a tortoise drawing its limbs inside its shell.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi seated in rock-steady padmasana in a serene stone chamber at dawn, beside a peaceful tortoise resting on a mossy stone, symbolizing total sense-withdrawal. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "The Master instructed: 'Choosing a noiseless seat, sitting in Padmasana or Svastikasana, withdraw all senses into the heart just as a tortoise draws in its limbs! Filling the body with Prana through twelve matras and retaining it in Kumbhaka, sharpen the razor-blade of the mind upon the whetstone of dispassion!'",
                "vo_ta": "குரு உபதேசித்தார்: 'சத்தமில்லாத இடத்தில் பத்மாசனத்தில் அமர்ந்து, ஆமை தன் உறுப்புகளை உள்ளிழுப்பது போல் புலன்களை இதயத்தில் ஒடுக்குக! பன்னிரண்டு மாத்திரை அளவு பிராணனைப் பூரித்துக் கும்பகத்தில் நிறுத்தி, வைராக்கியம் எனும் சாணைக்கல்லில் மனம் எனும் கத்தியைத் தீட்டுவாயாக!'",
                "sub_cue": "Sharpen the razor-blade of the mind upon the whetstone of Vairagya!",
                "sound": "Rhythmic 12-beat pranayama count on soft mridangam with a focused Rudra Veena line."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Slow vertical camera tilt up the yogi's body from the big toes, ankles, shins, knees, and thighs to the navel, as a sharp golden blade of Prana-light severs the knots at each marma joint.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps vertical tilt shot of a meditating Indian yogi in padmasana; a luminous golden beam of prana light ascends step-by-step from his toes, ankles, knees, and thighs up to the navel, dissolving dark energetic knots at each joint. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then begins the step-by-step Kshurika meditation: fixing the breath and mind on the big toes, ankles, shins, knees, thighs, base, and navel, the yogi applies the red-hot razor of Dharana and Pranayama! One by one, he severs attachment to the lower vital junctions without injury or doubt, drawing all life-force upward!",
                "vo_ta": "அதன்பின் படிப்படியான க்ஷுரிகா தாரணை தொடங்குகிறது: கால் பெருவிரல், கணுக்கால், முழங்கால், தொடை, மூலம் மற்றும் நாபி ஆகிய மர்ம ஸ்தானங்களில் பிராணனையும் மனதையும் நிறுத்தி, தாரணை எனும் கூரிய கத்தியால் கீழ் நிலைப் பற்று முடிச்சுகளை ஒவ்வொன்றாக அறுத்து பிராணனை மேலேற்றுகிறான் யோகி!",
                "sub_cue": "Step by step from toes to navel, the razor of Dharana severs attachment to the mortal limbs.",
                "sound": "Ascending scale on the Saraswati Veena with crisp, decisive metallic overtones at each marma point."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Macro shot of a tiny spider climbing upward along a single gleaming white silk thread toward the sunlight, dissolving into the yogi's Prana rising along the pure white Sushumna nadi.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps macro-to-medium shot of a tiny spider ascending a single gleaming white silk thread in a sunbeam, transitioning to a meditating yogi whose prana rises along a single pure white Sushumna channel in the spine. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Entering the region of the heart where one hundred and one main nadis branch into seventy-two thousand channels, the yogi beholds the central Sushumna—pure and white as a lotus fiber! Just as a spider leaves its complex web and climbs a single thread into open space, the yogi severs the seventy-two thousand side-cords with the razor of wisdom and ascends through Sushumna alone!",
                "vo_ta": "எழுபத்திரண்டாயிரம் நாடிகள் பிரியும் இதயப் பகுதியில், தாமரை நூல் போல் வெண்மையான சுஷும்னா நாடியை யோகி காண்கிறான்! சிலந்தி தன் சிக்கலான வலையை விட்டுவிட்டு ஒரே நூல் வழியே ஆகாயத்தில் ஏறுவது போல, ஞானக் கத்தியால் பக்க நாடிகளின் பற்றை அறுத்து சுஷும்னா வழியாக மட்டுமே யோகி மேலேறுகிறான்!",
                "sub_cue": "Like a spider climbing a single thread, sever the 72,000 cords and ascend through white Sushumna!",
                "sound": "High, delicate Bansuri and Violin unison climbing steadily into the upper octave."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi's throat and crown as a blindingly pure flash of golden-white light severs the final knot of vasana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of the meditating yogi as a brilliant golden-white flash of prana light rises through his throat into the crown chakra, dissolving all shadows into pure radiance. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Severing all subtle vasanas of good and evil with the diamond-sharp Kshurika of concentration, the yogi merges Prana into the Supreme Imperishable at the crown! Just as a severed cord can never bind again, his samsaric bondage is cut forever!",
                "vo_ta": "புண்ணிய-பாவ வாசனைகள் அனைத்தையும் தாரணை எனும் வைரக் கத்தியால் அறுத்தெறிந்து, சிரசின் உச்சியில் அழிவற்ற பரம்பொருளில் பிராணனை ஒடுக்குகிறான் யோகி! அறுபட்ட கயிறு மீண்டும் கட்ட முடியாதது போல, அவனது சம்சார பந்தம் நிரந்தரமாக அறுபடுகிறது!",
                "sub_cue": "तां छित्त्वा क्षुरिकाध्यानैर्न भूयः संसरिष्यति — Severing all bonds with Kshurika-Dhyana, he never returns!",
                "sound": "Resonant conch shell blast and crystalline bell chime."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogi seated in luminous stillness as the stone walls of the sanctuary seem to dissolve into golden morning sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the illumined yogi seated in padmasana inside the sunlit stone sanctuary, golden light filling the chamber with boundless peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Freed from all knots of the nadis, abiding in the spotless sky of the Supreme Self, he attains immediate liberation and timeless immortality.",
                "vo_ta": "நாடி முடிச்சுகள் அனைத்திலிருந்தும் விடுபட்டு, பரமாத்மாவின் களங்கமற்ற ஆகாயத்தில் நிலைபெற்று, அவர் உடனடி முக்தியையும் அமரத்துவத்தையும் அடைகிறார்.",
                "sub_cue": "Freed from all knots of the nadis, the Yogi abides in spotless Immortality.",
                "sound": "Spacious Tanpura and harmonic singing bowls."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back from the stone meditation sanctuary into the sunlit forest at dawn.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian stone meditation sanctuary and sunlit forest at dawn. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Kshurika Upanishad: sharpen your awareness with dispassion, cut through the web of distraction, and ascend the single luminous thread of Truth. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு க்ஷுரிகா உபநிடதம் நிறைவுறுகிறது: வைராக்கியத்தால் விழிப்புணர்வைக் கூர்மையாக்கி, மனச்சிதறல் வலையை அறுத்து, சத்தியத்தின் ஒற்றை ஒளி நூல் வழியே உயர்வோமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Cut through the web of distraction with the razor of Dharana. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into serene morning air."
            }
        ]
    },
    # 25 (YOGA 6). TEJOBINDU UPANISHAD (#37)
    {
        "story_id": "YOGA_06_TEJOBINDU",
        "muktika_number": 37,
        "name_sanskrit": "तेजोबिन्दूपनिषद्",
        "name_iast": "Tejobindūpaniṣad",
        "name_tamil": "தேஜோபிந்து உபநிடதம்",
        "name_english": "Tejobindu Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Blazing Point of Light & 15-Limbed Raja Yoga: Shiva to Kumara & Ribhu to Nidagha",
        "story_title_tamil": "தேஜோபிந்து தியானமும் 15-அங்க ராஜயோகமும்: குமாரருக்கு சிவனும் நிதாகருக்கு ரிபுவும் அருளியது",
        "characters": "Lord Paramashiva (The Supreme Guru), Kumara Kartikeya (Skanda, The Celestial Seeker), Maharishi Ribhu & Disciple Nidagha",
        "verse_sanskrit": "तेजोबिन्दुः परं ध्यानं विश्वात्मा हृदि संस्थितः । चिन्मात्रोऽहं सदाशिवो नित्यशुद्धो निरञ्जनः ॥",
        "verse_tamil_translit": "தேஜோபிந்து: பரம் த்யானம் விஸ்வாத்மா ஹ்ருதி ஸம்ஸ்தித: | சின்மாத்ரோஹம் ஸதாஷிவோ நித்யஷுத்தோ நிரஞ்ஜன: ||",
        "verse_meaning_english": "Supreme meditation is upon the Tejobindu—the blazing point of Light that is the Soul of the Universe seated within the heart! 'I am Pure Consciousness alone (Chinmatra), I am Sadashiva, eternally pure and spotless!'",
        "verse_meaning_tamil": "இதயத்தில் உறையும் பிரபஞ்ச ஆத்மாவான 'தேஜோபிந்து'—பேரொளிப் புள்ளியின் மீதான தியானமே பரம தியானமாகும்! 'நான் சின்மாத்திரன்—தூய உணர்வு மட்டுமே; நித்திய பரிசுத்தமான சதாசிவனே நான்!'",
        "theme": "The grand monument of Advaita-Yoga: meditation on the subtle Tejobindu in the heart, the Fifteen-Limbed (Panchadashanga) Raja Yoga where every limb (Yama, Niyama, Tyaga, Mauna, Desha, Kala, Asana, Mulabandha, Dehasamya, Driksthiti, Pranayama, Pratyahara, Dharana, Dhyana, Samadhi) is redefined as non-dual Brahman-awareness, and Ribhu's roar of 'Chinmatroham' to Nidagha.",
        "SettingVisual": "Majestic Kailasa-Andhranagari granite temple peak and sunlit forest hermitage glowing with a blazing golden-white point of light (Tejobindu)",
        "ProtagonistVisual": "Lord Kumara (Skanda) bowing before Paramashiva, and young ascetic Nidagha bowing before Maharishi Ribhu",
        "GuruVisual": "Lord Paramashiva in luminous Dakshinamurti-Yogi form, and Maharishi Ribhu radiating golden non-dual ecstasy",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide crane shot of a high Himalayan granite peak at golden dawn where Kumara bows before Lord Paramashiva.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps majestic crane shot on a sunlit Himalayan granite peak at dawn. Youthful radiant Kumara bows with folded hands before Lord Paramashiva seated in lotus posture, a brilliant golden point of light (Tejobindu) shining at the heart center. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's monumental Tejobindu Upanishad, Kumara Kartikeya bowed before his Father, Lord Paramashiva, and asked: 'O Bhagavan! Reveal to me the supreme mystery of the Tejobindu—the blazing point of Consciousness in the heart—and the royal path of Fifteen-Limbed Yoga!'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் மகா உபநிடதமான தேஜோபிந்து உபநிடதத்தில், குமாரக் கடவுள் தன் தந்தையான பரமசிவனை வணங்கிக் கேட்டார்: 'பகவானே! இதயத்தில் ஒளிரும் தேஜோபிந்துவின் பரம ரகசியத்தையும், பதினைந்து அங்கங்கள் கொண்ட ராஜயோக நெறியையும் எனக்கு அருள்வீராக!'",
                "sub_cue": "Kumara asks Paramashiva: 'Reveal the mystery of the Tejobindu and the 15-Limbed Royal Yoga!'",
                "sound": "Deep cosmic Damaru and Shankha resonance, followed by a majestic Rudra Veena alapana in Raga Shanmukhapriya."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Extreme close-up of the meditating yogi's heart center where a microscopic, sun-bright golden-white point of light (Tejobindu) blazes beyond the three gunas.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps extreme close-up shot of an ancient Indian yogi in deep samadhi; within his heart lotus shines a microscopic yet blindingly radiant golden-white point of light (Tejobindu) illuminating his serene face. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Shiva spoke: 'Listen, O Shadanan! Subtle, atomic, yet vaster than the cosmos is the Tejobindu seated in the heart—the seat of Shiva, peaceful, beyond speech and mind! Only the heroic seeker who has conquered greed, anger, and fear can fix his gaze upon this blazing point of Pure Consciousness!'",
                "vo_ta": "சிவபெருமான் அருளினார்: 'கேளாய் ஷண்முகா! அணுவிற்கும் அணுவாய், பிரபஞ்சத்திற்கும் பெரிதாய் இதயத்தில் ஒளிர்வதே தேஜோபிந்து—वाக்குக்கும் மனதிற்கும் எட்டாத சாந்த சிவபதம்! பேராசை, சினம், அச்சம் ஆகியவற்றை வென்ற வீர சாதகனால் மட்டுமே இந்தப் பேரொளிப் புள்ளியில் சித்தத்தை நிறுத்த முடியும்!'",
                "sub_cue": "तेजोबिन्दुः परं ध्यानं — Meditate upon the blazing Point of Light seated in the heart!",
                "sound": "High, crystalline harmonic bell and deep Tanpura fifths."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Sweeping tracking shot around fifteen glowing stone pillars in a circular mandapam, representing the Fifteen Limbs of Yoga (Panchadashanga Yoga).",
                "prompt": "16:9 widescreen 8K photorealistic 24fps sweeping tracking shot inside a circular ancient Indian granite mandapam with fifteen carved pillars glowing in golden morning sunlight around a central meditating yogi. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Lord Shiva unveiled the extraordinary Panchadashanga Yoga—the Fifteen Limbs of Advaita Yoga: Yama, Niyama, Tyaga (renunciation of world-illusion), Mauna (inner silence), Desha (solitary space of Consciousness), Kala (timeless moment), Asana, Mulabandha, Dehasamya, Driksthiti, Pranayama, Pratyahara, Dharana, Dhyana, and Samadhi!",
                "vo_ta": "அதன்பின் பதினைந்து அங்கங்கள் கொண்ட அத்வைத யோகத்தை (பஞ்சதசாங்க யோகம்) ஈசன் வெளியிட்டார்: இயமம், நியமம், தியாகம் (பிரபஞ்ச மாயையைத் துறத்தல்), மௌனம், தேசம், காலம், ஆசனம், மூலபந்தம், தேகசாம்யம், த்ருக்ஸ்திதி, பிராணாயாமம், பிரத்யாஹாரம், தாரணை, தியானம் மற்றும் சமாதி!",
                "sub_cue": "15-Limbed Advaita Yoga: every limb is redefined as non-dual awareness of Brahman!",
                "sound": "Rhythmic 15-beat tala cycle on Mridangam with soaring Bansuri melody."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Medium shot of the yogi practicing Advaita-Pranayama: exhaling the illusion of the world (Rechaka), inhaling 'I am Brahman' (Puraka), and retaining that non-dual certainty (Kumbhaka).",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a radiant Indian yogi seated on a granite ledge at sunrise, inhaling golden cosmic light into his heart and exhaling dark mist, abiding in motionless Kumbhaka. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "What is true Asana? That posture in which one effortlessly contemplates Brahman! What is true Pranayama? Negating the illusion of the world is Rechaka—exhalation! The conviction 'I am Brahman alone' is Puraka—inhalation! And holding that non-dual certainty without wavering is the true Kumbhaka of the wise!",
                "vo_ta": "உண்மையான ஆசனம் எது? எதில் அமர்ந்து பிரம்மத்தைச் சுகமாகத் தியானிக்க முடியுமோ அதுவே! உண்மையான பிராணாயாமம் எது? உலகம் மித்தை எனத் தள்ளுவதே ரேசகம் (மூச்சு விடுதல்)! 'நானே பிரம்மம்' என்ற எண்ணமே பூரகம் (மூச்சு வாங்குதல்)! அந்த விருத்தி அசையாமல் நிலைத்திருப்பதே ஞானிகளின் உண்மையான கும்பகம்!",
                "sub_cue": "Negating illusion is Rechaka; 'I am Brahman' is Puraka; steady abidance is true Kumbhaka!",
                "sound": "Deep yogic breath fused with Saraswati Veena and Violin harmonies."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Transition to Maharishi Ribhu instructing Nidagha in a sunlit forest clearing, both glowing with the ecstatic roar of 'Chinmatroham' (I am Pure Consciousness alone).",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic cinematic shot of Maharishi Ribhu and disciple Nidagha in a sunlit forest clearing; Ribhu raises his hand in fearless realization as golden light blazes from both sages. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the second half of the Upanishad, Maharishi Ribhu thunders the pinnacle of realization to his disciple Nidagha: 'Chinmatroham Sadashivo! Everything that appears is Chinmatra—Pure Consciousness alone! There is no dualistic world, no separate mind, no sorrow—I am the indivisible, self-luminous Atman!'",
                "vo_ta": "உபநிடதத்தின் பிற்பகுதியில், ரிபு மகரிஷி தன் சீடர் நிதாகருக்கு அத்வைத சிகரத்தை முழங்குகிறார்: 'சின்மாத்ரோஹம் ஸதாஷிவ:! காணப்படும் அனைத்தும் சின்மாத்திரம்—தூய உணர்வு மட்டுமே! இரண்டாவது பொருள் ஏதுமில்லை, தனி மனமில்லை, சோகமில்லை—நானே சுயம்பிரகாசமான அகண்ட ஆத்மா!'",
                "sub_cue": "चिन्मात्रोऽहं सदाशिवः — I am Pure Consciousness alone, the spotless Sadashiva!",
                "sound": "Thunderous Vedic choral chant of 'Chinmatroham Sadashivah' with conch and temple bells."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide cosmic shot of the mountain peak and forest dissolving into one seamless ocean of golden-white Tejobindu light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cosmic shot of the Himalayan peak and forest bathed in an ocean of golden-white Tejobindu radiance, where the meditating yogi and the universe shine as one seamless consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "When the mind forgets all vasanas and becomes one with Brahman, that is true Samadhi! In that fullness, the seeker, the path, and the goal merge into the One Eternal Light.",
                "vo_ta": "வாசனைகள் அனைத்தும் மறந்து மனம் பிரம்மமாகவே மாறிவிடும் நிலையே உண்மையான சமாதி! அந்தப் பூரணத்தில் தேடுபவன், பாதை, இலக்கு ஆகிய மூன்றும் ஒரே நித்தியப் பேரொளியில் ஒன்றிவிடுகின்றன.",
                "sub_cue": "Seeker, Path, and Goal merge into the One Eternal Tejobindu!",
                "sound": "Expansive, celestial Santoor and Tanpura sustain."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the golden Himalayan summit at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the golden Himalayan summit at sunrise where Paramashiva and Kumara sit in eternal stillness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Tejobindu Upanishad: inhale the truth 'I am Brahman,' exhale all fear and limitation, and shine as the blazing point of Pure Consciousness. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு தேஜோபிந்து உபநிடதம் நிறைவுறுகிறது: 'நானே பிரம்மம்' என்ற சத்தியத்தை உள்வாங்கி, அச்சத்தையும் எல்லையையும் வெளிவிட்டு, தூய உணர்வின் பேரொளிப் புள்ளியாகப் பிரகாசிப்போமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Inhale 'I am Brahman'; shine as the blazing Point of Pure Consciousness. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into serene mountain wind."
            }
        ]
    },
    # 26 (YOGA 7). NADABINDU UPANISHAD (#38)
    {
        "story_id": "YOGA_07_NADABINDU",
        "muktika_number": 38,
        "name_sanskrit": "नादबिन्दूपनिषद्",
        "name_iast": "Nādabindūpaniṣad",
        "name_tamil": "நாதபிந்து உபநிடதம்",
        "name_english": "Nadabindu Upanishad",
        "veda": "Rig Veda",
        "category": "Yoga",
        "story_title_english": "The Hamsa Bird of Omkara & The Honeybee of Nada-Anusandhana",
        "story_title_tamil": "ஓங்கார ஹம்ஸப் பறவையும் நாதானுசந்தான வண்டும்: நாதபிந்து உபநிடதம்",
        "characters": "The Rigvedic Nada-Yogi Practicing Siddhasana & Vaishnavi Mudra, The Cosmic Hamsa Bird of Pranava, The Honeybee of the Mind",
        "verse_sanskrit": "अकारो दक्षिणः पक्ष उकारस्तूत्तरः स्मृतः । मकारं पुच्छमित्याहुर्अर्धमात्रा तु मस्तकम् ॥ मकरन्दं पिबन् भृङ्गो गन्धान् नापेक्षते यथा । नादासक्तं तथा चित्तं विषयान् न हि काङ्क्षति ॥",
        "verse_tamil_translit": "அகாரோ தக்ஷிண: பக்ஷ உகாரஸ்தூத்தர: ஸ்ம்ருத: | மகரந்தம் பிபன் ப்ருங்கோ கந்தான் நாபேக்ஷதே யதா | நாதாஸக்தம் ததா சித்தம் விஷயான் ந ஹி காங்க்ஷதி ||",
        "verse_meaning_english": " Of the Hamsa bird of Omkara, A-kara is the right wing, U-kara is the left wing, Ma-kara is the tail, and Ardhamatra is the head! Just as a bee drinking the nectar of a flower no longer cares for external scents, the mind absorbed in inner Nada never craves sense-objects!",
        "verse_meaning_tamil": "ஓங்கார ஹம்ஸப் பறவையின் வலது சிறகு அகாரம், இடது சிறகு உகாரம், வால் பகுதி மகாரம், சிரசு அர்த்தமாத்திரை! மலரின் தேனைப் பருகும் வண்டு பிற வாசனைகளை நாடாதது போல, உள் நாதத்தில் லயித்த சித்தம் உலக விஷயங்களை ஒருபோதும் விரும்புவதில்லை!",
        "theme": "The supreme Rigvedic treatise on Nada-Yoga: visualizing Omkara as the cosmic Hamsa bird, burning Prarabdha karma through the twelve matras of Pranava, practicing Siddhasana with Vaishnavi Mudra, and absorbing the mind like a nectar-drinking bee or a charmed deer into the inner Anahata Nada until it dissolves into Soundless Parabrahman.",
        "SettingVisual": "Sunlit Rigvedic mountain cave overlooking a lotus valley with honeybees, spotted deer, and a soaring white swan in the golden sky",
        "ProtagonistVisual": "A serene Nada-Yogi seated in Siddhasana with eyes half-open in Vaishnavi Mudra, listening inwardly to the cosmic sound",
        "GuruVisual": "Venerable Rigvedic Acharya of Nada-Yoga seated beside a Rudra Veena and glowing brass lamp",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide shot of a white swan soaring across a golden sunrise sky above a Rigvedic mountain hermitage, gliding down to a yogi seated before his Guru.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide cinematic shot of a pure white swan soaring across a golden sunrise sky above an ancient Indian mountain hermitage, where a disciple bows before a venerable Rigvedic Yoga Acharya. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Rig Veda's Nadabindu Upanishad—the Upanishad of the Sound-Seed of Immortality—the Master reveals how the sacred syllable Om becomes a living bird of light that carries the yogi beyond karma into the Soundless Absolute.",
                "vo_ta": "ரிக் வேதத்தின் நாதபிந்து உபநிடதத்தில், பிரணவ மந்திரமான 'ஓம்' எவ்வாறு ஒளிமயமான அன்னப் பறவையாக மாறி, யோகியை கர்ம பந்தங்களுக்கு அப்பால் உள்ள நிசப்தப் பரம்பொருளுக்கு அழைத்துச் செல்கிறது என்பதை குரு விளக்குகிறார்.",
                "sub_cue": "How does Omkara carry the Yogi beyond karma into the Soundless Absolute?",
                "sound": "Soaring wingbeats, morning temple bell, and a pure Tanpura and Bansuri introduction."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Luminous spiritual visualization of the Hamsa Bird of Omkara hovering above the meditating yogi's heart: right wing A-kara, left wing U-kara, tail Ma-kara, head Ardhamatra.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of a meditating Indian yogi in padmasana; above his heart shimmers a translucent golden-white swan of prana light whose wings, tail, and head glow with sacred radiance. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Behold the anatomy of the Omkara-Hamsa: 'A-kara is its right wing, U-kara is its left wing, Ma-kara is its tail, and the subtle Ardhamatra is its head! Its legs are the gunas, its body is Tattva, its right eye is Dharma, and its left eye is Jnana! Riding this Hamsa bird of twelve matras, the yogi burns away even past karmic impressions!'",
                "vo_ta": "ஓங்கார ஹம்ஸத்தின் திருவுருவத்தைக் காணீர்: 'அகாரம் அதன் வலது சிறகு, உகாரம் இடது சிறகு, மகாரம் அதன் வால், சூட்சுமமான அர்த்தமாத்திரையே அதன் சிரசு! தர்மமும் ஞானமும் அதன் இரு கண்கள்! பன்னிரண்டு மாத்திரைகள் கொண்ட இந்த ஓங்கார அன்னத்தின் மீது ஏறும் யோகி, பழைய கர்ம வாசனைகளையும் சுட்டெரிக்கிறான்!'",
                "sub_cue": "अकारो दक्षिणः पक्ष उकारस्तूत्तरः स्मृतः — A-kara is the right wing, U-kara the left, Ardhamatra the head of the Hamsa!",
                "sound": "Twelve-beat resonant Omkara chant layered with Saraswati Veena arpeggios."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Close-up of the yogi seated in Siddhasana with the three bandhas and Vaishnavi Mudra (eyes open without blinking, gaze directed inward), listening to the right ear's inner sound.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi seated in Siddhasana inside a stone cave; his eyes are serenely half-open in Vaishnavi mudra while golden ripples of inner sound glow softly around his right ear and crown. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then the Master taught the practice of Nada-Anusandhana: 'Sitting in Siddhasana and practicing Vaishnavi Mudra—where the eyes remain gently open while the gaze is fixed entirely within—listen continuously to the unstruck Nada in the right ear! First it roars like the ocean, thundercloud, and waterfall; then it refines into the mridanga, bell, conch, flute, veena, and humming bee!'",
                "vo_ta": "அதன்பின் நாதானுசந்தான முறையை குரு போதித்தார்: 'சித்தாசனத்தில் அமர்ந்து, கண்கள் திறந்திருந்தாலும் பார்வை உள்முகமாக நிலைத்திருக்கும் வைஷ்ணவி முத்திரையில், வலது காதில் ஒலிக்கும் அனாஹத நாதத்தைக் கேட்பாயாக! முதலில் கடல் மற்றும் மேக முழக்கம் போலத் தொடங்கும் அவ்வொலி, மெல்ல மிருதங்கம், மணி, சங்கு, குழல், வீணை மற்றும் வண்டின் ரீங்காரமாக நுட்பமடையும்!'",
                "sub_cue": "In Siddhasana and Vaishnavi Mudra, listen as ocean-roar refines into flute, veena, and humming bee!",
                "sound": "Acoustic transition from ocean waves and thunder to bell, flute, veena, and a sweet, subtle bee-hum."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Poetic nature metaphors: (1) a honeybee absorbed in drinking lotus nectar, (2) a spotted deer standing entranced by flute music, and (3) a cobra swaying motionless to a reed pipe.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a golden honeybee drinking nectar deep inside a blooming pink lotus flower at dawn while a spotted deer stands utterly still in the sunlit forest background, entranced by sacred flute music. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Listen to the golden metaphors of the Nadabindu: 'Just as a bee drinking the sweet nectar of a lotus no longer wanders after outer scents, the mind absorbed in inner Nada never craves worldly sense-objects! Like a wild elephant tamed by the goad of Nada, like a bird whose wings are clipped, or like a deer spellbound by music, the restless mind becomes utterly still!'",
                "vo_ta": "நாதபிந்துவின் பொன்னான உவமைகளைக் கேளீர்: 'தாமரைத் தேனைப் பருகும் வண்டு பிற வாசனைகளைத் தேடாதது போல, உள் நாதத்தில் லயித்த மனம் உலக போகங்களை ஒருபோதும் நாடுவதில்லை! அங்குசத்தால் அடக்கப்பட்ட மதயானை போலவும், இசையில் மயங்கி நிற்கும் மான் போலவும் அலைபாயும் மனம் நாதத்தில் முழுமையாக அடங்குகிறது!'",
                "sub_cue": "मकरन्दं पिबन् भृङ्गो — Like a bee drinking nectar, the mind absorbed in Nada craves no outer object!",
                "sound": "Enchanting Bansuri solo in Raga Madhuvanti with soft bee-like Tanpura resonance."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Macro shot of a camphor flame burning down the last piece of dry wood and then extinguishing itself into clear space, dissolving to the yogi in Unmani Samadhi.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps macro-to-close-up shot of a sacred fire consuming a sandalwood stick and vanishing into pure clear air, transitioning to the yogi in Unmani Samadhi glowing with soundless golden light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Just as fire burning dry wood dies down of itself when the fuel is consumed, so the mind, absorbed in Nada, dissolves along with Prana! Transcending even the subtle sound, the yogi enters Unmani—where the Soundless Parabrahman shines alone!",
                "vo_ta": "விறகை எரிக்கும் நெருப்பு விறகு தீர்ந்ததும் தானும் அடங்கிவிடுவது போல, நாதத்தில் லயித்த மனம் பிராணனோடு சேர்ந்து கரைந்து போகிறது! சூட்சும நாதத்தையும் கடந்து 'உன்மனி' நிலையை அடையும் யோகி, நிசப்தப் பரப்பிரம்மமாகவே ஒளிர்கிறார்!",
                "sub_cue": "As fire subsides when fuel is consumed, the mind absorbed in Nada dissolves into Soundless Parabrahman!",
                "sound": "Gradual fade of all musical instruments into a single, crystalline high harmonic and profound silence."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogi seated like a motionless statue in the sunlit cave, untouched by heat, cold, joy, or sorrow.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the illumined Nada-Yogi seated in motionless samadhi on a sunlit mountain ledge, radiating serene golden light across the valley. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Freed from all states and all thoughts, his body still as wood yet his awareness vast as the cosmos, the yogi abides in the supreme Vishnu-pada—the immortal abode of Brahman.",
                "vo_ta": "அவஸ்தைகள் அனைத்தும் நீங்கி, எண்ணங்களற்று, பிரபஞ்சமளாவிய தூய உணர்வாய், அமரத்துவமான விஷ்ணு பதத்தில்—பரப்பிரம்ம நிலையில் யோகி நிலைபெறுகிறார்.",
                "sub_cue": "Freed from all thoughts, the Nada-Yogi abides in the immortal Vishnu-Pada.",
                "sound": "Spacious, ethereal Tanpura and singing bowl resonance."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the lotus valley and mountain hermitage as the white swan soars into the golden sun.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the sunlit lotus valley and mountain cave as a white swan soars toward the golden morning sun. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Nadabindu Upanishad: let the honeybee of your mind drink the inner nectar of Nada until sound itself dissolves into the boundless silence of the Self. Om Vang Me Manasi Pratishthita... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு நாதபிந்து உபநிடதம் நிறைவுறுகிறது: நம் மனம் எனும் வண்டு உள் நாதத் தேனைப் பருகி, ஆத்மாவின் எல்லையற்ற மௌனப் பெருவெளியில் கரைவதாக. ஓம் வாங் மே மனஸி ப்ரதிஷ்டிதா... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Let the bee of the mind drink inner Nada and dissolve into the Silence of the Self. Om Shanti.",
                "sound": "Rigvedic Shanti Mantra 'Om Vang Me Manasi' fading into gentle wind."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 27 (YOGA 8). DHYANABINDU UPANISHAD (#39)
    {
        "story_id": "YOGA_08_DHYANABINDU",
        "muktika_number": 39,
        "name_sanskrit": "ध्यानबिन्दूपनिषद्",
        "name_iast": "Dhyānabindūpaniṣad",
        "name_tamil": "தியானபிந்து உபநிடதம்",
        "name_english": "Dhyanabindu Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Bow of Pranava & The Spider of Prana: Piercing the Target of Brahman",
        "story_title_tamil": "பிரணவ வில்லும் பிராணச் சிலந்தியும்: பிரம்ம இலக்கைத் துளைக்கும் தியானபிந்து உபநிடதம்",
        "characters": "The Master of Dhyana-Yoga, The Focused Archer-Yogi of Pranava, The Four Great Asanas (Siddha, Bhadra, Simha, Padma)",
        "verse_sanskrit": "यदि शैलसमं पापं विस्तीर्णं बहुयोजनम् । भिद्यते ध्यानयोगेन नान्यो भेदः कदाचन ॥ प्रणवो धनुः शरो ह्यात्मा ब्रह्म तल्लक्ष्यमुच्यते । अप्रमत्तेन वेद्धव्यं शरवत्तन्मयो भवेत् ॥",
        "verse_tamil_translit": "யதி ஷைலஸமம் பாபம் விஸ்தீர்ணம் பஹுயோஜனம் | பித்யதே த்யானயோகேன நான்யோ பேத: கதாசன || ப்ரணவோ தனு: ஷரோ ஹ்யாத்மா ப்ரஹ்ம தல்லக்ஷ்யமுச்யதே ||",
        "verse_meaning_english": "Even if a mountain of sin stretches across many leagues, it is shattered by Dhyana-Yoga alone, and by no other means! Pranava is the bow, the soul is the arrow, and Brahman is the target; pierce It with unwavering focus, and become one with It like the arrow!",
        "verse_meaning_tamil": "பல யோஜனை தூரம் விரிந்த மலை போன்ற பாவமாயினும், தியான யோகத்தால் மட்டுமே அது தகர்க்கப்படுகிறது; வேறு எந்த வழியாலும் அல்ல! பிரணவமே வில், ஆத்மாவே அம்பு, பிரம்மமே இலக்கு; கவனச்சிதறலின்றி அதனை எய்து, அம்பு இலக்கில் தைப்பது போல் பிரம்மத்தோடு ஒன்றாகிவிடு!",
        "theme": "Shattering mountains of karma through Dhyana-Yoga; the subtle sound-point cleaner than a lotus fiber; the archery of Pranava; the spider drawing back its web; the Four Asanas, Three Bandhas, Khechari Mudra, and turning downward the inverted lotus of the heart through Kumbhaka.",
        "SettingVisual": "Towering Himalayan granite peaks at golden dawn, with a serene stone cave where a yogi practices Padmasana and Khechari Mudra",
        "ProtagonistVisual": "An earnest Krishna Yajurvedic yogi seated in Padmasana, practising the three bandhas and inner archery of awareness",
        "GuruVisual": "Venerable Dhyana-Yoga Acharya seated beside a lotus pond, holding a delicate lotus stem fiber",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide crane shot of towering Himalayan peaks bathed in golden sunrise, gliding into a stone cave where a disciple bows before the Dhyana-Yoga Acharya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of towering Himalayan granite mountains at golden dawn, moving into a serene stone cave where a yogi bows with folded hands before a luminous Acharya. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's Dhyanabindu Upanishad, the Master opens with a thunderous assurance of hope: 'Even if a seeker's past sins stand like a mountain range stretching across many leagues, they are shattered to dust by Dhyana-Yoga alone—and by no other means whatsoever!'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் தியானபிந்து உபநிடதத்தில், குரு நம்பிக்கையூட்டும் சிம்மநாதத்துடன் தொடங்குகிறார்: 'பல யோஜனை தூரம் விரிந்த மலைத்தொடர் போன்ற பாவக் குவியலாயினும், தியான யோகத்தால் மட்டுமே அது தூள் தூளாகத் தகர்க்கப்படுகிறது—வேறு எந்த உபாயத்தாலும் அல்ல!'",
                "sub_cue": "यदि शैलसमं पापं — Even a mountain of karma is shattered by Dhyana-Yoga alone!",
                "sound": "Deep mountain echo, temple gong strike, and a majestic Rudra Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Macro shot of the Guru splitting a delicate lotus stalk revealing a gossamer-thin white fiber inside, dissolving to a golden point of light at the crown.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps macro-to-close-up shot of a sage's fingers gently splitting a green lotus stem to reveal a gossamer-thin white fiber glistening in golden morning light, symbolizing the subtle Nada-Bindu. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Where does the highest Dhyana rest? 'Finer than the hundredth part of a lotus-stalk fiber is the subtle Bindu-Nada at the crown of Omkara! Just as fragrance is hidden inside flowers and ghee inside milk, the Lord dwells within every being as the jewel in the thread!'",
                "vo_ta": "உயர்ந்த தியானம் எங்கே நிலைபெறுகிறது? 'தாமரைத் தண்டின் நூலில் நூறில் ஒரு பங்கை விட நுட்பமானது ஓங்காரத்தின் உச்சியிலுள்ள நாத-பிந்து! மலரில் நறுமணமும் பாலில் நெய்யும் மறைந்திருப்பது போல, நூலில் கோர்க்கப்பட்ட மணியாக இறைவன் எல்லா உயிர்களிலும் உறைகிறான்!'",
                "sub_cue": "Finer than a lotus fiber is the Bindu-Nada where the Supreme Lord shines.",
                "sound": "Delicate, high-register Santoor and Violin harmonics."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Visionary shot of the yogi's awareness becoming a golden arrow fitted to the bow of Pranava, flying straight into the blazing sun of Brahman.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a meditating Indian yogi in padmasana; from his heart a luminous golden arrow of awareness launches from a bow of Omkara light straight into a blazing golden sun of Consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then the Master taught the archery of the soul: 'Pranavo dhanuh, sharo hy atma, Brahma tal-lakshyam uchyate—Pranava is the bow, the soul is the arrow, and Brahman is the supreme target! With unswerving focus, pierce that target and become one with It as the arrow merges into the mark!'",
                "vo_ta": "அதன்பின் ஆத்ம வில்வித்தையை குரு போதித்தார்: 'ப்ரணவோ தனு: ஷரோ ஹ்யாத்மா ப்ரஹ்ம தல்லக்ஷ்யமுச்யதே — பிரணவமே வில், ஆத்மாவே அம்பு, பிரம்மமே இலக்கு! கவனச்சிதறலின்றி அந்த இலக்கைத் துளைத்து, அம்பு இலக்கில் ஒன்றிவிடுவது போல் பிரம்மமாகவே மாறிவிடு!'",
                "sub_cue": "प्रणवो धनुः शरो ह्यात्मा ब्रह्म तल्लक्ष्यमुच्यते — Pranava is the Bow, Atman the Arrow, Brahman the Target!",
                "sound": "Taut bowstring resonance releasing into a soaring, sustained Bansuri and Shankha note."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of the yogi's heart center where a downward-facing eight-petalled lotus turns upward and blossoms in full golden glory as he performs Kumbhaka and the Three Bandhas.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi performing Mula Bandha, Uddiyana Bandha, and Jalandhara Bandha in Padmasana; inside his chest, a downward-facing lotus of golden light turns upward and blooms radiantly. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Mastering the four great Asanas—Siddha, Bhadra, Simha, and Padma—along with Mula Bandha, Uddiyana Bandha, Jalandhara Bandha, and Khechari Mudra, the yogi performs Kumbhaka! By the power of breath-retention, the downward-facing lotus of the heart turns upward and blooms in full glory, while the yogi draws back his prana like a spider drawing in its thread!",
                "vo_ta": "சித்தம், பத்ரம், சிம்மம், பத்மம் ஆகிய நான்கு ஆசனங்களிலும், மூலபந்தம், உட்டியான பந்தம், ஜாலந்தர பந்தம் மற்றும் கேசரி முத்திரையிலும் தேர்ந்து யோகி கும்பகம் புரிகிறான்! பிராணாயாம சக்தியால் இதயத்தில் கவிழ்ந்திருக்கும் தாமரை மேல்நோக்கித் திரும்பி மலர்கிறது; சிலந்தி தன் நூலை உள்ளிழுப்பது போல் பிராணனை யோகி ஆத்மாவில் ஒடுக்குகிறான்!",
                "sub_cue": "Through the Three Bandhas and Kumbhaka, the downward lotus of the heart turns upward and blooms!",
                "sound": "Deep rhythmic Kumbhaka pulse with blossoming Saraswati Veena chords."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi's crown chakra where the subtle Nada sounds culminate in the soundless Paramatman.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of the meditating yogi in samadhi as a vertical pillar of golden-white light connects his upturned heart lotus to the thousand-petalled crown chakra. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the pericarp of that awakened lotus shines the Sun, the Moon, and the Fire; and in the center of the Flame dwells the Paramatman—smaller than a mustard seed yet vaster than the universe! Beholding Him through Dhyana, the yogi transcends birth and death forever!",
                "vo_ta": "மலர்ந்த அந்த இதயத் தாமரையின் நடுவே சூரியன், சந்திரன், அக்னி மண்டலங்கள் ஒளிர்கின்றன; அச்சுடரின் மையத்தில் கடுகளவினும் நுட்பமாய், பிரபஞ்சத்தினும் பெரிதாய்ப் பரமாத்மா உறைகிறார்! தியானத்தால் அவரைத் தரிசிக்கும் யோகி பிறப்பு-இறப்பை நிரந்தரமாகக் கடக்கிறான்!",
                "sub_cue": "In the center of the Heart-Flame shines the Paramatman, vaster than the cosmos!",
                "sound": "Crescendo of temple bells, conch, and Vedic choral chant."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogi seated in motionless samadhi in the Himalayan cave, bathed in golden morning light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the illumined yogi seated in padmasana inside the sunlit Himalayan cave, radiating golden peace across the mountain peaks. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Merged like the arrow in the target, where knower, meditation, and the object of meditation become One, the yogi abides in the supreme peace of Nirvana.",
                "vo_ta": "இலக்கில் தைத்த அம்பைப் போல, தியானிப்பவன், தியானம், தியானிக்கப்படும் பொருள் மூன்றும் ஒன்றாகி, பரம நிர்வாண சாந்தியில் யோகி நிலைபெறுகிறார்.",
                "sub_cue": "Knower, Meditation, and Target become One in the supreme peace of Brahman.",
                "sound": "Serene Bansuri and Tanpura sustain in Raga Hindolam."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the Himalayan peaks at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the golden Himalayan peaks and stone cave at sunrise. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Dhyanabindu Upanishad: aim the arrow of your soul with the bow of Omkara, turn the lotus of your heart toward the Light, and become one with the Eternal. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு தியானபிந்து உபநிடதம் நிறைவுறுகிறது: ஓங்கார வில்லால் ஆத்ம அம்பை எய்து, இதயத் தாமரையை ஒளியை நோக்கி மலர்த்தி, நித்தியப் பரம்பொருளோடு ஒன்றாவோமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Turn the lotus of the heart toward the Light; become one with the Eternal. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into mountain wind."
            }
        ]
    },
    # 28 (YOGA 9). BRAHMAVIDYA UPANISHAD (#40)
    {
        "story_id": "YOGA_09_BRAHMAVIDYA",
        "muktika_number": 40,
        "name_sanskrit": "ब्रह्मविद्योपनिषद्",
        "name_iast": "Brahmavidyopaniṣad",
        "name_tamil": "பிரம்மவித்யா உபநிடதம்",
        "name_english": "Brahmavidya Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Bell Sound of Om & The Fivefold Hamsa Lineage: Dissolving Mind into Prana",
        "story_title_tamil": "வெண்கல மணியின் ஓங்கார நாதமும் ஹம்ஸ பரம்பரையும்: பிரம்மவித்யா உபநிடதம்",
        "characters": "Lord Brahma, Vasishtha, Shakti, Parashara, Vyasa, and Shuka (The Golden Lineage of Hamsa-Vidya), The Awakened Yogi",
        "verse_sanskrit": "कांस्यघण्टानिनादस्तु यथा लीयति शान्तये । ओङ्कारस्तु तथा योज्यः शान्तये सर्वमिच्छता ॥ छिद्यन्ते सर्वसन्देहाः क्षीयन्ते चास्य कर्मणि । तस्मिन्दृष्टे परावरे ॥",
        "verse_tamil_translit": "காம்ஸ்யகண்டாநிநாதஸ்து யதா லீயதி ஷாந்தயே | ஓங்காரஸ்து ததா யோஜ்ய: ஷாந்தயே ஸர்வமிச்சதா ||",
        "verse_meaning_english": "Just as the ringing chime of a bronze bell trails off and dissolves into utter silence, so should Omkara be meditated upon by one who seeks supreme peace! When the Supreme Self is beheld, the knot of the heart is untied, all doubts are severed, and all karmas are destroyed!",
        "verse_meaning_tamil": "வெண்கல மணியின் நாதம் மெல்ல நீண்டு பேரமைதியில் கரைந்துபோவது போல, பரம சாந்தியை நாடுபவன் ஓங்காரத்தைத் தியானிக்க வேண்டும்! மேலான பரமாத்மாவைத் தரிசிக்கும்போது இதய முடிச்சு அவிழ்ந்து, சகல ஐயங்களும் அறுபட்டு, கர்மங்கள் அனைத்தும் அழிகின்றன!",
        "theme": "The resonance of Omkara trailing into silence like a bronze bell (Kamsya-ghanta); the Sushumna shining like the sun inside the body; the golden lineage from Brahma to Vasishtha, Shakti, Parashara, Vyasa, and Shuka; and merging Jiva and Paramatman like milk poured into milk or water into water.",
        "SettingVisual": "Ancient South Indian granite temple mandapam with a large suspended bronze bell and a serene Himalayan meditation cave at dawn",
        "ProtagonistVisual": "Young Sage Shuka and earnest disciples listening to the resonance of the bronze bell and meditating on the inner Sushumna",
        "GuruVisual": "Maharishi Vyasa and Vasishtha representing the unbroken Guru-parampara of Brahmavidya",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Close-up of a venerable Guru striking a massive ancient bronze temple bell at dawn; as the camera pulls back, the golden sound-wave ripples into the serene silence of the meditation hall.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot in an ancient Indian granite temple mandapam at golden sunrise. A venerable Guru gently strikes a suspended bronze bell while disciples sit in padmasana below, listening as the sound trails into silence. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's Brahmavidya Upanishad, the Master reveals the secret of the sacred syllable Om through the unforgettable image of a bronze bell: 'Just as the ringing sound of a bronze bell trails off gradually and dissolves into utter peace, so should Omkara be meditated upon by one who seeks supreme liberation!'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் பிரம்மவித்யா உபநிடதத்தில், வெண்கல மணியின் உவமை வழியே ஓங்கார ரகசியத்தை குரு வெளியிடுகிறார்: 'வெண்கல மணியின் நாதம் மெல்ல நீண்டு பேரமைதியில் கரைந்துபோவது போல, முக்தியை நாடுபவன் ஓங்கார நாதத்தின் முடிவில் உள்ள மௌனத்தைத் தியானிக்க வேண்டும்!'",
                "sub_cue": "कांस्यघण्टानिनादस्तु यथा लीयति शान्तये — As the sound of a bronze bell dissolves into silence, so meditate on Om!",
                "sound": "Rich, long-sustaining bronze temple bell strike trailing for 15 seconds into pure Tanpura silence."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of the meditating disciple as the three letters A, U, M (representing Rig, Yajur, Sama; Earth, Atmosphere, Heaven; Brahma, Vishnu, Rudra) converge into a single flame at the crown.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi in padmasana; three streams of golden, silver, and ruby prana light converge into a single blazing flame of light between his eyebrows. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Within the syllable Om dwell the three Vedas, the three worlds, and the three powers—A-kara glowing like the Sun, U-kara shining like the Moon, and Ma-kara flashing like lightning! Above all three shines the Ardhamatra, thin as a lotus thread, glowing like the tip of a lamp-flame!",
                "vo_ta": "ஓங்காரத்தினுள் மூன்று வேதங்களும் மூவுலகங்களும் அடங்கியுள்ளன—அகாரம் சூரியனைப் போலவும், உகாரம் சந்திரனைப் போலவும், மகாரம் மின்னலைப் போலவும் ஒளிர்கின்றன! இம்மூன்றிற்கும் மேலே தாமரை நூல் போல் நுட்பமான அர்த்தமாத்திரை தீபச் சுடரின் நுனி போல் பிரகாசிக்கிறது!",
                "sub_cue": "Above Sun, Moon, and Lightning shines the Ardhamatra like the tip of a lamp-flame!",
                "sound": "Three-part vocal harmony merging into a single high Bansuri note."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of the yogi's spine glowing with the golden sun-channel of Sushumna, purifying the seventy-two thousand nadis.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a meditating yogi in a sunlit granite cave; along his spine blazes the golden Sushumna channel like the morning sun, radiating light into the surrounding nadis. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Along the central column of the body runs the Sushumna nadi, luminous as the Sun! Piercing the lotus of the heart and ascending to the crown portal between the eyebrows, the yogi hears the unstruck sound of the bell and enters the immortal abode of Brahma!",
                "vo_ta": "உடலின் மையத்தில் சூரியனைப் போல் ஒளிரும் சுஷும்னா நாடி செல்கிறது! இதயத் தாமரையை ஊடுருவிப் புருவ மத்தியின் வழியே சிரசின் உச்சியை அடையும் யோகி, அங்கே ஒலிக்கும் அனாஹத மணி நாதத்தைக் கேட்டு அமரத்துவப் பதத்தை அடைகிறான்!",
                "sub_cue": "Ascending the sun-bright Sushumna, the Yogi hears the inner bell and enters Immortality.",
                "sound": "Resonant inner bell chimes layered with Saraswati Veena."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Majestic lineage montage: Pitamaha Brahma imparting the Hamsa-Vidya to Vasishtha, Vasishtha to Shakti, Shakti to Parashara, Parashara to Vyasa, and Vyasa to young Shuka.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic wide shot of Maharishi Vyasa and young radiant Sage Shuka seated beneath a sacred banyan tree at sunrise, surrounded by the luminous ancestral presence of Vasishtha and Parashara. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then the Upanishad reveals the sacred Guru-Parampara of Hamsa-Yoga: Pitamaha Brahma taught this secret of the breath to Vasishtha; Vasishtha taught it to Shakti; Shakti imparted it to Parashara; Parashara gave it to Vyasa; and Vyasa bestowed it upon his illumined son Shuka! Restraining the breath through Kumbhaka, the Hamsa ceases its restless flight and rests in the Self!",
                "vo_ta": "அதன்பின் ஹம்ஸ யோகத்தின் புனித குரு பரம்பரையை உபநிடதம் போற்றுகிறது: பிரம்மதேவர் வசிஷ்டருக்கும், வசிஷ்டர் சக்தி முனிவருக்கும், சக்தி பராசரருக்கும், பராசரர் வியாசருக்கும், வியாசர் தன் புதல்வர் சுகப் பிரம்மத்திற்கும் இந்தப் பிராண ரகசியத்தை உபதேசித்தனர்! கும்பகத்தால் பிராணனை நிறுத்தி, ஹம்ஸத்தை ஆத்மாவில் நிலைபெறச் செய்கிறான் யோகி!",
                "sub_cue": "The Golden Lineage: Brahma → Vasishtha → Shakti → Parashara → Vyasa → Shuka!",
                "sound": "Noble, reverent Pakhawaj and Rudra Veena composition honoring the Guru-Parampara."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Macro shot of pure white milk being poured into a bowl of milk, golden ghee into ghee, and crystal water into water—becoming completely indistinguishable.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps macro cinematic shot of pure white milk being poured smoothly into an earthen bowl of white milk in golden morning sunlight, becoming one seamless whole without distinction, while a sage meditates behind. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Look at the supreme union of Jiva and Paramatman: 'Kshire kshiram yatha kshiptam, tailam taile, jalam jale—just as milk poured into milk, oil poured into oil, and water poured into water become completely one without any separation, so does the yogi's soul merge indivisibly into the Supreme Atman!'",
                "vo_ta": "ஜீவாத்மாவும் பரமாத்மாவும் இணையும் பரம ஐக்கியத்தைக் காணீர்: 'க்ஷீரே க்ஷீரம் யதா க்ஷிப்தம் தைலம் தைலே ஜலம் ஜலே — பாலில் ஊற்றிய பாலும், எண்ணெயில் கலந்த எண்ணெயும், நீரில் கலந்த நீரும் பிரித்தறிய முடியாதபடி ஒன்றாவது போல, ஆத்மாவை உணர்ந்த யோகி பரமாத்மாவோடு இரண்டறக் கலந்துவிடுகிறான்!'",
                "sub_cue": "क्षीरे क्षीरं यथा क्षिप्तं — As milk poured into milk becomes one, the Yogi merges into the Supreme Atman!",
                "sound": "Liquid, seamless Violin and Bansuri unison resolving into a single pure tonic note."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Vyasa and Shuka seated in luminous samadhi as the knot of the heart dissolves in golden light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Maharishi Vyasa and Sage Shuka seated in nirvikalpa samadhi beneath the banyan tree at sunrise, bathed in golden-white radiance. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Bhidyate hridayagranthih, chidyante sarvasamshayah—when that Supreme and Inferior is beheld as One, the knot of the heart is broken, all doubts are severed, and all karmas are exhausted forever!",
                "vo_ta": "பித்யதே ஹ்ருதயக்ரந்தி: சித்யந்தே ஸர்வஸம்ஷயா: — அந்தப் பரம்பொருளை நேருக்கு நேர் தரிசிக்கும்போது இதய முடிச்சு அவிழ்கிறது, சகல சந்தேகங்களும் அறுபடுகின்றன, கர்ம வினைகள் அனைத்தும் என்றென்றும் அழிகின்றன!",
                "sub_cue": "भिद्यते हृदयग्रन्थिश्छिद्यन्ते सर्वसंशयाः — The knot of the heart breaks and all doubts vanish!",
                "sound": "Triumphant conch shell and celestial Vedic chorus."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back from the granite temple mandapam and banyan grove into the golden morning sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian granite temple mandapam and banyan grove bathed in golden sunrise light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Brahmavidya Upanishad: follow the chime of Omkara into the boundless silence where your soul and the Supreme are forever one, like milk in milk. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பிரம்மவித்யா உபநிடதம் நிறைவுறுகிறது: ஓங்கார மணி நாதத்தின் வழியே எல்லையற்ற மௌனத்தில் புகுந்து, பாலில் கலந்த பால் போல் பரமாத்மாவோடு ஒன்றாவோமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Follow the chime of Omkara into Silence; become one with the Supreme like milk in milk. Om Shanti.",
                "sound": "Final bronze bell chime and 'Om Saha Navavatu' fading into silence."
            }
        ]
    },
    # 29 (YOGA 10). YOGATATTVA UPANISHAD (#41)
    {
        "story_id": "YOGA_10_YOGATATTVA",
        "muktika_number": 41,
        "name_sanskrit": "योगतत्त्वोपनिषद्",
        "name_iast": "Yogatattvopaniṣad",
        "name_tamil": "யோகதத்வ உபநிடதம்",
        "name_english": "Yogatattva Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "Lord Vishnu Reveals the Fourfold Yoga (Mantra, Laya, Hatha, Raja) to Brahma",
        "story_title_tamil": "நால்வகை யோகமும் (மந்திர, லய, ஹட, ராஜ) ஞான யோக ஐக்கியமும்: பிரம்மனுக்கு விஷ்ணு உபதேசம்",
        "characters": "Lord Mahavishnu (Purushottama, The Supreme Guru), Pitamaha Brahma (The Creator Seeker), The Master Yogi of the Five Elemental Dharanas",
        "verse_sanskrit": "योगात्सञ्जायते ज्ञानं ज्ञानाद्योगः प्रवर्तते । योगज्ञानाभियुक्तस्य नान्यत्पश्यन्ति योगिनः ॥ मन्त्रयोगो लयश्चैव हठो राजायोगस्तथा । आरम्भश्च घटश्चैव तथा परिचयोऽपि च । निष्पत्तिः सर्वयोगेषु अवस्थाः परिकीर्तिताः ॥",
        "verse_tamil_translit": "யோகாத் ஸஞ்ஜாயதே க்ஞானம் க்ஞானாத் யோக: ப்ரவர்த்ததே | மந்த்ரயோகோ லயஸ்சைவ ஹடோ ராஜயோகஸ்ததா ||",
        "verse_meaning_english": "From Yoga arises Knowledge, and from Knowledge Yoga advances; for him who is endowed with both Yoga and Jnana, there is nothing unattainable! Mantra Yoga, Laya Yoga, Hatha Yoga, and Raja Yoga—and the four stages of Arambha, Ghata, Parichaya, and Nishpatti—lead to supreme liberation!",
        "verse_meaning_tamil": "யோகத்திலிருந்து ஞானம் பிறக்கிறது, ஞானத்தினால் யோகம் சிறக்கிறது; யோகமும் ஞானமும் இணைந்தவருக்கு எட்டாதது எதுவுமில்லை! மந்திர யோகம், லய யோகம், ஹட யோகம், ராஜ யோகம் ஆகிய நான்கும், ஆரம்பம், கடம், பரிசயம், நிஷ்பத்தி எனும் நான்கு அவஸ்தைகளும் பரம முக்திக்கு இட்டுச் செல்கின்றன!",
        "theme": "Lord Vishnu's comprehensive blueprint of Yoga to Brahma: the inseparable twin wings of Jnana and Yoga, the Four Yogas (Mantra, Laya, Hatha, Raja), the Four Avasthas (Arambha, Ghata, Parichaya, Nishpatti), Nadi-shodhana, the Five Elemental Dharanas (Prithvi, Apas, Tejas, Vayu, Akasha), and the warning not to be distracted by Siddhis on the way to Kaivalya.",
        "SettingVisual": "Cosmic golden-sapphire sanctuary of Lord Vishnu transitioning to a serene forest matha with a small doorway where a yogi masters the five elements",
        "ProtagonistVisual": "Pitamaha Brahma bowing before Mahavishnu, and a disciplined yogi practicing Nadi-shodhana and Pancha-tattva Dharana",
        "GuruVisual": "Lord Mahavishnu (Purushottama) radiating golden-blue effulgence",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic slow dolly-in across a golden-lit cosmic sanctuary where Pitamaha Brahma bows before Lord Mahavishnu.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps majestic dolly shot in a sacred ancient Indian temple sanctuary at golden dawn. Pitamaha Brahma bows with folded hands before the luminous golden-sapphire presence of Lord Mahavishnu seated on a lotus stone throne. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's Yogatattva Upanishad, Pitamaha Brahma bowed before Lord Mahavishnu, the Supreme Purushottama, and asked: 'O Bhagavan! How does the soul bound by Maya attain liberation? What is the true relationship between Jnana and Yoga?'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் யோகதத்வ உபநிடதத்தில், பிதாமகர் பிரம்மதேவர் புருஷோத்தமனான மகாவிஷ்ணுவை வணங்கிக் கேட்டார்: 'பகவானே! மாயையால் கட்டுண்ட ஜீவன் முக்தியடைவது எவ்வாறு? ஞானத்திற்கும் யோகத்திற்கும் உள்ள உண்மையான தொடர்பு யாது?'",
                "sub_cue": "Brahma asks Lord Vishnu: 'What is the true union of Jnana and Yoga that liberates the soul?'",
                "sound": "Deep Panchajanya Shankha resonance, gentle water waves, and a serene Saraswati Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Lord Vishnu's compassionate face as two golden wings of light (Yoga and Jnana) lift a swan into the sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of a radiant white swan rising into golden morning sunbeams with two symmetrical wings of light, while a yogi meditates below in a stone pavilion. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Vishnu declared the golden axiom: 'Yogat sanjayate jnanam, jnanad yogah pravartate—Knowledge without Yoga cannot secure liberation, and Yoga without Knowledge cannot bear fruit! Therefore, the seeker of liberation must practice both Yoga and Jnana intensely, like the two wings of a soaring bird!'",
                "vo_ta": "மகாவிஷ்ணு பொன்னான விதியை அருளினார்: 'யோகாத் ஸஞ்ஜாயதே க்ஞானம் க்ஞானாத் யோக: ப்ரவர்த்ததே — யோகம் இல்லாத ஞானத்தாலோ, ஞானம் இல்லாத யோகத்தாலோ முக்தி கிட்டாது! பறவையின் இரு சிறகுகளைப் போல யோகத்தையும் ஞானத்தையும் ஒருங்கே பயில்பவனே பரம பதத்தை அடைகிறான்!'",
                "sub_cue": "योगात्सञ्जायते ज्ञानं ज्ञानाद्योगः प्रवर्तते — Yoga and Jnana are the two inseparable wings of Liberation!",
                "sound": "Balanced duet of Bansuri flute and Carnatic violin in Raga Kalyani."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Four-part visual progression showing a yogi ascending through Mantra Yoga, Laya Yoga, Hatha Yoga, and Raja Yoga across the four stages of Arambha, Ghata, Parichaya, and Nishpatti.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot inside a clean, quiet ancient Indian thatched yoga hut with a small doorway, where a yogi sits on a kusha mat practicing alternate-nostril Nadi-shodhana pranayama in golden dawn light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Vishnu classified Yoga into four paths—Mantra Yoga, Laya Yoga, Hatha Yoga, and Raja Yoga—and four progressive stages: Arambha (where the nadis are purified through 80 daily pranayamas), Ghata (where Prana and Apana unite), Parichaya (where Kundalini awakens into the sky of consciousness), and Nishpatti (where all karmic seeds are burned in Samadhi)!",
                "vo_ta": "யோகத்தை மந்திர யோகம், லய யோகம், ஹட யோகம், ராஜ யோகம் என நான்காகவும்; ஆரம்பம் (நாடி சுத்தி), கடம் (பிராண-அபான ஐக்கியம்), பரிசயம் (சுஷும்னா பிரவேசம்), நிஷ்பத்தி (சமாதி பூரணம்) என நான்கு அவஸ்தைகளாகவும் பகவான் வகுத்தருளினார்!",
                "sub_cue": "Four Yogas (Mantra, Laya, Hatha, Raja) and Four Stages (Arambha, Ghata, Parichaya, Nishpatti).",
                "sound": "Steady 16-64-32 rhythmic pranayama pulse on soft mridangam."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Spectacular visualization of the Five Elemental Dharanas (Pancha-Tattva Dharana) glowing at five centers of the yogi's body: yellow square of Earth, white crescent of Water, red triangle of Fire, smoky circle of Air, and pure blue Ether.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a meditating Indian yogi in padmasana; along his torso shimmer five sacred elemental lights—golden-yellow earth, silver-white crescent water, ruby-red triangular fire, smoky-blue air, and pure starlit ether. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Vishnu taught the Five Elemental Dharanas: fixing Prana for five ghatikas each on yellow Earth (La-kara), white crescent Water (Va-kara), red triangular Fire (Ra-kara), smoky Air (Ya-kara), and spotless Sky (Ha-kara), the yogi conquers all five elements! Yet the Lord warned: 'Never display miraculous Siddhis before the world! Hide your powers and stay fixed on Liberation alone!'",
                "vo_ta": "அதன்பின் பஞ்சபூத தாரணையை பகவான் அருளினார்: பொன்னிறப் பிருத்வி (ல), பிறைவடிவ வெண்ணிற அப்பு (வ), செந்நிற முக்கோணத் தேஜஸ் (ர), வாயு (ய), நிர்மல ஆகாயம் (ஹ) ஆகிய ஐந்திலும் பிராணனை நிறுத்தி பஞ்ச பூதங்களையும் வெல்கிறான் யோகி! ஆயினும், 'அணிமா முதலான சித்திகளை உலகோர் முன் காட்டாமல் மறைத்து, மோட்சத்தில் மட்டுமே குறியாக இருப்பாயாக!' என எச்சரிக்கிறார் பகவான்.",
                "sub_cue": "Master the Five Elemental Dharanas; shun the display of Siddhis and seek Moksha alone!",
                "sound": "Five ascending harmonic chords on Rudra Veena and Santoor."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of a glowing brass lamp placed inside a clay pot vs. the pot breaking so the light shines unhindered everywhere.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of a glowing golden flame inside an earthen pot; as the clay walls fall away, the golden light expands unhindered in all directions around the meditating yogi. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Just as a lamp placed inside a pot does not shine outside, but when the pot is broken its light blazes forth unhindered, so when the pot of body-identification is dissolved in Raja-Yoga Samadhi, the self-luminous Atman shines as the Infinite!",
                "vo_ta": "குடத்தினுள் வைக்கப்பட்ட தீபம் வெளியே தெரிவதில்லை; ஆனால் குடம் உடைந்ததும் அச்சுடர் எங்கும் தடையின்றிப் பிரகாசிப்பது போல, தேகாபிமானம் எனும் குடம் ராஜயோக சமாதியில் உடையும்போது சுயம்பிரகாச ஆத்மா எங்கும் நிறைந்து ஒளிர்கிறது!",
                "sub_cue": "When the pot of ego breaks in Samadhi, the lamp of the Self shines unhindered everywhere!",
                "sound": "Crystalline chime and soaring Shankha and Veena crescendo."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogi in Nishpatti Samadhi, where Jiva and Paramatman are united like salt dissolved in water.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the illumined yogi seated in Nishpatti Samadhi on a sunlit mountain terrace, bathed in golden-blue Vishnu radiance. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "As salt dissolved in water becomes one with water, so when Manas and Atman unite in Samadhi, duality vanishes forever and the yogi abides as Supreme Brahman.",
                "vo_ta": "நீரில் கரைந்த உப்பு நீரோடு ஒன்றாவது போல, மனமும் ஆத்மாவும் சமாதியில் இணையும்போது இருமை மறைந்து யோகி பரப்பிரம்மமாகவேத் திகழ்கிறார்.",
                "sub_cue": "As salt in water, Mind and Atman unite in indivisible Samadhi.",
                "sound": "Spacious Tanpura and Bansuri peace harmonies."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the sunlit sanctuary as Brahma bows before Lord Mahavishnu.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian temple sanctuary bathed in golden sunrise light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Yogatattva Upanishad: unite the two wings of Yoga practice and Self-Knowledge, transcend the lure of lesser powers, and soar into the boundless sky of Kaivalya. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு யோகதத்வ உபநிடதம் நிறைவுறுகிறது: யோக சாதனை, ஆத்ம ஞானம் எனும் இரு சிறகுகளையும் இணைத்து, கைவல்ய முக்தி வானில் சிறகடிப்போமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Unite the wings of Yoga and Jnana; soar into boundless Kaivalya. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into peaceful morning air."
            }
        ]
    },
    # 30 (YOGA 11). TRISHIKHIBRAHMANA UPANISHAD (#44)
    {
        "story_id": "YOGA_11_TRISHIKHIBRAHMANA",
        "muktika_number": 44,
        "name_sanskrit": "त्रिशिखिब्राह्मणोपनिषद्",
        "name_iast": "Triśikhibrahmaṇopaniṣad",
        "name_tamil": "திரிசிகி பிராம்மண உபநிடதம்",
        "name_english": "Trishikhibrahmana Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Yoga",
        "story_title_english": "Trishikhi Brahmana Travels to Aditya-Loka: Lord Surya's Eight-Limbed Yoga of Shiva",
        "story_title_tamil": "ஆதித்ய லோகம் சென்ற திரிசிகி பிராம்மணர்: சூரிய பகவான் அருளிய அஷ்டாங்க சிவயோகம்",
        "characters": "Trishikhi Brahmana (The Three-Tufted Vedic Seeker), Bhagavan Surya (Aditya, The Cosmic Sun-God & Guru)",
        "verse_sanskrit": "किं कार्यं किं च वा ज्ञानं ब्रूहि मे सूर्यपूजित । अहिंसा सत्यमस्तेयं ब्रह्मचर्यं दयार्जवम् । क्षमा धृतिर्मिताहारः शौचं चेति यमा दश ॥",
        "verse_tamil_translit": "கிம் கார்யம் கிம் ச வா க்ஞானம் ப்ரூஹி மே ஸூர்யபூஜித | அஹிம்ஸா ஸத்யமஸ்தேயம் ப்ரஹ்மசர்யம் தயார்ஜவம் ||",
        "verse_meaning_english": "'What is body, what is Prana, what is the Cause, and what is the Self? Tell me, O Adored Sun-God!' Surya taught the ten Yamas—non-violence, truth, non-stealing, continence, compassion, rectitude, forgiveness, fortitude, moderate diet, and purity—leading through Ashtanga Yoga to the Spotless Shiva!",
        "verse_meaning_tamil": "'உடல் எது? பிராணன் எது? முதற்காரணம் எது? ஆத்மா எது? சூரிய பகவானே எனக்குக் கூறுவீராக!' அஹிம்சை, சத்தியம், திருடாமை, பிரம்மச்சரியம், தயை, நேர்மை, பொறுமை, உறுதி, மித ஆகாரம், தூய்மை ஆகிய பத்து இயமங்களுடன் கூடிய அஷ்டாங்க யோகத்தால் களங்கமற்ற சிவபதத்தை அடைய சூரியன் அருளினார்!",
        "theme": "The seeker Trishikhi Brahmana ascending to the realm of the Sun (Aditya-loka) to question Bhagavan Surya about the body, soul, creation, and liberation; Surya's exposition of how the universe evolves from Avyakta-Shiva, the seventeen-asana Ashtanga Yoga, Kumbhaka mastery, and beholding the Niranjana Atman at the center of the Kanda and Heart.",
        "SettingVisual": "Blazing golden-amber temple terrace high in the Himalayan clouds facing the rising Sun (Aditya-Mandala)",
        "ProtagonistVisual": "Trishikhi Brahmana, an austere Shukla Yajurvedic seeker with three sacred locks of hair, bowing in golden sunlight",
        "GuruVisual": "Bhagavan Surya (Aditya), radiating warm golden solar effulgence from the solar orb",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide crane shot ascending toward a high Himalayan solar terrace at dawn as Trishikhi Brahmana bows before the blazing golden orb of Bhagavan Surya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an ancient Indian stone terrace high in the Himalayan clouds at sunrise. Austere sage Trishikhi Brahmana bows with folded hands before the blazing golden solar orb of Bhagavan Surya. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Shukla Yajur Veda's Trishikhibrahmana Upanishad, the earnest seeker Trishikhi Brahmana traveled to the luminous realm of Aditya and bowed before the Sun-God: 'O Bhagavan! Tell me—what is the body, what is Prana, what is the First Cause, and what is the Supreme Atman?'",
                "vo_ta": "சுக்ல யஜுர் வேதத்தின் திரிசிகி பிராம்மண உபநிடதத்தில், திரிசிகி எனும் அந்தணர் ஒளிமயமான ஆதித்ய மண்டலத்தை அடைந்து சூரிய பகவானை வணங்கிக் கேட்டார்: 'பகவானே! உடல் எது? பிராணன் எது? முதற்காரணம் எது? பரமாத்மா எது? எனக்கு அருள்வீராக!'",
                "sub_cue": "Trishikhi Brahmana asks Lord Surya: 'What is the Body, Prana, Cause, and Supreme Atman?'",
                "sound": "Golden solar horn/conch resonance, morning mountain breeze, and a radiant Rudra Veena alapana in Raga Surya."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Trishikhi's face illuminated by golden solar rays as Surya reveals how all creation emerges from the One Shiva.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Trishikhi Brahmana's earnest face bathed in warm golden solar rays as five subtle elemental spheres of light shimmer in the air before him. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Bhagavan Surya answered: 'All this is indeed Shiva—pure, spotless, and absolute! By His own self-effulgence, from Avyakta arose Mahat, Ahankara, the five elements, and this body! Though bound by karma in ignorance, how is the soul freed? By Karma-Yoga and Jnana-Yoga united through the Eight Limbs of Ashtanga Yoga!'",
                "vo_ta": "சூரிய பகவான் அருளினார்: 'இவை அனைத்துமே களங்கமற்ற கேவல சிவ சொரூபமே! அவ்யக்தத்திலிருந்து மகத், அகங்காரம், பஞ்ச பூதங்கள் மற்றும் இவ்வுடல் தோன்றின! கர்மயோகமும் ஞானயோகமும் இணைந்த அஷ்டாங்க யோகத்தாலேயே ஜீவன் முக்தியடைகிறான்!'",
                "sub_cue": "All this is spotless Shiva; through Karma-Yoga and Jnana-Yoga united in Ashtanga Yoga, the soul is freed!",
                "sound": "Steady Pakhawaj beat and a luminous Saraswati Veena melody."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium tracking shot of the yogi practicing the Ten Yamas, Ten Niyamas, and the classic Asanas (Padma, Vajra, Siddha, Simha, Gomukha) on the sunlit terrace.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium tracking shot of Trishikhi Brahmana seated in flawless Padmasana on the sunlit stone terrace overlooking the mountain clouds, radiating ethical purity and physical steadiness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Surya redefined the foundations of Yoga: 'Extreme indifference to all sensory craving is the supreme Yama! Continuous flow of devotion toward the Supreme Principle is the supreme Niyama! Looking upon all things with indifference to worldly gain is the supreme Asana! Together with the ten Yamas, ten Niyamas, and seventeen postures, the yogi prepares the temple of the body!'",
                "vo_ta": "யோகத்தின் அடிப்படைகளை சூரிய பகவான் ஆழமாக வரையறுத்தார்: 'இந்திரிய போகங்களில் கொண்ட பூரண பற்றின்மையே உத்தம இயமம்! பரம்பொருளின் மீது இடைவிடாது செல்லும் மனப்பதிவே உத்தம நியமம்! சர்வ வஸ்துக்களிலும் உதாசீன பாவனையுடன் இருப்பதே உத்தம ஆசனம்!'",
                "sub_cue": "Detachment is Yama, continuous devotion to the Supreme is Niyama, equanimity is Asana!",
                "sound": "Inspiring Bansuri flute melody in Raga Bilahari."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of the yogi's navel center (Kanda), glowing like a white bird's egg where 72,000 nadis meet, as Kundalini awakens through Kumbhaka.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of a meditating Indian yogi in padmasana; at his navel center glows a luminous oval Kanda of light from which golden threads of prana radiate into the central Sushumna channel. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the center of the body lies the Kanda—nine fingers above the base, four fingers wide, shaped like a bird's egg—from which seventy-two thousand nadis branch out! Purifying them through Rechaka, Puraka, and Kumbhaka, and practicing the five elemental Dharanas, the yogi awakens Kundalini into the central Sushumna!",
                "vo_ta": "உடலின் மையத்தில் பறவை முட்டை வடிவில் 'கந்தம்' எனும் நாடிகளின் மூலம் உள்ளது; அங்கிருந்து எழுபத்திரண்டாயிரம் நாடிகள் பிரிகின்றன! பிராணாயாமத்தாலும் பஞ்சபூத தாரணையாலும் நாடிகளைத் தூய்மைப்படுத்தி, குண்டலினியை சுஷும்னா வழியே மேலேற்றுகிறான் யோகி!",
                "sub_cue": "From the Kanda at the center of the body, awaken Kundalini through Kumbhaka into Sushumna!",
                "sound": "Deep rhythmic Kumbhaka breath with shimmering Santoor and Veena overtones."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic zoom into the yogi's heart and crown as a smokeless, steady flame of Vasudeva-Atman shines like lightning in a raincloud.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of Trishikhi Brahmana in deep samadhi at sunrise; within his heart and crown blazes a steady, smokeless golden flame of Consciousness like lightning in a golden cloud. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Surya revealed the climax of Dhyana and Samadhi: 'Behold the Supreme Atman—Vasudeva, Niranjana—shining like a smokeless lamp-flame, like a flash of lightning in a raincloud! When the mind forgets even the effort of meditation and merges completely into that Self-Luminous Witness, that is Samadhi!'",
                "vo_ta": "அதன்பின் தியானம் மற்றும் சமாதியின் உச்சத்தை சூரியன் வெளியிட்டார்: 'புகையில்லாத் தீபச் சுடர் போலவும், கார்மேகத்தில் தோன்றும் மின்னல் கொடி போலவும் ஒளிரும் நிரஞ்சன வாசுதேவ ஆத்மாவைத் தரிசிப்பாயாக! தியானிப்பவன் என்ற நினைப்பும் மறைந்து அச்சுயம்பிரகாச சாட்சியில் ஒன்றிவிடுவதே சமாதி!'",
                "sub_cue": "Shining like a smokeless flame, the Niranjana Atman is realized in Samadhi!",
                "sound": "Majestic crescendo of conch, temple bells, and Vedic choral chant."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Trishikhi Brahmana seated in luminous stillness on the solar terrace, his aura indistinguishable from the golden morning sun.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Trishikhi Brahmana meditating in lotus posture on the Himalayan terrace at sunrise, his form glowing like a second golden sun in total oneness with Aditya. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Knowing that one's own Self is the all-pervading Consciousness, free from old age, death, and sorrow, Trishikhi Brahmana attained supreme Kaivalya—where there is no return.",
                "vo_ta": "மூப்பு, மரணம், சோகம் அற்ற எங்கும் நிறைந்த சைதன்யமே தன் ஆத்மா என்பதை உணர்ந்த திரிசிகி பிராம்மணர், மறுபிறப்பற்ற கைவல்ய முக்தியை அடைந்தார்.",
                "sub_cue": "Realizing the Self as the all-pervading Consciousness, Trishikhi attains supreme Kaivalya.",
                "sound": "Spacious Tanpura and Violin sustain in Raga Hamsadhwani."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the golden Himalayan clouds and solar terrace.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the sunlit Himalayan terrace and sea of golden clouds at dawn. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Trishikhibrahmana Upanishad: purify your life with the Yamas and Niyamas, kindle the smokeless flame of Dhyana, and shine with the immortal radiance of the Sun of Consciousness. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு திரிசிகி பிராம்மண உபநிடதம் நிறைவுறுகிறது: இயம-நியமங்களால் வாழ்வைத் தூய்மையாக்கி, புகையில்லா தியானச் சுடரை ஏற்றி, ஆத்ம சூரியனாகப் பிரகாசிப்போமாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Kindle the smokeless flame of Dhyana; shine as the Sun of Consciousness. Om Shanti.",
                "sound": "Shanti Mantra 'Om Purnamadah' fading into golden mountain air."
            }
        ]
    },
    # 31 (YOGA 12). YOGACHUDAMANI UPANISHAD (#46)
    {
        "story_id": "YOGA_12_YOGACHUDAMANI",
        "muktika_number": 46,
        "name_sanskrit": "योगचूडामण्युपनिषद्",
        "name_iast": "Yogacūḍāmaṇyupaniṣad",
        "name_tamil": "யோகசூடாமணி உபநிடதம்",
        "name_english": "Yogachudamani Upanishad",
        "veda": "Sama Veda",
        "category": "Yoga",
        "story_title_english": "The Crest-Jewel of Yoga: Awakening Kundalini Across the Six Chakras & Three Bandhas",
        "story_title_tamil": "யோகத்தின் சூடாமணி: ஆறு சக்கரங்களையும் மூன்று பந்தங்களையும் கடந்த குண்டலினி விழிப்பு",
        "characters": "The Master of Shadanga & Kundalini Yoga, The Awakened Sama Vedic Yogi, Goddess Kundalini (Mother of the Three Worlds)",
        "verse_sanskrit": "आसनं प्राणसंरोधः प्रत्याहारश्च धारणा । ध्यानं समाधिरेतानि योगाङ्गानि भवन्ति षट् ॥ प्रसुप्ता भुजगाकारा पद्मतन्तुनिभा शुभा । प्रबुद्धा वह्नियोगेन व्रजत्यूर्ध्वं सुषुम्नया ॥",
        "verse_tamil_translit": "ஆஸனம் ப்ராணஸம்ரோத: ப்ரத்யாஹாரஸ்ச தாரணா | த்யானம் ஸமாதிரேதானி யோகாங்கானி பவந்தி ஷட் ||",
        "verse_meaning_english": "Asana, Pranayama, Pratyahara, Dharana, Dhyana, and Samadhi—these are the six limbs of Yoga! Sleeping like a coiled serpent, bright as a lotus fiber, when awakened by the fire of Yoga, Kundalini ascends upward through the Sushumna!",
        "verse_meaning_tamil": "ஆசனம், பிராணாயாமம், பிரத்யாஹாரம், தாரணை, தியானம், சமாதி ஆகிய ஆறும் யோகத்தின் அங்கங்களாகும்! தாமரை நூல் போல் ஒளிரும் குண்டலினி சக்தி, யோக அக்னியால் விழித்தெழுந்து சுஷும்னா நாடி வழியாக மேல்நோக்கி உயர்கிறாள்!",
        "theme": "The Crown-Jewel of Sama Vedic Yoga: the six limbs of Shadanga Yoga, the luminous map of the Six Chakras (4-petalled Muladhara, 6-petalled Svadhishthana, 10-petalled Manipura, 12-petalled Anahata, 16-petalled Vishuddhi, 2-petalled Ajna, and Sahasrara), awakening Kundalini through the Three Bandhas, and taming Prana like a mahout tames a wild elephant or lion.",
        "SettingVisual": "Sacred Sama Vedic granite cave sanctuary lit by golden oil lamps, with a serene lotus pond outside at dawn",
        "ProtagonistVisual": "A Sama Vedic yogi seated in Siddhasana/Kamalasana, his spine illuminated by the six glowing lotus chakras",
        "GuruVisual": "Venerable Sama Vedic Yoga Master imparting the secret of the Crest-Jewel (Chudamani) of Yoga",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly shot into a sunlit Sama Vedic stone cave sanctuary where a disciple bows before the Master of Kundalini Yoga.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot into an ancient Indian granite cave sanctuary at golden dawn. A devoted yogi bows with folded hands before a luminous Sama Vedic Yoga Master seated on a kusha mat beside brass oil lamps. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Sama Veda's Yogachudamani Upanishad—the Crest-Jewel of Yoga—the Master unveils the secret architecture of the subtle body for all seekers of liberation: the Six Limbs of Yoga—Asana, Pranayama, Pratyahara, Dharana, Dhyana, and Samadhi—and the awakening of the cosmic power within!",
                "vo_ta": "சாம வேதத்தின் யோகசூடாமணி உபநிடதத்தில்—யோகத்தின் முடிமணியில்—முக்தியை நாடும் சாதகர்களுக்கு சூட்சும சரீரத்தின் ரகசிய அமைப்பை குரு வெளியிடுகிறார்: ஆசனம், பிராணாயாமம், பிரத்யாஹாரம், தாரணை, தியானம், சமாதி எனும் ஆறு அங்கங்களும் குண்டலினி விழிப்பும்!",
                "sub_cue": "The Crest-Jewel of Yoga: the Six Limbs and the secret architecture of the subtle body.",
                "sound": "Deep Sama Veda Omkara chant, temple bell, and a mystical Rudra Veena prelude."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Vertical rising camera movement along the meditating yogi's spine, illuminating the Six Lotuses (4, 6, 10, 12, 16, and 2 petals) up to the thousand-petalled crown.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps vertical rising shot of an ancient Indian yogi seated in Siddhasana; along his spine glow six luminous lotus chakras of golden and prismatic prana light ascending to the radiant thousand-petalled crown chakra. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Behold the six sacred lotuses along the spine: the four-petalled Muladhara at the base, the six-petalled Svadhishthana, the ten-petalled Manipura at the navel, the twelve-petalled Anahata in the heart, the sixteen-petalled Vishuddhi at the throat, the two-petalled Ajna between the eyebrows, and above them all, the thousand-petalled Sahasrara!",
                "vo_ta": "முதுகுத்தண்டில் மிளிரும் ஆறு ஆதார கமலங்களைக் காணீர்: நான்கு இதழ் மூலாதாரம், ஆறு இதழ் சுவாதிஷ்டானம், பத்து இதழ் மணிபூரகம், பன்னிரண்டு இதழ் அனாஹதம், பதினாறு இதழ் விசுத்தி, இரண்டு இதழ் ஆக்ஞை மற்றும் இவை அனைத்திற்கும் மேலாக ஆயிரம் இதழ் சகஸ்ராரம்!",
                "sub_cue": "Six Lotuses (4, 6, 10, 12, 16, 2 petals) culminating in the Thousand-Petalled Sahasrara!",
                "sound": "Ascending seven-note raga scale on Santoor and Bansuri with harmonic chimes at each chakra."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Close-up of the yogi's base center where Kundalini, bright as a lotus fiber, awakens from her eight-coiled slumber and enters the doorway of Sushumna.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of a meditating yogi in padmasana; a slender, lotus-fiber-bright golden stream of Kundalini prana awakens at the base of his spine and rises gracefully up the central Sushumna channel. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Above the Kanda sleeps Maha-Kundalini in eight coils, guarding the portal of Brahman! Awakened by the fire of Prana and Apana, bright as a slender lotus fiber, she uncoils and enters the royal highway of Sushumna—for Kundalini alone is the giver of liberation to yogis!",
                "vo_ta": "கந்தத்திற்கு மேலே எட்டுச் சுருள்களாய் உறங்கும் மகா குண்டலினி பிரம்ம வாசலைக் காத்து நிற்கிறாள்! பிராண-அபான அக்னியால் விழித்தெழுந்து, தாமரை நூல் போல் ஒளிரும் அவள் சுஷும்னா राजபாதையில் புகுகிறாள்—ஏனெனில் குண்டலினியே யோகியருக்கு முக்தி அருள்பவள்!",
                "sub_cue": "प्रबुद्धा वह्नियोगेन व्रजत्यूर्ध्वं सुषुम्नया — Awakened by Yoga-fire, Kundalini ascends through Sushumna!",
                "sound": "Rising Saraswati Veena glissando accompanied by deep, resonant pakhawaj."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Cinematic metaphor: a skilled mahout gently guiding a mighty royal elephant, cross-dissolving to the yogi performing Mula Bandha, Uddiyana Bandha, Jalandhara Bandha, and Khechari Mudra.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a gentle Indian mahout guiding a calm, majestic tusker elephant along a forest path at dawn, transitioning to a yogi in padmasana mastering the three bandhas with serene authority. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "How is the mighty breath mastered? 'Just as a lion, an elephant, or a tiger is tamed step by step with patience, so should Prana be brought under control gradually—otherwise it harms the impatient practitioner!' Through Mula Bandha, the great bird of Uddiyana Bandha, the net-lock of Jalandhara Bandha, and Khechari Mudra, old age and decay are conquered!",
                "vo_ta": "வல்லமை மிக்க பிராணனை வசப்படுத்துவது எவ்வாறு? 'சிங்கம், யானை அல்லது புலியைப் பொறுமையோடு படிப்படியாகப் பழக்குவது போல, பிராணனையும் மெல்ல மெல்லவே வசப்படுத்த வேண்டும்!' மூலபந்தம், உட்டியான பந்தம், ஜாலந்தர பந்தம் மற்றும் கேசரி முத்திரையால் மூப்பும் சோர்வும் வெல்லப்படுகின்றன!",
                "sub_cue": "As an elephant or lion is tamed step by step, master Prana gradually through the Three Bandhas!",
                "sound": "Measured, majestic Mridangam rhythm with warm Violin phrases."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi's crown chakra where the Moon of Ida and the Sun of Pingala unite in the nectar-ocean of Sahasrara.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of an illumined Indian yogi in samadhi; at his crown chakra, golden solar light and silvery lunar light merge into a radiant thousand-petalled lotus of immortal nectar. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "When the Sun of Pingala and the Moon of Ida dissolve into the central channel, and Kundalini unites with Paramashiva in the Sahasrara, the two-syllable Hamsa-Soham mantra resolves into the soundless Ardhamatra of Pranava!",
                "vo_ta": "பிங்கலை எனும் சூரியனும் இடை எனும் சந்திரனும் சுஷும்னாவில் ஒடுங்கி, சகஸ்ராரத் தாமரையில் குண்டலினி பரமசிவனுடன் இணையும்போது, ஹம்ஸ-ஸோஹம் மந்திரம் பிரணவத்தின் நிசப்த அர்த்தமாத்திரையில் கரைகிறது!",
                "sub_cue": "Sun and Moon unite in Sushumna as Kundalini merges with Paramashiva in Sahasrara!",
                "sound": "Triumphant Shankha, temple bells, and multi-octave Omkara resonance."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogi seated in luminous stillness in the cave as golden light bathes the lotus pond outside.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the awakened yogi meditating inside the granite cave overlooking a sunlit lotus pond at dawn, his form glowing with the Crest-Jewel light of Samadhi. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Wearing this Crest-Jewel of Yoga, where Prana, Bindu, Nada, and Mind become One, the yogi shines in eternal bliss beyond all bondage.",
                "vo_ta": "பிராணன், விந்து, நாதம், மனம் ஆகிய நான்கும் ஒன்றாகும் இந்த யோக சூடாமணியை அணிந்த யோகி, சகல பந்தங்களையும் கடந்து நித்திய ஆனந்தத்தில் திளைக்கிறார்.",
                "sub_cue": "Where Prana, Bindu, Nada, and Mind become One, the Yogi wears the Crest-Jewel of Bliss.",
                "sound": "Serene Bansuri and Tanpura harmony in Raga Anandabhairavi."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the sunlit lotus pond and cave sanctuary.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian granite cave sanctuary and blooming lotus pond at golden sunrise. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Yogachudamani Upanishad: tame the breath with patience, awaken the inner lotus highway, and rest in the crown of Pure Consciousness. Om Apyayantu Mamangani... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு யோகசூடாமணி உபநிடதம் நிறைவுறுகிறது: பொறுமையோடு பிராணனை வசப்படுத்தி, உள் ஆதார தாமரைகளை மலர்த்தி, தூய உணர்வின் சிகரத்தில் நிலைபெறுவோமாக. ஓம் ஆப்யாயந்து மமாங்கானி... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Awaken the inner lotus highway; rest in the Crown of Pure Consciousness. Om Shanti.",
                "sound": "Sama Veda Shanti Mantra fading into tranquil morning water ripples."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 32 (YOGA 13). MANDALABRAHMANA UPANISHAD (#48)
    {
        "story_id": "YOGA_13_MANDALABRAHMANA",
        "muktika_number": 48,
        "name_sanskrit": "मण्डलब्राह्मणोपनिषद्",
        "name_iast": "Maṇḍalabrāhmaṇopaniṣad",
        "name_tamil": "மண்டல பிராம்மண உபநிடதம்",
        "name_english": "Mandalabrahmana Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Yoga",
        "story_title_english": "Yajnavalkya Travels to Aditya-Mandala: The Five Tarakas & Shambhavi Mudra",
        "story_title_tamil": "சூரிய மண்டலம் சென்ற யாக்ஞவல்கியர்: ஐந்து தாரக ஒளிகளும் சாம்பவி முத்திரையும்",
        "characters": "Maharishi Yajnavalkya (The Great Seeker of Light), Bhagavan Aditya (Surya Narayana, The Cosmic Sun-God)",
        "verse_sanskrit": "अन्तर्लक्ष्यं बहिर्दृष्टिर्निमेषोन्मेषवर्जिता । एषा सा शाम्भवी मुद्रा सर्वतन्त्रेषु गोपिता ॥",
        "verse_tamil_translit": "அந்தர்லக்ஷ்யம் பஹிர்த்ருஷ்டிர் நிமேஷோன்மேஷவர்ஜிதா | ஏஷா ஸா ஷாம்பவீ முத்ரா ஸர்வதந்த்ரேஷு கோபிதா ||",
        "verse_meaning_english": "Fixing the attention upon the internal target while the outer gaze remains open without blinking or closing the eyelids—this is the supreme Shambhavi Mudra kept secret in all Tantras and Vedas!",
        "verse_meaning_tamil": "சித்தத்தை உள் இலக்கில் நிலைநிறுத்தி, இமைகளைக் கொட்டாமல் புறப் பார்வை திறந்திருக்கும் நிலையே சகல ஆகமங்களிலும் போற்றப்படும் ரகசியமான 'சாம்பவி முத்திரை' ஆகும்!",
        "theme": "Maharishi Yajnavalkya ascending to the Solar Orb (Aditya-Mandala) to receive from Lord Surya the science of Ashtanga Yoga, the Three Lakshyas (Antar, Bahir, Madhya), the Five Akashas (Akasha, Parakasha, Mahakasha, Suryakasha, Paramakasha), the Five Tarakas, and the supreme Amanaska Raja-Yoga through Shambhavi Mudra.",
        "SettingVisual": "Blazing golden solar sanctuary overlooking the snow-crowned Himalayas at dawn, where Yajnavalkya meditates in Shambhavi Mudra",
        "ProtagonistVisual": "Maharishi Yajnavalkya with luminous white beard and unblinking eyes in Shambhavi Mudra",
        "GuruVisual": "Bhagavan Aditya (Surya Narayana), the Purusha within the Solar Mandala",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide crane shot ascending toward a sunlit Himalayan stone terrace facing the rising golden Solar Mandala as Maharishi Yajnavalkya bows before Bhagavan Aditya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of a high Himalayan granite terrace at golden sunrise. Maharishi Yajnavalkya with flowing white beard bows with folded hands before the blazing golden solar mandala of Bhagavan Aditya. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Shukla Yajur Veda's Mandalabrahmana Upanishad, the great sage Yajnavalkya ascended to the luminous realm of Aditya-Mandala and bowed before the Purusha in the Sun: 'O Bhagavan! Expound to me the supreme Tattva of the Self and the secret of Taraka-Yoga!'",
                "vo_ta": "சுக்ல யஜுர் வேதத்தின் மண்டல பிராம்மண உபநிடதத்தில், யாக்ஞவல்கிய மகரிஷி சூரிய மண்டலத்தை அடைந்து ஆதித்ய புருஷனை வணங்கிக் கேட்டார்: 'பகவானே! ஆத்ம தத்துவத்தின் பரம ரகசியத்தையும் தாரக யோகத்தையும் எனக்கு உபதேசித்தருளுங்கள்!'",
                "sub_cue": "Yajnavalkya asks Lord Aditya: 'Reveal the supreme Atma-Tattva and the secret of Taraka-Yoga!'",
                "sound": "Golden solar Shankha blast, crisp mountain wind, and a radiant Rudra Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Yajnavalkya's eyes as three concentric rings of light (Murti-Taraka, Amurti-Taraka, and Madhya-Lakshya) shimmer between his eyebrows.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps extreme close-up shot of Maharishi Yajnavalkya's serene face in meditation; between his eyebrows shimmers a luminous golden-blue star of Taraka light reflected in his unblinking eyes. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Bhagavan Narayana in the Solar Orb replied: 'Know the Eightfold Yoga enriched by the secret of Taraka! That which ferries the soul across the ocean of rebirth is Taraka! It is twofold—Purva-Taraka (with form, between the eyebrows) and Uttara-Taraka (formless, beyond the palate)—united through the three gazes of Antar-lakshya, Bahir-lakshya, and Madhya-lakshya!'",
                "vo_ta": "சூரிய மண்டல நாராயணர் அருளினார்: 'பிறவிக் கடலைக் கடக்கச் செய்வதால் இது தாரகம் எனப்படுகிறது! புருவ மத்தியில் ஒளிரும் மூர்த்தி தாரகம், அண்ணத்திற்கு மேலே ஒளிரும் அமூர்த்தி தாரகம் என இது இருவகைப்படும்; அந்தர் லக்ஷ்யம், பஹிர் லக்ஷ்யம், மத்ய லக்ஷ்யம் எனும் மூன்று பார்வைகளால் இதனைத் தரிசிக்க வேண்டும்!'",
                "sub_cue": "That which ferries the soul across samsara is Taraka—beheld through the Three Lakshyas!",
                "sound": "Crystalline harmonic overtones and a soaring Bansuri melody in Raga Suryakantam."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Spectacular five-stage visual expansion showing the Five Akashas: from dark Akasha to fiery Parakasha, sun-bright Mahakasha, ten-million-sun Suryakasha, and blissful Paramakasha.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of Maharishi Yajnavalkya meditating on a stone dais as five expanding domes of golden and solar light—the Five Akashas—illuminate the sky around him. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Aditya unveiled the Five Cosmic Skies of Consciousness—the Pancha-Akasha: Akasha, Parakasha, Mahakasha, Tattvakasha, and Suryakasha shining with the splendor of ten million suns! Beholding the inner light without and within, the yogi burns away the five sheaths and all karmic bonds!",
                "vo_ta": "அதன்பின் உணர்வின் ஐந்து ஆகாயங்களை (பஞ்ச ஆகாசம்) சூரிய பகவான் வெளியிட்டார்: ஆகாசம், பராகாசம், மஹாகாசம், தத்வாகாசம் மற்றும் கோடி சூரியப் பிரகாசம் கொண்ட சூர்யாகாசம்! உள்ளும் புறமும் இப்பேரொளியைத் தரிசிக்கும் யோகி பஞ்ச கோசங்களையும் கர்ம தளைகளையும் சுட்டெரிக்கிறான்!",
                "sub_cue": "The Five Skies of Consciousness culminate in Suryakasha—shining like ten million suns!",
                "sound": "Five ascending orchestral Veena and Santoor chords building into solar brilliance."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Intimate close-up of Yajnavalkya practicing Shambhavi Mudra: his eyes remain gently open and unblinking while his awareness rests completely in the inner light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Maharishi Yajnavalkya in Shambhavi Mudra—his eyes gently open and completely unblinking while his gaze is turned inward into the golden light of the heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Here shines the supreme verse of Shambhavi Mudra: 'Antar-lakshyam bahir-drishtir, nimeshonmesha-varjita—fixing the awareness upon the inner target while the outer eyes remain open without blinking, this is the revered Shambhavi Mudra kept secret in all scriptures!' Just as camphor merges into fire and salt into water, the mind in Shambhavi Mudra dissolves into Brahman!",
                "vo_ta": "இங்கே சாம்பவி முத்திரையின் மகா சுலோகம் ஒலிக்கிறது: 'அந்தர்லக்ஷ்யம் பஹிர்த்ருஷ்டிர் நிமேஷோன்மேஷவர்ஜிதா — சித்தத்தை உள் இலக்கில் நிறுத்தி, இமை கொட்டாமல் புறப் பார்வை திறந்திருப்பதே சகல சாஸ்திரங்களிலும் போற்றப்படும் ரகசிய சாம்பவி முத்திரை!' கற்பூரம் தீயிலும் உப்பு நீரிலும் கரைவது போல இதில் மனம் பிரம்மத்தில் கரைகிறது!",
                "sub_cue": "अन्तर्लक्ष्यं बहिर्दृष्टिर्निमेषोन्मेषवर्जिता — Inner focus with unblinking outer gaze: this is Shambhavi Mudra!",
                "sound": "Deep, breathless Tanpura resonance with a single, unwavering Violin harmonic."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of Yajnavalkya entering Amanaska Raja-Yoga—where the mind has ceased to exist as a separate entity, leaving only the Purusha in the Solar Orb.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic shot of Maharishi Yajnavalkya seated in Amanaska Samadhi; the blazing golden orb of the rising sun aligns directly behind his crown chakra like a cosmic halo. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Transcending waking, dream, deep sleep, and Turiya, Yajnavalkya entered Amanaska—the Mindless Royal Yoga! He realized: 'That Golden Purusha who dwells in the center of the Solar Orb—He am I (Soham)! I am the spotless, non-dual Brahman!'",
                "vo_ta": "நான்கு அவஸ்தைகளையும் கடந்து யாக்ஞவல்கியர் 'அமனஸ்க' எனும் மனமற்ற ராஜயோகத்தில் புகுந்தார்! 'சூரிய மண்டலத்தின் நடுவே ஒளிரும் அந்தப் பொன்மயமான புருஷன் நானே (ஸோஹம்)! நானே களங்கமற்ற அத்வைதப் பிரம்மம்!' என உணர்ந்தார்.",
                "sub_cue": "Entering Amanaska Raja-Yoga: 'The Golden Purusha in the Solar Mandala—He am I!'",
                "sound": "Triumphant Shankha, temple bells, and Vedic choral chant of 'So-Aham'."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Yajnavalkya seated like a motionless lamp in a windless place on the Himalayan peak, radiating golden peace.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Maharishi Yajnavalkya seated like a windless lamp in samadhi on the Himalayan granite terrace, bathed in golden solar effulgence. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Like a lamp shining steady in a windless chamber, free from all mental modifications, the Jivanmukta abides in the fullness of Purnananda.",
                "vo_ta": "காற்றில்லாத இடத்தில் அசையாது சுடர்விடும் தீபத்தைப் போல, சகல மன விருத்திகளும் அற்று ஜீவன்முக்தர் பூரண ஆனந்தத்தில் நிலைபெறுகிறார்.",
                "sub_cue": "Steady as a lamp in a windless place, the Jivanmukta shines in Purnananda.",
                "sound": "Serene Bansuri and Saraswati Veena duet."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the golden Himalayan peaks and solar horizon.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the snow-crowned Himalayas bathed in golden sunrise light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Mandalabrahmana Upanishad: keep your inner gaze fixed on the Star of Consciousness while moving through the world, and realize your oneness with the Eternal Sun. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு மண்டல பிராம்மண உபநிடதம் நிறைவுறுகிறது: உலகில் வாழும்போதும் உள் பார்வையை ஆத்ம தாரகையில் நிறுத்தி, நித்திய சூரியனோடு நமது ஒருமையை உணர்வோமாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Fix your inner gaze on the Star of Consciousness; realize the Eternal Sun. Om Shanti.",
                "sound": "Shanti Mantra 'Om Purnamadah' fading into golden mountain air."
            }
        ]
    },
    # 33 (YOGA 14). SHANDILYA UPANISHAD (#58)
    {
        "story_id": "YOGA_14_SHANDILYA",
        "muktika_number": 58,
        "name_sanskrit": "शाण्डिल्योपनिषद्",
        "name_iast": "Śāṇḍilyopaniṣad",
        "name_tamil": "சாண்டில்ய உபநிடதம்",
        "name_english": "Shandilya Upanishad",
        "veda": "Atharva Veda",
        "category": "Yoga",
        "story_title_english": "Shandilya Questions Atharvan: The 10 Yamas, 10 Niyamas & The Cosmic Atman",
        "story_title_tamil": "அதர்வ மகரிஷியிடம் சாண்டில்யர் கேட்ட அஷ்டாங்க யோகமும் ஆத்ம தரிசனமும்",
        "characters": "Sage Shandilya (The Great Seeker of Yoga & Bhakti-Jnana), Maharishi Atharvan (Primordial Seer of the Atharva Veda), Dattatreya (Referenced in the Brahman-section)",
        "verse_sanskrit": "अहिंसा सत्यमस्तेयं ब्रह्मचर्यं दयार्जवम् । क्षमा धृतिर्मिताहारः शौचं चेति यमा दश ॥ तपः सन्तोष आस्तिक्यं दानमीश्वरपूजनम् । सिद्धान्तश्रवणं चैव ह्रीर्मतिश्च जपो हुतम् ॥",
        "verse_tamil_translit": "அஹிம்ஸா ஸத்யமஸ்தேயம் ப்ரஹ்மசர்யம் தயார்ஜவம் | க்ஷமா த்ருதிர் மிதாஹார: ஷௌசம் சேதி யமா தஷ ||",
        "verse_meaning_english": "Non-violence, truth, non-stealing, continence, compassion, rectitude, forgiveness, fortitude, moderate diet, and purity are the ten Yamas! Austerity, contentment, faith, charity, worship of God, hearing Vedanta, modesty, discerning intellect, Japa, and sacrifice are the ten Niyamas!",
        "verse_meaning_tamil": "அஹிம்சை, சத்தியம், திருடாமை, பிரம்மச்சரியம், தயை, நேர்மை, பொறுமை, மன உறுதி, மித ஆகாரம், தூய்மை ஆகிய பத்தும் இயமங்கள்! தவம், திருப்தி, ஆஸ்திக्यம், தானம், ஈஸ்வர பூஜை, வேதாந்த சிரவணம், நாணம், நன்மதி, ஜபம், ஹோமம் ஆகிய பத்தும் நியமங்கள்!",
        "theme": "The grand Atharva Vedic compendium of Ashtanga Yoga taught by Maharishi Atharvan to Shandilya: the complete 10 Yamas, 10 Niyamas, 8 Asanas, purification of the 14 Nadis and 10 Vayus, awakening Kundalini through the Three Granthis, Five Prathyaharas, Five Dharanas, Two Dhyanas (Saguna & Nirguna), and the crowning Shandilya-Vidya of the all-encompassing Atman.",
        "SettingVisual": "Ancient Atharva Vedic forest ashram surrounded by giant deodar trees, a crystal stream, and a carved stone yoga mandapam at golden dawn",
        "ProtagonistVisual": "Sage Shandilya in white cotton and rudraksha, bowing with earnest devotion and palm-leaf manuscripts",
        "GuruVisual": "Maharishi Atharvan, venerable patriarch of the Atharva Veda, radiating golden prana light",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide crane shot descending into an ancient Atharva Vedic deodar forest ashram at sunrise where Sage Shandilya bows before Maharishi Atharvan.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an ancient Indian deodar forest ashram at golden dawn. Sage Shandilya bows with folded hands before venerable Maharishi Atharvan seated on a carved stone dais beside a glowing homa fire. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Atharva Veda's great Shandilya Upanishad, Sage Shandilya bowed before his Guru, Maharishi Atharvan, and asked: 'O Bhagavan! Teach me the complete Eight-Limbed Ashtanga Yoga which serves as the direct gateway to the Supreme Atman!'",
                "vo_ta": "அதர்வ வேதத்தின் சாண்டில்ய உபநிடதத்தில், சாண்டில்ய முனிவர் தன் குருவான அதர்வ மகரிஷியை வணங்கிக் கேட்டார்: 'பகவானே! பரமாத்ம தரிசனத்திற்கு நேரடி வாசலாக அமையும் அஷ்டாங்க யோகத்தின் முழுமையான நெறியை எனக்கு உபதேசித்தருளுங்கள்!'",
                "sub_cue": "Shandilya asks Maharishi Atharvan: 'Teach me the complete Eight-Limbed Yoga leading to the Self!'",
                "sound": "Resonant Atharva Veda chant, morning forest birdsong, and a warm Tanpura and Rudra Veena prelude."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium tracking shot of Shandilya and fellow disciples embodying the Ten Yamas and Ten Niyamas in daily ashram life—compassion to deer, moderate pure food, and Vedanta study.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium tracking shot in a sunlit forest ashram showing Sage Shandilya gently feeding a spotted deer while fellow ascetics sit in serene study and meditation, embodying the ten Yamas and Niyamas. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Maharishi Atharvan laid down the twenty pillars of ethical foundation: the Ten Yamas—Ahimsa, Satya, Asteya, Brahmacharya, Daya, Arjava, Kshama, Dhriti, Mitahara, and Shaucha—and the Ten Niyamas—Tapas, Santosha, Astikya, Dana, Ishwara-pujana, Siddhanta-shravana, Hri, Mati, Japa, and Vrata! Without ethical purity, Yoga can never blossom!",
                "vo_ta": "அதர்வ மகரிஷி தர்மத்தின் இருபது தூண்களை நிறுவினார்: அஹிம்சை, சத்தியம், திருடாமை, பிரம்மச்சரியம், தயை, நேர்மை, பொறுமை, உறுதி, மித ஆகாரம், தூய்மை எனும் பத்து இயமங்கள்; மற்றும் தவம், திருப்தி, ஆஸ்திக्यம், தானம், ஈஸ்வர பூஜை, வேதாந்த சிரவணம், நாணம், நன்மதி, ஜபம், விரதம் எனும் பத்து நியமங்கள்!",
                "sub_cue": "10 Yamas & 10 Niyamas: the twenty ethical pillars upon which the temple of Yoga stands!",
                "sound": "Inspiring Bansuri and Mridangam composition in Raga Dharmavati."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Close-up of the yogi seated in Padmasana inside a peaceful matha, purifying the fourteen main Nadis (Sushumna, Ida, Pingala, Saraswati, Kuhu, etc.) and Ten Vayus.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Sage Shandilya seated in Padmasana inside a serene stone pavilion; subtle golden and silver streams of prana flow through fourteen luminous nadi channels toward his central spine. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Mastering the eight classical Asanas, the yogi purifies the fourteen principal Nadis—led by Ida, Pingala, and Sushumna—and the ten vital Vayus! Through three months of disciplined Nadi-shodhana Pranayama with Gayatri and Pranava, the nadis become spotless and the body grows light, luminous, and fragrant!",
                "vo_ta": "எட்டு முக்கிய ஆசனங்களில் தேர்ந்து, இடை, பிங்கலை, சுஷும்னா முதலான பதினான்கு பிரதான நாடிகளையும் பத்து வாயுக்களையும் யோகி தூய்மைப்படுத்துகிறான்! மூன்று மாத கால பிராணாயாம சாதனையால் நாடிகள் சுத்தியடைந்து உடல் இலகுவாகித் தேஜஸ் பெறுகிறது!",
                "sub_cue": "Purifying the 14 Nadis and 10 Vayus through Pranayama, the body becomes light and luminous.",
                "sound": "Rhythmic pranayama breath cycles layered with shimmering Santoor arpeggios."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Dramatic internal-external shot of Kundalini ascending through the Three Granthis (Brahma-granthi, Vishnu-granthi, Rudra-granthi) as the yogi practices the Five Pratyaharas.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a meditating Indian yogi in Siddhasana; a blazing golden-white column of Kundalini light ascends his spine, piercing three glowing energetic knots at the base, heart, and eyebrow center. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Uniting Prana and Apana through the Bandhas and Mudras, the yogi awakens Kundalini to pierce the three cosmic knots—Brahma-granthi, Vishnu-granthi, and Rudra-granthi! Practicing fivefold Pratyahara—including seeing the Self in every object the eye falls upon—and fivefold Dharana, he enters Saguna and Nirguna Dhyana!",
                "vo_ta": "பந்தங்களாலும் முத்திரைகளாலும் பிராண-அபானனை இணைத்து, பிரம்ம கிரந்தி, விஷ்ணு கிரந்தி, ருத்ர கிரந்தி எனும் மூன்று முடிச்சுகளையும் ஊடுருவச் செய்கிறான் யோகி! காணும் பொருள் அனைத்திலும் ஆத்மாவைக் காணும் ஐவகைப் பிரத்யாஹாரத்தாலும் தாரணையாலும் சகுண மற்றும் நிர்குண தியானத்தில் அவன் ஆழ்கிறான்!",
                "sub_cue": "Piercing Brahma, Vishnu, and Rudra Granthis, the Yogi enters Nirguna Dhyana!",
                "sound": "Three resonant Pakhawaj accents followed by a soaring Saraswati Veena melody."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Majestic close-up of Shandilya in Samadhi as the crowning Shandilya-Vidya of Brahman is revealed: smaller than a grain of rice, vaster than the heavens.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of Sage Shandilya in nirvikalpa samadhi at dawn; within his heart lotus shines a brilliant golden sun of Consciousness that expands to encompass the entire mountain sky. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Maharishi Atharvan imparted the supreme Brahma-Vidya: 'All this universe is indeed Brahman! Smaller than a grain of rice or mustard seed within my heart, yet vaster than the earth, the atmosphere, and all the heavens—that Self is Brahman! When Jiva and Paramatman become perfectly one in Samadhi, all vasanas perish forever!'",
                "vo_ta": "அப்போது அதர்வ மகரிஷி பரம பிரம்மவித்தையை அருளினார்: 'இப் பிரபஞ்சம் அனைத்துமே பிரம்மம்! என் இதயத்தினுள் தினையளவினும் சிறிதாய், ஆயினும் பூமிக்கும் வானத்திற்கும் மேலாய் விரிந்திருக்கும் அந்த ஆத்மாவே பிரம்மம்! ஜீவாத்மாவும் பரமாத்மாவும் சமாதியில் ஒன்றாகும்போது சகல வாசனைகளும் அழிகின்றன!'",
                "sub_cue": "Smaller than a mustard seed within the heart, yet vaster than the heavens—That Atman is Brahman!",
                "sound": "Triumphant Shankha, temple bells, and Vedic choral chant."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Shandilya and Atharvan seated in luminous oneness beneath the deodar trees, beholding the indivisible Shiva-Dattatreya Consciousness.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Maharishi Atharvan and Sage Shandilya seated in luminous samadhi in the sunlit deodar forest ashram, radiating boundless peace and bliss. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Beholding the supreme Dattatreya-Shiva Principle—one, fearless, peaceful, and luminous—Shandilya rested in the nectar of Kaivalya.",
                "vo_ta": "ஏகமாய், அச்சமற்றதாய், சாந்தமாய் ஒளிரும் தத்தாத்ரேய-சிவ தத்துவத்தை நேருக்கு நேர் தரிசித்த சாண்டில்யர், கைவல்ய அமிர்தத்தில் நிலைபெற்றார்.",
                "sub_cue": "Beholding the One Fearless Shiva-Principle, Shandilya rests in Kaivalya.",
                "sound": "Serene Violin and Tanpura sustain in Raga Shanmukhapriya."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the deodar forest ashram at golden sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian deodar forest ashram bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Shandilya Upanishad: build your life on the twenty pillars of virtue, awaken the central channel of peace, and realize the Infinite within your own heart. Om Bhadram Karnebhih... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு சாண்டில்ய உபநிடதம் நிறைவுறுகிறது: இருபது தர்மத் தூண்களின் மீது வாழ்வை அமைத்து, இதயத்து எல்லையற்ற பரம்பொருளை உணர்வோமாக. ஓம் பத்ரம் கர்ணேபி:... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Build life on virtue; realize the Infinite within the heart. Om Shanti.",
                "sound": "Atharva Veda Shanti Mantra 'Om Bhadram Karnebhih' fading into forest breeze."
            }
        ]
    },
    # 34 (YOGA 15). YOGASHIKHA UPANISHAD (#63)
    {
        "story_id": "YOGA_15_YOGASHIKHA",
        "muktika_number": 63,
        "name_sanskrit": "योगशिखोपनिषद्",
        "name_iast": "Yogaśikhopaniṣad",
        "name_tamil": "யோகசிகா உபநிடதம்",
        "name_english": "Yogashikha Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Flame-Crest of Maha-Yoga: Lord Maheshwara Instructs Pitamaha Brahma",
        "story_title_tamil": "மகாயோகத்தின் சிகரச் சுடர்: பிரம்மதேவருக்கு மகேஸ்வரன் அருளிய யோகசிகா உபநிடதம்",
        "characters": "Lord Maheshwara (Shankara, The Supreme Yogi), Pitamaha Brahma (Hiranyagarbha, The Creator Seeker), The Siddha-Yogi of Maha-Yoga",
        "verse_sanskrit": "ज्ञानं योगात्मकं விद्धि योगश्चात्मनि तिष्ठति । तयोर्द्वयोरभेदेन यः पश्यति स पश्यति ॥ अग्नौकरणमन्त्राणां वाचा सिद्धिरुदाहृता । योगेनैव तु मोक्षः स्यादिति वेदविदो विदुः ॥",
        "verse_tamil_translit": "க்ஞானம் யோகாத்மகம் வித்தி யோகஸ்சாத்மனி திஷ்டதி | தயோர்த்வயோரபேதேன ய: பஷ்யதி ஸ பஷ்யதி ||",
        "verse_meaning_english": "Know that true Knowledge is of the nature of Yoga, and Yoga abides in the Self; he who sees no difference between Jnana and Yoga, he alone truly sees! Mere verbal recitation without Yoga cannot heal the bite of samsara, just as speaking the word 'lamp' does not dispel darkness!",
        "verse_meaning_tamil": "உண்மையான ஞானம் யோக வடிவானது, யோகமோ ஆத்மாவில் நிலைபெற்றது; ஞானத்திற்கும் யோகத்திற்கும் பேதமில்லாமல் காண்பவனே உண்மையில் காண்பவன்! 'விளக்கு' என்ற சொல்லால் இருள் விலகாதது போல, யோகமில்லாத வெறும் வாய்மொழி வாதங்களால் சம்சார விஷம் நீங்காது!",
        "theme": "The encyclopedic six-chapter crown of the Yoga Upanishads taught by Lord Maheshwara to Brahma: why mere dry talk of Jnana without Yoga is like saying 'lamp' in the dark, the synthesis of Mantra-Laya-Hatha-Raja into Maha-Yoga, opening the closed door of Sushumna through Kundalini, and the Diamond Body (Vajra-deha) of the Jivanmukta.",
        "SettingVisual": "Majestic Mount Kailasa granite meditation plateau bathed in golden solar and lunar light, overlooking a vast Himalayan valley",
        "ProtagonistVisual": "Pitamaha Brahma bowing with folded hands before Lord Maheshwara",
        "GuruVisual": "Lord Maheshwara (Shankara) seated in Siddhasana on a tiger-skin/granite dais, radiating golden-white Maha-Yoga effulgence",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide crane shot over a high Kailasa granite plateau at golden sunrise where Pitamaha Brahma bows before Lord Maheshwara.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of a majestic Himalayan granite plateau at golden dawn. Pitamaha Brahma bows with folded hands before Lord Maheshwara seated in lotus posture, radiating serene golden-white yogic light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's monumental six-chapter Yogashikha Upanishad—the Flame-Crest of Yoga—Pitamaha Brahma approached Lord Shankara and asked: 'O Lord of Yogis! Why do souls bound by maya suffer in samsara, and what is the unfailing path to eternal liberation?'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் ஆறு அத்தியாயங்கள் கொண்ட மகா உபநிடதமான யோகசிகா உபநிடதத்தில், பிரம்மதேவர் சிவபெருமானை வணங்கிக் கேட்டார்: 'யோகேஸ்வரா! மாயையால் கட்டுண்ட ஜீவர்கள் ஏன் சம்சாரத்தில் உழல்கின்றனர்? நித்திய முக்திக்குத் தவறாத வழி யாது?'",
                "sub_cue": "Brahma asks Lord Maheshwara: 'What is the unfailing path from maya to eternal liberation?'",
                "sound": "Deep Kailasa Damaru and Shankha resonance, followed by a majestic Rudra Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of a dark chamber where someone merely speaks the word 'Deepa' vs. lighting an actual golden oil lamp that instantly banishes the darkness.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot inside a dark stone chamber where a sage lights a brass oil lamp with a golden flame, instantly banishing the shadows and illuminating ancient carved pillars. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Lord Maheshwara exposed the fallacy of dry intellectualism: 'Merely repeating the word lamp in the dark never dispels darkness! And merely talking of medicine never cures a disease! In the same way, mere verbal scholarship without the direct fire of Yoga can never burn away karmic vasanas! Know that Jnana and Yoga are one indivisible flame!'",
                "vo_ta": "வெறும் வாய்மொழிப் पाण्डित्यத்தின் போலித்தனத்தை மகேஸ்வரன் தோலுரித்தார்: 'இருட்டில் விளக்கு விளக்கு என்று வாயால் சொன்னால் இருள் விலகாது! மருந்தின் பெயரைச் சொன்னால் நோய் தீராது! அதுபோல யோக அக்னியில்லாத வெறும் வாதங்களால் கர்ம வாசனைகள் அழியாது! ஞானமும் யோகமும் பிரிக்க முடியாத ஒரே சுடர் என்பதை அறிவாயாக!'",
                "sub_cue": "Speaking the word 'Lamp' does not dispel darkness—unite Jnana with the living fire of Yoga!",
                "sound": "Warm ignition of a lamp flame accompanied by a resonant Saraswati Veena chord."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of a yogi uniting the Four Yogas (Mantra, Laya, Hatha, Raja) into the single golden stream of Maha-Yoga.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a radiant Indian yogi seated in Siddhasana on a mountain ledge; four streams of golden light converge from around him into a single blazing pillar of Maha-Yoga in his heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Shankara revealed the synthesis of Maha-Yoga: 'One who practices Hatha without Raja, or Raja without Hatha, never reaches perfection! Mantra Yoga, Laya Yoga, Hatha Yoga, and Raja Yoga are four rungs of one ladder called Maha-Yoga—where the breath, the nadis, and the mind dissolve into Consciousness!'",
                "vo_ta": "மகாயோகத்தின் ஒருங்கிணைப்பை ஈசன் வெளியிட்டார்: 'ராஜயோகம் இல்லாத ஹடயோகமோ, ஹடயோகம் இல்லாத ராஜயோகமோ பூரணமடையாது! மந்திர, லய, ஹட, ராஜ யோகங்கள் நான்கும் மகாயோகம் எனும் ஒரே ஏணியின் நான்கு படிகளாகும்!'",
                "sub_cue": "Mantra, Laya, Hatha, and Raja Yoga unite as the four rungs of Maha-Yoga!",
                "sound": "Four-part instrumental harmony of Veena, Bansuri, Violin, and Mridangam."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Cinematic metaphor: a householder unlocking a sealed palace gate with a golden key, dissolving into Kundalini unlocking the portal of Sushumna through Mula Bandha and Uddiyana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic close-up of an ancient ornate bronze key turning open a massive carved temple door into blinding golden light, transitioning to Kundalini rising up the spine of a meditating yogi. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Look at the sleeping Kundalini covering the mouth of Sushumna with her face! 'Just as a man opens a locked door with a key, the yogi unlocks the portal of Brahman by awakening Kundalini with the fire of Prana!' Piercing the Muladhara, Svadhishthana, Manipura, Anahata, Vishuddhi, and Ajna, she bathes in the nectar of the Moon at the crown!",
                "vo_ta": "சுஷும்னா வாசலைத் தன் முகத்தால் மூடிக்கொண்டு உறங்கும் குண்டலினியைக் காணீர்! 'பூட்டிய கதவைத் திறவுகோலால் திறப்பது போல, பிராண அக்னியால் குண்டலினியை எழுப்பி பிரம்ம வாசலைத் திறக்கிறான் யோகி!' ஆறு ஆதாரங்களையும் ஊடுருவிச் சிரசின் சந்திர மண்டல அமிர்தத்தில் அவள் நீராடுகிறாள்!",
                "sub_cue": "As one unlocks a door with a key, unlock the portal of Sushumna by awakening Kundalini!",
                "sound": "Resonant metallic unlock sound followed by a soaring, nectarine Bansuri solo."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi's body shining like a diamond (Vajra-deha) in Samadhi as the Omkara flame blazes from base to crown.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of an illumined Indian yogi in nirvikalpa samadhi; his entire form glows with a diamond-like golden-white effulgence (Vajra-deha) as the flame of Omkara shines at his crown. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "When the internal Sun and Moon are united, the yogi's body becomes Vajra-deha—impervious to disease, decay, and sorrow! Even if the heavens fall, his mind in Nirvikalpa Samadhi never wavers from the self-luminous Shiva-Atman!",
                "vo_ta": "உள் சூரியனும் சந்திரனும் இணையும்போது யோகியின் உடல் பிணியும் மூப்பும் தீண்டாத வஜ்ர தேகமாக மாறுகிறது! வானமே இடிந்து விழுந்தாலும், நிர்விகல்ப சமாதியில் நிலைபெற்ற அவரது மனம் சுயம்பிரகாச சிவ-ஆத்மாவிலிருந்து அணுவளவும் அசைவதில்லை!",
                "sub_cue": "Uniting inner Sun and Moon, the Yogi attains the fearless Diamond State of Nirvikalpa Samadhi!",
                "sound": "Triumphant Shankha, temple bells, and Vedic choral chant."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Lord Maheshwara and Pitamaha Brahma seated in luminous oneness on the Kailasa plateau.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Lord Maheshwara and Pitamaha Brahma seated in silent samadhi on the sunlit Himalayan plateau, enveloped in one seamless golden aura of Consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Realizing that the temple of the body is the macrocosm itself—with Mount Meru as the spine and all sacred rivers as the nadis—the Jivanmukta abides as the Cosmic Lord.",
                "vo_ta": "முதுகுத்தண்டே மேரு மலையாகவும், நாடிகளே புனித நதிகளாகவும் கொண்ட இவ்வுடலே பிரபஞ்ச ஆலயம் என்பதை உணர்ந்து, ஜீவன்முக்தர் விஸ்வ நாயகனாகவே வீற்றிருக்கிறார்.",
                "sub_cue": "Mount Meru is the spine, sacred rivers are the nadis—the Yogi abides as the Cosmic Lord!",
                "sound": "Expansive Rudra Veena and Tanpura sustain."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the golden Himalayan peaks at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the snow-clad Himalayan peaks bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Yogashikha Upanishad: do not stop at mere words—kindle the flame-crest of Maha-Yoga and unlock the immortal sanctuary within. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு யோகசிகா உபநிடதம் நிறைவுறுகிறது: வெறும் வார்த்தைகளில் நின்றுவிடாமல், மகாயோகத்தின் சிகரச் சுடரை ஏற்றி அகக் கருவறையைத் திறப்போமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Kindle the flame-crest of Maha-Yoga; unlock the Immortal Sanctuary within. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into serene mountain wind."
            }
        ]
    }
])

UPANISHADS_DATA.extend([
    # 35 (YOGA 16). PASUPATABRAHMANA UPANISHAD (#77)
    {
        "story_id": "YOGA_16_PASUPATABRAHMANA",
        "muktika_number": 77,
        "name_sanskrit": "पाशुपतब्राह्मणोपनिषद्",
        "name_iast": "Pāśupatabrāhmaṇopaniṣad",
        "name_tamil": "பாசுபத பிராம்மண உபநிடதம்",
        "name_english": "Pasupatabrahmana Upanishad",
        "veda": "Atharva Veda",
        "category": "Yoga",
        "story_title_english": "Vaishravana Questions Brahma: The Inner Sacrifice of the Hamsa-Sutratman & Pasupati",
        "story_title_tamil": "பிரம்மனிடம் வைஸ்ரவணன் கேட்ட ஹம்ஸ-சூத்ராத்ம அக வேள்வியும் பசுபதி தரிசனமும்",
        "characters": "Vaishravana (Kubera / Seeker of the Atharva Veda), Pitamaha Brahma (Svayambhu, The Creator Guru), Pasupati (The Lord of All Souls)",
        "verse_sanskrit": "अन्तःशरीरे निहितो गुहायामजः पुराणो निधनोऽद्वितीयः । हंसः सोऽहं परमात्मा सदाशिवः पशूनां पतिः ॥",
        "verse_tamil_translit": "அந்த:ஷரீரே நிஹிதோ குஹாயாமஜ: புராணோ நிதனோ அத்விதீய: | ஹம்ஸ: ஸோஹம் பரமாத்மா ஸதாஷிவ: பஷூனாம் பதி: ||",
        "verse_meaning_english": "Hidden in the secret cave within the body dwells the Unborn, Ancient, Eternal One without a second! He is the Hamsa—'He am I' (Soham)—the Supreme Atman, Sadashiva, the Lord of all souls (Pasupati)!",
        "verse_meaning_tamil": "உடலின் இதயக் குகையினுள் பிறப்பற்ற, பழமையான, அழிவற்ற இரண்டற்ற ஏகப் பரம்பொருள் உறைகிறது! அதுவே ஹம்ஸம்—'ஸோஹம்'—சகல உயிர்களின் நாயகனான பசுபதி சதாசிவன்!",
        "theme": "Vaishravana questioning Svayambhu Brahma on the secret of time, breath, and sacrifice: how the Hamsa-Pranava is the true Yajnopavita and Brahma-sutra, how the seeker's own inner awareness is the true Ashvamedha sacrifice, and how realizing the Pasupati within frees the Pashu (bound soul) from all fetters (Pasha).",
        "SettingVisual": "Ancient Atharva Vedic granite temple courtyard at dawn with a glowing homa altar and Himalayan peaks in the background",
        "ProtagonistVisual": "Vaishravana in dignified ancient Indian attire with rudraksha beads, bowing humbly before Svayambhu Brahma",
        "GuruVisual": "Pitamaha Brahma (Svayambhu) seated on a lotus stone throne, radiating golden Hamsa-Pranava light",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide crane shot descending into an ancient granite temple courtyard at golden sunrise where Vaishravana bows before Svayambhu Brahma.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an ancient Indian granite temple courtyard at golden dawn. Noble seeker Vaishravana bows with folded hands before Svayambhu Brahma seated on a carved lotus dais beside a sacred fire. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Atharva Veda's Pasupatabrahmana Upanishad, Vaishravana approached the Self-Born Lord Brahma and asked: 'O Bhagavan! What is the origin of the Kalas of Time and Breath? Who is the true performer of sacrifice within this body, and how does the bound soul realize Lord Pasupati?'",
                "vo_ta": "அதர்வ வேதத்தின் பாசுபத பிராம்மண உபநிடதத்தில், வைஸ்ரவணன் சுயம்பு பிரம்மதேவரை அணுகி வினவினான்: 'பகவானே! காலக் கலைகளின் மூலம் எது? இவ்வுடலினுள் உண்மையான வேள்வியை நடத்துபவர் யார்? கட்டுண்ட ஜீவன் பசுபதியை உணர்வது எவ்வாறு?'",
                "sub_cue": "Vaishravana asks Brahma: 'Who is the true performer of sacrifice within the body?'",
                "sound": "Deep temple conch, crackling sacred fire, and a solemn Rudra Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of the meditating seeker's breath as the Hamsa-Sutra weaves a golden thread of Pranava through the heart and crown.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi in padmasana; a luminous golden thread of Hamsa-Pranava light weaves through his heart and crown chakra, shining brighter than any outer cotton thread. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Brahma replied: 'The Hamsa of the breath—moving between Pranava and the heart—is the true Sutratman, the inner Sacred Thread! Without knowing this Hamsa-Sutra of three Matras, no external thread or outer sacrifice can ever make one a true Brahmana!'",
                "vo_ta": "பிரம்மதேவர் அருளினார்: 'இதயத்திற்கும் பிரணவத்திற்கும் இடையே இயங்கும் ஹம்ஸ மூச்சே உண்மையான சூத்ராத்மா—அகப் பூணூல்! மூன்று மாத்திரைகள் கொண்ட இந்த ஹம்ஸ சூத்திரத்தை அறியாமல், வெறும் புற நூலாலோ சடங்காலோ எவனும் பிரம்மஞானி ஆக முடியாது!'",
                "sub_cue": "The Hamsa-Pranava is the true Sacred Thread (Brahma-Sutra) within the heart!",
                "sound": "Rhythmic breath-synchronized Bansuri and Tanpura drone."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of the yogi seated in inner contemplation as his senses (horses) are reined in by the mind-charioteer in the inner Ashvamedha.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a serene Indian yogi meditating in a stone mandapam at sunrise, golden rays of light drawing inward from his eyes and ears into the glowing altar of his heart. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "What is the true sacrifice? 'The Atman itself is the sacrificial horse, the body is the altar, the Pranas are the priests, and offering all sense-objects into the fire of Self-Knowledge is the supreme inner Ashvamedha! For the yogi who performs this continuous inner yajna, no external ritual remains!'",
                "vo_ta": "உண்மையான யாகம் எது? 'ஆத்மாவே யாக அஸ்வம், உடலே யாகசாலை, பிராணன்களே ரித்விக்குகள், புலன் நுகர்ச்சிகளை ஆத்ம ஞானத் தீயில் ஆஹுதி அளிப்பதே பரம அஸ்வமேத யாகம்! இந்த இடைவிடாத அக வேள்வியைச் செய்யும் யோகிக்குப் புறச் சடங்குகள் தேவையில்லை!'",
                "sub_cue": "Offering sense-objects into the fire of Self-Knowledge is the true inner Ashvamedha!",
                "sound": "Majestic Pakhawaj rhythm and Saraswati Veena chords."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Visual metaphor: a royal swan gliding effortlessly across the sky and water without obstruction, dissolving to the yogi contemplating 'Hamsa Soham'.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic shot of a pure white swan gliding across golden sunlit water and rising into the open sky, transitioning to a yogi in deep meditation whose heart glows with 'Hamsa Soham' light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Just as the royal Hamsa moves freely through water, earth, and sky without ever being bound, the yogi who meditates on the Hamsa-Kala within the Sushumna sees all thirty-six Tattvas dissolve into Pure Consciousness! What is forbidden food to the ignorant becomes pure nectar of awareness to the Self-knower!",
                "vo_ta": "ராஜ ஹம்ஸம் நீரிலும் நிலத்திலும் வானிலும் தடையின்றி உலாவுவது போல, சுஷும்னாவில் ஹம்ஸ கலையைத் தியானிக்கும் யோகி முப்பத்தாறு தத்துவங்களும் தூய சைதன்யத்தில் ஒடுங்குவதைக் காண்கிறான்!",
                "sub_cue": "Meditating on the Hamsa-Kala in Sushumna, all 36 Tattvas dissolve into Pure Consciousness!",
                "sound": "Soaring Carnatic violin and flute duet in Raga Hamsanadam."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi's heart-cave where the Pashu (individual soul) drops itsasha (fetters of maya) and shines as Pasupati-Sadashiva.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of an illumined Indian yogi in samadhi; dark chains of maya dissolve into golden dust around his heart as a brilliant golden-white Shiva-jyoti blazes forth. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then shines the Pasupata realization: 'When the individual soul shakes off the Pasha—the fetter of ego and delusion—it discovers that it was never a bound Pashu at all, but Pasupati Himself—the Unborn, Ancient, Secondless Sadashiva shining in the cave of the heart!'",
                "vo_ta": "அப்போது பாசுபத ஞானம் சுடர்விடுகிறது: 'அகங்காரம், மாயை எனும் பாசத் தளையை ஜீவன் உதறித் தள்ளும்போது, தான் கட்டுண்ட பசு அல்ல, இதயக் குகையில் ஒளிரும் பிறப்பற்ற இரண்டற்ற பசுபதி சதாசிவனே தான் என்பதை உணர்கிறான்!'",
                "sub_cue": "अन्तःशरीरे निहितो गुहायाम् — Free of Pasha, the soul shines as Pasupati-Sadashiva Himself!",
                "sound": "Thunderous Damaru, Shankha, and Vedic choral chant of 'Hamsah Soham Pasupatih'."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the awakened sage beholding the entire universe as the play of one Consciousness (Chinmatra).",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Svayambhu Brahma and Vaishravana seated in luminous samadhi in the sunlit granite courtyard, surrounded by a unified golden aura. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Beholding only the Self in all directions—above, below, within, and without—the knower of Pasupata-Brahma-Vidya crosses beyond death into immortality.",
                "vo_ta": "மேலும் கீழும் உள்ளும் புறமும் ஆத்மாவை மட்டுமே தரிசிக்கும் பாசுபத பிரம்மவித்யா ஞானி, மரணத்தைக் கடந்து அமரத்துவத்தில் நிலைபெறுகிறார்.",
                "sub_cue": "Beholding the One Self in all directions, the Sage attains Immortality.",
                "sound": "Spacious Santoor and Tanpura sustain."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the granite temple courtyard at golden sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian granite temple courtyard bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Pasupatabrahmana Upanishad: wear the inner thread of Hamsa-awareness, break the fetters of ego, and shine as the Lord of Consciousness. Om Bhadram Karnebhih... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு பாசுபத பிராம்மண உபநிடதம் நிறைவுறுகிறது: ஹம்ஸ விழிப்புணர்வு எனும் அகப் பூணூலை அணிந்து, பாசத் தளையை அறுத்துப் பசுபதியாய் ஒளிர்வோமாக. ஓம் பத்ரம் கர்ணேபி:... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Break the fetters of ego; shine as the immortal Pasupati within. Om Shanti.",
                "sound": "Atharva Veda Shanti Mantra 'Om Bhadram Karnebhih' fading into morning air."
            }
        ]
    },
    # 36 (YOGA 17). YOGA-KUNDALINI UPANISHAD (#86)
    {
        "story_id": "YOGA_17_YOGAKUNDALINI",
        "muktika_number": 86,
        "name_sanskrit": "योगकुण्डल्युपनिषद्",
        "name_iast": "Yogakuṇḍalyupaniṣad",
        "name_tamil": "யோககுண்டலினி உபநிடதம்",
        "name_english": "Yoga-Kundalini Upanishad",
        "veda": "Krishna Yajur Veda",
        "category": "Yoga",
        "story_title_english": "Piercing the Three Cosmic Knots & The Khechari Science: Gautama & Sanatkumara",
        "story_title_tamil": "மூன்று கிரந்திகளைத் துளைக்கும் குண்டலினியும் கேசரி வித்தையும்: யோககுண்டலினி உபநிடதம்",
        "characters": "Lord Shiva / Sanatkumara (The Master of Kundalini & Khechari), Maharishi Gautama / The Heroic Kundalini Yogi, Goddess Shakti Kundalini",
        "verse_sanskrit": "हेतुद्वयं हि चित्तस्य वासना च समीरणः । तयोर्विनष्ट एकस्मिंस्तद्द्वावपि विनश्यतः ॥ ब्रह्मग्रन्थिं ततो भिद्ध्वा विष्णुग्रन्थिं ततः परम् । रुद्रग्रन्थिं च भिद्ध्वैव कमलं याति षोडशम् ॥",
        "verse_tamil_translit": "ஹேதுத்வயம் ஹி சித்தஸ்ய வாஸனா ச ஸமீரண: | தயோர் வினஷ்ட ஏகஸ்மின் தத் த்வாவபி வினஷ்யத: || ப்ரஹ்மக்ரந்திம் ததோ பித்வா விஷ்ணுக்ரந்திம் தத: பரம் | ருத்ரக்ரந்திம் ச பித்வைவ ||",
        "verse_meaning_english": "Twofold is the cause of the restless mind: Vasana (subtle desire-impression) and Samirana (vital breath); when either one of these two is conquered, both perish together! Piercing first the Brahma-granthi, then the Vishnu-granthi, and finally the Rudra-granthi, Kundalini ascends to the sixteen-petalled and thousand-petalled lotuses!",
        "verse_meaning_tamil": "அலைபாயும் சித்தத்திற்கு வாசனை மற்றும் பிராணன் (சமீரணன்) ஆகிய இரண்டுமே காரணங்கள்; இவற்றுள் ஒன்றை வென்றாலே இரண்டும் ஒருங்கே அடங்கிவிடும்! முதலில் பிரம்ம கிரந்தியையும், பின் விஷ்ணு கிரந்தியையும், அதன்பின் ருத்ர கிரந்தியையும் துளைத்துக்கொண்டு குண்டலினி சகஸ்ராரத்தை அடைகிறாள்!",
        "theme": "The definitive three-chapter treatise on Kundalini Yoga: conquering Chitta through its twin roots (Vasana and Prana) via Mitahara, Asana, and Shakti-chalana; Saraswati-chalana and the three Bandhas; Kundalini piercing the Three Granthis (Brahma, Vishnu, Rudra); the complete science of Khechari Mudra in Chapter 2; and Videhamukti in Chapter 3.",
        "SettingVisual": "Luminous Himalayan granite cave sanctuary at dawn where golden-white Kundalini light ascends through three glowing energetic knots",
        "ProtagonistVisual": "A heroic Krishna Yajurvedic yogi seated in Padmasana/Siddhasana practicing Shakti-chalana and Khechari Mudra",
        "GuruVisual": "Bhagavan Sanatkumara / Shiva Acharya seated in radiant lotus posture",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Slow dolly shot into a Himalayan granite cave at golden dawn where a yogi bows before the Master of Kundalini Yoga.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic dolly shot into an ancient Himalayan granite cave at golden sunrise. A resolute yogi bows with folded hands before a luminous Yoga Acharya seated on a deer-skin mat beside a brass oil lamp. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Krishna Yajur Veda's celebrated Yoga-Kundalini Upanishad, the Master opens with the golden law of the mind: 'Hetu-dvayam hi chittasya, vasana cha samiranah—twofold is the cause of the restless mind: subtle Vasanas and the vital breath Prana! When either one of these two is conquered, both are stilled together!'",
                "vo_ta": "கிருஷ்ண யஜுர் வேதத்தின் புகழ்பெற்ற யோககுண்டலினி உபநிடதம் மனதின் பொன்னான விதியோடு தொடங்குகிறது: 'ஹேதுத்வயம் ஹி சித்தஸ்ய வாஸனா ச ஸமீரண: — அலைபாயும் சித்தத்திற்கு வாசனை மற்றும் பிராண வாயு ஆகிய இரண்டுமே காரணங்கள்! இவற்றுள் ஒன்றை வசப்படுத்தினாலே இரண்டும் ஒருங்கே அடங்கிவிடும்!'",
                "sub_cue": "हेतुद्वयं हि चित्तस्य वासना च समीरणः — Vasana and Prana are the two roots of the mind; master one and both are stilled!",
                "sound": "Deep cave resonance, temple bell chime, and a focused Rudra Veena and Tanpura prelude."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Medium shot of the yogi practicing the three keys to Prana mastery: Mitahara (pure, moderate diet leaving a quarter of the stomach empty), Padmasana/Vajrasana, and Shakti-chalana.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of an ancient Indian yogi seated in rock-steady Padmasana in a sunlit stone cave, a subtle golden glow of Shakti-chalana awakening at the base of his spine. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "How does the yogi first conquer Prana? 'By three means: Mitahara—partaking of pure, sweet, nourishing food while leaving one-fourth of the stomach free; Asana—steadiness in Padmasana or Vajrasana; and third, Shakti-chalana—awakening the sleeping Kundalini through Saraswati-chalana and Kumbhaka!'",
                "vo_ta": "பிராணனை வெல்லும் மூன்று வழிகள் யாவை? 'முதலாவது மித ஆகாரம்—இனிமையான தூய உணவை வயிற்றின் கால் பங்கு காலியாக இருக்கும்படி உண்ணுதல்; இரண்டாவது பத்மாசனம் அல்லது வஜ்ராசனம்; மூன்றாவது சக்தி சாலனம்—உறங்கும் குண்டலினியை சரஸ்வதி சாலனத்தாலும் கும்பகத்தாலும் தட்டியெழுப்புதல்!'",
                "sub_cue": "Three Keys to Prana Mastery: Mitahara, Steady Asana, and Shakti-Chalana!",
                "sound": "Steady Pakhawaj pulse and ascending Bansuri phrases."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Spectacular vertical tracking shot along the yogi's spine as Kundalini, propelled by Mula, Uddiyana, and Jalandhara Bandhas, pierces the Three Cosmic Knots (Brahma, Vishnu, and Rudra Granthis).",
                "prompt": "16:9 widescreen 8K photorealistic 24fps vertical tracking shot of a meditating Indian yogi in padmasana; a blazing golden-white column of Kundalini fire rises up the Sushumna, bursting through three glowing energetic knots at the base, heart, and eyebrow center. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Applying Mula Bandha, Uddiyana Bandha, and Jalandhara Bandha, the yogi drives Prana into Sushumna! Then Kundalini blazes upward: first she pierces the Brahma-granthi of Rajas at the base; next she shatters the Vishnu-granthi of Sattva at the heart; and finally she cleaves the Rudra-granthi at the eyebrow center, ascending to the Moon of the sixteen-petalled and thousand-petalled lotuses!",
                "vo_ta": "மூலபந்தம், உட்டியான பந்தம், ஜாலந்தர பந்தம் ஆகிய மூன்று பந்தங்களால் பிராணனை சுஷும்னாவில் செலுத்துகிறான் யோகி! அப்போது குண்டலினி சுடர்விட்டெழுந்து முதலில் பிரம்ம கிரந்தியையும், பின் இதயத்தில் விஷ்ணு கிரந்தியையும், புருவ மத்தியில் ருத்ர கிரந்தியையும் உடைத்துக்கொண்டு சகஸ்ரார சந்திர மண்டலத்தை அடைகிறாள்!",
                "sub_cue": "ब्रह्मग्रन्थिं ततो भिद्ध्वा विष्णुग्रन्थिं... रुद्रग्रन्थिं च — Kundalini pierces the Three Granthis into the Crown!",
                "sound": "Three dramatic percussion crescendos resolving into a shimmering, high-register Santoor and Veena cascade."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of the yogi in Chapter 2 practicing the sacred Khechari Mudra, tasting the immortal Somadhara nectar at the crown palate while his mind soars in Chidakasha.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an illumined Indian yogi in Khechari Mudra inside a sunlit cave; a cool silvery-golden drop of Soma nectar shimmers at the crown chakra, bathing his serene face in immortal light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the second chapter, Lord Shiva reveals to Gautama the royal science of Khechari Vidya: 'Because the mind moves in Kha (the sky of Brahman) and the tongue enters the cranial vault, it is revered as Khechari! Drinking the immortal Soma nectar that flows from the thousand-petalled lotus, the yogi conquers hunger, thirst, disease, old age, and death!'",
                "vo_ta": "இரண்டாம் அத்தியாயத்தில் கேசரி வித்தையின் ரகசியம் விரிகிறது: 'மனம் சிதாகாசத்தில் சஞ்சரிப்பதாலும், நாக்கு கபால குகையில் பிரவேசிப்பதாலும் இது கேசரி எனப்படுகிறது! சகஸ்ராரத்திலிருந்து பொழியும் சோம அமிர்தத்தைப் பருகும் யோகி பசி, தாகம், பிணி, மூப்பு, மரணம் ஆகியவற்றை வெல்கிறான்!'",
                "sub_cue": "Soaring in the Sky of Consciousness through Khechari Mudra, the Yogi drinks the immortal Soma!",
                "sound": "Crystalline water-drop chimes and nectarine Violin melody in Raga Amritavarshini."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi in Chapter 3 beholding the Atman shining like a lamp inside a pot, then breaking the pot of illusion to merge with the Infinite.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of the meditating yogi in Nirvikalpa Samadhi as the three chakras and sixteen adharas dissolve into one boundless ocean of golden-white Consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the third chapter, having mastered the three Chakras, sixteen Adharas, and five Akashas, the yogi enters Nirvikalpa Samadhi! Just as the illusory snake vanishes when the rope is seen, the entire universe of names and forms vanishes into the One Indivisible Atman!",
                "vo_ta": "மூன்றாம் அத்தியாயத்தில், மூன்று சக்கரங்கள், பதினாறு ஆதாரங்கள் மற்றும் ஐந்து ஆகாயங்களைக் கடந்து யோகி நிர்விகல்ப சமாதியில் ஆழ்கிறார்! கயிற்றைக் கண்டதும் பொய்ப் பாம்பு மறைவது போல, நாம ரூபப் பிரபஞ்சம் ஏக ஆத்மாவில் கரைந்து போகிறது!",
                "sub_cue": "As the illusory snake vanishes in the rope, all duality vanishes in Nirvikalpa Samadhi!",
                "sound": "Triumphant Shankha blast and multi-octave Omkara choral resonance."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogi abiding in Videhamukti—effortless bodiless freedom even while seated on the mountain peak, like the wind resting in space.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the illumined yogi seated on a high Himalayan peak at sunrise, his translucent golden aura merging seamlessly into the boundless sky in Videhamukti. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "When Prana dissolves like wind in the sky, the yogi attains Videhamukti—bodiless, Conditioner-free immortality where there is neither rising nor setting, neither inside nor outside, only Pure Consciousness!",
                "vo_ta": "காற்று ஆகாயத்தில் ஒடுங்குவது போல் பிராணன் லயிக்கும்போது, உள்ளும் புறமும் அற்ற, உதயமும் அஸ்தமனமும் இல்லாத விதேகமுக்திப் பேரின்பத்தில் யோகி நிலைபெறுகிறார்!",
                "sub_cue": "Like wind dissolving into the sky, the Yogi attains supreme Videhamukti!",
                "sound": "Spacious Tanpura and ethereal Bansuri sustain."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the Himalayan cave and golden sunrise peaks.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the Himalayan granite cave and snow-capped peaks bathed in golden morning light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Yoga-Kundalini Upanishad: still the breath to still desire, untie the three knots of ego, and awaken the Mother Power of Consciousness within. Om Saha Navavatu... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு யோககுண்டலினி உபநிடதம் நிறைவுறுகிறது: பிராணனை அடக்கி வாசனையை வென்று, மூன்று கிரந்திகளையும் அவிழ்த்து ஆத்ம சக்தியை விழித்தெழச் செய்வோமாக. ஓம் ஸஹ நாவவது... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Still the breath, untie the three knots, and awaken Kundalini into the Infinite. Om Shanti.",
                "sound": "Shanti Mantra 'Om Saha Navavatu' fading into peaceful mountain air."
            }
        ]
    },
    # 37 (YOGA 18). DARSHANA (JABALA-DARSHANA) UPANISHAD (#90)
    {
        "story_id": "YOGA_18_DARSHANA",
        "muktika_number": 90,
        "name_sanskrit": "दर्शनोपनिषद् (जाबालदर्शनोपनिषद्)",
        "name_iast": "Darśanopaniṣad",
        "name_tamil": "தர்சன (ஜாபால தர்சன) உபநிடதம்",
        "name_english": "Darshana Upanishad",
        "veda": "Sama Veda",
        "category": "Yoga",
        "story_title_english": "Lord Dattatreya Reveals the Inner Sacred Rivers & Eight-Limbed Yoga to Sankriti",
        "story_title_tamil": "சான்கிருதிக்கு தத்தாத்ரேயர் அருளிய அகப் புனித நதிகளும் அஷ்டாங்க யோக தரிசனமும்",
        "characters": "Lord Dattatreya (Mahayogi & Incarnation of Vishnu-Shiva), Sage Sankriti (Devoted Disciple)",
        "verse_sanskrit": "शरीरं मन्दिरं प्रोक्तं सिद्धिदं सर्वदेहिनाम् । इडा भागीरथी प्रोक्ता पिङ्गला यमुना नदी । तयोर्मध्ये गता नाडी सुषुम्नाख्या सरस्वती ॥",
        "verse_tamil_translit": "ஷரீரம் மந்திரம் ப்ரோக்தம் ஸித்திதம் ஸர்வதேஹினாம் | இடா பாகீரதீ ப்ரோக்தா பிங்கலா யமுனா நதீ | தயோர்மத்யே கதா நாடீ ஸுஷும்னாக்யா ஸரஸ்வதீ ||",
        "verse_meaning_english": "This body itself is declared to be the sacred temple granting perfection to all beings! The Ida channel is the Ganges (Bhagirathi), the Pingala is the Yamuna river, and the central Sushumna between them is the sacred Saraswati—their confluence is the inner Prayaga!",
        "verse_meaning_tamil": "இந்த உடலே சகல உயிர்களுக்கும் சித்தியளிக்கும் திருக்கோயில்! இடை நாடியே கங்கை (பாகீரதி), பிங்கலை நாடியே யமுனை, இவற்றின் நடுவே செல்லும் சுஷும்னாவே சரஸ்வதி நதி—இம்மூன்றும் கூடும் இடமே அகப் பிரயாகை!",
        "theme": "Lord Dattatreya's luminous ten-chapter teaching of Ashtanga Yoga to Sage Sankriti: why every limb of Yoga culminates in non-dual Darshana (Direct Vision of the Self), how the body contains the sacred tirthas (Ida=Ganga, Pingala=Yamuna, Sushumna=Saraswati, Kashi, Prayaga, Kedara), and how bathing in the inner Triveni of Self-Knowledge grants liberation.",
        "SettingVisual": "Sacred Himalayan confluence of rivers at golden dawn under an Audumbara tree, where Lord Dattatreya instructs Sage Sankriti",
        "ProtagonistVisual": "Sage Sankriti in white bark-cloth and rudraksha, kneeling with folded hands and radiant eyes",
        "GuruVisual": "Lord Dattatreya, smiling Mahayogi seated on a granite boulder beside the river confluence, radiating golden-white light",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Wide crane shot over a sacred mountain river confluence at golden sunrise where Sage Sankriti bows before Lord Dattatreya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of a sacred Himalayan river confluence at golden dawn. Sage Sankriti kneels with folded hands before the radiant Mahayogi Lord Dattatreya seated on a granite boulder under an Audumbara tree. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Sama Veda's ten-chapter Darshana Upanishad—also revered as the Jabala-Darshana—Sage Sankriti bowed before the Great Yogi Lord Dattatreya and asked: 'O Bhagavan! Expound to me the Eight-Limbed Yoga through which the wise attain the direct Darshana—the immediate vision of the Supreme Atman!'",
                "vo_ta": "சாம வேதத்தின் பத்து அத்தியாயங்கள் கொண்ட தர்சன உபநிடதத்தில், சான்கிருதி முனிவர் மகா யோகியான பகவான் தத்தாத்ரேயரை வணங்கிக் கேட்டார்: 'பகவானே! பரமாத்மாவை நேருக்கு நேர் தரிசிக்கும் அஷ்டாங்க யோக நெறியை எனக்கு உபதேசித்தருளுங்கள்!'",
                "sub_cue": "Sankriti asks Lord Dattatreya: 'Teach me the Ashtanga Yoga that grants direct Darshana of the Self!'",
                "sound": "Rushing river confluence, morning koel birdsong, and a serene Sama Veda Tanpura and Bansuri prelude."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Dattatreya's eyes as he redefines Ahimsa, Satya, and Asteya not merely as outer rules, but as non-dual Vedantic vision.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Lord Dattatreya's serene, smiling face bathed in golden dawn light, his hand raised in jnana mudra as Sage Sankriti listens in rapt attention. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Dattatreya elevated the Ten Yamas and Ten Niyamas to the height of Advaita: 'Knowing that the Atman can never hurt or be hurt is the highest Ahimsa! Knowing that nothing exists apart from Brahman is the highest Satya! And claiming nothing as mine because all is the Self is the highest Asteya!'",
                "vo_ta": "பத்து இயமங்களையும் பத்து நியமங்களையும் அத்வைத சிகரத்திற்கு உயர்த்தினார் தத்தாத்ரேயர்: 'எங்கும் நிறைந்த ஆத்மா யாரையும் இம்சிக்காது என்ற ஞானமே உத்தம அஹிம்சை! பிரம்மத்தைத் தவிர வேறொன்றுமில்லை என்பதே உத்தம சத்தியம்! ஆத்மாவைத் தவிர தனக்கென எதுவுமில்லை என்பதே உத்தம அஸ்தேயம்!'",
                "sub_cue": "Knowing that nothing exists apart from the One Atman is the highest Ahimsa and Satya!",
                "sound": "Warm Saraswati Veena and Mridangam rhythm in Raga Chakravakam."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Spectacular anatomical-spiritual visualization: the yogi's body shining as a sacred geography of India—Mount Meru spine, Ida-Ganga, Pingala-Yamuna, and Sushumna-Saraswati meeting at the eyebrow Triveni.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic medium shot of a meditating Indian yogi in padmasana; within his torso flow three luminous streams—silvery Ida-Ganga, golden Pingala-Yamuna, and radiant white Sushumna-Saraswati—uniting at the Triveni confluence between his eyebrows. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Dattatreya revealed the inner pilgrimage of the fourth chapter: 'Why wander blindly to outer shrines while ignoring the temple of the body? Ida is the sacred Bhagirathi Ganga, Pingala is the Yamuna, and the central Sushumna between them is the hidden Saraswati! Their junction is the inner Prayaga, and between the eyebrows shines the eternal Varanasi!'",
                "vo_ta": "நான்காம் அத்தியாயத்தில் அகத் தீர்த்த யாத்திரையின் ரகசியத்தை தத்தாத்ரேயர் வெளியிட்டார்: 'உடல் எனும் திருக்கோயிலை மறந்து புறத்தே மட்டும் ஏன் அலைகிறீர்கள்? இடை நாடியே பாகீரதி கங்கை, பிங்கலையே யமுனை, நடுவே செல்லும் சுஷும்னாவே சரஸ்வதி! இம்மூன்றும் கூடும் புருவ மத்தியில் அகப் பிரயாகையும் வாரணாசியும் ஒளிர்கின்றன!'",
                "sub_cue": "इडा भागीरथी प्रोक्ता पिङ्गला यमुना नदी — Ida is Ganga, Pingala is Yamuna, Sushumna is Saraswati!",
                "sound": "Flowing three-part river harmony of Veena, Bansuri, and Violin."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of muddy water vs. crystal inner water: the yogi bathing his mind in the inner Tirtha of Pranayama and Pratyahara.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Sage Sankriti seated in deep pranayama beside the crystal river at sunrise; golden light washes through his heart lotus, purifying all mental impressions. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "If outer water alone granted liberation, would not the fish and frogs living in the Ganges be liberated first? 'True bathing is washing away the mud of ego and desire in the inner Tirtha of Self-Knowledge!' Through Pranayama—where the universe is exhaled, the Self is inhaled, and non-dual awareness is retained—the nadis become pure crystal!",
                "vo_ta": "புற நீரில் மூழ்குவதால் மட்டுமே முக்தி கிட்டுமென்றால், நதியில் வாழும் மீன்களும் தவளைகளும் முதலில் முக்தி அடையாதா? 'அகங்காரம், ஆசை எனும் சேற்றை ஆத்ம ஞான தீர்த்தத்தில் கழுவுவதே உண்மையான புனித நீராடல்!' பிரபஞ்ச மாயையை வெளிவிட்டு, ஆத்ம பாவனையை உள்வாங்கி நிலைநிறுத்தும் பிராணாயாமத்தால் நாடிகள் பளிங்கு போல் தூய்மையடைகின்றன!",
                "sub_cue": "Not outer water alone, but bathing the mind in the Triveni of Self-Knowledge grants Moksha!",
                "sound": "Gentle water chimes and rhythmic pranayama breath cycles."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic zoom into the yogi's heart and eyebrow center as Nirguna Dhyana blossoms into the direct Darshana of 'Aham Brahmasmi'.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of Sage Sankriti in Nirguna Dhyana before Lord Dattatreya; a blindingly pure golden-white sun of Consciousness shines from his heart, dissolving all duality into Samadhi. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Rising from fivefold Dharana through Saguna Dhyana into Nirguna Dhyana, the yogi beholds the direct Darshana: 'I am non-dual, spotless, timeless Consciousness! When Jiva and Paramatman become effortlessly one like space in a pot merging with cosmic space, that is Samadhi!'",
                "vo_ta": "ஐவகைத் தாரணையிலிருந்து சகுண தியானம் வழியே நிர்குண தியானத்திற்கு உயரும் யோகி நேரடி ஆத்ம தரிசனம் பெறுகிறார்: 'நானே இரண்டற்ற, களங்கமற்ற, காலமற்ற தூய சைதன்யம்! ஜீவாத்மாவும் பரமாத்மாவும் ஆகாயத்தில் ஆகாயம் கலப்பது போல் ஒன்றாவதே சமாதி!'",
                "sub_cue": "Rising into Nirguna Dhyana, Jiva and Paramatman merge into indivisible Samadhi!",
                "sound": "Triumphant Shankha, temple bells, and Vedic choral chant."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Sankriti and Dattatreya seated in luminous stillness at the river confluence, bathed in golden morning light.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Lord Dattatreya and Sage Sankriti seated in samadhi beside the Himalayan river confluence at dawn, radiating golden-white peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Having bathed in the inner Triveni and beheld the supreme Darshana of the Self, Sankriti became free of all doubts and abided in eternal bliss.",
                "vo_ta": "அகத் திரிவேணி சங்கமத்தில் நீராடி ஆத்ம தரிசனம் பெற்ற சான்கிருதி முனிவர், சகல ஐயங்களும் நீங்கி நித்திய ஆனந்தத்தில் நிலைபெற்றார்.",
                "sub_cue": "Bathing in the inner Triveni, the Sage abides in the eternal bliss of Atma-Darshana.",
                "sound": "Spacious Santoor and Bansuri harmony."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the Himalayan river confluence and Audumbara tree at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the sacred Himalayan river confluence bathed in golden sunrise light. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Darshana Upanishad: discover the sacred Ganga, Yamuna, and Saraswati flowing within your own breath, and behold the direct Darshana of the Divine within. Om Apyayantu Mamangani... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு தர்சன உபநிடதம் நிறைவுறுகிறது: நம் மூச்சினுள்ளேயே பாயும் கங்கை, யமுனை, சரஸ்வதியை உணர்ந்து, உள்ளிருக்கும் இறைவனின் நேருக்கு நேர் தரிசனத்தைப் பெறுவோமாக. ஓம் ஆப்யாயந்து மமாங்கானி... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Discover the sacred Triveni within your breath; behold the direct Darshana of the Self. Om Shanti.",
                "sound": "Sama Veda Shanti Mantra fading into gentle river waves."
            }
        ]
    },
    # 38 (YOGA 19). MAHAVAKYA UPANISHAD (#92)
    {
        "story_id": "YOGA_19_MAHAVAKYA",
        "muktika_number": 92,
        "name_sanskrit": "महावाक्योपनिषद्",
        "name_iast": "Mahāvākyopaniṣad",
        "name_tamil": "மகாவாக்ய உபநிடதம்",
        "name_english": "Mahavakya Upanishad",
        "veda": "Atharva Veda",
        "category": "Yoga",
        "story_title_english": "The Sun of Knowledge that Banishes Cosmic Darkness: Brahma's Secret of Hamsa-Vidya",
        "story_title_tamil": "அறியாமை இருளை விரட்டும் ஞான சூரியன்: பிரம்மதேவர் அருளிய மகாவாக்ய உபநிடதம்",
        "characters": "Pitamaha Brahma (The Creator Guru), The Circle of Atharva Vedic Siddha-Yogis, The Inner Aditya (Sun of Consciousness)",
        "verse_sanskrit": "नैषां तमो न गिलति न च रजो न च सत्वम् । एषोऽन्तरादित्ये हिरण्मयः पुरुषो दृश्यते । स एष जीवो विरजः परमात्मा सोऽहम् ॥",
        "verse_tamil_translit": "ஏஷோ அந்தராதித்யே ஹிரண்மய: புருஷோ த்ருஷ்யதே | ஸ ஏஷ ஜீவோ விரஜ: பரமாத்மா ஸோஹம் ||",
        "verse_meaning_english": "Darkness never swallows this Light! Within the inner Sun is beheld the Golden Purusha; that spotless Self, the Paramatman—He am I (Soham)!",
        "verse_meaning_tamil": "அறியாமை இருளால் ஒருபோதும் விழுங்க முடியாத பேரொளி இது! உள் சூரிய மண்டலத்தில் பொன்மயமான புருஷன் தரிசிக்கப்படுகிறான்; அந்தக் களங்கமற்ற பரமாத்மாவே நான் (ஸோஹம்)!",
        "theme": "Pitamaha Brahma's concise thunderbolt of Yoga-Vedanta: knowledge is not destroyed by ignorance any more than darkness can swallow the rising sun; through Hamsa-Yoga and Shambhavi Mudra, the yogi beholds the inner Aditya shining like a smokeless lamp and realizes the ultimate Mahavakya 'Hamsah Soham—Sa Esha Jivo Virajah Paramatma'.",
        "SettingVisual": "Blazing golden sunrise breaking over a dark Himalayan valley, illuminating an ancient granite cave where Pitamaha Brahma instructs the Siddha-Yogis",
        "ProtagonistVisual": "A circle of Atharva Vedic yogis seated in Siddhasana and Shambhavi Mudra, their faces lit by golden dawn rays",
        "GuruVisual": "Pitamaha Brahma radiating golden solar effulgence",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Dramatic wide time-lapse-to-24fps shot of golden sunrise breaking over a pitch-dark Himalayan valley, instantly banishing the night shadows as yogis bow before Pitamaha Brahma.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic wide shot of golden sunrise breaking over a dark Himalayan mountain valley, instantly banishing the night shadows as ancient Indian yogis bow before radiant Pitamaha Brahma on a stone terrace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the Atharva Veda's Mahavakya Upanishad, Pitamaha Brahma reveals the supreme secret of Yoga-Vedanta to the assembly of sages: 'Listen to the great declaration! Ignorance can never swallow Self-Knowledge, just as cave-darkness can never swallow the blazing rising Sun!'",
                "vo_ta": "அதர்வ வேதத்தின் மகாவாக்ய உபநிடதத்தில், பிதாமகர் பிரம்மதேவர் முனிவர்களுக்கு யோக-வேதாந்தத்தின் பரம ரகசியத்தை அருள்கிறார்: 'மகாவாக்கியத்தைக் கேளுங்கள்! உதயமாகும் சூரியனைக் குகை இருளால் விழுங்க முடியாதது போல, ஆத்ம ஞானத்தை அறியாமை இருளால் ஒருபோதும் விழுங்க முடியாது!'",
                "sub_cue": "Darkness can never swallow the rising Sun; Ignorance can never overpower Self-Knowledge!",
                "sound": "Deep cosmic Shankha blast as golden sunlight breaks, followed by a radiant Rudra Veena alapana."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of a yogi whose attention is scattered outward vs. turning the mind inward through Hamsa-Pranayama to pierce the veil of Tamas.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of an ancient Indian yogi seated in padmasana at dawn, drawing golden prana breath inward to his heart center as dark mist dissolves around him. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Brahma explained: 'Why does the soul seem bound? Because the outward-turned mind mistakes the five sheaths of food, breath, mind, intellect, and bliss for the Self! Only through the direct Yoga of Hamsa-Vidya and Pranava can the veil of Tamas and Rajas be dissolved!'",
                "vo_ta": "பிரம்மதேவர் விளக்கினார்: 'ஜீவன் ஏன் கட்டுண்டது போல் தோன்றுகிறது? வெளிமுகமாகச் செல்லும் மனம் பஞ்ச கோசங்களையே ஆத்மா என மயங்குவதால்! ஹம்ஸ வித்தை மற்றும் பிரணவ யோகத்தால் மட்டுமே தமஸ் மற்றும் ரஜோ குணத் திரைகளைக் கரைக்க முடியும்!'",
                "sub_cue": "Through Hamsa-Yoga and Pranava, dissolve the veil of the five sheaths!",
                "sound": "Rhythmic pranayama breath and a clear Bansuri melody in Raga Bhupalam."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Medium shot of the yogi uniting Apana and Prana, raising the inner energy through the Sushumna to the eyebrow center in Khechari and Shambhavi Mudra.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps medium shot of a serene Indian yogi seated in Siddhasana and Shambhavi Mudra inside a sunlit stone cave, a vertical golden beam of prana uniting his heart and eyebrow center. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Uniting Prana and Apana and ascending through the central Sushumna channel, the yogi fixes his gaze in Shambhavi and Khechari Mudra! There, at the junction of the eyebrows and crown, he beholds the inner Aditya—shining with the splendor of ten million suns!",
                "vo_ta": "பிராணனையும் அபானனையும் இணைத்து சுஷும்னா வழியே மேலேற்றி, சாம்பவி மற்றும் கேசரி முத்திரையில் நிலைபெறுகிறான் யோகி! அங்கே புருவ மத்திக்கும் சிரசிற்கும் இடையே கோடி சூரியப் பிரகாசத்துடன் ஒளிரும் உள் ஆதித்யனை அவன் தரிசிக்கிறான்!",
                "sub_cue": "In Shambhavi and Khechari Mudra, behold the inner Sun shining like ten million suns!",
                "sound": "Shimmering Santoor and Violin harmonics rising in intensity."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Macro shot of water poured into water and space inside a jar merging with cosmic space, while the inner Sun-Moon-Fire Mandala glows in the heart.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps cinematic close-up of crystal water pouring seamlessly into a calm lotus pool reflecting the golden morning sun, while a yogi meditates in luminous stillness on the bank. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Within that inner Mandala of Sun, Moon, and Fire shines the spotless Turiya-Atman! Just as water poured into water becomes one, and space inside a jar is never separate from the boundless sky, the yogi's awareness merges into the Golden Purusha within the Sun!",
                "vo_ta": "சூரிய, சந்திர, அக்னி மண்டலங்களின் நடுவே களங்கமற்ற துரிய ஆத்மா ஒளிர்கிறது! நீரில் ஊற்றிய நீர் ஒன்றாவது போலவும், குடத்து ஆகாயம் மகா ஆகாயத்தோடு ஒன்றாக இருப்பது போலவும், யோகியின் உணர்வு உள் சூரிய புருஷனோடு இரண்டறக் கலக்கிறது!",
                "sub_cue": "Within Sun, Moon, and Fire shines the spotless Turiya-Atman!",
                "sound": "Fluid Saraswati Veena and Bansuri unison."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi's face glowing like the Golden Purusha as he realizes the Mahavakya 'Sa Esha Jivo Virajah Paramatma Soham'.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of an illumined Indian yogi in samadhi; his face and heart blaze with golden solar radiance as he realizes the Mahavakya 'Soham'. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then bursts forth the living Mahavakya—not as a mere sentence on the lips, but as blazing yogic vision: 'Esho antar-aditye hiranmayah purusho drishyate—this Golden Purusha beheld within the inner Sun, this spotless Jiva, is none other than the Supreme Paramatman! He am I—Soham!'",
                "vo_ta": "அப்போது மகாவாக்கியம் வெறும் சொற்களாக அல்லாமல், சுடர்விடும் யோக தரிசனமாக வெடித்துக் கிளம்புகிறது: 'ஏஷோ அந்தராதித்யே ஹிரண்மய: புருஷோ த்ருஷ்யதே — உள் சூரியனில் தரிசிக்கப்படும் இந்தப் பொன்மய புருஷனே, இந்தக் களங்கமற்ற ஜீவனே சாட்சாத் பரமாத்மா! அவனே நான்—ஸோஹம்!'",
                "sub_cue": "स एष जीवो विरजः परमात्मा सोऽहम् — This spotless Jiva is the Supreme Paramatman: He am I!",
                "sound": "Triumphant Shankha, temple bells, and Vedic choral roar of 'Soham Paramatma'."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of the yogis seated on the sunlit Himalayan terrace, shining as the self-effulgent Shiva-Vishnu-Brahman.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of the awakened yogis seated in padmasana on the Himalayan stone terrace at sunrise, bathed in a unified ocean of golden solar consciousness. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "For him who beholds this inner Sun of Mahavakya, there is neither day nor night, neither bondage nor sorrow—he himself is Shiva, he is Vishnu, he is the Imperishable Brahman!",
                "vo_ta": "மகாவாக்கியத்தின் இந்த உள் சூரியனைத் தரிசித்தவருக்கு இரவும் இல்லை, பகலும் இல்லை; பந்தமும் இல்லை, சோகமும் இல்லை—அவரே சிவன், அவரே விஷ்ணு, அவரே அழிவற்ற பிரம்மம்!",
                "sub_cue": "Neither day nor night, neither bondage nor sorrow—he shines as the Imperishable Brahman!",
                "sound": "Spacious Tanpura and harmonic singing bowls."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the golden Himalayan valley at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the golden Himalayan mountain valley bathed in brilliant morning sunlight. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes the Mahavakya Upanishad: turn your gaze toward the inner Sun that darkness can never touch, and live the supreme truth of Soham. Om Bhadram Karnebhih... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு மகாவாக்ய உபநிடதம் நிறைவுறுகிறது: இருள் தீண்ட முடியாத உள் ஆத்ம சூரியனைத் தரிசித்து, 'ஸோஹம்' எனும் மகாவாக்கிய சத்தியத்தில் வாழ்வோமாக. ஓம் பத்ரம் கர்ணேபி:... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "Behold the inner Sun that darkness can never touch; live the truth of Soham. Om Shanti.",
                "sound": "Atharva Veda Shanti Mantra 'Om Bhadram Karnebhih' fading into golden mountain air."
            }
        ]
    },
    # 39 (YOGA 20). YOGARAJA (TARASARA / PANCHABRAHMA / PRANAGNIHOTRA YOGA) UPANISHAD (#91 / #93 / #94)
    {
        "story_id": "YOGA_20_TARASARA_YOGARAJA",
        "muktika_number": 91,
        "name_sanskrit": "तारसारोपनिषद् (योगराजोपनिषद् / प्राणाग्निहोत्रयोगः)",
        "name_iast": "Tārasāropaniṣad (Yogarājopaniṣad)",
        "name_tamil": "தாரஸார (யோகராஜ) உபநிடதம்",
        "name_english": "Tarasara (Yogaraja) Upanishad",
        "veda": "Shukla Yajur Veda",
        "category": "Yoga",
        "story_title_english": "The Royal Crown of Fourfold Yoga & The Eight-Kala Taraka Mantra: Yajnavalkya & Bharadvaja",
        "story_title_tamil": "நால்வகை யோக மகுடமும் அஷ்டகலா தாரக மந்திரமும்: யாக்ஞவல்கியர் மற்றும் பரத்வாஜர்",
        "characters": "Maharishi Bharadvaja (Devoted Seeker), Maharishi Yajnavalkya (Master of Taraka-Pranava), The Royal Yogi of Mantra, Laya, Hatha & Raja Yoga",
        "verse_sanskrit": "योगं च द्विविधं प्रोक्तं पूर्वं मन्त्रलयौ तथा । हठो राजायोगश्चेति चतुर्धा कल्पितो बुधैः ॥ ओमित्येतदक्षरं परं ब्रह्म तदेवोपास्यम् ॥",
        "verse_tamil_translit": "யோகம் ச த்விவிதம் ப்ரோக்தம் பூர்வம் மந்த்ரலயௌ ததா | ஹடோ ராஜயோகஸ்சேதி சதுர்தா கல்பிதோ புதை: | ஓமித்யேததக்ஷரம் பரம் ப்ரஹ்ம ததேவோபாஸ்யம் ||",
        "verse_meaning_english": "Yoga is expounded by the wise in four crowns: Mantra Yoga, Laya Yoga, Hatha Yoga, and Raja Yoga! And the Imperishable Syllable Om—the Taraka Brahman of eight subtle Kalas—that alone is to be meditated upon for supreme liberation!",
        "verse_meaning_tamil": "மந்திர யோகம், லய யோகம், ஹட யோகம், ராஜ யோகம் என நான்கு மகுடங்களாக ஞானிகளால் யோகம் போற்றப்படுகிறது! எட்டு சூட்சும கலைகள் கொண்ட அழிவற்ற 'ஓம்' எனும் தாரகப் பிரம்மமே பரம முக்திக்காக உபாசிக்கத்தக்கது!",
        "theme": "The grand finale of the Yoga Upanishads uniting the Tarasara (Essence of the Taraka Mantra taught by Yajnavalkya to Bharadvaja) and the Yogaraja (King of Yogas): how Mantra, Laya, Hatha, and Raja Yoga ascend through the Nine Chakras (Brahmapura) and Eight Kalas of Om Narayana into the Inner Avimukta where the Jiva shines as the Immortal Brahman.",
        "SettingVisual": "Magnificent Shukla Yajurvedic granite temple mandapam overlooking the sacred Ganges at Varanasi/Kaveri at golden dawn",
        "ProtagonistVisual": "Maharishi Bharadvaja bowing with folded hands before Maharishi Yajnavalkya",
        "GuruVisual": "Maharishi Yajnavalkya seated beside a blazing golden lamp, radiating the Eight-Kala Omkara light",
        "scenes": [
            {
                "num": 1, "window": "00:00 - 00:45",
                "title": "The Sacred Setting & The Seeker's Question (Upakrama)",
                "camera": "Majestic wide crane shot of an ancient carved granite mandapam overlooking a sacred river at golden sunrise, where Maharishi Bharadvaja bows before Maharishi Yajnavalkya.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide crane shot of an ancient Indian carved granite mandapam overlooking a sacred river at golden dawn. Maharishi Bharadvaja bows with folded hands before venerable Maharishi Yajnavalkya seated beside a glowing brass oil lamp. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In the crowning synthesis of the Tarasara and Yogaraja tradition, Maharishi Bharadvaja approached the great sage Yajnavalkya and asked: 'O Bhagavan! What is the supreme Taraka—the saving essence of Yoga and Pranava—that ferries the soul across the ocean of birth and death into Avimukta?'",
                "vo_ta": "தாரஸார மற்றும் யோகராஜ மரபின் மகுடமாக, பரத்வாஜ மகரிஷி யாக்ஞவல்கியரை அணுகிக் கேட்டார்: 'பகவானே! பிறப்பு-இறப்புப் பெருங்கடலைக் கடக்கச் செய்து அவிமுக்தப் பதத்தில் சேர்க்கும் யோகம் மற்றும் பிரணவத்தின் 'தாரக' சாரம் எது?'",
                "sub_cue": "Bharadvaja asks Yajnavalkya: 'What is the supreme Taraka-Yoga that ferries the soul across samsara?'",
                "sound": "Deep temple Shankha, flowing river waves, and a majestic Rudra Veena alapana in Raga Kalyani."
            },
            {
                "num": 2, "window": "00:45 - 01:30",
                "title": "The Encounter / The Trial of Qualification (Adhikara & Pariksha)",
                "camera": "Close-up of Yajnavalkya's radiant eyes as he points to the inner Kurukshetra and Avimukta between the eyebrows.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Maharishi Yajnavalkya's serene face bathed in golden morning light, a luminous golden star glowing between his eyebrows at the inner Avimukta center. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Yajnavalkya replied: 'Know that the body itself is Kurukshetra—the sacred field of the gods—and between Varana and Nasi, at the junction of the eyebrows, shines the eternal Avimukta! To enter that inner sanctuary, the wise practice the Royal Fourfold Yoga—Mantra, Laya, Hatha, and Raja—crowned by the Eight-Kala Taraka Pranava!'",
                "vo_ta": "யாக்ஞவல்கியர் அருளினார்: 'இந்த உடலே தேவர்களின் யாக பூமியான குருக்ஷேத்திரம்; புருவ மத்தியில் ஒளிர்வதே நித்திய அவிமுக்தம்! அந்த அகக் கருவறையில் புக மந்திர, லய, ஹட, ராஜ எனும் நால்வகை யோகத்தையும், எட்டு கலை கொண்ட தாரகப் பிரணவத்தையும் ஞானிகள் உபாசிக்கின்றனர்!'",
                "sub_cue": "Uniting Mantra, Laya, Hatha, and Raja Yoga, enter the inner Avimukta through Taraka-Pranava!",
                "sound": "Four-part harmonic chime and serene Bansuri melody."
            },
            {
                "num": 3, "window": "01:30 - 02:15",
                "title": "The First Teaching / Overcoming Outer Bonds (Purvapaksha)",
                "camera": "Vertical rising camera movement along the meditating yogi's spine, illuminating the Nine Lotuses of Brahmapura from Muladhara to Sahasrara.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps vertical rising shot of a meditating Indian yogi in padmasana; along his spine shine nine luminous chakras of golden prana light ascending from the base to the radiant crown lotus. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "In this city of Brahman—Brahmapura—shine nine luminous chakra-centres! Drawing the downward Apana upward to unite with Prana, and churning the fire of Kundalini like butter from milk, the yogi ascends through Sushumna to the crown portal!",
                "vo_ta": "பிரம்மபுரியாகிய இவ்வுடலில் ஒன்பது ஒளிச் சக்கரங்கள் மிளிர்கின்றன! அபானனை மேலேற்றிப் பிராணனுடன் இணைத்து, பாலிலிருந்து வெண்ணெய் கடைவது போல் தியானத்தால் குண்டலினிச் சுடரை எழுப்பிச் சிரசின் உச்சிக்கு உயர்கிறான் யோகி!",
                "sub_cue": "Churning Prana like butter from milk, ascend through the Nine Lotuses of Brahmapura!",
                "sound": "Ascending Saraswati Veena and Pakhawaj crescendo."
            },
            {
                "num": 4, "window": "02:15 - 03:00",
                "title": "The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)",
                "camera": "Close-up of the meditating yogi's heart and crown as the Eight Kalas of Omkara (A-kara, U-kara, Ma-kara, Bindu, Nada, Kala, Kalatita, and Paratpara) shine like eight concentric suns.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps close-up shot of Maharishi Bharadvaja in deep dhyana; eight concentric golden rings of Omkara light radiate from his heart and crown chakra in the sunlit mandapam. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Then Yajnavalkya revealed the Eight-Kala Taraka Omkara: 'A-kara is Brahma, U-kara is Vishnu, Ma-kara is Rudra, Bindu is Ishwara, Nada is Sadashiva, Kala is Shakti, Kalatita is Para-Narayana, and beyond all is the spotless Paratpara Turiya! Meditating upon this eightfold Pranava, every bond of karma is burned to ashes!'",
                "vo_ta": "அதன்பின் எட்டு கலை தாரக ஓங்காரத்தை யாக்ஞவல்கியர் வெளியிட்டார்: 'அகாரமே பிரம்மா, உகாரமே விஷ்ணு, மகாரமே ருத்ரன், விந்துவே ஈஸ்வரன், நாதமே சதாசிவன், கலையே சக்தி, கலாதிதமே நாராயணன், இவை அனைத்திற்கும் மேலானதே களங்கமற்ற பராத்பர துரியம்! இந்த அஷ்டகலா பிரணவத்தைத் தியானிக்க சகல கர்மங்களும் சாம்பலாகின்றன!'",
                "sub_cue": "Meditating on the Eight-Kala Taraka Pranava, all karmic bonds burn to ashes!",
                "sound": "Eight-layered harmonic Omkara chant resonating across three octaves."
            },
            {
                "num": 5, "window": "03:00 - 03:45",
                "title": "The Climax of Upadesha / Inner Awakening (Siddhanta)",
                "camera": "Dramatic close-up of the yogi's eyes in Shambhavi/Khechari stillness as the sound of Omkara dissolves into the Soundless Absolute.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps dramatic close-up of the illumined yogi in Raja-Yoga Samadhi; his entire form glows with golden-white solar effulgence as the morning sun rises behind the granite pillars. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Om ity etad aksharam Param Brahma, tad evopasyam—this Imperishable Syllable Om is the Supreme Brahman itself! When the triple world of waking, dream, and sleep dissolves into Turiya, the yogi realizes: 'I am that Chinmatra—Pure Consciousness alone, immortal and fearless!'",
                "vo_ta": "ஓமித்யேததக்ஷரம் பரம் ப்ரஹ்ம ததேவோபாஸ்யம் — இந்த அழிவற்ற ஓங்காரமே பரப்பிரம்மம்! விழிப்பு, கனவு, உறக்கம் ஆகிய மூன்றும் துரியத்தில் ஒடுங்கும்போது, 'நானே அமரத்துவமான, அச்சமற்ற சின்மாத்திரப் பரம்பொருள்!' என யோகி உணர்கிறார்!",
                "sub_cue": "ओमित्येतदक्षरं परं ब्रह्म — This Imperishable Om is Supreme Brahman itself!",
                "sound": "Triumphant Shankha blast, temple bells, and Vedic choral roar."
            },
            {
                "num": 6, "window": "03:45 - 04:30",
                "title": "Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)",
                "camera": "Wide shot of Yajnavalkya and Bharadvaja seated in luminous Jivanmukti oneness overlooking the sacred river at sunrise.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps wide shot of Maharishi Yajnavalkya and Maharishi Bharadvaja seated in silent samadhi in the sunlit granite mandapam overlooking the golden river at dawn. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Crowned with the royal diadem of Raja-Yoga and Sannyasa wisdom, the Jivanmukta beholds the One Self shining in every atom of existence.",
                "vo_ta": "ராஜயோகம் மற்றும் சந்நியாச ஞான மகுடம் சூடிய ஜீவன்முக்தர், பிரபஞ்சத்தின் ஒவ்வொரு அணுவிலும் ஒளிரும் ஏக ஆத்மாவையே தரிசிக்கிறார்.",
                "sub_cue": "Crowned with Raja-Yoga and Sannyasa wisdom, the Jivanmukta beholds the One Self in all.",
                "sound": "Soaring Violin, Bansuri, and Saraswati Veena symphony in Raga Sindhubhairavi."
            },
            {
                "num": 7, "window": "04:30 - 05:15",
                "title": "The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)",
                "camera": "Slow crane pull-back over the granite mandapam and golden river into the morning sky.",
                "prompt": "16:9 widescreen 8K photorealistic 24fps aerial pull-back shot over the ancient Indian granite mandapam and golden river at sunrise, radiating eternal peace. Zero modern elements, zero text, zero subtitles, zero borders.",
                "vo_en": "Thus concludes our sacred journey through the Sannyasa and Yoga Upanishads of the Muktika canon: may the fire of detachment purify our hearts, may the royal path of Yoga steady our breath, and may we awaken today to the Immortal Brahman shining within. Om Purnamadah Purnamidam... Om Shanti, Shanti, Shantihi.",
                "vo_ta": "இவ்வாறு முக்திகா உபநிடதங்களின் சந்நியாச மற்றும் யோக உபநிடதப் பயணம் இனிதே நிறைவுறுகிறது: வைராக்கியச் சுடர் நம் இதயத்தைத் தூய்மையாக்கட்டும், ராஜயோக நெறி நம் பிராணனை நிலைநிறுத்தட்டும், நமக்குள்ளேயே ஒளிரும் அமரத்துவப் பிரம்மத்தை இன்றே நாம் உணர்வோமாக. ஓம் பூர்ணமத: பூர்ணமிதம்... ஓம் சாந்தி! சாந்தி! சாந்திஹி!",
                "sub_cue": "May Vairagya and Yoga awaken us to the Immortal Brahman within. Om Shanti, Shanti, Shantihi.",
                "sound": "Grand Vedic Shanti invocation 'Om Purnamadah Purnamidam' with temple bells and river waves fading into eternal peace."
            }
        ]
    }
])


def build_youtube_metadata(item):
    cat_ta = "சந்நியாச உபநிடதம்" if item["category"] == "Sannyasa" else "யோக உபநிடதம்"
    yt_title = f"{item['name_tamil']} | {item['story_title_tamil']} | {item['name_english']} ({item['story_title_english']}) | Muktika #{item['muktika_number']}"
    yt_hook = (
        f"Discover the sacred wisdom of {item['name_english']} ({item['name_tamil']} - Muktika Canon #{item['muktika_number']}) from the {item['veda']}. "
        f"{item['story_title_english']} — {item['story_title_tamil']}."
    )
    yt_desc = (
        f"🔱 {item['name_tamil']} ({item['name_english']} - {item['name_sanskrit']}) | Muktika Upanishad #{item['muktika_number']}\n"
        f"📖 Story / Parable: {item['story_title_english']} | {item['story_title_tamil']}\n"
        f"🕉️ Associated Veda: {item['veda']} | Category: {item['category']} Upanishad ({cat_ta})\n"
        f"👥 Key Characters / Sages: {item['characters']}\n\n"
        f"✨ Core Upanishadic Sloka:\n{item['verse_sanskrit']}\n"
        f"தமிழ் ஒலிபெயர்ப்பு: {item['verse_tamil_translit']}\n\n"
        f"💡 Meaning (English): {item['verse_meaning_english']}\n"
        f"💡 பொருள் (தமிழ்): {item['verse_meaning_tamil']}\n\n"
        f"🎯 Philosophical Theme: {item['theme']}\n\n"
        f"⏱️ 7-Scene Chapter Timestamps:\n"
        f"00:00 - Scene 1: The Sacred Setting & The Seeker's Question (Upakrama)\n"
        f"00:45 - Scene 2: The Encounter / The Trial of Qualification (Adhikara & Pariksha)\n"
        f"01:30 - Scene 3: The First Teaching / Overcoming Outer Bonds (Purvapaksha)\n"
        f"02:15 - Scene 4: The Deeper Yogic / Ascetic Practice & Metaphor (Drishtanta / Sadhana)\n"
        f"03:00 - Scene 5: The Climax of Upadesha / Inner Awakening (Siddhanta)\n"
        f"03:45 - Scene 6: Direct Realization & Cosmic Vision (Samadhi / Jivanmukti)\n"
        f"04:30 - Scene 7: The Eternal Benediction & Living Wisdom (Phala Sruti & Shanti)\n\n"
        f"#Upanishads #{item['name_english'].replace(' ', '').replace('-', '')} #GuruKulaDesam #Vedanta #TamilSpiritual #{item['category']}Upanishad #Muktika108 #BharataWisdom"
    )
    yt_tags = [
        item["name_english"],
        item["name_tamil"],
        item["name_iast"],
        f"{item['category']} Upanishads",
        item["veda"],
        "108 Upanishads Tamil",
        "Muktika Upanishads",
        "Guru Kula Desam",
        "Advaita Vedanta",
        "Kundalini Yoga Upanishad" if item["category"] == "Yoga" else "Sannyasa Dharma Upanishad"
    ]
    return {
        "title_16x9": yt_title,
        "hook": yt_hook,
        "description": yt_desc,
        "tags": yt_tags
    }


def render_markdown(item, yt_meta):
    lines = []
    lines.append(f"# {item['story_id']}: {item['name_english']} ({item['name_tamil']} / {item['name_sanskrit']})")
    lines.append("")
    lines.append("## 1. Header & Metadata")
    lines.append("")
    lines.append(f"- **Story ID**: `{item['story_id']}`")
    lines.append(f"- **Muktika Upanishad Number**: #{item['muktika_number']} (of 108)")
    lines.append(f"- **Upanishad Name (Sanskrit)**: {item['name_sanskrit']}")
    lines.append(f"- **Upanishad Name (IAST)**: *{item['name_iast']}*")
    lines.append(f"- **Upanishad Name (Tamil)**: {item['name_tamil']}")
    lines.append(f"- **Upanishad Name (English)**: {item['name_english']}")
    lines.append(f"- **Associated Veda**: {item['veda']}")
    lines.append(f"- **Category**: `{item['category']}`")
    lines.append(f"- **Story / Parable Title (English)**: {item['story_title_english']}")
    lines.append(f"- **Story / Parable Title (Tamil)**: {item['story_title_tamil']}")
    lines.append(f"- **Key Characters / Sages / Deities**: {item['characters']}")
    lines.append("")
    lines.append("### Core Upanishadic Verse")
    lines.append(f"- **Sanskrit Sloka**:\n  > {item['verse_sanskrit']}")
    lines.append(f"- **Tamil Transliteration**:\n  > {item['verse_tamil_translit']}")
    lines.append(f"- **English Meaning**: {item['verse_meaning_english']}")
    lines.append(f"- **Tamil Meaning (தமிழ் பொருள்)**: {item['verse_meaning_tamil']}")
    lines.append("")
    lines.append("### Philosophical & Moral Theme")
    lines.append(f"{item['theme']}")
    lines.append("")
    lines.append("### YouTube Metadata Block (16:9 Long-Form)")
    lines.append(f"- **16:9 Title**: `{yt_meta['title_16x9']}`")
    lines.append(f"- **Opening Hook**: {yt_meta['hook']}")
    lines.append(f"- **Tags**: `{', '.join(yt_meta['tags'])}`")
    lines.append("- **Description**:")
    lines.append("```text")
    lines.append(yt_meta["description"])
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Locked Visual Continuity Bible")
    lines.append("")
    lines.append(f"- **Primary Setting & Architecture**: {item['SettingVisual']} ({LOCKED_VISUAL_BIBLE['aesthetic']}).")
    lines.append(f"- **Protagonist / Seeker Lock**: {item['ProtagonistVisual']}.")
    lines.append(f"- **Guru / Deity Lock**: {item['GuruVisual']}.")
    lines.append(f"- **Resolution & Frame Rate**: {LOCKED_VISUAL_BIBLE['resolution_fps']}.")
    lines.append(f"- **Lighting & Atmosphere**: {LOCKED_VISUAL_BIBLE['lighting']}.")
    lines.append(f"- **Costume & Props**: {LOCKED_VISUAL_BIBLE['costume_props']}.")
    lines.append(f"- **Hard Exclusions**: {LOCKED_VISUAL_BIBLE['hard_exclusions']}.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Full 7-Scene Detailed Breakdown (16:9 Widescreen Production)")
    lines.append("")

    for sc in item["scenes"]:
        lines.append(f"### Scene {sc['num']} ({sc['window']}): {sc['title']}")
        lines.append("")
        lines.append(f"- **Scene Title & Duration Window**: Scene {sc['num']} ({sc['window']}) — {sc['title']}")
        lines.append(f"- **Camera & Cinematography**: {sc['camera']}")
        lines.append(f"- **Google Flow / Veo 16:9 Video Generation Prompt**:")
        lines.append(f"  > `{sc['prompt']}`")
        lines.append(f"- **Voiceover / Narration Script (English)**:")
        lines.append(f"  > \"{sc['vo_en']}\"")
        lines.append(f"- **Voiceover / Narration Script (Tamil - செந்தமிழ் உரைநடை)**:")
        lines.append(f"  > \"{sc['vo_ta']}\"")
        lines.append(f"- **On-Screen Subtitle / Verse Cue**: `{sc['sub_cue']}`")
        lines.append(f"- **Sound Design & Sangeetham Cue**: {sc['sound']}")
        lines.append("")

    return "\n".join(lines)


def slugify(text):
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return s


def main():
    os.makedirs(SANNYASA_DIR, exist_ok=True)
    os.makedirs(YOGA_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)

    sannyasa_count = 0
    yoga_count = 0
    enriched_records = []

    for item in UPANISHADS_DATA:
        yt_meta = build_youtube_metadata(item)
        md_content = render_markdown(item, yt_meta)

        if item["category"] == "Sannyasa":
            sannyasa_count += 1
            fname = f"{sannyasa_count:02d}_muktika_{item['muktika_number']:03d}_{slugify(item['name_english'])}.md"
            out_path = os.path.join(SANNYASA_DIR, fname)
        else:
            yoga_count += 1
            fname = f"{yoga_count:02d}_muktika_{item['muktika_number']:03d}_{slugify(item['name_english'])}.md"
            out_path = os.path.join(YOGA_DIR, fname)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        record = dict(item)
        record["youtube_metadata"] = yt_meta
        record["locked_visual_continuity_bible"] = {
            **LOCKED_VISUAL_BIBLE,
            "setting_visual": item["SettingVisual"],
            "protagonist_visual": item["ProtagonistVisual"],
            "guru_visual": item["GuruVisual"]
        }
        record["markdown_file"] = out_path
        enriched_records.append(record)

    dataset = {
        "agent": "Agent 2: Sannyasa & Yoga Upanishads Story & 7-Scene Screenplay Architect",
        "total_upanishads": len(enriched_records),
        "sannyasa_upanishads_count": sannyasa_count,
        "yoga_upanishads_count": yoga_count,
        "locked_visual_bible_defaults": LOCKED_VISUAL_BIBLE,
        "upanishads": enriched_records
    }

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Generated {sannyasa_count} Sannyasa Upanishads in {SANNYASA_DIR}")
    print(f"Generated {yoga_count} Yoga Upanishads in {YOGA_DIR}")
    print(f"Saved JSON dataset ({len(enriched_records)} total entries) to {JSON_OUT}")


if __name__ == "__main__":
    main()
