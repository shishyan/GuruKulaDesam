import json
import os
import shutil
import re

# Load Grade 1 images
grade1_images = []
if os.path.exists('grade1_images.json'):
    with open('grade1_images.json', 'r', encoding='utf-8') as f:
        grade1_images = json.load(f)

print(f"Loaded {len(grade1_images)} Grade 1 images.")

# Navigation & Footer
from build_google_site_pages import get_header, get_footer

# Grades Metadata Definition
grades_info = [
    {
        "num": 1,
        "title_ta": "தரம் 1",
        "title_en": "Grade 1",
        "icon": "📖",
        "motto": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
        "subtitle": "தொடக்கநிலை சைவ நெறி — கடவுள் வணக்கம், நற்பண்புகள் & 60 பாட நூல்கள்",
        "topics": [
            "கடவுள் வழிபாடு: முழுமுதற் கடவுள் விநாயகர், சிவபெருமான், முருகப்பெருமான் துதிகள்",
            "நமசிவாய வாழ்க: திருவைந்தெழுத்து மந்திரத்தின் பெருமையும் ஓதும் முறையும்",
            "அப்பர் & சம்பந்தர் பெருமக்கள் அருளிய தொடக்கத் திருமுறைப் பாடல்கள்",
            "நல்லொழுக்கம் & பெற்றோர், குருவை வணங்கும் உன்னத நெறிகள்",
            "உயிர்களிடத்தில் அன்பு செலுத்துதல் மற்றும் எளிய சைவ வழிபாட்டு முறைகள்"
        ],
        "has_sheets": True
    },
    {
        "num": 2,
        "title_ta": "தரம் 2",
        "title_en": "Grade 2",
        "icon": "🪔",
        "motto": "மந்திர மாவது நீறு வானவர் மேலது நீறு",
        "subtitle": "சிவ சின்னங்களின் மகிமை, திருக்கோயில் வழிபாடு & ஒழுக்க நெறிகள்",
        "topics": [
            "சிவ சின்னங்கள்: திருநீறு (விபூதி) மற்றும் உருத்திராக்க மாலையின் புனிதத்துவம்",
            "திருக்கோயில் வழிபாடு: கோபுர தரிசனம், நந்தி வழிபாடு, பிரகார வலம் வரும் முறை",
            "திருஞானசம்பந்தர் அருளிய 'தோடுடைய செவியன்' திருப்பதிக எளிய விளக்கம்",
            "சைவ விரதங்கள்: சோமவார விரதம் மற்றும் சிவராத்திரி வழிபாடு அறிமுகம்",
            "வாய்மை, இன்சொல் பேசுதல் மற்றும் சக மாணவர்களுடன் சகோதரத்துவம் பேணல்"
        ],
        "has_sheets": False
    },
    {
        "num": 3,
        "title_ta": "தரம் 3",
        "title_en": "Grade 3",
        "icon": "🔱",
        "motto": "கண்ணப்பன் ஒப்பதோர் அன்பின்மை கண்டபின் என் ஒப்பன் என்று அருள் செய்து",
        "subtitle": "அறுபத்து மூவர் நாயன்மார் கதைகள் & பன்னிரு திருமுறைகள் அறிமுகம்",
        "topics": [
            "பன்னிரு திருமுறைகள்: முதல் மூன்று திருமுறைகள் மற்றும் தேவாரம் பாடிய மூவர்",
            "நாயன்மார் வரலாறுகள்: கண்ணப்ப நாயனாரின் உன்னத பக்தி & சிறுத்தொண்டர் தியாகம்",
            "திருநாவுக்கரசர் அருளிய 'கூற்றாயினவாறு விலக்ககலீர்' தேவாரம்",
            "பஞ்ச பூதத் தலங்கள்: நிலம் (காஞ்சி), நீர் (திருவானைக்கா), நெருப்பு (திருவண்ணாமலை), காற்று (காளஹஸ்தி), ஆகாயம் (சிதம்பரம்)",
            "ஜீவகாருண்யம்: தாவரங்கள், விலங்கினங்களை வதைக்காமல் அன்பு பாராட்டுதல்"
        ],
        "has_sheets": False
    },
    {
        "num": 4,
        "title_ta": "தரம் 4",
        "title_en": "Grade 4",
        "icon": "📜",
        "motto": "பித்தா பிறைசூடி பெருமானே அருளாளா",
        "subtitle": "நால்வர் பெருமக்கள் வாழ்வு, திருக்கோயில் கட்டடக் கலை & திருவாசகம்",
        "topics": [
            "சமயக்குரவர் நால்வர்: சம்பந்தர், அப்பர், சுந்தரர், மாணிக்கவாசகர் அருளிய அருள்நெறிகள்",
            "சுந்தரமூர்த்தி சுவாமிகள் திருவாழ்வும் 'பித்தா பிறைசூடி' பதிகமும்",
            "மாணிக்கவாசகர் அருளிய திருவாசகத் தேன்: சிவபுராணம் மற்றும் திருவெம்பாவை",
            "திருக்கோயில் கலைகள்: விமானம், கொடிமரம், பலிபீடம், கருவறை ஆகியவற்றின் தத்துவங்கள்",
            "அறநெறி வாழ்வு: பொய் பேசாமை, புறங்கூறாமை, தூய சிந்தனை வளர்த்தல்"
        ],
        "has_sheets": False
    },
    {
        "num": 5,
        "title_ta": "தரம் 5",
        "title_en": "Grade 5",
        "icon": "🌺",
        "motto": "சொற்றுணை வேதியன் சோதி வானவன் நற்றுணை யாவது நமச்சி வாயவே",
        "subtitle": "சைவ விரதங்கள், பெரியபுராண நாயன்மார்கள் & சமூக நல்லிணக்கம்",
        "topics": [
            "முக்கிய சைவ விரதங்கள்: கந்த சஷ்டி, மகா சிவராத்திரி, ஆருத்ரா தரிசனம், கார்த்திகை தீபம்",
            "சேக்கிழார் பெருமான் அருளிய பெரியபுராணம் (திருத்தொண்டர் புராணம்) சிறப்புகள்",
            "அப்பர் பெருமானின் நற்றுணைப் பதிகம்: கல்லோடு பிணைத்துக் கடலில் பாய்ச்சியபோது நிகழ்ந்த அற்புதம்",
            "சைவ மரபில் அன்னதானம், குருபூசை மற்றும் மகேசுவர பூசையின் பெருமை",
            "சுற்றுச்சூழல் பாதுகாப்பு: நந்தவனங்கள் அமைத்தல், வில்வ மரம், திருநீற்றுப் பச்சிலை பேணுதல்"
        ],
        "has_sheets": False
    },
    {
        "num": 6,
        "title_ta": "தரம் 6",
        "title_en": "Grade 6",
        "icon": "🕉️",
        "motto": "அன்பும் சிவமும் இரண்டென்பர் அறிவிலார் அன்பே சிவமாவது ஆரும் அறிகிலார்",
        "subtitle": "சைவ சித்தாந்த தத்துவ தொடக்கம் — பதி, பசு, பாசம் & பண்கள்",
        "topics": [
            "சைவ சித்தாந்த முப்பொருள்கள்: பதி (இறைவன்), பசு (உயிர்), பாசம் (மும்மலங்கள்)",
            "மும்மலங்கள் அறிமுகம்: ஆணவம், கன்மம், மாயை ஆகியவற்றின் இயல்புகள்",
            "தேவாரப் பண்களும் திருமுறை இசையும்: காந்தாரம், நட்டராகம், கொல்லி, பஞ்சமம்",
            "திருமந்திர தத்துவம்: 'உடம்பினை முன்னம் இழுக்கென் றிருந்தேன் உடம்பினுக் குள்ளே உறுபொருள் கண்டேன்'",
            "தியான முறைகள்: பிராணாயாமம் மற்றும் எளிய சிவ தியானப் பயிற்சி"
        ],
        "has_sheets": False
    },
    {
        "num": 7,
        "title_ta": "தரம் 7",
        "title_en": "Grade 7",
        "icon": "🔔",
        "motto": "வேயுறு தோளிபங்கன் விடமுண்ட கண்டன் மிகநல்ல வீணை தடவி",
        "subtitle": "கோளறு திருப்பதிகம், நவக்கிரக தத்துவம் & சைவ சமய மறுமலர்ச்சி",
        "topics": [
            "கோளறு திருப்பதிகம்: நாளும் கோளும் நலிவு செய்யாமல் இறை அருளைப் பெறும் மார்க்கம்",
            "தமிழகத்தில் பக்தி இயக்கம் மற்றும் சமண, பௌத்த கொள்கைகளுடன் சைவ விவாதங்கள்",
            "மங்கையர்க்கரசியார், குலச்சிறையார் மற்றும் பாண்டி நாட்டு சைவ மீட்பு",
            "சைவ ஆகமங்கள் அறிமுகம்: சரியை, கிரியை, யோகம், ஞானம் எனும் நான்கு பாதைகள்",
            "திருத்தொண்டர் திருவந்தாதி மற்றும் நம்பியாண்டார் நம்பி திருமுறை தொகுத்த வரலாறு"
        ],
        "has_sheets": False
    },
    {
        "num": 8,
        "title_ta": "தரம் 8",
        "title_en": "Grade 8",
        "icon": "✨",
        "motto": "திருத்தொண்டத் தொகை உரைத்த தம்பிரான் தோழர் சுந்தரர்",
        "subtitle": "திருத்தொண்டத் தொகை, யோக மார்க்கம் & சைவ தீட்சை நெறிகள்",
        "topics": [
            "சுந்தரர் அருளிய திருத்தொண்டத் தொகை: 60 தனி அடியார்கள் மற்றும் 9 தொகை அடியார்கள்",
            "சைவ தீட்சைகள்: சமய தீட்சை, விசேட தீட்சை, நிர்வாண தீட்சை ஆகியவற்றின் உட்கருத்து",
            "மாணிக்கவாசகர் வாழ்வும் திருவாசக அனுபவமும்: நரியைக் குதிரையாக்கிய திருவிளையாடல்",
            "சைவ யோகம்: ஆதார சக்கரங்கள், அஷ்டாங்க யோகம் மற்றும் குண்டலினி விழிப்புணர்வு",
            "திருவாசகப் பதிகங்கள்: பிடித்த பத்து, அச்சோப் பதிகம், அன்னைப்பத்து ஆழ்ந்த சிந்தனைகள்"
        ],
        "has_sheets": False
    },
    {
        "num": 9,
        "title_ta": "தரம் 9",
        "title_en": "Grade 9",
        "icon": "⚜️",
        "motto": "மெய்கண்ட தேவர் அருளிய சிவஞான போதம் நற்பாடம்",
        "subtitle": "மெய்கண்ட சாத்திரங்கள், சிவஞானபோதம் & சதாசிவ தத்துவம்",
        "topics": [
            "பதினான்கு மெய்கண்ட சாத்திரங்கள் அறிமுகம் (சிவஞானபோதம் முதல் சங்கற்ப நிராகரணம் வரை)",
            "மெய்கண்டார் அருளிய சிவஞானபோதம்: பன்னிரண்டு சூத்திரங்களின் சுருக்க விளக்கம்",
            "உண்மை ஞானம்: பாச ஞானம், பசு ஞானம் கடந்து பதி ஞானம் பெறுதல்",
            "சைவ ஆதீனங்கள் மற்றும் திருமடங்களின் வரலாற்றுப் பணிகள் (தருமபுரம், திருவாவடுதுறை, மதுரை)",
            "திருவுந்தியார் மற்றும் திருக்களிற்றுப்படியார் பாடல்கள் சிந்தனை"
        ],
        "has_sheets": False
    },
    {
        "num": 10,
        "title_ta": "தரம் 10",
        "title_en": "Grade 10",
        "icon": "🌟",
        "motto": "சாத்திர ஞானமும் திருமுறைப் பனுவலும் ஆன்ம முக்திக்கு வாயில்கள்",
        "subtitle": "பொதுத் தேர்வு (GCE O/L) பாடநெறி — சிவஞான சித்தியார் & ஆன்ம இயல்பு",
        "topics": [
            "அருணந்தி சிவாசாரியார் அருளிய சிவஞான சித்தியார்: பரபக்கம் மற்றும் சுபக்கம் ஒப்பீடு",
            "ஆன்மாவின் இலக்கணம்: சாக்கிரம், சொப்பனம், சுழுத்தி, துரியம், துரியாதீதம் ஆகிய ஐந்து அவத்தைகள்",
            "கன்ம வினைப் பயன்கள்: சஞ்சிதம், பிராரப்தம், ஆகாமியம் அறுபடும் முறை",
            "சைவ இலக்கிய ஆழம்: கந்தபுராணம், திருவிளையாடற் புராணம், திருப்புகழ் தத்துவங்கள்",
            "தேர்வு வழிகாட்டி: முந்தைய ஆண்டு வினாத்தாள்கள், மாதிரிக் கட்டுரைகள், பதிக ஒப்புவித்தல்"
        ],
        "has_sheets": False
    },
    {
        "num": 11,
        "title_ta": "தரம் 11",
        "title_en": "Grade 11",
        "icon": "🔱",
        "motto": "யாவர்க்குமாம் இறைவற்கு ஒரு பச்சிலை யாவர்க்குமாம் பசுவுக்கு ஒரு வாயுறை",
        "subtitle": "சைவப் பண்பாட்டு வரலாறு, கல்வெட்டுகள் & சோழர்-பாண்டியர் பேரரசு",
        "topics": [
            "சோழப் பேரரசு மற்றும் சைவ மறுமலர்ச்சி: இராஜராஜ சோழன் தில்லைத் திருமுறை மீட்டல்",
            "தஞ்சைப் பெருவுடையார் கோயில், கங்கைகொண்ட சோழபுரம் சிற்பக் கலை & கல்வெட்டுகள்",
            "சைவ வேதாந்த உரையாடல்: ஆதி சங்கரர், இராமானுஜர், மத்துவர் கொள்கைகளுடன் சைவ சித்தாந்த ஒப்பாய்வு",
            "சைவ உரையாசிரியர்கள்: சிவஞான முனிவர் (திராவிட மாபாடியம்), மாதவச் சிவஞான யோகிகள்",
            "ஆன்மீக நெறிமுறைகள்: தீய பழக்கங்கள் தவிர்த்தல், தியானம், நித்திய கர்மானுஷ்டானங்கள்"
        ],
        "has_sheets": False
    },
    {
        "num": 12,
        "title_ta": "தரம் 12",
        "title_en": "Grade 12",
        "icon": "👑",
        "motto": "செம்மலர் நோன்றாள் சேரல் — பரமுக்திப் பேறு",
        "subtitle": "உயர்நிலை (GCE A/L) சைவ சித்தாந்த சாத்திரங்கள், மகா பெரியவா & சன்மார்க்கம்",
        "topics": [
            "முழுமையான சிவஞானபோத விரிவுரை: பிரமாணவியல், இலக்கணவியல், சாதனவியல், பயனியல்",
            "பரமுக்தி & சீவன்முக்தி: உடலோடு வாழும்போதே சிவானந்தத்தில் திளைக்கும் ஞானியர் இயல்பு",
            "காஞ்சி மகா பெரியவா அருளிய 'தெய்வத்தின் குரல்': அத்வைத-சைவ சமரச ஞானம்",
            "வள்ளலார் சுத்த சன்மார்க்கம்: அருட்பெருஞ்சோதி தனிப்பெருங்கருணை, மரணமிலாப் பெருவாழ்வு",
            "உயர்நிலைக் கல்வி & பல்கலைக்கழக ஆய்வு வழிகாட்டல்: சைவத் தத்துவ ஆய்வுக் கட்டுரைகள்"
        ],
        "has_sheets": False
    }
]

