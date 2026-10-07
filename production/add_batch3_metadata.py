# -*- coding: utf-8 -*-
"""
Adds rich, canonical metadata for Batch 3 (Chapters 39, 40, 42, 44, 45, 46)
Statecraft & Political Wisdom Suite
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "production" / "metadata" / "thirukkural_releases_metadata.json"

BATCH3_META = [
    {
        "chapter_number": 39,
        "tamil_title": "அதிகாரம் 39 - இறைமாட்சி",
        "transliterated_title": "Iraimaatchi",
        "thematic_english_title": "Sovereign Majesty & Royal Excellence",
        "canonical_youtube_title": "அதிகாரம் 39 - இறைமாட்சி | Iraimaatchi - Sovereign Majesty & Royal Excellence | Guru Kula Desam",
        "track_id": "mCwNR1Bytj4",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் (Royalty & Sovereign Governance)",
        "kural_range": "381 - 390",
        "key_kurals": [
            {
                "number": 381,
                "tamil": "படைகுடி கூழ்அமைச்சு நட்பரண் ஆறும்\nஉடையான் அரசருள் ஏறு.",
                "english": "He who possesses these six limbs—an army, citizens, wealth, ministers, allies, and a fortress—is a lion among kings."
            },
            {
                "number": 388,
                "tamil": "முறைசெய்து காப்பாற்றும் மன்னவன் மக்கட்கு\nஇறையென்று வைக்கப் படும்.",
                "english": "The monarch who administers impartial justice and faithfully defends his people will be revered as divine providence."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 39: இறைமாட்சி (Iraimaatchi) — ஓர் அரசுக்குரிய ஆறு அங்கங்களையும் (படை, குடி, கூழ், அமைச்சு, நட்பு, அரண்), நீதி தவறாத செங்கோல் ஆட்சியின் மாண்பையும் விளக்கும் அரசறிவியல் அதிகாரம்.\n\n'படைகுடி கூழ்அமைச்சு நட்பரண் ஆறும்\nஉடையான் அரசருள் ஏறு.' (குறள் 381)\n\nமுறைசெய்து குடிமக்களைக் காப்பாற்றும் மன்னவனே மக்களின் நெஞ்சில் இறைவனாக மதிக்கப்படுவான். கொடை, கருணை, நேர்மையான செங்கோல் மற்றும் குடிமக்களைக் காக்கும் ஆற்றல் கொண்ட மன்னன் உலக மன்னர்களுக்கெல்லாம் ஒளிவிளக்காகத் திகழ்வான்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) கம்பீர ராஜ இன்னிசையில், சங்க கால மாமன்னர் தர்பார், செங்கோல் மற்றும் 37 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 39: Iraimaatchi (Sovereign Majesty & Royal Excellence) from Thirukkural by Thiruvalluvar.\n\n'He who commands these six limbs—a disciplined army, flourishing citizens, abundant wealth, wise ministers, loyal allies, and impregnable fortresses—stands as a lion among monarchs.' (Kural 381)\n\nValluvar inaugurates Porutpaal (The Book of Statecraft) with the profound architecture of righteous sovereignty. The ruler is defined not by tyranny, but by accessibility, upright justice (Sengol), economic foresight, and the moral fortitude to welcome frank criticism from wise counselors.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, paired with 37 photorealistic visual artworks under ceremonial floral court atmosphere.",
            "timestamps": [
                {"time": "00:00", "label": "அரசின் ஆறு அங்கங்களும் மாட்சியும் - குறள் 381 (The Six Limbs of Statecraft)"},
                {"time": "00:55", "label": "அஞ்சாமை, ஈகை, அறிவு, ஊக்கம் (The Four Sovereign Virtues)"},
                {"time": "01:55", "label": "முறைசெய்து காப்பாற்றும் மன்னவன் - குறள் 388 (The Divine Scepter of Justice)"},
                {"time": "02:55", "label": "உலக மன்னர்களுக்கெல்லாம் ஒளிவிளக்கு (The Beacon of Sovereign Majesty)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 39 - இறைமாட்சி (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=mCwNR1Bytj4",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#இறைமாட்சி", "#Thirukkural", "#Iraimaatchi", "#SovereignMajesty", "#Statecraft", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 40,
        "tamil_title": "அதிகாரம் 40 - கல்வி",
        "transliterated_title": "Kalvi",
        "thematic_english_title": "Sacred Learning & The Lamp of Education",
        "canonical_youtube_title": "அதிகாரம் 40 - கல்வி | Kalvi - Sacred Learning & The Lamp of Education | Guru Kula Desam",
        "track_id": "KZxknhbVIk0",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் (Royalty & Sovereign Governance)",
        "kural_range": "391 - 400",
        "key_kurals": [
            {
                "number": 391,
                "tamil": "கற்க கசடறக் கற்பவை கற்றபின்\nநிற்க அதற்குத் தக.",
                "english": "Learn thoroughly and flawlessly whatever you choose to learn; then let your daily conduct be guided by that learning."
            },
            {
                "number": 392,
                "tamil": "எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும்\nகண்ணென்ப வாழும் உயிர்க்கு.",
                "english": "Numbers (arithmetic) and Letters (literature)—these two sacred sciences are the twin living eyes of mankind."
            },
            {
                "number": 400,
                "tamil": "கேடில் விழுச்செல்வம் கல்வி ஒருவற்கு\nமாடல்ல மற்றை யவை.",
                "english": "Learning is the only imperishable, indestructible wealth for man; all other material possessions are mere transient dross."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 40: கல்வி (Kalvi) — அறியாமை இருளைப் போக்கும் அழியா ஞான தீபத்தையும், எழுத்து, எண் எனும் இரு கண்களையும் போற்றும் சங்க கால வள்ளுவ பேருரை.\n\n'கற்க கசடறக் கற்பவை கற்றபின்\nநிற்க அதற்குத் தக.' (குறள் 391)\n\n'எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும்\nகண்ணென்ப வாழும் உயிர்க்கு.' (குறள் 392)\n\nதொட்டனைத் தூறும் மணற்கேணி போல, கற்கக் கற்க மனிதனின் அறிவு ஊற்றெடுத்துப் பெருகும். ஒருவனுக்கு அழியாத விழுச்செல்வம் கல்வி ஒன்றே; மற்றவை எல்லாம் செல்வம் ஆகாது.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) தெய்வீக இன்னிசையுடன், சங்க கால குருகுலக் கல்வி, ஓலைச்சுவடிகள், மணற்கேணி மற்றும் 59 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 40: Kalvi (Sacred Learning & The Imperishable Wealth of Knowledge) from Thirukkural by Thiruvalluvar.\n\n'Learn with flawless clarity whatever is worthy of learning; and having learned, walk steadfastly according to that wisdom.' (Kural 391)\n\nValluvar immortalizes education as the sovereign light of human civilization. Letters and numbers are proclaimed as the living eyes of the soul; without them, physical eyes are mere scars. Like a sand-well that yields fresh water the deeper it is dug, human intellect expands boundlessly the deeper one drinks from the fountain of knowledge.\n\nExperience this sweeping 59-shot cinematic release produced by Guru Kula Desam under gentle atmospheric morning drizzle.",
            "timestamps": [
                {"time": "00:00", "label": "கற்க கசடறக் கற்பவை - குறள் 391 (Flawless Learning & Conduct)"},
                {"time": "01:25", "label": "எண்ணும் எழுத்தும் கண்ணெனத் தகும் - குறள் 392 (Letters & Numbers as Twin Eyes)"},
                {"time": "02:50", "label": "தொட்டனைத் தூறும் மணற்கேணி - குறள் 396 (The Inexhaustible Sand-Well of Wisdom)"},
                {"time": "04:20", "label": "கேடில் விழுச்செல்வம் கல்வி - குறள் 400 (The Indestructible Treasure of Mind)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 40 - கல்வி (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=KZxknhbVIk0",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#கல்வி", "#Thirukkural", "#Kalvi", "#Education", "#SacredLearning", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 42,
        "tamil_title": "அதிகாரம் 42 - கேள்வி",
        "transliterated_title": "Kelvi",
        "thematic_english_title": "The Wisdom of Listening to the Sages",
        "canonical_youtube_title": "அதிகாரம் 42 - கேள்வி | Kelvi - The Wisdom of Listening to the Sages | Guru Kula Desam",
        "track_id": "vbMywONB5Wc",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் (Royalty & Sovereign Governance)",
        "kural_range": "411 - 420",
        "key_kurals": [
            {
                "number": 411,
                "tamil": "செல்வத்துள் செல்வம் செவிச்செல்வம் அச்செல்வம்\nசெல்வத்துள் எல்லாம் தலை.",
                "english": "The wealth gained through the hearing ear is the treasure of all treasures; it is the crowning head of all human riches."
            },
            {
                "number": 414,
                "tamil": "கற்றிலன் ஆயினும் கேட்க அஃதொருவற்கு\nஒற்கத்தின் ஊற்றாந் துணை.",
                "english": "Even if unlettered, let a man continually listen to the wise; in times of stumbling adversity, it will serve as an unshakeable staff."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 42: கேள்வி (Kelvi - கேள்விச் செல்வம்) — நூல் கற்காத நிலையிலும் கூட, சான்றோர்களின் வாய்மொழிகளைக் கேட்டுப் பெறும் ஞானமே மனிதனுக்கு ஆபத்தில் ஊன்றுகோலாய் நிற்கும் மாபெரும் செல்வம்.\n\n'செல்வத்துள் செல்வம் செவிச்செல்வம் அச்செல்வம்\nசெல்வத்துள் எல்லாம் தலை.' (குறள் 411)\n\nசெவிக்கு உணவில்லாத போதே வயிற்றுக்கு சிறிது ஈயப்படும். சான்றோர்களின் நற்போதனைகளைக் கேட்டு உணர்ந்தவர்கள் வழுக்கலான சேற்று நிலத்தில் ஊன்றிய ஊன்றுகோல் போல வழுவாமல் நிலைத்து நிற்பார்கள்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) தெய்வீக இன்னிசையுடன், சான்றோர் பேரவை, யாழ் இசை, தத்துவ உரை மற்றும் 41 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 42: Kelvi (The Possession of Hearing / Oral Wisdom from the Sages) from Thirukkural by Thiruvalluvar.\n\n'The wealth acquired through the attentive ear is the supreme wealth; it stands as the crowning chief among all worldly treasures.' (Kural 411)\n\nValluvar reveals the supremacy of attentive listening over superficial reading. When the ear lacks intellectual food, only then should food be offered to the stomach. Even for those unable to read, words absorbed from wise masters act as an unbending walking staff on slippery, treacherous slopes.\n\nExperience this complete cinematic musical release produced by Guru Kula Desam, harmonized with 41 photorealistic artworks under reflective atmospheric rain.",
            "timestamps": [
                {"time": "00:00", "label": "செவிச்செல்வமே செல்வத்துள் தலை - குறள் 411 (The Supreme Treasure of the Ear)"},
                {"time": "01:05", "label": "செவிக்கு உணவு இல்லாத போது (Spiritual Hunger Above Bodily Food)"},
                {"time": "02:15", "label": "ஒற்கத்தின் ஊற்றாந் துணை - குறள் 414 (The Unshakable Staff in Adversity)"},
                {"time": "03:20", "label": "சான்றோர்களின் அமர வாய்மொழி (The Immortal Spoken Wisdom)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 42 - கேள்வி (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=vbMywONB5Wc",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#கேள்வி", "#Thirukkural", "#Kelvi", "#ListeningWisdom", "#OralTradition", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 44,
        "tamil_title": "அதிகாரம் 44 - குற்றங்கடிதல்",
        "transliterated_title": "Kutrangadithal",
        "thematic_english_title": "Guarding against Faults & Moral Vigilance",
        "canonical_youtube_title": "அதிகாரம் 44 - குற்றங்கடிதல் | Kutrangadithal - Guarding against Faults & Moral Vigilance | Guru Kula Desam",
        "track_id": "VVkl8bORJXg",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் (Royalty & Sovereign Governance)",
        "kural_range": "431 - 440",
        "key_kurals": [
            {
                "number": 433,
                "tamil": "தினைத்துணையாம் குற்றம் வரினும் பனைத்துணையாக்\nகொள்வர் பழிநாணு வார்.",
                "english": "Though a fault be small as a tiny millet seed, those who dread dishonor will regard it as colossal as a towering palmyra palm."
            },
            {
                "number": 435,
                "tamil": "வருமுன்னர்க் காவாதான் வாழ்க்கை எரிமுன்னர்\nவைத்தூறு போலக் கெடும்.",
                "english": "The life of one who does not guard against faults before they occur will perish like a dry haystack before an advancing fire."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 44: குற்றங்கடிதல் (Kutrangadithal) — தன்னிடம் தோன்றும் சிறு குறைகளையும் தொடக்கத்திலேயே கிள்ளி எறிந்து, தன் வாழ்வையும் நாட்டையும் அழிவிலிருந்து காக்கும் விவேகம்.\n\n'தினைத்துணையாம் குற்றம் வரினும் பனைத்துணையாக்\nகொள்வர் பழிநாணு வார்.' (குறள் 433)\n\n'வருமுன்னர்க் காவாதான் வாழ்க்கை எரிமுன்னர்\nவைத்தூறு போலக் கெடும்.' (குறள் 435)\n\nசெருக்கு, சினம், சிற்றின்பம் ஆகிய குற்றங்கள் மன்னனின் மாண்பை அழிக்கும். குற்றம் நேர்வதற்கு முன்னரே தடுத்துக் கொள்ளாதவனின் வாழ்க்கை நெருப்பின் முன் நின்ற வைக்கோல் போர் போல சுட்டெரிக்கப்படும். தன் குற்றத்தை முதலில் களைபவனை எந்தப் பழியும் தொட முடியாது.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) எச்சரிக்கை தவழும் கம்பீர இசையமைப்பில், 36 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 44: Kutrangadithal (Guarding against Faults & Moral Self-Correction) from Thirukkural by Thiruvalluvar.\n\n'Though an error be tiny as a millet grain, those who dread dishonor perceive it as colossal as a towering palmyra tree.' (Kural 433)\n\n'The destiny of one who fails to foresee and rectify flaws before disaster strikes will be consumed like a dry haystack before a leaping spark.' (Kural 435)\n\nValluvar instructs leaders and individuals alike that internal moral blind spots are deadlier than external invaders. By rooting out arrogance, unwarranted wrath, and unprincipled indulgence from within oneself before judging others, one establishes an impregnable moral fortress.\n\nExperience this complete cinematic release produced by Guru Kula Desam, featuring 36 dramatic artworks under atmospheric rainfall and storm warnings.",
            "timestamps": [
                {"time": "00:00", "label": "செருக்கு, சினம், சிறுமை என்னும் குற்றங்கள் (The Destructive Inner Vices)"},
                {"time": "00:55", "label": "தினைத்துணைக் குற்றமும் பனைத்துணையாகும் - குறள் 433 (The Magnified Grain of Error)"},
                {"time": "01:50", "label": "எரிமுன்னர் வைத்தூறு போன்ற வாழ்க்கை - குறள் 435 (The Consuming Spark of Neglect)"},
                {"time": "02:45", "label": "தன் குற்றம் நீக்கிப் பிறர் குற்றம் காண்க (The Invulnerable Purity of Self-Audit)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 44 - குற்றங்கடிதல் (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=VVkl8bORJXg",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#குற்றங்கடிதல்", "#Thirukkural", "#Kutrangadithal", "#SelfDiscipline", "#Vigilance", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 45,
        "tamil_title": "அதிகாரம் 45 - பெரியாரைத் துணைக்கோடல்",
        "transliterated_title": "Periyaaraith Thunaikkodal",
        "thematic_english_title": "Seeking the Fellowship & Counsel of Sages",
        "canonical_youtube_title": "அதிகாரம் 45 - பெரியாரைத் துணைக்கோடல் | Periyaaraith Thunaikkodal - Fellowship of Sages | Guru Kula Desam",
        "track_id": "HRN77i6Kio8",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் (Royalty & Sovereign Governance)",
        "kural_range": "441 - 450",
        "key_kurals": [
            {
                "number": 444,
                "tamil": "இடிக்குந் துணையாரை யாள்வாரை யாரே\nகெடுக்குந் தகைமை யவர்.",
                "english": "Who on earth has the power to destroy the ruler who secures counselors courageous enough to sharply rebuke his faults?"
            },
            {
                "number": 445,
                "tamil": "இடிப்பாரை இல்லாத ஏமரா மன்னன்\nகெடுப்பார் இலானும் கெடும்.",
                "english": "The unguarded king who possesses no fearless counselors to reprove him will perish of himself, even without external enemies."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 45: பெரியாரைத் துணைக்கோடல் (Periyaaraith Thunaikkodal) — தவத்திலும் அறிவிலும் சிறந்த பெரியோர்களை துணையாகக் கொண்டு, தவறுகளை இடித்துரைக்கும் சான்றோர்களை அரவணைத்து ஆட்சி நடத்தும் அரச நெறி.\n\n'இடிக்குந் துணையாரை யாள்வாரை யாரே\nகெடுக்குந் தகைமை யவர்.' (குறள் 444)\n\n'இடிப்பாரை இல்லாத ஏமரா மன்னன்\nகெடுப்பார் இலானும் கெடும்.' (குறள் 445)\n\nகுற்றங்களை அச்சமின்றி சுட்டிக்காட்டும் பெரியோர்களை துணையாகக் கொண்ட மன்னனை எந்தப் பகையாலும் வெல்ல முடியாது. அப்படி இடித்துக் கூறும் சான்றோர் இல்லாத மன்னன், பகைவரே இல்லாவிட்டாலும் தானே அழிந்து போவான்.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) பக்குவமான சாந்த இசையமைப்பில், வன முனிவர்கள், அரச சபை, ஞானிகள் உபதேசம் மற்றும் 42 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 45: Periyaaraith Thunaikkodal (Seeking the Alliance & Guidance of the Great) from Thirukkural by Thiruvalluvar.\n\n'Who indeed has the strength to overthrow the sovereign who surrounds his throne with mentors bold enough to sharply rebuke his faults?' (Kural 444)\n\n'The unguided ruler who has no fearless counselors to admonish him will crumble and perish of himself, even if no enemies attack him.' (Kural 445)\n\nValluvar presents genuine statecraft as the courageous invitation of honest criticism. Surrounding oneself with sycophants guarantees ruin; but cherishing seasoned philosophers and moral preceptors endows the state with an invulnerable shield against foreign intrigue and domestic decay.\n\nExperience this complete cinematic musical release by Guru Kula Desam, harmonized with 42 photorealistic artworks under gentle forest mist and morning drizzle.",
            "timestamps": [
                {"time": "00:00", "label": "அறிவிலும் தவத்திலும் சிறந்த பெரியோரை நாடுதல் (Inviting the Venerable Sages)"},
                {"time": "01:05", "label": "இடிக்குந் துணையாரை ஆள்வாரை யார் கெடுப்பார் - குறள் 444 (The Shield of Honest Critics)"},
                {"time": "02:15", "label": "இடிப்பாரை இல்லாத மன்னன் தானாகக் கெடும் - குறள் 445 (The Fall of the Unguided)"},
                {"time": "03:30", "label": "ஞானிகள் அருளால் நிலைக்கும் ராஜ்யம் (The Eternal Kingdom of Truth)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 45 - பெரியாரைத் துணைக்கோடல் (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=HRN77i6Kio8",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#பெரியாரைத்துணைக்கோடல்", "#Thirukkural", "#PeriyaaraithThunaikkodal", "#WiseCounsel", "#SpiritualMentors", "#GuruKulaDesam"
        ]
    },
    {
        "chapter_number": 46,
        "tamil_title": "அதிகாரம் 46 - சிற்றினஞ்சேராமை",
        "transliterated_title": "Sitrinanjeraamai",
        "thematic_english_title": "Avoiding Base Fellowship & The Law of Association",
        "canonical_youtube_title": "அதிகாரம் 46 - சிற்றினஞ்சேராமை | Sitrinanjeraamai - Avoiding Base Fellowship | Guru Kula Desam",
        "track_id": "wylRNpaJNmY",
        "paal": "பொருட்பால் (Book of Wealth & Statecraft)",
        "iyal": "அரசியல் (Royalty & Sovereign Governance)",
        "kural_range": "451 - 460",
        "key_kurals": [
            {
                "number": 452,
                "tamil": "நிலத்தியல்பால் நீர்திரிந் தற்றாகும் மாந்தர்க்கு\nஇனத்தியல்ப தாகும் அறிவு.",
                "english": "As pure rainwater transforms its color and taste according to the nature of the soil it falls upon, man's character takes the nature of his companions."
            },
            {
                "number": 460,
                "tamil": "நல்லினத்தின் ஊங்கும் துணையில்லை தீயினத்தின்\nஅல்லல் படுப்பதூஉம் இல்.",
                "english": "There is no greater guardian ally in life than noble companionship; and there is no greater source of ruin and misery than base fellowship."
            }
        ],
        "description": {
            "tamil_summary": "அதிகாரம் 46: சிற்றினஞ்சேராமை (Sitrinanjeraamai) — சேர்ந்த இடத்தைப் பொறுத்தே நீர் நிறம் மாறுவது போல, நாம் சேரும் சகவாசத்தைப் பொறுத்தே நமது குணமும் வாழ்வும் அமையும் என்பதை எச்சரிக்கும் வள்ளுவ உளவியல் நெறி.\n\n'நிலத்தியல்பால் நீர்திரிந் தற்றாகும் மாந்தர்க்கு\nஇனத்தியல்ப தாகும் அறிவு.' (குறள் 452)\n\n'நல்லினத்தின் ஊங்கும் துணையில்லை தீயினத்தின்\nஅல்லல் படுப்பதூஉம் இல்.' (குறள் 460)\n\nசான்றோர்கள் கீழ்மக்களின் தொடர்பைக் கண்டு அஞ்சுவர். நல்லவர்களின் சேர்க்கையை விட மேலான துணையும் உலகத்தில் இல்லை; தீயவர்களின் சேர்க்கையை விட பேரழிவைத் தரும் பகையும் வேறு எதுவும் இல்லை.\n\nகுரு குல தேசத்தின் (@guru-kula-desam) தத்துவப் பண்ணிசையில், செம்மண் நிலத்தில் கலக்கும் மழைநீரின் உவமை, சான்றோர் நட்பு மற்றும் 53 தனித்துவ கலைக் காட்சிகளுடன் கூடிய முழு நீள காவியத் திரைப்படம்.",
            "english_summary": "Chapter 46: Sitrinanjeraamai (Avoiding Base Fellowship & The Supreme Law of Association) from Thirukkural by Thiruvalluvar.\n\n'Even as pristine rainwater changes its nature according to the soil upon which it falls, human wisdom and character take the very nature of one's associates.' (Kural 452)\n\n'There is no greater uplifting ally in this universe than noble fellowship; and there is no deeper pit of ruin and misery than the company of the base.' (Kural 460)\n\nValluvar unveils profound psychological insight: while the intellect is developed through study, character is irrevocably shaped by one's inner circle. Purity of mind, purity of deeds, and immortal glory depend entirely upon walking in the fellowship of the righteous.\n\nExperience this sweeping 53-shot cinematic masterpiece produced by Guru Kula Desam under symbolic atmospheric rainfall.",
            "timestamps": [
                {"time": "00:00", "label": "சிற்றினத்தை அஞ்சி ஒதுங்கும் சான்றோர் (The Noble Dread of Base Company)"},
                {"time": "01:25", "label": "நிலத்தியல்பால் நீர் திரிந்தற்று - குறள் 452 (Rainwater Taking the Nature of Soil)"},
                {"time": "02:50", "label": "மனத்தூய்மையும் இனத்தூய்மையும் (Purity of Mind Rooted in Company)"},
                {"time": "04:15", "label": "நல்லினத்தின் ஊங்கும் துணை இல்லை - குறள் 460 (The Supreme Refuge of Noble Fellowship)"}
            ],
            "audio_credits": {
                "track": "அதிகாரம் 46 - சிற்றினஞ்சேராமை (Original Master)",
                "artist": "Guru Kula Desam",
                "vocals_engineering": "Nagarajan Balasubramanian",
                "audio_source_url": "https://www.youtube.com/watch?v=wylRNpaJNmY",
                "playlist_url": "https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro"
            },
            "call_to_action": "Subscribe to @guru-kula-desam for authentic Thirukkural cinematic musical compositions and timeless Tamil ethical heritage."
        },
        "hashtags": [
            "#திருக்குறள்", "#சிற்றினஞ்சேராமை", "#Thirukkural", "#Sitrinanjeraamai", "#LawOfAssociation", "#NobleFriendship", "#GuruKulaDesam"
        ]
    }
]

def update_metadata():
    existing = []
    if META_PATH.exists():
        with open(META_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
            
    existing_nums = {item["chapter_number"] for item in existing}
    added_count = 0
    
    for item in BATCH3_META:
        if item["chapter_number"] in existing_nums:
            for idx, ex in enumerate(existing):
                if ex["chapter_number"] == item["chapter_number"]:
                    existing[idx] = item
                    break
        else:
            existing.append(item)
            added_count += 1
            
    existing.sort(key=lambda x: x["chapter_number"])
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
        
    print(f"Updated {META_PATH} successfully! Total chapters in metadata: {len(existing)}")

if __name__ == "__main__":
    update_metadata()
