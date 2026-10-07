import json
import csv
import re
import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

# 1. Load data
with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live = json.load(f)

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

# 18 Master film unlisted IDs that need canonical prefix
UNLISTED_KURAL_MAP = {
    "6OUebTuktZI": (8, "அன்புடைமை", "Anbudaimai", "Original Audio"),
    "CUMZcTM4y7w": (5, "இல்வாழ்க்கை", "Ilvaazhkkai", "Original Audio"),
    "aZ830iKkqBs": (45, "பெரியாரைத் துணைக்கோடல்", "Periyarai Thunaikodal", "Remix Audio"),
    "c5OwVOaYsW0": (42, "கேள்வி", "Kelvi Selvam", "Remix Audio"),
    "fQspUClJyg8": (30, "வாய்மை", "Vaaymai", "Remix Audio"),
    "rm7aFPyapA0": (25, "அருளுடைமை", "Aruludaimai", "Original Audio"),
    "uadGicFNeqo": (40, "கல்வி", "Kalvi", "Original Audio"),
    "xvkMEdaF7w4": (31, "வெகுளாமை", "Vegulaamai", "Full Song Film"),
    "zzJZkyX1GL4": (44, "குற்றங்கடிதல்", "Kuttrangadithal", "Remix Audio"),
}

# Collect all tracks
all_vids = set()
catalog_by_id = {}
for cat_name, items in catalog.items():
    for it in items:
        vid = it['id']
        all_vids.add(vid)
        catalog_by_id[vid] = (cat_name, it)

for vid in live.keys():
    all_vids.add(vid)

print(f"Total unique tracks to compile: {len(all_vids)}")

master_records = []
genre_counts = defaultdict(int)
track_types = defaultdict(int)

