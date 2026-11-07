# -*- coding: utf-8 -*-
"""Agent 3 Part 2: 14 Vaishnava Upanishads data module."""

def make_vaishnava(uid, mnum, name_en, name_sa, name_ta, veda, story_en, story_ta,
                   chars, sloka_sa, sloka_ta, mean_en, mean_ta, theme, setting,
                   hook_en, hook_ta, dlg_en, dlg_ta, trial_en, trial_ta,
                   rev_en, rev_ta, sadhana_en, sadhana_ta, close_en, close_ta):
    base_cam = [
        "Sweeping crane shot across the luminous Milk Ocean (Kshirabdhi) and golden Vaikuntha Gopuram",
        "Warm medium shot of the sage and seeker beside blooming Tulasi and lotus lamps",
        "Dynamic tracking shot through the churning cosmic waves of Maya toward the inner heart-cave",
        "Close-up on the radiant Sudarshana Chakra and Kaustubha gem reflecting in the seeker's eyes",
        "Grand 360-degree orbital reveal of Vishvarupa Narayana spanning galaxies and heart-space",
        "Intimate macro shot of Tulasi beads, Urdhvapundra tilaka, and tranquil breath synchronization",
        "Slow pull-back into eternal Vaikuntha light with golden Garuda wings and Pranava resonance"
    ]
    titles = [
        "The Cosmic Longing at Vaikuntha's Threshold",
        "The Seeker Questions the Sage",
        "Crossing the Ocean of Maya and Fear",
        "The Mahavakya of Narayana Consciousness",
        "Vision of the All-Pervading Vishvarupa",
        "Taraka Mantra, Bhakti & Inner Surrender",
        "Supreme Abode of Eternal Bliss (Vishnu-Pada)"
    ]
    cues = [
        "Panchajanya Shankha (conch) call + shimmering Veena arpeggio + ocean waves",
        "Melodic Carnatic flute in Raga Hamsadhwani + gentle temple bell",
        "Deep Mridangam pulse + swirling wind + meditative tanpura drone",
        "Celestial choir swell + golden chime + resonant Om Namo Narayanaya hum",
        "Majestic Nagaswaram & orchestral strings + cosmic heartbeat",
        "Peaceful Vrindavan/Kaveri river breeze + soft karatals (cymbals)",
        "Sustained Shankha & Veena harmonic fade into pure silence"
    ]
    scenes = []
    vo_pairs = [
        (hook_en, hook_ta),
        (dlg_en, dlg_ta),
        (trial_en, trial_ta),
        (f"{sloka_sa} — {mean_en}", f"{sloka_ta} — {mean_ta}"),
        (rev_en, rev_ta),
        (sadhana_en, sadhana_ta),
        (close_en, close_ta),
    ]
    for idx in range(7):
        ven, vta = vo_pairs[idx]
        scenes.append({
            "scene_num": idx + 1,
            "title": titles[idx],
            "camera": base_cam[idx],
            "flow_prompt": (
                f"Ultra-detailed 8K South Indian Vaishnava spiritual cinema, {setting}, "
                f"Scene {idx+1}: {titles[idx]}, featuring {chars}. Sapphire and molten-gold lighting, "
                f"glowing Tulasi and lotus petals in volumetric rays, authentic Divya Desam temple grandeur, "
                f"no text overlays, cinematic 16:9 framing."
            ),
            "vo_en": ven,
            "vo_ta": vta,
            "subtitle_cue": f"[Scene {idx+1}] {ven[:90]}... | {vta[:90]}...",
            "sound_cue": cues[idx]
        })
    return {
        "id": uid,
        "muktika_num": mnum,
        "name_en": name_en,
        "name_sa": name_sa,
        "name_ta": name_ta,
        "veda": veda,
        "category": "Vaishnava",
        "story_title_en": story_en,
        "story_title_ta": story_ta,
        "characters": chars,
        "sloka_sa": sloka_sa,
        "sloka_ta": sloka_ta,
        "sloka_meaning_en": mean_en,
        "sloka_meaning_ta": mean_ta,
        "theme": theme,
        "visual_setting": setting,
        "scenes": scenes
    }

