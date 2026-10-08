"""
Comprehensive Scripture Detection & Disambiguation Engine
channel: @guru-kula-desam
"""

import json
import re
import os
import csv
import shutil
import hashlib

MASTER_JSON = "master_all_598_songs_catalog.json"
MASTER_CSV = "master_all_598_songs_catalog.csv"
CATALOG_JSON = "assets/data/catalog.json"
CATALOG_JS = "assets/data/catalog.js"
PENDING_JSON = "channel_direct_uploads_pending.json"
LIVE_META_JSON = os.path.join("data", "dumps", "live_youtube_metadata.json")

with open(MASTER_JSON, "r", encoding="utf-8") as f:
    master = json.load(f)

with open(CATALOG_JSON, "r", encoding="utf-8") as f:
    catalog_data = json.load(f)

live_meta = {}
if os.path.exists(LIVE_META_JSON):
    with open(LIVE_META_JSON, "r", encoding="utf-8") as f:
        live_meta = json.load(f)

# Build lookup
cat_by_id = {}
for c_name, items in catalog_data.items():
    for it in items:
        cat_by_id[it["id"]] = (c_name, it)

PREFIXES_TAMIL = [
    "திருக்குறள்", "திருவாசகம்", "தேவாரம்", "திருவருட்பா", "கந்தர் அலங்காரம்",
    "கந்தர் அநுபூதி", "கந்தர் அனுபூதி", "கந்த சஷ்டி கவசம்", "கந்த புராணம்",
    "திருப்புகழ்", "திருப்பாவை", "பெரியாழ்வார் திருமொழி", "பெரியபுராணம்",
    "பன்னிரு திருமுறை", "திருமந்திரம்", "அபிராமி அந்தாதி", "விநாயகர் அகவல்",
    "விநாயகர் நான்மணிமாலை", "ஆதிசங்கரர்", "சிவ ஸ்தோத்திரம்", "சிவ நாமாவளி",
    "நாம சங்கீர்த்தனம்", "தமிழ்த்தாய் வாழ்த்து", "தேசிய கீதம்", "ஆலய நாதம்",
    "இசைத் தியானம்", "சிவ பக்திப் பாடல்", "முருகன் துதி", "விஷ்ணு துதி",
    "அம்மன் துதி", "விநாயகர் துதி", "பக்திப் பாடல்", "நவக்கிரக துதி", "ஆஞ்சநேயர் துதி",
    "பாரதியார்", "பழமொழி நானூறு", "தத்துவப் பாடல்"
]
prefix_pat = r"^(" + "|".join(re.escape(p) for p in PREFIXES_TAMIL) + r")\s*[:—–-]\s*"

ENG_PREFIXES = [
    "Thirukkural", "Thiruvasagam", "Thevaram", "Thiruvarutpa", "Kandhar Alangaram",
    "Kandhar Anuboothi", "Kandha Sashti Kavasam", "Kandha Puranam", "Thiruppugazh",
    "Thiruppavai", "Periyapuranam", "Panniru Thirumurai", "Thirumanthiram",
    "Abhirami Andhadhi", "Shiva Devotional", "Murugan Devotional", "Vishnu Devotional",
    "Amman Devotional", "Vinayagar Devotional", "Devotional", "Nama Sankeerthanam",
    "Shiva Namavali", "Shiva Stotram", "Adi Shankara", "National Anthem",
    "Tamil Thai Vazhthu", "Aalaya Naatham", "Ambient Meditation", "Navagraha", "Anjaneyar Devotional",
    "Bharathiyar", "Pazhamozhi Naanooru", "Philosophical Song"
]
eng_prefix_pat = r"^(" + "|".join(re.escape(p) for p in ENG_PREFIXES) + r")\s*[:—–-]\s*"


def strip_all_prefixes(tam_str, eng_str):
    # Iteratively strip any leading prefix pattern
    t = tam_str.strip()
    while True:
        sub = re.sub(prefix_pat, "", t, flags=re.IGNORECASE).strip()
        if sub == t:
            break
        t = sub

    e = eng_str.strip()
    while True:
        sub = re.sub(eng_prefix_pat, "", e, flags=re.IGNORECASE).strip()
        if sub == e:
            break
        e = sub
    return t, e

