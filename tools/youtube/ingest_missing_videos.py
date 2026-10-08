import sys, os, json, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CATALOG_JSON_PATH = os.path.join(ROOT_DIR, 'docs', 'assets', 'data', 'catalog.json')
CATALOG_JS_PATH = os.path.join(ROOT_DIR, 'docs', 'assets', 'data', 'catalog.js')
THIRUKKURAL_HTML_PATH = os.path.join(ROOT_DIR, 'docs', 'thirukkural.html')
MASTER_CATALOG_PATH = os.path.join(ROOT_DIR, 'master_all_598_songs_catalog.json')
LIVE_UPLOADS_PATH = os.path.join(ROOT_DIR, 'data', 'dumps', 'channel_live_uploads.json')
KURALS_ALL_PATH = os.path.join(ROOT_DIR, 'production', 'thirukkural_all.json')

# Load kurals
k_data = json.load(open(KURALS_ALL_PATH, encoding='utf-8'))
kurals = k_data['kural'] if isinstance(k_data, dict) and 'kural' in k_data else k_data
k_by_num = {k['Number']: k for k in kurals}

# Chapter meta definitions for 18 chapters
CHAPTERS_DATA = {
    5: {
        'name_ta': 'இல்வாழ்க்கை',
        'name_en': 'Ilvazhkkai',
        'sub_en': 'Domestic Virtue & Family Dharma',
        'key_kural': 47,
        'meaning': 'இல்லறத்திற்குரிய நல்லியல்புகளோடு வாழ்வாங்கு வாழ்பவன், முக்தி பெற கடுமையாக முயலும் மற்ற துறவிகள் அனைவரிலும் தலைசிறந்தவன் ஆவான்.'
    },
    8: {
        'name_ta': 'அன்புடைமை',
        'name_en': 'Anbudaimai',
        'sub_en': 'The Possession of Love',
        'key_kural': 71,
        'meaning': 'அன்பை அடைத்து வைக்கக்கூடிய கதவு ஏதும் இல்லை; தம்மால் அன்புகாட்டப்படும் அன்பர்களின் துன்பத்தைக் கண்டபோதே கண்ணீராக வெளிப்பட்டு அன்பை வெளிப்படுத்திவிடும்.'
    },
    16: {
        'name_ta': 'பொறையுடைமை',
        'name_en': 'Poraiyudaimai',
        'sub_en': 'The Possession of Patience & Forbearance',
        'key_kural': 151,
        'meaning': 'தன்னைத் தோண்டிப் பிளப்பவர்களையும் தாங்கி நிற்கும் பூமித்தாயைப் போல, தம்மை இகழ்ந்து துன்புறுத்துவோரையும் பொறுத்து மன்னிப்பதே மனிதப் பண்புகளில் தலையாயதாகும்.'
    },
    25: {
        'name_ta': 'அருளுடைமை',
        'name_en': 'Aruludaimai',
        'sub_en': 'The Possession of Compassion & Grace',
        'key_kural': 241,
        'meaning': 'எல்லா உயிர்களிடத்தும் கருணை காட்டும் அருள் என்னும் செல்வமே தலையாய செல்வமாகும்; பொருள் செல்வம் என்பது இழிந்தவர்களிடத்திலும் கூட இருக்கும்.'
    },
    26: {
        'name_ta': 'புலால் உண்ணாமை',
        'name_en': 'Pulaal Unnaamai',
        'sub_en': 'Universal Compassion & Ahimsa',
        'key_kural': 251,
        'meaning': 'தன் உடலை வளர்ப்பதற்காக மற்றொரு உயிரின் உடலை (இறைச்சியை) உண்பவன், எவ்வாறு தன் நெஞ்சில் கருணையையும் ஜீவகாருண்யத்தையும் நிலைநிறுத்த முடியும்?'
    },
    27: {
        'name_ta': 'தவம்',
        'name_en': 'Thavam',
        'sub_en': 'Spiritual Austerity & Meditation',
        'key_kural': 261,
        'meaning': 'தனக்கு வரும் துன்பங்களைப் பொறுத்துக் கொள்வதும், மற்ற எந்த உயிருக்கும் துன்பம் செய்யாதிருப்பதும் ஆகிய இவ்விரண்டுமே தவத்தின் மெய்யான வடிவமாகும்.'
    },
    30: {
        'name_ta': 'வாய்மை',
        'name_en': 'Vaaymai',
        'sub_en': 'Truthfulness & Absolute Integrity',
        'key_kural': 291,
        'meaning': 'உண்மை பேசுதல் என்று போற்றப்படுவது எதுவென்றால், எந்த உயிருக்கும் சிறிதும் தீமை தராத நன்மையான சொற்களைப் பேசுவதேயாகும்.'
    },
    31: {
        'name_ta': 'வெகுளாமை',
        'name_en': 'Vegulaamai',
        'sub_en': 'Conquest of Anger & Equanimity',
        'key_kural': 301,
        'meaning': 'தன் கோபம் பலிக்கும் எளியவரிடம் கோபம் கொள்ளாமல் மனத்தை அடக்குபவனே உண்மையான சினம்காப்பவன்; பலிக்காத வலிமைமிக்கவரிடம் கோபத்தை அடக்கினால் என்ன, அடக்காவிட்டால் என்ன.'
    },
    39: {
        'name_ta': 'இறைமாட்சி',
        'name_en': 'Irai Maatchi',
        'sub_en': 'The Greatness of a Sovereign Ruler',
        'key_kural': 381,
        'meaning': 'வீரமிக்க படை, அறிவுள்ள குடிமக்கள், திரண்ட செல்வம், தேர்ந்த அமைச்சர், நல்ல நட்பு, வலிமையான அரண் ஆகிய ஆறும் உடைய ஆட்சியாளனே அரசர்களுள் சிங்கம் போன்றவனாவான்.'
    },
    40: {
        'name_ta': 'கல்வி',
        'name_en': 'Kalvi',
        'sub_en': 'The Imperishable Wealth of Learning',
        'key_kural': 391,
        'meaning': 'கற்கத் தகுந்த நன்னூல்களைக் குற்றமறக் கற்க வேண்டும்; அவ்வாறு கற்ற பிறகு, கற்ற நன்னெறியின் வழியே தன் வாழ்நாளில் வழுவாது வாழ வேண்டும்.'
    },
    42: {
        'name_ta': 'கேள்வி',
        'name_en': 'Kelvi Selvam',
        'sub_en': 'The Treasure of Deep Listening',
        'key_kural': 411,
        'meaning': 'சான்றோர்களின் அருள்மொழிகளைக் கேட்டுப் பெறும் கேள்விச் செல்வமே எல்லாச் செல்வங்களிலும் மிகச் சிறந்த தலையாய செல்வமாகும்.'
    },
    44: {
        'name_ta': 'குற்றங்கடிதல்',
        'name_en': 'Kuttrangadithal',
        'sub_en': 'Correction of Faults & Self-Vigilance',
        'key_kural': 431,
        'meaning': 'பழிபாவங்களுக்கு அஞ்சும் சான்றோர்கள், தமக்குத் தினை அளவு மிகச் சிறிய குற்றம் நேர்ந்தாலும், அதனைப் பனை மரத்தைப் போலப் பெரிதாகக் கருதி உடனே திருத்திக் கொள்வர்.'
    },
    45: {
        'name_ta': 'பெரியாரைத் துணைக்கோடல்',
        'name_en': 'Periyarai Thunaikodal',
        'sub_en': 'Associating with the Wise & Great',
        'key_kural': 441,
        'meaning': 'கிடைத்தற்கு அரிய பேறுகள் எல்லாவற்றிலும் மிகச் சிறந்த பேறு எதுவென்றால், தம்மிலும் முதிர்ந்த சான்றோர்களைப் போற்றி அவர்களுக்குத் துணையாகவும் நண்பராகவும் ஆக்கிக் கொள்வதேயாகும்.'
    },
    46: {
        'name_ta': 'சிற்றினம் சேராமை',
        'name_en': 'Sitrinam Seraamai',
        'sub_en': 'Avoiding the Company of the Base',
        'key_kural': 451,
        'meaning': 'சேர்ந்த நிலத்தின் தன்மையால் நீரானது தனது குணம் மாறுவது போல, மனிதர்களுக்குத் தாம் சேர்கின்ற சிற்றினத்தின் சகவாசத்தால் மனமும் அறிவும் மாறிவிடும்; எனவே நற்பண்பாளர்களைச் சேர்க.'
    },
    52: {
        'name_ta': 'தெரிந்து வினையாடல்',
        'name_en': 'Therinthu Vinaiyaadal',
        'sub_en': 'Right Delegation & Selection of Capability',
        'key_kural': 511,
        'meaning': 'இச்செயலை முடிக்கவல்லவன் இவன் என்பதை ஆராய்ந்து, செயலையும் ஆராய்ந்து, தக்க காலத்தோடு பொருந்துமாறு உணர்ந்து அவனிடம் அச்செயலை ஒப்படைக்க வேண்டும்.'
    },
    54: {
        'name_ta': 'பொச்சாவாமை',
        'name_en': 'Pochchaavaamai',
        'sub_en': 'Freedom from Negligence & Unfailing Vigilance',
        'key_kural': 531,
        'meaning': 'அளவுகடந்த சினத்தை விடவும், அளவுக்கு மீறிய மகிழ்ச்சியில் மெய்மறந்து விழிப்புணர்வை இழக்கும் கவனக்குறைவே (மறதி) ஒருவனுக்குப் பேராபத்தைத் தரும்.'
    },
    57: {
        'name_ta': 'வெருவந்த செய்யாமை',
        'name_en': 'Veruvandha Seyyaamai',
        'sub_en': 'Absence of Tyranny & Just Governance',
        'key_kural': 561,
        'meaning': 'குற்றத்தை நடுநிலையோடு ஆராய்ந்து, மீண்டும் அக்குற்றம் செய்யாதவாறு தக்க தண்டனை விதித்து நாட்டு மக்களைக் காப்பவனே சிறந்த அரசனாவான்.'
    },
    61: {
        'name_ta': 'மடியின்மை',
        'name_en': 'Madiyinmai',
        'sub_en': 'Overcoming Indolence & Relentless Diligence',
        'key_kural': 601,
        'meaning': 'தன் குலப்பெருமை என்னும் அணையாத ஒளிவிளக்கானது, சோம்பல் என்னும் இருள் அல்லது அழுக்கு வந்து படிந்தால் ஒளியிழந்து அழிந்து போகும்.'
    }
}

