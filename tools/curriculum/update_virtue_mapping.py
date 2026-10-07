# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Alphabets to Virtue Mapping Engine
Maps Tamil alphabets (உயிர் & மெய் எழுத்துக்கள்) to sacred virtues,
structured progressively across 3 difficulty tiers and 12 class grades:
  Tier 1: அறிதல் / கற்றல் (To Learn - Grades 1 to 4)
  Tier 2: செய்தல் / பின்பற்றுதல் (To Follow & Habituate - Grades 5 to 8)
  Tier 3: நிலைநிறுத்துதல் / காத்தல் (To Maintain & Master under Adversity - Grades 9 to 12)
"""

import os
import re

VIRTUES_BY_GRADE = {
    1: {
        "tier": "Tier 1: அறிதல் & கற்றல் (To Learn & Cultivate)",
        "tier_badge": "நிலை 1: அறிதல் (Learn)",
        "tier_color": "#2a9d8f",
        "letters": ["அ", "ஆ", "இ", "ஈ"],
        "title": "அறம், சாந்தம், இன்சொல் & ஈகை",
        "english_title": "Righteousness, Calmness, Pleasant Speech & Sharing",
        "description": "குழந்தைப் பருவத்தில் எளிய வாழ்க்கை நெறிகளாக அறத்தை விரும்புதல், கோபத்தைத் தணித்தல், இனிமையாகப் பேசுதல் மற்றும் பிறருடன் பகிர்ந்து உண்ணுதல் ஆகிய அடிப்படைப் பண்புகளை அறிந்து பழகுதல்.",
        "virtues": [
            {
                "letter": "அ",
                "virtue": "அறம் (Righteousness & Love of Virtue)",
                "verse": "அறஞ்செய விரும்பு — ஔவையார் (ஆத்திசூடி) / அகர முதல எழுத்தெல்லாம் — திருக்குறள் 1",
                "meaning": "எல்லா எழுத்துக்களுக்கும் 'அ'கரம் முதலாவது போல, மனித வாழ்க்கைக்கு நற்செயல்களை விரும்பிச் செய்வதே முதன்மையான பண்பாகும்.",
                "exercise": "தினமும் ஒரு நல்ல செயலை (பெரியவர்களுக்கு உதவுதல், தாவரங்களுக்கு நீர் ஊற்றுதல்) விரும்பிச் செய்தல்."
            },
            {
                "letter": "ஆ",
                "virtue": "ஆறுதல் / சினம் தணித்தல் (Calmness & Gentleness)",
                "verse": "ஆறுவது சினம் — ஔவையார் (ஆத்திசூடி) / ஆலயம் தொழுவது சாலவும் நன்று — கொன்றை வேந்தன்",
                "meaning": "கோபத்தை உடனுக்குடன் தணித்துக் கொள்வது அமைதியான உள்ளத்திற்கும் நல்ல நட்பிற்கும் வித்தாகும்.",
                "exercise": "கோபம் வரும் போது அமைதியாக 'ஓம் நமச்சிவாய' சொல்லி 10 வரை எண்ணி மனதை அமைதிப்படுத்துதல்."
            },
            {
                "letter": "இ",
                "virtue": "இன்சொல் (Pleasant & Respectful Speech)",
                "verse": "இனிய உளவாக இன்னாத கூறல் கனியிருப்பக் காய்கவர்ந் தற்று — திருக்குறள் 100",
                "meaning": "இனிமையான சொற்கள் இருக்கும் போது கடுமையான சொற்களைப் பேசுவது இனிய பழத்தை விடுத்துக் காயைத் தின்பதற்கு ஒப்பானது.",
                "exercise": "வீட்டிலும் பள்ளியிலும் அனைவரிடமும் 'தயவுசெய்து', 'நன்றி', 'வணக்கம்' போன்ற இன்சொற்களைப் பேசுதல்."
            },
            {
                "letter": "ஈ",
                "virtue": "ஈகை (Sharing with Love)",
                "verse": "ஈவது விலக்கேல் — ஆத்திசூடி / ஈதல் இசைபட வாழ்தல் — திருக்குறள் 231",
                "meaning": "தேவையுள்ளோருக்கு உங்களால் இயன்ற உணவையோ பொருள்களையோ மகிழ்ச்சியோடு பகிர்ந்து கொடுத்தல்.",
                "exercise": "தன்னுடைய சிற்றுண்டியை அல்லது எழுத்துப் பொருளைத் தோழர்களுடன் இன்முகத்தோடு பகிர்தல்."
            }
        ]
    },
    2: {
        "tier": "Tier 1: அறிதல் & கற்றல் (To Learn & Cultivate)",
        "tier_badge": "நிலை 1: அறிதல் (Learn)",
        "tier_color": "#2a9d8f",
        "letters": ["உ", "ஊ", "எ", "ஏ"],
        "title": "உண்மை, ஊக்கம், கல்வி மரியாதை & தன்மானம்",
        "english_title": "Truthfulness, Enthusiasm, Reverence for Learning & Self-Reliance",
        "description": "உண்மை பேசுதல், கல்வியில் சோர்வில்லா ஊக்கம் காட்டுதல், பெற்றோர் ஆசிரியர்களை மதித்தல் மற்றும் தன்மானத்தோடு வாழ்வதன் அடிப்படைகளை அறிதல்.",
        "virtues": [
            {
                "letter": "உ",
                "virtue": "உண்மை & உழைப்பு (Truthfulness & Diligence)",
                "verse": "உடையது விளம்பேல் — ஆத்திசூடி / அன்னையும் பிதாவும் முன்னறி தெய்வம் — கொன்றை வேந்தன்",
                "meaning": "தவறு நிகழ்ந்தாலும் அஞ்சாமல் உண்மையை ஒப்புக்கொள்ளுதல்; பெற்றோருக்கு உதவியாக இருத்தல்.",
                "exercise": "தன் அன்றாடப் பாடங்களையும் வேலைகளையும் சோம்பலின்றித் தானே செய்து முடித்தல்."
            },
            {
                "letter": "ஊ",
                "virtue": "ஊக்கம் (Enthusiasm in Studies & Play)",
                "verse": "ஊக்கமது கைவிடேல் — ஆத்திசூடி / ஊருடன் பகைக்கின் வேருடன் கெடும் — கொன்றை வேந்தன்",
                "meaning": "எந்தச் செயலைச் செய்தாலும் சோர்வடையாமல் ஆர்வத்தோடும் புத்துணர்ச்சியோடும் ஈடுபடுதல்.",
                "exercise": "கடினமான பாடம் அல்லது விளையாட்டாக இருந்தாலும் விடாமுயற்சியோடு கற்றுக்கொள்ளுதல்."
            },
            {
                "letter": "எ",
                "virtue": "எண்ணும் எழுத்தும் (Reverence for Literacy & Numeracy)",
                "verse": "எண் எழுத்து இகழேல் — ஆத்திசூடி / எண்ணும் எழுத்தும் கண் எனத் தகும் — கொன்றை வேந்தன்",
                "meaning": "கணிதமும் மொழியும் மனிதருக்கு இரு கண்கள் போன்றவை; கல்வியை ஒருபோதும் அலட்சியம் செய்யலாகாது.",
                "exercise": "புத்தகங்களையும் எழுத்துக் கருவிகளையும் கடவுளைப் போல தூய்மையாகவும் பக்தியோடும் கையாளுதல்."
            },
            {
                "letter": "ஏ",
                "virtue": "ஏற்பது இகழ்ச்சி (Self-Reliance & Noble Independence)",
                "verse": "ஏற்பது இகழ்ச்சி — ஆத்திசூடி / ஏவா மக்கள் மூவா மருந்து — கொன்றை வேந்தன்",
                "meaning": "பிறரிடம் கையேந்திப் பிச்சையெடுப்பது இழிவானது; சொல்லாமலேயே நற்பணிகளைச் செய்யும் பிள்ளைகள் அமுதமாவர்.",
                "exercise": "தன் பொருள்களைத் தானே பாதுகாத்துக் கொள்ளுதல், பிறரைச் சார்ந்து வாழும் பழக்கத்தைத் தவிர்த்தல்."
            }
        ]
    },
    3: {
        "tier": "Tier 1: அறிதல் & கற்றல் (To Learn & Cultivate)",
        "tier_badge": "நிலை 1: அறிதல் (Learn)",
        "tier_color": "#2a9d8f",
        "letters": ["ஐ", "ஒ", "ஓ", "ஔ", "ஃ"],
        "title": "ஐயமின்மை, ஒப்புரவு, ஓதுதல், ஔவியமின்மை & நேர்மை",
        "english_title": "Charity, Community Harmony, Daily Scripture Reading, Freedom from Malice & Equanimity",
        "description": "சமூகத்தோடு இணைந்து வாழும் நெறி, தினமும் திருமுறைகளை ஓதும் பழக்கம், பொறாமையற்ற குணம் மற்றும் நேர்மையான அளவீடு.",
        "virtues": [
            {
                "letter": "ஐ",
                "virtue": "ஐயமிட்டு உண் (Feed the Needy First)",
                "verse": "ஐயமிட்டு உண் — ஆத்திசூடி / ஐயம் புகினும் செய்வன செய் — கொன்றை வேந்தன்",
                "meaning": "பசித்திருக்கும் ஏழைகளுக்கும் பிற உயிர்களுக்கும் உணவளித்த பின்னரே தான் உண்ண வேண்டும் என்ற ஜீவகாருண்யம்.",
                "exercise": "வீட்டு வாசலில் வரும் பறவைகளுக்கும் பிராணிகளுக்கும் ஒரு பிடி உணவும் நீரும் வைத்த பின் உண்ணுதல்."
            },
            {
                "letter": "ஒ",
                "virtue": "ஒப்புரவு (Universal Harmony & Cooperation)",
                "verse": "ஒப்புரவு ஒழுகு — ஆத்திசூடி / ஒன்றுபட்டால் உண்டு வாழ்வு",
                "meaning": "ஊரோடும் உலகத்தோடும் ஒத்துப்போய், அனைவரையும் தன்னுடை சகோதரர்களாகக் கருதி ஒற்றுமையுடன் வாழ்தல்.",
                "exercise": "பள்ளியில் அனைத்து மாணவர்களுடனும் பேதமின்றி நட்பு பாராட்டி ஒற்றுமையாகச் செயல்படுதல்."
            },
            {
                "letter": "ஓ",
                "virtue": "ஓதுதல் (Sacred Chanting & Reading)",
                "verse": "ஓதுவது ஒழியேல் — ஆத்திசூடி / ஓதலின் நன்றே ஒழுக்கம் உடைமை — கொன்றை வேந்தன்",
                "meaning": "அறிவு தரும் நூல்களையும் தேவாரம், திருவாசகப் பதிகங்களையும் ஒருநாளும் ஓதாமல் விடக்கூடாது.",
                "exercise": "தினமும் காலையிலும் மாலையிலும் ஒரு திருமுறைப் பாடலை பண்ணோடு பாடி வழிபடுதல்."
            },
            {
                "letter": "ஔ",
                "virtue": "ஔவியமின்மை (Absence of Envy & Jealousy)",
                "verse": "ஔவியம் பேசேல் — ஆத்திசூடி / ஔவியம் பேசுதல் ஆக்கத்திற்கு அழிவு — கொன்றை வேந்தன்",
                "meaning": "மற்றொருவர் நல்ல நிலையை அடையும் போது பொறாமைப்பட்டுப் பேசக்கூடாது; பொறாமை நல்வாழ்வை அழிக்கும்.",
                "exercise": "வகுப்பில் மற்றொரு மாணவர் வெற்றி பெறும் போது மனதாரப் பாராட்டி மகிழ்தல்."
            },
            {
                "letter": "ஃ",
                "virtue": "அஃகம் சுருக்கேல் (Fair Dealing & Integrity in Measure)",
                "verse": "அஃகம் சுருக்கேல் — ஆத்திசூடி / அஃகமும் காசும் சிக்கெனத் தேடு — கொன்றை வேந்தன்",
                "meaning": "கொடுக்கல் வாங்கலில் எடையையோ அளவையோ குறைத்து நேர்மையற்ற முறையில் ஆதாயம் தேடக்கூடாது.",
                "exercise": "விளையாட்டிலும் படிப்பிலும் நேர்மையைக் கடைப்பிடித்தல், குறுக்கு வழியைத் தவிர்த்தல்."
            }
        ]
    },
    4: {
        "tier": "Tier 1: அறிதல் & தொடங்குதல் (To Learn & Initiate Action)",
        "tier_badge": "நிலை 1: தொடங்குதல் (Initiate)",
        "tier_color": "#2a9d8f",
        "letters": ["க", "ங"],
        "title": "கருணை, ஜீவகாருண்யம் & குடும்பப் பணிவு",
        "english_title": "Universal Compassion, Non-injury & Family Adaptability",
        "description": "அனைத்து உயிர்களிடத்தும் கருணை காட்டுதல், தன் சுற்றத்தாரோடும் சமூகத்தோடும் பணிவோடு இணைந்து செயல்படுதல்.",
        "virtues": [
            {
                "letter": "க",
                "virtue": "கருணை & கொல்லாமை (Compassion & Non-violence)",
                "verse": "கண்டொன்று சொல்லேல் — ஆத்திசூடி / வாடிய பயிரைக் கண்டபோதெல்லாம் வாடினேன் — வள்ளலார்",
                "meaning": "மனதில் ஒன்றை வைத்துக்கொண்டு வாயில் வேறொன்றைப் பேசலாகாது; எவ்வுயிருக்கும் துன்பம் செய்யாத தயவு.",
                "exercise": "மரக்கிளைகளை முறிக்காமல், எறும்பு, பூச்சிகளை மிதிக்காமல் இயற்கையைக் காக்கும் வாழ்வியல் பழக்கம்."
            },
            {
                "letter": "ங",
                "virtue": "ஙப்போல் வளைதல் (Humility & Adaptability with Kin)",
                "verse": "ஙப் போல் வளை — ஔவையார் (ஆத்திசூடி)",
                "meaning": "‘ங’ என்ற மெல்லின எழுத்து தன் இன வல்லினக் கூட்டத்தோடு பொருந்தி வளைவது போல, குடும்பத்தோடும் நல்லோரோடும் பணிந்து வாழ்தல்.",
                "exercise": "ஆணவமும் பிடிவாதமும் இல்லாமல் பெற்றோர் மற்றும் ஆசிரியரின் வழிகாட்டுதலை பணிவோடு ஏற்றல்."
            }
        ]
    },
    5: {
        "tier": "Tier 2: செய்தல் & பின்பற்றுதல் (To Follow & Habituate)",
        "tier_badge": "நிலை 2: பின்பற்றுதல் (Follow)",
        "tier_color": "#e9c46a",
        "letters": ["ச", "ஞ"],
        "title": "சத்துவ ஒழுக்கம், செய்ந்நன்றி & ஞான நாட்டம்",
        "english_title": "Sattvic Discipline, Lifelong Gratitude & Thirst for Wisdom",
        "description": "உடல், மனம், வாக்கு ஆகிய மூன்றிலும் தூய்மை பேணுதல்; செய்த நன்றியை எக்காலத்தும் மறவாமை; ஞான நூல்களைத் தேடிக் கற்றல்.",
        "virtues": [
            {
                "letter": "ச",
                "virtue": "செய்ந்நன்றி அறிதல் & சத்துவம் (Gratitude & Pure Character)",
                "verse": "செய்யாமல் செய்த உதவிக்கு வையகமும் வானகமும் ஆற்றல் அரிது — திருக்குறள் 101 / சனி நீராடு — ஆத்திசூடி",
                "meaning": "தான் ஓர் உதவியும் செய்யாதிருந்தும் தனக்கு உதவி செய்தவரின் நன்மையை மூவுலகைக் காட்டிலும் பெரிதாகப் போற்றுதல்.",
                "exercise": "தனக்கு கல்வி கற்பிக்கும் ஆசிரியர்களுக்கும் வளர்க்கும் பெற்றோருக்கும் நன்றி செலுத்தி பணிவிடை செய்தல்."
            },
            {
                "letter": "ஞ",
                "virtue": "ஞாயம்பட உரைத்தல் & காலமறிதல் (Righteous Wisdom & Timely Action)",
                "verse": "ஞயம்பட உரை — ஆத்திசூடி / ஞாலம் கருதினுங் கைகூடும் காலம் கருதி இடத்தாற் செயின் — திருக்குறள் 484",
                "meaning": "நீதியும் அழகும் பொருந்தப் பேசுதல்; செய்ய வேண்டிய கடமைகளை உரிய காலத்தில் தகுந்த முறையில் செய்து முடித்தல்.",
                "exercise": "நேரத்தை வீணடிக்காமல் கால அட்டவணையின்படி படித்து, நற்பணிகளில் முன்னிற்பது."
            }
        ]
    },
    6: {
        "tier": "Tier 2: செய்தல் & பின்பற்றுதல் (To Follow & Habituate)",
        "tier_badge": "நிலை 2: பின்பற்றுதல் (Follow)",
        "tier_color": "#e9c46a",
        "letters": ["த"],
        "title": "தன்னடக்கம், ஐம்பொறி அடக்கம் & அடக்கமுடைமை",
        "english_title": "Self-Restraint, Mastery of Five Senses & Humility",
        "description": "ஐம்பொறிகளின் வழியே மனதைச் செல்லவிடாமல் நெறிப்படுத்துதல்; கல்வி அறிவினால் செருக்கு அடையாமல் அடக்கத்தோடு இருத்தல்.",
        "virtues": [
            {
                "letter": "த",
                "virtue": "அடக்கமுடைமை & தவம் (Sensory Control & Temperance)",
                "verse": "ஒருமையுள் ஆமைபோல் ஐந்துஅடக்கல் ஆற்றின் எழுமையும் ஏமாப் புடைத்து — திருக்குறள் 126 / தீயாரைக் காண்பதுவும் தீதே",
                "meaning": "ஆமை ஆபத்து வரும்போது தன் ஐந்து உறுப்புகளையும் அடக்கிக் கொள்வது போல, தீமையிலிருந்து தன் ஐம்பொறிகளையும் காப்பவனுக்குப் பிறவிதோறும் காவல் உண்டாகும்.",
                "exercise": "கண் (தீய காட்சிகளைப் பாராமை), செவி (புறங்கூறலைக் கேளாமை), நாக்கு (தீய சொற்களைப் பேசாமை, சுவைக்கு அடிமையாகாமை) என புலனடக்கம் பழகுதல்."
            }
        ]
    },
    7: {
        "tier": "Tier 2: செய்தல் & பின்பற்றுதல் (To Follow & Habituate)",
        "tier_badge": "நிலை 2: பின்பற்றுதல் (Follow)",
        "tier_color": "#e9c46a",
        "letters": ["ந"],
        "title": "நடுவுநிலைமை, நன்றி மறவாமை & நட்பாராய்தல்",
        "english_title": "Impartial Justice, Unshakable Gratitude & Noble Friendship",
        "description": "சுயநலமோ பாரபட்சமோ இன்றி நடுவுநிலை தவறாது நீதியை நிலைநிறுத்துதல்; தீய நட்பை விலக்கித் தூய நற்பண்பாளர்களைத் தேர்ந்தெடுத்தல்.",
        "virtues": [
            {
                "letter": "ந",
                "virtue": "நடுவுநிலைமை & நற்பண்பு (Impartiality & Right Association)",
                "verse": "சமன்செய்து சீர்தூக்கும் கோல்போல் அமைந்தொருபால் கோடாமை சான்றோர்க் கணி — திருக்குறள் 118 / நன்மை கடைப்பிடி",
                "meaning": "துலாக்கோல் போல சமமாக நின்று எளியவர் வலியவர் என்ற பாரபட்சமின்றி நியாயத்தின் வழி நிற்றல் சான்றோரின் அழகாகும்.",
                "exercise": "தோழர்களிடையே பிரச்சனை வரும்போது தன் நண்பன் என்பதற்காக தவறை நியாயப்படுத்தாமல் நீதியின் பக்கம் பேசுதல்."
            }
        ]
    },
    8: {
        "tier": "Tier 2: நிலைநிறுத்துதல் தொடக்கம் (Transition to Sustained Virtue)",
        "tier_badge": "நிலை 2: உறுதிப்பாடு (Sustain)",
        "tier_color": "#e9c46a",
        "letters": ["ப"],
        "title": "பொறையுடைமை, பெரியாரைத் துணைக்கோடல் & பக்தி",
        "english_title": "Forbearance under Insult, Seeking Noble Mentors & Deep Devotion",
        "description": "துன்பமும் ஏளனமும் வரும்போது நிலம் போலப் பொறுமை காத்தல்; ஆன்மீகப் பெரியோர்களின் துணையை நாடி நிற்றல்.",
        "virtues": [
            {
                "letter": "ப",
                "virtue": "பொறையுடைமை (Forbearance & Tolerance)",
                "verse": "அகழ்வாரைத் தாங்கும் நிலம்போலத் தம்மை இகழ்வார்ப் பொறுத்தல் தலை — திருக்குறள் 151 / பெரியாரைத் துணைக்கோடல்",
                "meaning": "தன்னைத் தோண்டுபவரையும் தாங்கும் பூமியைப் போல, தம்மை இகழ்ந்து பேசுபவரையும் பொறுத்துக் கொள்வதே தலைசிறந்த பண்பு.",
                "exercise": "கோபமூட்டும் சொற்களை எதிர்கொள்ளும்போது வன்முறையோ மறுபழிச்சொல்லோ இன்றி பொறுமையோடு புன்னகையுடன் கையாளுதல்."
            }
        ]
    },
    9: {
        "tier": "Tier 3: நிலைநிறுத்துதல் & காத்தல் (To Maintain & Uphold under Adversity)",
        "tier_badge": "நிலை 3: நிலைநிறுத்துதல் (Maintain)",
        "tier_color": "#e76f51",
        "letters": ["ம"],
        "title": "மனத்தூய்மை, அழுக்காறாமை & சான்றாண்மை",
        "english_title": "Inner Purity, Freedom from Envy & Resolute Character",
        "description": "வெளியில் நல்லவராகக் காட்டி உள்ளத்தில் மாசோடு வாழாமல், மனசாட்சிக்கு விரோதமில்லாத அகத்தூய்மையை நிலைநிறுத்துதல்.",
        "virtues": [
            {
                "letter": "ம",
                "virtue": "மனத்தூய்மை & அழுக்காறாமை (Purity of Mind & Soul)",
                "verse": "மனத்துக்கண் மாசிலன் ஆதல் அனைத்தறன் ஆகுல நீர பிற — திருக்குறள் 34 / மன்னிக்கப் பழகு",
                "meaning": "மனதில் குற்றம் இல்லாமல் வாழ்வதே அறத்தின் முழுமை; மற்ற ஆரவாரச் சடங்குகள் எல்லாம் பயனற்ற வெற்று ஆரவாரங்களே.",
                "exercise": "யாரும் பார்க்காத தனிமையிலும் மனதில் தீய எண்ணங்கள், காழ்ப்புணர்ச்சி வராமல் சிவ சிந்தனையோடு மனதை தூய்மையாக வைத்தல்."
            }
        ]
    },
    10: {
        "tier": "Tier 3: நிலைநிறுத்துதல் & காத்தல் (To Maintain & Uphold under Adversity)",
        "tier_badge": "நிலை 3: நிலைநிறுத்துதல் (Maintain)",
        "tier_color": "#e76f51",
        "letters": ["ய", "வ"],
        "title": "யாதும் ஊரே — சமநோக்கு & எந்தச் சூழலிலும் வாய்மை",
        "english_title": "Cosmic Brotherhood, Universal Vision & Absolute Truthfulness",
        "description": "குறுகிய எல்லைகளைக் கடந்து உலக மாந்தர் அனைவரையும் உடன் பிறந்தாராகப் பார்த்தல்; எந்தச் சோதனை வந்தாலும் வாய்மை தவறாமை.",
        "virtues": [
            {
                "letter": "ய",
                "virtue": "யாதும் ஊரே — சமநோக்கு (Cosmic Brotherhood)",
                "verse": "யாதும் ஊரே யாவரும் கேளிர் தீதும் நன்றும் பிறர்தர வாரா — புறநானூறு 192 / யாகாவா ராயினும் நாகாக்க — திருக்குறள் 127",
                "meaning": "எல்லா ஊர்களும் எம் ஊரே; எல்லா மக்களும் எம் உறவினரே. நன்மையும் தீமையும் பிறரால் வருவதில்லை, நம் செயல்களாலேயே வருகின்றன.",
                "exercise": "சாதி, மதம், மொழி, தேச பேதங்களின்றி மனிதநேயத்தோடு அனைவரிடமும் சமநோக்குடன் பழகுதல்."
            },
            {
                "letter": "வ",
                "virtue": "வாய்மை — தீமையில்லாத உண்மை (Absolute Truthfulness)",
                "verse": "வாய்மை எனப்படுவது யாதெனின் யாதொன்றும் தீமை இலாத சொலல் — திருக்குறள் 291 / வினைத்திட்பம்",
                "meaning": "எந்த உயிருக்கும் ஒரு சிறிதும் தீங்கு விளைவிக்காத நன்மையான சொற்களைப் பேசுவதே வாய்மையாகும்.",
                "exercise": "தமக்கு நஷ்டமோ தண்டனையோ ஏற்படும் சூழ்நிலையிலும் துணிவோடு உண்மையை நிலைநாட்டுதல்."
            }
        ]
    },
    11: {
        "tier": "Tier 3: நிலைநிறுத்துதல் & காத்தல் (To Maintain & Uphold under Adversity)",
        "tier_badge": "நிலை 3: நிலைநிறுத்துதல் (Maintain)",
        "tier_color": "#e76f51",
        "letters": ["ழ", "ள"],
        "title": "விழுப்பம் — ஒழுக்கத்தை உயிரினும் மேலாகப் பேணல் & அவாவறுத்தல்",
        "english_title": "Moral Excellence Beyond Life Itself & Transcendence of Desires",
        "description": "உயிரே போகும் நிலை வரினும் தன் ஒழுக்க நெறியைக் கைவிடாமை; உலகியல் மாயைகளில் சிக்காமல் பற்றற்ற ஞான வாழ்வை நிலைநிறுத்துதல்.",
        "virtues": [
            {
                "letter": "ழ",
                "virtue": "விழுப்பம் — ஒழுக்க மேன்மை (Highest Moral Excellence)",
                "verse": "ஒழுக்கம் விழுப்பம் தரலான் ஒழுக்கம் உயிரினும் ஓம்பப் படும் — திருக்குறள் 131",
                "meaning": "ஒழுக்கமே மனிதனுக்குச் சிறப்பைத் தரும்; ஆகவே அவ்வொழுக்கத்தை உயிரை விடவும் மேலானதாகப் போற்றிக் காக்க வேண்டும்.",
                "exercise": "பிரபலமான சமூக அழுத்தங்கள், கவர்ச்சிகள், நண்பர்களின் தூண்டுதல்கள் இருப்பினும் தன் ஆன்மீகக் கொள்கையில் தளராமல் நிற்றல்."
            },
            {
                "letter": "ள",
                "virtue": "அவாவறுத்தல் & எளிமை (Transcendence of Greed & Simplicity)",
                "verse": "வேண்டுங்கால் வேண்டும் பிறவாமை மற்றது வேண்டாமை வேண்ட வரும் — திருக்குறள் 362",
                "meaning": "ஒருவன் எதையாவது விரும்ப வேண்டுமானால், பிறப்பற்ற முக்தியையே விரும்ப வேண்டும்; அது ஆசைகளை அறுத்தலாலேயே கிட்டும்.",
                "exercise": "ஆடம்பரம், பகட்டு, வீண் நுகர்வுப் பழக்கங்களைத் துறந்து எளிய தெய்வீக வாழ்வை மனதாரப் பின்பற்றுதல்."
            }
        ]
    },
    12: {
        "tier": "Tier 3: முழுமை & முக்தி நிலை (Mastery, Cosmic Dharma & Surrender)",
        "tier_badge": "நிலை 3: ஞான முழுமை (Mastery)",
        "tier_color": "#e76f51",
        "letters": ["ற", "ன"],
        "title": "அறநெறி வழுவாமை & சிவானந்தப் பூரண சரணாகதி",
        "english_title": "Unyielding Steadfastness in Dharma & Ultimate Divine Union",
        "description": "இறைவனோடு இரண்டறக் கலக்கும் சிவானந்தப் பெருநிலை; உலகியல் மாயைகள் முற்றிலுமாக ஒழிந்து அன்பே சிவமாய் வாழும் ஜீவன்முக்தி நிலை.",
        "virtues": [
            {
                "letter": "ற",
                "virtue": "அறநெறி வழுவாமை (Unyielding Cosmic Dharma)",
                "verse": "அறத்தாறு இதுவென வேண்டா சிவிகை பொறுத்தானோடு ஊர்ந்தான் இடை — திருக்குறள் 37 / மேன்மைகொள் சைவநீதி விளங்குக உலகம் எல்லாம் — தேவாரம்",
                "meaning": "பல்லக்கைச் சுமப்பவனுக்கும் அதில் ஏறிச் செல்பவனுக்கும் இடையில் உள்ள அறத்தின் பயனை உணர்ந்து எக்காலத்தும் அறநெறி தவறாமை.",
                "exercise": "வாழ்வின் இன்ப துன்பங்கள், வெற்றி தோல்விகள் இரண்டையும் சமமாகப் பாவித்து தர்மத்தை மட்டுமே உறுதியாகப் பற்றிக்கொள்ளுதல்."
            },
            {
                "letter": "ன",
                "virtue": "நன்னெறி நிறைவு — அன்பே சிவம் & பூரண சரணாகதி (Supreme Divine Realization)",
                "verse": "அன்பும் சிவமும் இரண்டென்பர் அறிவிலார் அன்பே சிவமாவது ஆரும் அறிகிலார் — திருமந்திரம் (திருமூலர்) / சிவோஹம் பாவனை",
                "meaning": "அன்பும் சிவமும் தனித்தனியானவை அல்ல; தூய அன்பே சிவம் என்பதை உணர்ந்து சகல ஜீவராசிகளிடத்தும் பரம்பொருளைக் காணும் பேரானந்த நிலை.",
                "exercise": "'யான்' 'எனது' என்ற அகந்தையை முழுமையாக ஈசனின் திருவடிகளில் சமர்ப்பித்து, உலக நன்மைக்காகவே தன் வாழ்க்கையை அர்ப்பணித்தல்."
            }
        ]
    }
}

def generate_grade_virtue_box(grade):
    data = VIRTUES_BY_GRADE.get(grade)
    if not data:
        return ""

    letters_str = " • ".join(f"‘{l}’" for l in data["letters"])
    virtues_html = ""
    for v in data["virtues"]:
        virtues_html += f"""
        <div style="background: rgba(0, 0, 0, 0.4); border-left: 3px solid var(--gold); border-radius: 0 10px 10px 0; padding: 14px 18px; margin-bottom: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
            <div style="color: var(--gold-bright); font-size: 1.05rem; font-weight: 700;">
              <span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">{v['letter']}</span>
              {v['virtue']}
            </div>
            <span style="font-size: 0.76rem; color: var(--gold-soft); background: rgba(212,175,55,0.12); padding: 2px 10px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.25);">தரம் {grade} இலக்கு</span>
          </div>
          <div style="font-family: 'Mukta Malar', serif; font-size: 0.98rem; color: #fff; line-height: 1.6; margin-bottom: 6px; font-weight: 500;">
            📖 <em>{v['verse']}</em>
          </div>
          <div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; margin-bottom: 8px;">
            💡 <strong>விளக்கம்:</strong> {v['meaning']}
          </div>
          <div style="background: rgba(42, 157, 143, 0.08); border: 1px solid rgba(42, 157, 143, 0.25); border-radius: 6px; padding: 8px 12px; font-size: 0.88rem; color: #b7e4c7; line-height: 1.5;">
            🎯 <strong>மாணவர் அன்றாடப் பயிற்சி (Daily Practice):</strong> {v['exercise']}
          </div>
        </div>
        """

    box_html = f"""
    <!-- Alphabets to Virtue Mapping Section (Grade {grade} Specific) -->
    <section class="scripture-study-section" style="margin-top: 36px; margin-bottom: 36px; border: 1px solid var(--border-gold-hover); background: rgba(15, 18, 26, 0.95); box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; border-bottom: 1px solid rgba(212,175,55,0.2); padding-bottom: 10px;">
        <span class="source-badge" style="background: linear-gradient(135deg, #d4af37, #996515); color: #000; font-weight: 800;">🔤 அகர வரிசை நற்பண்பு நெறிமுறைமை • தரம் {grade}</span>
        <span style="background: {data['tier_color']}22; color: {data['tier_color']}; border: 1px solid {data['tier_color']}55; padding: 4px 12px; border-radius: 14px; font-size: 0.8rem; font-weight: 700;">
          {data['tier_badge']}
        </span>
      </div>

      <h2 style="color: var(--gold-bright); font-size: 1.35rem; margin-bottom: 8px;">
        எழுத்துகள் {letters_str} — {data['title']}
      </h2>
      <div style="font-size: 0.88rem; color: var(--gold-soft); margin-bottom: 14px; font-weight: 600;">
        {data['english_title']} • {data['tier']}
      </div>
      <p style="color: var(--text-main); font-size: 0.95rem; line-height: 1.7; margin-bottom: 20px;">
        {data['description']}
      </p>

      <div class="virtues-container">
        {virtues_html}
      </div>

      <div style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed rgba(212,175,55,0.2); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 0.82rem; color: var(--text-muted);">
        <span>🌱 படிப்படியான நற்பண்பு வளர்ச்சி: கற்றல் (Grades 1-4) ➔ பின்பற்றுதல் (Grades 5-8) ➔ நிலைநிறுத்துதல் (Grades 9-12)</span>
        <a href="kalvi.html#virtue-mapping" style="color: var(--gold); text-decoration: none; font-weight: 700;">அனைத்து 12 தரங்களின் நற்பண்பு அட்டவணை ↗</a>
      </div>
    </section>
    """
    return box_html

def update_grade_file(filepath, grade):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has virtue section
    if 'அகர வரிசை நற்பண்பு நெறிமுறைமை' in content:
        # replace existing section if already present
        content = re.sub(
            r'<!-- Alphabets to Virtue Mapping Section.*?<!-- Detailed Learning Units',
            generate_grade_virtue_box(grade) + '\n\n    <!-- Detailed Learning Units',
            content,
            flags=re.DOTALL
        )
    else:
        # insert before Detailed Learning Units or Core Lessons
        target = '<!-- Detailed Learning Units / Master Lessons -->'
        if target in content:
            content = content.replace(target, generate_grade_virtue_box(grade) + '\n\n    ' + target)
        else:
            # fallback: insert before lessons-container or cards-grid
            target2 = '<div class="lessons-container">'
            if target2 in content:
                content = content.replace(target2, generate_grade_virtue_box(grade) + '\n\n    ' + target2)
            else:
                # insert before footer
                target3 = '<footer class="site-footer">'
                content = content.replace(target3, generate_grade_virtue_box(grade) + '\n\n  ' + target3)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def generate_kalvi_virtue_hub():
    rows_html = ""
    for g in range(1, 13):
        data = VIRTUES_BY_GRADE[g]
        letters_str = " ".join(data["letters"])
        virtues_summary = ", ".join(v["virtue"].split("(")[0].strip() for v in data["virtues"])
        first_verse = data["virtues"][0]["verse"].split("—")[0].strip()
        rows_html += f"""
        <tr style="border-bottom: 1px solid rgba(212,175,55,0.15);">
          <td style="padding: 12px 14px; font-weight: 700; color: var(--gold-bright); white-space: nowrap;">
            <a href="tharam-{g}.html" style="color: var(--gold-bright); text-decoration: none;">தரம் {g} (Gr {g}) ↗</a>
          </td>
          <td style="padding: 12px 14px; font-weight: 800; font-size: 1.15rem; color: var(--gold); letter-spacing: 2px;">
            {letters_str}
          </td>
          <td style="padding: 12px 14px;">
            <span style="background: {data['tier_color']}22; color: {data['tier_color']}; border: 1px solid {data['tier_color']}55; padding: 2px 8px; border-radius: 10px; font-size: 0.74rem; font-weight: 700; display: inline-block; white-space: nowrap;">
              {data['tier_badge']}
            </span>
          </td>
          <td style="padding: 12px 14px; color: var(--text-main); font-weight: 600;">
            {virtues_summary}
          </td>
          <td style="padding: 12px 14px; font-family: 'Mukta Malar', serif; font-size: 0.92rem; color: var(--gold-soft); font-style: italic;">
            "{first_verse}"
          </td>
          <td style="padding: 12px 14px; text-align: center; white-space: nowrap;">
            <a href="tharam-{g}.html" class="tag" style="padding: 4px 10px; border-radius: 12px; background: rgba(212,175,55,0.1); border: 1px solid var(--border-gold); text-decoration: none; font-size: 0.78rem;">
              பயிற்சி காண்க ↗
            </a>
          </td>
        </tr>
        """

    hub_html = f"""
    <!-- Complete Master Alphabets to Virtue Hub -->
    <section class="scripture-study-section" id="virtue-mapping" style="margin-top: 40px; margin-bottom: 40px; border: 1px solid var(--border-gold-hover); background: rgba(14, 17, 24, 0.95); padding: 32px 28px; border-radius: 18px; box-shadow: 0 15px 40px rgba(0,0,0,0.6);">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
        <span class="source-badge" style="background: var(--gold-gradient); color: #000; font-weight: 800; font-size: 0.85rem;">
          ✨ அகர வரிசை நற்பண்பு நெறிமுறைமை (Alphabets to Virtue Progression) ✨
        </span>
        <span style="color: var(--gold-soft); font-size: 0.85rem; font-weight: 600;">
          12 வகுப்புகள் • 3 முதிர்ச்சி நிலைகள் • 30+ நற்பண்புகள்
        </span>
      </div>

      <h2 style="color: var(--gold-bright); font-size: 1.6rem; margin-bottom: 10px;">
        தமிழ் எழுத்து முதல் தர்ம முழுமை வரை — படிப்படியான நற்பண்பு வளர்ச்சி
      </h2>
      <p style="color: var(--text-muted); font-size: 0.96rem; line-height: 1.7; max-width: 900px; margin-bottom: 24px;">
        ஆத்திசூடி, கொன்றை வேந்தன், திருக்குறள் மற்றும் பன்னிரு திருமுறைகளின் வழியில், தமிழ் எழுத்துக்களோடு மாணவர்களின் நற்பண்புகளையும் ஒழுக்கத்தையும் படிப்படியாகக் கற்பித்து, பின்பற்றி, சோதனைகளிலும் நிலைநிறுத்தும் முழுமையான ஆன்மீகப் பாடத்திட்ட வரைபடம்.
      </p>

      <!-- 3 Tier Progression Architecture Cards -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin-bottom: 28px;">
        <div style="background: rgba(42, 157, 143, 0.08); border: 1px solid rgba(42, 157, 143, 0.3); border-radius: 12px; padding: 18px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="font-size: 1.3rem;">🟢</span>
            <h4 style="color: #2a9d8f; margin: 0; font-size: 1.05rem;">நிலை 1: அறிதல் &amp; கற்றல் (To Learn)</h4>
          </div>
          <div style="font-size: 0.8rem; color: var(--gold-soft); margin-bottom: 8px; font-weight: 700;">தரம் 1 முதல் தரம் 4 வரை (தொடக்க நிலை)</div>
          <p style="color: var(--text-main); font-size: 0.86rem; line-height: 1.6; margin: 0;">
            அறம், அன்பு, ஆறுதல், இன்சொல், ஈகை, உண்மை, ஊக்கம், பெற்றோரை மதித்தல் மற்றும் ஜீவகாருண்யம் ஆகிய அடிப்படை நற்பண்புகளை அறிந்து ஆர்வத்துடன் பழகுதல்.
          </p>
        </div>

        <div style="background: rgba(233, 196, 106, 0.08); border: 1px solid rgba(233, 196, 106, 0.3); border-radius: 12px; padding: 18px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="font-size: 1.3rem;">🟡</span>
            <h4 style="color: #e9c46a; margin: 0; font-size: 1.05rem;">நிலை 2: செய்தல் &amp; பின்பற்றுதல் (To Follow)</h4>
          </div>
          <div style="font-size: 0.8rem; color: var(--gold-soft); margin-bottom: 8px; font-weight: 700;">தரம் 5 முதல் தரம் 8 வரை (நடுநிலை)</div>
          <p style="color: var(--text-main); font-size: 0.86rem; line-height: 1.6; margin: 0;">
            செய்த நன்றியை மறவாமை, ஐம்பொறி அடக்கம், வெகுளாமை (சினமின்மை), நடுவுநிலைமை, பொறையுடைமை மற்றும் கடமை உணர்வை வாழ்க்கையில் தொடர்ச்சியாகக் கடைப்பிடித்தல்.
          </p>
        </div>

        <div style="background: rgba(231, 111, 81, 0.08); border: 1px solid rgba(231, 111, 81, 0.3); border-radius: 12px; padding: 18px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="font-size: 1.3rem;">🔴</span>
            <h4 style="color: #e76f51; margin: 0; font-size: 1.05rem;">நிலை 3: நிலைநிறுத்துதல் &amp; காத்தல் (To Maintain)</h4>
          </div>
          <div style="font-size: 0.8rem; color: var(--gold-soft); margin-bottom: 8px; font-weight: 700;">தரம் 9 முதல் தரம் 12 வரை (உயர்நிலை &amp; மேல்நிலை)</div>
          <p style="color: var(--text-main); font-size: 0.86rem; line-height: 1.6; margin: 0;">
            அழுக்காறாமை (பொறாமையின்மை), எந்தச் சூழலிலும் வாய்மை, சான்றாண்மை, உலகியல் ஆசைகளை அறுத்த அவாவறுத்தல், தர்மத்தில் உறுதியோடு நின்று சிவானந்த சரணாகதி அடைதல்.
          </p>
        </div>
      </div>

      <!-- Master Matrix Table -->
      <div style="overflow-x: auto; background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid var(--border-gold);">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.88rem;">
          <thead>
            <tr style="background: rgba(212,175,55,0.12); border-bottom: 2px solid var(--border-gold);">
              <th style="padding: 12px 14px; color: var(--gold-bright); font-weight: 700;">வகுப்பு / தரம்</th>
              <th style="padding: 12px 14px; color: var(--gold-bright); font-weight: 700;">எழுத்துகள்</th>
              <th style="padding: 12px 14px; color: var(--gold-bright); font-weight: 700;">முதிர்ச்சி நிலை</th>
              <th style="padding: 12px 14px; color: var(--gold-bright); font-weight: 700;">நற்பண்புகள் (Virtues)</th>
              <th style="padding: 12px 14px; color: var(--gold-bright); font-weight: 700;">மூலப் பாடல் மேற்கோள்</th>
              <th style="padding: 12px 14px; color: var(--gold-bright); font-weight: 700; text-align: center;">விரிவுரை</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
    </section>
    """
    return hub_html

def update_kalvi_page(filepath):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    hub_html = generate_kalvi_virtue_hub()
    if 'id="virtue-mapping"' in content:
        # replace existing section
        content = re.sub(
            r'<!-- Complete Master Alphabets to Virtue Hub.*?<!-- 3 Tier Progression',
            hub_html,
            content,
            flags=re.DOTALL
        )
    else:
        # insert before section-divider-title (அனைத்து 12 தரங்களின் பாடநெறி)
        target = '<h2 class="section-divider-title">அனைத்து 12 தரங்களின் பாடநெறி'
        if target in content:
            content = content.replace(target, hub_html + '\n\n    ' + target)
        else:
            target2 = '<div class="grades-grid">'
            content = content.replace(target2, hub_html + '\n\n    ' + target2)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def update_syllabus_page(filepath):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    hub_html = generate_kalvi_virtue_hub()
    if 'id="virtue-mapping"' not in content:
        target = '<footer class="site-footer">'
        if target in content:
            content = content.replace(target, hub_html + '\n\n  ' + target)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("Starting Alphabets to Virtue Mapping integration across all pages...")
    
    # 1. Update kalvi.html
    for p in ['kalvi.html', 'docs/kalvi.html', 'site/kalvi.html']:
        if update_kalvi_page(p):
            print(f"Updated virtue hub in: {p}")

    # 2. Update syllabus.html
    for p in ['syllabus.html', 'docs/syllabus.html', 'site/syllabus.html']:
        if update_syllabus_page(p):
            print(f"Updated virtue hub in syllabus: {p}")

    # 3. Update all 12 Grade pages (tharam-1 to tharam-12)
    for g in range(1, 13):
        for prefix in ['', 'docs/', 'site/']:
            fname = f"{prefix}tharam-{g}.html"
            if update_grade_file(fname, g):
                print(f"Updated Grade {g} virtue section in: {fname}")

    print("Successfully integrated Alphabets to Virtue Mapping across all class levels!")

if __name__ == '__main__':
    main()