# Specific canonical mapping
SPECIFIC_EXACT = {
    # Shiva / Thiruvasagam
    "சிவகவசம்": ("சிவ ஸ்தோத்திரம்", "Shiva Stotram", "சிவ கவசம்", "Shiva Kavasam"),
    "சிவபுராணம்": ("திருவாசகம்", "Thiruvasagam", "சிவபுராணம்", "Sivapuranam"),
    "அச்சோ": ("திருவாசகம்", "Thiruvasagam", "அச்சோப் பதிகம்", "Achcho Pathigam"),
    "பூவார் சென்னி": ("திருவாசகம்", "Thiruvasagam", "பூவார் சென்னி மன்னன் (யாத்திரைப் பத்து)", "Poovar Senni Mannan"),
    "யாத்திரைப் பத்து": ("திருவாசகம்", "Thiruvasagam", "பூவார் சென்னி மன்னன் (யாத்திரைப் பத்து)", "Poovar Senni Mannan"),
    "திருப்புலம்பல்": ("திருவாசகம்", "Thiruvasagam", "திருப்புலம்பல்", "Thiruppulambal"),
    "அன்னைப்பத்து": ("திருவாசகம்", "Thiruvasagam", "அன்னைப்பத்து", "Annaippathu"),
    "குழைத்த பத்து": ("திருவாசகம்", "Thiruvasagam", "குழைத்த பத்து", "Kuzhaitha Pathu"),
    "வேண்டுமே இத்தனையும்": ("திருவாசகம்", "Thiruvasagam", "வேண்டுமே இத்தனையும் (திருவெம்பாவை)", "Vendumey Iththanaiyum"),
    "ஆதியும் அந்தமும்": ("திருவாசகம்", "Thiruvasagam", "திருவெம்பாவை (ஆதியும் அந்தமும்)", "Thiruvempavai"),
    "போற்றித் திருஅகவல்": ("திருவாசகம்", "Thiruvasagam", "போற்றித் திருஅகவல்", "Potrith Thiruagaval"),
    "போற்றி திரு அகவல்": ("திருவாசகம்", "Thiruvasagam", "போற்றித் திருஅகவல்", "Potrith Thiruagaval"),
    "தென்னாடுடைய சிவனே": ("திருவாசகம்", "Thiruvasagam", "தென்னாடுடைய சிவனே போற்றி", "Thennadudaiya Sivaney Potri"),
    "தென் நாடுடைய சிவனே": ("திருவாசகம்", "Thiruvasagam", "தென்னாடுடைய சிவனே போற்றி", "Thennadudaiya Sivaney Potri"),
    "கள்ளப் பிழையும்": ("திருவாசகம்", "Thiruvasagam", "கள்ளப் பிழையும் (போற்றித் திருஅகவல்)", "Kalla Pizhaiyum"),
    "ஆனந்த மாலை": ("திருவாசகம்", "Thiruvasagam", "ஆனந்த மாலை", "Anandha Maalai"),
    "பிரார்த்தனைப் பத்து": ("திருவாசகம்", "Thiruvasagam", "பிரார்த்தனைப் பத்து", "Prarthanai Pathu"),
    "குறி கலந்த இசை": ("திருவாசகம்", "Thiruvasagam", "குறி கலந்த இசை", "Kuri Kalandha Isai"),
    "திருவார்த்தை": ("திருவாசகம்", "Thiruvasagam", "திருவார்த்தை", "Thiruvaarthai"),
    "திரு உந்தியார்": ("திருவாசகம்", "Thiruvasagam", "திரு உந்தியார்", "Thiru Unthiyar"),
    "திருஏசறவு": ("திருவாசகம்", "Thiruvasagam", "திருஏசறவு", "Thiruesaravu"),
    "திருப்படை ஆட்சி": ("திருவாசகம்", "Thiruvasagam", "திருப்படை ஆட்சி", "Thiruppadai Aatchi"),
    "சென்னிப்பத்து": ("திருவாசகம்", "Thiruvasagam", "சென்னிப்பத்து", "Sennippathu"),
    "நடராஜர் பத்து": ("திருவாசகம்", "Thiruvasagam", "நடராஜர் பத்து", "Natarajar Pathu"),
    "எண்ணப் பதிகம்": ("திருவாசகம்", "Thiruvasagam", "எண்ணப் பதிகம்", "Ennap Pathigam"),
    "திருவெண்பா": ("திருவாசகம்", "Thiruvasagam", "திருவெண்பா", "Thiruvenba"),
    "நமச்சிவாய வாழ்க": ("திருவாசகம்", "Thiruvasagam", "சிவபுராணம் (நமச்சிவாய வாழ்க)", "Namasivaya Vaazhga"),

    # Shiva / Thevaram
    "மாசில் வீணையும்": ("தேவாரம்", "Thevaram", "மாசில் வீணையும்", "Maasil Veenaiyum"),
    "திருநீற்று": ("தேவாரம்", "Thevaram", "திருநீற்றுப் பதிகம் (மந்திரமாவது நீறு)", "Thiruneetru Pathigam"),
    "மந்திரமாவது நீறு": ("தேவாரம்", "Thevaram", "திருநீற்றுப் பதிகம் (மந்திரமாவது நீறு)", "Thiruneetru Pathigam"),
    "துஞ்சலும் துஞ்சல்": ("தேவாரம்", "Thevaram", "நமச்சிவாயப் பதிகம் (துஞ்சலும் துஞ்சல்)", "Tunjalum Tunjal"),
    "திருவோத்தூர்": ("தேவாரம்", "Thevaram", "திருவோத்தூர் பதிகம் (பூத்தேர்ந்து ஆயன)", "Thiruvothur Pathigam"),
    "பூத்தேர்ந்து": ("தேவாரம்", "Thevaram", "திருவோத்தூர் பதிகம் (பூத்தேர்ந்து ஆயன)", "Thiruvothur Pathigam"),
    "அன்னம் பாலிக்கும்": ("தேவாரம்", "Thevaram", "தில்லைத் திருப்பதிகம் (அன்னம் பாலிக்கும்)", "Annam Paalikkum Thillai"),
    "பண்டாய நான்மறை": ("தேவாரம்", "Thevaram", "பண்டாய நான்மறை", "Pandaaya Naanmarai"),
    "அவிநாசி": ("தேவாரம்", "Thevaram", "அவிநாசிப் பதிகம்", "Avinasi Pathigam"),
    "கடவுளைக் கடலுள்": ("தேவாரம்", "Thevaram", "கடவுளைக் கடலுள் எழு (திருக்குறுந்தொகை)", "Kadavulai Kadalul Ezhu"),
    "கரைந்து கைதொழுவாரையும்": ("தேவாரம்", "Thevaram", "கரைந்து கைதொழுவாரையும்", "Karainthu Kaithozhuvar"),
    "கோளறு பதிகம்": ("தேவாரம்", "Thevaram", "கோளறு திருப்பதிகம்", "Kolaru Pathigam"),
    "கோளறு திருப்பதிகம்": ("தேவாரம்", "Thevaram", "கோளறு திருப்பதிகம்", "Kolaru Pathigam"),
    "பிடியதன் உருவுமை": ("தேவாரம்", "Thevaram", "பிடியதன் உருவுமை (விநாயகர் துதி)", "Pidiyathan Uruvumai"),
    "திருமுல்லைவாயில்": ("தேவாரம்", "Thevaram", "திருமுல்லைவாயில் பதிகம்", "Thirumullaivayil Pathigam"),

    # Periyapuranam / Thirumurai
    "தில்லை வாழ் அந்தணர்": ("பெரியபுராணம்", "Periyapuranam", "தில்லை வாழ் அந்தணர் சருக்கம்", "Thillai Vazh Anthanar"),
    "உலகெலாம் உணர்ந்து": ("பெரியபுராணம்", "Periyapuranam", "உலகெலாம் உணர்ந்து ஓதற்கு அரியவன்", "Ulagelam Unarnthu"),
    "திருமந்திரம்": ("திருமந்திரம்", "Thirumanthiram", "முதலாம் தந்திரம்", "Mudhal Thanthiram"),
    "திருப்பல்லாண்டு": ("பன்னிரு திருமுறை", "Panniru Thirumurai", "திருப்பல்லாண்டு (சேந்தனார்)", "Thiru Pallaandu"),
    "திருவையாறு": ("பன்னிரு திருமுறை", "Panniru Thirumurai", "திருவையாறு சாரம்", "Thiruvaiyaaru Saaram"),

    # Thiruvarutpa / Vallalar
    "அன்பு மாலை": ("திருவருட்பா", "Thiruvarutpa", "அன்பு மாலை", "Anbu Maalai"),
    "அருளியல் வினாவல்": ("திருவருட்பா", "Thiruvarutpa", "அருளியல் வினாவல்", "Aruliyal Vinaaval"),
    "நற்றுணை விளக்கம்": ("திருவருட்பா", "Thiruvarutpa", "நற்றுணை விளக்கம்", "Nattrunai Vilakkam"),
    "அபராதத்து ஆற்றாமை": ("திருவருட்பா", "Thiruvarutpa", "அபராதத்து ஆற்றாமை", "Abaraathathu Aatraamai"),
    "அபராத விண்ணப்பம்": ("திருவருட்பா", "Thiruvarutpa", "அபராத விண்ணப்பம்", "Aparadha Vinnappam"),
    "ஆடலமுதப் பத்து": ("திருவருட்பா", "Thiruvarutpa", "ஆடலமுதப் பத்து", "Aadalamudha Pathu"),
    "புண்ணிய விளக்கம்": ("திருவருட்பா", "Thiruvarutpa", "புண்ணிய விளக்கம்", "Punniya Vilakkam"),
    "திருவடிப் புகழ்ச்சி": ("திருவருட்பா", "Thiruvarutpa", "திருவடிப் புகழ்ச்சி", "Thiruvadi Pugazhchi"),
    "சிவ பதி விளக்கம்": ("திருவருட்பா", "Thiruvarutpa", "சிவ பதி விளக்கம்", "Siva Pathi Vilakkam"),
    "திருவருள் வேட்கை": ("திருவருட்பா", "Thiruvarutpa", "திருவருள் வேட்கை", "Thiruvarul Vetkai"),
    "திருவடிச் சரண்புகல்": ("திருவருட்பா", "Thiruvarutpa", "திருவடிச் சரண்புகல்", "Thiruvadi Saranpugal"),
    "தோடுடையார்": ("திருவருட்பா", "Thiruvarutpa", "தோடுடையார்", "Thodudaiyaar"),
    "திருச்சாதனத்": ("திருவருட்பா", "Thiruvarutpa", "திருச்சாதனத் தெய்வத் திறம்", "Thiruchathanath Thiram"),
    "அருட்பெருஞ்சோதி": ("திருவருட்பா", "Thiruvarutpa", "அருட்பெருஞ்சோதி அகவல்", "Arutperunjothi Agaval"),
    "கொடைமடப் புகழ்ச்சி": ("திருவருட்பா", "Thiruvarutpa", "கொடைமடப் புகழ்ச்சி", "Kodaimada Pugazhchi"),
    "சிவ சுப்ரமணியர்": ("திருவருட்பா", "Thiruvarutpa", "சிவ சுப்ரமணியர் திருவிருத்தம்", "Siva Subramaniyar"),
    "சுப்ரமண்யர் திருவிருத்தம்": ("திருவருட்பா", "Thiruvarutpa", "சிவ சுப்ரமணியர் திருவிருத்தம்", "Siva Subramaniyar"),
    "வாழ்வது தமிழ்": ("திருவருட்பா", "Thiruvarutpa", "வாழ்வது தமிழ் ஆகட்டும்", "Vaazvathu Thamiz"),
    "எழுத்தறியும் பெருமான்": ("திருவருட்பா", "Thiruvarutpa", "எழுத்தறியும் பெருமான் மாலை", "Ezhuthariyum Peruman"),
    "சிவபுண்ணியத் தேற்றம்": ("திருவருட்பா", "Thiruvarutpa", "சிவபுண்ணியத் தேற்றம்", "Sivapunniya Thetram"),
    "காட்சிப் பெருமிதம்": ("திருவருட்பா", "Thiruvarutpa", "காட்சிப் பெருமிதம்", "Kaatchi Perumitham"),
    "திருவருள் வழக்க விளக்கம்": ("திருவருட்பா", "Thiruvarutpa", "திருவருள் வழக்க விளக்கம்", "Thiruvarul Vazhakka Vilakkam"),
    "இங்கித மாலை": ("திருவருட்பா", "Thiruvarutpa", "இங்கித மாலை", "Ingitha Maalai"),
    "கோயிலாகநல்": ("திருவருட்பா", "Thiruvarutpa", "கோயிலாகநல் (பழமொழிமேல்)", "Koiyilakanal"),
    "உள்ளம் ஒரு கோவில்": ("திருவருட்பா", "Thiruvarutpa", "உள்ளம் ஒரு கோவில்", "Ullam Oru Kovil"),
    "தாமரை மலரே": ("திருவருட்பா", "Thiruvarutpa", "தாமரை மலரே", "Thamarai Malare"),
    "அறிவரும் பெருமை": ("திருவருட்பா", "Thiruvarutpa", "அறிவரும் பெருமை", "Arivarum Perumai"),
    "அன்பே சரணம் அருளே சரணம்": ("திருவருட்பா", "Thiruvarutpa", "அன்பே சரணம் அருளே சரணம்", "Anbe Saranam Arule Saranam"),
    "விழியிலே மலர்ந்தது": ("திருவருட்பா", "Thiruvarutpa", "விழியிலே மலர்ந்தது", "Vizhiyile Malarnthathu"),
    "நெஞ்சறிவுறுத்தல்": ("திருவருட்பா", "Thiruvarutpa", "நெஞ்சறிவுறுத்தல் (ஒன்றாய்ப் பலவாய்)", "Nenjarivuruthal"),
    "திருவருண் முறையீடு": ("திருவருட்பா", "Thiruvarutpa", "திருவருண் முறையீடு", "Thiruvarun Muraiyidu"),
    "சொற்பெரு மெய்ஞ்ஞான": ("திருவருட்பா", "Thiruvarutpa", "சொற்பெரு மெய்ஞ்ஞான", "Sorpperu Meygnana"),
    "பரசிவ வணக்கம்": ("திருவருட்பா", "Thiruvarutpa", "பரசிவ வணக்கம்", "Parasiva Vanakkam"),
    "வடிவுடை மாணிக்கமாலை": ("திருவருட்பா", "Thiruvarutpa", "வடிவுடை மாணிக்கமாலை", "Vadivudai Manikkamalai"),

    # Murugan
    "நாள் என் செய்யும்": ("கந்தர் அலங்காரம்", "Kandhar Alangaram", "நாள் என் செய்யும்", "Naal En Seyyum"),
    "உருவாய் அருவாய்": ("கந்தர் அநுபூதி", "Kandhar Anuboothi", "உருவாய் அருவாய்", "Uruvaai Aruvaai"),
    "கௌமாரம் ஸ்துதி": ("கந்தர் அநுபூதி", "Kandhar Anuboothi", "கௌமாரம் ஸ்துதி", "Koumaram Stuthi"),
    "முருகர் வார வழிபாடு": ("கந்தர் அநுபூதி", "Kandhar Anuboothi", "முருகர் வார வழிபாடு", "Murugar Vaara Vazhipadu"),
    "சஷ்டி கவசம்": ("கந்த சஷ்டி கவசம்", "Kandha Sashti Kavasam", "முழு கவசம்", "Kandha Sashti Kavasam"),
    "வான் முகில்": ("கந்த புராணம்", "Kandha Puranam", "வான் முகில் வழாது பெய்க", "Vaan Mugil Vazhadhu Peyga"),
    "திகட சக்கர": ("கந்த புராணம்", "Kandha Puranam", "திகட சக்கர சண்முகத்தோன் (காப்பு)", "Thigada Sakkara"),
    "ஆறுமுகம் ஆறுமுகம்": ("திருப்புகழ்", "Thiruppugazh", "ஆறுமுகம் ஆறுமுகம்", "Arumugam Arumugam"),
    "கைத்தல நிறைகனி": ("திருப்புகழ்", "Thiruppugazh", "கைத்தல நிறைகனி", "Kaithala Niraigani"),
    "நாத விந்துகள்": ("திருப்புகழ்", "Thiruppugazh", "நாத விந்துகள் (பழனி)", "Naatha Vindhugal"),
    "திருப்புகழ் 566": ("திருப்புகழ்", "Thiruppugazh", "திருப்புகழ் 566 (இரத்னகிரி)", "Rathinagiri Thiruppugazh"),
    "திருப்புகழ் 712": ("திருப்புகழ்", "Thiruppugazh", "திருப்புகழ் 712 (திருப்போரூர்)", "Thirupporur Thiruppugazh"),
    "திருப்புகழ் விலாசம்": ("திருப்புகழ்", "Thiruppugazh", "திருப்புகழ் விலாசம்", "Thiruppugazh Vilasam"),

    # Vaishnava
    "மார்கழித் திங்கள்": ("திருப்பாவை", "Thiruppavai", "பாசுரம் 1 - மார்கழித் திங்கள்", "Margazhi Thingal"),
    "வையத்து வாழ்வீர்": ("திருப்பாவை", "Thiruppavai", "பாசுரம் 2 - வையத்து வாழ்வீர்", "Vaiyathu Vazhveer"),
    "ஓங்கி உலகளந்த": ("திருப்பாவை", "Thiruppavai", "பாசுரம் 3 - ஓங்கி உலகளந்த", "Ongi Ulagalantha"),
    "கண்ணன் தாலாட்டு": ("பெரியாழ்வார் திருமொழி", "Periyazhvar Thirumozhi", "கண்ணன் தாலாட்டு", "Kannan Thalattu"),
    "நமோ நாராயணம்": ("விஷ்ணு துதி", "Vishnu Devotional", "நமோ நாராயணம் (தசாவதாரம்)", "Namo Narayanam"),
    "ரகுபதி ராகவ": ("ராம பஜனை", "Rama Bhajan", "ரகுபதி ராகவ ராஜா ராம்", "Raghupati Raghava"),
    "ஹரே கிருஷ்ணா": ("மகா மந்திரம்", "Maha Mantra", "ஹரே கிருஷ்ணா ஹரே ராமா", "Hare Krishna Hare Rama"),
    "இராம கிருஷ்ண துதி": ("பஜனை", "Bhajan", "இராம கிருஷ்ண துதி", "Rama Krishna Thuthi"),
    "இராம ராம ராம": ("நாம சங்கீர்த்தனம்", "Nama Sankeerthanam", "இராம ராம ராம ஹரே", "Rama Rama Hare"),
    "கிருஷ்ண மந்திரம்": ("கிருஷ்ண துதி", "Krishna Devotional", "கிருஷ்ண மந்திரம்", "Krishna Mantra"),
    "நமச்சிவாய ஸங்கீர்த்தனம்": ("நாம சங்கீர்த்தனம்", "Nama Sankeerthanam", "நமச்சிவாய சங்கீர்த்தனம்", "Namasivaya Sankeerthanam"),
    "ஆதி யோகீஸ்வரர்": ("சிவ நாமாவளி", "Shiva Namavali", "ஆதி யோகீஸ்வரர் சரணம்", "Aadhi Yogeeswarar"),
    "ஈஸ்வர நாமவளி": ("சிவ நாமாவளி", "Shiva Namavali", "ஈஸ்வர நாமவளி சரணம்", "Eswara Namavali"),
    "ஸ்மரணாத": ("சிவ ஸ்தோத்திரம்", "Shiva Stotram", "ஸ்மரணாதருணாசலம்", "Smaranad Arunachalam"),
    "வேதஸார": ("ஆதிசங்கரர்", "Adi Shankara", "வேதஸார சிவ ஸ்தோத்ரம்", "Vedasaara Shiva Stotram"),
    "வேதசார்": ("ஆதிசங்கரர்", "Adi Shankara", "வேதஸார சிவ ஸ்தோத்ரம்", "Vedasaara Shiva Stotram"),
    "சிவநேச வெண்பா": ("சிவ பக்திப் பாடல்", "Shiva Devotional", "சிவநேச வெண்பா", "Sivanesa Venba"),
    "தியாக வண்ணப் பதிகம்": ("சிவ பக்திப் பாடல்", "Shiva Devotional", "தியாக வண்ணப் பதிகம்", "Thiyaga Vanna Pathigam"),
    "திருவசிய மந்திரம்": ("சிவ பக்திப் பாடல்", "Shiva Devotional", "திருவசிய மந்திரம்", "Thiruvasiyam Mantra"),

    # Other Specifics
    "தனந்தரும் கல்விதரும்": ("அபிராமி அந்தாதி", "Abhirami Andhadhi", "தனந்தரும் கல்விதரும்", "Dhanam Tharum Kalvi Tharum"),
    "சரஸ்வதி போற்றி": ("சரஸ்வதி போற்றி", "Saraswathi Stotram", "108 சரஸ்வதி போற்றி", "108 Saraswathi Potri"),
    "மகாமாயி": ("அம்மன் துதி", "Amman Devotional", "மகாமாயி சமயபுரத்தாயே", "Magamayi Samayapurathaye"),
    "கணேச பஞ்சரத்னம்": ("ஆதிசங்கரர்", "Adi Shankara", "மகா கணேச பஞ்சரத்னம்", "Maha Ganesha Pancharatnam"),
    "பாலும் தெளிதேனும்": ("விநாயகர் நான்மணிமாலை", "Vinayagar Nanmanimalai", "பாலும் தெளிதேனும்", "Paalum Thelithenum"),
    "கண நாதா ஓம்": ("விநாயகர் துதி", "Vinayagar Devotional", "கண நாதா ஓம்", "Gana Natha Om"),
    "தமிழ்த்தாய் வாழ்த்து": ("தமிழ்த்தாய் வாழ்த்து", "Tamil Thai Vazhthu", "நீராரும் கடலுடுத்த", "Neeraarum Kadaludutha"),
    "நீராரும் கடலுடுத்த": ("தமிழ்த்தாய் வாழ்த்து", "Tamil Thai Vazhthu", "நீராரும் கடலுடுத்த", "Neeraarum Kadaludutha"),
    "தேசிய கீதம்": ("தேசிய கீதம்", "National Anthem", "ஜன கண மன", "Jana Gana Mana"),
    "இந்திய தேசிய கீதம்": ("தேசிய கீதம்", "National Anthem", "ஜன கண மன", "Jana Gana Mana"),
    "சனி பகவான்": ("நவக்கிரக துதி", "Navagraha Stotram", "ஸ்ரீ சனி பகவான் துதி", "Sani Bhagavan Thuthi"),
    "ஆஞ்சநேயர் துதி": ("ஆஞ்சநேயர் துதி", "Anjaneyar Devotional", "ஆஞ்சநேயர் துதி", "Anjaneyar Thuthi"),
    "ஆலய நாதம்": ("ஆலய நாதம்", "Aalaya Naatham", "இந்திய ஹார்மோனிக்கா தியானம்", "Harmonica Meditation"),
    "interstellar": ("இசைத் தியானம்", "Ambient Meditation", "இன்டர்ஸ்டெல்லார் (Interstellar)", "Interstellar Meditation"),
    "தாயின் மணிக்கொடி": ("பாரதியார்", "Bharathiyar", "தாயின் மணிக்கொடி பாரீர்", "Thayin Manikkodi Paareer"),
    "பாரதியார்": ("பாரதியார்", "Bharathiyar", "தாயின் மணிக்கொடி பாரீர்", "Thayin Manikkodi Paareer"),
    "பழமொழி நானூறு": ("பழமொழி நானூறு", "Pazhamozhi Naanooru", "கோயிலாகநல்", "Koiyilakanal"),
    "சம்சாரம் என்பது வீணை": ("தத்துவப் பாடல்", "Philosophical Song", "சம்சாரம் என்பது வீணை", "Samsaram Enbathu Veenai")
}


