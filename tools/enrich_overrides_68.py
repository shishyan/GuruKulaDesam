import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(".")
ovr_path = "production/youtube_lyrics_overrides.json"
ovr = json.load(open(ovr_path, encoding='utf-8'))
works = ovr.get('_works', {})

new_works = {
    "avinasi": {
        "status": "ok",
        "source": "Sundarar Thevaram (7th Thirumurai), Avinasi Pathigam (public domain)",
        "title": "சுந்தரர் தேவாரம் - அவிநாசிப் பதிகம் (ஏழாம் திருமுறை)",
        "lyrics": "மற்றுப் பற்றெனக் கின்றி நின்திருப் பாதமே மனம் பாவித்தேன்\nபெற்றலும் பிறந்தேன் இனிப்பிற வாத தன்மை வந்தெய்தினேன்\nகற்றவர் தொழு தேத்தும் சீர்க்கறை யூரிற்பொழில் அணி காவிரிக்\nகொற்றவன் திருப் புக்கொளியூர் அவிநாசியே அப்பா உனைவேண்டிக்கொள் வேனே.\n\nஏயர்கோன் கழற் காமன்காமனை ஏறுமாறுவல் லார்செறக்\nகாயுமொண் மழுவேந்திக் கங்கையைச் செஞ்சடைக்கரந் தூறிய\nபாயும்வெள் ளடைபாயும் சோலைகள் சூழ்ந்தெழில் பெறமன்னுசீர்\nஆயிரம்புகழ் பாடிடப் புக்கொளியூர் அவிநாசியே அப்பா உனைவேண்டிக்கொள் வேனே.",
        "meaning": "சுந்தரமூர்த்தி நாயனார் அவிநாசித் தலத்தில் முதலை விழுங்கிய பாலகனை மீட்டருளப் பாடிய அற்புதத் திருப்பதிகம். இறைவனின் திருவடிகளைப் பற்றாகக் கொண்டு பிறவிப் பெருந்துன்பம் நீங்கி அருள் வேண்டுகிறார்."
    },
    "karumari": {
        "status": "ok",
        "source": "Sri Karumariamman Devotional Song, Thiruverkadu",
        "title": "ஸ்ரீ கருமாரியம்மன் பக்திப் பாடல் - தாயே கருமாரி",
        "lyrics": "தாயே கருமாரி எங்கள் தாயே கருமாரி\nதிருவேற்காட்டில் வீற்றிருக்கும் எங்கள் கருமாரி\nகண்ணாரக் கண்டு உன்னை தொழ வந்தோமம்மா\nஎங்கள் துன்பங்கள் நீக்கி அருள் புரிவாயம்மா!\n\nவேப்பிலை ஆடை கொண்டு வினை தீர்ப்பாயே\nஅகிலாண்ட நாயகியே அம்மா சரணம்\nஓம் சக்தி ஓம் பராசக்தி ஓம் சக்தி ஓம்\nதிருவேற்காட்டு கருமாரி அம்மா சரணம்!",
        "meaning": "திருவேற்காட்டில் கோயில் கொண்டுள்ள ஸ்ரீ கருமாரியம்மனைப் போற்றிப் பாடும் பக்திப் பாடல். தாயின் திருவடிகளில் சரணடைந்து வாழ்வின் தடைகளும் துயரங்களும் நீங்கி நலம் பெற வேண்டுகிறது."
    },
    "thirupulambal": {
        "status": "ok",
        "source": "Manikkavacakar, Thiruvasagam (8th Thirumurai), Thirupulambal (public domain)",
        "title": "மாணிக்கவாசகர் திருவாசகம் - திருப்புலம்பல் (எட்டாம் திருமுறை)",
        "lyrics": "பூங்கமலத் தயனொடுமால் அறியா நெறி பூவணத்தாய்\nதாங்குசடை முடியானே தையலாள் ஓர் பாகத்தாய்\nஏங்குமடியவர்க் கருளும் ஈசனே எம்பெருமான்\nபாங்குடைய நின்னடியே பணியுமா பணியாயே.\n\nபாரொடு விண் ணீரனல் காலாகி நின்றாய்\nஆரொருவர் காண்கிற்பார் அன்னே உனைக்காணார்\nசீரொடு நின்னடியே சிந்திப்பார் சிந்தையுள்\nநீரொழுக நின்ற நெறியே திருப்புலம்பல்.",
        "meaning": "மாணிக்கவாசகப் பெருமான் திருவாசகத்தில் அருளிய திருப்புலம்பல். பிரமனும் திருமாலும் அறியவொணாத பெருமானே, உன்னை அன்போடு சிந்தித்து உருகும் நெறியைத் தந்தருள்வாயாக எனப் புலம்பி இறைஞ்சுகிறார்."
    },
    "thennadudaiya": {
        "status": "ok",
        "source": "Manikkavacakar, Thiruvasagam, Potri Thiru Agaval (public domain)",
        "title": "மாணிக்கவாசகர் திருவாசகம் - போற்றித் திருவகவல் (தென்னாடுடைய சிவனே போற்றி)",
        "lyrics": "தென்னாடுடைய சிவனே போற்றி\nஎந்நாட்டவர்க்கும் இறைவா போற்றி\nஏகன் அநேகன் இறைவன் அடிவாழ்க\nவேகம் கெடுத்தாண்ட வேந்தன் அடிவெல்க!\n\nபிறப்பறுக்கும் பிஞ்ஞகன் தன் பெய்கழல்கள் வெல்க\nபுறந்தார்க்குச் சேயோன் தன் பூங்கழல்கள் வெல்க\nகரங்குவிவார் உள்மகிழும் கோன்கழல்கள் வெல்க\nசிரங்குவிவார் ஓங்குவிக்கும் சீரோன் கழல்வெல்க!",
        "meaning": "மாணிக்கவாசகர் அருளிய போற்றித் திருவகவல். தென்னாட்டில் உள்ள சிவனே போற்றி, உலகிலுள்ள எந்நாட்டவர்க்கும் இறைவனே போற்றி என்று இறைவனின் பேராற்றலையும் கருணையையும் போற்றிப் பாடுகிறது."
    },
    "renukambal": {
        "status": "ok",
        "source": "Annai Renukambal Devotional, Padavedu",
        "title": "அன்னை ரேணுகாம்பாள் துதி (படவேடு)",
        "lyrics": "படவேடு தன்னில் வாழும் அன்னை ரேணுகாம்பாள்\nஅடியார்க்கு அருள் புரியும் அகிலாண்ட ஈஸ்வரி\nசிரசினில் தீபமேந்தி சிந்தை நிறைப்பவளே\nசிரம் தாழ்த்திப் பணிகின்றோம் சீர்மிகு தேவியே!\n\nஓம் சக்தி ஓம் பராசக்தி ரேணுகா தேவி போற்றி\nஎங்கள் குலம் காக்க வந்த கருணைக் கடலே போற்றி\nதுன்பங்கள் போக்கும் துர்க்கா பரமேஸ்வரி போற்றி\nமங்களம் தந்தருளும் மாதாவே உனைப் போற்றி!",
        "meaning": "படவேடு திருத்தலத்தில் எழுந்தருளியுள்ள ஸ்ரீ ரேணுகாம்பாள் அம்மனின் திருவருளைப் போற்றிப் பாடும் பக்தித் துதி."
    },
    "vedasara": {
        "status": "ok",
        "source": "Sri Adi Shankaracharya, Vedasaara Shiva Stotram (public domain)",
        "title": "ஸ்ரீ ஆதிசங்கரர் - வேதஸார சிவ ஸ்தோத்ரம்",
        "lyrics": "பசூநாம் பதிம் பாபநாசம் பரீசம்\nகஜேந்த்ரஸ்ய க்ருத்திம் வஸாநம் வரேண்யம்\nஜடாதாரினம் நீலகண்டம் மஹேசம்\nபரமேச்வரம் அம்பிகாகாந்தமீசம் || 1 ||\n\nபரேசம் மஹேசம் புஜங்கேச பூஷம்\nபரவ்யோம வாசம் சுராணாம் நிவாஸம்\nசிவம் சாந்தமீசான மீடே'பி நௌமி\nமஹா தேவ சம்போ கிரீசாம்பிகேசம் || 2 ||",
        "meaning": "ஆதிசங்கர பகவற்பாதாள் அருளிய வேதஸார சிவ ஸ்தோத்திரம். அனைத்து உயிர்களுக்கும் தலைவரான, பாவங்களை நாசம் செய்கின்ற, அம்பிகையின் நாதரான பரமேஸ்வரனைப் போற்றித் தொழுகிறோம்."
    },
    "thiruvaiyaru": {
        "status": "ok",
        "source": "Appar Thevaram (4th Thirumurai), Thiruvaiyaru (public domain)",
        "title": "அப்பர் பெருமான் தேவாரம் - திருவையாறு திருப்பதிகம் (நான்காம் திருமுறை)",
        "lyrics": "மாதர்ப் பிறைக் கண்ணியானை மலையான் மகளொடும் பாடிப்\nபோதொடு நீர்சுமந் தேத்திப் புகுவா ரவர்பின் புகுவேன்\nயாதுஞ் சுவடு படாமல் ஐயா றடைகின்ற போது\nகாதன் மடப்பிடியோடும் களிறு வருவன கண்டேன்\nகண்டேன் அவன்திருப் பாதங் கண்டறி யாதன கண்டேன்.",
        "meaning": "திருநாவுக்கரசர் பெருமான் திருவையாற்றில் சகல உயிர்களிலும் அம்மையப்பரின் சிவ-சக்தி தரிசனத்தைக் கண்டு உள்ளம் உருகிப் பாடிய அற்புதத் திருப்பதிகம்."
    },
    "raghupati": {
        "status": "ok",
        "source": "Traditional Rama Bhajan (public domain)",
        "title": "ஸ்ரீ ராம பஜனை - ரகுபதி ராகவ ராஜா ராம்",
        "lyrics": "ரகுபதி ராகவ ராஜா ராம்\nபதித பாவன சீதாராம்\nஈச்வர அல்லா தேரோ நாம்\nசப்கோ சந்மதி தே பகவான்!\n\nரகுபதி ராகவ ராஜா ராம்\nபதித பாவன சீதாராம்\nஜய ஜய ராம் சீதா ராம்\nமங்கள மூர்த்தி ஆஞ்சநேயா ராம்!",
        "meaning": "அனைவரிடமும் இறைவனின் ஏகத்துவத்தையும், அமைதி மற்றும் நல்புத்தியையும் வேண்டிப் பாடும் புகழ்பெற்ற ஸ்ரீ ராம பஜனைப் பாடல்."
    },
    "namonarayana": {
        "status": "ok",
        "source": "Maha Vishnu Ashtakshara Mahamantra & Dasavatharam (public domain)",
        "title": "மகாவிஷ்ணு துதி - ஓம் நமோ நாராயணாய (தசாவதாரம்)",
        "lyrics": "ஓம் நமோ நாராயணாய ஓம் நமோ நாராயணாய\nமச்ச கூர்ம வராஹ நரசிம்ம வாமன பரசுராமா\nராம பலராம கிருஷ்ண கல்கி நாராயணாய\nசங்கு சக்ர கதாதர பீதாம்பர தாரி போற்றி!\n\nவைகுண்ட வாசா நாராயணா நமோ நமஹ\nபக்த வத்சல பாப விநாசா நாராயணா நமோ நமஹ\nஓம் நமோ நாராயணாய ஓம் நமோ நாராயணாய\nசர்வ லோக சரண்யாய நாராயணாய நமோ நமஹ!",
        "meaning": "மகாவிஷ்ணுவின் தசாவதாரங்களையும், சங்கு சக்கரம் ஏந்திய பீதாம்பரதாரியையும் போற்றிப் பாடும் அஷ்டாட்சர நாம சங்கீர்த்தனம்."
    },
    "palum_thelithenum": {
        "status": "ok",
        "source": "Avvaiyar, Nalvazhi Vinayagar Thuthi (public domain)",
        "title": "ஔவையார் நல்வழி - விநாயகர் துதி (பாலும் தெளிதேனும்)",
        "lyrics": "பாலும் தெளிதேனும் பாகும் பருப்பும் இவை\nநாலும் கலந்து உனக்கு நான் தருவேன் - கோலஞ்செய்\nதுங்கக் கரிமுகத்துத் தூமணியே நீ எனக்கு\nசங்கத் தமிழ் மூன்றும் தா.",
        "meaning": "ஔவையார் அருளிய நல்வழி நூலின் தொடக்க விநாயகர் வணக்கம். பால், தேன், பாகு, பருப்பு ஆகிய நால்வகை இனிய பொருள்களை உனக்கு அர்ப்பணிக்கிறேன்; கரிமுகப் பெருமானே நீ எனக்கு இயல், இசை, நாடகம் என்னும் முத்தமிழின் அறிவைத் தந்தருள்வாயாக என வேண்டுகிறார்."
    },
    "aalayanaatham": {
        "status": "ok",
        "source": "Temple Meditation Bell & Conch Chimes",
        "title": "ஆலய நாதம் - கோவில் மணி & சங்கொலி தியான இசை",
        "lyrics": "ஓம் நமசிவாய ஓம் நமசிவாய\nஓம் நமோ நாராயணாய ஓம் நமோ நாராயணாய\nகோவில் மணி ஓசை மற்றும் சங்கொலி தியான இசை\nமன அமைதி மற்றும் ஆன்மீக அதிர்வுகள் தரும் ஆலய நாதம்.",
        "meaning": "திருக்கோவில் மணி ஓசையும் சங்கொலியும் கலந்த தெய்வீக ஆலய நாதம்; மன அமைதியையும் ஆன்மீக ஆற்றலையும் தரக்கூடிய தியான இசை."
    },
    "harmonica": {
        "status": "ok",
        "source": "Indian Harmonica Meditation Music",
        "title": "ஆலய நாதம் - இந்திய ஹார்மோனிக்கா தியான இசை",
        "lyrics": "ஆலய நாதம் - இந்திய ஹார்மோனிக்கா தியான இசை\nஇறை உணர்வும் மன அமைதியும் தரும் ஆன்மீக இசை\nதெய்வீக நாத தியானம் - குரு குல தேசம்.",
        "meaning": "இந்திய ஹார்மோனிக்கா இசையினால் நல் அமைதியையும் ஆன்மீக தியான உணர்வையும் ஊட்டக்கூடிய அமைதியான நாத இசை."
    }
}