# Attach verses to CHAPTERS_DATA
for ch, cdata in CHAPTERS_DATA.items():
    k_item = k_by_num.get(cdata['key_kural'])
    if k_item:
        cdata['lyrics'] = f"{k_item['Line1']}\n{k_item['Line2']}"
    else:
        cdata['lyrics'] = ""

# Load Master and Live data
master = json.load(open(MASTER_CATALOG_PATH, encoding='utf-8'))
m_dict = {m['video_id']: m for m in master}

live = json.load(open(LIVE_UPLOADS_PATH, encoding='utf-8'))
l_dict = {e['id']: e for e in (live if isinstance(live, list) else live.get('entries', []))}

# Missing 45 IDs
missing_45 = [
    '0fD-z3s_g2A', '2Pun6K7h984', '2U45AXlx7DA', '2_TfLljo1qg', '3CICxCn-4A0',
    '5uRYFxhT32k', '9kHN9Dzrv7o', 'B60TIM5LLvY', 'BoOWFaOGczE', 'C05GEfkJZaY',
    'DhHGetUJlAI', 'EChaj0wXk_0', 'F-aVgFOdKFo', 'F6PrK6E9qB0', 'Fh3HfGUObmg',
    'FvpGjzaW2TA', 'GfGlO3RQuik', 'HRN77i6Kio8', 'IEk-wwY3rC8', 'KI7uUFiJO1E',
    'KZxknhbVIk0', 'Mata6vtnrjQ', 'O0hASl4BS2c', 'OzejLLvDq5s', 'PmziMZrMHfE',
    'R-5gWfRNMts', 'R82hz_s2YGQ', 'VVkl8bORJXg', 'WM8EPZ4KK2s', '_Ceq0AzIQ9c',
    'aSQrSHA4YtU', 'aTFvlXMPBSE', 'djYooU1LmGk', 'h2q-ADrbBc4', 'hjcH8zbEleE',
    'jO2i4bcZ2ts', 'lneosghJWgs', 'mCwNR1Bytj4', 'n9lAyAdzo60', 'oEH4ztdn2Nc',
    'r75xdfETSbE', 'v_dsHTOvKP8', 'vbMywONB5Wc', 'wylRNpaJNmY', 'xcUlgFsrepU'
]