def resolve_scripture_and_names(vid, title, cat_entry):
    raw_title = live_meta.get(vid, {}).get("title", title)
    cat_name, it_meta = cat_entry if cat_entry else (None, {})
    src = it_meta.get("source", "")
    auth = it_meta.get("author", "")
    genre = it_meta.get("genre", "") or cat_name or ""
    
    # Combined text for classification
    combo = f"{title} {raw_title} {src} {auth} {genre}".lower()

    # 1. Thirukkural check
    if "அதிகாரம்" in combo or "thirukkural" in combo or "திருக்குறள்" in combo:
        m = re.search(r"அதிகாரம்\s+(\d+)\s*-\s*([^|\[\(]+)", title)
        if not m:
            m = re.search(r"அதிகாரம்\s+(\d+)\s*-\s*([^|\[\(]+)", raw_title)
        if m:
            num = m.group(1).strip()
            name = m.group(2).strip()
            var = ""
            for v_tag, v_val in [
                ("பகுதி 1", " (பகுதி 1)"), ("Part 1", " (பகுதி 1)"), (" I ", " I"),
                ("பகுதி 2", " (பகுதி 2)"), ("Part 2", " (பகுதி 2)"), (" II ", " II"),
                ("Remix", " (Remix)"), ("Female", " (Female)"), ("Sad", " (Sad)"),
                ("Symphony", " (Symphony)"), ("Pop", " (Pop)"), ("Original", " (Original)")
            ]:
                if v_tag.lower() in title.lower() or v_tag.lower() in raw_title.lower():
                    var = v_val
                    break
            parts = title.split("|")
            eng_raw = parts[1].strip() if len(parts) > 1 else parts[0].strip()
            eng_clean = re.sub(r"(?i)\b(Thirukkural|Cinematic|Film|Song|Remix|Full|Audio)\b", "", eng_raw)
            eng_clean = re.sub(r"\[.*?\]", "", eng_clean).strip(" -|:")
            if not eng_clean or re.search(r"[\u0b80-\u0bff]", eng_clean):
                eng_clean = name
            return "திருக்குறள்", "Thirukkural", f"அதிகாரம் {num} - {name}{var}", eng_clean

    # 2. Check exact known map
    for k, (tam_s, eng_s, tam_n, eng_n) in SPECIFIC_EXACT.items():
        if k.lower() in combo:
            var = ""
            for v_tag, v_val in [
                (" II", " II"), ("(II)", " II"), (" 2", " II"),
                (" III", " III"), ("(III)", " III"),
                (" I", " I"), ("(I)", " I"),
                ("Remix", " (Remix)"), ("Symphony", " (Symphony)")
            ]:
                if v_tag.lower() in title.lower() or v_tag.lower() in raw_title.lower():
                    var = v_val
                    break
            final_tam_n = f"{tam_n}{var}" if var not in tam_n else tam_n
            final_eng_n = f"{eng_n}{var}" if var not in eng_n else eng_n
            return tam_s, eng_s, final_tam_n, final_eng_n

    # 3. Corpus-level fallback matching
    # Thiruvarutpa
    if "திருவருட்பா" in combo or "thiruvarutpa" in combo or "வள்ளலார்" in combo or "vallalar" in combo:
        tam_s, eng_s = "திருவருட்பா", "Thiruvarutpa"
    # Thiruvasagam
    elif "திருவாசகம்" in combo or "thiruvasagam" in combo or "மாணிக்கவாசகர்" in combo:
        tam_s, eng_s = "திருவாசகம்", "Thiruvasagam"
    # Thevaram
    elif "தேவாரம்" in combo or "thevaram" in combo or "அப்பர்" in combo or "சம்பந்தர்" in combo or "சுந்தரர்" in combo:
        tam_s, eng_s = "தேவாரம்", "Thevaram"
    # Thiruppugazh
    elif "திருப்புகழ்" in combo or "thiruppugazh" in combo or "அருணகிரி" in combo:
        tam_s, eng_s = "திருப்புகழ்", "Thiruppugazh"
    # Kandhar Alangaram
    elif "அலங்காரம்" in combo or "alangaram" in combo:
        tam_s, eng_s = "கந்தர் அலங்காரம்", "Kandhar Alangaram"
    # Kandhar Anuboothi
    elif "அநுபூதி" in combo or "அனுபூதி" in combo or "anuboothi" in combo:
        tam_s, eng_s = "கந்தர் அநுபூதி", "Kandhar Anuboothi"
    # Thiruppavai
    elif "திருப்பாவை" in combo or "thiruppavai" in combo or "ஆண்டாள்" in combo:
        tam_s, eng_s = "திருப்பாவை", "Thiruppavai"
    # Periyapuranam
    elif "பெரியபுராணம்" in combo or "periyapuranam" in combo or "சேக்கிழார்" in combo:
        tam_s, eng_s = "பெரியபுராணம்", "Periyapuranam"
    # Thirumanthiram
    elif "திருமந்திரம்" in combo or "thirumanthiram" in combo or "திருமூலர்" in combo:
        tam_s, eng_s = "திருமந்திரம்", "Thirumanthiram"
    # Abhirami Andhadhi
    elif "அபிராமி" in combo or "abhirami" in combo:
        tam_s, eng_s = "அபிராமி அந்தாதி", "Abhirami Andhadhi"
    # Vinayagar Agaval / Devotional
    elif "விநாயக" in combo or "vinayagar" in combo or "பிள்ளையார்" in combo or "ganesha" in combo:
        tam_s, eng_s = "விநாயகர் துதி", "Vinayagar Devotional"
    # Murugan Devotional
    elif "முருக" in combo or "murugan" in combo or "கந்த" in combo:
        tam_s, eng_s = "முருகன் துதி", "Murugan Devotional"
    # Vishnu / Krishna
    elif "விஷ்ணு" in combo or "vishnu" in combo or "கிருஷ்ண" in combo or "krishna" in combo or "நாராயண" in combo:
        tam_s, eng_s = "விஷ்ணு துதி", "Vishnu Devotional"
    # Amman
    elif "அம்மன்" in combo or "amman" in combo or "துர்க்கை" in combo:
        tam_s, eng_s = "அம்மன் துதி", "Amman Devotional"
    # Shiva
    elif "சிவ" in combo or "shiva" in combo or "ஈஸ்வர" in combo or "சிவன்" in combo:
        tam_s, eng_s = "சிவ பக்திப் பாடல்", "Shiva Devotional"
    else:
        tam_s, eng_s = "பக்திப் பாடல்", "Devotional"

    # Extract clean base names
    parts = raw_title.split("|") if "|" in raw_title else title.split("|")
    tam_raw = parts[0].strip()
    eng_raw = parts[1].strip() if len(parts) > 1 else parts[0].strip()

    clean_tam, clean_eng = strip_all_prefixes(tam_raw, eng_raw)
    
    # Remove year tags like "2026"
    clean_tam = re.sub(r"\b2026\b", "", clean_tam).strip()
    clean_eng = re.sub(r"\b2026\b", "", clean_eng).strip()

    # Clean English noise
    clean_eng = re.sub(r"(?i)\b(Cinematic|Film|Song|Devotional|Lord Shiva|Shiva|Thirukkural)\b", "", clean_eng)
    clean_eng = re.sub(r"\[.*?\]", "", clean_eng).strip(" -|:")
    if not clean_eng or re.search(r"[\u0b80-\u0bff]", clean_eng):
        clean_eng = clean_tam

    return tam_s, eng_s, clean_tam, clean_eng

