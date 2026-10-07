"""
upgrade_thirukkural_cinema.py
Enriches thirukkural.html cinema theatre and catalog with all 12 produced master films:
Chapters: 5, 8, 16, 25, 26, 27, 30, 31, 52, 54, 57, 61.
Mirrors across root ./, docs/, and site/.
"""

import os
import re
import json

ALL_CHAPTERS = [5, 8, 16, 25, 26, 27, 30, 31, 52, 54, 57, 61]

CHAPTER_INFO = {
    5: {
        "num": 5,
        "tabTitle": "அதிகாரம் 5: இல்வாழ்க்கை",
        "tabSub": "இல்லற தர்மம் &amp; அதிவேக முக்தி (35 காட்சிகள்)",
        "badge": "அதிகாரம் 5",
        "cat": "அறத்துப்பால் • இல்லறவியல்",
        "title": "இல்வாழ்க்கை (Domestic Virtue & Grihastha Dharma)",
        "desc": "அறநெறி பிறழாது, குடும்ப உறுப்பினர்களை அரவணைத்து, துறவிகளுக்கும் உலக உயிர்களுக்கும் துணையாக நின்று குடும்பம் நடத்தும் தலையாய வாழ்க்கை.",
        "verse": '"இயல்பினான் இல்வாழ்க்கை வாழ்பவன் என்பான்<br>முயல்வாருள் எல்லாம் தலை" (குறள் 47)',
        "meaning": "பொருள்: இல்லறத்திற்குரிய நல்லியல்புகளோடு வாழ்வாங்கு வாழ்பவன், முக்தி பெற கடுமையாக முயலும் மற்ற துறவிகள் அனைவரிலும் தலைசிறந்தவன் ஆவான்.",
        "living": "இல்லறக் கடமைகளை ஈஸ்வர அர்ப்பணமாய் ஏற்று, சுயநலத்தை மாய்த்து, அனைவரிடமும் அன்பு செலுத்துவதே அதிவேக முக்தி நெறியாகும்.",
        "fullVideo": "assets/videos/adhikaram_05_ilvaazhkkai.mp4",
        "shortVideo": "assets/videos/short_05_grihastha.mp4",
        "poster": "assets/images/lessons/grade8_chatur_ashrama.jpg",
        "youtubeId": "CUMZcTM4y7w",
        "fullDur": "கால அளவு: ~5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    8: {
        "num": 8,
        "tabTitle": "அதிகாரம் 8: அன்புடைமை",
        "tabSub": "வற்றாத மனிதநேயம் &amp; பிரபஞ்ச நேயம் (32 காட்சிகள்)",
        "badge": "அதிகாரம் 8",
        "cat": "அறத்துப்பால் • இல்லறவியல்",
        "title": "அன்புடைமை (Loving-Kindness & Universal Affection)",
        "desc": "எல்லா உயிர்களிடத்தும் வற்றாத அன்பு செலுத்தி, தன்னுயிர் போல் பிறரையும் போற்றி வாழும் உயர்ந்த மனிதநேயப் பண்பு.",
        "verse": '"அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார்<br>என்பும் உரியர் பிறர்க்கு" (குறள் 72)',
        "meaning": "பொருள்: அன்பில்லாதவர் எல்லாப் பொருட்களையும் தமக்கே உரியதாகக் கொள்வர்; ஆனால் அன்புடையவரோ தம் எலும்பையும் பிறர்க்குத் தந்து வாழ்வர்.",
        "living": "சுயநலத்தைத் துறந்து, குடும்பத்திலும் சமுதாயத்திலும் எல்லைகளற்ற தூய அன்பைப் பொழிந்து அனைவரையும் அரவணைத்தல்.",
        "fullVideo": "assets/videos/adhikaram_08_anbudaimai.mp4",
        "shortVideo": "assets/videos/short_08_love.mp4",
        "poster": "assets/images/lessons/harvesting_family_dharma.jpg",
        "youtubeId": "6OUebTuktZI",
        "fullDur": "கால அளவு: ~5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    16: {
        "num": 16,
        "tabTitle": "அதிகாரம் 16: பொறையுடைமை",
        "tabSub": "பூமி போன்ற பொறுமையும் பெருமன்னிப்பும் (34 காட்சிகள்)",
        "badge": "அதிகாரம் 16",
        "cat": "அறத்துப்பால் • இல்லறவியல்",
        "title": "பொறையுடைமை (Forbearance & Supreme Forgiveness)",
        "desc": "பிறர் செய்யும் தீமைகளையும் நிந்தனைகளையும் பூமியைப் போல பொறுத்துக்கொண்டு அவர்களை மன்னித்தருளும் பெருந்தன்மை.",
        "verse": '"அகழ்வாரைத் தாங்கும் நிலம்போலத் தம்மை<br>இகழ்வார்ப் பொறுத்தல் தலை" (குறள் 151)',
        "meaning": "பொருள்: தன்னைத் தோண்டுபவரையும் தாங்கும் பூமியைப் போல, தன்னை இகழ்ந்து பேசுபவரையும் பொறுத்துக் கொள்வதே தலையாய அறமாகும்.",
        "living": "கோபத்தை வென்று, பிறர் செய்யும் தவறுகளைப் பெருந்தன்மையோடு மன்னித்து சாந்தியை நிலைநாட்டுதல்.",
        "fullVideo": "assets/videos/adhikaram_16_poraiyudaimai.mp4",
        "shortVideo": "assets/videos/short_16_patience.mp4",
        "poster": "assets/images/lessons/wise_counsel_nobility.jpg",
        "youtubeId": "juGQ6ncADIg",
        "fullDur": "கால அளவு: ~5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    25: {
        "num": 25,
        "tabTitle": "அதிகாரம் 25: அருளுடைமை",
        "tabSub": "அனைத்து ஜீவராசிகளிடமும் இறையருள் (30 காட்சிகள்)",
        "badge": "அதிகாரம் 25",
        "cat": "அறத்துப்பால் • துறவறவியல்",
        "title": "அருளுடைமை (Universal Grace & Compassion)",
        "desc": "எந்தவித எதிர்பார்ப்புமின்றி உலகத்து எளிய உயிர்களிடத்தும் கருணை காட்டி, துன்பம் தீர்க்கும் பேரருள் நெறி.",
        "verse": '"அருட்செல்வம் செல்வத்துள் செல்வம் பொருட்செல்வம்<br>பூரியார் கண்ணும் உள" (குறள் 241)',
        "meaning": "பொருள்: உயிர்கள் மீது காட்டும் அருளாகிய செல்வமே செல்வங்களில் தலையாயது; பொருட்செல்வமோ இழிந்தவர்களிடத்திலும் இருக்கும்.",
        "living": "வாய் பேச முடியாத உயிர்களிடத்தும் ஆதரவற்றோரிடத்தும் இறைவனைக் கண்டு அருள்புரிவதே மெய்யான தர்மம்.",
        "fullVideo": "assets/videos/adhikaram_25_aruludaimai.mp4",
        "shortVideo": "assets/videos/short_25_grace.mp4",
        "poster": "assets/images/lessons/sage_universal_compassion.jpg",
        "youtubeId": "rm7aFPyapA0",
        "fullDur": "கால அளவு: ~5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    26: {
        "num": 26,
        "tabTitle": "அதிகாரம் 26: புலால் உண்ணாமை",
        "tabSub": "அஹிம்சை &amp; ஜீவகாருண்யம் (46 காட்சிகள்)",
        "badge": "அதிகாரம் 26",
        "cat": "அறத்துப்பால் • துறவறவியல்",
        "title": "புலால் உண்ணாமை (Abstinence from Flesh)",
        "desc": "பிற உயிர்களைத் தன்னுயிர் போல் கருதி, அவைகளின் உடலைத் தன் உடலை வளர்க்க உண்ணாது வாழும் மாபெரும் ஜீவகாருண்ய அறம்.",
        "verse": '"தன்னுன் பெருக்கற்குத் தான்பிறி தூனுண்ணும்<br>எங்ஙனம் ஆளும் அருள்" (குறள் 251)',
        "meaning": "பொருள்: தன் உடலைப் பருக்கச் செய்வதற்காகத் தான் மற்றோர் உயிரின் உடலைத் தின்னும் மனிதன், எவ்வாறு அருளுடையவனாக இருக்க முடியும்?",
        "living": "எவ்வுயிர்க்கும் அன்பு செய்து, உன்னத இல்லறத்தை அஹிம்சை நெறியில் வாழ்ந்து காட்டுவதே அதிவேக முக்தியாகும்.",
        "fullVideo": "assets/videos/adhikaram_26_pulaal_unnaamai.mp4",
        "shortVideo": "assets/videos/short_26_ahimsa.mp4",
        "poster": "assets/images/lessons/noble_feast_ahimsa.jpg",
        "youtubeId": "MoNK5N2chcg",
        "fullDur": "கால அளவு: 4.5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 42 வினாடிகள் • வேகக் குறும்படம்"
    },
    27: {
        "num": 27,
        "tabTitle": "அதிகாரம் 27: தவம்",
        "tabSub": "ஆழ்ந்த நோன்பும் மனக் கட்டுப்பாடும் (30 காட்சிகள்)",
        "badge": "அதிகாரம் 27",
        "cat": "அறத்துப்பால் • துறவறவியல்",
        "title": "தவம் (Austerity & Inner Mastery)",
        "desc": "தனக்கு வரும் துன்பங்களைப் பொறுத்துக்கொண்டு, பிற உயிர்களுக்கு எந்தத் துன்பமும் செய்யாமல் ஐம்பொறிகளை அடக்கும் மன உறுதி.",
        "verse": '"உற்றநோய் நோன்றல் உயிர்க்குறுகண் செய்யாமை<br>அற்றே தவத்திற் குரு" (குறள் 261)',
        "meaning": "பொருள்: தனக்கு நேரும் துன்பங்களைப் பொறுத்துக் கொள்ளுதலும், பிற உயிர்களுக்குத் துன்பம் செய்யாமையுமே தவத்தின் உண்மையான வடிவமாகும்.",
        "living": "சோதனைகள் வரும்போது மனந்தளராமல் பொறுமை காத்து, தினசரி தர்மக் கடமையை ஆத்மார்த்தமாக நிறைவேற்றுவதே சிறந்த தவம்.",
        "fullVideo": "assets/videos/adhikaram_27_thavam.mp4",
        "shortVideo": "assets/videos/short_27_thavam.mp4",
        "poster": "assets/images/lessons/thavam_tapas_meditation.jpg",
        "youtubeId": "sa5f7NcYuRQ",
        "fullDur": "கால அளவு: 4.5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    30: {
        "num": 30,
        "tabTitle": "அதிகாரம் 30: வாய்மை",
        "tabSub": "சத்திய விரதமும் தூய சொல்லும் (30 காட்சிகள்)",
        "badge": "அதிகாரம் 30",
        "cat": "அறத்துப்பால் • துறவறவியல்",
        "title": "வாய்மை (The Power of Absolute Truthfulness)",
        "desc": "எந்த ஒரு உயிருக்கும் தீமை பயக்காத நன்மையை விளைவிக்கும் தூய சத்தியத்தை மட்டுமே பேசி வாழும் வாய்மை நெறி.",
        "verse": '"வாய்மை எனப்படுவது யாதெனின் யாதொன்றும்<br>தீமை இலாத சொலல்" (குறள் 291)',
        "meaning": "பொருள்: வாய்மை என்று கூறப்படுவது எதுவென்றால், யாருக்கும் சிறிதும் தீமை தராத தூய சொற்களைப் பேசுவதே ஆகும்.",
        "living": "பேச்சிலும் சிந்தனையிலும் செயலிலும் பொய்ம்மையை நீக்கி, சத்தியத்தின் வழியில் நின்றால் சகல புண்ணியங்களும் கைகூடும்.",
        "fullVideo": "assets/videos/adhikaram_30_vaaimai.mp4",
        "shortVideo": "assets/videos/short_30_truth.mp4",
        "poster": "assets/images/lessons/scholar_palm_manuscript.jpg",
        "youtubeId": "fQspUClJyg8",
        "fullDur": "கால அளவு: ~5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    31: {
        "num": 31,
        "tabTitle": "அதிகாரம் 31: வெகுளாமை",
        "tabSub": "சினத்தை வென்று சாந்தி காத்தல் (30 காட்சிகள்)",
        "badge": "அதிகாரம் 31",
        "cat": "அறத்துப்பால் • துறவறவியல்",
        "title": "வெகுளாமை (Restraint from Anger & Inner Peace)",
        "desc": "தன்னால் தண்டிக்க முடிகின்ற எளியவரிடத்திலும் சினம் கொள்ளாமல் அடக்கி ஆளும் உன்னதமான சாந்த குணம்.",
        "verse": '"செல்லிடத்துக் காப்பான் சினங்காப்பான் அல்லிடத்துக்<br>காக்கின்என் காவாக்கால் என்" (குறள் 301)',
        "meaning": "பொருள்: தன் சினம் பலிக்கும் இடத்தில் கோபப்படாமல் காப்பவனே உண்மையிலேயே சினம் காப்பவன்; பலிக்காத இடத்தில் சினத்தைக் காத்தாலும் ஒன்றுதான், காக்காவிட்டாலும் ஒன்றுதான்.",
        "living": "சினம் எழும் வேளையில் சாந்த தியானத்தில் ஆழ்ந்து, ஆத்திரத்தை அடக்கி ஆன்ம பலத்தைப் பெருக்குதல்.",
        "fullVideo": "assets/videos/adhikaram_31_vegulaamai.mp4",
        "shortVideo": "assets/videos/short_31_anger.mp4",
        "poster": "assets/images/lessons/mountain_cave_tapas.jpg",
        "youtubeId": "xvkMEdaF7w4",
        "fullDur": "கால அளவு: ~5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    52: {
        "num": 52,
        "tabTitle": "அதிகாரம் 52: தெரிந்து வினையாடல்",
        "tabSub": "தகுதியறிந்து பொறுப்பளிக்கும் நிர்வாகம் (30 காட்சிகள்)",
        "badge": "அதிகாரம் 52",
        "cat": "பொருட்பால் • அமைச்சு / அரசியல்",
        "title": "தெரிந்து வினையாடல் (Discerning Management & Action)",
        "desc": "தகுதியான நபர்களை அவர்களின் அறிவு, ஒழுக்கம், விசுவாசம் ஆகியவற்றால் ஆய்ந்து அறிந்து, தகுந்த பணிகளில் பொறுப்பளிக்கும் மேலாண்மை நெறி.",
        "verse": '"இதனை இதனால் இவன்முடிக்கும் என்றாய்ந்து<br>அதனை அவன்கண் விடல்" (குறள் 517)',
        "meaning": "பொருள்: இந்தச் செயலை இக்கருவியினால் இவன் முடிப்பான் என்று தீர ஆராய்ந்து, அச்செயலை அவனிடம் ஒப்படைக்க வேண்டும்.",
        "living": "குடும்பத்திலும் சமுதாயத்திலும் சரியான நபர்களுக்கு மதிப்பளித்து பொறுப்புகளைப் பகிர்ந்து தலைமை தாங்கும் நிர்வாக மாண்பு.",
        "fullVideo": "assets/videos/adhikaram_52_therinthu_vinaiyaadal.mp4",
        "shortVideo": "assets/videos/short_52_vinai.mp4",
        "poster": "assets/images/lessons/royal_administration_dharma.jpg",
        "youtubeId": "Hq6XdaHfdfo",
        "fullDur": "கால அளவு: 6 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 45 வினாடிகள் • வேகக் குறும்படம்"
    },
    54: {
        "num": 54,
        "tabTitle": "அதிகாரம் 54: பொச்சாவாமை",
        "tabSub": "மறதியின்மையும் விழிப்புணர்வும் (30 காட்சிகள்)",
        "badge": "அதிகாரம் 54",
        "cat": "பொருட்பால் • அமைச்சு / ஆட்சி",
        "title": "பொச்சாவாமை (Unfailing Vigilance & Mindfulness)",
        "desc": "எக்காலத்திலும் கடமைகளில் மறதியும் கவனக்குறைவும் இன்றி, எப்போதும் விழிப்புணர்வுடன் செயலாற்றும் உயர் பண்பு.",
        "verse": '"இறந்த வெகுளியின் தீதே சிறந்த<br>உவகை மகிழ்ச்சியின் சோர்வு" (குறள் 531)',
        "meaning": "பொருள்: மிதமிஞ்சிய கோபத்தை விட, மிகுந்த மகிழ்ச்சியினால் உண்டாகும் கவனக்குறைவும் மறதியும் ஒருவருக்குப் பெருங்கேடு விளைவிக்கும்.",
        "living": "வெற்றி அல்லது மகிழ்ச்சிக் காலங்களிலும் தன் தர்மத்தையும் பணிவையும் மறக்காமல் எப்போதும் விழிப்புடன் வாழும் நெறி.",
        "fullVideo": "assets/videos/adhikaram_54_pochchaavaamai.mp4",
        "shortVideo": "assets/videos/short_54_vigilance.mp4",
        "poster": "assets/images/lessons/mindfulness_vigilance.jpg",
        "youtubeId": "2c3bdbcn4BI",
        "fullDur": "கால அளவு: 5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 40 வினாடிகள் • வேகக் குறும்படம்"
    },
    57: {
        "num": 57,
        "tabTitle": "அதிகாரம் 57: வெருவந்த செய்யாமை",
        "tabSub": "இன்சொல்லும் நீதியும் காக்கும் தலைமை (30 காட்சிகள்)",
        "badge": "அதிகாரம் 57",
        "cat": "பொருட்பால் • அரசியல் / சான்றாண்மை",
        "title": "வெருவந்த செய்யாமை (Gentle & Just Leadership)",
        "desc": "மக்களை அச்சுறுத்தும் கொடுஞ்செயல்களைச் செய்யாமல், இனிய முகத்தோடும் நியாயமான தீர்ப்போடும் தலைமை தாங்கும் நீதி நெறி.",
        "verse": '"இன்சொலான் ஈத்தளிக்க வல்லார்க்குத் தன்சொலான்<br>தான்கண் டனைத்திவ் வுலகு" (குறள் 568)',
        "meaning": "பொருள்: இன்சொல் கூறி, தக்கவர்க்குப் பொருளுதவி செய்து காக்க வல்ல தலைவனுக்கு, உலகம் அவன் விரும்புமாறு அமையும்.",
        "living": "வீட்டிலும் வெளியிலும் பயமுறுத்தும் அதிகாரமின்றி, இன்சொல்லாலும் அன்பாலும் அனைவரையும் வழிநடத்தும் குடும்பத் தலைவன் பண்பு.",
        "fullVideo": "assets/videos/adhikaram_57_veruvantha_seyyaamai.mp4",
        "shortVideo": "assets/videos/short_57_justice.mp4",
        "poster": "assets/images/lessons/gentle_justice_governance.jpg",
        "youtubeId": "3MOpXVMpA9s",
        "fullDur": "கால அளவு: 5.5 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 42 வினாடிகள் • வேகக் குறும்படம்"
    },
    61: {
        "num": 61,
        "tabTitle": "அதிகாரம் 61: மடியின்மை",
        "tabSub": "சோம்பலை வென்று உழைக்கும் மாண்பு (30 காட்சிகள்)",
        "badge": "அதிகாரம் 61",
        "cat": "பொருட்பால் • குடிசெயல்வகை",
        "title": "மடியின்மை (Conquering Sloth & Relentless Industry)",
        "desc": "சோம்பலை வேரறுத்து, சுறுசுறுப்புடனும் விடாமுயற்சியுடனும் உழைத்துத் தன் குடும்பத்தையும் சமுதாயத்தையும் உயர்த்தும் அறம்.",
        "verse": '"குடிமடிந்து குற்றம் பெருகும் மடிமடிந்து<br>மாண்ட உஞற்றி லவர்க்கு" (குறள் 604)',
        "meaning": "பொருள்: சோம்பலில் மூழ்கிச் சிறந்த முயற்சி செய்யாதவர்களுடைய குடும்பப் பெருமை அழியும்; குற்றங்கள் பெருகும்.",
        "living": "தினமும் அதிகாலை எழுந்து தன் உழைப்பை ஈசனுக்கே அர்ப்பணித்து, சோம்பலை மாய்த்து தன் குடும்பத்தை மாண்புறச் செய்தல்.",
        "fullVideo": "assets/videos/adhikaram_61_madiyinmai.mp4",
        "shortVideo": "assets/videos/short_61_industry.mp4",
        "poster": "assets/images/lessons/industrious_diligent_artisan.jpg",
        "youtubeId": "aV2BV7aQq6k",
        "fullDur": "கால அளவு: 4 நிமிடங்கள் • 1080p HD",
        "shortDur": "கால அளவு: 38 வினாடிகள் • வேகக் குறும்படம்"
    }
}

