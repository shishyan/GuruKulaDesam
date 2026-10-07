import json
import re
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('all_uploads.json', 'r', encoding='utf-8') as f:
    uploads = json.load(f)

with open('all_playlist_items.json', 'r', encoding='utf-8') as f:
    pl_items = json.load(f)

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

# Build quick lookup of playlists for each video
vid_to_pls = {}
for it in pl_items:
    vid = it.get('video_id')
    pname = it.get('playlist_title')
    if vid not in vid_to_pls:
        vid_to_pls[vid] = set()
    vid_to_pls[vid].add(pname)

# Canonical Thirukkural Chapter Map (1 to 133)
CHAPTER_MAP = {
    1: ("கடவுள் வாழ்த்து", "Kadavul Vazhthu"),
    2: ("வான் சிறப்பு", "Vaan Sirappu"),
    3: ("நீத்தார் பெருமை", "Neethar Perumai"),
    4: ("அறன் வலியுறுத்தல்", "Aran Valiyuruthal"),
    5: ("இல்வாழ்க்கை", "Ilvaazhkkai"),
    6: ("வாழ்க்கைத் துணைநலம்", "Vaazkkai Thunai"),
    7: ("மக்கட்பேறு", "Makkatperu"),
    8: ("அன்புடைமை", "Anbudaimai"),
    9: ("விருந்தோம்பல்", "Virunthombal"),
    10: ("இனியவை கூறல்", "Iniyavai Kooral"),
    11: ("செய்ந்நன்றியறிதல்", "Sei Nandri Arithal"),
    12: ("நடுவுநிலைமை", "Naduvunilaimai"),
    13: ("அடக்கமுடைமை", "Adakkamudaimai"),
    14: ("ஒழுக்கமுடைமை", "Ozhukkamudaimai"),
    15: ("பிறனில் விழையாமை", "Piranil Vizhaiyaamai"),
    16: ("பொறையுடைமை", "Poraiyudaimai"),
    17: ("அழுக்காறாமை", "Azhukkaarாmai"),
    18: ("வெஃகாமை", "Vekkaamai"),
    19: ("புறங்கூறாமை", "Purangkooraamai"),
    20: ("பயனில சொல்லாமை", "Payanila Sollaamai"),
    21: ("தீவினையச்சம்", "Theevinai Acham"),
    22: ("ஒப்புரவறிதல்", "Oppuravarithal"),
    23: ("ஈகை", "Eegai"),
    24: ("புகழ்", "Pugazh"),
    25: ("அருளுடைமை", "Aruludaimai"),
    26: ("புலால் உண்ணாமை", "Pulaal Unnaamai"),
    27: ("தவம்", "Thavam"),
    28: ("கூடா ஒழுக்கம்", "Kooda Ozhukkam"),
    29: ("கள்ளாமை", "Kallaamai"),
    30: ("வாய்மை", "Vaaymai"),
    31: ("வெகுளாமை", "Vegulaamai"),
    32: ("இன்னா செய்யாமை", "Inna Seidharai"),
    33: ("கொல்லாமை", "Kollaamai"),
    34: ("நிலையாமை", "Nilaiyaamai"),
    35: ("துறவு", "Thuravu"),
    36: ("மெய்யுணர்தல்", "Meyyunarithal"),
    37: ("அவாவறுத்தல்", "Avaa Aruththal"),
    38: ("ஊழ்", "Oozh Vinai"),
    39: ("இறைமாட்சி", "Irai Maatchi"),
    40: ("கல்வி", "Kalvi"),
    41: ("கல்லாமை", "Kallaamai"),
    42: ("கேள்வி", "Kelvi Selvam"),
    43: ("அறிவுடைமை", "Arivudaimai"),
    44: ("குற்றங்கடிதல்", "Kuttrangadithal"),
    45: ("பெரியாரைத் துணைக்கோடல்", "Periyarai Thunaikodal"),
    46: ("சிற்றினம் சேராமை", "Sittrinam Seramai"),
    47: ("தெரிந்து செயல்வகை", "Therinthu Seyalvagai"),
    48: ("வலியறிதல்", "Valiyarithal"),
    49: ("காலமறிதல்", "Kaalamarithal"),
    50: ("இடனறிதல்", "Idanarithal"),
    51: ("தெரிந்து தெளிதல்", "Therinthu Thelithal"),
    52: ("தெரிந்து வினையாடல்", "Therinthu Vinaiyaadal"),
    53: ("சுற்றந்தழால்", "Suttranthazhaal"),
    54: ("பொச்சாவாமை", "Pochavaamai"),
    55: ("செங்கோன்மை", "Sengonmai"),
    56: ("கொடுங்கோன்மை", "Kodungonmai"),
    57: ("வெருவந்த செய்யாமை", "Veruvandha Seyyaamai"),
    58: ("கண்ணோட்டம்", "Kannottam"),
    59: ("ஒற்றாடல்", "Ottraadal"),
    60: ("ஊக்கமுடைமை", "Ookkamudaimai"),
    61: ("மடியின்மை", "Madiyinmai"),
    62: ("ஆள்வினையுடைமை", "Aalvinaiyudaimai"),
    63: ("இடுக்கண் அழியாமை", "Idukkan Azhiyaamai"),
    64: ("அமைச்சு", "Amaichu"),
    65: ("சொல்வன்மை", "Solvanmai"),
    66: ("வினைத்தூய்மை", "Vinai Thooymai"),
    67: ("வினைத்திட்பம்", "Vinai Thitpam"),
    68: ("வினைசெயல்வகை", "Vinai Seyalvagai"),
    69: ("தூது", "Thoothu"),
    70: ("மன்னரைச் சேர்ந்தொழுதல்", "Mannarai Sernthozhuthal"),
    71: ("குறிப்பறிதல்", "Kuripparithal"),
    72: ("அவையறிதல்", "Avaiyarithal"),
    73: ("அவையஞ்சாமை", "Avai Anjaamai"),
    74: ("நாடு", "Naadu"),
    75: ("அரண்", "Aran"),
    76: ("பொருள் செயல்வகை", "Porul Seyalvagai"),
    78: ("படைச்செருக்கு", "Padaicherukku"),
    79: ("நட்பு", "Natpu"),
    80: ("நட்பாராய்தல்", "Natpaaraaythal"),
    81: ("பழைமை", "Pazhaimai"),
    82: ("தீ நட்பு", "Thee Natpu"),
    83: ("கூடா நட்பு", "Kooda Natpu"),
    84: ("பேதைமை", "Pethaimai"),
    125: ("நெஞ்சறிவுறுத்தல்", "Nenjari Vuruthal"),
}