def build_final_title(tam_s, eng_s, tam_n, eng_n, track_type, is_remix=False):
    desc = "Film" if ("Film" in track_type or "Video" in track_type or "film" in track_type) else "Audio"
    if is_remix:
        desc = "Remix"

    # Strip prefixes if any slipped in
    tam_n, eng_n = strip_all_prefixes(tam_n, eng_n)
    tam_n = re.sub(r"\s+", " ", tam_n).strip(" -|:")
    eng_n = re.sub(r"\s+", " ", eng_n).strip(" -|:")

    # Form title candidate 1: Full bilingual
    cand = f"{tam_s}: {tam_n} | {eng_s}: {eng_n} [{desc}]"
    if len(cand) <= 95:
        return cand

    # Candidate 2: Compact english
    cand = f"{tam_s}: {tam_n} | {eng_n} [{desc}]"
    if len(cand) <= 95:
        return cand

    # Candidate 3: Truncate english safely
    max_eng = 95 - len(f"{tam_s}: {tam_n} | ") - len(f" [{desc}]")
    if max_eng > 6:
        cand = f"{tam_s}: {tam_n} | {eng_n[:max_eng].strip()} [{desc}]"
        if len(cand) <= 95:
            return cand

    # Candidate 4: Minimal
    cand = f"{tam_s}: {tam_n} | [{desc}]"
    return cand[:95].strip()

