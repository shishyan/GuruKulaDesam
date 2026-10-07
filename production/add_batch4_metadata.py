# -*- coding: utf-8 -*-
"""
Adds rich, canonical metadata for Batch 4 (Chapters 60, 62, 65, 66, 67, 74)
Dynamic Enterprise & Heroic Action Suite
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "production" / "metadata" / "thirukkural_releases_metadata.json"

BATCH4_META = [
    {
        "chapter_number": 60,
        "tamil_title": "அதிகாரம் 60 - ஊக்கமுடைமை",
        "transliterated_title": "Ookkamudaimai",
        "thematic_english_title": "Energy, Zeal & Unyielding Determination",
        "canonical_youtube_title": "அதிகாரம் 60 - ஊக்கமுடைமை | Ookkamudaimai - Energy & Resolve | Guru Kula Desam",
        "track_id": "XN5ENUbmSOE",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் (Royalty & Active Enterprise)",
        "kural_range": "591 - 600",
        "key_kurals": [
            {
                "number": 595,
                "tamil": "வெள்ளத் தனைய மலர்நீட்டம் மாந்தர்தம்\nஉள்ளத் தனைய துயர்வு.",
                "english": "The stalk of the water lily grows with the depth of water; even so does the stature of a human rise with the greatness of their mind's resolve."
            },
            {
                "number": 596,
                "tamil": "உள்ளுவ தெல்லாம் உயர்வுள்ளல் மற்றது\nதள்ளினும் தள்ளாமை நீர்த்து.",
                "english": "Let all your aspirations be lofty; even if thwarted by circumstances, that nobility of spirit is an achievement in itself."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 60: ஊக்கமுடைமை (Ookkamudaimai) — உள்ளத்தில் எழும் தளராத ஊக்கமும், வினையாற்றும் ஆற்றலுமே ஒரு மனிதனின் அழியாத உண்மையான செல்வம் என்பதை உலகிற்கு உணர்த்தும் அதிகாரம்.\n\n'வெள்ளத் தனைய மலர்நீட்டம் மாந்தர்தம்\nஉள்ளத் தனைய துயர்வு.' (குறள் 595)\n\n'உள்ளுவ தெல்லாம் உயர்வுள்ளல் மற்றது\nதள்ளினும் தள்ளாமை நீர்த்து.' (குறள் 596)\n\nநீரின் ஆழத்திற்கு ஏற்ப தாமரை மலரின் தண்டு உயர்ந்து மலர்வது போல, ஒரு மனிதனின் உள்ளத்து ஊக்கத்தின் அளவுக்கு ஏற்ப அவன் வாழ்வில் உயர்வடைவான். ஊக்கம் இல்லாதவன் மரம் போன்றவனே. எண்ணுவதெல்லாம் உயர்வாகவே எண்ண வேண்டும்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) கம்பீர இன்னிசையில், 50 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 60: Ookkamudaimai (Energy, Zeal & Unyielding Determination) from Thirukkural by Thiruvalluvar.\n\n'The lotus stalk lengthens according to the depth of the water; so too does human greatness rise in proportion to the depth of one\\'s inner resolution.' (Kural 595)\n\nValluvar declares that true possession is the possession of relentless inner energy; material riches come and go like shifting sands. Even when an elephant is pierced with arrows, it stands unyielding—so must a noble soul remain steadfast against adversity.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, paired with 50 photorealistic visual artworks under dynamic rain and thunder atmospheric blend.",
            "timestamps": [
                {"time": "00:00", "label": "ஊக்கமே உண்மையான உடைமை - குறள் 591 (Possessing Energy as True Wealth)"},
                {"time": "01:15", "label": "ஆக்கம் அதர்வினாய்ச் செல்லும் - குறள் 594 (Fortune Seeks the Energetic)"},
                {"time": "02:20", "label": "வெள்ளத் தனைய மலர்நீட்டம் - குறள் 595 (The Stature of Lofty Soul)"},
                {"time": "03:40", "label": "உள்ளுவ தெல்லாம் உயர்வுள்ளல் - குறள் 596 (Aspire Ever for the Highest)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 60 - ஊக்கமுடைமை (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=XN5ENUbmSOE",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#ஊக்கமுடைமை", "#Thirukkural", "#Ookkamudaimai", "#Energy", "#Determination", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 62,
        "tamil_title": "அதிகாரம் 62 - ஆள்வினையுடைமை",
        "transliterated_title": "Aalvinaiyudaimai",
        "thematic_english_title": "Industrious Enterprise & Defeating Fate",
        "canonical_youtube_title": "அதிகாரம் 62 - ஆள்வினையுடைமை | Aalvinaiyudaimai - Manly Effort | Guru Kula Desam",
        "track_id": "zj4_pEqa_cs",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் / குடிசெயல்வகை (Self-Effort & Action)",
        "kural_range": "611 - 620",
        "key_kurals": [
            {
                "number": 619,
                "tamil": "தெய்வத்தான் ஆகா தெனினும் முயற்சிதன்\nமெய்வருத்தக் கூலி தரும்.",
                "english": "Though divine fate itself should deny success, unyielding labor will surely yield the rightful reward equal to bodily exertion."
            },
            {
                "number": 620,
                "tamil": "ஊழையும் உப்பக்கம் காண்பர் உலைவின்றித்\nதாழாது உஞற்று பவர்.",
                "english": "Those who strive without faltering or despair will see even stubborn adverse destiny turn its back and retreat."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 62: ஆள்வினையுடைமை (Aalvinaiyudaimai) — மனிதனின் அயராத உழைப்பும் முயற்சியும் விதியையும் வெல்லும் ஆற்றல் படைத்தது என்பதைப் பறைசாற்றும் உன்னத அதிகாரம்.\n\n'தெய்வத்தான் ஆகா தெனினும் முயற்சிதன்\nமெய்வருத்தக் கூலி தரும்.' (குறள் 619)\n\n'ஊழையும் உப்பக்கம் காண்பர் உலைவின்றித்\nதாழாது உஞற்று பவர்.' (குறள் 620)\n\nவிதியால் முடியாது என்று கைவிடப்பட்டாலும், உடலை வருத்திச் செய்யும் கடும் முயற்சி அதற்கான பலனைத் தந்தே தீரும். சோர்வின்றித் தொடர்ந்து முயல்பவர்கள் ஊழையும் (விதியையும்) புறமுதுகிட்டு ஓடச் செய்வர்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) கம்பீர இன்னிசையில், 47 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 62: Aalvinaiyudaimai (Industrious Enterprise & Overcoming Fate) from Thirukkural by Thiruvalluvar.\n\n'Even if the gods say it cannot be, hard bodily toil will never fail to yield its rightful fruit.' (Kural 619)\n\n'Those who labor untiringly and undaunted will conquer even adverse destiny itself.' (Kural 620)\n\nValluvar presents one of world literature's most soaring anthems to human agency, industrious labor, and the indomitable power of work over fatalism. Where sloth invites ruin, purposeful sweat constructs prosperity and eternal dignity.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, paired with 47 photorealistic visual artworks under refreshing drizzle atmosphere.",
            "timestamps": [
                {"time": "00:00", "label": "அருமை உடைத்தென் றசாவாமை - குறள் 611 (Never Despair at Difficulty)"},
                {"time": "01:10", "label": "முயற்சி திருவினை ஆக்கும் - குறள் 616 (Effort Yields Abundance)"},
                {"time": "02:15", "label": "தெய்வத்தான் ஆகா தெனினும் - குறள் 619 (Labor Rewards Bodily Toil)"},
                {"time": "03:30", "label": "ஊழையும் உப்பக்கம் காண்பர் - குறள் 620 (Conquering Fate Through Work)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 62 - ஆள்வினையுடைமை (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=zj4_pEqa_cs",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#ஆள்வினையுடைமை", "#Thirukkural", "#Aalvinaiyudaimai", "#ManlyEffort", "#Perseverance", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 65,
        "tamil_title": "அதிகாரம் 65 - சொல்வன்மை",
        "transliterated_title": "Solvanmai",
        "thematic_english_title": "The Power of Eloquence & Persuasive Speech",
        "canonical_youtube_title": "அதிகாரம் 65 - சொல்வன்மை | Solvanmai - Power of Eloquence | Guru Kula Desam",
        "track_id": "rOowxP53oWA",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அமைச்சியல் (Ministers & Statesmanship)",
        "kural_range": "641 - 650",
        "key_kurals": [
            {
                "number": 641,
                "tamil": "நாநலம் என்னும் நலனுடைமை அந்நலம்\nயாநலத் துள்ளதூஉம் அன்று.",
                "english": "The possession of the virtue of an eloquent tongue is a treasure above all other treasures in this world."
            },
            {
                "number": 645,
                "tamil": "சொல்லுக சொல்லைப் பிறிதோர்சொல் அச்சொல்லை\nவெல்லுஞ்சொல் இன்மை அறிந்து.",
                "english": "Speak such words as cannot be surpassed or refuted by any other word spoken in response."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 65: சொல்வன்மை (Solvanmai) — நாவின் சொல்லாற்றலும், சான்றோர் அவையில் பேசும் நாவன்மையும் பிற எல்லாச் செல்வங்களையும் விட மேலானது என்பதை விளக்கும் உன்னத அதிகாரம்.\n\n'நாநலம் என்னும் நலனுடைமை அந்நலம்\nயாநலத் துள்ளதூஉம் அன்று.' (குறள் 641)\n\n'சொல்லுக சொல்லைப் பிறிதோர்சொல் அச்சொல்லை\nவெல்லுஞ்சொல் இன்மை அறிந்து.' (குறள் 645)\n\nஒருவன் பேசும் சொல்லை வெல்லும் சொல் வேறு எதுவும் இல்லை என்பதை ஆராய்ந்து, நேர்த்தியாகவும் தெளிவாகவும் பேச வேண்டும். கேட்போரை வசீகரித்து, கேளாதவரையும் விரும்பச் செய்யும் இனிய சொல்லாற்றல் உலகையே வசப்படுத்தும்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) கம்பீர இன்னிசையில், 54 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 65: Solvanmai (The Power of Eloquence & Persuasive Speech) from Thirukkural by Thiruvalluvar.\n\n'The treasure of an eloquent tongue is a virtue unmatched by any other virtue possessed by mortals.' (Kural 641)\n\n'Utter such words as can never be refuted or overcome by any counter-speech.' (Kural 645)\n\nValluvar outlines the art of diplomatic rhetoric, concise logic, and the profound ethics of communication. The skilled speaker captivates allies, disarms enemies, and articulates profound truths with clarity, grace, and flawless precision.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, paired with 54 photorealistic visual artworks under ceremonial floral court atmosphere.",
            "timestamps": [
                {"time": "00:00", "label": "நாநலம் என்னும் நலனுடைமை - குறள் 641 (The Supreme Virtue of Speech)"},
                {"time": "01:25", "label": "ஆக்கமும் கேடும் தரும் சொல் - குறள் 642 (Speech of Wealth and Ruin)"},
                {"time": "02:40", "label": "சொல்லுக சொல்லை வெல்லுஞ்சொல் இன்மை அறிந்து - குறள் 645 (Irrefutable Speech)"},
                {"time": "04:00", "label": "இணரூழ்த்தும் நாறா மலர் அனையர் - குறள் 650 (The Flower of Eloquence)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 65 - சொல்வன்மை (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=rOowxP53oWA",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#சொல்வன்மை", "#Thirukkural", "#Solvanmai", "#Eloquence", "#PowerOfSpeech", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 66,
        "tamil_title": "அதிகாரம் 66 - வினைத்தூய்மை",
        "transliterated_title": "Vinaithooymai",
        "thematic_english_title": "Purity of Action & Moral Integrity",
        "canonical_youtube_title": "அதிகாரம் 66 - வினைத்தூய்மை | Vinaithooymai - Purity of Action | Guru Kula Desam",
        "track_id": "D95woYqPoPI",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அமைச்சியல் (Ministers & Righteous Action)",
        "kural_range": "651 - 660",
        "key_kurals": [
            {
                "number": 656,
                "tamil": "ஈன்றாள் பசிகாண்பான் ஆயினும் செய்யற்க\nசான்றோர் பழிக்கும் வினை.",
                "english": "Even if one were to witness one's own mother starving, commit never an act that is condemned by the wise and virtuous."
            },
            {
                "number": 660,
                "tamil": "சலத்தால் பொருள்செய்தே மார்த்தல் பசுமண்\nகலத்துள்நீர் பெய்திரீஇ யற்று.",
                "english": "Accumulating wealth through deceit and wicked means is like pouring water into an unbaked clay pot—both vessel and water perish."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 66: வினைத்தூய்மை (Vinaithooymai) — செயலில் நேர்மையும் பரிசுத்தமும் காத்து, எந்த இக்கட்டான சூழலிலும் அறநெறி தவறிய தீய செயல்களைச் செய்யக் கூடாது என்று வழிகாட்டும் உன்னத அதிகாரம்.\n\n'ஈன்றாள் பசிகாண்பான் ஆயினும் செய்யற்க\nசான்றோர் பழிக்கும் வினை.' (குறள் 656)\n\n'சலத்தால் பொருள்செய்தே மார்த்தல் பசுமண்\nகலத்துள்நீர் பெய்திரீஇ யற்று.' (குறள் 660)\n\nபெற்ற தாயின் பசியைக் காண நேர்ந்தாலும் சான்றோர் பழிக்கும் தீய செயல்களைச் செய்யக்கூடாது. வஞ்சனையால் செல்வத்தைச் சேர்த்துப் பாதுகாப்பது, சுடாத பச்சை மண்கலத்தில் நீரை ஊற்றி வைப்பது போன்றதாகும்; பாண்டமும் அழியும், நீரும் பாழாகும்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) கம்பீர இன்னிசையில், 44 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 66: Vinaithooymai (Purity of Action & Moral Integrity) from Thirukkural by Thiruvalluvar.\n\n'Even if you must watch your own mother faint from hunger, never commit an action condemned by the wise.' (Kural 656)\n\n'Accumulating fortune through deception is like pouring pure water into an unbaked vessel of green clay—both dissolve and are lost.' (Kural 660)\n\nValluvar insists on moral absolutism in statecraft and personal action. The noble end can never justify corrupt means; unrighteous gains bring destruction, while clean actions preserve honor, soul, and posterity forever.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, paired with 44 photorealistic visual artworks under cleansing drizzle atmosphere.",
            "timestamps": [
                {"time": "00:00", "label": "வினைத்தூய்மை வேண்டும் - குறள் 651 (Purity of Deeds as Supreme Virtue)"},
                {"time": "01:05", "label": "சான்றோர் பழிக்கும் வினை செய்யற்க - குறள் 656 (Rejecting Unrighteous Action)"},
                {"time": "02:15", "label": "அழக்கொண்ட எல்லாம் அழப்போம் - குறள் 659 (Ill-Gotten Gains Depart in Tears)"},
                {"time": "03:20", "label": "பசுமண் கலத்துள் நீர் - குறள் 660 (The Dissolving Clay Pot)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 66 - வினைத்தூய்மை (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=D95woYqPoPI",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#வினைத்தூய்மை", "#Thirukkural", "#Vinaithooymai", "#PurityOfAction", "#Integrity", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 67,
        "tamil_title": "அதிகாரம் 67 - வினைத்திட்பம்",
        "transliterated_title": "Vinaithitpam",
        "thematic_english_title": "Resolute Action & Unshakable Will",
        "canonical_youtube_title": "அதிகாரம் 67 - வினைத்திட்பம் | Vinaithitpam - Resolute Action | Guru Kula Desam",
        "track_id": "0WurYH-hkNM",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அமைச்சியல் (Ministers & Executive Execution)",
        "kural_range": "661 - 670",
        "key_kurals": [
            {
                "number": 666,
                "tamil": "எண்ணிய எண்ணியாங்கு எய்துப எண்ணியார்\nதிண்ணியர் ஆகப் பெறின்.",
                "english": "Whatever is conceived will be achieved precisely as conceived, if the planner's mind possesses unshakable firmness of resolve."
            },
            {
                "number": 667,
                "tamil": "உருவுகண்டு எள்ளாமை வேண்டும் உருள்பெருந்தேர்க்கு\nஅச்சாணி அன்னார் உடைத்து.",
                "english": "Despise no one on account of their modest stature; the colossal rolling chariot is held secure by the tiny linchpin."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 67: வினைத்திட்பம் (Vinaithitpam) — எடுத்த காரியத்தை இடையில் கைவிடாமல், மன உறுதியோடு இறுதிவரை நடத்தி முடிக்கும் திட்பமான செயல் திறனை விளக்கும் அதிகாரம்.\n\n'எண்ணிய எண்ணியாங்கு எய்துப எண்ணியார்\nதிண்ணியர் ஆகப் பெறின்.' (குறள் 666)\n\n'உருவுகண்டு எள்ளாமை வேண்டும் உருள்பெருந்தேர்க்கு\nஅச்சாணி அன்னார் உடைத்து.' (குறள் 667)\n\nஎண்ணியவர் உறுதியான மன வலிமை உடையவராக இருந்தால், அவர் எண்ணியதை எண்ணியவாறே அடைவர். உருவத்தின் அளவைக் கண்டு எவரையும் இகழக்கூடாது; பெரிய தேர் ஓடுவதற்குச் சிறிய அச்சாணியே ஆதாரமாக இருப்பதைப் போன்ற ஆற்றல் உடையவர்கள் உலகில் உள்ளனர்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) கம்பீர இன்னிசையில், 49 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 67: Vinaithitpam (Resolute Action & Unshakable Will) from Thirukkural by Thiruvalluvar.\n\n'What is conceived will be achieved precisely as intended, if the architect of the deed stands firm in unbroken resolve.' (Kural 666)\n\n'Despise no soul merely for their modest physical stature; the mighty, rolling ceremonial chariot is held securely by the tiny linchpin.' (Kural 667)\n\nValluvar delivers the master manual of decisive execution. Deliberate without haste, but once the decision is made, strike like lightning without delay or hesitation. Unwavering purpose brings any grand vision into reality.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, paired with 49 photorealistic visual artworks under dramatic rain and thunder atmosphere.",
            "timestamps": [
                {"time": "00:00", "label": "வினைத்திட்பம் என்பது ஒருவன் மனத்திட்பம் - குறள் 661 (Firmness of Mind as Essence)"},
                {"time": "01:10", "label": "எண்ணிய எண்ணியாங்கு எய்துப - குறள் 666 (Vision Manifested into Reality)"},
                {"time": "02:25", "label": "உருவுகண்டு எள்ளாமை வேண்டும் - குறள் 667 (The Mighty Linchpin)"},
                {"time": "03:45", "label": "சொல்லுதல் யார்க்கும் எளிய - குறள் 664 (Action Speaking louder than Words)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 67 - வினைத்திட்பம் (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=0WurYH-hkNM",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#வினைத்திட்பம்", "#Thirukkural", "#Vinaithitpam", "#ResoluteAction", "#IronWill", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 74,
        "tamil_title": "அதிகாரம் 74 - நாடு",
        "transliterated_title": "Naadu",
        "thematic_english_title": "The Prosperous Realm & Ideal Country",
        "canonical_youtube_title": "அதிகாரம் 74 - நாடு | Naadu - The Prosperous Realm | Guru Kula Desam",
        "track_id": "gjo0AfKBzsU",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரணியல் / நாட்டியல் (The Homeland & Its Prosperity)",
        "kural_range": "731 - 740",
        "key_kurals": [
            {
                "number": 737,
                "tamil": "இருபுனலும் வாய்ந்த மலையும் வருபுனலும்\nவல்லரணும் நாட்டிற்கு உறுப்பு.",
                "english": "Twin waters (rains and underground springs), well-sited protective mountains, flowing perennial rivers, and impregnable fortresses are the essential limbs of a great realm."
            },
            {
                "number": 738,
                "tamil": "பிணியின்மை செல்வம் விளைவின்பம் ஏமம்\nஅணிஎன்ப நாட்டிற்குஇவ் வைந்து.",
                "english": "Freedom from disease, abundant wealth, rich harvests, joyous living, and defensive security—these five are the ornaments of an ideal nation."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 74: நாடு (Naadu) — இயற்கை வளம், செழிப்பான வேளாண்மை, அமைதி, நோயின்மை, மற்றும் தர்ம நெறி தவறாத தலைவனைக் கொண்ட ஓர் இலட்சிய தேசத்தின் அமைப்பை விவரிக்கும் அதிகாரம்.\n\n'இருபுனலும் வாய்ந்த மலையும் வருபுனலும்\nவல்லரணும் நாட்டிற்கு உறுப்பு.' (குறள் 737)\n\n'பிணியின்மை செல்வம் விளைவின்பம் ஏமம்\nஅணிஎன்ப நாட்டிற்குஇவ் வைந்து.' (குறள் 738)\n\nமழைநீரும் ஊற்றுநீரும், உயர்ந்த மலையும், வற்றாத நதியும், வலிமையான அரணும் ஒரு நாட்டின் தூண்கள். நோயற்ற வாழ்வு, செல்வம், விளைச்சல், மகிழ்ச்சி, மற்றும் பாதுகாப்பு ஆகிய ஐந்தும் ஒரு நாட்டின் அணிகலன்கள் ஆகும்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) கம்பீர இன்னிசையில், 35 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 74: Naadu (The Prosperous Realm & Ideal Country) from Thirukkural by Thiruvalluvar.\n\n'Twin waters (rainfall and springs), sheltered mountains, perennial rivers, and sturdy fortresses constitute the body of a realm.' (Kural 737)\n\n'Freedom from pestilence, flourishing wealth, bountiful harvests, public happiness, and absolute security—these five are the ornaments of a true nation.' (Kural 738)\n\nValluvar outlines his visionary political geography of the ideal homeland: an agrarian paradise free from famine, banditry, and internal sedition, where fertile lands yield spontaneous abundance under benevolent and gentle leadership.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, paired with 35 photorealistic visual artworks under celebratory floral golden-hour atmosphere.",
            "timestamps": [
                {"time": "00:00", "label": "நாட்டின் வளம் - குறள் 731 (The Abundance of the Realm)"},
                {"time": "00:50", "label": "வளரும் புனலும் மலையும் - குறள் 737 (Rivers, Mountains and Fortresses)"},
                {"time": "01:45", "label": "பிணியின்மை செல்வம் விளைவின்பம் ஏமம் - குறள் 738 (The Five Jewels of the Nation)"},
                {"time": "02:40", "label": "மன்னன் மாண்பு - குறள் 740 (The Crown of Righteous Sovereignty)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 74 - நாடு (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=gjo0AfKBzsU",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#நாடு", "#Thirukkural", "#Naadu", "#ProsperousRealm", "#IdealCountry", "#GuruKulaDesam"
        ]
    }
]

def main():
    if not META_PATH.exists():
        existing = []
    else:
        with open(META_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)

    existing_chs = {item["chapter_number"]: idx for idx, item in enumerate(existing)}

    added = 0
    updated = 0
    for meta in BATCH4_META:
        ch = meta["chapter_number"]
        if ch in existing_chs:
            existing[existing_chs[ch]] = meta
            updated += 1
        else:
            existing.append(meta)
            added += 1

    existing.sort(key=lambda x: x["chapter_number"])

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"✅ Metadata updated: {added} chapters added, {updated} updated.")
    print(f"Total chapters in registry: {len(existing)}")

if __name__ == "__main__":
    main()