def map_video(vid):
    m = m_dict.get(vid)
    l = l_dict.get(vid)
    
    # Identify chapter
    title_raw = (m.get('canonical_title') if m else '') or (l.get('title') if l else '')
    ch_num = None
    ch_m = re.search(r'அதிகாரம்\s*(\d+)', title_raw)
    if ch_m:
        ch_num = int(ch_m.group(1))
    else:
        for ch, meta in CHAPTERS_DATA.items():
            if meta['name_ta'] in title_raw or meta['name_en'].lower() in title_raw.lower():
                ch_num = ch
                break
    
    if not ch_num or ch_num not in CHAPTERS_DATA:
        raise ValueError(f"Could not map chapter for {vid}: {title_raw}")
    
    cdata = CHAPTERS_DATA[ch_num]
    
    # Determine type: "film" or "audio"
    is_film = False
    if m:
        if m.get('descriptor') == 'Film' or 'Film' in m.get('track_type', ''):
            is_film = True
    if l:
        if 'Film' in l.get('title', '') or 'Guru Kula Desam' in l.get('title', ''):
            is_film = True
    if vid in ['F6PrK6E9qB0', 'FvpGjzaW2TA', 'Mata6vtnrjQ', 'n9lAyAdzo60', 'oEH4ztdn2Nc']:
        is_film = True
    
    track_type = "film" if is_film else "audio"
    
    # Determine canonical title
    if m and m.get('canonical_title'):
        title = m['canonical_title']
    elif l and l.get('title'):
        # For the 5 new ones, standardize
        # e.g., 'அதிகாரம் 52 - தெரிந்து வினையாடல் | Therinthu Vinaiyaadal - Right Delegation | Guru Kula Desam'
        title = f"திருக்குறள்: அதிகாரம் {ch_num} - {cdata['name_ta']} | Thirukkural: {cdata['name_en']} [Film]"
    else:
        title = f"திருக்குறள்: அதிகாரம் {ch_num} - {cdata['name_ta']} | Thirukkural: {cdata['name_en']} [{'Film' if is_film else 'Audio'}]"
    
    # Description
    desc = f"திருக்குறள் - அதிகாரம் {ch_num}: {cdata['name_ta']} | {cdata['name_en']}\n\n"
    if is_film:
        desc += f"A full-song cinematic film with moving devotional imagery exploring {cdata['sub_en']}.\n\n"
    else:
        desc += f"Original sacred musical composition exploring {cdata['sub_en']}.\n\n"
    desc += f"Official YouTube: https://www.youtube.com/watch?v={vid}\n\n#Thirukkural #{cdata['name_en']} #GuruKulaDesam"
    
    entry = {
        "id": vid,
        "title": title,
        "type": track_type,
        "playlists": [
            "Discography",
            "திருக்குறள் | Thirukkural — Master Collection"
        ],
        "category": "thirukkural",
        "description": desc,
        "author": "திருவள்ளுவர் (Thiruvalluvar)",
        "source": f"திருக்குறள் — அதிகாரம்: {cdata['name_ta']}",
        "lyrics": cdata['lyrics'],
        "meaning": cdata['meaning']
    }
    return entry