VAISHNAVA_LIST = [
    make_vaishnava(
        "vaishnava_01_narayana", 18, "Narayana Upanishad", "नारायणोपनिषद्", "நாராயண உபநிஷதம்", "Krishna Yajur Veda",
        "The Cosmic Impulse of Narayana and the Eight-Syllabled Ashtakshara Mantra",
        "நாராயணனின் படைப்புச் சங்கல்பமும் அஷ்டாக்ஷர மந்திரத்தின் மகிமையும்",
        "Primordial Purusha Bhagavan Narayana & Vedic Rishis",
        "ॐ नमो नारायणायेति मन्त्रोपासनया वैकुण्ठभुवनं गमिष्यति ।",
        "ஓம் நமோ நாராயணாய இதி மந்த்ரோபாஸனயா வைகுண்ட புவனம் கமிஷ்யதி |",
        "By meditating on the eight-syllabled mantra 'Om Namo Narayanaya', the seeker attains the immortal realm of Vaikuntha.",
        "'ஓம் நமோ நாராயணாய' எனும் எட்டெழுத்து மந்திர உபாசனையால் சாதகன் அழிவற்ற வைகுண்டப் பேற்றை அடைகிறான்.",
        "Narayana as the source of Prana, Mind, Senses, Brahma, Rudra, and the liberating power of Ashtakshara.",
        "Radiant Kshirabdhi (Cosmic Ocean of Milk) where Ananta-Shayana Narayana glows like a million suns upon Adishesha",
        "In the primordial stillness before time, Purusha Haa Narayana desired: 'Let Me bring forth living beings from My own fullness.'",
        "காலம் தோன்றுவதற்கு முன் புருஷனான ஸ்ரீமந் நாராயணன், 'நான் உயிர்களைப் படைப்பேன்' எனத் திருவுள்ளம் கொண்டார்.",
        "From Narayana arose Prana, mind, all sense organs, space, wind, light, water, and the fertile earth.",
        "நாராயணனிடமிருந்தே பிராணன், மனம், இந்திரியங்கள், ஆகாயம், காற்று, நெருப்பு, நீர், பூமி அனைத்தும் தோன்றின.",
        "From Narayana emerged Brahma, Rudra, Indra, Prajapati, and the twelve Adityas—all sustained by His single breath.",
        "நாராயணனிடமிருந்தே பிரம்மா, உருத்திரன், இந்திரன், பிரஜாபதி, பன்னிரு ஆதித்தர்கள் தோன்றி நிலைபெறுகின்றனர்.",
        "The rishis discovered the supreme secret: 'Om' (1), 'Namo' (2), 'Narayanaya' (5)—the immortal eight-syllabled Ashtakshara.",
        "ரிஷிகள் பரம ரகசியத்தைக் கண்டனர்: 'ஓம்' (1), 'நமோ' (2), 'நாராயணாய' (5) எனும் எட்டெழுத்து மந்திரமே அமரத்துவம் தருவது.",
        "Within the inverted lotus bud of the heart burns an unwavering golden flame where Narayana dwells as the Inner Controller.",
        "இதயத் தாமரை மொட்டின் நடுவே அணையாத் தீபச் சுடராக நாராயணன் அந்தர்யாமியாக உறைகிறார்.",
        "Chanting 'Om Namo Narayanaya' with every breath, the seeker merges into the boundless lotus-eyed Lord.",
        "மூச்சு마다 'ஓம் நமோ நாராயணாய' என ஜபிக்கும் சாதகன் செந்தாமரைக் கண்ணனின் பேரொளியில் கலக்கிறான்."
    ),
    make_vaishnava(
        "vaishnava_02_nrisimhatapaniya", 27, "Nrisimhatapaniya Upanishad", "नृसिंहतापनीयोपनिषद्", "ந்ருஸிம்ஹதாபனீய உபநிஷதம்", "Atharva Veda",
        "Prajapati's Fearless Mantraraja: How the Man-Lion Lord Shatters Death and Maya",
        "பிரஜாபதி அருளிய மந்திரராஜம்: மரண பயம் போக்கும் நரசிம்மப் பெருமான்",
        "Lord Prajapati, the Devas, Prahlada & Bhagavan Lakshmi-Narasimha",
        "उग्रं वीरं महाविष्णुं ज्वलन्तं सर्वतोमुखम् । नृसिंहं भीषणं भद्रं मृत्युमृत्युं नमाम्यहम् ॥",
        "உக்ரம் வீரம் மஹாவிஷ்ணும் ஜ்வலந்தம் ஸர்வதோமுகம் | ந்ருஸிம்ஹம் பீஷணம் பத்ரம் ம்ருத்யும்ருத்யும் நமாம்யஹம் ||",
        "I bow to Lord Nrisimha—heroic, all-pervading Maha-Vishnu, blazing in all directions, terrifying to evil, auspicious, the Death of death itself!",
        "உக்கிரமானவரும், வீரரும், எங்கும் சுடர்விடும் மகாவிஷ்ணுவும், மரணத்திற்கே மரணமான மங்கள நரசிம்மரை வணங்குகிறேன்!",
        "The 32-syllabled Anushtubh Mantraraja of Nrisimha and the six-spoked Sudarshana Chakra protecting the soul.",
        "Towering golden pillar splitting open in a burst of solar lightning to reveal serene yet majestic Lakshmi-Narasimha",
        "Afflicted by fear of death, darkness, and samsara, the Devas approached Prajapati begging for an invincible spiritual fortress.",
        "மரண பயத்தாலும் சம்சார இருளாலும் வாடிய தேவர்கள் பிரஜாபதியிடம் அழியாத ஆன்மீகக் கோட்டையை வேண்டினர்.",
        "Prajapati revealed the king of all mantras—the 32-syllabled Nrisimha Anushtubh Mantraraja, crowned by Pranava.",
        "பிரஜாபதி மந்திரங்களுக்கெல்லாம் அரசனான 32 எழுத்து நரசிம்ம அனுஷ்டுப் மந்திரராஜத்தை உபதேசித்தார்.",
        "He explained each word: 'Ugram' because He uproots ignorance; 'Viram' because He empowers the soul; 'Mahavishnum' because He pervades all.",
        "'உக்ரம்' அறியாமையை வேரறுப்பது; 'வீரம்' ஆன்ம பலம் தருவது; 'மகாவிஷ்ணும்' எங்கும் நிறைந்தது என விளக்கினார்.",
        "Blazing on all sides ('Jvalantam Sarvatomukham'), Nrisimha is terrifying to ego-demons yet infinitely auspicious ('Bhadram') to devotees like Prahlada.",
        "அகங்கார அசுரர்களுக்கு அச்சம் தருபவராயினும், பிரகலாதன் போன்ற அடியார்களுக்குப் பரம மங்களமானவர் நரசிம்மர்.",
        "Around the seeker spins the blazing Sudarshana Mahachakra of 6, 8, 12, and 32 spokes, burning away every inner obstacle.",
        "சாதகனைச் சுற்றி சுழலும் சுதர்சன மகாசக்கரம் அனைத்து அகத் தடைகளையும் சுட்டெரித்துக் காக்கிறது.",
        "Realizing Nrisimha as the Fourth (Turiya) pure consciousness beyond waking, dream, and sleep, the yogi becomes fearless forever.",
        "விழிப்பு, கனவு, உறக்கம் கடந்த துரிய அறிவே நரசிம்மம் என உணரும் யோகி என்றென்றும் அச்சமற்றவனாகிறான்."
    ),
    make_vaishnava(
        "vaishnava_03_mahanarayana", 52, "Mahanarayana Upanishad", "महानारायणोपनिषद्", "மஹாநாராயண உபநிஷதம்", "Krishna Yajur Veda",
        "The Flame Inside the Heart-Lotus and the Cosmic Hymn of Narayana Suktam",
        "இதயத் தாமரையின் நீலச் சுடரும் நாராயண சூக்தத்தின் பிரபஞ்ச முழக்கமும்",
        "Sage Yajnavalkya, Ambhrini & Indwelling Lord Narayana",
        "अन्तर्बहिश्च तत्सर्वं व्याप्य नारायणः स्थितः । नीलतोयदमध्यस्था विद्युल्लेखेव भास्वरा ।",
        "அந்தர்பஹிஶ்ச தத்ஸர்வம் வ்யாப்ய நாராயண: ஸ்தித: | நீலதோயத மத்யஸ்தா வித்யுல்லேகேவ பாஸ்வரா |",
        "Pervading everything inside and outside stands Narayana—shining like a streak of golden lightning within a dark-blue raincloud in the heart.",
        "உள்ளும் புறமும் அனைத்தையும் ஊடுருவி நிற்கும் நாராயணன், இதயத்தில் கார்மேகத்தின் நடுவே மின்னல் கொடி போல் ஒளிர்கிறான்.",
        "Meditating on the Dahara-akasha (subtle heart-space) flame and living every action as a cosmic sacrifice (Yajna).",
        "Cosmic vision transitioning from starry galaxies into a microscopic golden flame inside an inverted lotus bud in the chest",
        "The sages asked: 'Where does the infinite Lord who is smaller than an atom and greater than the cosmos actually reside?'",
        "'அணுவிற்கும் அணுவாய், அண்டத்திற்கும் பெரியதாய் விளங்கும் இறைவன் எங்கே உறைகிறான்?' என முனிவர்கள் கேட்டனர்.",
        "The Upanishad revealed: whatever is seen or heard in this universe, Narayana pervades it both inside and outside!",
        "இவ்வுலகில் காணப்படுவதும் கேட்கப்படுவதும் எதுவாயினும், அதன் உள்ளும் புறமும் நாராயணனே வியாபித்துள்ளான்!",
        "Within the citadel of the body lies the small lotus of the heart, pointing downward until awakened by Pranayama and devotion.",
        "உடல் எனும் கோட்டைக்குள் இருக்கும் இதயத் தாமரை, பிராணாயாமத்தாலும் பக்தியாலும் மேல்நோக்கி மலர்கிறது.",
        "In its center dances a steady flame, slender as the awn of a paddy grain, glowing like golden lightning inside a blue cloud.",
        "அதன் நடுவே நெல் நுனி போல் நுட்பமான அக்னிச் சுடரில், நீல மேகத்தில் மின்னல் போல் பரமாத்மா பிரகாசிக்கிறான்.",
        "Truth (Satya), austerity (Tapas), self-control (Dama), peace (Shama), and charity (Dana) are the pillars of this inner temple.",
        "சத்தியம், தவம், புலனடக்கம், சமம், தானம் ஆகியவையே இந்த அகக் கோயிலின் தாங்கும் தூண்களாகும்.",
        "Abiding in that heart-flame where Mahesha, Brahma, and Vishnu are One, the seeker attains supreme immortality.",
        "மும்மூர்த்திகளும் ஒன்றாக ஒளிரும் அந்த இதயச் சுடரில் நிலைபெறும் சாதகன் பரம அமரத்துவம் அடைகிறான்."
    ),
    make_vaishnava(
        "vaishnava_04_ramarahasya", 54, "Ramarahasya Upanishad", "रामरहस्योपनिषद्", "ராமரஹஸ்ய உபநிஷதம்", "Atharva Veda",
        "Hanuman Reveals to Sanaka and the Rishis: Why the Name 'Rama' Equals the Entire Tantra & Veda",
        "சனகாதி முனிவர்களுக்கு அனுமன் உரைத்த ராம நாம ரகசியம்",
        "Bhakta Hanuman, Sanaka, Prahlada, Vibhishana & Sri Rama",
        "रमन्ते योगिनोऽनन्ते नित्यानन्दे चिदात्मनि । इति रामपदेनासौ परं ब्रह्माभिधीयते ॥",
        "ரமந்தே யோகினோனந்தே நித்யானந்தே சிதாத்மனி | இதி ராமபதேனாஸௌ பரம் ப்ரஹ்மாபிதீயதே ||",
        "Because yogis revel in the infinite, eternal bliss of pure Consciousness, that Supreme Brahman itself is called 'Rama'!",
        "யோகிகள் எல்லையற்ற நித்திய ஆனந்த சிதாத்மாவில் ரமிப்பதால் (மகிழ்வதால்), அந்தப் பரப்பிரம்மமே 'ராமன்' எனப்படுகிறது!",
        "Hanuman's direct realization that Sita is Mulaprakriti, Lakshmana is protective awareness, and Rama is Parabrahman.",
        "Sacred grove in Ayodhya beside the Sarayu river where radiant Hanuman sits surrounded by glowing rishis",
        "Great sages headed by Sanaka and devotees like Prahlada and Vibhishana asked Hanuman: 'O Maruti! What is the supreme truth of the Vedas?'",
        "சனகாதி முனிவர்களும் பிரகலாதன், விபீஷணன் ஆகியோரும் அனுமனிடம், 'மாருதி! வேதங்களின் പരम ரகசியம் எது?' எனக் கேட்டனர்.",
        "Hanuman folded his hands in thrilled devotion and declared: 'Among all truths, the Taraka Brahman Sri Rama is the highest!'",
        "அனுமன் கரம் கூப்பி ஆனந்தத்துடன், 'அனைத்து தத்துவங்களிலும் தாரக பிரம்மமான ஸ்ரீ ராமனே மேலானவர்!' என்றார்.",
        "Sita Devi is primordial Prakriti (creative energy), and Sri Rama is pure Consciousness—their union sustains all worlds.",
        "சீதா பிராட்டியே மூலப் பிரகிருதி; ஸ்ரீ ராமனே சுத்த சைதன்யம்; இவ்விருவரின் இணைப்பே உலகங்களைக் காக்கிறது.",
        "Even the two syllables 'Ra-Ma' combine the fire-seed of Ashtakshara ('Ra' from Narayanaya) and the nectar-seed of Panchakshara ('Ma' from Namah Shivaya).",
        "'ரா-ம' எனும் இரண்டெழுத்தில் நாராயண மந்திரத்தின் உயிரான 'ர'கரமும், சிவ மந்திரத்தின் உயிரான 'ம'கரமும் இணைந்துள்ளன.",
        "Meditating on Rama seated under the Kalpavriksha tree with Sita, Lakshmana, and Hanuman fulfills every spiritual aspiration.",
        "கற்பக விருட்சத்தின் கீழ் சீதை, இலக்குவன், அனுமனுடன் வீற்றிருக்கும் ராமனைத் தியானித்தால் சகல சித்திகளும் கைகூடும்.",
        "Repeating the sweet name of Rama ninety-six million times—or even once with total love—liberates the soul into eternal bliss.",
        "தூய அன்போடு ராம நாமத்தை உச்சரிப்பவன் பிறவிப் பெருங்கடலைக் கடந்து நித்திய ஆனந்தத்தில் திளைக்கிறான்."
    ),
    make_vaishnava(
        "vaishnava_05_ramatapaniya", 55, "Ramatapaniya Upanishad", "रामतापनीयोपनिषद्", "ராமதாபனீய உபநிஷதம்", "Atharva Veda",
        "Shiva Whispers the Six-Syllabled Rama Taraka Mantra in Sacred Kashi",
        "காசியில் சிவபெருமான் உபதேசிக்கும் ஆறெழுத்து ராம தாரக மந்திரம்",
        "Lord Vishvanatha Shiva, Goddess Parvati, Sage Yajnavalkya & Sri Ramachandra",
        "रां रामाय नमः इति षडक्षरमन्त्रराजः संसारार्णवतारकः ।",
        "ராம் ராமாய நம: இதி ஷடக்ஷர மந்த்ரராஜ: ஸம்ஸாரார்ணவ தாரக: |",
        "'Ram Ramaya Namah'—this six-syllabled King of Mantras ferries all beings across the ocean of Samsara.",
        "'ராம் ராமாய நமஹ' எனும் ஆறெழுத்து மந்திரராஜமே பிறவிப் பெருங்கடலைக் கடக்கச் செய்யும் தாரக மந்திரம்.",
        "The cosmic Yantra of Sri Rama and Lord Shiva's role as the eternal Guru imparting the Taraka mantra in Kashi.",
        "Luminous Kashi Vishvanatha sanctum merging into the golden throne room of Ayodhya with the eight-petalled Rama Yantra",
        "Goddess Parvati asked Lord Shiva in Kailasa: 'O Lord! How does the boundless, formless Brahman take the sweet form of Prince Rama?'",
        "கைலாயத்தில் பார்வதி தேவி ஈசனிடம், 'இறைவா! உருவமற்ற பரப்பிரம்மம் எப்படி தசரத ராமனாக வடிவெடுத்தது?' எனக் கேட்டாள்.",
        "Shiva replied: just as liquid ghee solidifies into rich butter for the delight of devotees, Chinmaya Brahman appears as Sri Rama.",
        "உருகிய நெய் அடியார்களுக்காக உறைந்து வெண்ணெய் ஆவது போல், சின்மய பிரம்மமே ஸ்ரீ ராமனாகத் தோன்றியது என்றார் சிவன்.",
        "Shiva revealed why He resides in Kashi: to whisper the Taraka Mantra ('Ram Ramaya Namah') into the ear of departing souls.",
        "காசியில் முக்தி அடையும் உயிர்களின் செவியில் 'ராம் ராமாய நமஹ' எனும் தாரக மந்திரத்தை ஓதவே தான் அங்கு உறைவதாகக் கூறினார்.",
        "In the heart's eight-petalled lotus Yantra sits Sri Rama holding the Jnana-mudra and bow, flanked by Sita and Lakshmana.",
        "இதயத்தின் எட்டு இதழ் தாமரை யந்திரத்தில் ஞான முத்திரையுடன் சீதா-லக்ஷ்மண சமேதராக ஸ்ரீ ராமன் வீற்றிருக்கிறார்.",
        "Sage Yajnavalkya confirmed: whether learned or unlearned, whoever takes refuge in this Taraka name crosses all sorrow.",
        "கற்றவராயினும் கல்லாதவராயினும், இந்த தாரக நாமத்தைச் சரணடைபவர் அனைத்துத் துயரங்களையும் கடப்பார் என யாக்ஞவல்கியர் உறுதிப்படுத்தினார்.",
        "Where Rama's name is sung with devotion, Kashi itself manifests, and the soul shines as immortal Sachidananda.",
        "ராம நாமம் ஒலிக்கும் இடமே காசி க்ஷேத்திரமாகி, ஆன்மா சச்சிதானந்தப் பேரொளியாக மிளிர்கிறது."
    ),
    make_vaishnava(
        "vaishnava_06_vasudeva", 56, "Vasudeva Upanishad", "वासुदेवोपनिषद्", "வாஸுதேவ உபநிஷதம்", "Sama Veda",
        "Narada & Krishna: The Sacred Secret of Gopichandana and Urdhvapundra",
        "நாரதரும் ஸ்ரீ கிருஷ்ணரும்: கோபிசந்தனமும் ஊர்த்வபுண்டர தத்துவமும்",
        "Devarshi Narada & Bhagavan Sri Vasudeva Krishna",
        "ऊर्ध्वपुण्ड्रं धारयेद्यस्तु गोपीचन्दनمرत्तिकया स वासुदेवो भवति ।",
        "ஊர்த்வபுண்ட்ரம் தாரயேத் யஸ்து கோபீசந்தன మృத்திகயா ஸ வாஸுதேவோ பவதி |",
        "He who wears the vertical Urdhvapundra mark with sacred Gopichandana clay awakens his inner identity with Lord Vasudeva.",
        "கோபிசந்தனத்தால் ஊர்த்வபுண்டரத் திருமண் தரிப்பவன் தன் உள்ளே உறையும் வாசுதேவ தத்துவத்தை உணர்கிறான்.",
        "The vertical Urdhvapundra mark as the upward pathway of Sushumna leading to the supreme Vishnupada.",
        "Dvaraka palace courtyard overlooking the turquoise sea, where Narada with his Mahati veena bows before Lord Krishna",
        "Devarshi Narada bowed before Lord Vasudeva Krishna and asked: 'Lord, teach me the sacred rule and inner meaning of Gopichandana.'",
        "தேவர்ஷி நாரதர் வாசுதேவ கிருஷ்ணரை வணங்கி, 'இறைவா! கோபிசந்தன ஊர்த்வபுண்டரத்தின் விதியையும் உட்பொருளையும் கூறுங்கள்' என்றார்.",
        "Krishna smiled: Gopichandana is the sacred golden clay washed by the feet of the Gopis of Vrindavan and blessed by Chakratirtha.",
        "கிருஷ்ணர் புன்னகைத்து, 'கோபியரின் பாதம் பட்ட துவாரகை சக்ரதீர்த்தப் புனித மண்ணே கோபிசந்தனம்' என அருளினார்.",
        "Drawing the vertical Urdhvapundra lines upward from the nose bridge symbolizes the upward ascent of Prana toward Brahmarandhra.",
        "மூக்கின் நுனியிலிருந்து மேல்நோக்கி இடும் ஊர்த்வபுண்டரம், பிராணன் சுழுமுனை வழியே மேலேறுவதைக் குறிக்கிறது.",
        "Between the two vertical lines of Brahma and Rudra shines the central space—the seat of Sri Lakshmi and Lord Hari.",
        "இரு செங்குத்துக் கோடுகளின் நடுவே உள்ள திருவெளியே மகாலட்சுமியும் ஸ்ரீ ஹரியும் உறையும் திருத்தலம்.",
        "Adorning the twelve body centers with the twelve Kesava names turns the human body into a consecrated temple of Vishnu.",
        "கேசவாதி பன்னிரு நாமங்களால் உடலின் பன்னிரு இடங்களில் திருமண் தரிப்பது உடலை விஷ்ணு ஆலயமாக்குகிறது.",
        "For the realized yogi, the true Urdhvapundra is the single flame of Vasudeva-consciousness shining inside the heart.",
        "ஞான யோகிக்கு இதயக் குகையில் மேல்நோக்கிச் சுடர்விடும் வாசுதேவ அறிவே உண்மையான ஊர்த்வபுண்டரம் ஆகும்."
    ),
    make_vaishnava(
        "vaishnava_07_avyakta", 68, "Avyakta Upanishad", "अव्यक्तोपनिषद्", "அவ்யக்த உபநிஷதம்", "Sama Veda",
        "Prajapati's Tapas: How the Unmanifest Light Revealed the 32-Syllabled Anushtubh",
        "பிரஜாபதியின் தவம்: அவ்யக்தப் பேரொளியில் உதித்த முப்பத்திரண்டு எழுத்து வித்தை",
        "Lord Prajapati, Indra & the Unmanifest Avyakta Nrisimha-Hari",
        "नान्यद्वैदं विजानन्तं परं ज्योतिरव्यक्तम् ।",
        "நான்யத் வைதம் விஜானந்தம் பரம் ஜ்யோதிர் அவ்யக்தம் |",
        "Before creation there was nothing other than the Unmanifest Supreme Light, self-luminous and boundless.",
        "படைப்பிற்கு முன் சுயம்பிரகாசமான, எல்லையற்ற அவ்யக்தப் பேரொளியைத் தவிர வேறு எதுவும் இருக்கவில்லை.",
        "How Prajapati beheld the Green-and-Golden Cosmic Purusha (Harit-Pingala) and created the worlds through the Anushtubh hymn.",
        "Primordial golden-emerald nebula where Prajapati meditates on a thousand-petalled lotus",
        "In the beginning, nothing was manifest—only infinite, self-shining Avyakta (Unmanifest) Consciousness pervaded all space.",
        "ஆதியில் எதுவும் வெளிப்படவில்லை; சுய ஒளியான அவ்யக்த (வெளிப்படாத) சைதன்யம் மட்டுமே எங்கும் நிறைந்திருந்தது.",
        "From that Unmanifest Light arose Prajapati seated upon a cosmic lotus leaf, wondering: 'Why am I here, and what is my support?'",
        "அந்த அவ்யக்த ஒளியிலிருந்து தாமரை இலையில் தோன்றிய பிரஜாபதி, 'என் ஆதாரம் எது?' என ஆழ்ந்த தவத்தில் அமர்ந்தார்.",
        "After a thousand years of Tapas, he beheld the wondrous Harit-Pingala Purusha—half emerald-grace (Sri), half molten-gold (Nrisimha).",
        "ஆயிரம் ஆண்டுகள் தவத்திற்குப் பின், மரகதப் பசுமையும் பொன்னொளியும் இணைந்த அற்புதப் புருஷனைத் தரிசித்தார்.",
        "That Supreme Lord imparted the 32-syllabled Sama-Anushtubh mantra, whose 32 letters are the 32 Devas and cosmic principles.",
        "அந்தப் பரம புருஷன் முப்பத்திரண்டு தேவர்களின் சக்தி கொண்ட 32 எழுத்து சாம-அனுஷ்டுப் வித்தையை உபதேசித்தார்.",
        "Using those sacred syllables as building blocks, Prajapati wove the three Vedas, the sun, moon, and living worlds.",
        "அந்த முப்பத்திரண்டு அக்ஷரங்களைக் கொண்டே பிரஜாபதி மூன்று வேதங்களையும், சூரிய சந்திர உலகங்களையும் படைத்தார்.",
        "Whoever meditates on this Avyakta Vidya daily transcends the manifest universe and returns to the immortal Light.",
        "இந்த அவ்யக்த வித்தையை நாள்தோறும் தியானிப்பவர் தோற்ற உலகைக் கடந்து அழியாத பேரொளியில் கலக்கிறார்."
    )
]