# Generate Kalvi Hub (kalvi.html)
def generate_kalvi_hub():
    cards_html = ""
    for g in grades_info:
        extra_badge = '<span class="grade-card-badge">60 பாடப் படங்கள்</span>' if g['has_sheets'] else '<span class="grade-card-badge">பாடத்திட்டம்</span>'
        cards_html += f"""
        <a href="tharam-{g['num']}.html" class="grade-card">
          <div>
            <div class="grade-card-badge-row" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <span class="grade-card-badge">{g['title_ta']} ({g['title_en']})</span>
              {extra_badge}
            </div>
            <div class="grade-card-header">
              <div class="grade-card-icon">{g['icon']}</div>
              <div class="grade-card-title">
                <h3>{g['title_ta']} — சைவ நெறி</h3>
                <span>{g['title_en']} Spiritual Education</span>
              </div>
            </div>
            <p class="grade-card-desc" style="margin-top:12px;">{g['subtitle']}</p>
            <div style="font-size:0.8rem; color:var(--gold-soft); margin-top:10px; font-style:italic;">
              "{g['motto']}"
            </div>
          </div>
          <div class="grade-card-footer">
            <span>பாடங்களைக் காண்க</span>
            <span>அணுகுக ↗</span>
          </div>
        </a>
        """

    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>சைவ நெறி கல்வித் தளம் — தரம் 1 முதல் தரம் 12 வரை | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் சைவ நெறி பாடநெறி தளம். தரம் 1 முதல் 12 வரையிலான பள்ளி & ஆன்மீகப் பாடங்கள், திருமுறைத் தேவாரங்கள் மற்றும் பாடநூல்கள்.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header('kalvi_hub')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">ॐ சைவ நெறிப் பள்ளிக் கல்வி • தரம் 1 முதல் 12 வரை ॐ</div>
      <h1>சைவ நெறி கல்வித் தளம்</h1>
      <h2>Saiva Neri Spiritual &amp; Cultural Curriculum (Grades 1 to 12)</h2>
      <div class="verse-quote">"கற்றதனால் ஆய பயனென்கொல் வாலறிவன் நற்றாள் தொழாஅர் எனின்" — திருக்குறள் 2</div>
      <p class="hero-desc">
        மாணவர்களின் உள்ளத்தில் பக்தியையும், ஒழுக்கத்தையும், மெய்ஞ்ஞானத்தையும் விதைக்கும் உன்னதக் கல்வித் தளம். திருமுறைப் பாடல்கள், சைவ சித்தாந்த அடிப்படைகள், நாயன்மார் வரலாறுகள், இறை இசை மற்றும் ஒழுக்க நெறிகளை உள்ளடக்கிய 12 தரங்களுக்கான முழுமையான களஞ்சியம்.
      </p>
    </div>

    <!-- Google Sites Live Sync Banner -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 அதிகாரப்பூர்வ கூகிள் தளத்திலும் கிடைக்கிறது</h3>
        <p>குரு குல தேசம் கூகிள் சைட்ஸ் (Google Sites) தளத்தில் அமைக்கப்பட்ட அனைத்து பக்கங்களும் இங்கு ஒருங்கிணைக்கப்பட்டுள்ளன.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom" target="_blank" rel="noopener" class="gs-banner-btn">
        நேரடி கூகிள் தளம் காண்க ↗
      </a>
    </div>

    <!-- Key Navigation Highlights -->
    <div class="canonical-grid" style="margin-bottom: 30px;">
      <div class="canonical-card" onclick="location.href='tharam-1.html'" style="cursor: pointer; border-color: var(--gold-bright);">
        <h4>📖 தரம் 1 — முழுமையான 60 பாடப் படங்கள்</h4>
        <p>முதல் தர மாணவர்களுக்கான வண்ணமயமான 60 பாடநூல் பக்கங்கள், கடவுள் வாழ்த்து மற்றும் எளிய பயிற்சிகள்.</p>
        <span style="color: var(--gold); font-size: 0.82rem; font-weight: 700; margin-top: 6px; display: inline-block;">பக்கங்களை வாசிக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='irai-isai-virundhu.html'" style="cursor: pointer;">
        <h4>🎵 இறை இசை விருந்து (Syllabus Music)</h4>
        <p>பாலும் தெளிர் தேனும், குரு வணக்கம், கந்தர் அநுபூதி, பாரதியார் கானம், சிவபுராணம் ஆகிய 5 சிறப்புப் படைப்புகள்.</p>
        <span style="color: var(--gold); font-size: 0.82rem; font-weight: 700; margin-top: 6px; display: inline-block;">கேட்க & பாட ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='classes.html'" style="cursor: pointer;">
        <h4>🏛️ ஆன்லைன் வகுப்புகள் (Classes)</h4>
        <p>குருகுல முறை நேரடிப் பயிற்சி, வாராந்திர வகுப்புகள் மற்றும் தேர்வு வழிகாட்டுதல்கள்.</p>
        <span style="color: var(--gold); font-size: 0.82rem; font-weight: 700; margin-top: 6px; display: inline-block;">வகுப்பு விவரங்கள் ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='syllabus.html'" style="cursor: pointer;">
        <h4>📜 விரிவான பாடத்திட்டம் (Full Syllabus)</h4>
        <p>தொடக்க நிலை, இடைநிலை, உயர்நிலை மாணவர்களுக்கான முழுமையான சைவ சித்தாந்தப் பாடத்திட்டம்.</p>
        <span style="color: var(--gold); font-size: 0.82rem; font-weight: 700; margin-top: 6px; display: inline-block;">பாடத்திட்டம் அறிய ↗</span>
      </div>
    </div>

    <h2 class="section-divider-title">அனைத்து 12 தரங்களின் பாடநெறி (Select Your Grade)</h2>

    <div class="grades-grid">
      {cards_html}
    </div>
  </main>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
    with open('kalvi.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated kalvi.html")

generate_kalvi_hub()

# Generate Grade 1 with 60 sheets
def generate_grade1():
    sheets_html = ""
    for i, img_url in enumerate(grade1_images):
        page_num = i + 1
        sheets_html += f"""
        <div class="sheet-card">
          <div class="sheet-header">
            <span>பக்கம் {page_num}</span>
            <span style="font-size:0.75rem; color:var(--text-muted);">தரம் 1</span>
          </div>
          <div class="sheet-thumb" onclick="openSheetModal('{img_url}', {page_num}, 'சைவ நெறி தரம் 1')">
            <img src="{img_url}" loading="lazy" alt="தரம் 1 சைவ நெறி - பக்கம் {page_num}">
            <div class="sheet-zoom-overlay">🔍</div>
          </div>
          <div class="sheet-actions">
            <button class="sheet-btn sheet-btn-view" onclick="openSheetModal('{img_url}', {page_num}, 'சைவ நெறி தரம் 1')">
              🔍 பெரிதாக்குக
            </button>
            <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-1" target="_blank" rel="noopener" class="sheet-btn sheet-btn-direct" title="கூகிள் தளத்தில் காண்க">
              Google Site ↗
            </a>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>சைவ நெறி — தரம் 1 (Grade 1 Textbook & Lessons) | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் சைவ நெறி தரம் 1 முழுமையான 60 பாடப் படங்கள் மற்றும் பாடநூல் வழிகாட்டி.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header('tharam-1')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">📖 தரம் 1 • ஆரம்பக் கல்வி • 60 பாடப் படங்கள் 📖</div>
      <h1>சைவ நெறி — தரம் 1 (Grade 1)</h1>
      <h2>Saiva Neri Primary Educational Reader — 60 Complete Lesson Sheets</h2>
      <div class="verse-quote">"பாலும் தெளிதேனும் பாகும் பருப்பும் இவை நாலும் கலந்துனக்கு நான் தருவேன்" — ஔவையார்</div>
      <p class="hero-desc">
        குழந்தைகளுக்கான தொடக்க நிலை சைவ நெறிப் பாடப் புத்தகம். கடவுள் வணக்கம், விநாயகர், சிவபெருமான், முருகன் வழிபாடுகள், திருமுறைப் பாடல்கள், நற்பண்புகள் மற்றும் நல்லொழுக்கப் பயிற்சிகள் அடங்கிய 60 முழுமையான பாடப் படங்கள்.
      </p>
    </div>

    <!-- Live Google Sites Link Bar -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 அதிகாரப்பூர்வ கூகிள் சைட்ஸ் நேரடிப் பக்கம்</h3>
        <p>இந்த தரம் 1 பாடங்கள் கூகிள் சைட்ஸ் பக்கத்திலும் (<span style="color:var(--gold-bright);">Sites: தரம் 1</span>) நேரடியாகப் படிக்கக் கிடைக்கின்றன.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-1" target="_blank" rel="noopener" class="gs-banner-btn">
        கூகிள் தளத்தில் தரம் 1 காண்க ↗
      </a>
    </div>

    <!-- Quick Navigation Between Grades -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin: 20px 0; padding: 14px 20px; background:var(--bg-card); border-radius:12px; border:1px solid var(--border-gold);">
      <a href="kalvi.html" style="color:var(--gold); text-decoration:none; font-weight:600;">← அனைத்து தரங்கள் (All Grades)</a>
      <span style="color:var(--text-muted); font-size:0.9rem;">தரம் 1 / 12</span>
      <a href="tharam-2.html" style="color:var(--gold-bright); text-decoration:none; font-weight:700;">தரம் 2 காண்க (Grade 2) →</a>
    </div>

    <!-- Chapter Breakdown / Highlights -->
    <div class="scripture-study-section" style="margin-top: 20px;">
      <span class="source-badge">தரம் 1 பாடக் குறிப்புகள் &amp; நற்சிந்தனைகள்</span>
      <h2>தரம் 1 பாடத்திட்ட உள்ளடக்கம் (Syllabus Highlights)</h2>
      <ul style="margin-left: 20px; margin-top: 12px; color: var(--text-main); line-height: 1.8;">
        <li><strong>கடவுள் வணக்கம்:</strong> முழுமுதற் கடவுள் விநாயகர் வணக்கம், நமசிவாய மந்திரம் ஓதுதல்.</li>
        <li><strong>சைவத் தெய்வங்கள்:</strong> சிவபெருமான், உமையம்மை, முருகப்பெருமான், பிள்ளையார் அறிமுகம்.</li>
        <li><strong>திருக்கோயில் பழக்கங்கள்:</strong> நீராடித் தூய ஆடை அணிந்து திருக்கோயிலுக்குச் செல்லுதல், திருநீறு அணிதல்.</li>
        <li><strong>ஒழுக்க நெறிகள்:</strong> பெற்றோரை மதித்தல், ஆசிரியருக்குக் கீழ்ப்படிதல், எளியோர்க்கு உதவுதல்.</li>
        <li><strong>உயிர்களிடத்தில் அன்பு:</strong> பறவைகள், வளர்ப்புப் பிராணிகள் மற்றும் செடி கொடிகளுக்கு நீர் ஊற்றுதல்.</li>
      </ul>
    </div>

    <!-- 60 Sheets Grid -->
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:30px;">
      <h2 class="section-divider-title" style="margin:0;">முழுமையான 60 பாடநூல் பக்கங்கள் (All 60 Pages)</h2>
      <span style="color:var(--gold-bright); font-size:0.9rem; font-weight:600;">மொத்தம்: 60 பக்கங்கள்</span>
    </div>
    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:6px;">
      எந்தவொரு பக்கத்தின் மீதும் கிளிக் செய்து பெரிய அளவில் வாசிக்கலாம் (Click any sheet to zoom &amp; read in full resolution).
    </p>

    <div class="sheets-grid">
      {sheets_html}
    </div>

    <div style="text-align:center; margin: 40px 0;">
      <a href="tharam-2.html" class="gs-banner-btn" style="padding:14px 30px; font-size:1.05rem;">
        அடுத்த தரம்: தரம் 2 நோக்கிச் செல்க (Proceed to Grade 2) →
      </a>
    </div>
  </main>

  <!-- Sheet Zoom Modal -->
  <div class="sheet-modal" id="sheetModal" onclick="if(event.target === this) closeSheetModal()">
    <div class="sheet-modal-box">
      <div class="sheet-modal-header">
        <div class="sheet-modal-title" id="sheetModalTitle">தரம் 1 பாட நூல் பக்கம்</div>
        <button onclick="closeSheetModal()" style="background:transparent; border:none; color:#fff; font-size:1.5rem; cursor:pointer;">✕</button>
      </div>
      <div class="sheet-modal-body">
        <img id="sheetModalImg" src="" alt="Enlarged Sheet">
      </div>
      <div style="padding:10px 20px; background:rgba(12,15,21,0.95); display:flex; justify-content:space-between; align-items:center;">
        <span style="color:var(--text-muted); font-size:0.85rem;">விசைப்பலகை 'ESC' அழுத்தி மூடலாம்</span>
        <button onclick="closeSheetModal()" style="padding:6px 14px; background:var(--gold); border:none; border-radius:6px; font-weight:700; cursor:pointer;">மூடுக (Close)</button>
      </div>
    </div>
  </div>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
    with open('tharam-1.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated tharam-1.html")

generate_grade1()

# Generate Grades 2 to 12 individual pages
def generate_grades_2_to_12():
    for g in grades_info:
        if g['num'] == 1:
            continue
        num = g['num']
        prev_num = num - 1
        next_num = num + 1 if num < 12 else 1

        topics_li = "".join([f"<li>{t}</li>" for t in g['topics']])

        html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>சைவ நெறி — {g['title_ta']} ({g['title_en']}) | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் சைவ நெறி {g['title_ta']}. பாடத்திட்டம், பன்னிரு திருமுறைகள், சிவ சின்னங்கள் &amp; ஆன்மீக வழிகாட்டி.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header(f'tharam-{num}')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">ॐ சைவ நெறி • {g['title_ta']} • {g['title_en']} ॐ</div>
      <h1>சைவ நெறி — {g['title_ta']}</h1>
      <h2>Saiva Neri Spiritual Curriculum — {g['title_en']}</h2>
      <div class="verse-quote">"{g['motto']}"</div>
      <p class="hero-desc">{g['subtitle']}</p>
    </div>

    <!-- Live Google Sites Link Bar -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 கூகிள் சைட்ஸ் நேரடி இணைப்பு (Google Sites Mirror)</h3>
        <p>கூகிள் தளத்தில் உள்ள இந்த {g['title_ta']} பக்கத்தை நேரடியாகப் பார்வையிடவும்.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-{num}" target="_blank" rel="noopener" class="gs-banner-btn">
        கூகிள் தளத்தில் {g['title_ta']} காண்க ↗
      </a>
    </div>

    <!-- Grade Quick Navigation -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin: 20px 0; padding: 14px 20px; background:var(--bg-card); border-radius:12px; border:1px solid var(--border-gold);">
      <a href="tharam-{prev_num}.html" style="color:var(--gold); text-decoration:none; font-weight:600;">← முந்தைய தரம்: தரம் {prev_num}</a>
      <a href="kalvi.html" style="color:var(--text-muted); text-decoration:none; font-size:0.9rem;">கல்வித் தளம் (Curriculum Hub)</a>
      <a href="tharam-{next_num}.html" style="color:var(--gold-bright); text-decoration:none; font-weight:700;">அடுத்த தரம்: தரம் {next_num} →</a>
    </div>

    <!-- Syllabus Content Box -->
    <div class="scripture-study-section">
      <span class="source-badge">{g['title_ta']} — பாடத்திட்ட விவரங்கள் &amp; தலைப்புகள்</span>
      <h2>கற்பித்தல் நெறிகளும் பாட உள்ளடக்கமும் (Curriculum &amp; Learning Outcomes)</h2>
      <ul style="margin-left: 20px; margin-top: 14px; color: var(--text-main); line-height: 1.8;">
        {topics_li}
      </ul>
    </div>

    <!-- Related Devotional Links -->
    <h2 class="section-divider-title" style="margin-top:40px;">இணைந்த ஆன்மீகப் பிரிவுகள் (Related Traditions)</h2>
    <div class="canonical-grid">
      <div class="canonical-card" onclick="location.href='saiva-neri.html'" style="cursor: pointer;">
        <h4>🔱 பன்னிரு திருமுறைகள் (172 பாடல்கள்)</h4>
        <p>தேவாரம், திருவாசகம், திருவிசைப்பா, திருமந்திரப் பெருவெளியின் இசை வடிவங்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">கேட்க &amp; தியானிக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='irai-isai-virundhu.html'" style="cursor: pointer;">
        <h4>🎵 இறை இசை விருந்து (5 பாடல்கள்)</h4>
        <p>பாலும் தெளிர் தேனும், குரு வணக்கம், கந்தர் அநுபூதி, சிவபுராணப் பாடல்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">இறை இசை கேட்க ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='thirukkural.html'" style="cursor: pointer;">
        <h4>📜 திருக்குறள் வாழ்வியல் தர்மம்</h4>
        <p>அறத்துப்பால், பொருட்பால், இன்பத்துப்பால் 133 அதிகாரங்களின் சினிமா இசைத் திரைப்படங்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">குறள் நல்வழி ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='classes.html'" style="cursor: pointer;">
        <h4>🏛️ ஆன்லைன் &amp; குருகுல வகுப்புகள்</h4>
        <p>வாராந்திர நேரலை வகுப்புகள் மற்றும் தேர்வு வழிகாட்டுதலில் இணையுங்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">வகுப்பில் சேர ↗</span>
      </div>
    </div>
  </main>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
        with open(f'tharam-{num}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated tharam-{num}.html")

generate_grades_2_to_12()

# Generate Irai Isai Virundhu (irai-isai-virundhu.html)
def generate_irai_isai():
    songs = [
        {
            "id": "bJ2dt95RvqY",
            "title_ta": "பாலும் தெளிர் தேனும்",
            "title_en": "Paalum Theli Thenum",
            "author": "ஔவையார் (நல்வழி)",
            "deity": "முழுமுதற் கடவுள் ஸ்ரீ கணபதி (Lord Vinayagar)",
            "lyrics": """பாலும் தெளிதேனும் பாகும் பருப்பும் இவை
நாலும் கலந்துனக்கு நான் தருவேன் - கோலஞ்செய்
துங்கக் கரிமுகத்துத் தூமணியே நீயெனக்குச்
சங்கத் தமிழ் மூன்றும் தா!""",
            "meaning": "அழகிய தும்பிக்கையுடைய யானை முகப் பெருமானே! பால், தெளிந்த தேன், சர்க்கரைப் பாகு, சுவையான பருப்பு ஆகிய நான்கு அருமையான பொருள்களையும் கலந்து உனக்குப் படைக்கின்றேன். நீ எனக்கு இயல், இசை, நாடகம் என்னும் முத்தமிழ்ச் செல்வத்தையும் ஞானத்தையும் தந்தருள்வாயாக!"
        },
        {
            "id": "QiK97x3oK_Y",
            "title_ta": "குரு வணக்கம் (Guru Vanakkam)",
            "title_en": "Guru Vanakkam",
            "author": "பாரம்பரிய குருவந்தனம் & ஆசிரியப் பெருமை",
            "deity": "ஸ்ரீ தட்சிணாமூர்த்தி & சற்குருநாதர் (Satguru)",
            "lyrics": """குருபிரம்மா குருவிஷ்ணு குருதேவோ மஹேஸ்வர:
குரு சாக்ஷாத் பரம்பிரம்மா தஸ்மை ஸ்ரீ குரவே நம:

தெள்ளிய ஆலின் கீழ் இருந்த செல்வன் நல்கிய
அள்ளல் இல் இன்பத்து அமுதினை மாந்திடுவோம்!""",
            "meaning": "படைக்கும் பிரம்மனும், காக்கும் திருமாலும், சம்ஹரிக்கும் மகேஸ்வரனும் குருவே. கண்கண்ட பரப்பிரம்மமாக விளங்கும் அந்த குருபிரானுக்கு எனது சிரம் தாழ்ந்த நமஸ்காரங்கள். கல்லால மரத்தடியில் மௌன குருவாய் அமர்ந்து சனகாதி முனிவர்களுக்கு ஞானம் அருளிய தட்சிணாமூர்த்தியின் திருவடிகளைப் போற்றுகின்றோம்."
        },
        {
            "id": "a8PMcn1cjDo",
            "title_ta": "உருவாய் அருவாய் (கந்தர் அநுபூதி)",
            "title_en": "Uruvaai Aruvaai - Kandar Anubhuti",
            "author": "அருணகிரிநாத சுவாமிகள் (கந்தர் அநுபூதி)",
            "deity": "ஸ்ரீ பாலசுப்பிரமணியக் கடவுள் (Lord Murugan)",
            "lyrics": """உருவாய் அருவாய் உளதாய் இலதாய்
மருவாய் மலராய் மணியாய் ஒளியாய்க்
கருவாய் உயிராய்க் கதியாய் விதியாய்க்
குருவாய் வருவாய் அருள்வாய் குகனே!""",
            "meaning": "உருவமாகவும், அருவமாகவும், உள்ளதாகவும், இல்லாததாகவும், மணமாயும், மலராயும், நவரத்தின மணியாயும், அதனுள் ஒளிரும் சுடராயும், கருவாயும், உயிராயும், நாம் அடையும் நற்கதியாயும், இறை நியதியாயும் விளங்கும் குகப்பெருமானே! எனக்கு சற்குருவாக நேரில் வந்து உன் திருவடி ஞானத்தை அருள்புரிவாயாக!"
        },
        {
            "id": "ex9sEZwE2Co",
            "title_ta": "என்று தணியும் இந்த சுதந்திர தாகம்",
            "title_en": "Endru Thaniyum Indha Suthandhira Dhaagam",
            "author": "மகாகவி சுப்பிரமணிய பாரதியார்",
            "deity": "பாரத மாதா & தர்ம தேவதை",
            "lyrics": """என்று தணியும் இந்த சுதந்திர தாகம்?
என்று மடியும் எங்கள் அடிமையின் மோகம்?
என்றெம தன்னையின் கைகள் தளரும்?
என்றுநம் துன்பங்கள் தீர்ந்துபொய் யோயும்?

அன்னையே தாயே அருள் செய்ய வாராய்!""",
            "meaning": "மகாகவி பாரதியாரின் அனல் பறக்கும் தேசபக்தி மற்றும் ஆன்மீக விடுதலைப் பாடல். பாரத தாயின் விலங்குகளை ஒடித்து, தர்ம நெறியையும் சத்தியத்தையும் காக்கும் வீரத்தை நமக்கு வழங்கி அருளுமாறு பராசக்தியிடம் வேண்டும் விடுதலைப் பெருங்கானம்."
        },
        {
            "id": "Q8EDvpYLObA",
            "title_ta": "சிவ புராணம் (Siva Puranam)",
            "title_en": "Siva Puranam — Thiruvasagam",
            "author": "மாணிக்கவாசகப் பெருமான் (திருவாசகம் - எட்டாம் திருமுறை)",
            "deity": "சிவபெருமான் (Lord Shiva)",
            "lyrics": """நமச்சிவாய வாழ்க நாதன் தாள் வாழ்க
இமைப்பொழுதும் என் நெஞ்சில் நீங்காதான் தாள் வாழ்க
கோகழி ஆண்ட குருமணிதன் தாள் வாழ்க
ஆகமம் ஆகிநின்று அண்ணிப்பான் தாள் வாழ்க
ஏகன் அநேகன் இறைவன் அடிவாழ்க!""",
            "meaning": "பன்னிரு திருமுறைகளில் எட்டாம் திருமுறையான திருவாசகத்தின் முதற்பகுதி சிவபுராணம். திருவைந்தெழுத்தாகிய நமசிவாய மந்திரத்தை வாழ்த்தி, இமைக்கும் நொடிப்பொழுதும் இதயத்தை விட்டு அகலாத சிவபெருமானின் திருவடிகளைப் போற்றி ஆன்ம முக்தி நாடும் பரவசப் பனுவல்."
        }
    ]

    cards_html = ""
    for s in songs:
        cards_html += f"""
        <div class="music-feast-card">
          <div class="feast-media-frame">
            <iframe src="https://www.youtube.com/embed/{s['id']}?enablejsapi=1" title="{s['title_ta']}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          </div>
          <div class="feast-details">
            <div class="feast-badge-row">
              <span class="card-badge badge-film">இறை இசை விருந்து</span>
              <span class="card-badge badge-audio">{s['deity']}</span>
            </div>
            <h3 class="feast-title">{s['title_ta']}</h3>
            <div class="feast-meta">✍️ இயற்றியவர்: {s['author']}</div>
            <div class="feast-lyrics-box">{s['lyrics']}</div>
            <div class="feast-meaning">
              <strong>பொருள் விளக்கம்:</strong> {s['meaning']}
            </div>
            <div style="margin-top:8px;">
              <a href="https://www.youtube.com/watch?v={s['id']}" target="_blank" rel="noopener noreferrer" style="color:var(--gold-bright); font-size:0.85rem; font-weight:700; text-decoration:none;">
                YouTube தளத்தில் காண்க ↗
              </a>
            </div>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>இறை இசை விருந்து (Syllabus Music Feasts) | Guru Kula Desam</title>
  <meta name="description" content="பாலும் தெளிர் தேனும், குரு வணக்கம், கந்தர் அநுபூதி, பாரதியார் பாடல் மற்றும் சிவபுராணம் அடங்கிய குரு குல தேசத்தின் ஐந்து அமிர்த கானங்கள்.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header('irai-isai')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">🎵 பாடத்திட்ட இறை இசை விருந்து • 5 அமிர்தப் பாடல்கள் 🎵</div>
      <h1>இறை இசை விருந்து</h1>
      <h2>Syllabus Devotional Music Feasts — Sacred Tamil Hymns</h2>
      <div class="verse-quote">"இறைவன் இசையாய் இருப்பதனால் இசையே இறைவனை அடையும் எளிய வழி" — தேவாரம்</div>
      <p class="hero-desc">
        கூகிள் சைட்ஸ் பாடத்திட்டத்தில் இடம்பெற்றுள்ள 5 முக்கிய தெய்வீகப் பாடல்கள். விநாயகர் துதி, குரு வணக்கம், கந்தர் அநுபூதி, தேசபக்தி கானம் மற்றும் சிவபுராணம் ஆகிய ஐந்து அமிர்த கானங்களின் வீடியோக்கள், வரிகள் மற்றும் தத்துவ விளக்கங்கள்.
      </p>
    </div>

    <!-- Live Google Sites Link Bar -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 கூகிள் சைட்ஸ் 'இறை இசை விருந்து' நேரடிப் பக்கம்</h3>
        <p>Google Sites தளத்தில் அமைக்கப்பட்ட அதே ஐந்து இசைத் தொகுப்புகளை அங்கும் பார்வையிடலாம்.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/syllabus/%E0%AE%87%E0%AE%B1-%E0%AE%87%E0%AE%9A-%E0%AE%B5%E0%AE%B0%E0%AE%A8%E0%AE%A4" target="_blank" rel="noopener" class="gs-banner-btn">
        கூகிள் தளத்தில் இறை இசை காண்க ↗
      </a>
    </div>

    <div style="margin-top: 30px;">
      {cards_html}
    </div>
  </main>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
    with open('irai-isai-virundhu.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated irai-isai-virundhu.html")

generate_irai_isai()

# Generate Syllabus (syllabus.html)
def generate_syllabus():
    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>பாடத்திட்டம் — சைவ நெறி &amp; ஆன்மீகக் கல்வி | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் அதிகாரப்பூர்வ பாடத்திட்டம். சைவ நெறி, திருக்குறள் உலகப் பொதுமறை, சுத்த சன்மார்க்கம் மற்றும் இறை இசைப் பாடத்திட்ட வழிகாட்டி.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header('syllabus')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">📜 குரு குல தேச பாடத்திட்டப் பெருவெளி 📜</div>
      <h1>பாடத்திட்டம் (Syllabus)</h1>
      <h2>Comprehensive Spiritual &amp; Ethical Learning Curriculum</h2>
      <div class="verse-quote">"எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும் கண்ணென்ப வாழும் உயிர்க்கு" — திருக்குறள் 392</div>
      <p class="hero-desc">
        நமது ஆதி வேத மரபு, பன்னிரு திருமுறைகள், சைவ சித்தாந்தம், திருக்குறள் வாழ்வியல் தர்மம், காஞ்சி மகா பெரியவா அருளுரைகள் மற்றும் வள்ளலார் பெருமானின் ஜீவகாருண்ய ஒழுக்கத்தை ஒருங்கிணைத்த முழுமையான பாடத்திட்டம்.
      </p>
    </div>

    <!-- Live Google Sites Link Bar -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 கூகிள் சைட்ஸ் பாடத்திட்டப் பக்கம் (Syllabus on Google Sites)</h3>
        <p>கூகிள் தளத்திலும் இந்த பாடத்திட்டப் பக்கங்கள் நேரலையாக இணைக்கப்பட்டுள்ளன.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/syllabus/untitled-page" target="_blank" rel="noopener" class="gs-banner-btn">
        கூகிள் தளப் பாடத்திட்டம் ↗
      </a>
    </div>

    <!-- Syllabus Sections -->
    <div class="scripture-study-section">
      <span class="source-badge">நிலை 1: தொடக்கக் கல்வி (Primary: Grades 1 - 5)</span>
      <h2>அறநெறி &amp; பக்தி விதைத்தல் (Ethical &amp; Devotional Foundations)</h2>
      <p>சிறுவயதிலேயே ஆன்மீகச் சிந்தனைகளையும் தூய ஒழுக்கத்தையும் மனதில் பதியவைக்கும் எளிய பாடநெறி.</p>
      <ul style="margin-left:20px; margin-top:10px; line-height:1.8;">
        <li>விநாயகர், சிவபெருமான், முருகன், அம்பிகை துதிப் பாடல்கள் மனனம் செய்தல்</li>
        <li>திருக்கோயில் வழிபாட்டு முறைகள், திருநீறு அணிவதன் மகிமை, சைவச் சின்னங்கள்</li>
        <li>அறுபத்து மூவர் நாயன்மார் கதைகள் மற்றும் பெரியபுராண நாயன்மார்களின் தியாக வாழ்வு</li>
        <li><a href="tharam-1.html" style="color:var(--gold-bright);">தரம் 1 முதல் 60 வண்ணமயமான பாடப் படங்கள்</a> முழுமையான பயிற்சி</li>
      </ul>
    </div>

    <div class="scripture-study-section" style="margin-top:24px;">
      <span class="source-badge">நிலை 2: இடைநிலைக் கல்வி (Middle: Grades 6 - 9)</span>
      <h2>சைவ சித்தாந்த முப்பொருளியல் &amp; திருமுறை நெறி (Shaiva Philosophy)</h2>
      <p>பகுத்தறிவோடு கூடிய ஆன்மீகக் கல்வியும், வேத-உபநிடதத் தத்துவங்களும் கற்பிக்கப்படும் நிலை.</p>
      <ul style="margin-left:20px; margin-top:10px; line-height:1.8;">
        <li>பதி, பசு, பாசம் எனும் சைவ சித்தாந்த முப்பொருள் உண்மை விளக்கம்</li>
        <li>மும்மலங்கள் (ஆணவம், கன்மம், மாயை) இயல்பு மற்றும் அவற்றைக் கடக்கும் யோக வழி</li>
        <li>தேவாரப் பண்கள், திருவாசகம் சிவபுராணம் மற்றும் திருக்கோளறு திருப்பதிகம் ஓதும் நெறி</li>
        <li>சைவ ஆதீனங்கள், தமிழகத் திருத்தலங்கள், கோயில் கட்டடக் கலை மற்றும் கல்வெட்டுகள்</li>
      </ul>
    </div>

    <div class="scripture-study-section" style="margin-top:24px;">
      <span class="source-badge">நிலை 3: உயர்நிலைக் கல்வி (High &amp; Advanced: Grades 10 - 12)</span>
      <h2>மெய்கண்ட சாத்திரங்கள் &amp; ஆன்ம முக்தி (Advanced Siddhanta &amp; Moksha)</h2>
      <p>பொதுத்தேர்வு (O/L &amp; A/L) வழிகாட்டுதலும், சனாதன-சைவ-சன்மார்க்க மெய்ஞ்ஞானமும்.</p>
      <ul style="margin-left:20px; margin-top:10px; line-height:1.8;">
        <li>சிவஞானபோதம், சிவஞான சித்தியார், திருவருட்பயன் உள்ளிட்ட 14 மெய்கண்ட சாத்திரங்கள்</li>
        <li>காஞ்சி மகா பெரியவா அருளிய 'தெய்வத்தின் குரல்' சனாதன தர்ம ஒருமைப்பாடு</li>
        <li>திருவள்ளுவர் அருளிய 133 அதிகாரங்களின் உலக தர்ம அறநெறிகள் (185 இசைத் திரைப்படங்கள்)</li>
        <li>வள்ளலார் சுத்த சன்மார்க்கம்: ஜீவகாருண்யம், அருட்பெருஞ்சோதி அகவல், மரணமிலாப் பெருவாழ்வு</li>
      </ul>
    </div>

    <div style="text-align:center; margin: 40px 0;">
      <a href="kalvi.html" class="gs-banner-btn" style="padding:14px 28px; font-size:1.05rem;">
        12 தரங்களின் பாடங்களைப் பார்வையிட செல்க (Explore All 12 Grades) →
      </a>
    </div>
  </main>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
    with open('syllabus.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated syllabus.html")

generate_syllabus()

# Generate Classes (classes.html)
def generate_classes():
    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>வகுப்புகள் — ஆன்லைன் &amp; குருகுலப் பயிற்சி | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் ஆன்லைன் வகுப்புகள், வாராந்திர சைவ நெறிப் பயிலரங்குகள், திருமுறை இசை வகுப்புகள் &amp; சேர்க்கை வழிகாட்டி.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header('classes')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">🏛️ குருகுல மரபு • ஆன்லைன் &amp; நேரலை வகுப்புகள் 🏛️</div>
      <h1>வகுப்புகள் (Classes &amp; Gurukulam)</h1>
      <h2>Spiritual Learning, Online Classes &amp; Vedic Studies</h2>
      <div class="verse-quote">"ஆசிரியன் உரைத்ததை மனங்கொண்டு ஓதி உலகினில் மேன்மையடைவாய்" — மூதுரை</div>
      <p class="hero-desc">
        மாணவர்கள், இளைஞர்கள் மற்றும் ஆன்மீக ஆர்வலர்களுக்கு சைவ நெறி, திருமுறை இசை, திருக்குறள் விழுமியங்கள் மற்றும் தெய்வத்தின் குரல் வழிகாட்டலில் நடைபெறும் சிறப்பு வகுப்புகள்.
      </p>
    </div>

    <!-- Live Google Sites Link Bar -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 கூகிள் சைட்ஸ் 'வகுப்புகள்' பக்கம் (Classes on Google Sites)</h3>
        <p>Google Sites தளத்தின் வகுப்புகள் பக்கமும் நேரடியாக இணைக்கப்பட்டுள்ளது.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/classes/untitled-page" target="_blank" rel="noopener" class="gs-banner-btn">
        கூகிள் தள வகுப்புகள் காண்க ↗
      </a>
    </div>

    <!-- Class Types Grid -->
    <div class="canonical-grid" style="margin-top:30px;">
      <div class="canonical-card">
        <h4>📖 சைவ நெறி பள்ளிப் பாட வகுப்புகள் (Grades 1-12)</h4>
        <p>பள்ளி மாணவர்களுக்கான தரம் 1 முதல் 12 வரையிலான சைவ நெறிப் பாடங்கள், தேவாரத் திருப்பதிகங்கள் மற்றும் பொதுத்தேர்வு வழிகாட்டுதல்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">வார இறுதி வகுப்புகள் (Weekend Classes)</span>
      </div>

      <div class="canonical-card">
        <h4>🎵 திருமுறை இசை &amp; பண்ணிசைப் பயிலரங்கம்</h4>
        <p>தேவாரம், திருவாசகம், திருப்புகழ் மற்றும் திருவருட்பா பாடல்களை உரிய பண்களோடு பண்ணிசைத்துப் பாடும் இசைப் பயிற்சி.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">இறை இசைப் பயிற்சி</span>
      </div>

      <div class="canonical-card">
        <h4>📜 திருக்குறள் &amp; சன்மார்க்க அறநெறி வகுப்பு</h4>
        <p>வாழ்க்கை நெறிமுறைகள், மன அமைதி, ஜீவகாருண்யம் மற்றும் ஆன்மநேய ஒருமைப்பாட்டுக்கான சிறப்புச் சொற்பொழிவுகள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">அறநெறிச் சிந்தனை</span>
      </div>

      <div class="canonical-card">
        <h4>⚜️ தெய்வத்தின் குரல் &amp; வேத ஞானப் பயிலரங்கம்</h4>
        <p>காஞ்சி மகா பெரியவா அருளிய சனாதன தர்மம், சிவ-விஷ்ணு ஐக்கியம், கோசம்ரக்ஷணம் மற்றும் ஆத்ம விசாரம்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">வேத தரிசனம்</span>
      </div>
    </div>

    <!-- Contact & Enrollment Box -->
    <div class="scripture-study-section" style="margin-top:30px;">
      <span class="source-badge">வகுப்புச் சேர்க்கை &amp; தொடர்பு மையம்</span>
      <h2>வகுப்பில் சேரவும், மேலதிக விவரங்களுக்கும் (Contact &amp; Admission)</h2>
      <p>
        வகுப்புகள் ஆன்லைன் மூலமாகவும் (Google Meet / Zoom), கோயம்புத்தூர் மையத்திலும் நடைபெறுகின்றன. விரும்பும் அன்பர்கள் கீழ்க்கண்ட முகவரியிலோ அல்லது YouTube தளம் வாயிலாகவோ தொடர்பு கொள்ளலாம்.
      </p>
      <div style="margin-top: 16px; padding: 16px 20px; background: rgba(212, 175, 55, 0.08); border-radius: 12px; border: 1px solid var(--border-gold);">
        <p style="color: var(--gold-bright); font-weight: 700; font-size: 1.05rem;">📍 குரு குல தேசம் (Guru Kula Desam)</p>
        <p style="color: var(--text-main); margin-top: 6px;">32, SSS Jaya Enclave, Kovaipudur, Coimbatore, 641042, Tamil Nadu, India.</p>
        <p style="color: var(--text-muted); margin-top: 4px;">அதிகாரப்பூர்வ இணையதளம்: gurukuladesam.com</p>
      </div>
    </div>
  </main>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
    with open('classes.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated classes.html")

generate_classes()

# Generate YouTube Directory (youtube.html)
def generate_youtube():
    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>YouTube களஞ்சியம் — 580 இசைப் படைப்புகள் | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் அதிகாரப்பூர்வ YouTube சேனல் மற்றும் 580 இசைத் திரைப்படங்கள், திருக்குறள் மற்றும் சிவ பக்திப் பாடல்களின் முழுமையான பட்டியல்.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header('youtube')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">▶ YouTube அதிகாரப்பூர்வ ஆன்மீக ஒளிக்களஞ்சியம் ▶</div>
      <h1>குரு குல தேசம் YouTube தளம்</h1>
      <h2>Official YouTube Channel — 580 Sacred Musical Productions</h2>
      <div class="verse-quote">"பாட வாராய் நற்றமிழால் பாடி மகிழ்ந்திரு" — தேவாரம்</div>
      <p class="hero-desc">
        திருக்குறள் 133 அதிகாரங்களின் சினிமா இசைத் திரைப்படங்கள், பன்னிரு திருமுறைப் பதிகங்கள், கந்த சஷ்டி, சக்தி போற்றிகள் மற்றும் வள்ளலார் அருள்நெறிப் பாடல்களை உடனுக்குடன் கண்டு களிக்க YouTube சேனலுக்குச் சந்தாதாரராகுங்கள்.
      </p>
    </div>

    <!-- Live Google Sites YouTube Page Link -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 கூகிள் சைட்ஸ் YouTube பக்கம்</h3>
        <p>கூகிள் தளத்திலும் YouTube பக்க இணைப்புகள் ஒருங்கிணைக்கப்பட்டுள்ளன.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/youtube" target="_blank" rel="noopener" class="gs-banner-btn">
        கூகிள் தளத்தில் YouTube காண்க ↗
      </a>
    </div>

    <div style="text-align:center; margin:30px 0;">
      <a href="https://www.youtube.com/@guru-kula-desam?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="gs-banner-btn" style="background:#e63946; color:#fff; font-size:1.1rem; padding:14px 34px;">
        ▶ YouTube சேனலில் இணையுங்கள் (Subscribe Now)
      </a>
    </div>

    <!-- YouTube Categories -->
    <div class="canonical-grid">
      <div class="canonical-card" onclick="location.href='thirukkural.html'" style="cursor: pointer;">
        <h4>📜 திருக்குறள் சினிமா படங்கள் (185 படைப்புகள்)</h4>
        <p>133 அதிகாரங்களின் முழுமையான இசை மற்றும் சினிமா பட வெளியீடுகள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">பார்வையிட ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='saiva-neri.html'" style="cursor: pointer;">
        <h4>🔱 சிவ நெறிப் பதிகங்கள் (172 பாடல்கள்)</h4>
        <p>தேவாரம், திருவாசகம், திருமந்திரம் மற்றும் சிவபுராண சினிமா படங்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">பார்வையிட ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='sanmargam.html'" style="cursor: pointer;">
        <h4>✨ வள்ளலார் சன்மார்க்கம் (94 பாடல்கள்)</h4>
        <p>அருட்பெருஞ்சோதி அகவல், தனிப்பெருங்கருணை மற்றும் ஜீவகாருண்யம்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">பார்வையிட ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='irai-isai-virundhu.html'" style="cursor: pointer;">
        <h4>🎵 இறை இசை விருந்து (5 சிறப்புப் பாடல்கள்)</h4>
        <p>பாலும் தெளிர் தேனும், குரு வணக்கம், கந்தர் அநுபூதி, சிவபுராணம்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">பார்வையிட ↗</span>
      </div>
    </div>
  </main>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
    with open('youtube.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated youtube.html")

generate_youtube()

# Generate Google Site Overview (google-site.html)
def generate_google_site():
    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>கூகிள் தளம் நேரடி இணைப்பு — Google Sites Mirror | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் அதிகாரப்பூர்வ கூகிள் தளம் (Google Sites). அனைத்து 12 தரங்கள், பாடத்திட்டம், இறை இசை விருந்து மற்றும் வகுப்புகள்.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

{get_header('google_site')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">🌐 கூகிள் சைட்ஸ் அதிகாரப்பூர்வ தளம் 🌐</div>
      <h1>குரு குல தேசம் — Google Sites இணைப்பு</h1>
      <h2>Official Google Sites Mirror &amp; Direct Access Portal</h2>
      <div class="verse-quote">"ஒன்றே குலமும் ஒருவனே தேவனும்" — திருமந்திரம்</div>
      <p class="hero-desc">
        கூகிள் சைட்ஸ் (Google Sites) தளத்தில் உருவாக்கப்பட்ட குரு குல தேசம் பக்கங்கள் மற்றும் பாடநெறிகள். கீழ்க்கண்ட நேரடி இணைப்புகள் மூலமாக அத்தளத்தின் அனைத்து பக்கங்களையும் பார்வையிடலாம்.
      </p>
    </div>

    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 முதன்மை கூகிள் தளம் (Public Google Site)</h3>
        <p style="color:var(--gold-soft); font-family:monospace; margin-top:4px;">https://sites.google.com/view/wwwgurukuladesamcom</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom" target="_blank" rel="noopener" class="gs-banner-btn">
        முகப்பை திறக்க ↗
      </a>
    </div>

    <h2 class="section-divider-title">கூகிள் தளத்தின் அனைத்துப் பக்கங்கள் (All Google Sites Pages)</h2>

    <div class="canonical-grid">
      <div class="canonical-card" onclick="window.open('https://sites.google.com/view/wwwgurukuladesamcom/home', '_blank')" style="cursor:pointer;">
        <h4>🏠 முகப்புப் பக்கம் (Home)</h4>
        <p>குரு குல தேசம் கூகிள் சைட்ஸ் முகப்புப் பக்கம் மற்றும் தலைமையக முகவரி.</p>
        <span style="color:var(--gold); font-size:0.8rem; font-weight:700;">திறக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="window.open('https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-1', '_blank')" style="cursor:pointer; border-color:var(--gold-bright);">
        <h4>📖 சைவ நெறி — தரம் 1</h4>
        <p>கூகிள் தளத்தில் உள்ள 60 முழுமையான பாடப் புத்தகப் பக்கங்கள்.</p>
        <span style="color:var(--gold-bright); font-size:0.8rem; font-weight:700;">திறக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="window.open('https://sites.google.com/view/wwwgurukuladesamcom/home/syllabus/%E0%AE%87%E0%AE%B1-%E0%AE%87%E0%AE%9A-%E0%AE%B5%E0%AE%B0%E0%AE%A8%E0%AE%A4', '_blank')" style="cursor:pointer;">
        <h4>🎵 இறை இசை விருந்து</h4>
        <p>கூகிள் தளத்தில் பதிக்கப்பட்டுள்ள 5 தெய்வீக இசை வீடியோக்கள்.</p>
        <span style="color:var(--gold); font-size:0.8rem; font-weight:700;">திறக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="window.open('https://sites.google.com/view/wwwgurukuladesamcom/home/syllabus/untitled-page', '_blank')" style="cursor:pointer;">
        <h4>📜 பாடத்திட்டம் (Syllabus)</h4>
        <p>கூகிள் தளத்தில் உள்ள பாடத்திட்டப் பக்கம்.</p>
        <span style="color:var(--gold); font-size:0.8rem; font-weight:700;">திறக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="window.open('https://sites.google.com/view/wwwgurukuladesamcom/home/classes/untitled-page', '_blank')" style="cursor:pointer;">
        <h4>🏛️ வகுப்புகள் (Classes)</h4>
        <p>கூகிள் தளத்தில் உள்ள ஆன்லைன் வகுப்புகள் பக்கம்.</p>
        <span style="color:var(--gold); font-size:0.8rem; font-weight:700;">திறக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="window.open('https://sites.google.com/view/wwwgurukuladesamcom/home/youtube', '_blank')" style="cursor:pointer;">
        <h4>▶ YouTube பக்கம்</h4>
        <p>கூகிள் தளத்தில் உள்ள YouTube ஒளிக்களஞ்சியப் பக்கம்.</p>
        <span style="color:var(--gold); font-size:0.8rem; font-weight:700;">திறக்க ↗</span>
      </div>
    </div>
  </main>

{get_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""
    with open('google-site.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated google-site.html")

generate_google_site()

# 5. Update existing pages (index.html, saiva-neri.html, thirukkural.html, sanmargam.html, murugan.html, sakthi.html, vinayagar.html, vaishnava.html, about.html)
existing_pages = [
    ('index.html', 'home'),
    ('saiva-neri.html', 'saiva'),
    ('thirukkural.html', 'thirukkural'),
    ('sanmargam.html', 'sanmargam'),
    ('murugan.html', 'murugan'),
    ('sakthi.html', 'sakthi'),
    ('vinayagar.html', 'vinayagar'),
    ('vaishnava.html', 'vaishnava'),
    ('about.html', 'about'),
]

for filename, active_tag in existing_pages:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace header
        header_pattern = r'<header class="site-header">.*?</header>'
        new_hdr = get_header(active_tag)
        content = re.sub(header_pattern, new_hdr, content, flags=re.DOTALL)

        # Replace footer
        footer_pattern = r'<footer class="site-footer">.*?</footer>'
        new_ftr = get_footer()
        content = re.sub(footer_pattern, new_ftr, content, flags=re.DOTALL)

        # If index.html, also add a quick-access card to Kalvi Hub and Irai Isai in canonical-grid if not present
        if filename == 'index.html' and 'tharam-1.html' not in content:
            extra_cards = """
        <div class="canonical-card" onclick="location.href='kalvi.html'" style="cursor: pointer; border-color: var(--gold-bright);">
          <h4>📖 சைவ நெறி கல்வி (Grades 1-12)</h4>
          <p>தரம் 1 முதல் 12 வரையிலான சைவ நெறிப் பாடத்திட்டம், தரம் 1-ன் 60 பாடநூல் படங்கள் மற்றும் வழிகாட்டி.</p>
          <span style="color: var(--gold-bright); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">கல்விப் பிரிவு காண்க ↗</span>
        </div>

        <div class="canonical-card" onclick="location.href='irai-isai-virundhu.html'" style="cursor: pointer;">
          <h4>🎵 இறை இசை விருந்து (5 பாடல்கள்)</h4>
          <p>பாலும் தெளிர் தேனும், குரு வணக்கம், கந்தர் அநுபூதி, பாரதியார் பாடல் & சிவபுராணம்.</p>
          <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">இறை இசை கேட்க ↗</span>
        </div>
"""
            content = content.replace('<div class="canonical-grid">', '<div class="canonical-grid">' + extra_cards, 1)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated header and footer in {filename}")

# 6. Synchronize all HTML files and assets to site/ and docs/
all_html_files = [
    'index.html', 'saiva-neri.html', 'thirukkural.html', 'sanmargam.html',
    'murugan.html', 'sakthi.html', 'vinayagar.html', 'vaishnava.html', 'about.html',
    'kalvi.html', 'tharam-1.html', 'tharam-2.html', 'tharam-3.html', 'tharam-4.html',
    'tharam-5.html', 'tharam-6.html', 'tharam-7.html', 'tharam-8.html', 'tharam-9.html',
    'tharam-10.html', 'tharam-11.html', 'tharam-12.html',
    'irai-isai-virundhu.html', 'syllabus.html', 'classes.html', 'youtube.html', 'google-site.html'
]

# Ensure embed files are also retained
embed_files = [f for f in os.listdir('.') if f.startswith('embed_') and f.endswith('.html')]
all_html_files.extend(embed_files)

for target_dir in ['site', 'docs']:
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(os.path.join(target_dir, 'assets', 'css'), exist_ok=True)
    os.makedirs(os.path.join(target_dir, 'assets', 'js'), exist_ok=True)
    os.makedirs(os.path.join(target_dir, 'assets', 'data'), exist_ok=True)
    
    # Copy assets
    shutil.copy('assets/css/style.css', os.path.join(target_dir, 'assets', 'css', 'style.css'))
    shutil.copy('assets/js/main.js', os.path.join(target_dir, 'assets', 'js', 'main.js'))
    if os.path.exists('assets/data/catalog.json'):
        shutil.copy('assets/data/catalog.json', os.path.join(target_dir, 'assets', 'data', 'catalog.json'))

    # Copy HTML files
    for h in all_html_files:
        if os.path.exists(h):
            shutil.copy(h, os.path.join(target_dir, h))
    
    # Copy CNAME
    if os.path.exists('CNAME'):
        shutil.copy('CNAME', os.path.join(target_dir, 'CNAME'))

    print(f"Synchronized all {len(all_html_files)} HTML files and assets to {target_dir}/")

print("\nAll Google Site pages successfully created and integrated into Gurukuladesam repository!")