# Run transformation
transformed_master = []
for r in master:
    vid = r["video_id"]
    cat_entry = cat_by_id.get(vid)
    tam_s, eng_s, tam_n, eng_n = resolve_scripture_and_names(vid, r["canonical_title"], cat_entry)
    is_remix = "Remix" in r["canonical_title"] or "remix" in r.get("descriptor", "").lower()
    fin_title = build_final_title(tam_s, eng_s, tam_n, eng_n, r.get("track_type", "Film"), is_remix)
    
    assert len(fin_title) <= 95, f"Title > 95: {fin_title}"
    assert "Devotional Hymn" not in fin_title, f"Generic Devotional Hymn found in {vid}: {fin_title}"
    
    # Check for double colons in Tamil part
    tam_part = fin_title.split("|")[0].strip()
    colons = tam_part.count(":")
    if colons > 1:
        print(f"WARNING: Multiple colons in Tamil part: {fin_title}")

    r_copy = dict(r)
    r_copy["canonical_title"] = fin_title
    r_copy["scripture_source"] = tam_s
    r_copy["length"] = len(fin_title)
    p = fin_title.split("|")
    r_copy["tamil_title"] = p[0].strip()
    r_copy["english_title"] = re.sub(r"\[.*?\]", "", p[1]).strip() if len(p) > 1 else ""
    desc_m = re.search(r"\[(.*?)\]", fin_title)
    r_copy["descriptor"] = desc_m.group(1) if desc_m else ""
    transformed_master.append(r_copy)