EXACT_CANONICAL_OVERRIDES = {
    # Drafts / QC
    "fq0nJxj5aU4": "தனந்தரும் கல்விதரும் | Dhanam Tharum Kalvi Tharum [Cinematic Amman Film]",
    
    # Shiva / Devotional with issues or truncations
    "GJJW8gIHJ0E": "ஆதி யோகீஸ்வரர் நாம ஒளி சரணம் | Aadhi Yogeeswarar [Cinematic Shiva Film]",
    "2QOF2ycA4RQ": "ஆதி யோகீஸ்வரர் நாம ஒளி சரணம் | Aadhi Yogeeswarar [Cinematic Shiva Film]",
    "dpx7C3wuyio": "பூவார் சென்னி மன்னன் (திருவாசகம்) | Poovar Senni Mannan [Cinematic Shiva Film]",
    "IuZ6Qe-aiYI": "அச்சோப் பதிகம் (திருவாசகம்) | Achcho Pathigam [Cinematic Shiva Film]",
    "M4KRTTyoD_A": "அச்சோப் பதிகம் (திருவாசகம்) | Achcho Pathigam [Cinematic Shiva Film]",
    "h39OlLt4N9A": "சிவபுராணம் | Sivapuranam [Devotional Story Film]",
    "Y0tOS_2Azxs": "சிவபுராணம் 2026 (II) | Sivapuranam II [Cinematic Shiva Film]",
    "cKyT1Cv7zEA": "மாசில் வீணையும் | Maasil Veenaiyum [Cinematic Shiva Film]",
    "JzGTK1V3dkM": "திருநீற்றுப் பதிகம் | Thiruneetru Pathigam [Cinematic Shiva Film]",
    "xAgvuRIIl6o": "திருவையாறு திருமுறை (சாரம்) | Thiruvaiyaaru Thirumurai [Cinematic Shiva Film]",
    "xGb7ZXDRvVU": "துஞ்சலும் துஞ்சல் | Tunjalum Tunjal [Cinematic Shiva Film]",
    "_6amHDAc8EI": "வேதஸார சிவ ஸ்தோத்ரம் | Vedasaara Shiva Stotram [Cinematic Shiva Film]",
    "mb-lljpUJ5g": "தென்னாடுடைய சிவனே போற்றி | Thennadudaiya Sivaney Potri [Cinematic Shiva Film]",
    "XwlGJp3gqCc": "தென்னாடுடைய சிவனே போற்றி | Thennadudaiya Sivaney Potri [Cinematic Shiva Film]",
    "BbDNJdLDy-4": "திருப்புலம்பல் 2026 (திருவாசகம்) | Thiruppulambal [Cinematic Shiva Film]",
    "qQqwD3gjenE": "திருப்புலம்பல் 2026 (திருவாசகம்) | Thiruppulambal [Cinematic Shiva Film]",
    "o2cv5Oaii4M": "தென்னாடுடைய சிவனே போற்றி | Thennadudaiya Sivaney Potri [Cinematic Journey]",
    "S9WQ-O0tZJI": "திருப்படை ஆட்சி 2026 (திருவாசகம்) | Thiruppadai Aatchi HipHop [Shiva Film]",
    "o5PVED0ZcfU": "திருவெண்பா 2026 (திருவாசகம்) | Thiruvenba HipHop [Cinematic Shiva Film]",
    "CSqgMX4LhJI": "பிரார்த்தனைப் பத்து 2026 (திருவாசகம்) | Prarthanai Pathu [Shiva Film]",
    "2Gbhx6SwH-M": "திருவோத்தூர் பதிகம் - பூத்தேர்ந்து ஆயன | Thiruvothur Pathigam [Cinematic Shiva Film]",
    "qqpvlkv0mSY": "திருவோத்தூர் பதிகம் - பூத்தேர்ந்து ஆயன II | Thiruvothur Pathigam [Full Song]",
    "YycgNlQl6Go": "திருவோத்தூர் பதிகம் - பூத்தேர்ந்து ஆயன I | Thiruvothur Pathigam [Full Song]",
    "vZyHNMkm8xU": "திருவாசகம் - தென் நாடுடைய சிவனே போற்றி (Female) | Thennadudaiya Sivaney Potri",
    "8BPlAB-ZHHk": "கடவுளைக் கடலுள் எழு | Kadavulai Kadalul Ezhu [Cinematic Shiva Film]",
    "y7TMSgzWf8o": "அன்னம் பாலிக்கும் தில்லை | Annam Paalikkum Thillai [Cinematic Shiva Film]",
    "nutm-A24QcM": "பிடியதன் உருவுமை | Pidiyathan Uruvumai [Cinematic Shiva Film]",
    "bZmif21zNtw": "சிவநேச வெண்பா (திருவருட்பா) | Sivanesa Venba [Cinematic Shiva Film]",
    "CjUD2TU3oAY": "குறி கலந்த இசை | Kuri Kalandha Isai [Cinematic Shiva Film]",
    "gwTtvj-h77g": "திருமந்திரம் (முதல் தந்திரம்) | Thirumanthiram [Cinematic Shiva Film]",
    "qjxmrb4fmjA": "திருவோத்தூர் பதிகம் I | Thiruvothur I [Cinematic Shiva Film]",
    "8b2B047SSTo": "திருவோத்தூர் பதிகம் II | Thiruvothur II [Cinematic Shiva Film]",
    "34D_HpbRxfo": "திருவோத்தூர் பதிகம் III | Thiruvothur III [Cinematic Shiva Film]",
    "pWSY0_0UQwc": "திருவோத்தூர் பதிகம் (சாரம்) | Thiruvothur Saram [Cinematic Shiva Film]",
    "nsWHXJGDYA8": "அன்னைப்பத்து 2026 (திருவாசகம்) | Annaippathu [Cinematic Shiva Film]",
    "RmggfAhGNXU": "திருஏசறவு 2026 (திருவாசகம்) | Thiruesaravu [Cinematic Shiva Film]",
    "rr1zamJEIdg": "பண்டாய நான்மறை | Pandaaya Naanmarai [Cinematic Shiva Film]",

    # Vinayagar
    "AW4cljBWy2w": "பாலும் தெளிதேனும் | Paalum Thelithenum [Cinematic Vinayagar Film]",
    "RVMUEr1MOFo": "பாலும் தெளிதேனும் | Paalum Thelithenum [Cinematic Devotional Film]",
    "T1KiH3G5WPs": "மகா கணேச பஞ்சரத்னம் | Maha Ganesha Pancharatnam [Cinematic Devotional Film]",
    "zqStqzcFgbM": "மகா கணேச பஞ்சரத்னம் | Maha Ganesha Pancharatnam [Cinematic Devotional Film]",
    "Yvlg_8JBHL4": "திகட சக்கர 2026 | Thigada Sakkara [Cinematic Vinayagar Film]",
    "IhE1OvdIBKs": "கைத்தல நிறைகனி (திருப்புகழ்) | Kaiththala Niraigani [Vinayagar Film]",
    "GydxHEmyDPc": "கண நாதா ஓம் (Original) | Gana Natha Om [Cinematic Vinayagar Film]",
    "vFbw9hX0wO4": "கண நாதா ஓம் (Symphony) | Gana Natha Om [Cinematic Vinayagar Film]",

    # Murugan
    "pYh67ltckLQ": "நாள் என் செய்யும் | Naal En Seyyum [Cinematic Murugan Film]",
    "W2peLbC20sA": "சிவ சுப்ரமணியர் திருவிருத்தம் | Siva Subramaniyar Thiruvirutham [Murugan Film]",
    "-unILRjNLHQ": "ஸ்ரீ சுப்ரமண்யர் திருவிருத்தம் | Sree Subramanyar Thiruviruththam [Film]",
    "tCxe5Q1ogPc": "கந்த சஷ்டி கவசம் | Kandha Sashti Kavasam [Cinematic Murugan Film]",
    "8mzfe5h9JoY": "கந்த சஷ்டி கவசம் II | Kandha Sashti Kavasam II [Cinematic Murugan Film]",
    "PVcmqZuROSU": "கந்தர் சஷ்டி துதி 2026 | Kandhar Shashti Thuthi [Cinematic Murugan Film]",
    "On2xoZqBsss": "முத்தைத் தரு (திருப்புகழ்) | Muthai Tharu [Cinematic Thiruppugazh Film]",
    "3oJ2OPG-WCs": "முத்தைத் தரு 2026 (திருப்புகழ்) | Muthai Tharu [Cinematic Thiruppugazh Film]",
    "jpCBad1MjgI": "ஆறுமுகம் ஆறுமுகம் | Arumugam Arumugam [Cinematic Murugan Film]",
    "XqDL5bZgW9c": "உருவாய் அருவாய் (கந்தர் அனுபூதி) | Uruvaai Aruvaai [Murugan Film]",
    "C9Ea0-FfMNs": "நாத விந்துகள் (பழனி திருப்புகழ்) | Naatha Vindhugal [Murugan Film]",
    "YxP_uh3dM18": "திருப்புகழ் 712 - சீர் உலாவிய (திருப்போரூர் I) | Seer Ulaaviya I",
    "iPFEtwdcIxc": "திருப்புகழ் 712 - சீர் உலாவிய (திருப்போரூர் II) | Seer Ulaaviya II",
    "LL77sdbmUNE": "ஸ்ரீ சிவசண்முக நாம ஸங்கீர்த்தனம் 2026 | Siva Shanmuga Sankeerthanam",

    # Amman
    "grjVzzo-RWc": "மகாமாயி சமயபுரத்தாயே | Magamayi Samayapurathaye [Original Story Version]",
    "wehcVz3BMHo": "மகாமாயி சமயபுரத்தாயே | Magamayi Samayapurathaye [Cinematic Devotional Film]",
    "0k9CZLNA2TY": "தனந்தரும் கல்விதரும் | Dhanam Tharum Kalvi Tharum [Cinematic Amman Film]",
    "IT_-ioBG69g": "தனந்தரும் அபிராமி | Dhanam Tharum Abhirami [Cinematic Amman Film]",
    "Q2xax9mIhZw": "தனந்தரும் அபிராமி | Dhanam Tharum Abhirami [Original Devotional Track]",
    "7WnikKPxo-k": "ஆனந்த மாலை | Anandha Maalai [Cinematic Devotional Film]",
    "UUytjlINYLw": "அபிராமி அந்தாதி துதி | Abhirami Andhathi Thuthi [Cinematic Amman Film]",
    "w0lNqTk3QCU": "அபிராமி அந்தாதி துதி | Abhirami Andhathi Thuthi [Cinematic Devotional Film]",
    "94drEh5bkH0": "108 சரஸ்வதி போற்றி | 108 Saraswathi Potri [Cinematic Amman Film]",
    "hp1ctMubVmo": "லக்ஷ்மி 108 போற்றி | Lakshmi 108 Potri [Cinematic Amman Film]",
    "fzoZWnsJReg": "தாயே கருமாரி 2026 | Thaaye Karumari [Cinematic Amman Film]",
    "d4-qZaYo-4g": "காயத்ரி மந்திரம் 2026 | Gayathri Mantra [Cinematic Devotional Film]",
    "K0N0k3mNh_w": "அன்னை ரேணுகாம்பாள் துதி | Annai Renukambal [Cinematic Amman Film]",
    "jZI2pTITtBY": "திருவருட்பா - வடிவுடை மாணிக்கமாலை | Vadivudai Manikkamalai [Amman Film]",

    # Vishnu / Krishna
    "Q5G2h9GuGQs": "ரகுபதி ராகவ ராஜா ராம் | Raghupati Raghava [Cinematic Devotional Film]",
    "_DHXM8tymn8": "ரகுபதி ராகவ ராஜா ராம் | Raghupati Raghava [Cinematic Devotional Film]",
    "qWSwrdJMbSg": "இராம கிருஷ்ண துதி | Rama Krishna Thuthi [Cinematic Devotional Film]",
    "qW6CZgELq1o": "இராம ராம ராம ஹரே ஹரே | Rama Rama Rama Hare Hare [Cinematic Devotional Film]",
    "jfXxy-Y9zuA": "இராம ராம ராம ஹரே ஹரே | Rama Rama Rama Hare Hare [Cinematic Devotional Film]",
    "HPP3IG7DWRc": "ஹரே கிருஷ்ணா ஹரே ராமா | Hare Krishna Hare Rama [Cinematic Devotional Film]",
    "wnbjHShXh10": "ஹரே ராமா ஹரே கிருஷ்ணா | Hare Rama Hare Krishna [Cinematic Devotional Film]",
    "EXl0IUQXfoU": "ஹரே ராமா ஹரே கிருஷ்ணா I | Hare Rama Hare Krishna I [Cinematic Devotional Film]",
    "RDcw0Bol-cE": "திருப்பாவை - 1 (மார்கழித் திங்கள்) | Thiruppavai 1 [Cinematic Devotional Film]",
    "fkgEbW9HdtI": "திருப்பாவை - 1 (மார்கழித் திங்கள்) | Thiruppavai 1 [Cinematic Devotional Film]",
    "Lzkbhp_ehA8": "திருப்பாவை - 2 (வையத்து வாழ்வீர்) | Thiruppavai 2 [Cinematic Devotional Film]",
    "hm7_qUlTUiU": "திருப்பாவை - 2 (வையத்து வாழ்வீர்) | Thiruppavai 2 [Cinematic Devotional Film]",
    "phlMcxN_Cfw": "திருப்பாவை - 2 (வையத்து வாழ்வீர்காள்) | Thiruppavai 2 [Cinematic Devotional Film]",
    "To2l9uyCjMg": "திருப்பாவை - 3 (ஓங்கி உலகளந்த) | Thiruppavai 3 [Cinematic Devotional Film]",
    "468ErjVLRCs": "விஷ்ணும் ஜிஷ்ணும் | Vishnum Jishnum [Cinematic Devotional Film]",
    "4vZEVROZIx8": "நமோ நாராயணம் (தசாவதாரம்) | Namo Narayanam [Cinematic Devotional Film]",
    "s42Po5EpzyI": "நமோ நாராயணம் (தசாவதாரம்) | Namo Narayanam [Image Motion Devotional Film]",
    "dUYaclHH6Tk": "பெரியாழ்வார் திருமொழி தாலாட்டு 2026 (I) | Periyazhvar Lullaby I",
    "GCea1CAcjl8": "பெரியாழ்வார் திருமொழி தாலாட்டு 2026 (II) | Periyazhvar Lullaby II",
    "0W1FqHOYwDc": "பெரியாழ்வார் திருமொழி தாலாட்டு 2026 (III) | Periyazhvar Lullaby III",

    # Vallalar / Cultural / General
    "nGBmGzsD-kM": "திருவருட்பா - கொடைமடப் புகழ்ச்சி | Kodaimada Pugazhchi [Full Song]",
    "I-ZLmvGIiz4": "திருவருட்பா - சிவ பதி விளக்கம் | Siva Pathi Vilakkam [Full Song]",
    "lAWfE9YSJME": "திருவருட்பா - பரசிவ வணக்கம் | Parasiva Vanakkam [Full Song]",
    "kshlDPh2IqE": "திருவருட்பா - அபராதத்து ஆற்றாமை | Abaraathathu Aatraamai [Full Song]",
    "MlaG3Z3_Kck": "திருவருட்பா - காட்சிப் பெருமிதம் | Kaatchi Perumitham [Full Song]",
    "dbdp19C0j3M": "திருவருட்பா - திருவருள் வேட்கை II | Thiruvarul Vetkai II [Full Song]",
    "kyiaup-gjMc": "திருவருட்பா - எழுத்தறியும் பெருமான் மாலை | Ezhuthariyum Peruman Maalai",
    "juuVtFBK3X8": "திருவருட்பா - ஆடலமுதப் பத்து | Aadalamudha Pathu [Full Song]",
    "06ZOKy7SSvw": "திருவருட்பா - திருச்சாதனத் தெய்வத் திறம் | Thiruvasathanath Theiva Thiram",
    "YORF54ouPz0": "திருவருட்பா - சிவபுண்ணியத் தேற்றம் | Sivapunniya Thetram [Full Song]",
    "0TB3drCSvNc": "திருவருட்பா - திருவருள் வேட்கை I | Thiruvarul Vetkai I [Full Song]",
    "Z7qFXMBjnak": "திருவருட்பா - திருவடிச் சரண்புகல் | Thiruvadi Saranpugal [Full Song]",
    "DCJ2qoMSIBA": "திருவருட்பா - தியாக வண்ணப் பதிகம் | Thiyaga Vanna Pathigam [Full Song]",
    "hDoLscfeg5Q": "திருவருட்பா - திருவருள் வழக்க விளக்கம் | Thiruvarul Vazhakka Vilakkam",
    "uMK4LISQFE4": "திருவருட்பா - திருமுல்லைவாயில் II | Thirumullaivayil II [Full Song]",
    "73GrCFM_v6Q": "திருவருட்பா - திருமுல்லைவாயில் I | Thirumullaivayil I [Full Song]",
    "EOkuHFSfv8c": "திருவருட்பா - நமச்சிவாய ஸங்கீர்த்தனம் | Namasivaya Sankeerthanam [Full Song]",
    "XelTS98bLec": "திருவருட்பா - திருப்புகழ் விலாசம் | Thiruppugazh Vilasam [Full Song]",
    "4qnq1zW63hI": "திருவருட்பா - பதி விளக்கம் | Pathi Vilakkam [Full Song]",
    "7TlWCD9pa_0": "திருவருட்பா - முத்தி உபாயம் | Muthi Upayam [Full Song]",
    "PLBuPRdKMHE": "திருவருட்பா - அபராத விண்ணப்பம் III | Aparadha Vinnappam III [Full Song]",
    "-9bZmHzYO2g": "திருவருட்பா - அபராத விண்ணப்பம் II | Aparadha Vinnappam II [Full Song]",
    "4UGFfmEpphI": "திருவருட்பா - அபராத விண்ணப்பம் I | Aparadha Vinnappam I [Full Song]",
    "VyUqD3ZO3BU": "திருவருட்பா - அறிவரும் பெருமை | Arivarum Perumai [Full Song]",
    "cVbT38ujUTQ": "திருவருட்பா - அருள்விடை வேட்கை | Arulvidai Vetkai [Full Song]",
    "8KQc368hCmg": "திருவருட்பா - நெஞ்சொடு நேர்தல் | Nenjodu Nerthal [Full Song]",
    "-bqKXZW8vFk": "திருவருட்பா - அருளியல் வினாவல் | Aruliyal Vinaval [Full Song]",
    "SDPLWITWGho": "திருவருட்பா - நற்றுணை விளக்கம் | Nattrunai Vilakkam [Cinematic Shiva Film]",
    "5gzJXgmt7AY": "திருவருட்பா - திருவருண் முறையீடு | Thiruvarun Muraiyidu [Full Song]",
    "kkDJM6dKTxs": "திருவருட்பா - இங்கித மாலை 2026 | Ingitha Maalai [Cinematic Devotional Film]",
    "V7dOPmD9aWg": "அருட்பெருஞ்சோதி அகவல் 1 | Arutperunjothi Agaval 1 [Cinematic Devotional Film]",
    "9PUF7elNSOU": "அருட்பெருஞ்சோதி 2026 | Arutperunjothi [Cinematic Devotional Film]",
    "00BGSFBWdlA": "அருட்பெருஞ்சோதி 2026 II | Arutperunjothi II [Cinematic Devotional Film]",
    "3youy-33GtY": "அருட்பெருஞ்சோதி 2026 III | Arutperunjothi III [Cinematic Devotional Film]",
    "RtHz7rTLNHk": "அருட்பெருஞ்சோதி 2026 IV | Arutperunjothi IV [Cinematic Devotional Film]",
    "-ZkM45zylxs": "அருட்பெருஞ்சோதி 2026 V | Arutperunjothi V [Cinematic Devotional Film]",
    "gre-26HFBfA": "அருட்பெருஞ்சோதி 2026 VI | Arutperunjothi VI [Cinematic Devotional Film]",
    "UxsU284RHQY": "அருட்பெருஞ்சோதி அகவல் I | Arutperunjothi Agaval I [Cinematic Devotional Film]",
    "1W9SHSo-2Vk": "அருட்பெருஞ்சோதி அகவல் II | Arutperunjothi Agaval II [Cinematic Devotional Film]",
    "ZsxGP1jIZ-s": "அருள் நாம விளக்கம் | Arul Nama Vilakkam [Cinematic Devotional Film]",
    "X-EB6CFVz1E": "அவலத் தழுங்கல் 2026 | Avalath Thazhungal [Cinematic Devotional Film]",
    "Bq6eGijG9T4": "இந்திய தேசிய கீதம் 2026 | Indian National Anthem [Cinematic Film]",
    "QTxWZpg6F98": "உலகமெலாந் தனிநிறைந்த | Ulagamelan Thaniniraindha [Cinematic Devotional Film]",
    "x8x7cnUdTE4": "உள்ளம் ஒரு கோவில் (II) 2026 | Ullam Oru Kovil II [Cinematic Devotional Film]",
    "zuDJOeLjtcQ": "உள்ளம் ஒரு கோவில் 2026 | Ullam Oru Kovil [Cinematic Devotional Film]",
    "-Gd2dy_L98c": "ஏகமாய் அந்தமாய் (மதுவின் மடல்) | Ekamaai Anthamaai [Cinematic Devotional Film]",
    "0gK0asNO-RM": "குரு பகவான் துதி 2026 | Guru Bhagavan Thuthi [Cinematic Devotional Film]",
    "MDK8Oq7p1j8": "கொன்றை வேந்தன் | Konrai Vendhan [Cinematic Devotional Film]",
    "G4Tk8Z1tKRg": "கோயிலாகநல் - பழமொழிமேல் 2026 | Koiyilakanal [Cinematic Devotional Film]",
    "28Xnfhctf0I": "சம்சாரம் என்பது வீணை (REMIX) 2026 | Samsaram Enbathu Veenai [Remix Film]",
    "tAlN-7BPL7k": "சொற்பெரு மெய்ஞ்ஞான | Sorpperu Meygnana [Cinematic Devotional Film]",
    "6p5A87HdAAI": "ஞானத் திருவடி 2026 | Gnanath Thiruvadi [Cinematic Devotional Film]",
    "yMrpyhLlDc8": "தாமரை மலரே | Thamarai Malare [Cinematic Devotional Film]",
    "DYAKkr0e5jU": "திரு சனி பகவான் துதி 2026 | Sani Bhagavan Thuthi [Cinematic Devotional Film]",
    "WMtIb1EHwGw": "திரு சனி பகவான் பதிகம் 2026 | Sani Bhagavan Pathigam [Cinematic Devotional Film]",
    "1wD_X2LHCmw": "திருவசிய மந்திரம் 2026 | Thiruvasiyam Mantra [Cinematic Devotional Film]",
    "r2ulXHQihY0": "நெஞ்சறிவுறுத்தல் - ஒன்றாய்ப் பலவாய் | Nenjari Vuruthal [Devotional Film]",
    "Iky5L-131A4": "விழியிலே மலர்ந்தது (REMIX) 2026 | Vizhiyile Malarnthathu [Remix Film]",
    "KOroiTQUE0g": "வான் முகில் வழாது பெய்க | Vaan Mugil Vazhadhu Peyga [Cinematic Devotional Film]",
    "HU-f-FpjmTQ": "வான் முகில் வழாது பெய்க | Vaan Mugil Vazhadhu Peyga [Cinematic Devotional Film]",
    "ETELjf0OTi4": "தமிழ்த்தாய் வாழ்த்து | Tamil Thai Vazhthu [Cinematic Film]",
    "OnzFNGriZ24": "தமிழ்த்தாய் வாழ்த்து | Tamil Thai Vazhthu [Cinematic Film]",
    "CvDDeKLC4mw": "தாயின் மணிக்கொடி பாரீர் | Thayin Manikkodi Paareer [Cinematic Film]",
    "sTSKhkPNI64": "வாழ்வது தமிழ் ஆகட்டும் | Vaazvathu Thamiz Aagattum [Cinematic Film]",
    "lw2nEZfR7Kc": "அன்பே சரணம் அருளே சரணம் | Anbe Saranam Arule Saranam [Cinematic Film]",
    "Wf1Ehxt_A5s": "ஆலய நாதம் | Aalaya Naatham [Indian Harmonica Meditation]",
    "5gO0xpY_Y3E": "Hans Zimmer - Interstellar | Sacred Ambient Instrumental [Guru Kula Desam]",
    "7NECOtuTZ_Y": "ஆஞ்சநேயர் துதி | Anjaneyar Thuthi [Cinematic Devotional Film]",

    # Long / Truncated Thirukkural titles
    "dthZW-Wo8IU": "அதிகாரம் 70 - மன்னரைச் சேர்ந்தொழுதல் (Female) | Mannarai Sernthozhuthal",
    "HRN77i6Kio8": "அதிகாரம் 45 - பெரியாரைத் துணைக்கோடல் (Remix) | Periyarai Thunaikodal",
    "aSQrSHA4YtU": "அதிகாரம் 16 - பொறையுடைமை | Poraiyudaimai [Full Song Film]",
    "JDqbpISJjIA": "அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் (பகுதி 1) | Nenjari Vuruthal I [Full Song Film]",
    "7wJJCQrYo04": "அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் (பகுதி 2) | Nenjari Vuruthal II [Full Song Film]",
    "Y3xujLwXuBs": "அதிகாரம் 32 - இன்னா செய்யாமை | Inna Seidharai [Cinematic Thirukkural Film]",
}