VAISHNAVA_LIST.extend([
    make_vaishnava(
        "vaishnava_08_tarasara", 91, "Tarasara Upanishad", "तारसारोपनिषद्", "தாரஸார உபநிஷதம்", "Shukla Yajur Veda",
        "Yajnavalkya & Bharadvaja: Crossing the Ocean of Births via the Eightfold Omkara Narayana",
        "யாக்ஞவல்கியரும் பரத்வாஜரும்: பிறவிக்கடல் தாண்டும் எட்டெழுத்து ஓங்கார நாராயணன்",
        "Maharishi Yajnavalkya, Sage Bharadvaja & Eightfold Omkara Narayana",
        "ॐ नमो नारायणायेति तारकं चिदात्मकं नित्यमुपास्यं... तत्त्वमसि नारायणोऽहम् ।",
        "ஓம் நமோ நாராயணாயேதி தாரகம் சிதாத்மகம் நித்யமுபாஸ்யம்... தத்வமஸி நாராயணோஹம் |",
        "'Om Namo Narayanaya' is the liberating Taraka mantra of pure Consciousness, eternally to be meditated upon—Thou art That, I am Narayana!",
        "'ஓம் நமோ நாராயணாய' என்பதே பிறவிக்கடல் தாண்டும் சித்-சொரூப தாரக மந்திரம்; அதுவே நீயாக இருக்கிறாய், நானே நாராயணன்!",
        "Unifying Shukla Yajur Veda's Purna-Brahman with the eight subtle syllables of Om and the Ashtakshara mantra in Kurukshetra/Avimukta.",
        "Sacred confluence of Kurukshetra and Avimukta Kashi where Sage Yajnavalkya reveals the glowing eight-part Omkara to Bharadvaja",
        "Sage Bharadvaja approached Yajnavalkya and asked: 'Revered Master, where does the Imperishable dwell, and how do we cross samsara?'",
        "பரத்வாஜ முனிவர் யாக்ஞவல்கியரை வணங்கி, 'குருவே! அழியாத பரம்பொருள் எங்கு உறைகிறார்? பிறவிக்கடலைக் கடப்பது எவ்வாறு?' எனக் கேட்டார்.",
        "Yajnavalkya answered: 'Seek the inner Kurukshetra and Avimukta between the eyebrows and the heart, and board the boat of Taraka Pranava!'",
        "யாக்ஞவல்கியர் கூறினார்: 'தேவர்களைக் காக்கும் அக குருக்ஷேத்திரத்தையும் அவிமுக்தத் தலத்தையும் நாடி, பிரணவ தாரகப் படகில் ஏறுவாயாக!'",
        "From 'A-kara' arises Brahma, from 'U-kara' arises Vishnu, and from 'Ma-kara' arises Shiva, crowned by Bindu, Nada, Kala, Kalatita, and Paratpara.",
        "'அ'காரத்தில் பிரம்மாவும், 'உ'காரத்தில் விஷ்ணுவும், 'ம'காரத்தில் ருத்ரனும், மேலே பிந்து, நாதம், களை, கலாதீதம், பராৎபரமும் ஒளிர்கின்றன.",
        "These eight subtle limbs of Omkara unite with the eight syllables of 'Om Namo Narayanaya' as the cosmic body of Bhagavan Narayana.",
        "ஓங்காரத்தின் இந்த எட்டு நுண்ணிய அங்கங்களும் 'ஓம் நமோ நாராயணாய' எனும் எட்டெழுத்து மந்திரத்துடன் இணைந்து நாராயண சொரூபமாகின்றன.",
        "Chanting the Ashtakshara with the awareness 'I am that immortal Narayana', all karmic knots of the heart snap instantly.",
        "'அந்த அமிர்தமயமான நாராயணனே நான்' எனும் பாவனையுடன் அஷ்டாக்ஷரத்தை ஜபிக்க, இதய முடிச்சுகள் அவிழ்கின்றன.",
        "The Whole comes forth from the Whole, and the liberated sage remains forever as Purna Narayana.",
        "பூரணத்திலிருந்து பூரணம் தோன்றி, முக்தியடைந்த ஞானி நித்திய பூரண நாராயணனாகவே நிலைபெறுகிறான்."
    ),
    make_vaishnava(
        "vaishnava_09_gopalatapaniya", 95, "Gopala-tapaniya Upanishad", "गोपालतापनीयोपनिषद्", "கோபாலதாபனீய உபநிஷதம்", "Atharva Veda",
        "The Four Kumaras & Brahma: The Flute-Playing Govinda Under Vrindavana's Kalpavriksha",
        "நால்வர் குமாரர்களும் பிரம்மாவும்: விருந்தாவன கற்பக விருட்சத்தின் கீழ் குழலூதும் கோவிந்தன்",
        "Sanatkumara & the Four Kumaras, Creator Brahma, Sage Durvasa, Gopis & Bhagavan Gopala Krishna",
        "गोविन्दं सच्चिदानन्दं विग्रहं वृन्दावनसुरभूरुहतलासीनं सततं स्मरेत् ।",
        "கோவிந்தம் ஸச்சிதானந்த விக்ரஹம் வ்ருந்தாவன ஸுரபூருஹ தலாஸீனம் ஸததம் ஸ்மரேத் |",
        "Meditate ever upon Govinda—the embodiment of Sat-Chit-Ananda, seated beneath the celestial Kalpavriksha tree in Vrindavana!",
        "விருந்தாவனத்தின் தேவ கற்பக விருட்சத்தின் கீழ் வீற்றிருக்கும் சச்சிதானந்த சொரூபனான கோவிந்தனை எப்போதும் தியானிப்போம்!",
        "Revealing Shyamasundara Gopala Krishna as the Supreme Brahman through the 18-syllable Gopala Mantra and Durvasa's paradox of fasting.",
        "Luminous golden lotus of Mathura-Vrindavana under a jeweled Kalpavriksha tree where dark-blue Gopala Krishna plays His flute surrounded by cows and Gopis",
        "In Brahmaloka, the four Sanatkumaras asked their father Brahma: 'Who is the Supreme God of Gods? Whom does Death itself fear?'",
        "பிரம்மலோகத்தில் சனத்குமாரர்கள் பிரம்மதேவரிடம் கேட்டனர்: 'தேவர்களுக்கெல்லாம் பரம தேவன் யார்? மரணமும் அஞ்சுவது யாருக்கு?'",
        "Brahma replied in reverence: 'Sri Krishna, the eternal Gopala—Sat-Chit-Ananda in form—is the One Supreme Brahman!'",
        "பிரம்மதேவர் பணிவுடன் கூறினார்: 'சச்சிதானந்த வடிவமான கோபால கிருஷ்ணனே முழுமுதற் பரப்பிரம்மம்!'",
        "In Vrindavana, upon a thousand-petalled golden lotus beneath the wish-fulfilling Kalpavriksha, stands Shyamasundara wearing the Kaustubha gem.",
        "விருந்தாவனத்தில் ஆயிரம் இதழ் பொற்றாமரை மீது, கற்பக மரத்தடியில் கௌஸ்துப மணி மார்பனாகச் சியாமளக் கண்ணன் நிற்கிறான்.",
        "When the Gopis crossed the parted Yamuna to feed Sage Durvasa, Durvasa revealed why Krishna is the 'eternal faster and celibate'—the unattached Witness Self.",
        "யமுனை வழிவிட துர்வாசருக்கு உணவளித்த கோபியரிடம், ஆன்மா கர்மங்களில் ஒட்டாத சர்வ சாட்சி என்பதால் கண்ணன் நித்திய உபவாசி என முனிவர் விளக்கினார்.",
        "Meditating on the 18-syllable five-part mantra 'Klim Krishnaya Govindaya Gopijanavallabhaya Svaha', ego-separation dissolves.",
        "'க்லீம் கிருஷ்ணாய கோவிந்தாய கோபிஜனவல்லபாய ஸ்வாஹா' எனும் பதினெட்டெழுத்து மந்திரத்தைத் தியானிக்க அகங்காரப் பிரிவு கரைகிறது.",
        "Absorbed in Govinda's flute-call of Pranava, the seeker tastes the immortal nectar of Prema-Bhakti and Advaita.",
        "கோவிந்தனின் பிரணவக் குழலிசையில் லயிக்கும் சாதகன், பிரேம பக்தியும் அத்வைத முக்தியும் பெறுகிறான்."
    ),
    make_vaishnava(
        "vaishnava_10_krishna", 96, "Krishna Upanishad", "कृष्णोपनिषद्", "கிருஷ்ண உபநிஷதம்", "Atharva Veda",
        "From Dandakaranya to Gokula: How the Vedas and Virtues Reborn Around Bala Krishna",
        "தண்டகாரண்யம் முதல் கோகுலம் வரை: பாலகிருஷ்ணனைச் சூழ்ந்து அவதரித்த வேதங்களும் நற்பண்புகளும்",
        "Rishis of Dandakaranya, Sri Ramachandra, Nanda-Yashoda, Gopis & Bhagavan Bala Krishna",
        "यो नन्दः परमानन्दो यशोदा मुक्तिगेहिनी । माया सा त्रिविधा प्रोक्ता सत्त्वराजसतामसी ॥",
        "யோ நந்த: பரமானந்தோ யஸோதா முக்திகேஹினீ | மாயா ஸா த்ரிவிதா ப்ரோக்தா ஸத்வ ராஜஸ தாமஸீ ||",
        "Nanda is Supreme Bliss (Paramananda), Yashoda is the very Abode of Liberation (Mukti), and in their courtyard plays the Supreme Brahman as Krishna!",
        "நந்தகோபரே பரமானந்தம், யசோதையே முக்தியின் உறைவிடம்; அவர்களின் முற்றத்தில் பரப்பிரம்மமே கிருஷ்ணனாக விளையாடுகிறது!",
        "Allegorical Vedantic revelation of Gokula: every person, ornament, weapon, and cowherd in Krishna's Lila is a cosmic principle or Upanishadic truth.",
        "Enchanted twilight courtyard of Gokula transitioning from Dandakaranya forest, where the 16,108 Upanishadic Rik-mantras dance as Gopis around Sri Krishna",
        "In the ancient forest of Dandakaranya, the great Rishis beheld the radiant beauty of Lord Ramachandra and longed to embrace Him.",
        "தண்டகாரண்ய வனத்து முனிவர்கள் ஸ்ரீராமச்சந்திரனின் பேரழகைக் கண்டு, அவரை ஆரத் தழுவ வேண்டும் என ஏங்கினர்.",
        "Lord Rama blessed them gently: 'In My Krishna Avatar in Gokula, you shall be reborn as Gopis and embrace Me in pure love!'",
        "ஸ்ரீராமர் புன்னகையுடன் அருளினார்: 'எனது கிருஷ்ணாவதாரத்தில் நீங்கள் கோபியராகப் பிறந்து என்னைப் பேரன்பால் தழுவுவீர்கள்!'",
        "When Purna-Brahman descended in Gokula, Nanda became Supreme Bliss, Yashoda became Mukti, the Vedas became cows, and the Upanishads became 16,108 Gopis.",
        "பூரணப் பிரம்மம் கோகுலத்தில் அவதரித்தபோது, நந்தர் பரமானந்தமாகவும், யசோதை முக்தியாகவும், வேதங்கள் பசுக்களாகவும், உபநிஷதங்கள் கோபியராகவும் திகழ்ந்தனர்.",
        "Compassion became Mother Rohini, Peace became Satyabhama, Truth became Akroora, Self-Control became Uddhava, and Rudra became Krishna's bamboo flute!",
        "கருணையே ரோகிணியாகவும், சத்தியமே அக்ரூரராகவும், மனவடக்கமே உத்தவராகவும், சிவபெருமானே கண்ணனின் புல்லாங்குழலாகவும் மாறினர்!",
        "Meditating on Gokula as supreme Vaikuntha in the heart, the seeker churns the Ocean of Milk into the white butter of Self-Knowledge.",
        "கோகுலத்தையே இதய வைகுண்டமாகத் தியானிக்கும் சாதகன், பாற்கடலைக் கடைந்து ஆத்ம ஞானம் எனும் வெண்ணெயைப் பெறுகிறான்.",
        "Even the mortar to which Yashoda tied Krishna was stripped of ego, showing that Supreme Brahman is bound only by pure Devotion.",
        "ஆணவமற்ற தூய அன்பிற்கு மட்டுமே பரம்பொருள் கட்டுப்படும் என்பதைக் காட்டி, கோகுலமே வைகுண்டமாகப் பிரகாசித்தது."
    ),
    make_vaishnava(
        "vaishnava_11_hayagriva", 100, "Hayagriva Upanishad", "हयग्रीवोपनिषद्", "ஹயக்ரீவ உபநிஷதம்", "Atharva Veda",
        "The Pure Crystal Wisdom of Lord Hayagriva Who Restored the Stolen Vedas",
        "வேதங்களை மீட்டெடுத்த ஸ்படிகப் பேரொளி: ஞானானந்தமயனான ஸ்ரீ ஹயக்ரீவர்",
        "Devarishi Narada, Creator Brahma & Bhagavan Lakshmi-Hayagriva",
        "ज्ञानानन्दमयं देवं निर्मलं स्फटिकाकृतिम् । आधारं सर्वविद्यानां हयग्रीवमुपास्महे ॥",
        "ஞானானந்தமயம் தேவம் நிர்மலம் ஸ்படிகாக்ருதிம் | ஆதாரம் ஸர்வவித்யானாம் ஹயக்ரீவமுபாஸ்மஹே ||",
        "We meditate upon Lord Hayagriva, who is the embodiment of Knowledge and Bliss, pure as flawless crystal, and the foundation of all sciences!",
        "ஞானமும் ஆனந்தமும் நிறைந்தவரும், தூய ஸ்படிகம் போன்ற திருமேனியரும், அனைத்துக் கலைகளுக்கும் ஆதாரமானவருமான ஹயக்ரீவரை தியானிக்கிறோம்!",
        "Awakening supreme Vedic intelligence, speech (Vak), and Brahma-Vidya through the Mantra-raja of the Horse-Necked Lord Hayagriva.",
        "Dazzling white-lotus throne in Svetadvipa where four-armed Lord Hayagriva with a radiant white horse-countenance holds conch, discus, rosary, and Vedic scripture",
        "Devarishi Narada bowed to Creator Brahma and asked: 'Father, reveal to me that supreme Brahma-Vidya which destroys all sins and grants mastery of all wisdom!'",
        "தேவரிஷி நாரதர் பிரம்மதேவரை வணங்கி, 'தந்தையே! சகல பாவங்களையும் போக்கி, அனைத்து வித்தைகளையும் அருளும் பிரம்ம வித்தையை உபதேசியுங்கள்!' என்றார்.",
        "Brahma replied: 'When the demons of ignorance stole the Vedas into the dark abyss, the Supreme Lord manifested with a resplendent Horse-Countenance—Hayagriva!'",
        "பிரம்மதேவர் கூறினார்: 'அறியாமை அசுரர்கள் வேதங்களைக் கவர்ந்தபோது, பரம்பொருள் தூய வெள்ளைக் குதிரை முகத்துடன் ஹயக்ரீவராகத் தோன்றினார்!'",
        "His sacred neighing roar (*Udgitha*) vibrated as the primordial Omkara, shattering darkness and restoring the Upanishads.",
        "அவரது புனிதக் கனைப்பொலி பிரணவ ஓங்காரமாக ஒலித்து, அறியாமை இருளைப் பிளந்து வேத உபநிஷதங்களை மீட்டது.",
        "Pure as autumn moonlight and crystal, His four hands hold the Panchajanya conch, Sudarshana chakra, Japa-mala, and the Book of Jnana-Mudra.",
        "ஸ்படிகமும் குளிர் நிலவும் போன்ற அவர் திருக்கரங்களில் சங்கு, சக்கரம், ஜபமாலை மற்றும் ஞானமுத்திரைப் புத்தகம் மிளிர்கின்றன.",
        "Meditating on the king of mantras—'Lhoum Namah Visvarupaya Visvajihvaya Hayagrivaya'—a billion suns of wisdom dawn in the intellect.",
        "ஹயக்ரீவ மந்திரராஜனைத் தியானிப்பவனின் புத்தியில் கோடி சூர்யப் பிரகாசத்துடன் மெய்ஞ்ஞானம் உதயமாகிறது.",
        "Even one devoid of learning becomes an eloquent poet and knower of Brahman by the grace of Sri Hayagriva.",
        "ஸ்ரீ ஹயக்ரீவரின் அருளால், கல்லாதவனும் சிறந்த வாக்கு வன்மையும் பிரம்ம ஞானமும் பெற்று முக்தியடைகிறான்."
    ),
    make_vaishnava(
        "vaishnava_12_dattatreya", 101, "Dattatreya Upanishad", "दत्तात्रेयोपनिषद्", "தத்தாத்ரேய உபநிஷதம்", "Atharva Veda",
        "Brahma's Question to Vishnu: The Avadhuta Cosmic Guru Dattatreya",
        "விஷ்ணுவிடம் பிரம்மா கேட்ட வரம்: அவதூத குரு தத்தாத்ரேயரின் தத்துவ தரிசனம்",
        "Creator Brahma, Bhagavan Narayana & Avadhuta Guru Dattatreya (Son of Atri & Anasuya)",
        "दत्तात्रेयं शिवं शान्तं इन्द्रनीलनिभं प्रभुम् । आत्ममायारतं देवमवधूतं दिगम्बरम् ॥",
        "தத்தாத்ரேயம் சிவம் சாந்தம் இந்த்ரநீலநிபம் ப்ரபும் | ஆத்மமாயாரதம் தேவம் அவதூதம் திகம்பரம் ||",
        "Meditate upon Dattatreya—auspicious, serene, sapphire-hued Lord, revelling in His own Self-bliss, the supreme Avadhuta beyond all dualities!",
        "மங்களமானவரும், சாந்த சொரூபியும், நீலமணி வண்ணரும், ஆத்மானந்தத்தில் திளைப்பவருமான அவதூத குரு தத்தாத்ரேயரைத் தியானிப்போம்!",
        "Realizing the non-dual Guru principle (Brahma-Vishnu-Shiva in one form) through the Dam-Ham Hamsa mantra and Avadhuta detachment.",
        "Sacred hermitage of Sage Atri and Sati Anasuya under an Audumbara (cluster-fig) tree where radiant Dattatreya sits smeared with sacred ash, radiating Vishnu's Kaustubha light",
        "In Satyaloka, Creator Brahma asked Bhagavan Narayana: 'O Lord! How can bound souls cross this perilous ocean of Samsara?'",
        "சத்தியலோகத்தில் பிரம்மதேவர் பகவான் நாராயணனிடம், 'பிரபுவே! கட்டுண்ட ஜீவன்கள் இப்பிறவிக்கடலைக் கடப்பது எவ்வாறு?' எனக் கேட்டார்.",
        "Lord Narayana answered: 'Meditate on My own Avadhuta manifestation—Dattatreya, born to Sage Atri and the pure Anasuya as the unified light of Trimurti!'",
        "நாராயணன் அருளினார்: 'அத்ரி முனிவருக்கும் அனசூயைக்கும் மும்மூர்த்திகளின் ஒருங்கிணைந்த ஒளியாக அவதரித்த தத்தாத்ரேயரைத் தியானியுங்கள்!'",
        "Sapphire-hued like Indranila gem, wearing a garland of forest flowers and sacred ash, Dattatreya delights eternally in the Atman alone.",
        "இந்திரநீல மணி போன்ற திருமேனியும், திருநீறும் வனமாலையும் அணிந்து, தத்தாத்ரேயர் எப்போதும் ஆத்மானந்தத்தில் திளைக்கிறார்.",
        "His single-syllable seed 'Dam' fused with 'Ham' forms the Hamsa-Datta breath mantra: 'I am That Supreme Self!'",
        "'தம்' எனும் பீஜமும் 'ஹம்' எனும் ஹம்ஸ மூச்சும் இணைந்து, 'நானே அந்தப் பரமாத்மா' எனும் மெய்ஞ்ஞானத்தை உணர்த்துகிறது.",
        "Chanting the eight-syllabled 'Dram Dattatreyaya Namah' and the thirty-two-syllabled Anushtubh, the seeker becomes an inner Avadhuta.",
        "'த்ராம் தத்தாத்ரேயாய நமஹ' எனும் அஷ்டாக்ஷர மந்திரத்தை உபாசிப்பவன், விருப்பு வெறுப்பற்ற அக அவதூத நிலையை அடைகிறான்.",
        "Even the sight of such a liberated Yogi purifies the three worlds and releases ancestors from bondage.",
        "அத்தகைய தத்தாத்ரேய யோகியின் தரிசனமே மூவுலகங்களையும் புனிதமாக்கி, பிறவித் தளையிலிருந்து விடுவிக்கிறது."
    ),
    make_vaishnava(
        "vaishnava_13_garuda", 102, "Garuda Upanishad", "गारुडोपनिषद्", "காருட உபநிஷதம்", "Atharva Veda",
        "The Golden Wings of Vainateya: Neutralizing the Poison of Samsara",
        "வைனதேய கருடனின் பொன் சிறகுகள்: சம்சார விஷத்தை அமிர்தமாக்கும் பிரம்ம வித்தை",
        "Creator Brahma, Devarishi Narada & Pakshiraja Bhagavan Garuda",
        "तत्पुरुषाय विद्महे सुवर्णपक्षाय धीमहि । तन्नो गरुडः प्रचोदयात् ॥",
        "தத்புருஷாய வித்மஹே ஸுவர்ணபக்ஷாய தீமஹி | தன்னோ கருட: ப்ரசோதயாத் ||",
        "We know That Supreme Person; we meditate upon the Golden-Winged One—may Lord Garuda impel our intellect toward liberation!",
        "அந்தப் பரம புருஷனை அறிகிறோம்; பொன் சிறகுகள் கொண்டவரைத் தியானிக்கிறோம்; பக்ஷிராஜனான கருடன் எம் புத்தியைத் தூண்டுவாராக!",
        "Invoking Pakshiraja Garuda—the living embodiment of the three Vedas—to destroy both physical venom and the inner poison of ego, anger, and samsara.",
        "Celestial sky above Mount Meru where Golden-Winged Garuda soars carrying Lord Vishnu, his wings chanting the Sama Veda and dispelling dark venomous clouds",
        "Devarishi Narada approached Creator Brahma and asked: 'Lord, teach me that supreme Garuda Brahma-Vidya which destroys all deadly poisons!'",
        "தேவரிஷி நாரதர் பிரம்மதேவரை அணுகி, 'பெருமானே! கொடிய விஷங்கள் அனைத்தையும் அழிக்கும் கருட பிரம்ம வித்தையை அருளுங்கள்!' எனக் கேட்டார்.",
        "Brahma declared: 'Taught by Mahavishnu to Garuda, this sacred lore neutralizes Takshaka, Karkotaka, and the inner venom of lust, wrath, and delusion!'",
        "பிரம்மதேவர் கூறினார்: 'மகாவிஷ்ணு கருடனுக்கு அருளிய இவ்வித்தை, நாக விஷத்தையும் காமம்-வெகுளி-மயக்கம் எனும் அக விஷத்தையும் அழிக்கும்!'",
        "Lord Garuda is none other than the Vedas personified: the Rik, Yajus, and Sama Vedas form his radiant golden feathers and wings!",
        "பக்ஷிராஜனான கருடன் வேதங்களின் திருவுருவமே; ரிக், யஜுர், சாம வேதங்களே அவரது ஒளிவீசும் பொன் சிறகுகளாகும்!",
        "Vamadeva constitutes his southern wing, Brihat-Sama his northern wing, and the Gayatri metre is his very life-breath.",
        "வாமதேவ சாமம் அவரது வலது சிறகாகவும், பிருஹத் சாமம் இடது சிறகாகவும், காயத்ரி சந்தமே அவரது பிராணனாகவும் திகழ்கின்றன.",
        "Uttering the Garuda Gayatri and the thunderbolt command 'Hata visham! Pranashtam visham!', the poison of ignorance turns to dust.",
        "கருட காயத்ரியையும் 'விஷம் அழிந்தது! அறியாமை நஞ்சு ஒழிந்தது!' எனும் மந்திரத்தையும் உச்சரிக்க, சம்சார நஞ்சு பொடியாகிறது.",
        "Riding upon the golden wings of Vedic wisdom, the fearless soul ascends straight to the immortal feet of Lord Vishnu.",
        "வேத ஞானம் எனும் கருடனின் பொன் சிறகுகளில் ஏறி, அச்சமற்ற ஆன்மா மகாவிஷ்ணுவின் திருவடிகளை அடைகிறது."
    ),
    make_vaishnava(
        "vaishnava_14_kalisantarana", 103, "Kali-Santarana Upanishad", "कलिसन्तरणोपनिषद्", "கலிஸந்தரண உபநிஷதம்", "Krishna Yajur Veda",
        "Narada's Question for the Dark Age: The Sixteen-Name Hare Rama Maha-Mantra",
        "கலியுக இருள் நீக்கும் தாரக மந்திரம்: நாரதருக்குப் பிரம்மா அருளிய பதினாறு திருநாமங்கள்",
        "Devarishi Narada & Creator Lord Brahma",
        "हरे राम हरे राम राम राम हरे हरे । हरे कृष्ण हरे कृष्ण कृष्ण कृष्ण हरे हरे ॥",
        "ஹரே ராம ஹரே ராம ராம ராம ஹரே ஹரே | ஹரே கிருஷ்ண ஹரே கிருஷ்ண கிருஷ்ண கிருஷ்ண ஹரே ஹரே ||",
        "Hare Rama Hare Rama, Rama Rama Hare Hare; Hare Krishna Hare Krishna, Krishna Krishna Hare Hare—these sixteen names destroy the sixteen sheaths of ignorance!",
        "ஹரே ராம ஹரே ராம ராம ராம ஹரே ஹரே | ஹரே கிருஷ்ண ஹரே கிருஷ்ண கிருஷ்ண கிருஷ்ண ஹரே ஹரே — இப்பதினாறு நாமங்களும் ஜீவனின் பதினாறு கலை ஆவரணங்களை நீக்குகின்றன!",
        "Crossing the spiritual darkness and turmoil of Kali Yuga through the simple, rule-free chanting of the 16-name, 32-syllable Maha-Mantra.",
        "Transition from the twilight of Dvapara Yuga into Kali Yuga, where a golden-lotus sound-mandala of the 16 Hare Rama Hare Krishna names parts the storm clouds",
        "At the close of Dvapara Yuga, Devarishi Narada asked his father Brahma: 'O Lord! How shall fragile mortals cross the terrible ocean of Kali Yuga?'",
        "துவாபர யுகத்தின் இறுதியில் நாரதர் பிரம்மதேவரிடம், 'பகவானே! வரப்போகும் கொடிய கலியுகக் கடலை எளிய மனிதர்கள் எவ்வாறு கடப்பார்கள்?' எனக் கேட்டார்.",
        "Brahma spoke with deep compassion: 'Simply by uttering the primordial sixteen-name Maha-Mantra of Bhagavan Narayana, one shakes off all stains of Kali!'",
        "பிரம்மதேவர் கருணையுடன் கூறினார்: 'ஆதி புருஷனான நாராயணனின் பதினாறு திருநாம மஹாமந்திரத்தை உச்சரிப்பதால் கலியின் தோஷங்கள் அனைத்தும் நீங்கும்!'",
        "The Jiva within the heart is veiled by sixteen Kalas (subtle sheaths of ignorance and vital modifications).",
        "மனித இதயத்தில் உறையும் ஜீவன், பதினாறு கலைகள் எனும் அறியாமைத் திரைகளால் (ஆவரணங்களால்) மறைக்கப்பட்டுள்ளான்.",
        "Each of the sixteen divine names—Hare, Rama, and Krishna—burns away one veil, until Parabrahman shines unobstructed like the midday sun!",
        "இப்பதினாறு திருநாமங்களும் பதினாறு அறியாமைத் திரைகளைக் கிழித்தெறிய, மேகம் நீங்கிய சூரியன் போல் பரப்பிரம்மம் உள்ளே பிரகாசிக்கிறது!",
        "Chanting this 32-syllable mantra requires no rigid ritual rules; whether in purity or transition, constant remembrance purifies the heart.",
        "முப்பத்திரண்டு எழுத்துக்கள் கொண்ட இம்மந்திரத்தை ஓதக் கடுமையான விதிகள் இல்லை; எந்நிலையிலும் நாம ஸ்மரணை இதயத்தைத் தூய்மையாக்கும்.",
        "Crossing the darkness of Kali Yuga effortlessly, the devotee attains the supreme liberation of Sayujya Moksha.",
        "கலியுக இருளை எளிதில் கடந்து, நாம சங்கீர்த்தனத்தால் சாதகன் பரம முக்தியை அடைகிறான்."
    ),
])