# Ensure 1iJSN5jNJMo is included
existing_ids = {r["video_id"] for r in transformed_master}
if "1iJSN5jNJMo" not in existing_ids:
    transformed_master.append({
        "video_id": "1iJSN5jNJMo",
        "canonical_title": "திருக்குறள்: அதிகாரம் 26 - புலால் உண்ணாமை | Thirukkural: Pulaal Unnaamai [Film]",
        "scripture_source": "திருக்குறள்",
        "tamil_title": "திருக்குறள்: அதிகாரம் 26 - புலால் உண்ணாமை",
        "english_title": "Thirukkural: Pulaal Unnaamai",
        "descriptor": "Film",
        "length": 72,
        "genre": "திருக்குறள் (Thirukkural)",
        "track_type": "Cinematic Film / Video",
        "author": "திருவள்ளுவர் (Thiruvalluvar)",
        "source": "திருக்குறள் (அறத்துப்பால் - துறவறவியல்)",
        "playlists": ["Discography", "Thirukkural Full Album"],
        "youtube_url": "https://www.youtube.com/watch?v=1iJSN5jNJMo"
    })

print(f"Standardized {len(transformed_master)} master records.")

# Save master JSON & CSV
with open(MASTER_JSON, "w", encoding="utf-8") as f:
    json.dump(transformed_master, f, ensure_ascii=False, indent=2)

