#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 5: Group 5 — Sannyasa (19 Canon Texts) & Yoga (20 Canon Texts) Upanishads
Ultra-Detailed 5-Minute Google Flow Screenplay & 35-Shot Story Architect.

Upgrades all 39 Upanishad stories (19 Sannyasa + 20 Yoga) so that:
1. Every Story has a Complete Unabridged Storyline & Character Continuity Bible (multi-paragraph
   English and Senthamizh storyline + detailed visual locks for Guru, Seeker, Deity, Hermitage/Cave/Temple,
   and Yogic/Ascetic symbols so Google Flow maintains 100% continuity across all 35 shots).
2. Every one of the 7 Scenes (~45s each) in every story is expanded to include:
   - Dramatic Story & Philosophical Dialogue Beat (Upakhyana & Samvada)
   - 5 Distinct 9-Second Continuous 16:9 8K Google Flow / Veo Prompts:
     * Shot A (00s–09s): Wide Anamorphic Establishing / Forest Hermitage, Himalayan Cave, or Temple Dawn Shot
     * Shot B (09s–18s): Medium Tracking Shot on the Ascetic / Yogi / Guru Action & Mudra
     * Shot C (18s–27s): Macro / Close-Up Shot on the Sacred Symbol, Yogic Prana / Chakra / Sushumna Metaphor, Kamandalu, Danda, or Facial Stillness
     * Shot D (27s–36s): Over-the-Shoulder / Two-Shot Guru-Shishya Dialogue & Inner Awakening
     * Shot E (36s–45s): Slow Crane Ascent / Atmospheric Transition Shot bridging into the next scene
   - Expanded 45-Second Dramatic Narration & Dialogue in English (~115–135 words per scene, ~850–950 words per film)
   - Expanded 45-Second Dramatic Narration & Dialogue in Senthamizh (செந்தமிழ் உரைநடை) (~115–135 words per scene)
   - On-Screen Subtitle Cues & Sound Design / Sangeetham Score
3. Overwrites all .md files in:
   - /home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/03_sannyasa_upanishads/
   - /home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/04_yoga_upanishads/
   and updates /home/shishyan/GitHub/GuruKulaDesam/data/upanishads/agent2_sannyasa_yoga.json.