def generate_tabs_html():
    lines = ['      <!-- Chapter Tabs (All 12 Published Master Films) -->',
             '      <div class="cinema-chapter-tabs" style="display: flex; gap: 10px; overflow-x: auto; padding-bottom: 14px; margin-bottom: 20px;">']
    for num in ALL_CHAPTERS:
        info = CHAPTER_INFO[num]
        active_cls = " active" if num == 26 else ""
        bg_style = "background:rgba(229,169,60,0.15); border:1px solid var(--accent-gold); color:var(--accent-gold);" if num == 26 else "background:rgba(18,22,31,0.9); border:1px solid rgba(255,255,255,0.1); color:#94a3b8;"
        lines.append(f'        <button type="button" class="cinema-tab-btn{active_cls}" id="cin-tab-{num}" onclick="selectCinemaFilm({num})" style="{bg_style} padding:10px 16px; border-radius:10px; cursor:pointer; text-align:left; white-space:nowrap;">')
        lines.append(f'          <span style="font-weight:700; display:block;">{info["tabTitle"]}</span>')
        lines.append(f'          <span style="font-size:0.78rem; opacity:0.85;">{info["tabSub"]}</span>')
        lines.append('        </button>')
    lines.append('      </div>')
    return '\n'.join(lines)

def upgrade_file(filepath):
    print(f"Upgrading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the cinema-chapter-tabs block
    tabs_pattern = re.compile(r'<!-- Chapter Tabs -->\s*<div class="cinema-chapter-tabs".*?</div>\s*<!-- Main Cinema Display Grid', re.DOTALL)
    new_tabs = generate_tabs_html() + '\n\n      <!-- Main Cinema Display Grid'
    content = tabs_pattern.sub(new_tabs, content)

    # 2. Add the YouTube direct play button under video controls if not present
    yt_btn_markup = '<button type="button" class="cinema-yt-btn" id="btnCinemaYouTube" onclick="playCurrentCinemaFilmYouTube()" style="background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; border: none; padding: 6px 14px; border-radius: 8px; font-size: 0.82rem; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">▶️ யூடியூப் திரைப்படம் (YouTube 1080p)</button>'
    if 'id="btnCinemaYouTube"' not in content:
        content = content.replace(
            '<button type="button" class="cinema-mode-btn" id="btnModeShort"',
            f'{yt_btn_markup}\n              <button type="button" class="cinema-mode-btn" id="btnModeShort"'
        )

    # 3. Update CINEMA_FILMS_DATA in script
    cinema_data_json = json.dumps(CHAPTER_INFO, indent=6, ensure_ascii=False)
    cinema_data_code = f"const CINEMA_FILMS_DATA = {cinema_data_json};"
    
    cinema_data_pattern = re.compile(r'const CINEMA_FILMS_DATA = \{.*?\n    \};', re.DOTALL)
    content = cinema_data_pattern.sub(cinema_data_code, content)

    # 4. Update selectCinemaFilm JS function to support all 12 chapters and YouTube playback
    new_select_fn = f"""    const ALL_CINEMA_CHAPTER_NUMS = {json.dumps(ALL_CHAPTERS)};

    function selectCinemaFilm(chNum) {{
      currentCinemaChapter = chNum;
      const data = CINEMA_FILMS_DATA[chNum];
      if (!data) return;

      // Update Tab styling
      ALL_CINEMA_CHAPTER_NUMS.forEach(n => {{
        const btn = document.getElementById(`cin-tab-${{n}}`);
        if (btn) {{
          if (n === chNum) {{
            btn.style.background = 'rgba(229,169,60,0.15)';
            btn.style.borderColor = 'var(--accent-gold)';
            btn.style.color = 'var(--accent-gold)';
          }} else {{
            btn.style.background = 'rgba(18,22,31,0.9)';
            btn.style.borderColor = 'rgba(255,255,255,0.1)';
            btn.style.color = '#94a3b8';
          }}
        }}
      }});

      // Update Text details
      document.getElementById('cinemaChapterBadge').textContent = data.badge;
      document.getElementById('cinemaCategoryBadge').textContent = data.cat;
      document.getElementById('cinemaChapterTitle').textContent = data.title;
      document.getElementById('cinemaChapterDesc').textContent = data.desc;
      document.getElementById('cinemaKuralVerse').innerHTML = data.verse;
      document.getElementById('cinemaKuralMeaning').textContent = data.meaning;
      document.getElementById('cinemaLivingLesson').textContent = data.living;

      updateCinemaVideo();
    }}

    function playCurrentCinemaFilmYouTube() {{
      const data = CINEMA_FILMS_DATA[currentCinemaChapter];
      if (data && data.youtubeId) {{
        openPlayer(data.youtubeId, data.title);
      }}
    }}"""

    old_select_pattern = re.compile(r'function selectCinemaFilm\(chNum\) \{.*?updateCinemaVideo\(\);\s*\}', re.DOTALL)
    content = old_select_pattern.sub(new_select_fn, content)

    # 5. Update ILLARAVIYAL_DATA chapters 5, 8, 16 with their correct YouTube IDs
    content = content.replace('videoId: "C05GEfkJZaY"', 'videoId: "CUMZcTM4y7w"')
    content = content.replace('videoId: "yD_11P-Bskw"', 'videoId: "6OUebTuktZI"')
    # Chapter 16 was already juGQ6ncADIg or similar

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully upgraded {filepath}!")

if __name__ == '__main__':
    targets = ['thirukkural.html', 'docs/thirukkural.html', 'site/thirukkural.html']
    for t in targets:
        if os.path.exists(t):
            upgrade_file(t)
    print("Done all targets.")