with open(MASTER_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "S.No", "Video ID", "Canonical Title", "Scripture Source", "Tamil Title",
        "English Title", "Descriptor", "Length", "Genre", "Track Type", "Author", "Source"
    ])
    for i, r in enumerate(transformed_master, 1):
        writer.writerow([
            i, r["video_id"], r["canonical_title"], r["scripture_source"],
            r["tamil_title"], r["english_title"], r["descriptor"], r["length"],
            r["genre"], r["track_type"], r["author"], r["source"]
        ])

# Synchronize across folders (site/ and docs/)
for dest_dir in ["site/assets/data", "docs/assets/data"]:
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(MASTER_JSON, os.path.join(dest_dir, "master_all_598_songs_catalog.json"))
    shutil.copy2(MASTER_CSV, os.path.join(dest_dir, "master_all_598_songs_catalog.csv"))

# Verify 100% SHA-256 hash parity
base_hash = hashlib.sha256(open(MASTER_JSON, "rb").read()).hexdigest()
for folder in ["site/assets/data", "docs/assets/data"]:
    h = hashlib.sha256(open(os.path.join(folder, "master_all_598_songs_catalog.json"), "rb").read()).hexdigest()
    assert h == base_hash, f"Hash mismatch in {folder}"
print("100% SHA-256 hash parity verified across all master catalogs!")