"""

import os
import re
import json
import sys

BASE_DIR = "/home/shishyan/GitHub/GuruKulaDesam"
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
SANNYASA_DIR = os.path.join(BASE_DIR, "production", "upanishad_stories", "03_sannyasa_upanishads")
YOGA_DIR = os.path.join(BASE_DIR, "production", "upanishad_stories", "04_yoga_upanishads")
JSON_OUT = os.path.join(BASE_DIR, "data", "upanishads", "agent2_sannyasa_yoga.json")

sys.path.insert(0, TOOLS_DIR)
import build_upanishad_agent2_sannyasa_yoga as base_builder

LOCKED_VISUAL_BIBLE = base_builder.LOCKED_VISUAL_BIBLE

# Specific Storyline & Symbolism Enrichment Registry for all 39 Upanishads
STORY_ENRICHMENTS = {
    "SANNYASA_01_BRAHMA": {
        "guru_name": "Sage Pippalada",
        "seeker_name": "Maharishi Shaunaka",
        "guru_tamil": "பிப்பலாத முனிவர்",
        "seeker_tamil": "சௌனக மகரிஷி",
        "deity_focus": "The All-Pervading Atman-Purusha of the Four States (Wakefulness, Dream, Deep Sleep, and Turiya) shining as the inner Sacred Thread (Brahma-Sutra)",
        "ascetic_symbols": "Triple white cotton Yajnopavita (sacred thread), wooden Arani fire-churning sticks, four earthen oil lamps (representing Jagarita, Svapna, Sushupti, Turiya), white sesame seeds, clarified butter (ghee), kamandalu, and the golden inner thread of pure Consciousness",
        "sadhanas_en": "meditating upon the four seats of the Purusha (eye, throat, heart lotus, and crown), churning the body as the lower fire-stick with Omkara as the upper drill, and replacing the external cotton thread with the imperishable thread of Supreme Brahman",
        "sadhanas_ta": "விழிப்பு, கனவு, ஆழ்ந்த உறக்கம், துரியம் ஆகிய நான்கு அவஸ்தைகளின் இருப்பிடங்களைத் தியானித்து, உடலைக் கீழ்க்கட்டையாகவும் ஓங்காரத்தை மேல்கட்டையாகவும் கொண்டு தியான அக்னியைக் கடைந்து, புறப் பருத்திப் பூணூலை விடுத்து பரப்பிரம்மத்தையே நித்திய அகப் பூணூலாகத் தரிக்கும் சாதனை",
    },
    "SANNYASA_02_JABALA": {
        "guru_name": "Maharishi Yajnavalkya",
        "seeker_name": "Deva Guru Brihaspati, King Janaka of Videha, and Sage Atri",
        "guru_tamil": "மகரிஷி யாக்ஞவல்கியர்",
        "seeker_tamil": "தேவகுரு பிரகஸ்பதி, விதேக மன்னன் ஜனகர் மற்றும் அத்ரி முனிவர்",
        "deity_focus": "Lord Rudra-Shiva dwelling in the inner Avimukta (Varanasi) between the eyebrows and nose-bridge (Varana and Nasi), whispering the Taraka Mantra of Immortality",
        "ascetic_symbols": "Luminous indigo-golden Ajna lotus between the eyebrows, royal Videha gold crown set aside on granite, Prajapatya homa altar, internalized Prana-fire, and the emblem-free Paramahamsa state",
        "sadhanas_en": "discovering the inner Varanasi at the junction of Varana and Nasi between the eyebrows, embracing Sannyasa the very day detachment (Vairagya) dawns regardless of life-stage, merging external ritual fires into the vital breath, and wearing the Atman alone as one's Yajnopavita",
        "sadhanas_ta": "புருவ மத்தியில் வரணா மற்றும் நாசி இணையும் அக வாரணாசியைக் கண்டு, மனதில் வைராக்கியம் பிறக்கும் அன்றே சந்நியாசம் மேற்கொண்டு, புற யாக அக்னியைத் தன் பிராணனில் ஒடுக்கி, ஆத்மாவையே உண்மையான பூணூலாக உணரும் சாதனை",
    },
    "SANNYASA_03_ARUNI": {
        "guru_name": "Lord Prajapati",
        "seeker_name": "Sage Aruni (Uddalaka Aruni)",
        "guru_tamil": "பகவான் பிரஜாபதி",
        "seeker_tamil": "ஆருணி மகரிஷி",
        "deity_focus": "Lord Prajapati and the Cosmic Sun of Non-Dual Consciousness proclaimed in the Sama Veda ('Aham Annam Aham Annadah')",
        "ascetic_symbols": "Single bamboo staff (Vainava Danda), wooden sacrificial ladles released into a crystal Himalayan stream, loincloth (kaupina), cupped palms receiving alms as medicine, and blazing solar prana",
        "sadhanas_en": "relinquishing all karmic rituals, familial ties, and desires for the seven worlds from Bhurloka to Satyaloka, proclaiming the three fearless cries 'Chittam! Chittam! Chittam!' (Severed is the knot of ignorance!), taking alms strictly as medicine, and chanting the Sama Veda roar of universal oneness",
        "sadhanas_ta": "பூலோகம் முதல் சத்தியலோகம் வரையிலான ஏழு உலக ஆசைகளையும் உறவுகளையும் சடங்குகளையும் எச்சமின்றித் துறந்து, 'அறியாமைத் தளை அறுந்தது!' என மும்முறை முழங்கி, உணவை மருந்தாக மட்டுமே ஏற்று, 'நானே உணவு, நானே உண்பவன்' எனும் சாம கானத்தில் திளைக்கும் சாதனை",
    },
    "SANNYASA_04_PARAMAHAMSA": {
        "guru_name": "Bhagavan (The Supreme Adi Guru)",
        "seeker_name": "Devarishi Narada",
        "guru_tamil": "பகவான் ஆதிகுரு",
        "seeker_tamil": "தேவரிஷி நாரதர்",
        "deity_focus": "The Supreme Purusha of Infinite Bliss (Purnananda-eka-bodha Brahman) who dwells perpetually within the heart of the rare Paramahamsa",
        "ascetic_symbols": "Royal white swans (Hamsa) gliding untouched on a lotus lake, Narada's carved Mahati Veena, platter of gold coins ignored like dust, the sky as garment (Digambara), and the luminous inner Jnanadanda (Staff of Pure Knowledge)",
        "sadhanas_en": "transcending the six waves of existence (hunger, thirst, sorrow, delusion, old age, and death), refusing even to glance at gold with desire, discarding the wooden staff to hold the indivisible Jnanadanda of Self-Knowledge, and resting in Purnananda beyond all struggle",
        "sadhanas_ta": "பசி, தாகம், சோகம், மோகம், மூப்பு, மரணம் எனும் ஆறு ஊர்மிகளைக் கடந்து, பொன்னை ஆசையோடு பார்ப்பதையும் தவிர்த்து, மரத்தண்டத்திற்குப் பதில் 'ஞானதண்டம்' எனும் அக அறிவுக் கோலை ஏந்தி, பூரண ஆனந்தப் பிரம்மத்தில் நிலைபெறும் சாதனை",
    },
    "SANNYASA_05_MAITREYI": {
        "guru_name": "Sage Shakayanya & Lord Paramashiva",
        "seeker_name": "King Brihadratha & Goddess Maitreyi / Sage Maitreya",
        "guru_tamil": "சாகாயண்ய முனிவர் மற்றும் பரமசிவன்",
        "seeker_tamil": "மன்னன் பிருஹத்ரதன் மற்றும் மைத்ரேயி",
        "deity_focus": "Kevala Shiva (The Pure Non-Dual Self) enshrined within the living temple of the physical body ('Deho Devalayah Proktah')",
        "ascetic_symbols": "Austere bark-cloth (valkala), smokeless fire aura of Sage Shakayanya, natural stone Shiva Lingam, faded flowers of ignorance cast aside, and golden lotus petals of 'Soham' (He am I) awareness",
        "sadhanas_en": "cultivating intense dispassion (Vairagya) toward the transient physical body, purifying the mind (Chitta-shuddhi) until thoughts dissolve like salt in water, and performing the supreme inner Shiva-Puja without external flowers by bathing the mind in purity and abiding in Sahaja Samadhi",
        "sadhanas_ta": "நிலையற்ற உடலின் மீது தீவிர வைராக்கியம் கொண்டு, நீரில் உப்பு கரைவது போல் மன மாசுகளைக் கரைத்து, இவ்வுடலையே ஆலயமாகவும் ஜீவனையே சிவனாகவும் உணர்ந்து, 'ஸோஹம்' பாவனையால் மலரில்லா அகச் சிவபூஜை புரியும் சாதனை",
    },
    "SANNYASA_06_NIRVANA": {
        "guru_name": "The Supreme Avadhuta Master",
        "seeker_name": "The Circle of Dikshita Disciples in the Ajapa Matha",
        "guru_tamil": "பரம அவதூத குரு",
        "seeker_tamil": "அஜபா மடத்துத் தீக்ஷித சீடர்கள்",
        "deity_focus": "Akshayya Niranjana Parabrahman (The Imperishable, Spotless Absolute) realized through the sky-vast doctrine of Gagana-Siddhanta",
        "ascetic_symbols": "Boundless open sky canopy (Gagana-siddhanta), crystal mountain waterfall (Amrita-kallola-nadi), patched garment of cosmic consciousness, staff of fearless Samadhi, and the Western Sushumna channel",
        "sadhanas_en": "decoding the mystical twilight language (Sandhya-bhasha) of the Avadhuta where unuttered Ajapa breath is the monastery, compassion toward all beings is the begging bowl, discrimination is the loincloth, and ascending through the Western Sushumna pathway into Sahaja Samadhi",
        "sadhanas_ta": "உச்சரிக்கப்படாத அஜபா மூச்சையே மடமாகவும், சர்வபூத கருணையையே பிட்சைப் பாத்திரமாகவும், விவேகத்தையே ஆடையாகவும், நிர்விகல்ப சமாதியையே தண்டமாகவும் கொண்டு, பஸ்சிம சுஷும்னா வழியே சஹஜ சமாதியில் ஆழும் ககன சித்தாந்த சாதனை",
    },
    "SANNYASA_07_NARADAPARIVRAJAKA": {
        "guru_name": "Devarishi Narada & Pitamaha Brahma",
        "seeker_name": "Maharishi Shaunaka & the 88,000 Rishis of Naimisharanya",
        "guru_tamil": "தேவரிஷி நாரதர் மற்றும் பிதாமகர் பிரம்மா",
        "seeker_tamil": "சௌனக மகரிஷி மற்றும் நைமிசாரண்ய முனிவர்கள்",
        "deity_focus": "The Sixteen-Kala Taraka Pranava Brahman into which all rivers of individual names and forms merge like the ocean",
        "ascetic_symbols": "Narada's Mahati Veena, six ascending stone tiers representing the six orders of Sannyasins (Kutichaka to Avadhuta), a honeybee on a lotus (Madhukara-vritti), a tortoise withdrawing its limbs, and the 16-petalled golden wheel of Omkara",
        "sadhanas_en": "fulfilling the ten foundational vows of Ahimsa, Satya, Asteya, and Brahmacharya, ascending through the six rungs of renunciation, gathering alms like a gentle honeybee without bruising the flower, and meditating upon the sixteen subtle Kalas of Omkara across the four states of consciousness",
        "sadhanas_ta": "அஹிம்சை, சத்தியம் முதலான பத்து விரதங்களில் நிலைத்து, குடீசகர் முதல் அவதூதர் வரையிலான ஆறு படிகளில் உயர்ந்து, மலரை நோகடிக்காத வண்டைப் போல மதுகர விருத்தியில் உணவேற்று, பதினாறு கலை ஓங்காரத்தை நான்கு அவஸ்தைகளிலும் தியானிக்கும் சாதனை",
    },
    "SANNYASA_08_BHIKSHUKA": {
        "guru_name": "The Lineage of Paramahamsa Masters (Shuka, Dattatreya, Jada Bharata, Aruni)",
        "seeker_name": "The Four Orders of Mendicant Monks (Kutichaka, Bahudaka, Hamsa, Paramahamsa)",
        "guru_tamil": "சுகர், தத்தாத்ரேயர், ஜடபரதர் உள்ளிட்ட பரமஹம்ச குரு பரம்பரை",
        "seeker_tamil": "முக்தி நாடும் நான்கு வகை பிட்சுக்கள்",
        "deity_focus": "The Non-Dual Atman beheld equally in a clod of earth, a stone, and gold through the path of pure Yoga",
        "ascetic_symbols": "Triple bamboo staff (Tridanda), single bamboo staff (Ekadanda), leaf alms-bowl with eight morsels, a clod of earth beside a stone and a piece of gold, and an ancient unroofed temple overgrown with banyan roots",
        "sadhanas_en": "progressing from the thirty-two morsels of the hermitage-dwelling Kutichaka to the eight bee-gathered morsels of the Bahudaka, the one-night village stay of the Hamsa, and the supreme emblem-free Yoga of the Paramahamsa who sees earth, stone, and gold as one",
        "sadhanas_ta": "குடீசகர், பஹூதகர், ஹம்சர் ஆகிய நிலைகளைக் கடந்து, எட்டு கவள உணவை மட்டுமே யோக உடலின் பொருட்டு ஏற்று, மண்ணையும் கல்லையும் பொன்னையும் சமமாகக் கண்டு, சுகர் மற்றும் ஜடபரதர் வழியில் மோட்சத்தை மட்டுமே நாடும் பரமஹம்ச சாதனை",
    },
    "SANNYASA_09_TURIYATITA_AVADHUTA": {
        "guru_name": "Lord Adinarayana",
        "seeker_name": "Pitamaha Brahma & The Turiyatita Avadhuta Sage",
        "guru_tamil": "பகவான் ஆதிநாராயணர்",
        "seeker_tamil": "பிதாமகர் பிரம்மதேவர் மற்றும் துரீயாதீத அவதூதர்",
        "deity_focus": "Lord Adinarayana as the Veda-Purusha and the Turiyatita Absolute beyond even the fourth state of consciousness",
        "ascetic_symbols": "High Himalayan lotus lake, spotted deer grazing fearlessly beside a motionless yogi, discarded staff and water-pot at a sunlit cave mouth, and concentric rings of non-dual Pranava light",
        "sadhanas_en": "ripening step-by-step from Kutichaka to Paramahamsa and finally into the ultra-rare Turiyatita Avadhuta, practicing Gopravartika (partaking of unasked sustenance like a gentle cow), living with childlike egolessness without blessing or cursing, and dissolving waking, dream, and sleep in Pranava",
        "sadhanas_ta": "குடீசகர் முதல் பரமஹம்சர் வரை படிப்படியாகப் பக்குவமடைந்து, தண்டம் மற்றும் கமண்டலத்தையும் விடுத்து, பச்சிளம் குழந்தையைப் போல் மான-அவமானம் கடந்து, மூன்று அவஸ்தைகளையும் பிரணவத்தில் ஒடுக்கித் துரீயாதீத அவதூத நிலையில் திளைக்கும் சாதனை",
    },
    "SANNYASA_10_BRIHAT_SANNYASA": {
        "guru_name": "The Venerable Sama Vedic Acharya",
        "seeker_name": "The Assembly of Sama Vedic Forest Ascetics",
        "guru_tamil": "சாம வேத சந்நியாச ஆச்சாரியர்",
        "seeker_tamil": "சாம வேத வனத் துறவிகள்",
        "deity_focus": "The Changeless Witness Brahman, unshakeable like Mount Meru amidst the changing costumes of phenomenal life",
        "ascetic_symbols": "Vaisvanara homa fire inhaled into the breath, clay and bottle-gourd bowls (shunning gold, silver, and copper), a motionless python on a warm boulder (Ajagara-vritti), and a honeybee on forest blossoms",
        "sadhanas_en": "internalizing the Vaisvanara fire into one's own Prana, strictly shunning the six pitfalls of pseudo-asceticism (coveting fine bowls, fixed huts, pride of discipleship, and trading in mantras), living by Madhukara or python-like Ajagara-vritti, and witnessing the body like an actor changing costumes",
        "sadhanas_ta": "வைஸ்வானர அக்னியைத் தன் பிராணனில் உள்வாங்கி, பொன்-வெள்ளிப் பாத்திரங்களையும் போலித் துறவின் ஆறு பொறிகளையும் முற்றிலும் தவிர்த்து, மலைப்பாம்பைப் போன்ற அஜகர விருத்தியிலும் மதுகர விருத்தியிலும் வாழ்ந்து, நாடக நடிகனைப் போல் உடலின் செயல்களுக்குச் சாட்சியாக நிற்கும் சாதனை",
    },
    "SANNYASA_11_PARAMAHAMSA_PARIVRAJAKA": {
        "guru_name": "Bhagavan Adinarayana",
        "seeker_name": "Pitamaha Brahma & The Noble Seeker Weary of Samsara",
        "guru_tamil": "பகவான் ஆதிநாராயணர்",
        "seeker_tamil": "பிதாமகர் பிரம்மதேவர் மற்றும் முமுக்ஷு சாதகன்",
        "deity_focus": "The Eightfold Ashtanga Pranava Brahman proclaimed in the fearless lion-roar 'Ahameva Param Brahma'",
        "ascetic_symbols": "Fourfold qualification (Sadhana Chatushtaya), Viraja homa altar by a mountain river, open palms granting Abhaya (total fearlessness) to all creatures, and an eight-petalled golden lotus of Ashtanga Pranava in the heart",
        "sadhanas_en": "awakening from the exhaustion of sense-pleasures with the fourfold qualification (Viveka, Vairagya, Shat-sampatti, Mumukshutva), proclaiming the vow of universal fearlessness ('Abhayam Sarvabhutebhyah'), and meditating upon the eight limbs of Pranava (A, U, M, Ardhamatra, Nada, Bindu, Kala, Taraka)",
        "sadhanas_ta": "சாதன சதுஷ்டயத்துடன் விரஜா ஹோமம் செய்து, மூவுலக உயிர்களுக்கும் அபயம் அளித்து, மௌனமே தண்டமாகவும் ஆகாயமே பாத்திரமாகவும் கொண்டு, அஷ்டாங்க பிரணவ தியானத்தால் 'நானே பரப்பிரம்மம்' எனும் சிம்ம கர்ஜனையில் நிலைபெறும் சாதனை",
    },
    "SANNYASA_12_KUNDIKA": {
        "guru_name": "The Illumined Forest Guru",
        "seeker_name": "The Venerable Vanaprastha Elder Awakening into a Sky-Clad Yogi",
        "guru_tamil": "அக ஒளி கொண்ட வன குரு",
        "seeker_tamil": "வானப்பிரஸ்த முதியவர் / ஆகாய யோகி",
        "deity_focus": "Chidakasha Parabrahman—the Eternally Pure, Awakened, and Free Self ('Nityam Shuddho Buddho Muktah Svabhavatah')",
        "ascetic_symbols": "Traditional dried gourd water-pot (Kundika) beside a crystal mountain spring, clean white river sand as a bed, one's own folded arm as a pillow, water drops rolling off a lotus leaf, and wind sweeping across high mountain grass",
        "sadhanas_en": "consigning external fires into the breath, making the earth one's bed, one's arm the pillow, and the sky one's roof, moving freely like the wind (Pavanavat) untouched like a lotus leaf in water, and finally transcending even the outer Kundika pot to drink the nectar of Chidakasha",
        "sadhanas_ta": "பூமியையே படுக்கையாகவும், தன் கையையே தலையணையாகவும், வானத்தையே கூரையாகவும் கொண்டு, தாமரை இலையில் நீர் ஒட்டாதது போல் கர்மங்களில் பற்றின்றி, காற்றைப் போல் சுதந்திரமாக உலாவி, சிதாகாச அமிர்தக் கலசமாகத் திகழும் சாதனை",
    },
    "SANNYASA_13_PARABRAHMA": {
        "guru_name": "Sage Pippalada",
        "seeker_name": "Maharishi Shaunaka",
        "guru_tamil": "பிப்பலாத முனிவர்",
        "seeker_tamil": "சௌனக மகரிஷி",
        "deity_focus": "The Imperishable Parabrahman on which the entire cosmos is strung like luminous white pearls upon a golden thread",
        "ascetic_symbols": "Four subtle golden lotuses at the navel, heart, throat, and crown, a blazing camphor flame tip (representing the Jnana-Shikha), white pearls strung on a golden thread, and a shaven-headed Paramahamsa glowing with inner light",
        "sadhanas_en": "realizing the Purusha across the four chakras of navel, heart, throat, and crown within the ninety-six-finger human temple, untying the knot of ignorance in the heart, kindling the flame-crest of Self-Knowledge as one's true Shikha, and wearing Parabrahman as one's eternal Upavita",
        "sadhanas_ta": "தொண்ணூற்றாறு அங்குல உடலின் நான்கு ஆதாரங்களில் புருஷனை உணர்ந்து, இதயத்து அறியாமை முடிச்சை அவிழ்த்து, தீபத்தின் உச்சிச் சுடர் போன்ற ஞானத்தையே குடுமியாகவும் (சிகை), முத்துக்கள் கோர்க்கப்பட்ட கயிறு போன்ற பரப்பிரம்மத்தையே பூணூலாகவும் தரிக்கும் சாதனை",
    },
    "SANNYASA_14_AVADHUTA": {
        "guru_name": "Bhagavan Dattatreya (Adi-Guru of Avadhutas)",
        "seeker_name": "Sage Sankriti",
        "guru_tamil": "பகவான் தத்தாத்ரேயர்",
        "seeker_tamil": "சான்கிருதி முனிவர்",
        "deity_focus": "The Absolute Paramartha Truth where there is neither creation nor destruction, neither bound nor seeker, neither aspirant nor liberated",
        "ascetic_symbols": "Sacred Audumbara (cluster-fig) tree on Mount Sahyadri, four glowing golden Sanskrit syllables (A-Va-Dhu-Ta), a moving chariot with a motionless passenger inside, and the untainted morning Sun shining equally upon all places",
        "sadhanas_en": "embodying the four immortal syllables of A-Va-Dhu-Ta—Akshara (Imperishable), Varenya (Supreme), Dhuta-samsara-bandhana (Having shaken off all worldly bonds), and Tat Tvam Asi (Thou Art That)—moving like the untainted Sun and resting in the ultimate non-dual Paramarthata",
        "sadhanas_ta": "அழிவற்ற 'அ', போற்றத்தக்க 'வ', சம்சார பந்தங்களை உதறிய 'தூ', தத் த்வம் அஸி எனும் 'த' ஆகிய நான்கு எழுத்துக்களின் பொருளாக வாழ்ந்து, சூரியனைப் போல் எதிலும் களங்கப்படாமல், பந்தமும் முக்தியும் கடந்த பரமார்த்த சத்தியத்தில் நிலைபெறும் சாதனை",
    },
    "SANNYASA_15_KATHARUDRA": {
        "guru_name": "Bhagavan Prajapati",
        "seeker_name": "The Devas & A Virtuous Father Parting from His Awakened Son",
        "guru_tamil": "பகவான் பிரஜாபதி",
        "seeker_tamil": "தேவர்கள் மற்றும் துறவு பூணும் தந்தையும் ஞான மகனும்",
        "deity_focus": "The Rudra-Atman of the Four Mahavakyas who dissolves the illusory foam and waves of Maya back into the one Ocean of Satchidananda",
        "ascetic_symbols": "Father's hands blessing his son's head without a single tear, wooden sacrificial ladles offered into the homa fire, golden river waves and foam dissolving back into crystal water, and the four quarters of Consciousness merging in Turiya",
        "sadhanas_en": "performing the serene Kathashruti farewell where father and son part in mutual blessing without grief, offering fearlessness to all beings, beholding the phenomenal universe as mere waves and foam upon the ocean of the Self, and uniting the four Mahavakyas in Turiya",
        "sadhanas_ta": "தந்தையும் மகனும் கண்ணீரின்றி ஆத்ம வாழ்த்துக்களுடன் விடைபெற்று, சகல உயிர்களுக்கும் அபயம் அளித்து, நீரின் நுரையும் அலையும் நீரே என்பது போல் பிரபஞ்சத்தை ஆத்மாவாகக் கண்டு, நான்கு மகாவாக்கியங்களின் பொருளாகத் துரியத்தில் ஒளிரும் சாதனை",
    },
    "SANNYASA_16_YAJNAVALKYA": {
        "guru_name": "Maharishi Yajnavalkya",
        "seeker_name": "King Janaka of Videha & Disciple Priyavrata",
        "guru_tamil": "மகரிஷி யாக்ஞவல்கியர்",
        "seeker_tamil": "மன்னன் ஜனகர் மற்றும் பிரியவிரதன்",
        "deity_focus": "The All-Pervading Brahman ('Sarvam Khalvidam Brahma Tajjalan') in whom the universe is born, breathes, and dissolves",
        "ascetic_symbols": "Withered twisted vines on a stone wall (symbolizing aging-proof Trishna/craving), a rusty clay pot plated with copper (hypocrisy) vs. a pure crystal vessel, a fearless yogi meditating amidst storm winds, and a waveless ocean of peace",
        "sadhanas_en": "severing the ever-young demoness of Craving (Trishna) with the sword of Self-Knowledge, rejecting outer bead-rolling hypocrisy, cultivating forgiveness and equanimity that remains unshaken even amidst flying arrows or fire, and meditating on 'Sarvam Khalvidam Brahma'",
        "sadhanas_ta": "உடல் முதுமையடைந்தாலும் இளமையாகவேத் துள்ளும் 'த்ருஷ்ணா' எனும் ஆசைப் பேயை ஞான வாளால் அறுத்து, போலி வேடத்தைத் தவிர்த்து, போர்க்களத்திலும் நெருப்பிலும் கலங்காத சமநோக்குடன் 'சர்வம் கல்விதம் பிரம்ம' என அமைதியில் திளைக்கும் சாதனை",
    },
    "SANNYASA_17_VARAHA": {
        "guru_name": "Lord Adi-Varaha & Maharishi Ribhu",
        "seeker_name": "Maharishi Ribhu & Disciple Nidagha",
        "guru_tamil": "பகவான் ஆதிவராகர் மற்றும் ரிபு மகரிஷி",
        "seeker_tamil": "ரிபு மகரிஷி மற்றும் சீடர் நிதாகர்",
        "deity_focus": "Lord Vasudeva—the Imperishable Chinmatra Parabrahman beyond all ninety-six Tattvas",
        "ascetic_symbols": "Celestial golden-sapphire aura of Lord Adi-Varaha, geometric wheel of the 96 Tattvas, a caparisoned royal elephant in an ancient temple street, Ribhu disguised as a village rustic leaping onto Nidagha's shoulders, and a salt doll dissolving in the ocean",
        "sadhanas_en": "discerning the changeless Witness distinct from all ninety-six Tattvas, shattering the dualistic illusion of 'King above and elephant below' through Ribhu's living test of Nidagha, ascending the Seven Jnana-Bhumikas (Stages of Wisdom), and abiding as a spotless Jivanmukta",
        "sadhanas_ta": "தொண்ணூற்றாறு தத்துவங்களுக்கும் மேலான சாட்சியைப் பிரித்தறிந்து, 'மேலே இருக்கும் மன்னன் யார், கீழே இருக்கும் யானை யார்?' என்ற ரிபுவின் சோதனையால் பேத புத்தியைக் கடந்து, ஏழு ஞான பூமிகளில் ஏறி வாசுதேவப் பிரம்மமாக ஜீவன்முக்தியில் நிலைபெறும் சாதனை",
    },
    "SANNYASA_18_SHATYAYANIYA": {
        "guru_name": "The Venerable Shatyayaniya Vaishnava Acharya",
        "seeker_name": "The Assembly of Shukla Yajurvedic Seekers & Vaishnava Sannyasins",
        "guru_tamil": "சாட்யாயனீய ஆச்சாரியர்",
        "seeker_tamil": "சுக்ல யஜுர் வேத சாதகர்கள்",
        "deity_focus": "Lord Mahavishnu (Vasudeva) dwelling in the secret cave of the heart, whose five sacred emblems sanctify the steadfast monk",
        "ascetic_symbols": "An ancient bronze key turning a lock both ways (the Mind as cause of bondage and liberation), triple bamboo staff (Tridanda), gourd kamandalu, sacred Tulasi and Peepal courtyard by the Kaveri, and sixty luminous ancestral stars in the dawn sky",
        "sadhanas_en": "turning the key of the mind away from sense-objects toward nirvishaya freedom ('Mana eva manushyanam karanam bandha-mokshayoh'), bearing the five emblems of Vishnu with purity of speech, body, and mind, conquering the six inner enemies like a warrior who never retreats, and uplifting sixty generations",
        "sadhanas_ta": "'மனமே பந்தத்திற்கும் முக்திக்கும் காரணம்' என்பதை உணர்ந்து, விடய வாசனைகளிலிருந்து மனதைத் திருப்பி, காம-குரோதாதி ஆறு உட்பகைவர்களையும் போர்க்கள வீரனைப் போல் வென்று, அறுபது தலைமுறைகளைக் கரையேற்றும் வாசுதேவ சந்நியாச சாதனை",
    },
    "SANNYASA_19_LAGHU_SANNYASA": {
        "guru_name": "The Venerable Sama Vedic Guru",
        "seeker_name": "The Virtuous Householder Awakening into an Illumined Sannyasin",
        "guru_tamil": "சாம வேத சற்குரு",
        "seeker_tamil": "இல்லறக் கடமை முடித்த உத்தமத் துறவி",
        "deity_focus": "Jyotir Amritam Virajam Brahma—the Spotless, Sinless Immortal Light of Brahman shining in the purified Pranas",
        "ascetic_symbols": "Three glowing Agnihotra fire altars, golden ghee poured in the Viraja homa, five purified vital airs (Prana, Apana, Vyana, Udana, Samana), cotton thread released into the river, and village kitchen roofs after the cooking smoke has ceased",
        "sadhanas_en": "offering the Viraja homa to purify the five vital airs (Prana, Apana, Vyana, Udana, Samana), inhaling the sacred fire into one's own breath so that Apana becomes Garhapatya, Vyana becomes Dakshinagni, and Prana becomes Ahavaniya, and shining as the Immortal Light of Brahman",
        "sadhanas_ta": "விரஜா ஹோமத்தால் பஞ்ச பிராணன்களையும் சுத்தி செய்து, புற அக்னியைத் தன் மூச்சினுள் வாங்கி, ஒவ்வொரு மூச்சையுமே அக வேள்வியாக மாற்றி, 'ஜ்யோதிர் அம்ருதம்' எனும் களங்கமற்ற அமிர்த ஜோதியாகப் பிரகாசிக்கும் சாதனை",
    },
    "YOGA_01_SHWETASHVATARA": {
        "guru_name": "Maharishi Shwetashvatara ('He of the Pure White Senses')",
        "seeker_name": "The Assembly of Brahmavadin Rishis",
        "guru_tamil": "சுவேதாஸ்வதர மகரிஷி",
        "seeker_tamil": "பிரம்மவாதிகளான முனிவர்கள்",
        "deity_focus": "The One Cosmic Lord Rudra-Shiva and His Devatma-Shakti, luminous as the Sun beyond all darkness ('Vedaham Etam Purusham Mahantam')",
        "ascetic_symbols": "Two birds perched on one sacred Peepal tree (one eating bittersweet figs, the other shining as silent Witness), a quiet level Himalayan cave beside a gentle stream, nine yogic light-visions (mist, smoke, sun, fireflies, lightning, crystal, moon), and wooden Arani churning sticks",
        "sadhanas_en": "holding the three upper parts of the body (chest, neck, and head) erect in a pure, noiseless cave, restraining the senses in the heart to cross samsara in the boat of Omkara, beholding the nine inner heralds of light, churning Dhyana, and cultivating supreme Para-Bhakti to both God and Guru",
        "sadhanas_ta": "ஒரே மரத்தின் இரு பறவைகளில் சாட்சிப் பறவையைத் தரிசித்து, சமமான குகையில் மார்பு-கழுத்து-தலை நேராக அமர்ந்து, ஓங்காரத் தோணியால் சம்சாரத்தைக் கடந்து, மின்மினி-மின்னல்-பளிங்கு-சந்திரன் ஆகிய உள் ஒளிகளைக் கண்டு, இறைவனிடத்தும் குருவிடத்தும் பரம பக்தியால் முக்தி பெறும் சாதனை",
    },
    "YOGA_02_HAMSA": {
        "guru_name": "Bhagavan Sanatkumara (and Lord Shiva to Parvati)",
        "seeker_name": "Maharishi Gautama",
        "guru_tamil": "பகவான் சனத்குமாரர்",
        "seeker_tamil": "கௌதம மகரிஷி",
        "deity_focus": "The Hamsa-Soham Sadashiva shining in the pericarp of the Eight-Petalled Heart Lotus and in the Tenth Unstruck Sound of the Thundercloud",
        "ascetic_symbols": "Crystal Himalayan lake with a pure white swan, golden and silver breath-streams of 'Ham' and 'Sa' (21,600 times daily), an eight-petalled golden lotus in the heart, and concentric acoustic waves of the Ten Anahata Nada sounds",
        "sadhanas_en": "observing the 21,600 daily breaths chanting 'Ham' on exhalation and 'Sa' on inhalation, reversing Hamsa into 'Soham' (I am He), guiding the Hamsa bird from the eight directional petals of the heart lotus into the central pericarp, and merging the mind into the Tenth Unstruck Nada sound of the thundercloud",
        "sadhanas_ta": "நாள்தோறும் 21,600 முறை இயங்கும் 'ஹம்-ஸ' மூச்சை விழிப்புணர்வால் 'ஸோஹம்' என மாற்றி, இதயத்து எட்டு இதழ் தாமரையின் மையத்தில் ஹம்ஸத்தை நிறுத்தி, சினி முதல் மேக முழக்கம் வரையிலான பத்து அனாஹத நாதங்களில் பத்தாவது நாதத்தில் மனதைக் கரைக்கும் சாதனை",
    },
    "YOGA_03_AMRITABINDU": {
        "guru_name": "The Luminous Yoga Acharya",
        "seeker_name": "The Scholarly Vedic Seeker Burdened with Palm-Leaf Manuscripts",
        "guru_tamil": "யோக ஆச்சாரியர்",
        "seeker_tamil": "ஏட்டுச் சுவடிகளைச் சுமந்த வேதப் பண்டிதன்",
        "deity_focus": "Lord Vasudeva—the One Indivisible Atman shining like the single Moon reflected in many water pots and the one white milk drawn from many-colored cows",
        "ascetic_symbols": "Heavy bundles of palm-leaf manuscripts set aside, golden paddy grain winnowed from empty chaff, cows of many colors yielding one pure white milk, butter churned from milk, and earthen water pots reflecting the single sun",
        "sadhanas_en": "purifying the mind of desire (Nishkama), meditating first on Omkara with sound and then crossing into the Soundless Supreme (Ashabda Brahman), discarding the chaff of mere bookish debate after gathering the grain of wisdom, and beholding the one white milk of Consciousness in all beings",
        "sadhanas_ta": "ஆசையற்ற சுத்த மனதை வளர்த்து, சப்த ஓங்காரத்திலிருந்து நிசப்தப் பிரம்மத்திற்கு உயர்ந்து, நெல்மணியைக் கொண்ட பின் பதரை வீசுவது போல் ஏட்டுச் சுமையை விடுத்து, பல நிறப் பசுக்களின் பால் வெண்மையாகவே இருப்பது போல் சகல உயிர்களிலும் ஒரே ஆத்மாவைத் தரிசிக்கும் சாதனை",
    },
    "YOGA_04_AMRITANADA": {
        "guru_name": "The Venerable Master of Shadanga Yoga",
        "seeker_name": "The Torch-Bearing Seeker Entering the Cave of Light",
        "guru_tamil": "ஷடங்க யோக ஆச்சாரியர்",
        "seeker_tamil": "தீவந்தியுடன் சத்தியம் தேடி வந்த சாதகன்",
        "deity_focus": "The Immortal Soundless Brahman dwelling in the fearless Sky of the Heart (Akasha-Hridaya) and reached through the Chariot of Omkara",
        "ascetic_symbols": "Flaming wooden torch set down at a sunlit cave entrance, translucent golden Chariot of Omkara with Vishnu as charioteer, gold ore smelted pure in a clay crucible, five colored elemental Pranas (ruby, crystal, dark-blue, golden, milk-white), and the crown Brahmarandhra portal",
        "sadhanas_en": "setting aside the torch of mere textual study upon reaching direct Yoga, mounting the Chariot of Omkara, practicing the Six-Limbed Shadanga Yoga (Pratyahara, Dhyana, Pranayama, Dharana, Tarka, Samadhi), smelting away sensory impurities through Kumbhaka, and piercing the Brahmarandhra",
        "sadhanas_ta": "புதையலைக் கண்ட பின் தீவந்தியைக் கீழே வைப்பது போல் சாஸ்திர வாதங்களைக் கடந்து, ஓங்காரத் தேரில் ஏறி, பிரத்யாஹாரம் முதல் சமாதி வரையிலான ஷடங்க யோகத்தைப் பயின்று, நெருப்பில் இடப்பட்ட தங்கம் போல் பிராணாயாமத்தால் புலன்களைத் தூய்மையாக்கி ஆகாச ஹ்ருதயத்தில் புகும் சாதனை",
    },
    "YOGA_05_KSHURIKA": {
        "guru_name": "The Master of Kshurika-Dharana",
        "seeker_name": "The Resolute Yogi of the Razor's Edge",
        "guru_tamil": "க்ஷுரிகா தாரணை ஆச்சாரியர்",
        "seeker_tamil": "வைராக்கியச் சாதகன்",
        "deity_focus": "The Spotless Imperishable Paramatman at the summit of the single white lotus-thread of Sushumna",
        "ascetic_symbols": "A tortoise withdrawing its limbs, the razor-blade of Manas sharpened on the whetstone of Vairagya, glowing marma junctions from toes to navel, 72,000 nadi cords, and a tiny spider climbing a single gleaming white silk thread into the sky",
        "sadhanas_en": "withdrawing the senses like a tortoise, sharpening the razor of concentration (Kshurika-Dharana) on the whetstone of dispassion, ascending step-by-step from the toes, ankles, knees, thighs, and navel to sever karmic attachment at each vital joint, and climbing the single white Sushumna thread like a spider",
        "sadhanas_ta": "ஆமை போல் புலன்களை ஒடுக்கி, வைராக்கியச் சாணைக்கல்லில் தீட்டிய தாரணை எனும் கூரிய கத்தியால் கால் பெருவிரல் முதல் நாபி வரையிலான மர்ம முடிச்சுகளை அறுத்து, எழுபத்திரண்டாயிரம் பக்க நாடிகளின் பற்றை நீக்கி, சிலந்தி ஒற்றை நூலில் ஏறுவது போல் வெண்ணிற சுஷும்னாவில் மேலேறும் சாதனை",
    },
    "YOGA_06_TEJOBINDU": {
        "guru_name": "Lord Paramashiva & Maharishi Ribhu",
        "seeker_name": "Lord Kumara Kartikeya (Skanda) & Disciple Nidagha",
        "guru_tamil": "பரமசிவன் மற்றும் ரிபு மகரிஷி",
        "seeker_tamil": "குமாரக் கடவுள் (ஸ்கந்தன்) மற்றும் நிதாகர்",
        "deity_focus": "The Tejobindu—the atomic yet cosmos-encompassing Blazing Point of Light in the heart—proclaimed as 'Chinmatroham Sadashivah'",
        "ascetic_symbols": "Microscopic sun-bright Tejobindu star in the heart lotus, fifteen carved granite pillars of Panchadashanga Raja-Yoga, Advaita-Pranayama breath waves, and Maharishi Ribhu's golden aura of Chinmatra realization",
        "sadhanas_en": "meditating upon the blazing Tejobindu in the heart, practicing the Fifteen-Limbed Advaita Raja-Yoga where negating world-illusion is Rechaka (exhalation), affirming 'I am Brahman' is Puraka (inhalation), and unwavering abidance in That is Kumbhaka, culminating in 'Chinmatroham'",
        "sadhanas_ta": "இதயத்தில் ஒளிரும் தேஜோபிந்துவைத் தியானித்து, பதினைந்து அங்க ராஜயோகத்தில் உலக மாயையைத் தள்ளுவதே ரேசகமாகவும், 'நானே பிரம்மம்' என்பதே பூரகமாகவும், அதில் அசையாது நிற்பதே கும்பகமாகவும் கொண்டு, 'சின்மாத்ரோஹம் சதாசிவ:' என முழங்கும் சாதனை",
    },
    "YOGA_07_NADABINDU": {
        "guru_name": "The Venerable Rigvedic Acharya of Nada-Yoga",
        "seeker_name": "The Nada-Yogi in Siddhasana & Vaishnavi Mudra",
        "guru_tamil": "ரிக் வேத நாதயோக ஆச்சாரியர்",
        "seeker_tamil": "சித்தாசன நாதயோகி",
        "deity_focus": "The Soundless Parabrahman (Unmani / Vishnu-Pada) where both Prana and Mind dissolve like fire when its fuel is consumed",
        "ascetic_symbols": "Cosmic Hamsa bird of 12-matra Omkara (A-kara right wing, U-kara left wing, Ma-kara tail, Ardhamatra head), yogi in Siddhasana and Vaishnavi Mudra listening to the right ear, a honeybee drinking lotus nectar, a deer entranced by flute music, and a sandalwood fire subsiding into clear air",
        "sadhanas_en": "riding the twelve-matra Omkara Hamsa bird, sitting in Siddhasana with Vaishnavi Mudra to listen to the inner Nada in the right ear as it refines from ocean and thunder into bell, flute, veena, and humming bee, absorbing the mind like a nectar-drinking bee, and entering Soundless Unmani",
        "sadhanas_ta": "பன்னிரண்டு மாத்திரை ஓங்கார அன்னத்தில் ஏறி, சித்தாசனத்திலும் வைஷ்ணவி முத்திரையிலும் வலது காதில் ஒலிக்கும் அனாஹத நாதத்தைக் கேட்டு, தேனைப் பருகும் வண்டு போலவும் இசையில் மயங்கிய மான் போலவும் மனதை நாதத்தில் லயிக்கச் செய்து உன்மனி சமாதியில் ஆழும் சாதனை",
    },
    "YOGA_08_DHYANABINDU": {
        "guru_name": "The Venerable Dhyana-Yoga Acharya",
        "seeker_name": "The Focused Archer-Yogi of Pranava",
        "guru_tamil": "தியானயோக ஆச்சாரியர்",
        "seeker_tamil": "பிரணவ வில்வித்தை யோகி",
        "deity_focus": "The Paramatman shining in the center of the Sun-Moon-Fire Flame within the upturned Heart Lotus—smaller than a mustard seed yet vaster than the universe",
        "ascetic_symbols": "A gossamer-thin white fiber split from a green lotus stalk, a golden Bow of Pranava launching the Arrow of Atman into the Sun of Brahman, the Four Asanas (Siddha, Bhadra, Simha, Padma), and a downward-facing eight-petalled heart lotus turning upward to bloom in golden glory",
        "sadhanas_en": "shattering mountains of past karma through Dhyana-Yoga, meditating on the Bindu-Nada finer than the hundredth part of a lotus fiber, fitting the arrow of the soul to the bow of Pranava to pierce the target of Brahman, and applying the Three Bandhas and Kumbhaka to turn the heart-lotus upward",
        "sadhanas_ta": "மலை போன்ற பாவங்களையும் தியான யோகத்தால் தகர்த்து, தாமரை நூலினும் நுட்பமான நாத-பிந்துவைத் தியானித்து, பிரணவ வில்லால் ஆத்ம அம்பைப் பிரம்ம இலக்கில் எய்து, மூன்று பந்தங்களாலும் கும்பகத்தாலும் கவிழ்ந்திருக்கும் இதயத் தாமரையை மேல்நோக்கி மலரச் செய்யும் சாதனை",
    },
    "YOGA_09_BRAHMAVIDYA": {
        "guru_name": "Maharishi Vyasa & The Golden Lineage (Brahma, Vasishtha, Shakti, Parashara, Shuka)",
        "seeker_name": "Young Sage Shuka & Earnest Disciples",
        "guru_tamil": "வியாச மகரிஷி மற்றும் வசிஷ்ட-பராசர குரு பரம்பரை",
        "seeker_tamil": "இளம் முனிவர் சுகர் மற்றும் சீடர்கள்",
        "deity_focus": "The Indivisible Supreme Atman where Jiva and Paramatman merge like milk poured into milk, oil into oil, and water into water",
        "ascetic_symbols": "A massive suspended bronze temple bell (Kamsya-ghanta) whose chime trails into silence, the three lights of A-U-M (Sun, Moon, Lightning) crowned by the lamp-tip Ardhamatra, the sun-bright Sushumna channel, and pure white milk poured seamlessly into a bowl of milk",
        "sadhanas_en": "following the ringing resonance of Omkara as it trails off into utter silence like a bronze bell, ascending the sun-bright Sushumna installed by the lineage of Brahma, Vasishtha, Parashara, Vyasa, and Shuka, and uniting Jiva with Paramatman like milk poured into milk until the heart-knot breaks",
        "sadhanas_ta": "வெண்கல மணியின் நாதம் மெல்ல நீண்டு மௌனத்தில் கரைவது போல் ஓங்காரத்தைத் தியானித்து, சூரியனைப் போல் ஒளிரும் சுஷும்னா வழியே மேலேறி, பாலில் ஊற்றிய பாலும் நீரில் கலந்த நீரும் ஒன்றாவது போல் ஜீவாத்மாவைப் பரமாத்மாவில் கரைத்து இதய முடிச்சை அவிழ்க்கும் சாதனை",
    },
    "YOGA_10_YOGATATTVA": {
        "guru_name": "Lord Mahavishnu (Purushottama)",
        "seeker_name": "Pitamaha Brahma & The Disciplined Yogi of the Five Elements",
        "guru_tamil": "பகவான் மகாவிஷ்ணு (புருஷோத்தமன்)",
        "seeker_tamil": "பிதாமகர் பிரம்மதேவர் மற்றும் யோக சாதகன்",
        "deity_focus": "Lord Purushottama—the Self-Luminous Atman that blazes forth unhindered when the clay pot of body-ego breaks in Raja-Yoga Samadhi",
        "ascetic_symbols": "A white swan soaring on the two symmetrical wings of Yoga and Jnana, a quiet thatched yoga kutir with a small doorway, five elemental Dharana lights (yellow square Earth, white crescent Water, red triangle Fire, smoky Air, starlit Sky), and a glowing lamp inside a breaking clay pot",
        "sadhanas_en": "uniting the two inseparable wings of Yoga and Jnana, progressing through Mantra, Laya, Hatha, and Raja Yoga across the four stages of Arambha, Ghata, Parichaya, and Nishpatti, mastering the Five Elemental Dharanas while shunning the display of Siddhis, and merging Mind and Atman like salt in water",
        "sadhanas_ta": "பறவையின் இரு சிறகுகளான யோகத்தையும் ஞானத்தையும் இணைத்து, மந்திர-லய-ஹட-ராஜ யோகங்களிலும் ஆரம்பம்-கடம்-பரிசயம்-நிஷ்பத்தி எனும் நான்கு நிலைகளிலும் தேர்ந்து, பஞ்சபூத தாரணையால் பூதங்களை வென்று, சித்திகளில் மயங்காமல் ராஜயோக சமாதியில் நிலைபெறும் சாதனை",
    },
    "YOGA_11_TRISHIKHIBRAHMANA": {
        "guru_name": "Bhagavan Surya (Aditya, The Cosmic Sun-God)",
        "seeker_name": "Trishikhi Brahmana (The Three-Tufted Vedic Seeker)",
        "guru_tamil": "சூரிய பகவான் (ஆதித்யன்)",
        "seeker_tamil": "திரிசிகி பிராம்மணர்",
        "deity_focus": "The Spotless Niranjana Shiva-Vasudeva Atman shining in the heart like a smokeless lamp-flame and lightning in a raincloud",
        "ascetic_symbols": "High Himalayan solar terrace facing the blazing orb of Bhagavan Surya, the oval bird-egg Kanda center above the base where 72,000 nadis meet, seventeen classical yoga postures, and a steady smokeless flame glowing in the heart",
        "sadhanas_en": "practicing Karma-Yoga and Jnana-Yoga united in the Eight-Limbed Ashtanga Yoga of Lord Surya, mastering the ten Yamas, ten Niyamas, and seventeen Asanas, purifying the oval Kanda center through Kumbhaka to awaken Kundalini into Sushumna, and beholding the smokeless flame of the Niranjana Atman",
        "sadhanas_ta": "ஆதித்ய மண்டலத்துச் சூரிய பகவான் அருளிய அஷ்டாங்க சிவயோகத்தில் பத்து இயம-நியமங்களையும் பதினேழு ஆசனங்களையும் பயின்று, கும்பகத்தால் கந்தத்திலிருந்து எழும் குண்டலினியை சுஷும்னாவில் செலுத்தி, புகையில்லாத் தீபச் சுடர் போன்ற நிரஞ்சன ஆத்மாவைத் தரிசிக்கும் சாதனை",
    },
    "YOGA_12_YOGACHUDAMANI": {
        "guru_name": "The Venerable Sama Vedic Master of Kundalini Yoga",
        "seeker_name": "The Awakened Sama Vedic Yogi",
        "guru_tamil": "சாம வேத யோகசூடாமணி ஆச்சாரியர்",
        "seeker_tamil": "குண்டலினி யோக சாதகன்",
        "deity_focus": "Paramashiva and Maha-Kundalini united in the Thousand-Petalled Sahasrara Lotus where Prana, Bindu, Nada, and Mind become One",
        "ascetic_symbols": "Six glowing lotus chakras along the spine (4, 6, 10, 12, 16, and 2 petals) crowned by Sahasrara, lotus-fiber-bright Maha-Kundalini uncoiling from eight coils, a gentle mahout taming a royal tusker elephant step-by-step, and solar Pingala and lunar Ida merging",
        "sadhanas_en": "visualizing the Six Chakras from four-petalled Muladhara to two-petalled Ajna and Sahasrara, awakening the eight-coiled Maha-Kundalini through the fire of Yoga, taming the mighty Prana gradually like a mahout taming an elephant or lion through the Three Bandhas, and uniting Sun and Moon in the crown",
        "sadhanas_ta": "நான்கு இதழ் மூலாதாரம் முதல் ஆக்ஞை மற்றும் சகஸ்ராரம் வரையிலான ஆதார கமலங்களை அறிந்து, யானையையும் சிங்கத்தையும் படிப்படியாகப் பழக்குவது போல் பிராணனை மூன்று பந்தங்களால் வசப்படுத்தி, குண்டலினியைச் சகஸ்ராரத்தில் பரமசிவனுடன் இணைக்கும் யோகசூடாமணி சாதனை",
    },
    "YOGA_13_MANDALABRAHMANA": {
        "guru_name": "Bhagavan Aditya (Surya Narayana in the Solar Orb)",
        "seeker_name": "Maharishi Yajnavalkya",
        "guru_tamil": "சூரிய மண்டல நாராயணர் (ஆதித்ய பகவான்)",
        "seeker_tamil": "மகரிஷி யாக்ஞவல்கியர்",
        "deity_focus": "The Golden Purusha in the Solar Mandala realized through the Five Cosmic Skies (Pancha-Akasha) and the unblinking Shambhavi Mudra",
        "ascetic_symbols": "Blazing golden Solar Mandala aligned behind Yajnavalkya's crown, the Star of Taraka between the eyebrows, five expanding domes of cosmic light (Akasha to Suryakasha), unblinking open eyes of Shambhavi Mudra, and a steady lamp in a windless chamber",
        "sadhanas_en": "meditating on the twofold Taraka (Murti and Amurti) through the three gazes (Antar, Bahir, Madhya Lakshya), ascending through the Five Akashas up to Suryakasha shining like ten million suns, practicing the secret unblinking Shambhavi Mudra, and entering Amanaska (Mindless) Raja-Yoga",
        "sadhanas_ta": "மூன்று லக்ஷ்யங்களால் தாரகப் பிரம்மத்தை நோக்கி, கோடி சூரியப் பிரகாசம் கொண்ட சூர்யாகாசம் வரையிலான ஐந்து ஆகாயங்களைக் கடந்து, உள் இலக்கில் சித்தமும் இமை கொட்டாத புறப் பார்வையும் கொண்ட சாம்பவி முத்திரையால் அமனஸ்க ராஜயோகத்தில் நிலைபெறும் சாதனை",
    },
    "YOGA_14_SHANDILYA": {
        "guru_name": "Maharishi Atharvan",
        "seeker_name": "Sage Shandilya",
        "guru_tamil": "அதர்வ மகரிஷி",
        "seeker_tamil": "சாண்டில்ய முனிவர்",
        "deity_focus": "The Cosmic Atman-Brahman (Dattatreya-Shiva Principle)—smaller than a mustard seed within the heart yet vaster than the earth and heavens",
        "ascetic_symbols": "Deodar forest ashram where spotted deer are fed with compassion, twenty ethical pillars (10 Yamas & 10 Niyamas), fourteen luminous Nadi channels, three pierced Granthis (Brahma, Vishnu, Rudra), and a mustard seed expanding into a cosmic golden sun",
        "sadhanas_en": "establishing the twenty ethical pillars of the Ten Yamas and Ten Niyamas, purifying the fourteen principal Nadis and ten Vayus through Nadi-shodhana Pranayama, piercing the three Granthis, practicing the fivefold Pratyahara of seeing the Self in every object, and realizing the Shandilya-Vidya in Samadhi",
        "sadhanas_ta": "பத்து இயமங்கள் மற்றும் பத்து நியமங்கள் எனும் இருபது தர்மத் தூண்களில் நின்று, பதினான்கு நாடிகளையும் பத்து வாயுக்களையும் பிராணாயாமத்தால் சுத்தி செய்து, மூன்று கிரந்திகளை ஊடுருவி, இதயத்தில் தினையளவினும் நுட்பமாய் பிரபஞ்சத்தினும் பெரிதாய் ஒளிரும் ஆத்மாவை உணரும் சாதனை",
    },
    "YOGA_15_YOGASHIKHA": {
        "guru_name": "Lord Maheshwara (Shankara, The Lord of Yogis)",
        "seeker_name": "Pitamaha Brahma (Hiranyagarbha)",
        "guru_tamil": "பகவான் மகேஸ்வரன் (சிவபெருமான்)",
        "seeker_tamil": "பிதாமகர் பிரம்மதேவர்",
        "deity_focus": "The Self-Luminous Shiva-Atman realized through the Flame-Crest of Maha-Yoga (the synthesis of Mantra, Laya, Hatha, and Raja Yoga)",
        "ascetic_symbols": "A dark stone chamber illuminated only when an actual oil lamp is lit (not by merely saying 'lamp'), four streams of Yoga converging into one blazing pillar of Maha-Yoga, an ornate bronze key unlocking a massive temple door (Kundalini opening Sushumna), and the Diamond Body (Vajra-deha)",
        "sadhanas_en": "abandoning dry verbal scholarship that merely repeats the word 'lamp' in the dark, uniting Jnana and Yoga as one indivisible flame, integrating Mantra, Laya, Hatha, and Raja Yoga into Maha-Yoga, unlocking the door of Sushumna with the key of Kundalini, and attaining the fearless Vajra-deha in Samadhi",
        "sadhanas_ta": "இருட்டில் 'விளக்கு' என்று வாயால் சொல்வது போன்ற வெறும் வாதங்களை விடுத்து, ஞானத்தையும் யோகத்தையும் ஒரே சுடராக்கி, மந்திர-லய-ஹட-ராஜ யோகங்களை மகாயோகமாக இணைத்து, குண்டலினித் திறவுகோலால் சுஷும்னா வாசலைத் திறந்து வஜ்ர தேக சமாதியில் திளைக்கும் சாதனை",
    },
    "YOGA_16_PASUPATABRAHMANA": {
        "guru_name": "Svayambhu Pitamaha Brahma",
        "seeker_name": "Vaishravana",
        "guru_tamil": "சுயம்பு பிரம்மதேவர்",
        "seeker_tamil": "வைஸ்ரவணன்",
        "deity_focus": "Lord Pasupati-Sadashiva—the Unborn, Ancient, Secondless Hamsa-Sutratman dwelling in the cave of the heart",
        "ascetic_symbols": "Golden Hamsa-Pranava thread weaving through the heart and crown as the true Brahma-Sutra, the inner Ashvamedha altar where sense-horses are offered into the fire of Self-Knowledge, a royal swan moving freely across earth, water, and sky, and dark chains of Pasha dissolving into Shiva-light",
        "sadhanas_en": "wearing the three-matra Hamsa-Pranava breath as the true inner Yajnopavita (Sutratman), performing the continuous inner Ashvamedha sacrifice by offering all sense-objects into the fire of Self-Knowledge, dissolving the thirty-six Tattvas in Sushumna, and shaking off the fetters of Pasha to shine as Pasupati",
        "sadhanas_ta": "ஹம்ஸ-பிரணவ மூச்சையே உண்மையான அகப் பூணூலாகத் தரித்து, புலன் நுகர்ச்சிகளை ஆத்ம ஞானத் தீயில் இடும் அக அஸ்வமேத யாகம் புரிந்து, முப்பத்தாறு தத்துவங்களையும் சுஷும்னாவில் ஒடுக்கி, பாசத் தளையை நீக்கிப் பசுபதி சதாசிவனாக ஒளிரும் சாதனை",
    },
    "YOGA_17_YOGAKUNDALINI": {
        "guru_name": "Bhagavan Sanatkumara / Lord Shiva",
        "seeker_name": "Maharishi Gautama & The Heroic Kundalini Yogi",
        "guru_tamil": "பகவான் சனத்குமாரர் / சிவபெருமான்",
        "seeker_tamil": "கௌதம மகரிஷி மற்றும் குண்டலினி யோகி",
        "deity_focus": "The Conditionless Non-Dual Atman of Videhamukti realized when Kundalini pierces the Three Cosmic Knots and bathes in the Soma nectar of Sahasrara",
        "ascetic_symbols": "Twin roots of Chitta (Vasana and Prana), a bowl of pure Mitahara food, blazing Kundalini fire bursting through Brahma-Granthi, Vishnu-Granthi, and Rudra-Granthi, silvery-golden Soma nectar dripping in Khechari Mudra, and wind dissolving into the open Himalayan sky",
        "sadhanas_en": "mastering Prana to conquer Vasana through the three keys of Mitahara, steady Asana, and Shakti-chalana, applying the Three Bandhas to drive Kundalini through Brahma, Vishnu, and Rudra Granthis, drinking the immortal Soma nectar in Khechari Mudra, and attaining bodiless Videhamukti",
        "sadhanas_ta": "வாசனை மற்றும் பிராணன் எனும் மனதின் இரு வேர்களை மித ஆகாரம், ஆசனம், சக்தி சாலனம் ஆகியவற்றால் வென்று, மூன்று பந்தங்களால் பிரம்ம-விஷ்ணு-ருத்ர கிரந்திகளைத் துளைத்து, கேசரி முத்திரையால் சகஸ்ரார சோம அமிர்தத்தைப் பருகி விதேகமுக்தி பெறும் சாதனை",
    },
    "YOGA_18_DARSHANA": {
        "guru_name": "Mahayogi Lord Dattatreya",
        "seeker_name": "Sage Sankriti",
        "guru_tamil": "மகாயோகி பகவான் தத்தாத்ரேயர்",
        "seeker_tamil": "சான்கிருதி முனிவர்",
        "deity_focus": "The Non-Dual Atman beheld in direct Darshana within the temple of the body at the inner Triveni confluence of Ida, Pingala, and Sushumna",
        "ascetic_symbols": "Sacred Himalayan river confluence under an Audumbara tree, three luminous nadi-rivers inside the torso (silvery Ida-Ganga, golden Pingala-Yamuna, radiant white Sushumna-Saraswati) meeting at the eyebrow Prayaga/Varanasi, and crystal inner water of Self-Knowledge",
        "sadhanas_en": "practicing all eight limbs of Ashtanga Yoga with non-dual Vedantic vision, recognizing the body as the sacred temple containing Ganga (Ida), Yamuna (Pingala), and Saraswati (Sushumna), bathing the mind free of ego in the inner Triveni through Pranayama, and rising from Saguna to Nirguna Dhyana for direct Atma-Darshana",
        "sadhanas_ta": "இடை நாடியே கங்கையாகவும், பிங்கலையே யமுனையாகவும், சுஷும்னாவே சரஸ்வதியாகவும் கொண்ட இவ்வுடல் ஆலயத்தின் அகத் திரிவேணி சங்கமத்தில் மன மாசுகளைக் கழுவி, அத்வைத அஷ்டாங்க யோகத்தாலும் நிர்குண தியானத்தாலும் நேரடி ஆத்ம தரிசனம் பெறும் சாதனை",
    },
    "YOGA_19_MAHAVAKYA": {
        "guru_name": "Pitamaha Brahma",
        "seeker_name": "The Circle of Atharva Vedic Siddha-Yogis",
        "guru_tamil": "பிதாமகர் பிரம்மதேவர்",
        "seeker_tamil": "அதர்வ வேத சித்த யோகிகள்",
        "deity_focus": "The Golden Purusha within the Inner Sun (Antar-Aditya)—shining like ten million suns beyond all darkness and realized as 'Sa Esha Jivo Virajah Paramatma Soham'",
        "ascetic_symbols": "Blazing golden sunrise banishing pitch-dark night shadows over a Himalayan valley, five translucent sheaths (Pancha-kosha) dissolving, vertical golden beam of Shambhavi and Khechari Mudra, crystal water poured into water, and the Inner Sun-Moon-Fire Mandala",
        "sadhanas_en": "knowing with unshakeable certainty that ignorance can never swallow Self-Knowledge any more than darkness can swallow the rising Sun, dissolving the veil of the five sheaths through Hamsa-Vidya, uniting Prana and Apana in Shambhavi and Khechari Mudra, and realizing the Golden Purusha in the inner Sun as 'Soham'",
        "sadhanas_ta": "உதய சூரியனை இருள் விழுங்க முடியாதது போல் ஆத்ம ஞானத்தை அறியாமை விழுங்க முடியாது என உணர்ந்து, ஹம்ஸ வித்தையால் பஞ்ச கோசத் திரைகளை விலக்கி, சாம்பவி மற்றும் கேசரி முத்திரையில் கோடி சூரியப் பிரகாசம் கொண்ட உள் ஆதித்ய புருஷனை 'ஸோஹம்' எனத் தரிசிக்கும் சாதனை",
    },
    "YOGA_20_TARASARA_YOGARAJA": {
        "guru_name": "Maharishi Yajnavalkya",
        "seeker_name": "Maharishi Bharadvaja",
        "guru_tamil": "மகரிஷி யாக்ஞவல்கியர்",
        "seeker_tamil": "பரத்வாஜ மகரிஷி",
        "deity_focus": "The Eight-Kala Taraka Pranava Narayana-Brahman shining in the inner Avimukta and crowned with the Fourfold Royal Yoga (Mantra, Laya, Hatha, Raja)",
        "ascetic_symbols": "Carved granite mandapam overlooking the sacred Ganges at dawn, the inner Kurukshetra and Avimukta star between the eyebrows, Nine Lotuses of Brahmapura along the spine, and Eight concentric golden rings of the Taraka Omkara (A, U, M, Bindu, Nada, Kala, Kalatita, Paratpara)",
        "sadhanas_en": "uniting the four crowns of Mantra, Laya, Hatha, and Raja Yoga, churning Prana and Apana like butter from milk across the Nine Lotuses of Brahmapura, entering the inner Avimukta between Varana and Nasi, and meditating upon the Eight-Kala Taraka Omkara into pure Chinmatra realization",
        "sadhanas_ta": "மந்திர, லய, ஹட, ராஜ எனும் நால்வகை யோக மகுடங்களையும் இணைத்து, பிரம்மபுரியின் ஒன்பது சக்கரங்களில் பிராணனைக் கடைந்து மேலேற்றி, புருவ மத்தியின் அக அவிமுக்தத்தில் அகாரம் முதல் பராத்பரம் வரையிலான எட்டு கலை தாரக ஓங்காரத்தை உபாசித்து முக்தி பெறும் சாதனை",
    },
}


def build_unabridged_storyline(item, enr):
    """Generates a deep, multi-paragraph Unabridged Storyline & Character Continuity Bible in English & Tamil."""
    cat_label = "Sannyasa (Renunciation & Advaita Realization)" if item["category"] == "Sannyasa" else "Yoga (Kundalini, Pranayama, Nada & Raja-Yoga Samadhi)"
    story_en = (
        f"**Act I — The Spiritual Crisis & Sacred Assembly (Upakrama & Adhikara)**: In the timeless sacred landscape of {item['SettingVisual']}, "
        f"the {item['veda']} tradition preserves the immortal revelation of the *{item['name_english']}* (*{item['name_iast']}*, Muktika Canon #{item['muktika_number']}). "
        f"At the heart of this film stands the profound encounter between **{enr['seeker_name']}** ({item['ProtagonistVisual']}) and **{enr['guru_name']}** ({item['GuruVisual']}). "
        f"Having witnessed the fleeting nature of worldly rituals, finite pleasures, and outward religious emblems, the seeker approaches the Master with burning *Mumukshutva* (longing for liberation). "
        f"The Guru first tests the seeker's inner qualification (*Adhikara*), revealing why external forms alone cannot liberate a mind still bound by subtle cravings (*Vasana*) and restless vital breath (*Prana*).\n\n"
        f"**Act II — The Path of Inner Sadhana &Sacred Metaphor (Purvapaksha & Drishtanta)**: Step by step, **{enr['guru_name']}** dismantles outer illusions and initiates **{enr['seeker_name']}** "
        f"into the transformative discipline of {enr['sadhanas_en']}. Through vivid visual parables—{enr['ascetic_symbols']}—the Upanishad bridges rigorous inner practice with direct philosophical insight. "
        f"Every breath, every posture, and every drop of awareness is turned inward toward **{enr['deity_focus']}**.\n\n"
        f"**Act III — The Thunder of Upadesha & Jivanmukti Awakening (Siddhanta & Samadhi)**: In the climactic revelation, the Master utters the core Upanishadic Mahavakya: "
        f"*\"{item['verse_sanskrit']}\"* (*{item['verse_meaning_english']}*). As the knot of ignorance in the heart (*Hridaya-granthi*) shatters, the seeker enters *Nirvikalpa Samadhi*, "
        f"beholding the entire universe woven seamlessly upon the One Spotless Consciousness, and abides forever as a fearless *Jivanmukta*."
    )
    story_ta = (
        f"**முதல் அங்கம் — ஆன்மீகத் தேடலும் புனித சபையும் (உபக்ரமம் & அதிகாரம்)**: {item['veda']} மரபில் போற்றப்படும் முக்திகா உபநிடத வரிசையின் #{item['muktika_number']}-வது உபநிடதமான "
        f"**{item['name_tamil']}** (*{item['story_title_tamil']}*), பண்டைய பாரதத்தின் புனிதச் சூழலில் விரிகிறது. "
        f"இக்காவியத்தின் மையமாக **{enr['seeker_tamil']}** மற்றும் **{enr['guru_tamil']}** ஆகியோருக்கு இடையிலான மெய்ஞ்ஞான உரையாடல் அமைகிறது. "
        f"புறச் சடங்குகளாலும் நிலையற்ற உலக இன்பங்களாலும் பிறவிப் பிணி தீராது என்பதை உணர்ந்த சாதகன், தீவிர முமுக்ஷுத்வத்துடன் குருவின் திருவடிகளை அடைகிறான். "
        f"சாதகனின் மனப் பக்குவத்தையும் வைராக்கியத்தையும் சோதிக்கும் குரு, வாசனையையும் பிராணனையும் வெல்லாமல் வெறும் புற அடையாளங்களால் முக்தி கிட்டாது என்ற பேருண்மையை உணர்த்துகிறார்.\n\n"
        f"**இரண்டாம் அங்கம் — அகச் சாதனையும் உவமைத் தெளிவும் (பூர்வபக்ஷம் & திருஷ்டாந்தம்)**: அதன்பின், {enr['sadhanas_ta']} குறித்து **{enr['guru_tamil']}** படிப்படியாக உபதேசிக்கிறார். "
        f"உபநிடதத்தின் அழியா உவமைகள் வழியாக, சாதகனின் கவனச்சிதறல்கள் அனைத்தும் உள்முகமாகத் திருப்பப்பட்டு, இடைவிடாத தியான அக்னியால் சுஷும்னா நாடியும் இதயத் தாமரையும் பிரகாசிக்கத் தொடங்குகின்றன.\n\n"
        f"**மூன்றாம் அங்கம் — சித்தாந்த முழக்கமும் ஜீவன்முக்திப் பேரின்பமும் (சித்தாந்தம் & சமாதி)**: உபதேசத்தின் உச்சத்தில், *\"{item['verse_tamil_translit']}\"* "
        f"({item['verse_meaning_tamil']}) எனும் மூல மந்திரம் முழங்குகிறது! இதயத்து அறியாமை முடிச்சு அவிழ்ந்து, சகல ஐயங்களும் நீங்கி, பிரபஞ்சம் முழுவதையும் தன் சொந்த ஆத்ம சொரூபமாகவே நேருக்கு நேர் தரிசிக்கும் சாதகன், "
        f"வாழும்போதே முக்தனான ஜீவன்முக்தனாய் நித்திய சாந்தியில் நிலைபெறுகிறான்."
    )
    return story_en, story_ta


def build_five_subshots(item, sc, enr):
    """
    Constructs 5 distinct, non-repetitive 9-second continuous 16:9 8K Google Flow / Veo prompts
    for the given scene (Shot A [00-09s], Shot B [09-18s], Shot C [18-27s], Shot D [27-36s], Shot E [36-45s]).
    Maintains strict visual continuity locks while varying camera angle, lens focal length, and action beat.
    """
    setting = item["SettingVisual"]
    protag = item["ProtagonistVisual"]
    guru = item["GuruVisual"]
    symbols = enr["ascetic_symbols"]
    num = sc["num"]
    base_prompt_clean = sc["prompt"].replace("Zero modern elements, zero text, zero subtitles, zero borders.", "").strip().rstrip(".")
    exclusions = "Zero modern elements, zero synthetic fabrics, zero on-screen text, zero subtitles, zero watermarks, zero borders."

    # Scene-specific lighting & mood progression across the 5-minute film
    mood_map = {
        1: "misty pre-dawn to first golden sunrise rays piercing the ancient canopy",
        2: "warm golden morning light casting dramatic chiaroscuro rays across stone and kusha grass",
        3: "luminous morning sunbeams illuminating sacred ashram dust motes and subtle golden prana",
        4: "radiant high-morning golden-amber illumination highlighting sacred yogic metaphors and fire",
        5: "blazing spiritual zenith of golden-white prana effulgence and divine inner awakening",
        6: "transcendent cosmic golden-prismatic aura uniting earth, water, forest, and sky in Samadhi",
        7: "serene eternal golden sunrise benediction with peaceful temple bell and river reflections",
    }
    mood = mood_map.get(num, "sacred golden dawn illumination")

    shot_a = (
        f"16:9 widescreen 8K photorealistic 24fps anamorphic wide establishing shot (24mm lens, slow dolly-in, 00s-09s) of {setting} during {mood}. "
        f"{base_prompt_clean}. Atmospheric depth, natural volumetric light rays, authentic ancient Bharata architecture and foliage. {exclusions}"
    )

    shot_b = (
        f"16:9 widescreen 8K photorealistic 24fps medium tracking shot (50mm lens, smooth lateral Steadicam glide at 24fps, 09s-18s) focusing on {guru} and {protag}. "
        f"In this continuous beat of Scene {num} ({sc['title']}), {guru} performs a deliberate sacred mudra of instruction while {protag} responds with deep yogic attentiveness and reverent posture. "
        f"Rich handwoven cotton and bark-cloth textures, rudraksha beads, and {mood}. {exclusions}"
    )

    shot_c = (
        f"16:9 widescreen 8K photorealistic 24fps macro close-up shot (85mm macro prime lens, shallow depth of field, slow push-in, 18s-27s) capturing the sacred Upanishadic symbol and yogic metaphor of Scene {num}: "
        f"{symbols}. Subtle translucent golden yogic prana light shimmers around the heart lotus, breath, or sacred implements, visually embodying the teaching: '{sc['sub_cue']}'. "
        f"Micro-detailed skin, wood, stone, and flame textures. {exclusions}"
    )

    shot_d = (
        f"16:9 widescreen 8K photorealistic 24fps over-the-shoulder / intimate two-shot (35mm lens, slow orbital arc, 27s-36s) of Guru-Shishya Samvada between {guru} and {protag} inside {setting}. "
        f"As the philosophical dialogue peaks, {protag}'s eyes reflect profound inner awakening and stillness while golden prana light gently illuminates the space between Master and disciple. {exclusions}"
    )

    shot_e = (
        f"16:9 widescreen 8K photorealistic 24fps slow crane ascent and atmospheric transition shot (28mm lens, gentle upward pedestal and pull-back, 36s-45s) rising above {guru} and {protag} in {setting}. "
        f"Golden rays of {mood} ripple across the sacred landscape, holding a tranquil visual bridge into the next chapter of the Upanishad. {exclusions}"
    )

    return [
        {
            "shot_id": f"Scene_{num}_Shot_A",
            "window": "00s - 09s",
            "role": "Wide Anamorphic Establishing / Hermitage, Cave, or Temple Dawn Shot",
            "camera": "24mm anamorphic wide lens, slow cinematic dolly-in at 24fps establishing geography and sacred lighting",
            "prompt": shot_a,
        },
        {
            "shot_id": f"Scene_{num}_Shot_B",
            "window": "09s - 18s",
            "role": "Medium Tracking Shot on the Ascetic / Yogi / Guru Action & Mudra",
            "camera": "50mm prime lens, smooth lateral Steadicam tracking shot following character posture and mudra",
            "prompt": shot_b,
        },
        {
            "shot_id": f"Scene_{num}_Shot_C",
            "window": "18s - 27s",
            "role": "Macro / Close-Up Shot on Sacred Symbol, Yogic Prana / Chakra / Sushumna Metaphor, or Facial Stillness",
            "camera": "85mm macro close-up lens, shallow depth of field focusing on symbolic props, breath, or inner chakra light",
            "prompt": shot_c,
        },
        {
            "shot_id": f"Scene_{num}_Shot_D",
            "window": "27s - 36s",
            "role": "Over-the-Shoulder / Two-Shot Guru-Shishya Dialogue & Inner Awakening",
            "camera": "35mm lens, intimate over-the-shoulder orbital arc capturing emotional and spiritual transmission",
            "prompt": shot_d,
        },
        {
            "shot_id": f"Scene_{num}_Shot_E",
            "window": "36s - 45s",
            "role": "Slow Crane Ascent / Atmospheric Transition Shot",
            "camera": "28mm wide lens, slow crane elevation and pull-back bridging seamlessly into the next scene",
            "prompt": shot_e,
        },
    ]


def build_dramatic_beat_and_expanded_vo(item, sc, enr):
    """
    Expands each scene's dramatic beat (Upakhyana & Samvada), English VO (~115-135 words),
    and Senthamizh VO (~115-135 words) so that a 45-second scene has full, rich dramatic narration
    and Guru-Shishya dialogue without rushing or looping.
    """
    num = sc["num"]
    base_en = sc["vo_en"].strip()
    base_ta = sc["vo_ta"].strip()
    guru = enr["guru_name"]
    seeker = enr["seeker_name"]
    guru_ta = enr["guru_tamil"]
    seeker_ta = enr["seeker_tamil"]
    veda = item["veda"]
    up_en = item["name_english"]
    up_ta = item["name_tamil"]
    sloka_iast_cue = sc["sub_cue"]

    if num == 1:
        beat = (
            f"**Upakrama (Sacred Opening & The Seeker's Burning Question)**: In {item['SettingVisual']}, "
            f"**{seeker}** approaches **{guru}** with deep humility. Disillusioned with transient worldly pursuits and outer ritualism, "
            f"the seeker poses the foundational question of the *{up_en}*, initiating the sacred *Guru-Shishya Samvada*."
        )
        ext_en = (
            f"{base_en} Across the quiet sanctuary of {item['SettingVisual']}, the morning breeze carried the ancient resonance of the {veda}. "
            f"With folded hands and eyes brimming with earnest *Mumukshutva*, {seeker} spoke again in a voice trembling with spiritual hunger: "
            f"'O Venerable Master, for years I have observed outer rules and studied the sacred chants, yet the subtle knot of sorrow within my heart remains untied! "
            f"Have mercy upon me, and reveal that direct path by which the bound soul crosses beyond mortality into the fearless light of the Supreme!' "
            f"Beholding the pure sincerity of the disciple, {guru} raised his hand in serene blessing and began the immortal teaching."
        )
        ext_ta = (
            f"{base_ta} {veda} மரபின் புனித அதிர்வுகள் நிறைந்த அந்தத் தவச்சாலையில், காலைத் தென்றல் அமைதியாக வீசியது. "
            f"கைகூப்பி வணங்கிய {seeker_ta}, முக்திப் பேற்றிற்கான ஆழ்ந்த ஏக்கத்துடன் மீண்டும் பணிந்து வேண்டினார்: "
            f"'பூஜ்ய குருதேவரே! பல காலமாகப் புற நியதிகளையும் சாஸ்திரங்களையும் நான் பயின்று வந்தபோதிலும், என் இதயத்தினுள் இருக்கும் துன்ப முடிச்சு இன்னும் அவிழவில்லையே! "
            f"கருணை கூர்ந்து, கட்டுண்ட ஜீவன் மரண பயத்தைக் கடந்து அச்சமற்ற பரம்பொருளின் பேரொளியில் நிலைபெறும் நேரடி மார்க்கத்தை எனக்கு அருள்வீராக!' "
            f"சீடனின் உள்ளத் தூய்மையைக் கண்ட {guru_ta}, அபய ஹஸ்தம் உயர்த்திப் புன்னகையுடன் தனது அழியா உபதேசத்தைத் தொடங்கினார்."
        )
    elif num == 2:
        beat = (
            f"**Adhikara & Pariksha (The Trial of Qualification & Inner Turning)**: **{guru}** examines the readiness of **{seeker}**, "
            f"challenging the seeker's attachment to external identity, body-consciousness, and restless mental impressions (*Vasanas*). "
            f"The seeker resolves to turn the gaze completely inward."
        )
        ext_en = (
            f"{base_en} Looking deep into the disciple's eyes, {guru} spoke with compassionate authority: "
            f"'Hear this secret, O Seeker! The Infinite Truth is never won by mere outward show or mechanical habit while the mind still chases fleeting shadows. "
            f"Are you ready to cast aside every false crutch of ego and examine the very root of your breath and awareness?' "
            f"Hearing this piercing challenge, {seeker} bowed to the earth and answered with unwavering resolve: "
            f"'O Master, by your grace my attachment to fleeting appearances has fallen away; lead me through the fire of discrimination into the sanctuary of the Self!' "
            f"Thus tested in the crucible of *Viveka* and *Vairagya*, the disciple's heart opened to the higher mystery."
        )
        ext_ta = (
            f"{base_ta} சீடனின் கண்களை ஊடுருவிப் பார்த்த {guru_ta}, கருணையும் உறுதியும் கலந்த குரலில் மேலும் உரைத்தார்: "
            f"'சாதகனே, நன்றாகக் கேள்! மனம் சிற்றின்ப நிழல்களின் பின்னே ஓடிக்கொண்டிருக்கும்போது, வெறும் புற வேடங்களாலோ இயந்திரத்தனமான பழக்கங்களாலோ எல்லையற்ற சத்தியத்தை அடைய முடியாது. "
            f"அகங்காரத்தின் பொய்ப் பிடிப்புகளை எல்லாம் உதறிவிட்டு, உன் உயிரின் வேரையும் உணர்வின் மூலத்தையும் உற்றுநோக்க நீ சித்தமாக இருக்கிறாயா?' "
            f"குருவின் இந்தச் சோதனையைக் கேட்ட {seeker_ta}, சிரம் தாழ்த்தி வணங்கித் தயக்கமின்றிப் பதிலளித்தார்: "
            f"'குருவே! தங்கள் அருளால் நிலையற்ற தோற்றங்களின் மீதான என் பற்று நீங்கியது; விவேக அக்னியின் வழியே என்னை ஆத்ம சந்நிதிக்கு அழைத்துச் செல்லுங்கள்!' "
            f"இவ்வாறு விவேகமும் வைராக்கியமும் உறுதிப்பட்டதும், உயர் ஞானத்திற்கான கதவு திறந்தது."
        )
    elif num == 3:
        beat = (
            f"**Purvapaksha (Overcoming Outer Bonds & Discovering the Subtle Architecture)**: **{guru}** dismantles the illusion of the five sheaths and external dependency, "
            f"guiding **{seeker}** into the subtle anatomy of Prana, the Nadis, and the inward movement of Consciousness."
        )
        ext_en = (
            f"{base_en} As golden sunlight filtered into the sanctuary, {seeker} asked in wonder: "
            f"'O Bhagavan, when the outward senses are withdrawn and worldly conventions are left behind, by what inner compass does the yogi navigate the unseen realm of the spirit?' "
            f"{guru} answered with luminous clarity: 'When the restless currents of sight, sound, and craving are gathered back into the lotus of the heart, "
            f"the temple of this very body reveals its hidden pathways of light! Do not look for liberation in distant skies; "
            f"observe how the vital breath and conscious awareness meet within the central pillar of your own being, purifying every stain of past karma.'"
        )
        ext_ta = (
            f"{base_ta} பொன்னிறக் காலைக் கதிர்கள் ஆசிரமத்தினுள் ஊடுருவியபோது, {seeker_ta} வியப்புடன் வினவினார்: "
            f"'பகவானே! புறப் புலன்களை ஒடுக்கி உலகியல் கட்டுப்பாடுகளைக் கடந்த பின், கண்ணுக்குத் தெரியாத அக உலகில் யோகி எவ்வாறு தன் பயணத்தை வழிநடத்துகிறான்?' "
            f"அதற்கு {guru_ta} தெளிந்த ஞானத்தோடு பதிலளித்தார்: 'பார்வையும் ஓசையும் ஆசையும் இதயத் தாமரைக்குள் மீண்டும் ஒடுங்கும்போது, "
            f"இவ்வுடல் எனும் ஆலயமே தனது ரகசிய ஒளிப் பாதைகளை வெளிப்படுத்துகிறது! முக்தியைத் தொலைதூர வானில் தேடாதே; "
            f"உன் உள்ளேயே பிராணனும் தூய விழிப்புணர்வும் எவ்வாறு மைய நாடியில் இணைந்து பழைய கர்ம மாசுகளைத் தூய்மைப்படுத்துகின்றன என்பதை விழிப்போடு கவனிப்பாயாக!'"
        )
    elif num == 4:
        beat = (
            f"**Drishtanta & Sadhana (The Living Metaphor & Deep Ascetic/Yogic Practice)**: Through the vivid Upanishadic metaphor of {enr['ascetic_symbols']}, "
            f"**{guru}** demonstrates the exact step-by-step practice of {enr['sadhanas_en']}, which **{seeker}** immediately puts into living experience."
        )
        ext_en = (
            f"{base_en} Contemplating this living parable, {seeker} closed his eyes, steadied his posture, and aligned the flow of Prana with one-pointed devotion. "
            f"Watching the disciple's breath grow rhythmic and tranquil, {guru} whispered the guiding instruction of the *{up_en}*: "
            f"'Just as nature reveals its hidden essence only through patient, focused application, so must you hold your awareness steady without a single tremor of doubt! "
            f"Let every inhalation draw your scattered mind home to the center, and let every retention of awareness burn away the dry fuel of egoic desire, "
            f"until the inner nectar of immortality shines forth of its own accord!'"
        )
        ext_ta = (
            f"{base_ta} இந்த உயிரோட்டமான உவமையை உள்ளத்தில் இருத்திய {seeker_ta}, கண்களை மூடி ஆசனத்தில் நிலைபெற்று, ஒருமைப்பட்ட பக்தியுடன் பிராணனை முறைப்படுத்தினார். "
            f"சீடனின் மூச்சு சீராகி அமைதியடைவதைக் கண்ட {guru_ta}, {up_ta} காட்டும் சாதனை நெறியை மென்மையாக உபதேசித்தார்: "
            f"'இயற்கையில் மறைந்திருக்கும் சாரம் பொறுமையான முயற்சியால் மட்டுமே வெளிப்படுவது போல, எள்ளளவும் சந்தேகமின்றி உன் விழிப்புணர்வைத் துல்லியமாக நிலைநிறுத்து! "
            f"உள்வாங்கும் ஒவ்வொரு மூச்சும் சிதறிய மனதை இதய மையத்திற்கு அழைத்து வரட்டும்; தியான கும்பகத்தின் வெப்பத்தால் அகங்கார ஆசைகள் அனைத்தும் சாம்பலாகி, "
            f"உள்ளிருக்கும் அமிர்த தாரை தானாகவே சுரந்து பெருகுவதை அனுபூதியில் உணர்வாயாக!'"
        )
    elif num == 5:
        beat = (
            f"**Siddhanta (The Climax of Upadesha & The Lion-Roar of Awakening)**: The philosophical and yogic teaching reaches its thunderous zenith. "
            f"As the core verse ({sloka_iast_cue}) resounds, the veil of duality shatters and **{seeker}** awakens to the direct realization of **{enr['deity_focus']}**."
        )
        ext_en = (
            f"{base_en} As those immortal words of the *{up_en}* echoed like thunder across the timeless sanctuary, a blazing wave of golden-white effulgence "
            f"erupted within the heart and crown of {seeker}! Every lingering question, every fear of birth and death, and every illusion of separation dissolved "
            f"in an instant, like darkness before a thousand rising suns. In the depths of that radiant awakening, {seeker} realized with unshakeable certainty: "
            f"'Truly, I am neither this perishing body nor this wavering mind! I am that spotless, indivisible Consciousness in whom the entire cosmos rises and rests!'"
        )
        ext_ta = (
            f"{base_ta} {up_ta} அருளிய இந்த அழியா மகாவாக்கியம் இடிமுழக்கம் போல் எதிரொலித்த கணத்தில், {seeker_ta} அவர்களின் இதயத்திலும் சிரசிலும் "
            f"கோடி சூரியப் பிரகாசம் கொண்ட ஞானப் பேரொளி வெடித்துப் பரவியது! பிறப்பு-இறப்பு பற்றிய அச்சமும், ஜீவன்-பரமன் எனும் பேத மயக்கமும், "
            f"சூரிய உதயத்தின் முன் இருள் மறைவது போல் அக்கணமே தடமின்றி மறைந்தன. அந்தப் பேரானந்த விழிப்புணர்வில் திளைத்த சாதகன் அசைக்க முடியாத உறுதியுடன் உணர்ந்தான்: "
            f"'உண்மையில் நான் அழியும் இவ்வுடலும் அல்லன், அலைபாயும் இம்மனமும் அல்லன்! பிரபஞ்சம் அனைத்தும் எதில் தோன்றி ஒடுங்குகிறதோ, அந்தக் களங்கமற்ற அகண்ட சைதன்யப் பரம்பொருளே நான்!'"
        )
    elif num == 6:
        beat = (
            f"**Samadhi & Jivanmukti (Direct Cosmic Vision & Living Liberation)**: Established in *Nirvikalpa Samadhi*, **{seeker}** beholds the One Indivisible Self "
            f"pervading all beings, elements, and worlds, embodying the serene, unshakeable freedom of a *Jivanmukta*."
        )
        ext_en = (
            f"{base_en} Opening his eyes upon a transfigured universe, {seeker} beheld no second thing anywhere—every tree, every flowing stream, every bird in flight, "
            f"and the vast dome of the morning sky shimmered as waves of one boundless Ocean of *Satchidananda*. "
            f"Smiling in serene communion, {guru} blessed the awakened sage: 'Now you have reached the summit where the knower, the path of knowledge, and the Infinite Known "
            f"are forever One! Moving through the world like the untainted wind or resting in silent stillness, you are a *Jivanmukta*—liberated while living, "
            f"sanctifying the very earth beneath your feet!'"
        )
        ext_ta = (
            f"{base_ta} நிர்விகல்ப சமாதியின் நிறைவில் கண் விழித்த {seeker_ta}, எதிரே விரிந்த பிரபஞ்சத்தில் இரண்டாவது பொருள் எதனையுமே காணவில்லை—மரங்களும், ஓடும் நதியும், "
            f"பறவைகளும், விரிந்த ஆகாயமும் ஒரே சச்சிதானந்தப் பெருங்கடலின் அலைகளாகவே ஒளிர்ந்தன! "
            f"மௌனப் புன்னகையுடன் அவரை ஆசீர்வதித்த {guru_ta} அருளினார்: 'இப்போது அறிபவன், அறிவு, அறியப்படும் பொருள் ஆகிய மூன்றும் ஒன்றாகும் பரம சிகரத்தை நீ அடைந்துவிட்டாய்! "
            f"காற்றைப் போல் சுதந்திரமாக உலகில் உலாவினாலும், ஆழ்ந்த மௌனத்தில் வீற்றிருந்தாலும், நீ வாழும்போதே முக்தனான ஜீவன்முக்தன் ஆவாய்; "
            f"உன் பாதம் படும் பூமியெல்லாம் புனிதமடைகிறது!'"
        )
    else:
        beat = (
            f"**Phala Sruti & Shanti (The Eternal Benediction & Universal Peace Invocation)**: As the camera rises over {item['SettingVisual']}, "
            f"the timeless fruit of the *{up_en}* (*Phala Sruti*) is bestowed upon all seekers, closing with the Vedic Shanti Mantra."
        )
        ext_en = (
            f"{base_en} Whoever contemplates this sacred teaching of the *{up_en}* with a pure heart and steady mind is freed from the knots of karma and awakens to the "
            f"eternal majesty of the Indwelling Self. Across the centuries, from the ancient forest hermitages and Himalayan caves of Bharata to our own inner heart today, "
            f"the voice of {guru} and {seeker} calls us home to fearless freedom, unshakeable equanimity, and boundless compassion for all living beings. "
            f"May that Supreme Light illuminate our awareness forevermore. Om Shanti, Shanti, Shantihi."
        )
        ext_ta = (
            f"{base_ta} {up_ta} அருளும் இந்தப் புனித உபதேசத்தைத் தூய உள்ளத்தோடும் ஒருமைப்பட்ட மனத்தோடும் தியானிக்கும் எவரொருவரும், கர்ம முடிச்சுகளிலிருந்து விடுபட்டுத் "
            f"தன்னுள்ளேயே ஒளிரும் ஆத்ம சாம்ராஜ்யத்தை அடைகிறார்கள். பண்டைய பாரதத்தின் வன ஆசிரமங்களிலும் இமயக் குகைகளிலும் ஒலித்த {guru_ta} மற்றும் {seeker_ta} ஆகியோரின் "
            f"இந்த மெய்ஞ்ஞானப் பேரொளி, இன்றும் நம் இதயக் குகையில் அச்சமற்ற சுதந்திரத்தையும், சமநோக்கையும், சர்வபூத கருணையையும் மலரச் செய்கிறது. "
            f"அந்தப் பரம ஜோதி நம் அனைவரின் உணர்விலும் என்றென்றும் சுடர்விடுவதாக! ஓம் சாந்தி! சாந்தி! சாந்திஹி!"
        )

    return beat, ext_en, ext_ta


def render_upgraded_markdown(item, yt_meta):
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
    lines.append(f"- **Target Film Format**: `5-Minute (300–315s) 16:9 Widescreen 8K Movie — 7 Narrative Scenes × 5 Continuous 9s Google Flow Sub-Shots = 35 Total Shots`")
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
    lines.append("## 2. Complete Unabridged Storyline & Character Continuity Bible")
    lines.append("")
    lines.append("### 2A. Unabridged Narrative Arc (English)")
    lines.append(item["unabridged_storyline_en"])
    lines.append("")
    lines.append("### 2B. முழுமையான கதைச்சுருக்கம் மற்றும் தத்துவப் பின்னணி (செந்தமிழ் உரைநடை)")
    lines.append(item["unabridged_storyline_ta"])
    lines.append("")
    lines.append("### 2C. Locked Visual Continuity Bible (35-Shot Google Flow Lock)")
    vb = item["locked_visual_continuity_bible"]
    lines.append(f"- **Primary Setting & Architecture Lock**: {vb['setting_visual']} ({vb['aesthetic']}).")
    lines.append(f"- **Protagonist / Seeker Continuity Lock**: {vb['protagonist_visual']}.")
    lines.append(f"- **Guru / Deity Continuity Lock**: {vb['guru_visual']}.")
    lines.append(f"- **Deity / Brahma-Vidya Spiritual Focus**: {vb['deity_focus']}.")
    lines.append(f"- **Ascetic / Yogic Symbols & Props Lock**: {vb['ascetic_symbols']} ({vb['costume_props']}).")
    lines.append(f"- **Resolution & Frame Rate**: {vb['resolution_fps']}.")
    lines.append(f"- **Lighting & Atmosphere**: {vb['lighting']}.")
    lines.append(f"- **Hard Exclusions**: {vb['hard_exclusions']}.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Full 7-Scene / 35-Shot Ultra-Detailed Screenplay (16:9 Widescreen 5-Minute Film)")
    lines.append("")

    for sc in item["scenes"]:
        lines.append(f"### Scene {sc['num']} ({sc['window']}): {sc['title']}")
        lines.append("")
        lines.append(f"- **Scene Title & Duration Window**: Scene {sc['num']} ({sc['window']}) — {sc['title']} (45 Seconds / 5 Continuous 9s Sub-Shots)")
        lines.append(f"- **Dramatic Story & Philosophical Dialogue Beat (Upakhyana & Samvada)**: {sc['dramatic_beat']}")
        lines.append(f"- **Master Camera & Cinematography Plan**: {sc['camera']}")
        lines.append("")
        lines.append("#### 5 Continuous 9-Second Google Flow / Veo 16:9 Prompts (`Shot A` to `Shot E`)")
        for sh in sc["sub_shots"]:
            lines.append(f"- **`{sh['shot_id']}` ({sh['window']}) — {sh['role']}**:")
            lines.append(f"  - *Camera Motion*: {sh['camera']}")
            lines.append(f"  - *Google Flow Prompt*: `{sh['prompt']}`")
        lines.append("")
        lines.append("#### Expanded 45-Second Dramatic Narration & Dialogue (English)")
        lines.append(f"> \"{sc['vo_en']}\"")
        lines.append("")
        lines.append("#### விரிவான 45-விநாடி நாடக உரைநடை மற்றும் உரையாடல் (செந்தமிழ் உரைநடை)")
        lines.append(f"> \"{sc['vo_ta']}\"")
        lines.append("")
        lines.append(f"- **On-Screen Subtitle / Verse Cue**: `{sc['sub_cue']}`")
        lines.append(f"- **Sound Design & Sangeetham Score**: {sc['sound']}")
        lines.append("")

    return "\n".join(lines)


def main():
    os.makedirs(SANNYASA_DIR, exist_ok=True)
    os.makedirs(YOGA_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)

    sannyasa_count = 0
    yoga_count = 0
    total_scenes = 0
    total_shots = 0
    enriched_records = []

    for raw_item in base_builder.UPANISHADS_DATA:
        item = json.loads(json.dumps(raw_item))
        story_id = item["story_id"]
        enr = STORY_ENRICHMENTS[story_id]

        story_en, story_ta = build_unabridged_storyline(item, enr)
        item["unabridged_storyline_en"] = story_en
        item["unabridged_storyline_ta"] = story_ta

        item["locked_visual_continuity_bible"] = {
            **LOCKED_VISUAL_BIBLE,
            "setting_visual": item["SettingVisual"],
            "protagonist_visual": item["ProtagonistVisual"],
            "guru_visual": item["GuruVisual"],
            "guru_name": enr["guru_name"],
            "seeker_name": enr["seeker_name"],
            "deity_focus": enr["deity_focus"],
            "ascetic_symbols": enr["ascetic_symbols"],
        }

        for sc in item["scenes"]:
            total_scenes += 1
            sub_shots = build_five_subshots(item, sc, enr)
            total_shots += len(sub_shots)
            beat, ext_en, ext_ta = build_dramatic_beat_and_expanded_vo(item, sc, enr)

            sc["dramatic_beat"] = beat
            sc["sub_shots"] = sub_shots
            sc["vo_en"] = ext_en
            sc["vo_ta"] = ext_ta

        yt_meta = base_builder.build_youtube_metadata(item)
        item["youtube_metadata"] = yt_meta

        md_content = render_upgraded_markdown(item, yt_meta)

        if item["category"] == "Sannyasa":
            sannyasa_count += 1
            fname = f"{sannyasa_count:02d}_muktika_{item['muktika_number']:03d}_{base_builder.slugify(item['name_english'])}.md"
            out_path = os.path.join(SANNYASA_DIR, fname)
        else:
            yoga_count += 1
            fname = f"{yoga_count:02d}_muktika_{item['muktika_number']:03d}_{base_builder.slugify(item['name_english'])}.md"
            out_path = os.path.join(YOGA_DIR, fname)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        item["markdown_file"] = out_path
        enriched_records.append(item)

    dataset = {
        "agent": "Agent 5: Group 5 — Sannyasa (19 Canon Texts) & Yoga (20 Canon Texts) Upanishads Ultra-Detailed 5-Minute Google Flow Screenplay & 35-Shot Story Architect",
        "format_spec": "5-Minute (300-315s) 16:9 Widescreen 8K Film | 7 Scenes per Film | 5 Continuous 9s Sub-Shots (Shot A to Shot E) per Scene = 35 Google Flow Prompts per Film",
        "total_upanishads": len(enriched_records),
        "sannyasa_upanishads_count": sannyasa_count,
        "yoga_upanishads_count": yoga_count,
        "total_scenes": total_scenes,
        "total_sub_shots": total_shots,
        "locked_visual_bible_defaults": LOCKED_VISUAL_BIBLE,
        "upanishads": enriched_records,
    }

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Upgraded {sannyasa_count} Sannyasa Upanishads in {SANNYASA_DIR}")
    print(f"Upgraded {yoga_count} Yoga Upanishads in {YOGA_DIR}")
    print(f"Total Films: {len(enriched_records)} | Total Scenes: {total_scenes} | Total 9s Google Flow Shots: {total_shots}")
    print(f"Updated JSON dataset at {JSON_OUT}")


if __name__ == "__main__":
    main()