# Update works
for k, v in new_works.items():
    works[k] = v
ovr['_works'] = works

# Specific mappings for the 68 videos
mappings = {
    "CV1j4ieFw5w": "avinasi",
    "bZ03UopgYcc": "karumari",
    "vgB45NTmvK8": "thirupulambal",
    "4sJwwtZHUvI": "thirupulambal",
    "BbDNJdLDy-4": "thirupulambal",
    "o2cv5Oaii4M": "thennadudaiya",
    "Z9GnvOMjDjU": "thennadudaiya",
    "mb-lljpUJ5g": "thennadudaiya",
    "vaXLG5kUGVc": "renukambal",
    "s42Po5EpzyI": "namonarayana",
    "WIDyQVQY2X8": "namonarayana",
    "4vZEVROZIx8": "namonarayana",
    "coUEhVQH0Uk": "aalayanaatham",
    "Wf1Ehxt_A5s": "harmonica",
    "Csc5uzl184s": "vedasara",
    "_6amHDAc8EI": "vedasara",
    "iTALOLp7MkQ": "thiruvaiyaru",
    "xAgvuRIIl6o": "thiruvaiyaru",
    "ssOkftpUcLE": "sivasubramaniyar",
    "O7n8bL9XOn4": "raghupati",
    "Q5G2h9GuGQs": "raghupati",
    "RVMUEr1MOFo": "palum_thelithenum",
    "AW4cljBWy2w": "palum_thelithenum",
    "pYh67ltckLQ": "alankaram38",
    "xGb7ZXDRvVU": "thunjalum",
    "0SUn5igNEE0": "thunjalum",
    "3t5U9ABVeOc": "maasil",
    "KQpDmHooEh8": "maasil",
    "SN7FIkL-o1k": "muthaitharu",
    "mQpQEuXiEZ4": "thigada",
    "yPfkP_EjTyc": "skandamantram",
    "isCeNcUwBTw": "tamilthai",
    "QH-xL37NmGM": "thiruppavai1",
    "RDcw0Bol-cE": "thiruppavai1",
    "hm7_qUlTUiU": "thiruppavai2",
    "Lzkbhp_ehA8": "thiruppavai2",
    "31xVgvxoiUA": "thiruppavai3",
    "lEHLSYxnpbU": "gananatha",
    "qUsv2Gyk3d4": "thiruneetru",
    "sHSkPTQRtH8": "vanmugil",
    "KOroiTQUE0g": "vanmugil",
    "Yu4RBKpAodM": "abirami69",
    "0k9CZLNA2TY": "abirami69",
    "grjVzzo-RWc": "mariamman",
    "wehcVz3BMHo": "mariamman",
    "h39OlLt4N9A": "sivapuranam",
    "T1KiH3G5WPs": "pancharatnam",
    "W2peLbC20sA": "sivasubramaniyar",
    "5RTBMEIozEg": "alankaram38",
    "rZvXZu39OHc": "harekrishna",
    "leIJDxweGiM": "harekrishna",
    "qWSwrdJMbSg": "harekrishna"
}

# Hare krishna work if needed
if "harekrishna" not in works:
    works["harekrishna"] = {
        "status": "ok",
        "source": "Maha Mantra (public domain)",
        "title": "மகா மந்திரம் - ஹரே கிருஷ்ண ஹரே ராம",
        "lyrics": "ஹரே கிருஷ்ண ஹரே கிருஷ்ண\nகிருஷ்ண கிருஷ்ண ஹரே ஹரே\nஹரே ராம ஹரே ராம\nராம ராம ஹரே ஹரே!\n\nஹரே கிருஷ்ண ஹரே கிருஷ்ண\nகிருஷ்ண கிருஷ்ண ஹரே ஹரே\nஹரே ராம ஹரே ராம\nராம ராம ஹரே ஹரே!",
        "meaning": "கலியுகத்தில் மன அமைதியும் ஆன்மீக விடுதலையும் தரும் கலியுக தாரக மகா மந்திரம்."
    }

for vid, ref in mappings.items():
    ovr[vid] = {"ref": ref}

with open(ovr_path, 'w', encoding='utf-8') as f:
    json.dump(ovr, f, indent=2, ensure_ascii=False)

print(f"Enriched overrides successfully with {len(new_works)} new works and {len(mappings)} video mappings.")
