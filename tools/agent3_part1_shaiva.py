# -*- coding: utf-8 -*-
"""Agent 3 Part 1: 14 Shaiva Upanishads data module."""

def make_shaiva(uid, mnum, name_en, name_sa, name_ta, veda, story_en, story_ta,
                chars, sloka_sa, sloka_ta, mean_en, mean_ta, theme, setting,
                hook_en, hook_ta, dlg_en, dlg_ta, trial_en, trial_ta,
                rev_en, rev_ta, sadhana_en, sadhana_ta, close_en, close_ta):
    base_cam = [
        "Slow cinematic drone push-in through sacred temple pillars and glowing vibhuti mist",
        "Medium two-shot of seeker and sage beside a flickering homa fire under ancient banyan roots",
        "Dynamic tracking shot following the seeker's inner trial amidst cosmic Shiva-tandava lightning",
        "Extreme close-up on the sage's tranquil eyes opening as golden rudraksha beads illuminated",
        "Wide 360-degree orbital shot as the Jyotirlinga pillar of infinite light pierces the heavens",
        "Intimate macro shot of sacred ash (vibhuti) applied on the brow and glowing third-eye chakra",
        "Slow crane pull-back into the starry Kailasa night sky with a radiant golden Om emblem"
    ]
    titles = [
        "The Sacred Question at Kailasa's Foothills",
        "The Seeker Approaches the Master",
        "The Trial of Illusion and Bondage",
        "The Mahavakya of Shiva Consciousness",
        "The Cosmic Vision of Sadashiva",
        "Inner Sadhana: Vibhuti, Rudraksha & Panchakshara",
        "Eternal Liberation (Kaivalya Moksha)"
    ]
    cues = [
        "Deep Kailasa damaru pulse + resonant tanpura drone in C# + Temple bell",
        "Warm bamboo flute motif + crackling sacred fire ambiance",
        "Low sub-bass rumble + wind chimes + heartbeat rhythm",
        "Crystal singing bowl swell + celestial choir hum + Mridangam tap",
        "Full orchestral Veena & Nadaswaram crescendo + cosmic Om chant",
        "Gentle Himalayan stream + rhythmic breath-paced tanpura",
        "Fading temple conch (Shankha) + peaceful night crickets + sustained Om"
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
                f"Ultra-detailed 8K South Indian & Himalayan spiritual cinema, {setting}, "
                f"Scene {idx+1}: {titles[idx]}, featuring {chars}. Warm temple oil-lamp chiaroscuro, "
                f"sacred vibhuti particles glowing in volumetric golden sunbeams, authentic Shaiva iconography, "
                f"no text overlays, cinematic 16:9 composition."
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
        "category": "Shaiva",
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

SHAIVA_LIST = [
    make_shaiva(
        "shaiva_01_kaivalya", 12, "Kaivalya Upanishad", "कैवल्योपनिषद्", "கைவல்ய உபநிஷதம்", "Atharva Veda",
        "Ashvalayana & Brahma: The FireStick of Om and Supreme Aloneness",
        "ஆஸ்வலாயனரும் பிரம்மதேவரும்: ஓங்கார அரணியும் கைவல்ய மோட்சமும்",
        "Sage Ashvalayana & Creator Lord Brahma",
        "अचिन्त्यमव्यक्तमनन्तरूपं शिवं प्रशान्तममृतं ब्रह्मयोनिम् ।",
        "அசிந்த்யம் அவ்யக்தம் அனந்தரூபம் சிவம் பிரசாந்தம் அம்ருதம் பிரம்மயோனிம் |",
        "Unthinkable, unmanifest, of infinite forms, auspicious, peaceful, immortal source of Brahma is Shiva alone.",
        "சிந்தனைக்கு எட்டாத, வெளிப்படாத, முடிவற்ற வடிவங்கள் கொண்ட மங்களமான, அமைதியான அழிவற்ற சிவனே பரம்பொருள்.",
        "Making the heart the lower fire-stick and Om the upper fire-stick to ignite the flame of non-dual Shiva knowledge.",
        "Golden-lit Brahmaloka lotus sanctuary transitioning into an ancient Chidambaram-style forest hermitage",
        "Sage Ashvalayana bowed before Lord Brahma and asked for the supreme science of Brahman that instantly dissolves all karmic fetters.",
        "முனிவர் ஆஸ்வலாயனர் பிரம்மதேவரை வணங்கி, பிறவித் தளையை உடனே அறுக்கும் பிரம்ம வித்தையை உபதேசிக்குமாறு வேண்டினார்.",
        "Brahma instructed: combine Shraddha, Bhakti, and Dhyana Yoga—meditate within the lotus of the heart where three-eyed Nilakantha shines.",
        "சிரத்தை, பக்தி, தியான யோகம் ஆகிய மூன்றாலும் இதயத் தாமரையில் முக்கண் நீலகண்டனை தியானிக்க பிரம்மா வழிகாட்டினார்.",
        "Ashvalayana saw how the deluded Jiva identifies with waking, dream, and deep sleep bodies, forgetting its own sovereign bliss.",
        "விழிப்பு, கனவு, ஆழ்ந்த உறக்கம் ஆகிய மூன்று நிலைகளில் சிக்கித் தவிக்கும் ஜீவனின் மாயையை ஆஸ்வலாயனர் உணர்ந்தார்.",
        "Making his soul the lower Arani wood and Pranava Om the upper churning rod, he kindled the fire of Jnana and burned all bondage.",
        "தன் ஆன்மாவை கீழ் அரணியாகவும் ஓங்காரத்தை மேல் அரணியாகவும் கொண்டு ஞானத் தீயைக் கடைந்து பாசங்களை எரித்தார்.",
        "In that blaze, he realized: 'In me alone everything is born, exists, and dissolves—I am that non-dual Sadashiva!'",
        "'என்னிடத்திலேயே அனைத்தும் தோன்றி நிலைபெற்று ஒடுங்குகின்றன; அந்த இரண்டற்ற சதாசிவனே நான்!' என உணர்ந்தார்.",
        "Whoever recites this Kaivalya wisdom becomes pure as crystal, freed from rebirth into eternal Shiva-hood.",
        "இந்த கைவல்ய உபநிஷதத்தை உணர்பவர் பளிங்கு போல் தூய்மையாகி பிறவிப் பெருங்கடலைக் கடந்து சிவமயமாகிறார்."
    ),
    make_shaiva(
        "shaiva_02_atharvashiras", 22, "Atharvashiras Upanishad", "अथर्वशिरोपनिषद्", "அதர்வஸிரோபநிஷதம்", "Atharva Veda",
        "The Devas Search Mount Kailasa: Why Rudra Alone Is the One All-Pervading Lord",
        "கைலாயத்தில் தேவர்களின் தேடல்: உருத்திரனே ஏகப் பரம்பொருள்",
        "The Celestial Devas (Indra, Agni, Vayu) & Bhagavan Rudra",
        "एको रुद्रो न द्वितीयाय तस्थुः य इमांल्लोकानीशते ईशनीभिः ।",
        "ஏகோ ருத்ரோ ந த்விதீயாய தஸ்து: ய இமான் லோகான் ஈசதே ஈசனீபி: |",
        "Rudra is truly One; there is no second beside Him who rules all these worlds by His sovereign powers.",
        "உருத்திரன் ஒருவனே; இரண்டாவதாக எவருமில்லை. அவனே தன் ஈசத்துவ சக்தியால் உலகங்களை ஆள்கிறான்.",
        "Realizing that all gods, elements, prana, and cosmic directions are manifestations of the single Maheshvara.",
        "Snow-crowned Mount Kailasa illuminated by aurora-like cosmic Rudra-jyoti",
        "The Devas ascended to high heaven seeking to know who truly is Rudra, the mysterious Lord behind creation.",
        "தேவர்கள் சுவர்க்க லோகத்தைக் கடந்து, படைப்பின் பின்னணியில் உள்ள உருத்திரன் யார் என அறியச் சென்றனர்.",
        "When they beheld Bhagavan Rudra, He vanished from outer sight and spoke from the inner space of consciousness.",
        "பகவான் உருத்திரனை தரிசித்த கணமே அவர் மறைந்து, அவர்களின் அக ஆகாயத்திலிருந்து ஒலிக்கத் தொடங்கினார்.",
        "Rudra declared: 'I alone existed before the worlds, I exist now, and I shall exist hereafter—nothing stands outside Me.'",
        "'ஆதியிலும் நானே இருந்தேன், இப்போதும் நானே இருக்கிறேன், இனிமேலும் நானே இருப்பேன்' என உருத்திரன் முழங்கினார்.",
        "The Devas praised Him in awe: He Who is Brahma, Vishnu, Skanda, Indra, Agni, Sun, Moon, and supreme Pranava.",
        "அவரே பிரம்மா, விஷ்ணு, முருகன், இந்திரன், அக்னி, சூரியன், சந்திரன் மற்றும் பிரணவம் என தேவர்கள் போற்றினர்.",
        "They beheld the sacred Pasha-vimochana fire where internalizing Rudra removes the cattle-rope of ignorance.",
        "அறியாமை எனும் பாசக் கயிற்றை அறுக்கும் பசுபதி ஞானத் தீயை தேவர்கள் தரிசித்தனர்.",
        "Resting in that Oneness, every seeker who knows Rudra inside the heart attains supreme peace.",
        "இதயக் குகையில் உறையும் உருத்திரனை ஒருவனாக உணரும் சாதகன் பரம சாந்தியை அடைகிறான்."
    ),
    make_shaiva(
        "shaiva_03_atharvashikha", 23, "Atharvashikha Upanishad", "अथर्वशिखोपनिषद्", "அதர்வஸிகோபநிஷதம்", "Atharva Veda",
        "Sage Atharvan's Fourfold Resonance of Om Ending in Shiva-Shanta",
        "அதர்வா முனிவரின் ஓங்கார ரகசியம்: சிவ-சாந்த துரிய நிலை",
        "Sage Atharvan, Pippalada, Sanatkumara & Angiras",
        "शिव एव केवलोऽहं ध्यायेत् । ओंकारो हि सर्वं व्याप्य तिष्ठति ।",
        "சிவ ஏவ கேவலோஹம் த்யாயேத் | ஓங்காரோ ஹி சர்வம் வ்யாப்ய திஷ்டதி |",
        "Meditate only on 'I am Shiva the Auspicious One', for Omkara pervades and uplifts all existence.",
        "மங்களமான சிவனே நான் என தியானிக்க வேண்டும்; ஓங்காரமே பிரபஞ்சம் முழுவதையும் வியாபித்து நிற்கிறது.",
        "The four matras of Pranava (A, U, M, and the half-matra Ardhamatra) culminating in Shiva-Nirvana.",
        "Sacred acoustic mandapa carved in black granite where sound waves become visible golden mandalas",
        "Pippalada, Angiras, and Sanatkumara approached Sage Atharvan asking: What meditation yields the highest fruit instantly?",
        "பிப்பலாதர், அங்கிரஸ், சனத்குமாரர் ஆகியோர் அதர்வா முனிவரிடம் உயர்ந்த தியானம் எது எனக் கேட்டனர்.",
        "Atharvan answered cleanly: 'Meditate on Omkara alone! For Omkara is the supreme Parabrahman.'",
        "அதர்வா முனிவர் தெளிவாகக் கூறினார்: 'ஓங்காரத்தையே தியானியுங்கள்! அதுவே பரப்பிரம்மம்.'",
        "He unfolded the four quarters: 'A' is earth and Rigveda; 'U' is atmosphere and Yajurveda; 'M' is heaven and Samaveda.",
        "அகரம் பூமியும் ரிக் வேதமும்; உகரம் அந்தரिक्षமும் யஜுர் வேதமும்; மகரம் விண்ணும் சாம வேதமும் ஆகும்.",
        "Beyond the three syllables shines the fourth—the subtle Ardhamatra resonance that ascends straight into Shiva.",
        "மூன்று மாத்திரைகளையும் கடந்த அர்த்தமாத்திரை நாதமே அனைத்து பாவங்களையும் போக்கும் சிவ தத்துவம்.",
        "Brahma, Vishnu, and Rudra shine inside the syllable, yet Maheshvara Shiva is the peaceful Fourth (Turiya) Who liberates.",
        "மும்மூர்த்திகளையும் கடந்து நான்காம் துரிய நிலையில் சாந்த சிவனே மோட்சம் அளிக்கிறார்.",
        "Chanting Om with awareness of Shiva-Shanta dissolves the mind into boundless auspicious light.",
        "சிவ-சாந்த பாவனையுடன் ஓங்காரத்தை உச்சரிப்பவன் எல்லையற்ற அருட்பெருஞ்ஜோதியில் கலக்கிறான்."
    ),
    make_shaiva(
        "shaiva_04_brihajjabala", 26, "Brihajjabala Upanishad", "बृहज्जाबालोपनिषद्", "பிருஹஜ்ஜாபால உபநிஷதம்", "Atharva Veda",
        "Bhusunda & Kalagnirudra: The Alchemy of Sacred Vibhuti and Tripundra",
        "புசுண்ட முனிவரும் காளாக்னி உருத்திரரும்: திருநீற்றின் பெருமை",
        "Crow-Sage Bhusunda (Jabala lineage) & Lord Kalagnirudra",
        "भस्मनाङ्गानि संस्पृश्य त्रिपुण्ड्रं धारयेद्बुधः ।",
        "பஸ்மனாங்கானி சம்ஸ்ப்ருஶ்ய த்ரிபுண்ட்ரம் தாரயேத் புத: |",
        "Touching the limbs with sacred ash and wearing the three horizontal lines of Tripundra, the wise awaken to Shiva.",
        "திருநீற்றால் திருமேனியைத் தீண்டி திரிபுண்டரம் அணியும் ஞானி சிவ தத்துவத்தில் விழிப்படைகிறான்.",
        "Sacred Vibhuti as the primordial fire-essence of the universe that burns away threefold Mala (impurity).",
        "Sacred homa-kunda glowing at dawn beside a crystal river with golden-white Vibhuti rising like stardust",
        "Immortal Sage Bhusunda approached Lord Kalagnirudra to learn the eternal secret of Vibhuti-snana (the bath of sacred ash).",
        "புசுண்ட முனிவர் காளாக்னி உருத்திரரை அணுகி, திருநீற்று ஸ்நானத்தின் சनातन ரகசியத்தைக் கேட்டார்.",
        "Kalagnirudra revealed that when the five elements are reduced to their purest essence by Agni and Soma, sacred Bhasma remains.",
        "அக்னியும் சோமனும் இணைந்து பஞ்ச பூதங்களின் சாரமாகத் திகழ்வதே புனித விபூதி என உருத்திரர் விளக்கினார்.",
        "Bhusunda witnessed how water cleanses only the outer skin, whereas Agni-born Vibhuti purifies subtle karmic impressions.",
        "நீர் உடலை மட்டுமே தூய்மையாக்கும்; ஆனால் அக்னி மயமான திருநீறோ கர்ம வாசனைகளையே சுட்டெரிக்கும்.",
        "The five types of ash—Vibhuti, Bhasita, Bhasma, Kshara, and Raksha—correspond to the five faces of Sadashiva.",
        "விபூதி, பசிதம், பஸ்மம், க்ஷாரம், ரக்ஷை ஆகிய ஐந்தும் சதாசிவனின் ஐந்து திருமுகங்களின் அருட்சக்திகள்.",
        "Applying the three lines of Tripundra across the forehead balances Ida, Pingala, and opens the Sushumna third eye.",
        "நெற்றியில் இடும் மூன்று கோடுகள் இடகலை, பிங்கலையைச் சமப்படுத்தி சுழுமுனை ஞானக்கண்ணைத் திறக்கின்றன.",
        "Adorned in sacred ash and chanting Sri Rudram, the seeker walks the earth as a living temple of Shiva.",
        "திருநீறு அணிந்து ஸ்ரீ ருத்ரம் ஜபிக்கும் சாதகன் நடமாடும் சிவாலயமாகவே திகழ்கிறான்."
    ),
    make_shaiva(
        "shaiva_05_kalagnirudra", 28, "Kalagnirudra Upanishad", "कालाग्निरुद्रोपनिषद्", "காளாக்னி ருத்ர உபநிஷதம்", "Krishna Yajur Veda",
        "Sanatkumara Learns the Cosmic Secret of the Three Sacred Lines (Tripundra)",
        "சனத்குமாரருக்கு காளாக்னி உருத்திரர் அருளிய திரிபுண்டர தத்துவம்",
        "Sage Sanatkumara & Bhagavan Kalagnirudra",
        "रेखात्रयेण संवेष्ट्य ललाटे तु त्रिपुण्ड्रकम् ।",
        "ரேகாத்ரயேண சம்வேஷ்ட்ய லலாடே து த்ரிபுண்ட்ரகம் |",
        "Drawing the three sacred lines of Tripundra across the brow, one encompasses all triad realities in Shiva.",
        "புருவங்களுக்கு இடையே மூன்று திருநீற்றுக் கோடுகளை அணிபவன் மூவுலக தத்துவங்களையும் சிவனுக்குள் காண்கிறான்.",
        "Each of the three lines of Tripundra embodies a sacred triad: A-U-M, three Gunas, three worlds, three fires, and three Shaktis.",
        "Celestial hall of fire and light where three glowing horizontal beams of white radiance converge on the third eye",
        "Radiant Sanatkumara bowed to Lord Kalagnirudra asking: 'Lord, tell me the complete mystery and method of Tripundra.'",
        "சனத்குமாரர் காளாக்னி உருத்திரரைப் பணிந்து, 'இறைவா! திரிபுண்டரத்தின் முழுமையான விதியையும் தத்துவத்தையும் கூறுங்கள்' என்றார்.",
        "Kalagnirudra smiled: from eyebrow to eyebrow, draw three horizontal lines using sacred ash consecrated by Panchabrahma mantras.",
        "'சத்யோஜாதம் முதலான பஞ்சபிரம்ம மந்திரங்களால் திருநீற்றை எடுத்து புருவ இடைவெளியில் முக்கோடு இடுக' என்றார் ஈசன்.",
        "The first line is Garhapatya fire, the syllable 'A', Rajas, the physical body, Kriya Shakti, and Maheshvara.",
        "முதல் கோடு கார்ஹபத்ய அக்னி, அகரம், ரஜோ குணம், தூல சரீரம், கிரியா சக்தி மற்றும் மகேஸ்வரனைக் குறிக்கும்.",
        "The second line is Dakshinagni, the syllable 'U', Sattva, the subtle body, Iccha Shakti, and Sadashiva.",
        "இரண்டாம் கோடு தக்ஷிணாக்னி, உகரம், சத்வ குணம், சூக்கும சரீரம், இச்சா சக்தி மற்றும் சதாசிவனைக் குறிக்கும்.",
        "The third line is Ahavaniya fire, the syllable 'M', Tamas, the causal body, Jnana Shakti, and Parashiva.",
        "மூன்றாம் கோடு ஆகவனீய அக்னி, மகரம், தமோ குணம், காரண சரீரம், ஞான சக்தி மற்றும் பரசிவனைக் குறிக்கும்.",
        "He who wears this Tripundra with inner contemplation transcends the three states of time and attains Shiva-sayujya.",
        "இந்த முக்கோட்டின் தத்துவத்தை உணர்ந்து தரிப்பவர் முக்காலங்களையும் கடந்து சிவ சாயுஜ்யம் அடைகிறார்."
    ),
    make_shaiva(
        "shaiva_06_dakshinamurti", 45, "Dakshinamurti Upanishad", "दक्षिणामूर्त्युपनिषद्", "தக்ஷிணாமூர்த்தி உபநிஷதம்", "Krishna Yajur Veda",
        "Markandeya Under the Banyan Tree: The Silent Guru's Chinmudra",
        "மார்க்கண்டேயரும் ஆலமர் செல்வனும்: மௌன குருவின் சின்முத்திரை",
        "Long-lived Sage Markandeya, Shaunaka & Lord Medha Dakshinamurti",
        "मौनव्याख्याप्रकटितपरब्रह्मतत्त्वं युवानं वर्षिष्ठान्तेवसदृषिगणैरावृतं ब्रह्मनिष्ठैः ।",
        "மௌன வ்யாக்யா ப்ரகடித பரப்ரஹ்ம தத்வம் யுவானம் வர்ஷிஷ்டாந்தே வசத் ரிஷிகணை: ஆவ்ருதம் |",
        "Youthful Guru Dakshinamurti reveals the supreme Brahman through silent exposition to aged sages seated around Him.",
        "முதிய முனிவர்கள் சூழ்ந்திருக்க, இளமையான குரு தக்ஷிணாமூர்த்தி மௌன உபதேசத்தாலேயே பரப்பிரம்ம தத்துவத்தை உணர்த்துகிறார்.",
        "Supreme Jnana transmitted beyond spoken words through Chinmudra under the cosmic Vata-vriksha (banyan tree).",
        "Ancient sprawling banyan tree (Kallal tree) bathed in silver moonlight with youthful Dakshinamurti facing south",
        "In the Naimisha forest, Shaunaka asked long-lived Markandeya: 'By what secret knowledge do you remain eternally youthful and fearless of death?'",
        "நைமிசாரண்யத்தில் சௌனகர் மார்க்கண்டேயரிடம், 'மரண பயமின்றி என்றும் பதினாறு வயதுடன் திகழும் உமது ரகசியம் என்ன?' எனக் கேட்டார்.",
        "Markandeya revealed the secret of Shiva-Tattva-Sudha—meditating on the south-facing Guru, Lord Medha Dakshinamurti.",
        "தென்முகக் கடவுளான மேதா தக்ஷிணாமூர்த்தியின் சிவ-தத்துவ அமுத ரகசியத்தையே மார்க்கண்டேயர் வெளியிட்டார்.",
        "Aged rishis exhausted by endless scriptures sat beneath the banyan tree, their minds restless with unanswered doubts.",
        "சாஸ்திரங்களைப் படித்தும் ஐயம் தீராத முதிய முனிவர்கள் ஆலமரத்தடியில் அமைதியின்றி அமர்ந்திருந்தனர்.",
        "Youthful Dakshinamurti lifted His hand in Chinmudra—thumb and index joined, three fingers extended—and smiled in absolute silence.",
        "இளமையான தக்ஷிணாமூர்த்தி சின்முத்திரை காட்டிப் புன்னகைத்தபடி பரிபூரண மௌனத்தில் ஆழ்ந்தார்.",
        "In that luminous silence, every doubt vanished: the Jiva bowed to Ishvara, leaving behind ego, karma, and maya.",
        "அந்த மௌனப் பேரொளியில் முனிவர்களின் ஐயங்கள் அனைத்தும் விலகின; ஆணவம், கன்மம், மாயை மூன்றும் அகன்றன.",
        "Igniting the lamp of Atma-jnana within, the seeker becomes immortal like Markandeya, resting in pure awareness.",
        "அகத்தில் ஆத்ம தீபத்தை ஏற்றும் சாதகன் மார்க்கண்டேயரைப் போல் மரணமில்லாப் பெருவாழ்வு பெறுகிறான்."
    ),
    make_shaiva(
        "shaiva_07_sharabha", 50, "Sharabha Upanishad", "शरभोपनिषद्", "சரப உபநிஷதம்", "Atharva Veda",
        "Paippalada & Brahma: The Cosmic Winged Sharabha Who Calms Fierce Fury",
        "பைப்பலாதரும் பிரம்மாவும்: உக்கிரம் தணித்த சரபேஸ்வரப் பெருமான்",
        "Sage Paippalada, Lord Brahma, Narasimha & Lord Sharabheshvara",
        "यो वै महादेवो महाग्रासो महाशरभः सर्वभूतान्तरात्मा ।",
        "யோ வை மஹாதேவோ மஹாக்ராஸோ மஹாஶரப: ஸர்வபூதாந்தராத்மா |",
        "Mahadeva, appearing as the transcendent Sharabha, is the indwelling Self of all beings who absorbs all cosmic energies into peace.",
        "மகாதேவனே மகா சரபப் பறவையாகத் தோன்றி சகல உயிர்களின் அந்தராத்மாவாக உக்கிர சக்திகளை சாந்தப்படுத்துகிறார்.",
        "Transcending even fierce protective avatars into the supreme peaceful ground of Parameshvara.",
        "Dramatic celestial sky where golden-crimson fire meets cool sapphire-white Shiva radiance, winged lion-bird Sharabha soaring",
        "Paippalada asked Lord Brahma: 'Among all manifestations of divinity, who is the supreme shelter beyond cosmic turbulence?'",
        "பைப்பலாத முனிவர் பிரம்மதேவரிடம், 'பிரபஞ்சச் சீற்றங்களையெல்லாம் கடந்து நிற்கும் பரம புகலிடம் எது?' எனக் கேட்டார்.",
        "Brahma narrated how after slaying Hiranyakashipu, the fierce cosmic heat of Narasimha's protective wrath shook the worlds.",
        "இரணியனை வதம் செய்த பின் உலகைக் காக்கும் நரசிம்மரின் உக்கிர வெப்பத்தால் அண்டங்கள் நடுங்கிய வரலாற்றை பிரம்மா கூறினார்.",
        "To restore cosmic equilibrium, Mahesha assumed the wondrous form of Sharabha—with golden wings, lion claws, and cool moonlit grace.",
        "உலகச் சமநிலையை மீட்க மகேஸ்வரன் பொன் இறக்கைகளும் சிம்மப் பாதங்களும் கொண்ட சரபேஸ்வரராகத் தோன்றினார்.",
        "Sharabha embraced the fierce energy with boundless compassion, calming the blaze back into serene Vishnu-Shiva harmony.",
        "சரபேஸ்வரர் தன் கருணைச் சிறகுகளால் அந்த உக்கிரத்தைத் தணித்து, ஹரி-ஹர ஒற்றுமையின் சாந்தியை நிலைநாட்டினார்.",
        "Brahma declared: 'Vishnu and Rudra are one essence; Sharabha is the Turiya consciousness that dissolves all duality and fear.'",
        "'விஷ்ணுவும் உருத்திரனும் ஒன்றே; இருமைகளையும் அச்சத்தையும் நீக்கும் துரிய அறிவே சரபம்' என பிரம்மா அருளினார்.",
        "Whoever meditates on Sharabheshvara in the heart overcomes anger, fear, and obstacle, resting in fearless bliss.",
        "சரபேஸ்வரரை இதயத்தில் தியானிப்பவர் கோபம், அச்சம், தடைகள் நீங்கி அபய ஆனந்தத்தில் நிலைபெறுகிறார்."
    )
]

SHAIVA_LIST.extend([
    make_shaiva(
        "shaiva_08_akshamalika", 67, "Akshamalika Upanishad", "अक्षमालिकोपनिषद्", "அக்ஷமாலிகா உபநிஷதம்", "Rig Veda",
        "Prajapati & Guha (Murugan): The 50-Bead Rosary of the Sanskrit Alphabet",
        "பிரஜாபதியும் குகப் பெருமானும்: அக்ஷர மாலையின் ஐம்பது எழுத்து ரகசியம்",
        "Lord Prajapati & Commander Lord Guha (Kartikeya / Murugan)",
        "अकारादिक्षकारान्ताः पञ्चाशद्वर्णाः साक्षाच्छिवरूपाः ।",
        "அகாராதி க்ஷகாராந்தா: பஞ்சாஶத் வர்ணா: ஸாக்ஷாத் சிவரூபா: |",
        "From 'A' to 'Ksha', the fifty sacred letters threaded on the rosary are directly the living forms of Shiva and Shakti.",
        "'அ' முதல் 'க்ஷ' வரையிலான ஐம்பது மாத்ருகா எழுத்துக்களும் ஜபமாலையில் நேரடி சிவ-சக்தி வடிவங்களாகும்.",
        "Transforming the prayer rosary (Japa Mala) into the cosmic necklace of Matrika-Shakti and Meru consciousness.",
        "Sacred Murugan shrine in the hills where a glowing Rudraksha-crystal rosary floats in golden light above a lotus",
        "Prajapati bowed to Lord Guha (Subrahmanya), asking: 'O Skanda! Explain the mystery of the Akshamala rosary used by yogis.'",
        "பிரஜாபதி முருகப்பெருமானைப் பணிந்து, 'குகா! யோகிகள் கைக்கொள்ளும் ஜபமாலையின் ரகசியத்தை அருளுங்கள்' எனக் கேட்டார்.",
        "Guha explained: crystal, lotus seed, rudraksha, pearl, coral, and gold form the beads, threaded on the inner Sushumna cord.",
        "படிகம், தாமரை மணி, ருத்ராட்சம், முத்து, பவளம் ஆகிய மணிகளை சுழுமுனை எனும் உட்கயிற்றில் கோர்க்க வேண்டும் என்றார் குகன்.",
        "He consecrated each bead with the 50 Matrika letters from 'A' to 'La', awakening the sleeping mantric power inside speech.",
        "அகரம் முதல் ளகரம் வரையிலான ஐம்பது மாத்ருகா அக்ஷரங்களால் ஒவ்வொரு மணியையும் உயிர்ப்பிக்கும் முறையைக் காட்டினார்.",
        "The central summit bead—Meru—is annotated with 'Ksha', representing the unmoving Witness Sadashiva Whom one never crosses.",
        "மாலையின் நடுநாயகமான மேரு மணி 'க்ஷ' எனும் அக்ஷரமாகி, கடக்கக்கூடாத சாட்சி சதாசிவனாகத் திகழ்கிறது.",
        "Every rotation of the rosary aligns breath, syllable, and mind with the cosmic orbit of sun, moon, and stars.",
        "மாலையின் ஒவ்வொரு சுழற்சியும் மூச்சு, எழுத்து, மனம் ஆகியவற்றை சூரிய சந்திர கதியோடு இணைக்கிறது.",
        "He who chants with an awakened Akshamala purifies all speech and attains instant union with Shiva-Jnana.",
        "உயிர்ப்பிக்கப்பட்ட ஜபமாலையால் தியானிப்பவர் வாக்குத் தூய்மை பெற்று சிவஞானப் பெருவெளியில் கலக்கிறார்."
    ),
    make_shaiva(
        "shaiva_09_rudrahridaya", 85, "Rudrahridaya Upanishad", "रुद्रहृदयोपनिषद्", "ருத்ரஹ்ருதய உபநிஷதம்", "Krishna Yajur Veda",
        "Shuka & Vyasa: Uma Is Vishnu, and the Heart of Rudra Is Non-Dual Love",
        "சுகரும் வியாசரும்: உமையே விஷ்ணு, உருத்திரனின் இதயமே அद्वैதப் பேரன்பு",
        "Young Sage Shuka & Maharshi Veda Vyasa",
        "रुद्रो नर उमा नारी तस्मै तस्यै नमो नमः । रुद्रो ब्रह्मा उमा वाणी ।",
        "ருத்ரோ நர உமா நாரீ தஸ்மை தஸ்யை நமோ நம: | ருத்ரோ ப்ரஹ்மா உமா வாணீ |",
        "Rudra is the conscious Purusha and Uma is Prakriti; Rudra is Brahma and Uma is Sarasvati; salutations to Them Both!",
        "உருத்திரனே புருஷன், உமையே பிரகிருதி; உருத்திரனே பிரம்மா, உமையே சரஸ்வதி; இருவருக்கும் நமஸ்காரம்!",
        "The supreme non-difference of Shiva, Uma, and Vishnu within the sacred lotus of the heart.",
        "Himalayan Badarikashrama hermitage where Ardhanarishvara and Hari-Hara visions merge into a single golden sun",
        "Young Shuka asked his father Veda Vyasa: 'Who is the one Deva inside whom all Devas exist, and who gives liberation?'",
        "இளம் சுகர் தந்தை வியாசரிடம், 'எல்லாத் தேவர்களும் எவருக்குள் அடக்கம்? முக்தி தரும் அந்த ஏக இறைவன் யார்?' எனக் கேட்டார்.",
        "Vyasa sat beneath the Himalayan pines and revealed the secret Heart of Rudra—where all apparent dualities melt away.",
        "இமயமலை देवदारु மரத்தடியில் அமர்ந்த வியாசர், இருமைகள் அனைத்தும் கரையும் 'ருத்ர ஹ்ருதய' ரகசியத்தை உரைத்தார்.",
        "Shuka beheld the cosmic vision: Uma herself is Sri Vishnu, the shining Moon is Govinda, and Maheshvara is the inner Witness.",
        "உமையவளே மகாவிஷ்ணு! குளிர் நிலவே கோவிந்தன்! மகேஸ்வரனே அகச் சாட்சி எனும் அற்புதக் காட்சியை சுகர் கண்டார்.",
        "Every masculine form in the cosmos is Lord Rudra; every feminine power, grace, and melody is Goddess Uma.",
        "உலகின் ஆண் வடிவங்கள் அனைத்தும் உருத்திரன்; பெண் வடிவங்களும் கருணையும் உமாதேவியே ஆகும்.",
        "Just as watering the root of a great tree nourishes every branch and leaf, worshipping Rudra nourishes the entire universe.",
        "மரத்தின் வேருக்கு நீர் ஊற்றினால் கிளைகள் அனைத்தும் செழிப்பது போல், உருத்திர ஆராதனை பிரபஞ்சத்தையே மகிழ்விக்கிறது.",
        "Realizing the indivisible unity of Shiva, Shakti, and Hari as one's own Atman, Shuka entered supreme peace.",
        "சிவம், சக்தி, ஹரி ஆகிய மூன்றும் தன் ஆன்மாவே என உணர்ந்த சுகர் பரம சாந்தியில் ஆழ்ந்தார்."
    ),
    make_shaiva(
        "shaiva_10_bhasmajabala", 87, "Bhasmajabala Upanishad", "भस्मजाबालोपनिषद्", "பஸ்மஜாபால உபநிஷதம்", "Atharva Veda",
        "Jabala & Bhusunda in Kashi: Living and Dying in the Radiance of Sacred Ash",
        "காசியில் ஜாபால முனிவர்: திருநீறும் அவிமுக்த க்ஷேத்திரத்தின் முக்தி நெறியும்",
        "Sage Jabala Bhusunda & Lord Somaskanda Shiva at Kashi",
        "शिव एव गुरुः शिव एव वेदः शिव एव प्रभुः शिव एव अहम् ।",
        "சிவ ஏவ குரு: சிவ ஏவ வேத: சிவ ஏவ ப்ரபு: சிவ ஏவ அஹம் |",
        "Shiva alone is the Guru, Shiva alone is the Veda, Shiva alone is the Lord, and I myself am Shiva!",
        "சிவனே குரு, சிவனே வேதம், சிவனே தலைவன், அந்தச் சிவனே நான்!",
        "Daily consecration with Bhasma and dwelling in Kashi (the inner brow-center between Varana and Asi) for instant liberation.",
        "Dawn over Manikarnika and Panchaganga ghats of ancient Kashi glowing with golden temple spires and Rudra-jyoti",
        "Jabala Bhusunda climbed Mount Kailasa where Shiva sits with Uma and Skanda, asking for the direct dharma of liberation.",
        "ஜாபால புசுண்டர் கைலாயத்தில் சோமாஸ்கந்த மூர்த்தியாக வீற்றிருக்கும் சிவபெருமானிடம் நேர் முக்தி நெறியைக் கேட்டார்.",
        "Shiva taught the sacred rule of Tripundra from dawn till dusk, wearing Bhasma mixed with mantra water across 16 body centers.",
        "வைகறை முதல் அந்தி வரை மந்திர நீரால் குழைத்த திருநீற்றை உடலின் பதினாறு இடங்களில் தரிக்கும் விதியை ஈசன் அருளினார்.",
        "Even if one cannot perform complex yajnas, a single sincere application of Vibhuti with 'Tryambakam Yajamahe' burns mountains of sin.",
        "பெரிய யாகங்கள் செய்ய இயலாவிட்டாலும், 'த்ரயம்பகம் யஜாமஹே' எனத் திருநீறு அணிந்தாலே பாவ மலைகள் சாம்பலாகும்.",
        "Shiva then pointed to Kashi—Avimukta, the city never forsaken by Him—where Vishveshvara whispers the Taraka mantra.",
        "தான் என்றும் பிரியாத காசி எனும் அவிமுக்த தலத்தில் விஸ்வநாதர் தாரக மந்திரம் உபதேசிக்கும் ரகசியத்தைக் காட்டினார்.",
        "Internally, Kashi is the radiant Ajna space between the eyebrows, where the soul's dual currents merge into light.",
        "அகத்தில் புருவ மத்தியில் ஒளிரும் ஆக்ஞா சக்கரமே உண்மையான காசி க்ஷேத்திரம் என்பதை முனிவர் உணர்ந்தார்.",
        "Declaring 'Shivo'ham—I am Shiva alone!', the seeker abides in fearless immortality here and now.",
        "'சிவோஹம்—நானே சிவன்!' எனும் பேரறிவில் நிலைபெறும் சாதகன் இங்கேயே அமரத்துவம் எய்துகிறான்."
    ),
    make_shaiva(
        "shaiva_11_rudrakshajabala", 88, "Rudrakshajabala Upanishad", "रुद्राक्षजाबालोपनिषद्", "ருத்ராக்ஷஜாபால உபநிஷதம்", "Sama Veda",
        "Tears of Compassion: How Kalagnirudra's Eyes Birthed the Sacred Rudraksha",
        "கருணைக் கண்ணீர் துளிகள்: காளாக்னி உருத்திரரின் விழிகளில் உதித்த ருத்ராட்சம்",
        "Sage Bhusunda & Bhagavan Kalagnirudra",
        "त्रिपुरवधार्थं उन्मीलिताक्षस्य रुद्रस्य अश्रुबिन्दवः रुद्राक्षाः अभवन् ।",
        "த்ரிபுரவதார்த்தம் உன்மீலிதாக்ஷஸ்ய ருத்ரஸ்ய அஸ்ருபிந்தவ: ருத்ராக்ஷா: அபவன் |",
        "When Rudra opened His eyes after contemplation to liberate the three cities (Tripura), drops of compassionate tears became Rudraksha trees.",
        "திரிபுர சம்ஹாரத்தின் போது ஈசன் தன் விழிகளைத் திறந்தபோது வழிந்த கருணைக் கண்ணீர்த் துளிகளே ருத்ராட்ச மரங்களாயின.",
        "The sacred science of 1-to-14 Mukhi (faced) Rudraksha beads as living conduits of Shiva's grace.",
        "Ancient Himalayan forest where crystalline teardrops of light fall from Shiva's third eye and sprout into sacred Rudraksha trees",
        "Bhusunda asked Lord Kalagnirudra: 'How did Rudraksha beads originate, and what power do their different faces hold?'",
        "புசுண்ட முனிவர் காளாக்னி உருத்திரரிடம், 'ருத்ராட்ச மணிகள் எவ்வாறு தோன்றின? அதன் முகங்களின் மகிமை என்ன?' எனக் கேட்டார்.",
        "Kalagnirudra recalled the cosmic yoga of Tripura-samhara: for a thousand celestial years He held His eyes in deep stillness.",
        "திரிபுரங்களை எரிக்க ஆயிரம் தேவ ஆண்டுகள் ஈசன் கண் சிமிட்டாமல் யோகத்தில் ஆழ்ந்த வரலாற்றைக் கூறினார்.",
        "When His eyes opened in compassion for all beings, warm teardrops fell upon the earth and blossomed into Rudraksha trees.",
        "உயிர்களின் மேல் கொண்ட கருணையால் ஈசன் கண் திறந்தபோது விழுந்த கண்ணீர்த் துளிகளே பூமியில் ருத்ராட்ச விருட்சங்களாயின.",
        "The One-faced (Eka-mukhi) Rudraksha is Parashiva Himself; Five-faced is Sadashiva; Eleven-faced is the Eleven Rudras.",
        "ஒரு முக ருத்ராட்சம் பரசிவன்; ஐந்து முகம் சதாசிவன்; பதினொரு முகம் ஏகாதச உருத்திரர்களின் வடிவம்.",
        "Wearing Rudraksha on the crown, ears, neck, and wrists shields the aura and awakens kundalini toward Sahasrara.",
        "சிரசு, செவி, கண்டம், மணிக்கட்டில் ருத்ராட்சம் அணிவது பிராண கவசமாகி குண்டலினியை சஹஸ்ராரத்திற்கு உயர்த்துகிறது.",
        "Even beholding or touching a true Rudraksha with devotion bestows the merit of a million charities and leads to Rudra-loka.",
        "பக்தியுடன் ருத்ராட்சத்தைத் தரிசிப்பதும் அணிவதும் கோடி புண்ணியங்களைத் தந்து சிவலோகப் பேற்றை அளிக்கிறது."
    ),
    make_shaiva(
        "shaiva_12_ganapati", 89, "Ganapati Upanishad (Atharvashirsha)", "गणपत्युपनिषद्", "கணபதி உபநிஷதம் (அதர்வஸீர்ஷம்)", "Atharva Veda",
        "Sage Ganaka's Vision: Ganapati as the Primordial Sound 'Gam' and Supreme Brahman",
        "கணக ரிஷியின் தரிசனம்: 'கம்' எனும் மூல ஒலியாகத் திகழும் மகா கணபதி",
        "Rishi Ganaka & Supreme Lord Maha Ganapati",
        "त्वं मूलाधारस्थितोऽसि नित्यम् । त्वं शक्तित्रयात्मकः । त्वं ब्रह्मा त्वं विष्णुस्त्वं रुद्रः ।",
        "த்வம் மூலாதார ஸ்திதோஸி நித்யம் | த்வம் சக்தி த்ரயாத்மக: | த்வம் ப்ரஹ்மா த்வம் விஷ்ணுஸ்த்வம் ருத்ர: |",
        "Thou eternally abidest in the Muladhara chakra; Thou art the three Shaktis; Thou art Brahma, Vishnu, Rudra, and the supreme Om!",
        "நீயே மூலாதாரத்தில் நித்தியமாக உறைபவன்; இச்சா, கிரியா, ஞான சக்திகளின் வடிவம்; பிரம்மா, விஷ்ணு, உருத்திரன் மற்றும் ஓங்காரமும் நீயே!",
        "Awakening the Muladhara root consciousness through 'Om Gam Ganapataye Namah' to realize the obstacle-free Self.",
        "Radiant red-lotus Muladhara sanctum glowing with a four-armed golden-crimson Maha Ganapati holding noose, goad, and modaka",
        "Rishi Ganaka entered deep samadhi at the dawn of creation to behold the Principle that removes all obstacles to Self-knowledge.",
        "ஆத்ம ஞானத்திற்கு வரும் தடைகளை நீக்கும் மூல தத்துவத்தைக் காண கணக ரிஷி ஆழ்ந்த சமாதியில் அமர்ந்தார்.",
        "Before his inner eye shone Maha Ganapati—single-tusked (Ekadanta), four-armed, radiant as a million rising suns.",
        "அவரது அகக்கண்ணில் கோடி சூர்யப் பிரகாசத்துடன் ஏகதந்தனாக, நான்கு திருக்கரங்களுடன் மகா கணபதி தோன்றினார்.",
        "Ganaka realized that Ganapati is not merely a gatekeeper, but the direct creator, sustainer, and dissolver of the cosmos.",
        "கணபதி வாயிற்காவலர் மட்டுமல்ல; பிரபஞ்சத்தைப் படைத்து, காத்து, ஒடுக்கும் முழுமுதற் பரம்பொருள் என ரிஷி உணர்ந்தார்.",
        "Eternally seated in the Muladhara chakra at the base of the spine, Ganapati governs the three Gunas and three bodies.",
        "முதுகுத்தண்டின் அடியில் மூலாதார சக்கரத்தில் நித்தியமாக வீற்றிருந்து முக்குணங்களையும் மூன்று உடல்களையும் ஆள்பவர் அவரே.",
        "Uttering 'Ga' (first letter), 'Aa' (middle luminance), and the nasal 'M' crescent bindu, the yogi chants 'Om Gam Ganapataye Namah'.",
        "'க'கார முதலும், ஆகார நடுவும், விந்து நாதமும் இணைந்த 'ஓம் கம் கணபதயே நமஹ' எனும் மந்திரத்தை யோகி ஜபிக்கிறான்.",
        "All inner Vighnas (doubts and fears) dissolve like mist before the sun, revealing Ganapati as pure Sachidananda.",
        "சூரியன் முன் பனி போல் அகத் தடைகள் அனைத்தும் நீங்கி, சச்சிதானந்த கணபதியே தான் எனும் உண்மை புலப்படுகிறது."
    ),
    make_shaiva(
        "shaiva_13_panchabrahma", 93, "Panchabrahma Upanishad", "पञ्चब्रह्मोपनिषद्", "பஞ்சபிரம்ம உபநிஷதம்", "Krishna Yajur Veda",
        "Paippalada & Mahadeva: The Five Faces of Sadashiva That Weave the Universe",
        "பைப்பலாதரும் மகாதேவரும்: பிரபஞ்சத்தை நெய்யும் சதாசிவனின் ஐந்து திருமுகங்கள்",
        "Sage Paippalada, Shakalya & Five-Faced Lord Sadashiva",
        "सद्योजातं प्रपद्यामि... वामदेवाय नमो... अघोरेभ्यो... तत्पुरुषाय विद्महे... ईशानः सर्वविद्यानाम् ।",
        "ஸத்யோஜாதம் ப்ரபத்யாமி... வாமதேவாய நமோ... அகோரேப்யோ... தத்புருஷாய வித்மஹே... ஈசான: ஸர்வவித்யானாம் |",
        "Sadyojata, Vamadeva, Aghora, Tatpurusha, and Ishana—these five Brahman faces are the five elements, senses, and cosmic acts of Shiva.",
        "சத்யோஜாதம், வாமதேவம், அகோரம், தத்புருஷம், ஈசானம் ஆகிய ஐந்து பிரம்ம முகங்களே பஞ்ச பூதங்களும் பஞ்ச கிருத்தியங்களும் ஆகும்.",
        "Seeing the entire fivefold universe (Panchabhuta) as the five radiant faces of Sadashiva and transcending into Mahadeva.",
        "Monumental Chola-style sanctum where a five-faced crystalline Sadashiva Lingam radiates five elemental colors into the cosmos",
        "Paippalada asked: 'What existed at the very beginning, and how did the fivefold universe emerge from the One?'",
        "பைப்பலாதர் கேட்டார்: 'ஆதியில் இருந்தது என்ன? ஒன்றான பரம்பொருளிலிருந்து ஐம்பெரும் பூதங்கள் எவ்வாறு தோன்றின?'",
        "Mahadeva revealed the Panchabrahma mystery: Sadyojata is Earth and creation; Vamadeva is Water and preservation.",
        "மகாதேவர் பஞ்சபிரம்ம ரகசியத்தை அருளினார்: சத்யோஜாதம் பூமியும் படைப்பும்; வாமதேவம் நீரும் காத்தலும் ஆகும்.",
        "Aghora is Fire and transformation; Tatpurusha is Air and concealment (tirodhana); Ishana is Sky and liberating grace (anugraha).",
        "அகோரம் நெருப்பும் ஒடுக்கமும்; தத்புருஷம் காற்றும் மறைத்தலும்; ஈசானம் ஆகாயமும் அருளலும் (அனுக்கிரகம்) ஆகும்.",
        "Every breath, sense organ, and direction in the seeker's body is directly animated by these five faces of Sadashiva.",
        "மனித உடலின் ஒவ்வொரு மூச்சும், ஐம்பொறிகளும், திசைகளும் சதாசிவனின் இந்த ஐந்து முகங்களாலேயே இயங்குகின்றன.",
        "Yet beyond the five faces shines the Turiyatita Parashiva—formless, witness of the five, radiant in the lotus of the heart.",
        "ஆயினும் இந்த ஐந்து முகங்களுக்கும் மேலாக, இதயத் தாமரையில் உருவமற்ற துரியாதீத பரசிவன் சாட்சியாக ஒளிர்கிறான்.",
        "Knowing the fivefold world as Shiva's own play, the wise seeker attains liberation while living (Jivanmukti).",
        "ஐம்பெரும் பிரபஞ்சத்தையும் சிவனின் திருவிளையாடலாக உணரும் ஞானி வாழும் போதே ஜீவன்முக்தி அடைகிறான்."
    ),
    make_shaiva(
        "shaiva_14_jabali", 104, "Jabali Upanishad", "जाबाल्युपनिषद्", "ஜாபாலி உபநிஷதம்", "Sama Veda",
        "Jabali & Paippaladi: Pashupati, the Bound Jivas, and the Liberating Line of Ash",
        "ஜாபாலி முனிவரும் பைப்பலாதியும்: பசுபதியும் பாசம் நீக்கும் திருநீற்று நெறியும்",
        "Sage Jabali & Disciple Paippaladi",
        "पशुपतिः अहंकारबद्धान् जीवान् भस्मत्रिपुण्ड्रेण मोचयति ।",
        "பசுபதி: அஹங்கார பத்தான் ஜீவான் பஸ்ம த்ரிபுண்ட்ரேண மோசயதி |",
        "Lord Pashupati liberates the Jivas bound by ego-ropes through the wisdom of Shiva and the sacred Tripundra of ash.",
        "ஆணவப் பாசத்தால் கட்டுண்ட ஜீவன்களை பசுபதியான ஈசன் சிவஞானத்தாலும் திரிபுண்டரத் திருநீற்றாலும் விடுவிக்கிறார்.",
        "Shaiva Siddhanta triad within Vedanta: Pati (Lord Pashupati), Pashu (all living souls), and Pasha (Maya-bondage dissolved by Jnana).",
        "Serene forest ashram beside a lotus pond where deer and sages sit peacefully around Sage Jabali",
        "Disciple Paippaladi bowed to Sage Jabali and asked: 'Master, explain to me the ultimate truth of Pati, Pashu, and Pasha.'",
        "சீடர் பைப்பலாதி ஜாபாலி முனிவரை வணங்கி, 'குருவே! பதி, பசு, பாசம் ஆகியவற்றின் உண்மைத் தத்துவத்தை உபதேசியுங்கள்' என்றார்.",
        "Jabali answered: All conscious beings from Brahma down to a blade of grass are 'Pashu' when bound by ego and karma.",
        "பிரம்மா முதல் புல் பூண்டு வரை அகங்காரத்தாலும் கர்மத்தாலும் கட்டுண்ட அனைத்து உயிர்களும் 'பசு' எனப்படும் என்றார் ஜாபாலி.",
        "Their sole Lord and awakener is 'Pashupati'—Bhagavan Sadashiva, who pervades every heart as the silent Controller.",
        "அந்த உயிர்களின் ஒரே தலைவனும் மீட்பனும் 'பசுபதி'யான பகவான் சதாசிவனே; அவரே அனைத்து இதயங்களிலும் உறைபவர்.",
        "Ignorance of one's divine nature is 'Pasha' (the rope), and the sword that cuts this rope is Shiva-jnana symbolized by Vibhuti.",
        "தன் தெய்வீக இயல்பை மறந்த அறியாமையே 'பாசம்'; அதை அறுக்கும் ஞான வாளின் அடையாளமே புனித விபூதி.",
        "Consecrating the forehead, heart, and shoulders with three lines of ash reminds the soul: 'I am not the perishable body.'",
        "நெற்றி, மார்பு, தோள்களில் அணியும் முக்கோடு, 'நான் அழியும் உடலல்ல, அழியாத ஆன்மா' என்பதை நினைவூட்டுகிறது.",
        "Freed from Pashutva (cattle-like bondage), the awakened soul shines in eternal Shiva-state.",
        "பசுத் தன்மை எனும் கட்டிலிருந்து விடுபட்ட ஆன்மா, நித்திய சிவ நிலையில் பேரொளியாகப் பிரகாசிக்கிறது."
    )
])


import json
import os

def render_shaiva_markdown(u: dict) -> str:
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

def build_shaiva_files():
    out_md_dir = "/home/shishyan/GitHub/GuruKulaDesam/production/upanishad_stories/05_shaiva_upanishads"
    out_json_path = "/home/shishyan/GitHub/GuruKulaDesam/data/upanishads/agent3_shaiva.json"
    os.makedirs(out_md_dir, exist_ok=True)
    os.makedirs(os.path.dirname(out_json_path), exist_ok=True)

    for idx, item in enumerate(SHAIVA_LIST, start=1):
        fname = f"{idx:02d}_muktika_{item['muktika_num']:03d}_{item['id']}.md"
        fpath = os.path.join(out_md_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(render_shaiva_markdown(item))

    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(SHAIVA_LIST, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(SHAIVA_LIST)} Shaiva markdown files in {out_md_dir}")
    print(f"Generated JSON dataset at {out_json_path}")

if __name__ == "__main__":
    build_shaiva_files()
