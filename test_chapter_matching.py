import json
import re
import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

# Load all data
with open('all_uploads.json', 'r', encoding='utf-8') as f:
    uploads = json.load(f)

with open('all_playlist_items.json', 'r', encoding='utf-8') as f:
    pl_items = json.load(f)

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

# Canonical Tamil names for Thirukkural chapters 1 to 133
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

# Reverse search helper
def find_kural_chapter(title):
    cleaned = title.replace('திருக்குறள்', '').replace('-', ' ').strip()
    # Check for direct chapter number
    m = re.search(r'அதிகாரம்\s+(\d+)', title)
    if m:
        return int(m.group(1))
    
    # Check by keywords
    keyword_map = [
        (1, ["கடவுள் வாழ்த்து", "அகர முதல", "Agara Muthala"]),
        (2, ["வான் சிறப்பு", "Vaan Sirappu"]),
        (5, ["இல்வாழ்க்கை", "Ilvazhkkai"]),
        (6, ["வாழ்க்கைத் துணை", "வாழ்க்கை துணை", "Vaazkkai Thunai"]),
        (8, ["அன்புடைமை", "Anbudaimai"]),
        (16, ["பொறையுடைமை", "Porai"]),
        (25, ["அருளுடைமை", "Aruludaimai"]),
        (26, ["புலால் உண்ணாமை", "புலால்"]),
        (27, ["தவம்"]),
        (28, ["கூடா ஒழுக்கம்"]),
        (29, ["கள்ளாமை"]),
        (30, ["வாய்மை"]),
        (31, ["வெகுளாமை"]),
        (32, ["இன்னா செய்யாமை", "இன்னா செய்தாரை"]),
        (33, ["கொல்லாமை"]),
        (34, ["நிலையாமை"]),
        (35, ["துறவு"]),
        (36, ["மெய்யுணர்தல்"]),
        (37, ["அவாவறுத்தல்", "அவா அறுத்தல்"]),
        (38, ["ஊழ்", "ஊழ் வினை"]),
        (39, ["இறைமாட்சி", "இறை மாட்சி"]),
        (40, ["கல்வி"]),
        (41, ["கல்லாமை"]),
        (42, ["கேள்வி", "கேள்விச் செல்வம்"]),
        (43, ["அறிவுடைமை"]),
        (44, ["குற்றங்கடிதல்"]),
        (45, ["பெரியாரைத் துணைக்கோடல்", "பெரியாரைத்"]),
        (46, ["சிற்றினம் சேராமை", "சிற்றினஞ்சேராமை"]),
        (47, ["தெரிந்து செயல்வகை"]),
        (48, ["வலியறிதல்"]),
        (49, ["காலமறிதல்"]),
        (50, ["இடனறிதல்"]),
        (51, ["தெரிந்து தெளிதல்"]),
        (52, ["தெரிந்து வினையாடல்"]),
        (53, ["சுற்றந்தழால்"]),
        (54, ["பொச்சாவாமை"]),
        (55, ["செங்கோன்மை"]),
        (56, ["கொடுங்கோன்மை"]),
        (57, ["வெருவந்த செய்யாமை"]),
        (58, ["கண்ணோட்டம்"]),
        (59, ["ஒற்றாடல்"]),
        (60, ["ஊக்கமுடைமை"]),
        (61, ["மடியின்மை"]),
        (62, ["ஆள்வினையுடைமை"]),
        (63, ["இடுக்கண் அழியாமை"]),
        (64, ["அமைச்சு"]),
        (65, ["சொல்வன்மை"]),
        (66, ["வினைத்தூய்மை"]),
        (67, ["வினைத்திட்பம்"]),
        (68, ["வினைசெயல்வகை"]),
        (69, ["தூது"]),
        (70, ["மன்னரைச் சேர்ந்தொழுதல்"]),
        (71, ["குறிப்பறிதல்"]),
        (72, ["அவையறிதல்"]),
        (73, ["அவையஞ்சாமை", "அவை அஞ்சாமை"]),
        (74, ["நாடு"]),
        (75, ["அரண்"]),
        (76, ["பொருள் செயல்வகை"]),
        (78, ["படைச்செருக்கு"]),
        (79, ["நட்பு"]),
        (80, ["நட்பாராய்தல்"]),
        (81, ["பழைமை"]),
        (82, ["தீ நட்பு"]),
        (83, ["கூடா நட்பு"]),
        (84, ["பேதைமை"]),
        (125, ["நெஞ்சறிவுறுத்தல்", "Nenjari Vuruthal"]),
    ]
    for ch_num, kw_list in keyword_map:
        for kw in kw_list:
            if kw in title:
                return ch_num
    return None

print("Checking matching logic on 101 Thirukkural items in PLW7qBZp_Q8Ro...")
kural_items = [it for it in pl_items if it.get('playlist_id') == 'PLW7qBZp_Q8Ro']
unmatched = []
matched = []
for it in kural_items:
    t = it.get('title', '')
    vid = it.get('video_id', '')
    if not re.search(r'அதிகாரம்\s+\d+\s*[-–]', t):
        ch = find_kural_chapter(t)
        if ch:
            matched.append((vid, t, ch, CHAPTER_MAP[ch]))
        else:
            unmatched.append((vid, t))

print(f"Matched: {len(matched)} / {len(matched) + len(unmatched)}")
if unmatched:
    print("Unmatched:", unmatched)
else:
    print("SUCCESS: 100% of missing Thirukkural items matched to chapter!")