print(f"Loading {CATALOG_JSON_PATH}...")
catalog = json.load(open(CATALOG_JSON_PATH, encoding='utf-8'))

# Check existing items to avoid duplicates
existing_ids = {it['id'] for it in catalog['thirukkural']}
print(f"Pre-ingestion Thirukkural items: {len(catalog['thirukkural'])}, Unique across catalog: {len({it['id'] for items in catalog.values() for it in items})}")

added_count = 0
for vid in missing_45:
    if vid not in existing_ids:
        entry = map_video(vid)
        catalog['thirukkural'].append(entry)
        existing_ids.add(vid)
        added_count += 1

print(f"Added {added_count} new entries to catalog['thirukkural']!")

# Also upgrade any items that had fallback kural lyrics ("அறம்பொருள் இன்பம் வீடடைதல்")
upgraded_fallback_count = 0
for it in catalog['thirukkural']:
    if 'அறம்பொருள் இன்பம் வீடடைதல்' in it.get('lyrics', ''):
        ch_m = re.search(r'அதிகாரம்\s*(\d+)', it.get('title', ''))
        if not ch_m:
            ch_m = re.search(r'அதிகாரம்:\s*([^\n—]+)', it.get('source', ''))
        if ch_m:
            ch_num = None
            try:
                ch_num = int(ch_m.group(1))
            except:
                pass
            if ch_num and ch_num in CHAPTERS_DATA:
                cdata = CHAPTERS_DATA[ch_num]
                it['lyrics'] = cdata['lyrics']
                it['meaning'] = cdata['meaning']
                it['source'] = f"திருக்குறள் — அதிகாரம்: {cdata['name_ta']}"
                upgraded_fallback_count += 1