import json
import os


def render_vaishnava_markdown(u: dict) -> str:
    lines = [
        f"# {u['name_en']} ({u['name_sa']} | {u['name_ta']})",
        "",
        f"- **Catalog ID**: `{u['id']}`",
        f"- **Muktika Canon Number**: #{u['muktika_num']}",
        f"- **Veda**: {u['veda']}",
        f"- **Category**: {u['category']} Upanishad",
        f"- **Story Title (EN)**: {u['story_title_en']}",
        f"- **Story Title (TA)**: {u['story_title_ta']}",
        f"- **Primary Characters**: {u['characters']}",
        f"- **Core Philosophical Theme**: {u['theme']}",
        f"- **Visual Setting**: {u['visual_setting']}",
        "",
        "## Core Mahavakya / Sloka",
        f"- **Sanskrit**: `{u['sloka_sa']}`",
        f"- **Tamil Transliteration**: `{u['sloka_ta']}`",
        f"- **Meaning (EN)**: {u['sloka_meaning_en']}",
        f"- **Meaning (TA)**: {u['sloka_meaning_ta']}",
        "",
        "---",
        "",
        "## 7-Scene Master Video Production Screenplay",
        ""
    ]
    for s in u["scenes"]:
        lines.extend([
            f"### Scene {s['scene_num']}: {s['title']}",
            f"- **Camera & Cinematography**: {s['camera']}",
            f"- **Google Flow / Veo 8K Prompt**: `{s['flow_prompt']}`",
            f"- **Voiceover (English)**: {s['vo_en']}",
            f"- **Voiceover (Tamil)**: {s['vo_ta']}",
            f"- **Subtitle (.ass / .srt) Cue**: `{s['subtitle_cue']}`",
            f"- **Suno / Sound Design Cue**: {s['sound_cue']}",
            ""
        ])
    return "\n".join(lines)


def build_vaishnava_files():
    out_md_dir = "/home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/06_vaishnava_upanishads"
    out_json_path = "/home/shishyan/GitHub/GuruKulaDesam/data/upanishads/agent4_vaishnava.json"
    os.makedirs(out_md_dir, exist_ok=True)
    os.makedirs(os.path.dirname(out_json_path), exist_ok=True)

    for idx, item in enumerate(VAISHNAVA_LIST, start=1):
        fname = f"{idx:02d}_muktika_{item['muktika_num']:03d}_{item['id']}.md"
        fpath = os.path.join(out_md_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(render_vaishnava_markdown(item))

    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(VAISHNAVA_LIST, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(VAISHNAVA_LIST)} Vaishnava markdown files in {out_md_dir}")
    print(f"Generated JSON dataset at {out_json_path}")


if __name__ == "__main__":
    build_vaishnava_files()