def standardize_title(vid, current_title):
    t = current_title.strip()
    
    # 1. Check exact canonical override first
    if vid in EXACT_CANONICAL_OVERRIDES:
        return EXACT_CANONICAL_OVERRIDES[vid]

    pls = vid_to_pls.get(vid, set())
    is_kural = any('Thirukkural' in p or 'திருக்குறள்' in p for p in pls) or 'அதிகாரம்' in t or 'Thirukkural' in t
    
    # 2. Clean trailing marks
    t = re.sub(r'!\.m$', '', t)
    t = re.sub(r'\.m$', '', t)
    t = re.sub(r'!+$', '', t).strip()

    # 3. Thirukkural standardization
    if is_kural:
        m = re.match(r'அதிகாரம்\s+(\d+)\s*[-–]\s*(.*?)$', t)
        if m:
            ch_num = int(m.group(1))
            rest = m.group(2)
            if '|' in rest and len(t) <= 95:
                return t
            elif '|' in rest:
                parts = t.split('|')
                tam = parts[0].strip()
                eng = parts[1].strip()
                if len(eng) > 40:
                    eng = eng[:37] + '...'
                new_t = f"{tam} | {eng}"
                return new_t
            else:
                ch_info = CHAPTER_MAP.get(ch_num)
                eng_name = ch_info[1] if ch_info else rest.strip()
                return f"அதிகாரம் {ch_num} - {rest.strip()} | {eng_name} [Full Song Film]"
        else:
            from test_chapter_matching import find_kural_chapter
            ch_num = find_kural_chapter(t)
            if ch_num and ch_num in CHAPTER_MAP:
                tam_name, eng_name = CHAPTER_MAP[ch_num]
                var_match = re.search(r'\((Original|Remix|Female|Symphony|Sad|Rock|Pop|Slow)\)', t, re.IGNORECASE)
                var = f" ({var_match.group(1).title()})" if var_match else ""
                descriptor = "[Full Song Film]"
                if "Remix" in t:
                    descriptor = "[Remix Audio]"
                elif "Symphony" in t:
                    descriptor = "[Symphony]"
                elif "Original" in t:
                    descriptor = "[Original Audio]"
                
                new_t = f"அதிகாரம் {ch_num} - {tam_name}{var} | {eng_name} {descriptor}"
                if len(new_t) > 95:
                    new_t = f"அதிகாரம் {ch_num} - {tam_name}{var} | {eng_name}"
                return new_t

    # 4. Bilingual / Pipe separation
    if '|' not in t:
        bi_m = re.match(r'^(.*?)\s*\((.*?)\)$', t)
        if bi_m:
            p1, p2 = bi_m.group(1).strip(), bi_m.group(2).strip()
            if re.search(r'[\u0B80-\u0BFF]', p2) and not re.search(r'[\u0B80-\u0BFF]', p1):
                return f"{p2} | {p1} [Cinematic Devotional Film]"
            elif re.search(r'[\u0B80-\u0BFF]', p1) and not re.search(r'[\u0B80-\u0BFF]', p2):
                return f"{p1} | {p2} [Cinematic Devotional Film]"

        suffix = "[Cinematic Devotional Film]"
        if any('Shiva' in p for p in pls):
            suffix = "[Cinematic Shiva Film]"
        elif any('Murugar' in p for p in pls):
            suffix = "[Cinematic Murugan Film]"
        elif any('Vinayagar' in p for p in pls):
            suffix = "[Cinematic Vinayagar Film]"
        elif any('Amman' in p for p in pls):
            suffix = "[Cinematic Amman Film]"
        
        # Check if t already has suffix
        new_t = f"{t} | {t} {suffix}"
        if len(new_t) > 95:
            new_t = f"{t} | {suffix[1:-1]}"
        return new_t
    
    # 5. Length safety check
    if len(t) > 95:
        parts = t.split('|')
        tam = parts[0].strip()
        eng = parts[1].strip()
        max_eng = 90 - len(tam)
        if max_eng > 15:
            eng = eng[:max_eng].strip()
            return f"{tam} | {eng}"
        else:
            return tam[:95]

    return t