# Load channel uploads IDs
channel_vids = []
if os.path.exists("data/dumps/channel_upload_ids.json"):
    with open("data/dumps/channel_upload_ids.json", "r", encoding="utf-8") as f:
        channel_vids = json.load(f)

master_by_id = {r["video_id"]: r for r in transformed_master}

# Order pending direct uploads starting from the most recent upload on the channel
pending_list = []
seen = set()

for vid in channel_vids:
    if vid in master_by_id and vid not in seen:
        r = master_by_id[vid]
        pending_list.append({
            "video_id": r["video_id"],
            "current_title": live_meta.get(r["video_id"], {}).get("title", r["canonical_title"]),
            "new_title": r["canonical_title"],
            "length": r["length"],
            "playlists": r.get("playlists", [])
        })
        seen.add(vid)

# If any video in transformed_master marked as Film/Video not in channel_vids
for r in transformed_master:
    vid = r["video_id"]
    if vid not in seen and ("Film" in r.get("track_type", "") or "Video" in r.get("track_type", "")):
        pending_list.append({
            "video_id": r["video_id"],
            "current_title": live_meta.get(r["video_id"], {}).get("title", r["canonical_title"]),
            "new_title": r["canonical_title"],
            "length": r["length"],
            "playlists": r.get("playlists", [])
        })
        seen.add(vid)

with open(PENDING_JSON, "w", encoding="utf-8") as f:
    json.dump(pending_list, f, ensure_ascii=False, indent=2)

print(f"Saved {len(pending_list)} Direct Channel Uploads in {PENDING_JSON} ordered by recency!")

# Update web catalog.json and catalog.js
updated_cat_count = 0
for cat_key, items in catalog_data.items():
    for it in items:
        vid = it.get("id")
        if vid in master_by_id:
            it["title"] = master_by_id[vid]["canonical_title"]
            updated_cat_count += 1

with open(CATALOG_JSON, "w", encoding="utf-8") as f:
    json.dump(catalog_data, f, ensure_ascii=False, indent=2)

js_content = f"// Complete Curated Web Catalog ({len(transformed_master)} Compositions Across 8 Sacred Genres)\nwindow.GKD_SITE_CATALOG = " + json.dumps(catalog_data, ensure_ascii=False, indent=2) + ";\n"
with open(CATALOG_JS, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Updated {updated_cat_count} items in {CATALOG_JSON} and {CATALOG_JS}!")

# Replicate to site/ and docs/
for target_folder in ["site/assets/data", "docs/assets/data"]:
    shutil.copy2(CATALOG_JSON, os.path.join(target_folder, "catalog.json"))
    shutil.copy2(CATALOG_JS, os.path.join(target_folder, "catalog.js"))

# Verify SHA-256 parity
for filename in ["catalog.json", "catalog.js"]:
    base_hash = hashlib.sha256(open(os.path.join("assets/data", filename), "rb").read()).hexdigest()
    for tf in ["site/assets/data", "docs/assets/data"]:
        h = hashlib.sha256(open(os.path.join(tf, filename), "rb").read()).hexdigest()
        assert h == base_hash, f"Hash mismatch in {tf}/{filename}"

print("100% SHA-256 parity verified across root, site, and docs for all catalogs!")