print(f"Upgraded {upgraded_fallback_count} existing fallback items with authentic chapter verses!")

# Save catalog.json
with open(CATALOG_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)
print(f"Saved updated {CATALOG_JSON_PATH}")

# Save catalog.js
with open(CATALOG_JS_PATH, 'w', encoding='utf-8') as f:
    f.write("// Complete Curated Web Catalog (Sacred Musical Productions & Films)\n")
    f.write("window.GKD_SITE_CATALOG = ")
    json.dump(catalog, f, ensure_ascii=False, indent=2)
    f.write(";\n\n// Dual-binding for main.js search integration\nwindow.GURUKULA_CATALOG = window.GKD_SITE_CATALOG;\n")
print(f"Saved updated {CATALOG_JS_PATH}")

# Now update PAGE_ITEMS in docs/thirukkural.html
with open(THIRUKKURAL_HTML_PATH, 'r', encoding='utf-8') as f:
    html_content = f.read()

m = re.search(r'const PAGE_ITEMS = (\[.*?\]);', html_content)
if m:
    page_items = json.loads(m.group(1))
    page_item_ids = {it['id'] for it in page_items}
    added_to_page = 0
    
    # 5 new live films
    new_5_films = [
        ('n9lAyAdzo60', 26, 'புலால் உண்ணாமை', 'Pulaal Unnaamai'),
        ('FvpGjzaW2TA', 27, 'தவம்', 'Thavam'),
        ('F6PrK6E9qB0', 52, 'தெரிந்து வினையாடல்', 'Therinthu Vinaiyaadal'),
        ('oEH4ztdn2Nc', 54, 'பொச்சாவாமை', 'Pochchaavaamai'),
        ('Mata6vtnrjQ', 61, 'மடியின்மை', 'Madiyinmai')
    ]
    for vid, ch, name_ta, name_en in new_5_films:
        if vid not in page_item_ids:
            page_items.append({
                "id": vid,
                "title": f"அதிகாரம் {ch} - {name_ta} | {name_en} Cinematic Thirukkural Film",
                "type": "film",
                "playlists": [
                    "Discography",
                    "திருக்குறள் | Thirukkural — Master Collection"
                ]
            })
            page_item_ids.add(vid)
            added_to_page += 1
            
    # Also verify if any of the other missing_45 are not in PAGE_ITEMS
    for vid in missing_45:
        if vid not in page_item_ids:
            entry = map_video(vid)
            page_items.append({
                "id": vid,
                "title": entry["title"],
                "type": entry["type"],
                "playlists": entry["playlists"]
            })
            page_item_ids.add(vid)
            added_to_page += 1
            
    print(f"Added {added_to_page} entries to PAGE_ITEMS in thirukkural.html (total now: {len(page_items)})")
    
    # Replace PAGE_ITEMS in html
    new_page_items_str = f"const PAGE_ITEMS = {json.dumps(page_items, ensure_ascii=False)};"
    html_content = html_content[:m.start()] + new_page_items_str + html_content[m.end():]
    with open(THIRUKKURAL_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved updated {THIRUKKURAL_HTML_PATH}")

