# -*- coding: utf-8 -*-
"""Agent 5 (Agent 3 Part 3): 8 Shakta & 12 Extra-Canonical Upanishads data & story generator module."""

import json
import os
from pathlib import Path


def make_shakta(uid, mnum, name_en, name_sa, name_ta, veda, story_en, story_ta,
                chars, sloka_sa, sloka_ta, mean_en, mean_ta, theme, setting,
                hook_en, hook_ta, dlg_en, dlg_ta, trial_en, trial_ta,
                rev_en, rev_ta, sadhana_en, sadhana_ta, close_en, close_ta,
                extra_en=None, extra_ta=None):
    base_cam = [
        "Slow cinematic drone push-in through sacred Chola & Himalayan Shakti Peetha pillars and golden kumkuma mist",
        "Medium two-shot of seeker and divine preceptor beside a glowing Sri Chakra homa altar under ancient bilva and kadamba trees",
        "Dynamic tracking shot following the seeker's inner trial amidst cosmic Mahadevi lightning and swirling lotus petals",
        "Extreme close-up on the Mother Goddess's tranquil third eye opening as golden Sri Yantra geometry illuminates",
        "Wide 360-degree orbital shot as the radiant Bindu of Sri Lalita Tripurasundari blazes across the three worlds",
        "Intimate macro shot of sacred vermilion (kumkuma) and sandalwood applied on the brow and glowing Sahasrara lotus",
        "Slow crane pull-back into the starry Bindu-mandala night sky with a radiant golden Sri Chakra & Om emblem"
    ]
    titles = [
        "The Sacred Question Before the Divine Mother",
        "The Seeker Approaches the Shakti Preceptor",
        "The Trial of Maya and the Three Cities",
        "The Mahavakya of Para-Shakti Consciousness",
        "The Cosmic Vision of Sri Chakra & Mahadevi",
        "Inner Sadhana: Bhavana, Sri Vidya & Mantra",
        "Eternal Liberation in Non-Dual Shakti-Brahman"
    ]
    cues = [
        "Deep temple conch (Shankha) + resonant Veena & tanpura drone in D + sacred bell",
        "Warm Sarasvati Veena motif + crackling homa fire ambiance",
        "Low sub-bass pulse + ankle bells (Salangai) echo + rhythmic breath",
        "Crystal singing bowl swell + celestial Devi choir hum + Mridangam tap",
        "Full orchestral Nadaswaram & Veena crescendo + cosmic Panchadashi / Om chant",
        "Gentle Himalayan stream + rhythmic breath-paced tanpura",
        "Fading temple conch + peaceful night breeze + sustained Om Shanti"
    ]
    scenes = []
    if extra_en is not None and extra_ta is not None:
        s5_en, s5_ta = f"{rev_en} {sadhana_en}", f"{rev_ta} {sadhana_ta}"
        s6_en, s6_ta = close_en, close_ta
        s7_en, s7_ta = extra_en, extra_ta
    else:
        s5_en, s5_ta = rev_en, rev_ta
        s6_en, s6_ta = sadhana_en, sadhana_ta
        s7_en, s7_ta = close_en, close_ta
    vo_pairs = [
        (hook_en, hook_ta),
        (dlg_en, dlg_ta),
        (trial_en, trial_ta),
        (f"{sloka_sa} — {mean_en}", f"{sloka_ta} — {mean_ta}"),
        (s5_en, s5_ta),
        (s6_en, s6_ta),
        (s7_en, s7_ta),
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
                f"sacred golden kumkuma particles glowing in volumetric sunbeams, authentic Shakta & Sri Vidya iconography, "
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
        "category": "Shakta",
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


def make_extra(uid, mnum, name_en, name_sa, name_ta, veda, story_en, story_ta,
               chars, sloka_sa, sloka_ta, mean_en, mean_ta, theme, setting,
               hook_en, hook_ta, dlg_en, dlg_ta, trial_en, trial_ta,
               rev_en, rev_ta, sadhana_en, sadhana_ta, close_en, close_ta,
               extra_en=None, extra_ta=None):
    base_cam = [
        "Slow cinematic drone push-in through ancient Bharata forest hermitages and sacred river mist at dawn",
        "Medium two-shot of seeker and sage beside a flickering Vedic Agnihotra fire under ancient banyan roots",
        "Dynamic tracking shot following the seeker's inner inquiry across cosmic space and subtle breath",
        "Extreme close-up on the sage's luminous eyes opening as golden Pranava vibrations ripple through the air",
        "Wide 360-degree orbital shot as the Self-Luminous Sun of Consciousness pierces the veil of time",
        "Intimate macro shot of sacred palms folded in Atma-Puja and glowing heart-lotus light",
        "Slow crane pull-back into the infinite starry sky with a radiant golden Om & Arutperunjothi emblem"
    ]
    titles = [
        "The Sacred Assembly & The Eternal Question",
        "The Seeker Approaches the Illumined Master",
        "The Trial of Mind, Time, and Dualistic Illusion",
        "The Mahavakya of Self-Luminous Reality",
        "The Cosmic Vision of the All-Pervading Atman",
        "Inner Sadhana: Living Worship & Shiva-Sankalpa",
        "Supreme Liberation (Jivanmukti & Sahaja Samadhi)"
    ]
    cues = [
        "Deep Vedic Pranava drone + resonant tanpura in C# + distant temple bell",
        "Warm bamboo flute motif + crackling sacred Agnihotra fire ambiance",
        "Low sub-bass pulse + gentle wind chimes + meditative breath rhythm",
        "Crystal singing bowl swell + celestial Vedic chant hum + Mridangam tap",
        "Full orchestral Veena & Flute crescendo + cosmic Omkara resonance",
        "Gentle sacred river flow + rhythmic breath-paced tanpura",
        "Fading conch (Shankha) + peaceful forest dawn birds + sustained Om Shanti"
    ]
    scenes = []
    if extra_en is not None and extra_ta is not None:
        s5_en, s5_ta = f"{rev_en} {sadhana_en}", f"{rev_ta} {sadhana_ta}"
        s6_en, s6_ta = close_en, close_ta
        s7_en, s7_ta = extra_en, extra_ta
    else:
        s5_en, s5_ta = rev_en, rev_ta
        s6_en, s6_ta = sadhana_en, sadhana_ta
        s7_en, s7_ta = close_en, close_ta
    vo_pairs = [
        (hook_en, hook_ta),
        (dlg_en, dlg_ta),
        (trial_en, trial_ta),
        (f"{sloka_sa} — {mean_en}", f"{sloka_ta} — {mean_ta}"),
        (s5_en, s5_ta),
        (s6_en, s6_ta),
        (s7_en, s7_ta),
    ]
    for idx in range(7):
        ven, vta = vo_pairs[idx]
        scenes.append({
            "scene_num": idx + 1,
            "title": titles[idx],
            "camera": base_cam[idx],
            "flow_prompt": (
                f"Ultra-detailed 8K South Indian & Vedic spiritual cinema, {setting}, "
                f"Scene {idx+1}: {titles[idx]}, featuring {chars}. Warm temple oil-lamp and sunrise chiaroscuro, "
                f"golden dust motes glowing in volumetric sunbeams, authentic Upanishadic iconography, "
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
        "category": "Extra-Canonical",
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


SHAKTA_LIST = [
    make_shakta(
        "shakta_01_sita", 45, "Sita Upanishad", "सीतोपनिषद्", "சீதா உபநிஷதம்", "Atharva Veda",
        "The Devas & Prajapati: Sita as Mulaprakriti Born from the Plough-Tip of Yoga",
        "தேவர்களும் பிரஜாபதியும்: யோகக் கலப்பையின் முனையில் உதித்த மூலப்பிரகிருதி சீதை",
        "The Celestial Devas, Lord Prajapati & Goddess Maha-Sita (Mulaprakriti)",
        "सा सर्ववेदमयी सर्वदेवमयी सर्वलोकमयी सर्वकीर्तिमयी सर्वधर्ममयी सर्वआधारकार्यकारणमयी महालक्ष्मीः ।",
        "ஸா ஸர்வவேதமயீ ஸர்வதேவமயீ ஸர்வலோகமயீ ஸர்வகீர்த்திமயீ ஸர்வதர்மமயீ ஸர்வாதார கார்யகாரணமயீ மஹாலக்ஷ்மீ: |",
        "She is the embodiment of all Vedas, all Devas, all worlds, all glory, all Dharma, and the supreme cause and support of everything—Maha-Lakshmi Sita.",
        "அவளே அனைத்து வேதங்களும், அனைத்து தேவர்களும், அனைத்து உலகங்களும், தர்மமும், காரிய காரணங்களுக்கு ஆதாரமான மகாலட்சுமியான சீதை ஆவாள்.",
        "Sita is not merely an earthly princess but Mulaprakriti (Primordial Nature) and the triple Shakti of Ichha (Will), Jnana (Wisdom), and Kriya (Action) emerging at the tip of the Yogi's plough of contemplation.",
        "Golden Mithila plough-furrow transforming into a cosmic lotus mandala before Prajapati's celestial assembly",
        "Gathered in reverence around Creator Prajapati, the Devas asked: 'Who truly is Sita, and what is the secret of Her divine nature?'",
        "படைப்புக் கடவுளான பிரஜாபதியைச் சூழ்ந்து நின்ற தேவர்கள், 'சீதை என்பவள் உண்மையில் யார்? அவளது தெய்வீக சொரூபத்தின் ரகசியம் என்ன?' என்று கேட்டனர்.",
        "Prajapati answered: 'Sita is Adi-Prakriti—because she is forever united with the syllable Sa (Truth/Immortal Brahman) and sustains the cosmos, she is revered as Sita.'",
        "பிரஜாபதி பதிலளித்தார்: 'சீதையே ஆதி பிரகிருதி; சத்திய பிரம்மத்துடன் (ஸ-காரத்துடன்) இணைந்து அகிலத்தைத் தாங்குவதால் அவள் சீதை எனப் போற்றப்படுகிறாள்.'",
        "When the ignorant see only the physical furrow of the earth, they miss the subtle plough-tip (Langa-agra) where the Yogi's concentrated mind furrows into pure Consciousness.",
        "அறியாமையில் உழல்பவர்கள் மண்ணின் உழுசால் கோட்டை மட்டுமே காண்கிறார்கள்; ஆனால் யோகியின் ஒருமுகப்பட்ட மனம் எனும் கலப்பை முனையில் உதிக்கும் பேரறிவை அவர்கள் அறிவதில்லை.",
        "From that sacred furrow of Yoga shines Devi Sita in three radiant forms: Ichha-Shakti (Moon/Will), Jnana-Shakti (Sun/Wisdom), and Kriya-Shakti (Fire/Action).",
        "அந்த யோகக் கலப்பையின் முனையில் இச்சா சக்தி (சந்திரன்), ஞான சக்தி (சூரியன்), கிரியா சக்தி (அக்னி) எனும் முப்பெரும் ஒளியாக அன்னை சீதை பிரகாசிக்கிறாள்.",
        "As Savitri she chant-initiates the Gayatri; as Sri Mahalakshmi she nourishes all beings; and as Bhudevi she holds the universe in compassionate embrace.",
        "சாவித்திரியாக காயத்ரியை அருள்பவளும், மகாலட்சுமியாக உயிர்களைக் காப்பவளும், பூதேவியாகப் பிரபஞ்சத்தைத் தாங்குபவளும் அந்த ஒரே அன்னையே.",
        "The seeker who meditates upon Sri Rama as the Witness-Light and Sita as the dynamic Shakti of awareness awakens the plough of inner Yoga within the heart.",
        "சாட்சி பூதமான ஸ்ரீ ராமனை ஒளியாகவும், விழிப்புணர்வின் சக்தியாக சீதையையும் தியானிக்கும் சாதகன், தன் இதய வயலில் ஞானக் கலப்பையை இயக்குகிறான்.",
        "In that union of Sita and Rama, nature and spirit merge, and the seeker attains fearless, unbroken bliss.",
        "சீதையும் ராமனும் இணையும் அந்த அத்வைத நிலையில், பிரகிருதியும் புருஷனும் ஒன்றாகி, சாதகன் அச்சமற்ற பேரின்பத்தை அடைகிறான்."
    ),
    make_shakta(
        "shakta_02_tripuratapini", 80, "Tripuratapini Upanishad", "त्रिपुरातापिन्युपनिषद्", "திரிபுராதாபினி உபநிஷதம்", "Atharva Veda",
        "Bhagavan Shiva & The Devas: The 15-Syllable Panchadashi Vidya and the Secret of Sri Chakra",
        "பகவான் சிவனும் தேவர்களும்: பதினைந்து எழுத்து பஞ்சதசி வித்தையும் ஸ்ரீ சக்கர ரகசியமும்",
        "Lord Sadashiva, the Celestial Devas & Goddess Sri Lalita Tripurasundari",
        "कामो योनिः कमला वज्रपाणिर्गुहा हसा मातरिश्वाभ्रमिन्द्रः । पुनर्गुहा सकला मायया च पुरुच्यैषा विश्वमातादिविद्याम् ॥",
        "காமோ யோனி: கமலா வஜ்ரபாணிர் குஹா ஹஸா மாதரிஸ்வாப்ரமிந்த்ர: | புனர்குஹா ஸகலா மாயயா ச புருச்யைஷா விஸ்வமாதாதிவித்யாம் ||",
        "Through the sacred seed-syllables of Vagbhava, Kamaraja, and Shakti Kutas shines the primordial Panchadashi Vidya of the Mother of the Universe.",
        "வாக்பவ கூடம், காமராஜ கூடம், சக்தி கூடம் ஆகிய மூன்று கூடங்களில் பிரபஞ்ச மாதாவின் ஆதி வித்தையான பஞ்சதசி மந்திரம் ஒளிர்கிறது.",
        "Synthesis of Vedic Gayatri and Tantric Panchadashi Mantra (Ka-E-I-La-Hrim, Ha-Sa-Ka-Ha-La-Hrim, Sa-Ka-La-Hrim) mapped onto the cosmic Sri Chakra and Kamakala.",
        "Mount Kailasa crystal court opening into a blazing golden Meru Sri Chakra of nine interlocking triangles",
        "In the beginning, Bhagavan Shiva—radiant with the power of Tripurasundari—was approached by the Devas seeking the supreme saving wisdom.",
        "ஆதியில் திரிபுரசுந்தரியின் பேரருளால் ஒளிர்ந்த பகவான் சிவபெருமானை அணுகிய தேவர்கள், பிறவிப் பிணி தீர்க்கும் பரம வித்தையை உபதேசிக்குமாறு வேண்டினர்.",
        "Lord Shiva revealed that when the Vedic Gayatri expands into its esoteric heart, it becomes the 15-syllable Panchadashi Mantra of Sri Lalita.",
        "வேத மாதாவான காயத்ரி மந்திரத்தின் உட்பொருளே ஸ்ரீ லலிதாம்பிகையின் பதினைந்து எழுத்துப் பஞ்சதசி மகா மந்திரமாக விரிகிறது என்று சிவபெருமான் அருளினார்.",
        "Lost in external rituals, mortals fail to recognize the three Kutas—Fire of Speech (Vagbhava), Sun of Heart-Desire (Kamaraja), and Moon of Kundalini Grace (Shakti).",
        "புறச் சடங்குகளில் மயங்கும் மனிதர்கள், வாக்பவ கூடம் (அக்னி), காமராஜ கூடம் (சூரியன்), சக்தி கூடம் (சந்திரன்) ஆகிய முப்பெரும் உட்கூறுகளை உணர்வதில்லை.",
        "When the 16th hidden syllable (Shodashi) crowns the fifteen digits of the Moon, the seeker beholds the Mother beyond all changing phases of time.",
        "சந்திரனின் பதினைந்து கலைகளுக்கு மேலாகப் பதினாறாவது நித்திய கலையான ஷோடசி ஒளிரும்போது, காலத்தைக் கடந்த அன்னையின் தரிசனம் கிட்டுகிறது.",
        "Tracing the nine enclosures (Avaranas) of the Sri Chakra from the outer square of earth to the central Bindu of pure bliss, Shiva-Shakti are seen in eternal embrace.",
        "ஸ்ரீ சக்கரத்தின் ஒன்பது ஆவரணங்களையும் கடந்து நடுவில் உள்ள பிந்து ಸ್ಥಾನத்தை அடையும்போது, சிவசக்தி ஐக்கியத்தின் பேரானந்தம் வெளிப்படுகிறது.",
        "Meditating on Kamakala in the cave of the heart, the yogi dissolves the knots of ego, desire, and karma into the ocean of Consciousness.",
        "இதயக் குகையில் காமகலா தியானத்தில் நிலைக்கும் யோகி, அகங்காரம், ஆசை, கர்மம் எனும் முடிச்சுகளை அவிழ்த்து சித்-சமுத்திரத்தில் கலக்கிறான்.",
        "Whoever knows this Tripuratapini secret becomes one with the Empress of the Three Worlds and never returns to sorrow.",
        "திரிபுராதாபினி உபநிஷதத்தின் இந்த மெய்ஞ்ஞானத்தை உணர்பவன் மூவுலக ஆட்சி நாயகியுடன் இரண்டறக் கலந்து பிறவாப் பேரின்பம் பெறுகிறான்."
    ),
    make_shakta(
        "shakta_03_devi", 81, "Devi Upanishad", "देव्युपनिषद्", "தேவி உபநிஷதம்", "Atharva Veda",
        "All Devas Before Mahadevi: 'I Am Brahman-Consciousness, Empress of the Universe'",
        "மகாதேவியின் முன் தேவர்கள்: 'நானே பிரம்ம சொரூபிணி, அகிலத்தின் பேரரசி!'",
        "Indra, Agni, Varuna, all Vedic Devas & Supreme Mother Mahadevi (Durga/Brahmasvarupini)",
        "अहं ब्रह्मस्वरूपिणी । मत्तः प्रकृतिपुरुषात्मकं जगत् । शून्याशून्यं च । अहमानन्दानानन्दौ । विज्ञानाविज्ञाने अहम् ।",
        "அஹம் ப்ரஹ்மஸ்வரூபிணீ | மத்த: ப்ரக்ருதி புருஷாத்மகம் ஜகத் | சூன்யாசூன்யம் ச | அஹமானந்தானானந்தௌ | விஞ்ஞானாவிஞ்ஞானே அஹம் |",
        "I am of the nature of Supreme Brahman! From Me proceeds the universe of Prakriti and Purusha, the void and non-void, bliss and non-bliss, knowledge and ignorance.",
        "நானே பரப்பிரம்ம சொரூபிணி! என்னிடமிருந்தே பிரகிருதி-புருஷ மயமான இப்பிரபஞ்சமும், சூன்யமும் பூர்ணமும், ஆனந்தமும் ஞானமும் தோன்றுகின்றன.",
        "The supreme Shakta Mahavakya: The Goddess herself declares in the first person (Devi Atharvashirsha) that She is non-dual Brahman empowering all Vedic gods.",
        "Cosmic Himalayan amphitheater of golden fire where all thirty-three Vedic Devas bow before the Lion-mounted Mother",
        "All the Devas approached the Great Goddess in awe and asked with folded hands: 'O Mahadevi, who art Thou in truth?'",
        "தேவர்கள் அனைவரும் பேரொளியாக நின்ற மகாதேவியை அணுகி, இரு கரம் கூப்பி, 'மகாதேவியே! தாங்கள் உண்மையில் யார்?' என்று பணிவுடன் கேட்டனர்.",
        "With a voice resounding across galaxies, Devi declared: 'I am Brahman-Consciousness itself! From Me alone arise both Spirit (Purusha) and Nature (Prakriti).'",
        "அண்ட சராசரங்களும் அதிரும்படி அன்னை அருளினாள்: 'நானே பிரம்ம சொரூபிணி! புருஷனும் பிரகிருதியும் கூடிய இப்பிரபஞ்சம் என்னிடமிருந்தே உதிக்கிறது.'",
        "When the Devas wondered who moves the sun, fire, and breath, She proclaimed: 'I walk as the Rudras and Vasus; I sustain Mitra, Varuna, Indra, and Agni!'",
        "சூரியனையும் அக்னியையும் மூச்சையும் இயக்குவது யார் எனத் தேவர்கள் வியந்தபோது, 'நானே ருத்ரர்களாகவும் வசுக்களாகவும் சஞ்சரிக்கிறேன்; இந்திரனையும் அக்னியையும் நானே தாங்குகிறேன்' என்றாள்.",
        "She is the One without a second—both the transcendent Tureeeya silence and the dynamic Sakala universe, known only through non-dual wisdom.",
        "பிரம்மமும் அபிரம்மமும் அவளே; ஐம்பெரும் பூதங்களும் அவளே; இரண்டற்ற அத்வைத ஞானத்தால் மட்டுமே அறியப்படும் பரம்பொருள் அவளே.",
        "Beholding Her radiant form mounted on the Lion of Dharma, holding the noose of love and goad of awakening, the Devas chanted the immortal Durga Gayatri.",
        "தர்ம சிம்மத்தின் மீது அமர்ந்து, பாச அங்குசம் ஏந்தி, அபய வரதம் அருளும் அன்னையைத் தரிசித்த தேவர்கள், அழியாத துர்க்கா காயத்ரியால் போற்றினர்.",
        "In the lotus of the heart, the seeker invokes the nine-lettered Navarna and single-syllable Hrim mantra to cross the ocean of fear.",
        "இதயத் தாமரையில் உறையும் அன்னையை 'ஹ்ரீம்' எனும் மாயா பீஜத்தாலும் நவார்ண மந்திரத்தாலும் தியானிக்கும் சாதகன், பிறவிப் பெருங்கடலைக் கடக்கிறான்.",
        "Knowing the Mother as one's own innermost Witness-Self, all fear vanishes into the boundless peace of Devi Atharvashirsha.",
        "தன் அகத்துள் ஒளிரும் சாட்சி ஆன்மாவே ஜகன்மாதா என்பதை உணரும்போது, அனைத்து பயங்களும் நீங்கி நித்திய சாந்தி நிலவுகிறது."
    ),
    make_shakta(
        "shakta_04_tripura", 82, "Tripura Upanishad", "त्रिपुरोपनिषद्", "திரிபுரா உபநிஷதம்", "Rig Veda",
        "The Three Cities & The One Mother: Waking, Dream, and Deep Sleep Illumined by Tripura",
        "மூன்று புரங்களும் ஒரே அன்னையும்: நனவு, கனவு, ஆழ்உறக்கத்தை ஒளிரச் செய்யும் திரிபுரை",
        "Adi Shankaracharya (Commentator Lineage), Rigvedic Seers & Goddess Tripura (Turiya Chit-Shakti)",
        "तिस्रः पुरस्त्रिपथा विश्वचर्षणी अत्राकथा अक्षराः सन्निविष्टाः । अधिष्ठायैना अजरा पुराणी महत्तरा महिमा देवतानाम् ॥",
        "திஸ்ர: புரஸ்த்ரிபதா விஸ்வசர்ஷணீ அத்ராகதா அக்ஷரா: ஸன்னிவிஷ்டா: | அதிஷ்டாயைனா அஜரா புராணீ மஹத்தரா மஹிமா தேவதானாம் ||",
        "Three are the cities, three the paths open to all; here the imperishable letters are set. Presiding over them all is the ageless, ancient, supreme Majesty of the Gods—Tripura!",
        "மூன்று புரங்களும், மூன்று பாதைகளும் இங்கு விரிந்துள்ளன; இவற்றையெல்லாம் கடந்து ஆட்சி செய்பவள் மூப்பற்றவளும் ஆதியானவளுமான திரிபுரா தேவியின்ப் பெருமையே ஆகும்.",
        "Advaita Shakta synthesis (celebrated in Shankara's commentary): 'Tripura' means the Witness Consciousness that precedes and illumines the triad of Waking, Dream, and Deep Sleep.",
        "Sacred Rigvedic riverside mandapam where three concentric rings of fire, sun, and moon merge into one diamond star",
        "Why is the Supreme Reality worshiped by the wise as 'Tripura'—She of the Three Cities?",
        "பரம்பொருளை ஞானிகள் ஏன் 'திரிபுரா'—மூன்று புரங்களை உடையவள் என்று போற்றி வணங்குகிறார்கள்?",
        "The Rigvedic seers revealed: Every soul travels through three cities (Puras) and three paths—Waking (Jagrat), Dream (Svapna), and Deep Sleep (Sushupti).",
        "ரிக்வேத ரிஷிகள் உரைத்தனர்: ஒவ்வொரு உயிரும் விழிப்பு (நனவு), கனவு, ஆழ்உறக்கம் எனும் மூன்று புரங்களிலும் மூன்று பாதைகளிலுமே சஞ்சரிக்கிறது.",
        "Like travelers trapped in revolving citadels of gross body, subtle mind, and causal ignorance, mortals forget the motionless Queen who watches all three.",
        "ஸ்தூல உடல், சூட்சும மனம், காரண அறியாமை எனும் சுழலும் கோட்டைகளில் சிக்கிய மனிதர்கள், இம்மூன்றையும் சாட்சியாகக் காணும் அரசியை மறந்துவிடுகின்றனர்.",
        "Presiding over the three states—ageless, ancient, and self-luminous—shines the Fourth (Turiya) Consciousness, revered as Goddess Tripura!",
        "இம்மூன்று அவஸ்தைகளுக்கும் மேலாக, மூப்பற்றவளாய், பழமையானவளாய், சுயம்பிரகாசமாய் ஒளிரும் நான்காவது துரிய உணர்வே 'திரிபுரா' தேவி!",
        "Through the nine triangles of Prakriti and Purusha, She weaves creation, preservation, and dissolution while remaining utterly untouched.",
        "பிரகிருதி மற்றும் புருஷனின் ஒன்பது முக்கோணங்கள் வழியாகப் படைத்தல், காத்தல், ஒடுக்குதல் ஆகியவற்றை நிகழ்த்தினாலும், அவள் எதிலும் தோயாமல் தூயவளாக விளங்குகிறாள்.",
        "When the seeker unifies the external offering with internal samadhi, the three cities of duality melt into the single nectar-ocean of Sri Vidya.",
        "புற வழிபாட்டையும் அகச் சமாதியையும் சாதகன் ஒன்றிணைக்கும்போது, இருமை எனும் மூன்று புரங்களும் ஸ்ரீ வித்தையின் அமிர்தக் கடலில் கரைகின்றன.",
        "All desires fulfilled in the Self, the knower of Tripura abides as pure, undivided Consciousness.",
        "ஆன்மாவில் அனைத்து விருப்பங்களும் நிறைவுற, திரிபுரையை அறிந்த ஞானி பிளவற்ற தூய பிரக்ஞையாக நிலைத்திருக்கிறான்."
    ),
    make_shakta(
        "shakta_05_bhavana", 84, "Bhavana Upanishad", "भावनोपनिषद्", "பாவனா உபநிஷதம்", "Atharva Veda",
        "The Human Body as the Living Sri Chakra: Where Every Breath is the Mother's Arati",
        "மனித உடலே வாழும் ஸ்ரீ சக்கரம்: ஒவ்வொரு மூச்சும் அன்னையின் ஆராதனை",
        "Sri Guru (All-Power Embodiment) & Awakened Disciple meditating on the Inner Sri Chakra",
        "श्रीगुरुः सर्वकारणभूता शक्तिः । तेन நवरन्ध्ररूपो देहः नवचक्ररूपं श्रीचक्रम् ।",
        "ஸ்ரீகுரு: ஸர்வகாரணபூதா சக்தி: | தேன நவரந்த்ரரூபோ தேஹ: நவசக்ரரூபம் ஸ்ரீசக்ரம் |",
        "The auspicious Guru is the Supreme Shakti, the cause of all; through that realization, this nine-gated human body itself becomes the nine-enclosure Sri Chakra!",
        "ஸ்ரீ குருவே அனைத்திற்கும் காரணமான பராசக்தி; அந்த ஞான பாவனையால் ஒன்பது வாயில்கள் கொண்ட இந்த மனித உடலே ஒன்பது ஆவரணங்கள் கொண்ட ஸ்ரீ சக்கரமாகிறது!",
        "Internalization of Sri Vidya ritual (Antaryaga): transforming anatomy, senses, thoughts, and breath into the living mandala of Lalita Tripurasundari.",
        "Translucent yogic figure seated in Padmasana within a temple sanctum as a glowing 3D Sri Chakra aligns with the spine and chakras",
        "A sincere seeker asked the Guru: 'Must one collect gold, gems, and outer diagrams to worship the Divine Mother, or is her temple closer still?'",
        "உண்மையான சாதகன் ஒருவன் குருவிடம் கேட்டான்: 'ஜகன்மாதாவை வழிபடப் பொன்னும் மணியும் புறச் சக்கரங்களும் தேவையா, அல்லது அவளது ஆலயம் நமக்குள்ளேயே உள்ளதா?'",
        "The Guru smiled with compassion: 'Sri Guru himself is the Primordial Shakti! Look within—your own nine-gated body is the living Sri Chakra of nine enclosures.'",
        "குரு கருணையுடன் புன்னகைத்தார்: 'ஸ்ரீ குருவே ஆதி பராசக்தி! உன் உள்ளே பார்—ஒன்பது வாசல்கள் கொண்ட உன் உடலே ஒன்பது ஆவரணங்கள் கொண்ட வாழும் ஸ்ரீ சக்கரம்!'",
        "Skin, blood, flesh, fat, bone, marrow, and жизненная essence, together with the five senses and mind, form the Yoginis and mudras of the outer courts.",
        "தோல், இரத்தம், தசை, எலும்பு, மஜ்ஜை ஆகிய தாதுக்களும், ஐம்பொறிகளும் மனமும், ஆவரண தேவதைகளாகவும் யோகினிகளாகவும் உன்னுள்ளேயே திகழ்கின்றன.",
        "At the very center of the pericarp shines the Sahasrara lotus, where the individual soul (Jiva) is Shiva and Supreme Consciousness (Samvit) is Lalita!",
        "இதய மற்றும் சஹஸ்ரார கமலத்தின் நடுவே, சீவனே சிவனாகவும், தூய பிரக்ஞையே (சம்வித்) லலிதா பரமேஸ்வரியாகவும் ஒளிர்கிறார்கள்!",
        "Virtue and non-virtue become the offerings; unshakeable discrimination is the sacred bell; and the withdrawal of senses into stillness is the true mudra.",
        "புண்ணிய பாவங்களே நைவேத்தியம்; விவேகமே மணியோசை; ஐம்பொறிகளை அடக்கி மௌனத்தில் நிலைப்பதே உண்மையான முத்திரை வழிபாடு.",
        "Even natural breathing is the sixteen-fold royal service (Shodashopachara), and the contemplation 'I am That Brahman-Shakti' is the supreme Homa fire.",
        "சுவாசிக்கும் ஒவ்வொரு மூச்சுமே ஷோடச உபசார பூஜையாகிறது; 'நானே அந்தப் பராசக்தி' எனும் அभेद பாவனையே மேலான ஓம அக்னியாகிறது.",
        "Anchored in this unbroken Bhavana for even three Muhurtas, the seeker becomes a Jivanmukta—walking the earth as the Mother's own grace.",
        "இத்தகைய இடைவிடாத பாவனை யோகத்தில் நிலைக்கும் சாதகன், வாழும் போதே ஜீவன்முக்தனாகி அன்னையின் அருள் வடிவமாகவே திகழ்கிறான்."
    ),
    make_shakta(
        "shakta_06_saubhagyalakshmi", 105, "Saubhagyalakshmi Upanishad", "सौभाग्यलक्ष्म्युपनिषद्", "சௌபாக்யலக்ஷ்மி உபநிஷதம்", "Rig Veda",
        "Narayana & Rudra: How True Inner Fortune (Saubhagya) Blossoms Through Yoga and Sri Vidya",
        "நாராயணரும் ருத்ரனும்: ஸ்ரீ வித்தையும் ராஜ யோகமும் இணையும் உண்மையான சௌபாக்கியம்",
        "Bhagavan Narayana, Lord Rudra, Eternal Rishis & Goddess Saubhagya-Lakshmi",
        "हिरण्यवर्णां हरिणीं सुवर्णरजतस्रजाम् । चन्द्रां हिरण्मयीं लक्ष्मीं जातवेदो म आवह ॥",
        "ஹிரண்யவர்ணாம் ஹரிணீம் ஸுவர்ணரஜதஸ்ரஜாம் | சந்த்ராம் ஹிரண்மயீம் லக்ஷ்மீம் ஜாதவேதோ ம ஆவஹ ||",
        "O Jatavedas Agni, invoke for me that Lakshmi of golden hue, radiant as the moon and adorned with garlands of gold and silver—the Inner Light of Liberation!",
        "ஜாதவேத அக்னியே! பொன் நிறத்தவளும், சந்திரனைப் போல் குளிர்ந்த ஒளியுடையவளும், ஆன்ம விடுதலையின் செல்வமுமான அந்த லட்சுமி தேவியை எனக்குள் எழுந்தருளச் செய்வாயாக!",
        "Uniting the Vedic Sri Sukta and Shakta Sri Vidya with Ashtanga/Kundalini Yoga across the nine chakras to attain imperishable spiritual fortune (Moksha-Saubhagya).",
        "Celestial Milk Ocean and Himalayan lotus sanctuary where golden Sri Sukta verses spiral up the nine yogic chakras",
        "The great Rishis approached Bhagavan Narayana and Lord Rudra, asking: 'What is that imperishable Saubhagya (Fortune) that never fades with death?'",
        "மகரிஷிகள் பகவான் நாராயணரையும் ருத்ரனையும் அணுகி, 'மரணத்தாலும் அழியாத நித்திய சௌபாக்கியம் என்பது எது?' என்று கேட்டனர்.",
        "Narayana revealed the sacred Saubhagya-Lakshmi Vidya to Rudra: 'Outer wealth comes and goes like clouds, but the Lakshmi of Self-Realization is eternal.'",
        "நாராயணர் ருத்ரனுக்குச் சௌபாக்கிய லட்சுமி வித்தையை அருளினார்: 'புறச் செல்வம் மேகம் போல் வந்து போகும்; ஆனால் ஆன்ம ஞானம் எனும் லட்சுமியே நிலையானவள்.'",
        "To awaken Her, the seeker first chants the fifteen verses of the Sri Sukta with single-pointed purity and the seed syllable 'Srim'.",
        "அவளைத் தரிசிக்க, சாதகன் முதலில் தூய மனதுடன் ஸ்ரீ சூக்தத்தின் பதினைந்து ரிக்குகளையும் 'ஸ்ரீம்' எனும் பீஜ மந்திரத்தையும் தியானிக்க வேண்டும்.",
        "Yet mantra alone must merge into Yoga: conquering posture, breath, and desire, the yogi hears the unstruck Nada sound rising like a conch, flute, and veena.",
        "மந்திரம் யோகத்துடன் இணைய வேண்டும்; ஆசனமும் பிராணாயாமமும் கைகூடும்போது, சங்கு, புல்லாங்குழல், வீணை போன்ற அனாஹத நாதம் உள்ளே ஒலிக்கிறது.",
        "Through the nine chakras—from Muladhara and Svadhishthana up to Ajna, Bindu, Nada, and Nirvana-Chakra—Goddess Lakshmi ascends as liquid lightning.",
        "மூலாதாரம் முதல் ஆக்ஞை, பிந்து, நாதம், நிர்வாண சக்கரம் வரையிலான ஒன்பது சக்கரங்களின் வழியாக மகாலட்சுமி மின்னல் கொடியைப் போல் மேலெழுகிறாள்.",
        "In the thousand-petaled Sahasrara lotus, She shines not as coins of gold, but as the boundless nectar of Turiya consciousness.",
        "ஆயிரம் இதழ் கொண்ட சஹஸ்ரார தாமரையில், அவள் உலகியல் பொன்னாக அல்லாமல், துரியப் பேரறிவின் அமிர்த வெள்ளமாகப் பிரகாசிக்கிறாள்.",
        "Free from greed and dualistic sorrow, the knower of Saubhagya-Lakshmi enjoys the sovereignty of both worlds and attains liberation.",
        "பேராசையும் இருமைத் துயரமும் நீங்கிய சௌபாக்கிய லட்சுமி உபாசகன், இம்மையிலும் மறுமையிலும் பூரண விடுதலையை அடைகிறான்."
    ),
    make_shakta(
        "shakta_07_sarasvatirahasya", 106, "Sarasvati-rahasya Upanishad", "सरस्वतीरहस्योपनिषद्", "சரஸ்வதி ரகசிய உபநிஷதம்", "Krishna Yajur Veda",
        "Ashvalayana & Goddess Sarasvati: The Ten Rigvedic Hymns and the Secret that Maya is Only a Shadow",
        "ஆஸ்வலாயனரும் சரஸ்வதி தேவியும்: பத்து ரிக் வேத மந்திரங்களும் மாயை கடக்கும் பிரம்ம ஞானமும்",
        "Maharishi Ashvalayana & Goddess Bhagavati Sarasvati (Supreme Vak & Adhishthana Brahman)",
        "मयि सर्वमिदं प्रोतं सूत्रे मणिगणा इव । मामैवं জানतस्त्यागान्माया याति परिक्षयम् ॥",
        "மயி ஸர்வமிதம் ப்ரோதம் ஸூத்ரே மணிகணா இவ | மாமைவம் ஜானதஸ்த்யாகான் மாயா யாதி பரிக்ஷயம் ||",
        "In Me all this universe is strung like pearls upon a thread! For one who knows Me thus in truth, Maya utterly perishes.",
        "நூலில் கோக்கப்பட்ட மணிகளைப் போல இப்பிரபஞ்சம் அனைத்தும் என்னில் கோக்கப்பட்டுள்ளது! என்னை இவ்வாறு உள்ளபடி அறிபவனுக்கு மாயை முற்றிலும் அழிந்துவிடுகிறது.",
        "Union of Bhakti (10 Rigvedic Sarasvati mantras with seed syllables) and Advaita Vedanta (Goddess Sarasvati herself teaching Asangoham—'I am the unattached Witness beyond Maya').",
        "Crystal-clear Himalayan confluence where Goddess Sarasvati in luminous white silk holds the Veena and palm-leaf Vedas before Sage Ashvalayana",
        "Seeking the ultimate essence of Speech and Wisdom, Maharishi Ashvalayana performed austere penance and praised Bhagavati Sarasvati with ten Rigvedic hymns.",
        "வாக்கின் மூலத்தையும் பரம ஞானத்தையும் வேண்டி ஆஸ்வலாயன மகரிஷி கடும் தவம் இயற்றி, பத்து ரிக் வேத மந்திரங்களால் பகவதி சரஸ்வதியைப் போற்றினார்.",
        "From 'Prano Devi Sarasvati' to 'Utashyamah', each Vedic verse unlocked a secret Tantric seed—Aim, Klim, Blum, Hrim—illuminating the ten directions.",
        "'பிரணோ தேவி சரஸ்வதி' முதலான பத்து வேத மந்திரங்களும் 'ஐம், க்லீம், ஹ்ரீம்' எனும் பீஜ அட்சரங்களுடன் இணைந்து பத்துத் திசைகளையும் ஒளிரச் செய்தன.",
        "Pleased by his devotion, the White-Robed Mother appeared holding the Veena, Rosary, and Book of Wisdom, speaking in gentle, nectar-filled tones.",
        "அவரது பக்தியில் மகிழ்ந்த வெண்ணிற ஆடை அணிந்த வாணி தேவி, வீணையும் ஜபமாலையும் ஞானப் புத்தகமும் ஏந்திப் புன்னகையுடன் காட்சி தந்தாள்.",
        "Sarasvati revealed Her highest Rahasya (Secret): 'Wait not merely at the shore of words, O Ashvalayana! I am the timeless Brahman-Consciousness behind every syllable.'",
        "சரஸ்வதி தேவி தன் பரம ரகசியத்தை உரைத்தாள்: 'ஆஸ்வலாயனரே! வெறும் சொற்களின் கரையில் நின்றுவிடாதீர்; ஒவ்வொரு எழுத்துக்கும் பின்னால் ஒளிரும் காலமற்ற பிரம்ம உணர்வே நான்!'",
        "Just as space appears divided inside a jar or a hall yet remains one, I appear as Jiva and Ishvara only through the veil of Maya.",
        "குடத்திற்குள்ளும் மாளிகைக்குள்ளும் ஆகாயம் பிரிந்தது போல் தோன்றினாலும் அது ஒன்றே; அதுபோல் மாயையின் திரையால் மட்டுமே நான் ஜீவனாகவும் ஈஸ்வரனாகவும் தோன்றுகிறேன்.",
        "Practicing dualistic devotion and six-limbed meditation inside the heart-lotus, the seeker purifies the mind until the mirror of intellect reflects the One.",
        "இதயத் தாமரையில் பக்தியுடனும் ஆறு அங்க தியானத்துடனும் அன்னையை வழிபடும்போது, அந்தக்கரணம் தூய்மையடைந்து ஏகப் பரம்பொருளைப் பிரதிபலிக்கிறது.",
        "Awakening to the roar 'Asango-ham—I am unattached, self-luminous Consciousness!', the knower of Sarasvati-Rahasya shines free from delusion forever.",
        "'அசங்கோஹம்—நான் எதிலும் ஒட்டாத சுயம்பிரகாச சைதன்யம்!' எனும் ஞான முழக்கத்துடன், சரஸ்வதி ரகசியத்தை அறிந்தவன் மயக்கம் நீங்கி என்றும் சுதந்திரனாகிறான்."
    ),
    make_shakta(
        "shakta_08_bahvricha", 107, "Bahvricha Upanishad", "बह्वृचोपनिषद्", "பஹ்வ்ருச உபநிஷதம்", "Rig Veda",
        "In the Beginning Was the Goddess Alone: How Mahadevi Birthed the Trinity and the Four Mahavakyas",
        "ஆதியில் அன்னை ஒருத்தியே இருந்தாள்: மும்மூர்த்திகளையும் நான்கு மகாவாக்கியங்களையும் ஈன்ற பராசக்தி",
        "Rigvedic Bahvricha Seers & Adi-Parashakti Lalita Bala Tripurasundari",
        "देवी ह्येकाग्र आसीत् । सैव जगदण्डमसृजत् । प्रज्ञानं ब्रह्मेति वा अहं ब्रह्मास्मीति वा भाष्यते ।",
        "தேவீ ஹ்யேகாக்ர ஆஸீத் | ஸைவ ஜகதண்டமஸ்ருஜத் | ப்ரக்ஞானம் ப்ரஹ்மேதி வா அஹம் ப்ரஹ்மாஸ்மீதி வா பாஷ்யதே |",
        "Verily, the Goddess alone existed in the beginning! She alone projected the cosmic egg; it is She who is proclaimed as 'Prajnanam Brahma' and 'Aham Brahmasmi'.",
        "ஆதியில் தேவி ஒருத்தியே இருந்தாள்! அவளே பிரபஞ்ச அண்டத்தைப் படைத்தாள்; 'பிரக்ஞானம் பிரம்ம', 'அஹம் பிரம்மாஸ்மி' என்று வேதங்கள் போற்றுவதும் அவளையே ஆகும்.",
        "Supreme non-dual Shakta-Advaita: Adi-Shakti is the sole Reality from whom Brahma, Vishnu, Rudra, the Maruts, and all four Vedic Mahavakyas arise.",
        "Primordial golden-crimson cosmic ocean before creation, where a single blazing Bindu blossoms into the sixteen-petaled lotus of creation",
        "Before the sun dawned, before space unfurled, before even the creator gods opened their eyes—what existed in the very beginning?",
        "சூரியன் உதிக்கும் முன், ஆகாயம் விரியும் முன், படைப்புக் கடவுள்களும் கண் விழிக்கும் முன்—ஆதியில் இருந்தது என்ன?",
        "The Rigvedic Bahvricha seers proclaimed: 'Devi hy-ekagra asit—In the beginning, the Great Goddess alone existed, One without a second!'",
        "ரிக்வேத பஹ்வ்ருச ரிஷிகள் முழங்கினர்: 'தேவீ ஹ்யேகாக்ர ஆஸீத்—ஆதியில் இரண்டற்ற ஒருத்தியாக மகா தேவி மட்டுமே வீற்றிருந்தாள்!'",
        "By Her own sovereign wave of Kama-Kala, She projected the cosmic egg and gave birth to Brahma, Vishnu, Rudra, Indra, Agni, and the celestial Maruts.",
        "தன் சுதந்திரமான காமகலா சங்கல்பத்தால் அவளே பிரபஞ்ச அண்டத்தைத் தோற்றுவித்து, பிரம்மா, விஷ்ணு, ருத்ரன், இந்திரன், அக்னி ஆகியோரைப் படைத்தாள்.",
        "As Bala, Ambika, Bagalamukhi, and Savitri, She governs all worlds; yet in Her highest essence She is the nameless Turiyatita Consciousness.",
        "பாலாம்பிகையாகவும், பகளாமுகியாகவும், சாவித்திரியாகவும் உலகங்களை ஆளும் அவள், தன் பரம சொரூபத்தில் நாமரூபங்களைக் கடந்த துரியாதீத சித்-சக்தியே ஆவாள்.",
        "When the four Vedas thunder 'Prajnanam Brahma', 'Aham Brahmasmi', 'Tat Tvam Asi', and 'Ayam Atma Brahma', they are singing the glory of this Mother alone!",
        "நான்கு வேதங்களும் 'பிரக்ஞானம் பிரம்ம', 'அஹம் பிரம்மாஸ்மி', 'தத் த்வம் அஸி', 'அயம் ஆத்மா பிரம்ம' என்று முழங்குவது இந்த அன்னையின் மகிமையையே!",
        "She is the inner Shringataka triangle within the brow and heart, radiating the fifteen syllables of light and the sixteenth digit of immortality.",
        "நெற்றியிலும் இதயத்திலும் உள்ள சிருங்கார முக்கோணத்தில் உறைந்து, பதினைந்து கலைகளாகவும் பதினாறாவது அமிர்த கலையாகவும் ஒளிர்பவள் அவளே.",
        "Realizing 'There is nothing whatsoever separate from Her', the wise seeker dissolves into the supreme Shodashi-Brahman.",
        "'அவளைத் தவிர வேறொன்றும் இவ்வுலகில் இல்லை' என்று தெளிந்த ஞானி, பராசக்தியின் அகண்ட பேரொளியில் இரண்டறக் கலக்கிறான்."
    )
]


EXTRA_LIST = [
    make_extra(
        "extra_01_muktika", 108, "Muktika Upanishad", "मुक्तिकोपनिषद्", "முக்திகா உபநிஷதம்", "Shukla Yajur Veda",
        "Sri Rama & Hanuman in Ayodhya: The Canon of 108 Upanishads and the Lion-Roar of Mandukya",
        "அயோத்தியில் ஸ்ரீ ராமரும் அனுமனும்: 108 உபநிஷதங்களின்த் தொகுப்பும் மாண்டூக்ய முழக்கமும்",
        "Bhagavan Sri Ramachandra, Maruti Hanuman, Sita, Lakshmana & Maharishi Vasishtha",
        "माण्डूक्यमेकमेवालं मुमुक्षूणां विमुक्तये । तथाप्यसिद्धं चेज्ज्ञानं दशोपनिषदं पठ ॥",
        "மாண்டூக்யமேகமேவாலம் முமுக்ஷூணாம் விமுக்தயே | ததாப்யஸித்தம் சேஜ்ஞானம் தசோபநிஷதம் பட ||",
        "The Mandukya Upanishad alone is sufficient for the liberation of sincere seekers! If wisdom still ripens not, study the ten, thirty-two, or all 108 Upanishads.",
        "முமுட்சுக்களின் மோட்சத்திற்கு மாண்டூக்ய உபநிஷதம் ஒன்றே போதுமானது! அதிலும் ஞானம் நிலைபெறாவிட்டால் பத்து, முப்பத்திரண்டு அல்லது 108 உபநிஷதங்களையும் பயில்வாயாக.",
        "The grand culmination of the Upanishadic canon: Sri Rama reveals the 108 Upanishads across the four Vedas and teaches Vasanakshaya (dissolution of latent desires) and Manonasha (quieting of the mind) for Jivanmukti and Videhamukti.",
        "Golden throne hall of Ayodhya surrounded by rishis, where Maruti Hanuman kneels in radiant devotion before Sri Ramachandra",
        "In the resplendent court of Ayodhya, Maruti Hanuman bowed before Bhagavan Sri Rama and asked: 'Lord, how may a seeker cross the ocean of birth and death effortlessly?'",
        "அயோத்தியின் பொன்மயமான சபையில் பகவான் ஸ்ரீ ராமரை வணங்கிய மாருதி அனுமன், 'பிரபுவே! பிறவிப் பெருங்கடலை எளிதில் கடக்கும் மோட்ச உபாயம் யாது?' என்று கேட்டார்.",
        "Sri Rama smiled with boundless grace: 'Listen, O Maruti! My true form is pure Vedanta; through the crown of the four Vedas—the 108 Upanishads—the soul realizes its eternity.'",
        "ஸ்ரீ ராமர் கருணையுடன் புன்னகைத்து அருளினார்: 'மாருதி! வேதாந்தத்தில் நிலைபெற்றதே எனது நிஜ சொரூபம்; நான்கு வேதங்களின் மணிமுடியான 108 உபநிஷதங்களாலேயே ஆன்மா விடுதலை பெறுகிறது.'",
        "Just as a bird cannot fly with a single wing, true liberation requires two wings working together: Vasanakshaya (eradicating vasanas) and Manonasha (dissolution of the restless mind).",
        "பறவை ஒற்றைச் சிறகால் பறக்க முடியாதது போல, ஜீவன்முக்திக்கு வாசனாட்சயம் (ஆசைகளின் அழிவு), மனோநாசம் (மன ஒடுக்கம்) மற்றும் தத்துவ ஞானம் ஆகியவை ஒருங்கே தேவை.",
        "Rama declared the supreme secret: 'For the ripe seeker, the Mandukya Upanishad alone is enough to grant liberation! If not, study the 10, the 32, or all 108.'",
        "ஸ்ரீ ராமர் பரம ரகசியத்தை முழங்கினார்: 'முதிர்ந்த சாதகனுக்கு மாண்டூக்ய உபநிஷதம் ஒன்றே முக்தி அளிக்கப் போதுமானது! இல்லையேல் 10, 32 அல்லது 108 உபநிஷதங்களையும் தியானிப்பாயாக.'",
        "Dividing the 108 jewels across Rig, Shukla Yajur, Krishna Yajur, Sama, and Atharva Vedas with their Shanti Mantras, Rama illuminated the royal road to non-dual peace.",
        "ரிக், சுக்ல யஜுர், கிருஷ்ண யஜுர், சாம, அதர்வண வேதங்களில் 108 உபநிஷதங்களையும் சாந்தி மந்திரங்களுடன் வகைப்படுத்தி, அத்வைத சாந்தியின் ராஜபாட்டையை ராமர் காட்டினார்.",
        "When the lamp of inquiry extinguishes ego-desire, the mind ceases to agitate like a windless flame, even while living and acting in the world.",
        "ஆன்ம விசாரம் எனும் தீபத்தால் அகங்கார வாசனைகள் அழியும்போது, காற்றில்லாத இடத்து தீபம் போல் மனம் அடங்கி ஜீவன்முக்தி சித்திக்கிறது.",
        "Receiving Sri Rama's blessing in his heart, Hanuman shone with immortal Brahma-Vidya, guarding this 108-Upanishad treasure for all humanity.",
        "ஸ்ரீ ராமரின் உபதேசத்தை இதயத்தில் ஏற்ற ஆஞ்சநேயர், சிரஞ்சீவியாக பிரம்ம வித்தையில் ஒளிர்ந்து, 108 உபநிஷதப் புதையலை உலகிற்குக் காத்தருள்கிறார்."
    ),
    make_extra(
        "extra_02_bashkala", 109, "Bashkala Mantropanishad", "बाष्कलमन्त्रोपनिषद्", "பாஷ்கல மந்த்ரோபநிஷதம்", "Rig Veda",
        "Indra & Young Medhatithi: Carried to the Heavens by the Ram Who Is the All-Pervading Self",
        "இந்திரனும் இளம் மேதாதிதியும்: ஆட்டுக்கிடாய் வடிவில் விண்ணிற்கு ஏற்றிப் பிரம்ம ஞானம் அருளிய கதை",
        "Young Rishi Medhatithi (Kanva's son) & Lord Indra (as the Golden Ram / Supreme Atman)",
        "अहमेकः प्रथमं आसं वर्तामि च भविष्यामि च नान्यः कश्चिन्मत्तो व्यतिरिक्तः ।",
        "அஹமேக: ப்ரதமம் ஆஸம் வர்த்தாமி ச பவிஷ்யாமி ச நான்ய: கஸ்சின்மத்தோ வ்யதிரிக்த: |",
        "I alone existed in the beginning, I alone exist now, and I alone shall be! There is nothing whatsoever separate from Me, the Infinite Self.",
        "ஆதியில் நான் ஒருவனே இருந்தேன்; இப்போதும் இருக்கிறேன்; இனியும் இருப்பேன்! என்னைத் தவிர வேறொரு பொருள் இவ்வுலகில் சிறிதும் இல்லை.",
        "Rigvedic Upanishadic parable (mentioned in Rigveda 1.51.1 / Shankara's Brahmasutra Bhashya): Indra carries young Medhatithi aloft as a ram and reveals that the Lord of Thunder is none other than the fearless, all-pervading Brahman.",
        "Vedic Soma-sacrifice meadow rising into a luminous celestial chariot highway above golden storm clouds",
        "At a sacred Soma sacrifice, young Medhatithi—son of Sage Kanva—was pouring offerings when a mysterious golden ram suddenly appeared and carried him into the sky!",
        "புனிதமான சோம யாக சாலையில் கண்வ முனிவரின் புதல்வரான இளம் மேதாதிதி தவம் இயற்றியபோது, பொன்மயமான மேஷம் (ஆட்டுக்கிடாய்) ஒன்று தோன்றி அவரை விண்ணிற்குத் தூக்கிச் சென்றது!",
        "Yet Medhatithi, anchored in Vedic tapas, felt no terror; gazing into the dazzling eyes of his abductor, he asked: 'Who art thou behind this wondrous disguise?'",
        "தपोவலிமை மிக்க மேதாதிதி சிறிதும் அஞ்சாமல், தன்னைச் சுமந்து செல்லும் அந்த விந்தை உருவத்தின் ஒளிமயமான கண்களை நோக்கி, 'இவ்வுருவில் வந்திருக்கும் நீ யார்?' என்று கேட்டார்.",
        "Dropping the form of the ram, the figure blazed forth like a thousand suns as Indra, Lord of the Heavens, smiling at the boy's fearless inquiry.",
        "மாய ஆட்டுக்கிடாய் உருவம் மறைந்து, ஆயிரம் சூரியன்களின் பிரகாசத்துடன் தேவேந்திரன் தன் சுயரூபத்தில் தோன்றி, இளைஞனின் அச்சமற்ற கேள்வியைக் கண்டு புன்னகைத்தான்.",
        "Indra proclaimed the Bashkala roar of non-duality: 'Know Me not as a limited sky-god! I am the One Self who existed before creation, who breathes in every creature!'",
        "இந்திரன் பாஷ்கல அத்வைத முழக்கத்தை அருளினான்: 'என்னை வெறும் விண்ணுலகத் தேவனாக மட்டும் நினையாதே! படைப்பிற்கு முன்பும், எல்லா உயிர்களின் மூச்சாகவும் இருக்கும் ஏக ஆன்மாவே நான்!'",
        "He who drinks the Soma of inner awareness realizes that thunder, sun, wind, sacrifice, and the seeker's own heart are woven from a single ocean of Consciousness.",
        "அக விழிப்புணர்வு எனும் சோம ரசத்தைப் பருகுபவன், இடியும், சூரியனும், காற்றும், யாகமும், தன் சொந்த இதயமும் ஒரே பிரக்ஞைப் பெருங்கடலின் அலைகளே என்பதை உணர்கிறான்.",
        "Medhatithi saw that the journey from earth to heaven was an awakening from bodily limitation into the boundless expanse of Atman.",
        "மண்ணிலிருந்து விண்ணிற்குச் சென்ற அந்தப் பயணம், உடல் எனும் குறுகிய எல்லையிலிருந்து ஆன்மாவின் எல்லையற்ற விரிவிற்குள் நிகழ்ந்த விழிப்பே என்பதை மேதாதிதி உணர்ந்தார்.",
        "Returning to the earth illumined with twenty-five mantras of self-sovereignty, Medhatithi shone free from fear and death.",
        "இருபத்தைந்து மந்திரங்களின் ஆன்ம ஞானத்துடன் பூமிக்குத் திரும்பிய மேதாதிதி, மரண பயம் நீங்கிப் பிரம்ம ஞானியாகப் பிரகாசித்தார்."
    ),
    make_extra(
        "extra_03_chagleya", 110, "Chagleya Upanishad", "छागलेयोपनिषद्", "சாகலேய உபநிஷதம்", "Rig Veda",
        "The Sages at Kurukshetra & The Iron Cart: Why a Corpse Cannot Move Without the Soul-Driver",
        "குருக்ஷேத்திர முனிவர்களும் இரும்பு வண்டியும்: ஆன்ம சாரதி இல்லாமல் உடல் ஏன் இயங்குவதில்லை?",
        "The Sages of Kurukshetra, Sage Chagala (Kavasha Ailusha) & the Parable of the Highway Chariot",
        "यथा रथः सारथिना विना न चेष्टते तथा शरीरं प्रज्ञात्मना विना लोष्टवच्चेष्टते न कदाचन ।",
        "யதா ரத: ஸாரதினா வினா ந சேஷ்டதே ததா சரீரம் ப்ரக்ஞாத்மனா வினா லோஷ்டவச்சேஷ்டதே ந கதாசன |",
        "Just as a chariot cannot move a single inch without its charioteer, so too this physical body without the Conscious Self lies inert like a clod of earth!",
        "சாரதி இல்லாத தேர் எவ்வாறு ஓர் அங்குலம் கூட நகராதோ, அவ்வாறே பிரக்ஞை வடிவான ஆன்மா பிரிந்தபின் இவ்வுடல் மண்ணாங்கட்டி போலச் செயலற்றுக் கிடக்கிறது!",
        "Vivid Upanishadic drishtanta (parable): The body is merely a creaking iron-and-wood cart; it is the invisible Pratyag-Atman (Conscious Charioteer) that gives it sight, speech, and motion.",
        "Sacred Sarasvati-Kurukshetra riverside hermitage and an ancient dusty royal highway with an unyoked wooden chariot",
        "Proud of their ritual learning, the sages of Kurukshetra looked down upon the silent sage Chagala—until they asked: 'By whose power does this body speak, walk, and breathe?'",
        "குருக்ஷேத்திரத்தில் கூடிய முனிவர்கள் தங்கள் சடங்குக் கல்வியால் கர்வம் கொண்டிருந்தனர்; மௌன முனிவரான சாகலரிடம், 'இந்த உடல் எதனால் பேசுகிறது, நடக்கிறது, மூச்சு விடுகிறது?' என்று கேட்டனர்.",
        "Sage Chagala led them to the great highway by the Sarasvati river and pointed to a lifeless corpse lying beside a deserted wooden cart.",
        "சாகல முனிவர் அவர்களை சரஸ்வதி நதிக்கரை நெடுஞ்சாலைக்கு அழைத்துச் சென்று, அங்கே கேட்பாரற்றுக் கிடந்த ஒரு சடலத்தையும், சாரதி இல்லாத வண்டியையும் சுட்டிக்காட்டினார்.",
        "He asked: 'Look upon this body! It still has two eyes, two ears, hands, feet, and veins—why does it not rise when called, or flee when dogs approach?'",
        "அவர் கேட்டார்: 'இதோ பாருங்கள்! இந்த உடலிலும் இரண்டு கண்கள், காதுகள், கைகள், கால்கள் அப்படியே உள்ளனவே—அழைத்தால் ஏன் எழுவதில்லை? விலங்குகள் நெருங்கினால் ஏன் ஓடுவதில்லை?'",
        "Just as a heavy cart made of wood and iron screeches and rolls only while a living driver guides the reins, this body moves only while the Conscious Self (Prajnatman) abides within!",
        "மரத்தாலும் இரும்பாலும் செய்யப்பட்ட வண்டி, சாரதி ஒருவன் கடிவாளத்தைப் பிடித்து ஓட்டும் வரை மட்டுமே ஓடும்; அதுபோலப் பிரக்ஞை ஆன்மா உள்ளே இருக்கும் வரையில்தான் இவ்வுடல் இயங்குகிறது!",
        "The moment the unseen Charioteer steps down from the vehicle, relatives weep around a mere log of flesh and bone that cannot hear a word.",
        "கண்ணுக்குத் தெரியாத அந்த ஆன்ம சாரதி வண்டியிலிருந்து இறங்கிய கணமே, உறவினர்கள் கதறி அழுதாலும் கேட்காத வெறும் கட்டை போல உடல் சாய்ந்துவிடுகிறது.",
        "Hearing this piercing parable, the proud scholars bowed low in humility, realizing they had worshiped the cart while forgetting the Driver.",
        "உள்ளத்தைத் துளைக்கும் இந்த உவமையைக் கேட்ட பண்டிதர்கள் கர்வம் அழிந்து தலைவணங்கினர்; வண்டியைப் போற்றிச் சாரதியை மறந்த தங்கள் அறியாமையை உணர்ந்தனர்.",
        "Turning their gaze from the perishable chariot to the immortal Charioteer within, they attained the fearless light of the Self.",
        "அழியும் உடல் எனும் தேரிலிருந்து பார்வையைத் திருப்பி, உள்ளே உறையும் அழியாத ஆன்ம சாரதியைத் தரிசித்து அவர்கள் பிறவாப் பெருநிலை எய்தினர்."
    ),
    make_extra(
        "extra_04_arsheya", 111, "Arsheya Upanishad", "आर्षेयोपनिषद्", "ஆர்ஷேய உபநிஷதம்", "Sama Veda",
        "The Council of Five Great Rishis: Vishvamitra, Jamadagni, Bharadvaja, Gautama & Vasishtha on Brahman",
        "ஐம்பெரும் மகரிஷிகளின் திருச்சபை: விஸ்வாமித்திரர் முதல் வசிஷ்டர் வரை கண்ட அகண்ட பிரம்ம தரிசனம்",
        "Maharishis Vishvamitra, Jamadagni, Bharadvaja, Gautama & Vasishtha",
        "य एषोऽन्तरादित्ये हिरण्मयः पुरुषो दृश्यते य एषोऽन्तर्हृदयेऽणोरणीयान् महतो महीयान् स आत्मा तत्सत्यं तद्ब्रह्म ।",
        "ய ஏஷோந்தராதித்யே ஹிரண்மய: புருஷோ த்ருஸ்யதே ய ஏஷோந்தர்ஹ்ருதயே அனோரணீயான் மஹதோ மஹீயான் ஸ ஆத்மா தத்ஸத்யம் தத்ப்ரஹ்ம |",
        "That Golden Person seen within the Sun and within the cave of the heart—smaller than the smallest, greater than the greatest—He is the Self, He is Truth, He is Brahman!",
        "சூரிய மண்டலத்தின் உள்ளேயும் இதயக் குகையிலும் காணப்படும் பொன்மயமான புருஷன்—அணுவிற்கும் அணுவாய், அகண்டத்திற்கும் அகண்டமாய் விளங்கும் அவனே ஆன்மா, அவனே சத்திய பிரம்மம்!",
        "Philosophical dialogue (Samvada) of the five Sapta-Rishi patriarchs progressing from cosmic space, lightning, and prana to Vasishtha's non-dual realization of the Self-Luminous Atman.",
        "Grand forest convocation under ancient deodar trees ringed by five sacred fire altars and golden sunbeams",
        "Once, five great Vedic Rishis—Vishvamitra, Jamadagni, Bharadvaja, Gautama, and Vasishtha—gathered in a sacred assembly to inquire: 'What is the ultimate Reality (Brahman)?'",
        "ஒருமுறை விஸ்வாமித்திரர், ஜமதக்னி, பரத்வாஜர், கௌதமர், வசிஷ்டர் ஆகிய ஐம்பெரும் மகரிஷிகள் ஒன்றுகூடி, 'பரம்பொருளான பிரம்மம் எது?' என்று ஆராயத் தொடங்கினர்.",
        "Vishvamitra spoke first: 'Brahman is this vast expanse of Space between heaven and earth!'—yet Jamadagni pointed out that space itself is bounded and supported by a deeper cause.",
        "விஸ்வாமித்திரர் முதலில் கூறினார்: 'மண்ணிற்கும் விண்ணிற்கும் இடையே விரிந்துள்ள இந்த ஆகாயமே பிரம்மம்!' ஆனால் ஜமதக்னியோ, அதற்குள்ளும் ஒரு நுட்பமான ஆதாரம் உண்டு என்றார்.",
        "Bharadvaja praised the blazing lightning in the clouds, and Gautama extolled the thunderous roar of Prana; yet each realized that outer phenomena appear and vanish.",
        "பரத்வாஜர் மேகத்தில் மின்னும் மின்னலையும், கௌதமர் பிராணனின் இடி முழக்கத்தையும் பிரம்மம் என்றனர்; ஆயினும் புறத் தோற்றங்கள் அனைத்தும் தோன்றி மறையக்கூடியவையே என உணர்ந்தனர்.",
        "Then all four turned with folded hands to Maharishi Vasishtha, asking him to reveal that Supreme Reality which knows no boundary or decay.",
        "அப்போது நால்வரும் வசிஷ்ட மகரிஷியை நோக்கி இரு கரம் கூப்பி, எல்லையும் அழிவும் இல்லாத அந்தப் பரம சத்தியத்தை உபதேசிக்குமாறு வேண்டினர்.",
        "Vasishtha declared: 'That which shines within the Sun and within the lotus of your own heart—smaller than an atom, vaster than the cosmos—is the One Atman!'",
        "வசிஷ்டர் அருளினார்: 'வெளியே சூரியனிலும், உள்ளே உங்கள் இதயத் தாமரையிலும் ஒளிரும் அந்தப் பேரொளி—அணுவிலும் சிறியதாய், அண்டத்திலும் பெரியதாய் விளங்கும் அதுவே ஆன்மா!'",
        "It cannot be grasped by the eye or speech, yet by its light the eye sees, the mind thinks, and the five elements dance in harmony.",
        "கண்ணாலோ வாக்காலோ அதைப் பற்ற முடியாது; ஆனால் அதன் ஒளியாலேயே கண் காண்கிறது, மனம் சிந்திக்கிறது, பஞ்ச பூதங்களும் இயங்குகின்றன.",
        "Hearing Vasishtha's lion-roar of non-dual wisdom, the five Rishis merged into silent meditation, beholding the Self shining everywhere.",
        "வசிஷ்டரின் அத்வைத ஞான முழக்கத்தைக் கேட்ட ஐம்பெரும் முனிவர்களும் ஆழ்ந்த மௌன தியானத்தில் ஆழ்ந்து, எங்கும் நிறைந்த ஆன்ம ஒளியைத் தரிசித்தனர்."
    ),
    make_extra(
        "extra_05_shaunaka", 112, "Shaunaka Upanishad", "शौनकोपनिषद्", "சௌனக உபநிஷதம்", "Atharva Veda",
        "The Devas, the Asuras & the Invincible Shield of Om: How Indra and the Vasus Conquered Death",
        "தேவாசுரப் போரும் ஓங்காரக் கவசமும்: இந்திரனும் வசுக்களும் பிரணவத்தால் மரணத்தை வென்ற கதை",
        "Maharishi Shaunaka, Lord Indra, the Eight Vasus, the Rudras, Adityas & the Cosmic Pranava (Om)",
        "प्रणवो धनुः शरो ह्यात्मा ब्रह्म तल्लक्ष्यमुच्यते । ओमित्येकाक्षरं ब्रह्म देवानां परमा गतिः ॥",
        "ப்ரணவோ தனு: சரோ ஹ்யாத்மா ப்ரஹ்ம தல்லக்ஷ்யமுச்யதே | ஓமித்யேகாக்ஷரம் ப்ரஹ்ம தேவானாம் பரமா கதி: ||",
        "Pranava is the bow, the Self is the arrow, and Brahman is the supreme target! The single syllable Om is the invincible refuge of the Devas.",
        "பிரணவமே வில், ஆன்மாவே அம்பு, பிரம்மமே இலக்கு! 'ஓம்' எனும் ஓரெழுத்துப் பிரம்மமே தேவர்களின் வெல்ல முடியாத பரம புகலிடமாகும்.",
        "Atharvavedic esoteric mystery of the syllable Om (Pranava) during the cosmic sacrifice: when the Devas invoke Omkara at the head of every Vedic metre (Gayatri, Trishtubh, Jagati), darkness and Asuric ego cannot touch them.",
        "Celestial Vedic Soma-Yajna pavilion where golden syllables of Gayatri, Trishtubh, and Jagati fuse into a blazing shield of Omkara light",
        "When the Devas and Asuras contended for mastery over the worlds, the Devas performed a great Vedic sacrifice—yet the forces of darkness threatened to disrupt their offering.",
        "தேவர்களும் அசுரர்களும் உலக ஆதிக்கத்திற்காகப் போட்டியிட்டபோது, தேவர்கள் மாபெரும் வேள்வி இயற்றினர்; ஆனால் இருளின் சக்திகள் அந்த வேள்வியைத் தடுக்க முயன்றன.",
        "Indra and the eight Vasus approached the ancient seer Shaunaka and asked: 'By what invincible power can our morning, midday, and evening offerings become immortal?'",
        "இந்திரனும் எட்டு வசுக்களும் சௌனக முனிவரை அணுகி, 'எந்த வெல்ல முடியாத சக்தியால் எங்கள் காலை, நண்பகல், மாலை வேள்விகள் அமரத்துவம் பெறும்?' என்று கேட்டனர்.",
        "Shaunaka revealed the secret of the Sovereign Syllable: 'Place the immortal Pranava (Om) as the crown of every breath, every metre, and every offering!'",
        "சௌனகர் ஓரெழுத்து மந்திரத்தின் ரகசியத்தை உரைத்தார்: 'ஒவ்வொரு மூச்சின் முகப்பிலும், ஒவ்வொரு வேத சந்தஸ்ஸிலும் அழியாத பிரணவத்தை (ஓம்) மணிமுடியாக நிறுத்துங்கள்!'",
        "Taking refuge in Om, the Vasus invoked the Gayatri metre at dawn, the Rudras invoked the Trishtubh at noon, and the Adityas invoked the Jagati at sunset.",
        "ஓங்காரத்தைத் துணையாகக் கொண்டு, வசுக்கள் காலையில் காயத்ரி சந்தஸ்ஸையும், ருத்ரர்கள் நண்பகலில் த்ரிஷ்டுப்பையும், ஆதித்யர்கள் மாலையில் ஜகதி சந்தஸ்ஸையும் இயக்கினர்.",
        "As the resonant roar of 'Om' vibrated through the three worlds, the Asuras—who represent fragmented ego and selfish desire—were shattered like darkness before lightning!",
        "மூவுலகங்களிலும் 'ஓம்' எனும் பிரணவ நாதம் அதிர்ந்தபோது, சிதறிய அகங்காரத்தின் வடிவான அசுர சக்திகள் மின்னல் முன் இருள் போல் சிதறி ஓடின!",
        "For Om is both the four-quartered Brahman and the vital breath (Prana) inside the body; whoever chants it with awareness wears an armor no sorrow can pierce.",
        "ஏனெனில் ஓங்காரமே நான்கு பாதங்கள் கொண்ட பிரம்மமும் உடலின் பிராணனும் ஆகும்; விழிப்புணர்வுடன் அதை உச்சரிப்பவன் துன்பம் துளைக்க முடியாத கவசத்தை அணிகிறான்.",
        "Victorious through the Pranava, the Devas and the awakened seeker abide in the fearless immortality of the Self.",
        "பிரணவ சக்தியால் வெற்றி பெற்ற தேவர்களும் சாதகனும், மரணமற்ற ஆன்மாவின் அச்சமற்ற பேரின்பத்தில் நிலைபெறுகின்றனர்."
    ),
    make_extra(
        "extra_06_pranava", 113, "Pranava Upanishad", "प्रणवोपनिषद्", "பிரணவ உபநிஷதம்", "Atharva Veda",
        "Creator Brahma on the Golden Lotus: How One Syllable 'Om' Birthed the Cosmos",
        "பொற்றாமரையில் பிரம்மதேவர்: 'ஓம்' எனும் ஓரெழுத்திலிருந்து பிரபஞ்சம் உதித்த தவம்",
        "Creator Lord Brahma (Svayambhu) & Maharishi Atharvan on the Cosmic Golden Lotus",
        "ओमित्येतदक्षरमिदं सर्वं तस्योपव्याख्यानं भूतं भवद्भविष्यदिति सर्वमोंकार एव ।",
        "ஓமித்யேததக்ஷரமிதம் ஸர்வம் தஸ்யோபவ்யாக்யானம் பூதம் பவத்பவிஷ்யதிதி ஸர்வமோங்கார ஏவ |",
        "Om—this imperishable syllable is all this universe! Past, present, and future—all is Omkara alone, and whatever transcends the three times is also Om.",
        "ஓம் எனும் இந்த அழியாத அட்சரமே இப்பிரபஞ்சம் அனைத்தும்! இறந்தகாலம், நிகழ்காலம், எதிர்காலம் மற்றும் முக்காலத்தையும் கடந்த பரம்பொருள் அனைத்தும் ஓங்காரமே.",
        "Drawn from the Gopatha Brahmana of the Atharva Veda: Brahma meditates upon the single syllable Om on the cosmic lotus, discovering within its letters (A-U-M and Ardhamatra) the Vedas, worlds, elements, and states of consciousness.",
        "Infinite cosmic ocean where Creator Brahma sits upon a thousand-petaled golden lotus as radiant Sanskrit letters of A-U-M form galaxies",
        "At the dawn of creation, Lord Brahma found himself seated upon a luminous golden lotus rising from the primordial waters, wondering: 'By what single seed can I weave the universe?'",
        "படைப்பின் வைகறையில், ஆதி சமுத்திரத்திலிருந்து எழுந்த பொற்றாமரை மீது அமர்ந்திருந்த பிரம்மதேவர், 'எந்த ஒற்றை வித்தினால் இப்பிரபஞ்சத்தை நான் நெய்யப் போகிறேன்?' என்று சிந்தித்தார்.",
        "Closing his four pairs of eyes in deep tapas, Brahma heard the unstruck cosmic vibration resounding from the heart of the Infinite: 'OM!'",
        "நான்கு முகங்களையும் ஒருமுகப்படுத்தி ஆழ்ந்த தவத்தில் ஆழ்ந்த பிரம்மதேவர், எல்லையற்ற வெளியின் இதயத்திலிருந்து எழும் அனாஹத நாதத்தைக் கேட்டார்: 'ஓம்!'",
        "Contemplating the first letter 'A' (Akara), he beheld the Earth, Rigveda, Agni, the waking state, and the power of creation unfolding in red-gold radiance.",
        "முதல் எழுத்தான 'அ'காரத்தைத் தியானித்தபோது, பூமி, ரிக் வேதம், அக்னி, விழிப்பு நிலை மற்றும் படைப்புச் சக்தி ஆகியவை செம்பொன் ஒளியுடன் விரிவதைக் கண்டார்.",
        "Contemplating the second letter 'U' (Ukara), he beheld the Atmosphere, Yajurveda, Vayu, the dream state, and Vishnu's sustaining grace shining like lightning.",
        "இரண்டாம் எழுத்தான 'உ'காரத்தைத் தியானித்தபோது, அந்தரिक्षம், யஜுர் வேதம், வாயு, கனவு நிலை மற்றும் காக்கும் சக்தி ஆகியவை மின்னல் போல் ஒளிர்வதைக் கண்டார்.",
        "Contemplating the third letter 'M' (Makara), he beheld the Heavens, Samaveda, Surya, deep sleep, and Rudra's dissolving peace.",
        "மூன்றாம் எழுத்தான 'ம'காரத்தைத் தியானித்தபோது, சுவர்க்கம், சாம வேதம், சூரியன், ஆழ்உறக்கம் மற்றும் ஒடுக்கும் ருத்ர சக்தி ஆகியவற்றைத் தரிசித்தார்.",
        "And in the silent half-measure (Ardhamatra) beyond sound, Brahma discovered the Atharvaveda and the pure, changeless Turiya Atman.",
        "ஒலிக்கு அப்பாற்பட்ட மௌனமான அர்த்தமாத்திரையில், அதர்வண வேதத்தையும் மாறுபாடற்ற தூய துரிய ஆன்மாவையும் பிரம்மதேவர் கண்டுணர்ந்தார்.",
        "Whoever meditates upon this Pranava with every breath unites with the Creator's own Consciousness and transcends birth and death.",
        "ஒவ்வொரு மூச்சிலும் இந்தப் பிரணவ ரகசியத்தை உணர்ந்து தியானிப்பவன், படைப்பின் மூலப் பேரறிவுடன் ஒன்றிப் பிறப்பு இறப்பைக் கடக்கிறான்."
    ),
    make_extra(
        "extra_07_shivasankalpa", 114, "Shiva Sankalpa Upanishad", "शिवसंकल्पोपनिषद्", "சிவசங்கல்ப உபநிஷதம்", "Shukla Yajur Veda",
        "The Light of Lights That Travels Far: Mastering the Restless Mind Through Auspicious Resolve",
        "தொலைதூரம் பாயும் ஒளிகளின் ஒளி: சஞ்சல மனதைச் சிவசங்கல்பத்தால் வெல்லும் ரகசியம்",
        "Vedic Rishi Yajnavalkya / Kaundinya & A Seeker Struggling with a Restless Mind",
        "यज्जाग्रतो दूरमुदैति दैवं तदु सुप्तस्य तथैवेति दूरंगमं ज्योतिषां ज्योतिरेकं तन्मे मनः शिवसंकल्पमस्तु ॥",
        "யஜ்ஜாக்ரதோ தூரமுதைதி தைவம் தது ஸுப்தஸ்ய ததைவேதி தூரங்கமம் ஜ்யோதிஷாம் ஜ்யோதிரேகம் தன்மே மன: சிவஸங்கல்பமஸ்து ||",
        "That divine Mind which travels far when waking and returns in deep sleep—the one Light of all lights—may that Mind of mine be filled with auspicious Shiva-resolve!",
        "விழிப்பிலும் கனவிலும் தொலைதூரம் பாய்ந்து செல்வதும், ஆழ்உறக்கத்தில் ஒடுங்குவதும், ஒளிகளுக்கெல்லாம் ஒளியானதுமான என் மனம் மங்களகரமான சிவசங்கல்பம் உடையதாகட்டும்!",
        "The famous Vedic hymn of the Mind (Rigveda Khila / Shukla Yajurveda Ch. 34 expanded as Upanishad): harnessing the mind—the fastest charioteer and inner immortal flame—by anchoring every thought in Shiva (the Auspicious Non-Dual Good).",
        "Twilight Himalayan peak above a river of stars where a yogi's glowing mind-lotus transforms chaotic storm-winds into a serene golden Rudra-jyoti",
        "A troubled seeker cried out to his Guru: 'Master, my body sits still in the ashram, yet my mind leaps across a thousand leagues in a split second! How can I ever find peace?'",
        "மனம் அலைக்கழிந்த சாதகன் ஒருவன் குருவிடம் கதறினான்: 'குருவே! என் உடல் ஆசிரமத்தில் அமர்ந்திருக்கிறது; ஆனால் என் மனமோ ஒரு நொடியில் ஆயிரம் காத தூரம் பாய்கிறதே! நான் எவ்வாறு அமைதி பெறுவேன்?'",
        "The Rishi answered with a gentle smile: 'Fight not the mind with hatred! Recognize its divine majesty—for the Mind is the far-traveling Light of all sensory lights (Jyotisham Jyotih).'",
        "ரிஷி கனிவுடன் புன்னகைத்து அருளினார்: 'மனதை வெறுப்பால் எதிர்க்காதே! அதன் தெய்வீக மகிமையை உணர்வாயாக—ஏனெனில் ஐம்பொறி ஒளிகளுக்கெல்லாம் ஒளியாகத் திகழ்வது இந்த மனமே!'",
        "Like a skilled charioteer who controls swift horses with firm reins, the awakened mind guides human action; within it are strung the Rig, Sama, and Yajur Vedas like spokes in a wheel-hub.",
        "வேகமான குதிரைகளைக் கடிவாளத்தால் நடத்தும் தேர்ப்பாகனைப் போல, பக்குவப்பட்ட மனமே மனிதனை வழிநடத்துகிறது; தேர்ச்சக்கரத்தின் குடத்தில் ஆரக்கால்கள் போல் வேதங்கள் அனைத்தும் மனதிலேயே கோக்கப்பட்டுள்ளன.",
        "Within the heart shines an immortal flame smaller than a thumb; without that conscious mind-light, no ritual can be performed and no wisdom can be known.",
        "இதயத்தின் உள்ளே அணையாத் தீபமாக சுடர்விடும் அந்த உள்-ஒளி இல்லாமல், எந்த யாகமும் நிகழாது, எந்த ஞானமும் புலப்படாது.",
        "When the mind wanders toward greed, anger, and duality, it binds the soul; when that very mind turns toward Shiva (the Auspicious Truth), it becomes the doorway to Moksha!",
        "அந்த மனம் ஆசையிலும் கோபத்திலும் செல்லும்போது பந்தத்திற்குக் காரணமாகிறது; அதே மனம் சிவசங்கல்பத்தில் (மங்களப் பரம்பொருளில்) திரும்பும்போது மோட்சத்தின் வாசலாகிறது!",
        "With every breath the seeker affirms the immortal prayer: 'Tan me manah shivasankalpam astu—May my mind rest in the auspicious resolve of Shiva-Consciousness!'",
        "ஒவ்வொரு மூச்சிலும் சாதகன் உறுதிபூணுகிறான்: 'தன் மே மன: சிவசங்கல்பமஸ்து—என் மனம் எப்போதும் சிவமயமான மங்களச் சிந்தனையில் நிலைபெறட்டும்!'",
        "Bathed in that Shiva-Sankalpa, the restless wind of thought subsides into the boundless ocean of non-dual peace.",
        "அந்தச் சிவசங்கல்ப ஒளியில் நனையும்போது, அலைபாயும் எண்ணக் காற்று அடங்கி அத்வைத சாந்தி சமுத்திரமாக மனம் மாறுகிறது."
    ),
    make_extra(
        "extra_08_svasamvedya", 115, "Svasamvedya Upanishad", "स्वसंवेद्योपनिषद्", "ஸ்வஸம்வேத்ய உபநிஷதம்", "Atharva Veda",
        "Beyond Time, Space, and Words: The Radical Roar of Self-Validating Consciousness",
        "காலமும் இடமும் சொற்களும் கடந்த நிலை: தன்னால் தானே அறியப்படும் சுயம்பிரகாசப் பேரறிவு",
        "An Avadhuta Jivanmukta Sage & A Scholarly Seeker Burdened by Endless Scriptures",
        "न कालो न दिशो नात्मा न चान्यदपि किंचन । स्वसंवेद्यं परं तत्त्वं तदेवाहमिति स्थितिः ॥",
        "ந காலோ ந திசோ நாத்மா ந சான்யதபி கிஞ்சன | ஸ்வஸம்வேத்யம் பரம் தத்த்வம் ததேவாஹமிதி ஸ்திதி: ||",
        "There is neither time nor space, neither bondage nor liberation, nor anything other! Self-validating Supreme Consciousness alone shines—and abiding as That is the Truth.",
        "காலமும் இல்லை, திசைகளும் இல்லை, பந்தமும் இல்லை, முக்தியும் இல்லை! தன்னால் தானே அறியப்படும் சுயம்பிரகாசப் பரம்பொருள் ஒன்றே உள்ளது—அதுவே நான் எனும் நிலையே சத்தியம்.",
        "Radical Ajativada / Paramarthika Advaita: deconstructing all conceptual dualities (teacher/taught, pramana/prameya, time/space) to leave only Svasamvedya—Self-Luminous Awareness that requires no second light to know itself.",
        "Infinite mirror-like Himalayan high-altitude salt-flat at dawn where sky and earth merge into seamless golden-white radiance",
        "Carrying bundles of palm-leaf treatises on logic and debate, a weary scholar asked an Avadhuta sage: 'By what proof (Pramana) can I finally prove and see Brahman?'",
        "தர்க்க சாஸ்திர ஓலைச்சுவடிகளைச் சுமந்து களைத்த பண்டிதன் ஒருவன் அவதூத முனிவரிடம் கேட்டான்: 'எந்தப் பிரமாணத்தால் (ஆதாரத்தால்) நான் பிரம்மத்தை நிரூபித்துத் தரிசிக்க முடியும்?'",
        "The Avadhuta laughed like thunder in a clear sky: 'Do you carry a clay lamp at noon to prove that the blazing Sun exists?'",
        "தெளிந்த வானத்து இடி போல் அவதூதர் சிரித்தார்: 'நண்பகலில் கொளுத்தும் சூரியன் இருக்கிறதா என்று பார்க்க யாராவது அகல் விளக்கை ஏற்றித் தேடுவார்களா?'",
        "In supreme truth, there is no time, no space, no east or west, no teacher, no student, no ignorance, and no scripture—for all divisions are painted upon Consciousness!",
        "பரமார்த்திக சத்தியத்தில் காலமும் இல்லை, இடமும் இல்லை, திசைகளும் இல்லை, குருவும் இல்லை, சீடனும் இல்லை—இவை அனைத்தும் பிரக்ஞையின் மீது வரையப்பட்ட கற்பனைக் கோடுகளே!",
        "Words cannot reach That from which all words borrow their life; just as a dumb man tasting sweet sugarcane juice needs no debate to know its sweetness, Consciousness is Svasamvedya (Self-known)!",
        "கரும்புச் சாற்றைச் சுவைத்த ஊமை தன் அனுபவத்தைச் சொற்களால் விவரிக்க முடியாவிட்டாலும் அச்சுவை எவ்வாறு உண்மையோ, அவ்வாறே பிரம்ம அனுபவமும் தன்னால் தானே அறியப்படுவது (ஸ்வஸம்வேத்யம்)!",
        "The scholar dropped his heavy bundles of pride, realizing that the seeker searching for Brahman was already the very Light doing the searching.",
        "பிரம்மத்தைத் தேடிக்கொண்டிருந்த தானே அந்தத் தேடலுக்கு ஆதாரமான பேரொளி என்பதை உணர்ந்த பண்டிதன், தன் சாஸ்திரக் கர்வத்தை நழுவவிட்டான்.",
        "When the illusion of 'knowledge' and 'ignorance' cancels itself out like fire burning camphor, no trace of ego remains.",
        "கற்பூரத்தை எரித்த நெருப்பு தானும் மறைவது போல, அறியாமையை நீக்கிய அறிவும் அந்த அகண்ட மௌனத்தில் கரைந்து போகிறது.",
        "Resting in unshakeable Sahaja silence, the sage abides as Svasamvedya—the One Light that shines by itself forever.",
        "அசைக்க முடியாத சகஜ மௌனத்தில் நிலைத்து, தன்னால் தானே ஒளிரும் ஸ்வஸம்வேத்யப் பேரொளியாக ஞானி விளங்குகிறான்."
    ),
    make_extra(
        "extra_09_atmapuja", 116, "Atmapuja Upanishad", "आत्मपूजोपनिषद्", "ஆத்மபூஜா உபநிஷதம்", "Atharva Veda",
        "Where Sleep Is Samadhi and Walking Is Pradakshina: The Living Worship of the Self",
        "உறக்கமே சமாதி, நடையே பிரதட்சிணம்: வாழ்வின் ஒவ்வொரு நொடியும் ஆத்ம பூஜை ஆகும் வித்தை",
        "Jagadguru Adi Shankaracharya / Upanishadic Sage & A Devotee Seeking Unbroken Worship",
        "तस्य निश्चलज्ञानं ध्यानम् । सर्वविषयनिराशा पाद्यम् । निरन्तरं चिन्तनमर्चनम् । निद्रा समाधिः ।",
        "தஸ்ய நிஸ்சலக்ஞானம் த்யானம் | ஸர்வவிஷயநிராசா பாத்யம் | நிரந்தரம் சிந்தனமர்ச்சனம் | நித்ரா ஸமாதி: |",
        "Unwavering awareness is Dhyana; detachment from sense-craving is the foot-offering; unbroken remembrance is Archana; and deep sleep itself becomes Samadhi!",
        "அசையாத விழிப்புணர்வே தியானம்; பற்றற்ற தன்மையே பாத பூஜை; இடைவிடாத ஆன்ம சிந்தனையே அர்ச்சனை; ஆழ்ந்த உறக்கமே சமாதி!",
        "Transforming all seventeen steps of traditional temple Puja (Avahana, Asana, Snana, Dhupa, Dipa, Naivedya, Pradakshina, Namaskara) into continuous non-dual self-awareness in daily life.",
        "Serene Chola temple courtyard merging seamlessly into a meditator's glowing inner heart-sanctum",
        "A devoted householder asked his Guru: 'Master, my hands can offer flowers at the altar for only an hour a day—how can I worship the Lord without interruption?'",
        "பக்தியுள்ள இல்லறத்தான் ஒருவன் குருவிடம் கேட்டான்: 'குருவே! என் கைகளால் ஒரு நாளைக்கு ஒரு மணி நேரம் மட்டுமே பூக்களால் அர்ச்சனை செய்ய முடிகிறது—இடைவிடாமல் இறைவனைப் பூஜிப்பது எப்படி?'",
        "The Master revealed the radiant secret of Atma-Puja: 'When you recognize the Self within as the living Deity, every breath and action of your life becomes temple worship!'",
        "குரு ஆத்ம பூஜையின் ஒளிமயமான ரகசியத்தை அருளினார்: 'உன்னுள்ளே உறையும் ஆன்மாவையே மூலவராக உணரும்போது, உன் வாழ்வின் ஒவ்வொரு மூச்சும் செயலும் ஆலய வழிபாடாக மாறுகிறது!'",
        "Steadfast mindfulness is Dhyana; letting go of selfish craving washes the Lord's feet (Padya); and bathing the mind in pure Chidakasha is the sacred Abhisheka!",
        "அசையாத விழிப்புணர்வே தியானம்; பேராசையை விடுவதே இறைவனின் திருவடி விளக்கும் பாத்யம்; சிதாகாசத்தில் மனதை நனைப்பதே புனித அபிஷேகம்!",
        "Burning away residual vasanas is the fragrant incense (Dhupa); the self-luminous Witness is the temple lamp (Dipa); and contentment with nectar-peace is the Naivedya offering.",
        "வாசனைகளை எரிப்பதே நறுமணத் தூபம்; சுயம்பிரகாச சாட்சி உணர்வே மங்கள தீபம்; மனநிறைவு எனும் அமிர்தமே இறைவனுக்குப் படைக்கும் நைவேத்தியம்.",
        "Every step you walk upon the earth becomes circumambulation (Pradakshina); every spoken word becomes Mantra; and resting the body in sleep becomes Nirvikalpa Samadhi!",
        "மண்ணில் நீ நடக்கும் ஒவ்வொரு அடியும் பிரதட்சிணம்; பேசும் ஒவ்வொரு சொல்லும் மந்திர ஜபம்; இரவில் கொள்ளும் உறக்கமே நிர்விகல்ப சமாதி!",
        "Even silence becomes the highest praise when the ego bows into the oneness of 'So-ham—I am He'.",
        "'ஸோஹம்—அவனே நான்' எனும் ஒருமையில் அகங்காரம் கரையும்போது, ஆழ்ந்த மௌனமே மிக உயர்ந்த தோத்திரப் பாடலாகிறது.",
        "Practicing this effortless Atma-Puja day and night, the seeker turns the entire universe into a sanctum of liberation.",
        "இரவும் பகலும் இந்த இயல்பான ஆத்ம பூஜையில் திளைக்கும் சாதகனுக்கு, இப்பிரபஞ்சம் முழுவதுமே முக்தி அளிக்கும் கருவறையாக மாறுகிறது."
    ),
    make_extra(
        "extra_10_advaitabhavana", 117, "Advaita Bhavana Upanishad", "अद्वैतभावनोपनिषद्", "அத்வைத பாவனா உபநிஷதம்", "Atharva Veda",
        "Unbroken Non-Dual Vision & Arutperunjothi: Beholding the One Light of Grace in Every Atom",
        "அத்வைத பாவனையும் அருட்பெருஞ்ஜோதியும்: அணுவிலும் அகண்டத்திலும் ஒன்றே எனக் காணும் பேரறிவு",
        "Upanishadic Siddha Master, Vallalar Ramalinga Adigal Lineage & Awakened Seeker",
        "सर्वं खल्विदं ब्रह्म नेह नानास्ति किंचन । अखण्डैकरसज्योतिः शिवोहमद्वितीयकः ॥",
        "ஸர்வம் கல்விதம் ப்ரஹ்ம நேஹ நானாஸ்தி கிஞ்சன | அகண்டைகரஸஜ்யோதி: சிவோஹமத்விதீயக: ||",
        "All this universe is verily Brahman; there is no multiplicity here whatsoever! I am that indivisible, one-flavored Light of Grace (Arutperunjothi Shiva) without a second.",
        "இப்பிரபஞ்சம் அனைத்தும் பிரம்மமே; இங்குப் பிரிவு என்பதே சிறிதும் இல்லை! இரண்டற்ற அகண்ட ஏகரச அருட்பெருஞ்ஜோதிச் சிவனே நான்.",
        "Crowning synthesis of Upanishadic Advaita Bhavana with the Tamil Siddha and Sanmarga realization of Arutperunjothi (Supreme Light of Compassionate Grace): where Jiva-Karunya (compassion to all living beings) flows naturally from seeing the One Self in all.",
        "Radiant white-gold Hall of Wisdom (Gnana Sabhai) merging with an ancient Himalayan and Tamil temple sanctum as seven veils part before the Jyoti",
        "A seeker who had mastered dry philosophy asked the Siddha Master: 'I repeat that Brahman is One, yet why does my heart still feel separate from suffering creatures?'",
        "ஏட்டுச் சுரைக்காயாக வேதாந்தம் பயின்ற சாதகன் ஒருவன் சித்த குருவிடம் கேட்டான்: 'பிரம்மம் ஒன்றே என்று நான் வாயால் சொல்கிறேன்; ஆயினும் பிற உயிர்களின் துயரம் கண்டு என் இதயம் ஏன் இன்னும் பிரிந்து நிற்கிறது?'",
        "The Master pointed to a blazing lamp behind seven colored curtains: 'Because your knowledge is only on the tongue! True Advaita Bhavana dawns when the seven veils of ego-maya part to reveal the One Light of Grace!'",
        "ஏழு வண்ணத் திரைகளுக்குப் பின்னால் சுடர்விடும் ஜோதியைக் காட்டி குரு அருளினார்: 'உன் அறிவு நாவில் மட்டுமே உள்ளது! அகங்கார மாயையின் ஏழு திரைகளும் விலகும்போதுதான் அருட்பெருஞ்ஜோதியின் உண்மையான அத்வைத பாவனை உதிக்கும்!'",
        "As the dark, blue, green, red, golden, white, and mixed curtains of ignorance dissolved one by one, the seeker beheld the indivisible Jyoti pulsating inside every blade of grass and every beating heart.",
        "கறுப்பு, நீலம், பச்சை, சிவப்பு, பொன்மை, வெண்மை, கலப்பு எனும் அறியாமைத் திரைகள் ஒன்றன் பின் ஒன்றாக விலக, ஒவ்வொரு புல்லிலும் ஒவ்வொரு உயிரின் இதயத்திலும் ஒரே ஜோதி துடிப்பதைச் சாதகன் கண்டான்.",
        "Where there is true Non-Duality (Advaita), boundless compassion (Jiva-Karunya) flows automatically—for how can one hand strike the other when both belong to the same body?",
        "உண்மையான அத்வைத பாவனை உதிக்குமிடத்தில் ஜீவகாருண்யம் தானாகவே ஊற்றெடுக்கும்—ஏனெனில் ஒரே உடலின் ஒரு கையை மற்றொரு கை எவ்வாறு காயப்படுத்தும்?",
        "Space within the atom and space across galaxies are one; the light in the eye and the Light of Supreme Grace (Arutperunjothi) are indivisible!",
        "அணுவிற்குள் இருக்கும் வெளியும் அண்ட வெளியும் ஒன்றே; கண்ணின் ஒளியும் தனிப்பெரும் கருணை அருட்பெருஞ்ஜோதியும் பிரிக்க முடியாத ஒன்றே!",
        "Meditating continuously in this Advaita Bhavana, the boundaries between 'inside' and 'outside', 'mine' and 'thine', melt like salt dolls in the ocean of bliss.",
        "இந்த இடைவிடாத அத்வைத பாவனையில் திளைக்கும்போது, 'உள்ளே-வெளியே', 'நான்-நீ' எனும் எல்லைகள் ஆனந்தக் கடலில் உப்புப் பொம்மை போல் கரைகின்றன.",
        "Shining with deathless wisdom and universal love, the Siddha-Jivanmukta walks the world as a living lamp of Supreme Grace.",
        "மரணமிலாப் பெருவாழ்வும் எல்லா உயிர்களிடத்தும் அன்பும் கொண்டு, அருட்பெருஞ்ஜோதியின் வாழும் தீபமாக அந்த ஞானி உலகில் வலம் வருகிறான்."
    ),
    make_extra(
        "extra_11_narayaniya", 118, "Narayaniya (Yajnyiki) Upanishad", "नारायणीयोपनिषद् (याज्ञिकी)", "நாராயணீய (யாக்ஞிகீ) உபநிஷதம்", "Krishna Yajur Veda",
        "The Enlightened Seer's Breath as Eternal Agnihotra: Where Every Meal Is a Cosmic Sacrifice",
        "ஞானியின் மூச்சே நித்திய அக்னிஹோத்ரம்: உண்ணும் உணவும் வாழும் வாழ்வும் மகா வேள்வியாகும் ரகசியம்",
        "Maharishi Narayana, Vedic Seers of Taittiriya Aranyaka & A Self-RealizedVidvan",
        "तस्यैवं विदुषो यज्ञस्यात्मा यजमानः श्रद्धा पत्नी शरीरमिध्ममुरो वेदिर्लोमानि बर्हिर्वेदाः शिखा हृदयं यूपः ।",
        "தஸ்யைவம் விதுஷோ யக்ஞஸ்யாத்மா யஜமான: ச்ரத்தா பத்னீ சரீரமித்மமுரோ வேதிர்லோமானி பர்ஹிர்வேதா: சிகா ஹ்ருதயம் யூப: |",
        "For the enlightened knower, his own Self is the sacrificer, unwavering Faith is his consort, his body is the sacred fuel, his chest is the altar, and his heart is the sacrificial post!",
        "ஆன்ம ஞானம் பெற்ற வித்வானுக்கு, அவனது ஆன்மாவே எஜமானன், சிரத்தையே பத்தினி, உடலே சமித்து, மார்பே வேதிகை, இதயமே யாகசாலைத் தூண் ஆகும்!",
        "Culminating teaching of the Taittiriya Aranyaka (Book 10 / Mahanarayana-Yajnyiki Upanishad): the life of an illumined knower of Brahman is itself the supreme Sattra sacrifice, requiring no external ritual fire.",
        "Golden Vedic Taittiriya forest hermitage at sunset where a sage's glowing prana-fires illuminate the five Koshas",
        "When the Vedic seers asked how one who has transcended external ritual continues to honor the cosmic law, Maharishi Narayana revealed the Yajnyiki mystery of the Living Sacrifice.",
        "புற யாக சடங்குகளைக் கடந்த பிரம்ம ஞானி எவ்வாறு பிரபஞ்ச தர்மத்தைப் போற்றுகிறான் என்று முனிவர்கள் கேட்டபோது, மகரிஷி நாராயணர் 'வாழும் வேள்வி'யின் ரகசியத்தை அருளினார்.",
        "For the knower of Brahman (Vidvan), his entire existence becomes a continuous Vedic Yajna! His own inner Atman is the Yajamana (Sacrificer), and pure Shraddha (Faith) is his sacred consort.",
        "பிரம்ம வித்தையை உணர்ந்த ஞானியின் வாழ்க்கை முழுவதுமே ஒரு நித்திய வேள்வியாகிறது! அவனது ஆன்மாவே எஜமானன்; அசைக்க முடியாத சிரத்தையே அவனது தர்ம பத்தினி.",
        "His physical body is the sacred firewood, his chest is the Vedi altar, his heart is the golden sacrificial post, and his calm mind is the clarify-butter oblation.",
        "அவனது உடலே புனித சமித்து, மார்பே யாக வேதிகை, இதயமே பொன்மயமான யூபத் தூண், அமைதியான மனமே நெய் ஆஹுதி!",
        "Speech is the Hotri priest, vital breath (Prana) is the Udgatri singer, the eye is the Adhvaryu minister, and understanding is the Brahman supervisor.",
        "வாக்கே மந்திரம் ஓதும் ஹோத்ரு, பிராணனே சாம கானம் பாடும் உத்காத்ரு, கண்ணே அத்வர்யு, பேரறிவே வேள்வியைக் காக்கும் பிரம்மா.",
        "When he eats, he offers the five Prana-oblations into the gastric fire of Vaishvanara; his waking hours are the morning savana, and his deep peace is the evening completion.",
        "அவன் உண்ணும் ஒவ்வொரு கவளமும் வைஸ்வானர அக்னியில் இடப்படும் பிராண ஆஹுதி; அவனது பகல் பொழுதே காலை வேள்வி, அமைதியான இரவே மாலை வேள்வி.",
        "Truth, austerity, self-restraint, non-violence, and charity are his royal Dakshina gifts, and the moment of bodily death is merely the final ceremonial bath (Avabhritha Snana)!",
        "சத்தியம், தவம், புலனடக்கம், அகிம்சை, ஈகை ஆகியவையே தட்சிணை; உடலின் மரணமோ வேள்வியின் முடிவில் நிகழும் புனித நீராடல் (அவப்ருத ஸ்நானம்) மட்டுமே!",
        "Knowing this Narayaniya secret, the sage shines in the supreme sky of the heart, one with Narayana forever.",
        "இந்த நாராயணீய வேள்வி ரகசியத்தை உணர்ந்த ஞானி, இதய ஆகாயத்தில் நாராயணனுடன் இரண்டறக் கலந்து என்றும் ஒளிர்கிறான்."
    ),
    make_extra(
        "extra_12_heramba", 119, "Heramba Upanishad", "हेरम्बोपनिषद्", "ஹேரம்ப உபநிஷதம்", "Atharva Veda",
        "Parvati & Shiva on Kailash: The Fearless Five-Faced Lion-Mounted Heramba Ganapati",
        "கைலாயத்தில் பார்வதியும் சிவனும்: அபயமளிக்கும் சிம்ம வாகனப் பஞ்சமுக ஹேரம்ப கணபதி",
        "Goddess Parvati (Girija), Bhagavan Sadashiva & Five-Faced Lion-Mounted Heramba Ganapati",
        "दीनानाथैकशरणं पञ्चवक्त्रं सिंहवाहनं हेरम्बं प्रणमाम्यहं सर्वविघ्नप्रणाशनम् ।",
        "தீனானாதைகசரணம் பஞ்சவக்த்ரம் ஸிம்ஹவாஹனம் ஹேரம்பம் ப்ரணமாம்யஹம் ஸர்வவிக்னப்ரணாசனம் |",
        "I bow to Heramba Ganapati—the sole refuge of the humble and helpless, five-faced, riding the mighty Lion of Dharma, destroyer of all inner and outer obstacles!",
        "எளியவர்களின் ஒரே புகலிடமும், ஐந்து திருமுகங்கள் கொண்டவரும், தர்ம சிம்ம வாகனத்தில் பவனி வருபவரும், சகல வighனங்களையும் அழிப்பவருமான ஹேரம்ப கணபதியை வணங்குகிறேன்!",
        "Esoteric Ganapatya-Advaita Upanishad taught by Shiva to Parvati on Kailash: revealing the etymology of HE-RAM-BA (He = helpless seekers, Ram = protector/rejoicer, Ba = liberator into Brahman) and His five-faced cosmic form.",
        "Snow-crowned Mount Kailash glowing with golden sunrise as Five-Faced Heramba Ganapati appears upon a majestic white-gold Lion",
        "Seated upon the silver peak of Mount Kailash, Goddess Girija (Parvati) asked Lord Shiva: 'O Maheshvara, reveal to me the secret of Heramba Ganapati, who grants instant fearlessness to the humble!'",
        "வெள்ளிப் பனிமலையான கைலாய சிகரத்தில் வீற்றிருந்த பார்வதி தேவி சிவபெருமானிடம், 'மகேஸ்வரா! எளியவர்களுக்கும் சரணடைந்தவர்களுக்கும் உடனே அபயமளிக்கும் ஹேரம்ப கணபதியின் ரகசியத்தை அருளுங்கள்!' என்று கேட்டாள்.",
        "Lord Shiva smiled with tender reverence: 'Listen, O Devi! Even before I burned the Three Cities (Tripura), I meditated upon this supreme Heramba Tatva.'",
        "சிவபெருமான் வாஞ்சையுடன் அருளினார்: 'தேவி கேள்! முப்புரங்களை நான் எரிக்கும் முன்பும் கூட, இந்தப் பரம ஹேரம்ப தத்துவத்தையே தியானித்து வெற்றி பெற்றேன்.'",
        "Why is He called HERAMBA? 'HE' signifies the humble, afflicted Jivas caught in samsara; 'RAM' signifies the compassionate Protector who uplifts them; and 'BA' signifies Brahman, their eternal home!",
        "அவருக்கு ஏன் 'ஹேரம்பர்' என்ற திருநாமம் வந்தது? 'ஹே' என்பது பிறவிக் கடலில் தவிக்கும் எளிய உயிர்களைக் குறிக்கும்; 'ரம்' என்பது அவர்களைக் காக்கும் கருணையைக் குறிக்கும்; 'ப' என்பது பிரம்ம சொரூபத்தைக் குறிக்கும்!",
        "Mounted upon his mother's fearless Lion of Dharma, Heramba shines with five radiant faces—representing the पांचഭूत (five elements) and five Koshas—and ten arms holding the noose, goad, sweet modaka, and Abhaya mudra.",
        "அன்னையின் தர்ம சிம்ம வாகனத்தில் அமர்ந்து, பஞ்ச பூதங்களையும் குறிக்கும் ஐந்து திருமுகங்களுடனும், பாசம், அங்குசம், மோதகம், அபய வரத முத்திரை தாங்கிய பத்துக் கரங்களுடனும் ஹேரம்பர் ஜொலிக்கிறார்.",
        "When fear, grief, or spiritual doubt surrounds a seeker like a dark forest, remembering the Heramba Mantra splits the clouds of ego in an instant.",
        "பயமும் துயரமும் ஆன்மிக ஐயமும் இருண்ட காடு போல் சாதகனைச் சூழும்போது, ஹேரம்ப மந்திரத்தின் ஸ்மரணை கணப்பொழுதில் அகங்கார மேகங்களைப் பிளக்கிறது.",
        "In the Muladhara and Sahasrara alike, He is the Lord of Prana and the sweet Modaka of pure Bliss (Ananda).",
        "மூலாதாரத்திலும் சஹஸ்ராரத்திலும் பிராணனின் நாயகனாகவும், தூய சிவானந்த மோதகத்தை அருள்பவராகவும் அவரே வீற்றிருக்கிறார்.",
        "Blessed by Shiva and Parvati's revelation, whoever meditates on Heramba Ganapati becomes fearless, compassionate, and liberated in the Self.",
        "சிவ-பார்வதி அருளிய இந்த ஹேரம்ப உபநிஷதத்தைத் தியானிப்பவன், சகல பயங்களும் நீங்கிப் பூரண ஆன்ம விடுதலையை அடைகிறான்."
    )
]


SHANTI_BY_VEDA = {
    "Rig Veda": (
        "ॐ वाङ्मे मनसि प्रतिष्ठिता मनो मे वाचि प्रतिष्ठितमाविरावीर्म एधि ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "ஓம் வாங்மே மனஸி ப்ரதிஷ்டிதா மனோ மே வாசி ப்ரதிஷ்டிதமாவிராவீர்ம ஏதி || ஓம் சாந்தி: சாந்தி: சாந்தி: ||",
        "May my speech be established in my mind, and my mind be established in my speech; O Self-Luminous Brahman, reveal Thyself to me!"
    ),
    "Shukla Yajur Veda": (
        "ॐ पूर्णमदः पूर्णमिदं पूर्णात्पूर्णमुदच्यते । पूर्णस्य पूर्णमादाय पूर्णमेवावशिष्यते ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "ஓம் பூர்ணமத: பூர்ணமிதம் பூர்ணாத் பூர்ணமுதச்யதே | பூர்ணஸ்ய பூர்ணமாதாய பூர்ணமேவாவசிஷ்யதே || ஓம் சாந்தி: சாந்தி: சாந்தி: ||",
        "That Supreme Brahman is Whole, and this visible universe is Whole; from the Whole comes forth the Whole, and the Whole alone remains!"
    ),
    "Krishna Yajur Veda": (
        "ॐ सह नाववतु । सह नौ भुनक्तु । सह वीर्यं करवावहै । तेजस्वि नावधीतमस्तु मा विद्विषावहै ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "ஓம் ஸஹ நாவவது | ஸஹ நௌ புனக்து | ஸஹ வீர்யம் கரவாவஹை | தேஜஸ்வி நாவதீதமஸ்து மா வித்விஷாவஹை || ஓம் சாந்தி: சாந்தி: சாந்தி: ||",
        "May the Supreme Lord protect us both (Guru and Disciple); may He nourish us both; may our study be radiant with illumination, and may we never harbor disharmony!"
    ),
    "Sama Veda": (
        "ॐ आप्यायन्तु ममाङ्गानि वाक्प्राणश्चक्षुः श्रोत्रमथो बलमिन्द्रियाणि च सर्वाणि । सर्वं ब्रह्मौपनिषदं माऽहं ब्रह्म निराकुर्यां मा मा ब्रह्म निराकरोदनिराकरणमस्त्वनिराकरणं मेऽस्तु ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "ஓம் ஆப்யாயந்து மமாங்கானி வாக்ப்ராணஸ்சக்ஷு: ச்ரோத்ரமதோ பலமிந்த்ரியாணி ச ஸர்வாணி | ஸர்வம் ப்ரஹ்மௌபநிஷதம் மாஹம் ப்ரஹ்ம நிராகுர்யாம் || ஓம் சாந்தி: சாந்தி: சாந்தி: ||",
        "May my limbs, speech, vital breath, eye, ear, strength, and all senses grow vigorous; all is the Brahman of the Upanishads—may I never deny Brahman, and may Brahman never abandon me!"
    ),
    "Atharva Veda": (
        "ॐ भद्रं कर्णेभिः शृणुयाम देवा भद्रं पश्येमाक्षभिर्यजत्राः । स्थिरैरङ्गैस्तुष्टुवांसस्तनूभिर्व्यशेम देवहितं यदायुः ॥ ॐ शान्तिः शान्तिः शान्तिः ॥",
        "ஓம் பத்ரம் கர்ணேபி: ச்ருணுயாம தேவா பத்ரம் பஸ்யேமாக்ஷபிர்யஜத்ரா: | ஸ்திரைரங்கைஸ்துஷ்டுவாம்ஸஸ்தனூபிர்வ்யசேம தேவஹிதம் யதாயு: || ஓம் சாந்தி: சாந்தி: சாந்தி: ||",
        "O Devas, may we hear with our ears what is auspicious; may we behold with our eyes what is sacred and noble; with firm limbs and illumined hearts may we fulfill our divine life-span in peace!"
    ),
}

TIME_WINDOWS = [
    ("00:00 - 00:45", "00:00"),
    ("00:45 - 01:30", "00:45"),
    ("01:30 - 02:15", "01:30"),
    ("02:15 - 03:00", "02:15"),
    ("03:00 - 03:45", "03:00"),
    ("03:45 - 04:30", "03:45"),
    ("04:30 - 05:15", "04:30"),
]


def render_markdown(item: dict) -> str:
    uid = item["id"]
    mnum = item["muktika_num"]
    mnum_str = f"#{mnum:03d}"
    name_en = item["name_en"]
    name_sa = item["name_sa"]
    name_ta = item["name_ta"]
    veda = item["veda"]
    cat = item["category"]
    story_en = item["story_title_en"]
    story_ta = item["story_title_ta"]
    chars = item["characters"]
    sloka_sa = item["sloka_sa"]
    sloka_ta = item["sloka_ta"]
    mean_en = item["sloka_meaning_en"]
    mean_ta = item["sloka_meaning_ta"]
    theme = item["theme"]
    setting = item["visual_setting"]
    scenes = item["scenes"]

    shanti_sa, shanti_ta, shanti_en = SHANTI_BY_VEDA.get(
        veda, SHANTI_BY_VEDA["Atharva Veda"]
    )
    canon_note = (
        f"`{mnum_str}` (of 108 Muktika Canon Upanishads)"
        if mnum <= 108
        else f"`{mnum_str}` (Extra-Canonical Upanishad beyond Muktika 108)"
    )

    lines = [
        f"# {uid.upper()} — {name_en} ({mnum_str})",
        f"## {story_en}",
        f"### {story_ta}",
        "",
        "---",
        "",
        "## 1. Header & Canonical Metadata",
        "",
        f"- **Story ID**: `{uid}`",
        f"- **Canon Number**: {canon_note}",
        f"- **Upanishad Name (Sanskrit)**: {name_sa}",
        f"- **Upanishad Name (Tamil)**: {name_ta}",
        f"- **Upanishad Name (English)**: {name_en}",
        f"- **Associated Veda**: {veda}",
        f"- **Canonical Category**: `{cat}`",
        f"- **Story / Parable Title (English)**: {story_en}",
        f"- **Story / Parable Title (Tamil)**: {story_ta}",
        f"- **Key Characters / Sages / Deities**: {chars}",
        "",
        "### Core Mahavakya / Upanishadic Verse",
        "- **Authentic Sanskrit Sloka**:",
        f"  > **{sloka_sa}**",
        "- **Tamil Transliteration**:",
        f"  > *{sloka_ta}*",
        f"- **English Meaning**: {mean_en}",
        f"- **Tamil Meaning (தமிழ் பொருள்)**: {mean_ta}",
        "",
        "### Vedic Shanti Mantra",
        f"- **Sanskrit**: `{shanti_sa}`",
        f"- **Tamil**: `{shanti_ta}`",
        f"- **Meaning**: {shanti_en}",
        "",
        "### Philosophical & Moral Theme",
        f"{theme}",
        "",
        "### YouTube 16:9 Long-Form Metadata Block",
        f"- **16:9 Title (Tamil)**: `{name_ta} | {story_ta} | {mnum_str} | Guru Kula Desam`",
        f"- **16:9 Title (English)**: `{name_en} ({mnum_str}): {story_en} | 16:9 4K Vedanta Story | Guru Kula Desam`",
        f"- **Opening Hook (Tamil)**: {scenes[0]['vo_ta']}",
        f"- **Opening Hook (English)**: {scenes[0]['vo_en']}",
        "",
        "```text",
        f"{name_ta} ({name_en} - {mnum_str})",
        f"{story_ta} | {story_en}",
        "",
        "00:00 - Scene 1: " + scenes[0]["title"],
        "00:45 - Scene 2: " + scenes[1]["title"],
        "01:30 - Scene 3: " + scenes[2]["title"],
        "02:15 - Scene 4: " + scenes[3]["title"],
        "03:00 - Scene 5: " + scenes[4]["title"],
        "03:45 - Scene 6: " + scenes[5]["title"],
        "04:30 - Scene 7: " + scenes[6]["title"],
        "",
        "🔔 Subscribe to @guru-kula-desam for authentic 108 Upanishads, Thirukkural & South Indian Devotional Master Films.",
        "#Upanishads #GuruKulaDesam #Vedanta #TamilSpiritual #Mahavakya #SanatanaDharma",
        "```",
        "",
        "---",
        "",
        "## 2. Locked Visual Continuity Bible (16:9 8K 24fps)",
        "",
        "- **Aspect Ratio & Cinema Spec**: 16:9 Widescreen | 8K Photorealistic | 24fps Cinema Master (Arri Alexa 65 Prime Lens Aesthetic)",
        f"- **Story-Specific Sacred Setting**: {setting}",
        f"- **Key Characters / Iconography**: {chars}",
        "- **Lighting & Color Palette**: Golden Brahmamuhurtham sunrise rays, warm sacred Agnihotra & Sri Chakra homa firelight, brass oil lamps (Thoopam & Dheepam), and ethereal cosmic starlight during Aparoksha Anubhuti sequences.",
        "- **Hard Negative Exclusions**: NO modern clothing, NO eyeglasses, NO wristwatches, NO electric lights, NO plastic or synthetic materials, NO printed paper books, NO on-screen text, NO burned-in subtitles, NO watermarks, NO decorative borders in the raw AI video generation.",
        "- **8-Layer Compositing Compatibility**: Compatible with Guru Kula Desam v6.0 8-Layer 1080p/4K Pipeline.",
        "",
        "---",
        "",
        "## 3. Full 7-Scene Detailed Screenplay Breakdown (00:00 – 05:15)",
        "",
    ]

    for idx, sc in enumerate(scenes):
        tw, _ = TIME_WINDOWS[idx]
        snum = sc["scene_num"]
        lines.extend([
            f"### Scene {snum} ({tw}): {sc['title']}",
            "",
            f"- **Scene ID**: `{uid.upper()}_S0{snum}`",
            f"- **Duration Window**: `{tw}` (45 seconds)",
            f"- **Camera & Cinematography**: {sc['camera']}",
            "- **Google Flow / Veo 16:9 Video Generation Prompt**:",
            f"  > `{sc['flow_prompt']}`",
            "- **Voiceover / Narration Script (English)**:",
            f"  > {sc['vo_en']}",
            "- **Voiceover / Narration Script (Tamil - தமிழ் உரை)**:",
            f"  > {sc['vo_ta']}",
            f"- **Synchronized Subtitle Cue**: `{sc['subtitle_cue']}`",
            f"- **Sound & Music Design Cue**: `{sc['sound_cue']}`",
            "",
        ])

    return "\n".join(lines)


def generate_all():
    base_dir = Path("/home/shishyan/GitHub/GuruKulaDesam")
    shakta_dir = base_dir / "production" / "upanishad_stories" / "07_shakta_upanishads"
    extra_dir = base_dir / "production" / "upanishad_stories" / "08_extra_canonical_upanishads"
    json_path = base_dir / "data" / "upanishads" / "agent5_shakta_extra.json"

    shakta_dir.mkdir(parents=True, exist_ok=True)
    extra_dir.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    written_files = []

    for idx, item in enumerate(SHAKTA_LIST, start=1):
        fname = f"{idx:02d}_muktika_{item['muktika_num']:03d}_{item['id']}.md"
        fpath = shakta_dir / fname
        fpath.write_text(render_markdown(item), encoding="utf-8")
        written_files.append(str(fpath))

    for idx, item in enumerate(EXTRA_LIST, start=1):
        fname = f"{idx:02d}_muktika_{item['muktika_num']:03d}_{item['id']}.md"
        fpath = extra_dir / fname
        fpath.write_text(render_markdown(item), encoding="utf-8")
        written_files.append(str(fpath))

    payload = {
        "agent": "Agent 5: Shakta (8 Canon) & Extra-Canonical (12 Texts) Upanishads",
        "total_count": len(SHAKTA_LIST) + len(EXTRA_LIST),
        "shakta_count": len(SHAKTA_LIST),
        "extra_canonical_count": len(EXTRA_LIST),
        "shakta_upanishads": SHAKTA_LIST,
        "extra_canonical_upanishads": EXTRA_LIST,
        "all_upanishads": SHAKTA_LIST + EXTRA_LIST,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(written_files)} Markdown files and saved JSON to {json_path}")
    for wf in written_files:
        print(f"  - {wf}")


if __name__ == "__main__":
    generate_all()