for vid in sorted(all_vids):
    live_data = live.get(vid, {})
    cat_entry = catalog_by_id.get(vid)
    cat_name, cat_data = cat_entry if cat_entry else (None, {})

    # Determine title
    raw_title = live_data.get('title') or cat_data.get('title') or ''
    
    # Check if in unlisted kural map
    if vid in UNLISTED_KURAL_MAP:
        ch, tam_name, eng_name, desc_type = UNLISTED_KURAL_MAP[vid]
        canonical_title = f"அதிகாரம் {ch} - {tam_name} | {eng_name} [{desc_type}]"
    else:
        canonical_title = raw_title.strip()

    # Determine category/genre
    pls = cat_data.get('playlists', [])
    desc = live_data.get('description') or cat_data.get('description') or ''
    
    if 'அதிகாரம்' in canonical_title or 'திருக்குறள்' in canonical_title or 'Thirukkural' in canonical_title or cat_name == 'thirukkural':
        genre = "திருக்குறள் (Thirukkural)"
    elif cat_name == 'shiva' or any('Shiva' in p for p in pls) or 'சிவ' in canonical_title or 'நமச்சிவாய' in canonical_title or 'திருவாசகம்' in canonical_title or 'தேவாரம்' in canonical_title:
        genre = "சிவபெருமான் (Lord Shiva)"
    elif cat_name == 'murugan' or any('Murugar' in p for p in pls) or 'முருக' in canonical_title or 'கந்த' in canonical_title or 'திருப்புகழ்' in canonical_title:
        genre = "முருகப் பெருமான் (Lord Murugar)"
    elif cat_name == 'vishnu_krishna' or any('Vishnu' in p or 'Krishnar' in p for p in pls) or 'விஷ்ணு' in canonical_title or 'கிருஷ்ண' in canonical_title or 'ராம' in canonical_title or 'திருப்பாவை' in canonical_title:
        genre = "விஷ்ணு / கிருஷ்ணர் (Lord Vishnu & Krishna)"
    elif cat_name == 'amman' or any('Amman' in p for p in pls) or 'அம்மன்' in canonical_title or 'அபிராமி' in canonical_title or 'மாரி' in canonical_title:
        genre = "அம்மன் / சக்தி (Goddess Amman)"
    elif cat_name == 'vinayagar' or any('Vinayagar' in p for p in pls) or 'விநாயக' in canonical_title or 'கணேச' in canonical_title or 'கண நாதா' in canonical_title:
        genre = "விநாயகர் (Lord Vinayagar)"
    elif cat_name == 'vallalar_cultural' and ('திருவருட்பா' in canonical_title or 'வள்ளலார்' in canonical_title or 'அருட்பெருஞ்சோதி' in canonical_title):
        genre = "வள்ளலார் / சன்மார்க்கம் (Thiruvarutpa / Sanmargam)"
    else:
        genre = "மரபு & கலாச்சாரம் (Cultural & Heritage)"

    genre_counts[genre] += 1

    # Determine Type: Cinematic Film vs Audio Track
    is_distrokid = "Provided to YouTube by DistroKid" in desc
    c_type = cat_data.get('type')
    if c_type == 'film' or 'Cinematic' in canonical_title or 'Film' in canonical_title:
        track_type = "Cinematic Film / Video"
    elif is_distrokid or 'Audio' in canonical_title or 'Original' in canonical_title:
        track_type = "Audio Track (Master Composition)"
    else:
        track_type = "Devotional Music Video"

    track_types[track_type] += 1

    # Split Tamil vs English title
    parts = canonical_title.split('|')
    tam_title = parts[0].strip()
    eng_part = parts[1].strip() if len(parts) > 1 else ""
    desc_match = re.search(r'\[(.*?)\]', eng_part)
    descriptor = desc_match.group(1) if desc_match else ""
    eng_title = re.sub(r'\[.*?\]', '', eng_part).strip()

    author = cat_data.get('author') or ("திருவள்ளுவர் (Thiruvalluvar)" if "Thirukkural" in genre else "பாரம்பரிய சமய அருளாளர்கள்")
    source = cat_data.get('source') or ("திருக்குறள்" if "Thirukkural" in genre else "குரு குல தேசம் (Guru Kula Desam)")
    dur = live_data.get('duration') or "N/A"
    pub = live_data.get('publishedAt') or "2026"

    master_records.append({
        'video_id': vid,
        'canonical_title': canonical_title,
        'tamil_title': tam_title,
        'english_title': eng_title,
        'descriptor': descriptor,
        'length': len(canonical_title),
        'genre': genre,
        'track_type': track_type,
        'author': author,
        'source': source,
        'playlists': pls,
        'youtube_url': f"https://www.youtube.com/watch?v={vid}",
        'duration': dur,
        'published_at': pub
    })

print(f"\nCompiled {len(master_records)} total records.")
print("\n--- Breakdown by Genre ---")
for g, c in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {g:<45}: {c:3d} tracks")

print("\n--- Breakdown by Track Type ---")
for t, c in track_types.items():
    print(f"  {t:<35}: {c:3d} tracks")

# Check length safety
too_long = [r for r in master_records if r['length'] > 95]
print(f"\nTitles exceeding 95 chars: {len(too_long)}")
missing_pipe = [r for r in master_records if '|' not in r['canonical_title']]
print(f"Titles without '|': {len(missing_pipe)}")

# Save to master JSON
with open('master_all_598_songs_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(master_records, f, ensure_ascii=False, indent=2)

# Save to master CSV
with open('master_all_598_songs_catalog.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'S.No', 'Video ID', 'Canonical Title', 'Tamil Title', 'English Title',
        'Descriptor', 'Length (Chars)', 'Genre', 'Track Type', 'Author',
        'Source', 'Playlists', 'YouTube URL', 'Duration', 'Published Date'
    ])
    for i, r in enumerate(master_records, 1):
        writer.writerow([
            i, r['video_id'], r['canonical_title'], r['tamil_title'], r['english_title'],
            r['descriptor'], r['length'], r['genre'], r['track_type'], r['author'],
            r['source'], ' ; '.join(r['playlists']), r['youtube_url'], r['duration'], r['published_at']
        ])

print("\nSaved master_all_598_songs_catalog.json and master_all_598_songs_catalog.csv successfully!")