print("Executing comprehensive title standardization across all 580 tracks...")
all_updates = []
for vid, data in live_meta.items():
    curr_t = data.get('title', '')
    new_t = standardize_title(vid, curr_t)
    changed = (new_t != curr_t)
    all_updates.append({
        'video_id': vid,
        'current_title': curr_t,
        'new_title': new_t,
        'changed': changed,
        'length': len(new_t),
        'playlists': list(vid_to_pls.get(vid, []))
    })

changed_updates = [u for u in all_updates if u['changed']]
print(f"Total tracks audited: {len(all_updates)}")
print(f"Total titles needing update: {len(changed_updates)}")

too_long = [u for u in all_updates if u['length'] > 95]
print(f"Titles exceeding 95 chars: {len(too_long)}")
if too_long:
    for u in too_long:
        print(f"  TOO LONG ({u['length']}): [{u['video_id']}] {u['new_title']}")
else:
    print("SUCCESS: 100% of titles are within 95 characters (strictly <= YouTube limit 100)!")

# Check missing pipe
missing_pipe = [u for u in all_updates if '|' not in u['new_title']]
print(f"Titles without delimiter '|': {len(missing_pipe)}")
if missing_pipe:
    for u in missing_pipe:
        print(f"  NO PIPE: [{u['video_id']}] {u['new_title']}")
else:
    print("SUCCESS: 100% of titles carry canonical bilingual delimiter '|'!")

# Check draft or improper punctuation
improper = [u for u in all_updates if 'QC HOLD' in u['new_title'] or u['new_title'].endswith('!') or u['new_title'].endswith('.m') or '...' in u['new_title']]
print(f"Titles with improper punctuation / drafts / dots: {len(improper)}")
if improper:
    for u in improper:
        print(f"  IMPROPER: [{u['video_id']}] {u['new_title']}")
else:
    print("SUCCESS: 0 improper punctuation, 0 dots, 0 draft markers!")

# Save all updates
with open('all_channel_title_updates.json', 'w', encoding='utf-8') as f:
    json.dump(changed_updates, f, ensure_ascii=False, indent=2)

with open('all_channel_title_updates.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['video_id', 'current_title', 'new_title', 'length', 'playlists'])
    for u in changed_updates:
        writer.writerow([u['video_id'], u['current_title'], u['new_title'], u['length'], '; '.join(u['playlists'])])

print("\nSaved all_channel_title_updates.json and all_channel_title_updates.csv successfully!")
