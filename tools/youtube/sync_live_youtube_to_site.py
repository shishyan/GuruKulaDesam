#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Near-Live YouTube Sync Automation
===================================================
Fetches newly published videos from the official YouTube channel (@guru-kula-desam)
without consuming YouTube Data API quota (utilizing yt-dlp flat playlist extraction
or channel RSS feed fallback).

Automatically:
1. Detects new videos not yet present in docs/assets/data/catalog.json.
2. Enriches each new video with canonical titles, chapter details, authentic Tamil
   verses (couplets) and philosophical meanings from production/thirukkural_all.json.
3. Updates docs/assets/data/catalog.json & docs/assets/data/catalog.js.
4. Updates PAGE_ITEMS in docs/thirukkural.html if Thirukkural videos are detected.
5. Updates master_all_598_songs_catalog.json across repository roots.
6. Executes tools/sync/sync_trifolder.py --source docs to maintain 100% SHA-256 parity.
"""

import os
import sys
import json
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CHANNEL_URL = "https://www.youtube.com/@guru-kula-desam/videos"
CHANNEL_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UC-aZ5tL3uB1h_Z0rW2tC2hQ" # Fallback if channel ID known

CATALOG_JSON_PATH = os.path.join(ROOT_DIR, 'docs', 'assets', 'data', 'catalog.json')
CATALOG_JS_PATH = os.path.join(ROOT_DIR, 'docs', 'assets', 'data', 'catalog.js')
THIRUKKURAL_HTML_PATH = os.path.join(ROOT_DIR, 'docs', 'thirukkural.html')
KURALS_ALL_PATH = os.path.join(ROOT_DIR, 'production', 'thirukkural_all.json')

MASTER_CATALOG_PATHS = [
    os.path.join(ROOT_DIR, 'master_all_598_songs_catalog.json'),
    os.path.join(ROOT_DIR, 'assets', 'data', 'master_all_598_songs_catalog.json'),
    os.path.join(ROOT_DIR, 'docs', 'assets', 'data', 'master_all_598_songs_catalog.json'),
    os.path.join(ROOT_DIR, 'site', 'assets', 'data', 'master_all_598_songs_catalog.json'),
]

# Chapter definitions
CHAPTERS_DATA = {
    1: {'name_ta': 'கடவுள் வாழ்த்து', 'name_en': 'Kadavul Vazhthu', 'key_kural': 1, 'meaning': 'எழுத்துக்கள் எல்லாம் அகரத்தை முதலாகக் கொண்டு தொடங்குவது போல, உலகம் ஆதி பகவனாகிய இறைவனை முதலாகக் கொண்டு இயங்குகிறது.'},
    2: {'name_ta': 'வான் சிறப்பு', 'name_en': 'Vaan Sirappu', 'key_kural': 11, 'meaning': 'மழை தவறாது பொழிந்து உலக உயிர்களை வாழ்விப்பதால், அத்தகைய மழையே உலகிற்கு அமுதமாக விளங்குகிறது.'},
    5: {'name_ta': 'இல்வாழ்க்கை', 'name_en': 'Ilvazhkkai', 'key_kural': 47, 'meaning': 'இல்லறத்திற்குரிய நல்லியல்புகளோடு வாழ்வாங்கு வாழ்பவன், முக்தி பெற கடுமையாக முயலும் மற்ற துறவிகள் அனைவரிலும் தலைசிறந்தவன் ஆவான்.'},
    6: {'name_ta': 'வாழ்க்கைத் துணைநலம்', 'name_en': 'Vaazkkai Thunai', 'key_kural': 51, 'meaning': 'இல்லறத்திற்கு ஏற்ற நற்பண்புகளை உடையவளாகி, தன் கணவனின் வருவாய்க்குத் தக்கபடி குடும்பத்தை நடத்தும் குணமுடையவளே சிறந்த வாழ்க்கைத் துணை ஆவாள்.'},
    8: {'name_ta': 'அன்புடைமை', 'name_en': 'Anbudaimai', 'key_kural': 71, 'meaning': 'அன்பை அடைத்து வைக்கக்கூடிய கதவு ஏதும் இல்லை; தம்மால் அன்புகாட்டப்படும் அன்பர்களின் துன்பத்தைக் கண்டபோதே கண்ணீராக வெளிப்பட்டு அன்பை வெளிப்படுத்திவிடும்.'},
    16: {'name_ta': 'பொறையுடைமை', 'name_en': 'Poraiyudaimai', 'key_kural': 151, 'meaning': 'தன்னைத் தோண்டிப் பிளப்பவர்களையும் தாங்கி நிற்கும் பூமித்தாயைப் போல, தம்மை இகழ்ந்து துன்புறுத்துவோரையும் பொறுத்து மன்னிப்பதே மனிதப் பண்புகளில் தலையாயதாகும்.'},
    25: {'name_ta': 'அருளுடைமை', 'name_en': 'Aruludaimai', 'key_kural': 241, 'meaning': 'எல்லா உயிர்களிடத்தும் கருணை காட்டும் அருள் என்னும் செல்வமே தலையாய செல்வமாகும்; பொருள் செல்வம் என்பது இழிந்தவர்களிடத்திலும் கூட இருக்கும்.'},
    26: {'name_ta': 'புலால் உண்ணாமை', 'name_en': 'Pulaal Unnaamai', 'key_kural': 251, 'meaning': 'தன் உடலை வளர்ப்பதற்காக மற்றொரு உயிரின் உடலை (இறைச்சியை) உண்பவன், எவ்வாறு தன் நெஞ்சில் கருணையையும் ஜீவகாருண்யத்தையும் நிலைநிறுத்த முடியும்?'},
    27: {'name_ta': 'தவம்', 'name_en': 'Thavam', 'key_kural': 261, 'meaning': 'தனக்கு வரும் துன்பங்களைப் பொறுத்துக் கொள்வதும், மற்ற எந்த உயிருக்கும் துன்பம் செய்யாதிருப்பதும் ஆகிய இவ்விரண்டுமே தவத்தின் மெய்யான வடிவமாகும்.'},
    28: {'name_ta': 'கூடா ஒழுக்கம்', 'name_en': 'Kooda Ozhukkam', 'key_kural': 271, 'meaning': 'மனதில் தீய எண்ணங்களை வைத்துக்கொண்டு புறத்தே துறவு வேடம் பூண்டு வாழ்வது உலக வஞ்சனையாகும்.'},
    29: {'name_ta': 'கள்ளாமை', 'name_en': 'Kallaamai', 'key_kural': 281, 'meaning': 'பிறருக்குரிய பொருளை அவர்க்குத் தெரியாமல் களவாடி எடுத்துக்கொள்ளும் எண்ணம் நெஞ்சில் ஒருபோதும் எழலாகாது.'},
    30: {'name_ta': 'வாய்மை', 'name_en': 'Vaaymai', 'key_kural': 291, 'meaning': 'உண்மை பேசுதல் என்று போற்றப்படுவது எதுவென்றால், எந்த உயிருக்கும் சிறிதும் தீமை தராத நன்மையான சொற்களைப் பேசுவதேயாகும்.'},
    31: {'name_ta': 'வெகுளாமை', 'name_en': 'Vegulaamai', 'key_kural': 301, 'meaning': 'தன் கோபம் பலிக்கும் எளியவரிடம் கோபம் கொள்ளாமல் மனத்தை அடக்குபவனே உண்மையான சினம்காப்பவன்; பலிக்காத வலிமைமிக்கவரிடம் கோபத்தை அடக்கினால் என்ன, அடக்காவிட்டால் என்ன.'},
    32: {'name_ta': 'இன்னா செய்யாமை', 'name_en': 'Inna Seyyaamai', 'key_kural': 311, 'meaning': 'சிறந்த ஒழுக்கமுடைய சான்றோர் தமக்கு எத்தகைய செல்வப் பேறு கிடைப்பதாயினும் எவ்வுயிர்க்கும் இன்னா செய்யார்.'},
    33: {'name_ta': 'கொல்லாமை', 'name_en': 'Kollaamai', 'key_kural': 321, 'meaning': 'அறநெறிகள் அனைத்திலும் தலையாய அறநெறி எந்த ஓர் உயிரையும் கொல்லாதிருத்தலே ஆகும்.'},
    34: {'name_ta': 'நிலையாமை', 'name_en': 'Nilaiyaamai', 'key_kural': 331, 'meaning': 'நிலையற்ற உலகப் பொருட்களை நிலையானவை என்று மயங்கி நம்புவதே மனித அறியாமையின் உச்சமாகும்.'},
    35: {'name_ta': 'துறவு', 'name_en': 'Thuravu', 'key_kural': 341, 'meaning': 'எந்தெந்தப் பொருட்களின் மீதான பற்றை மனிதன் துறக்கின்றானோ, அந்தந்தப் பொருட்களால் வரும் துன்பங்களிலிருந்து அவன் விடுபடுகின்றான்.'},
    36: {'name_ta': 'மெய்யுணர்தல்', 'name_en': 'Meyyunarithal', 'key_kural': 351, 'meaning': 'எப்பொருளை எத்தன்மையதாகக் கண்டபோதிலும், அப்பொருளின் மெய்ப்பொருளை உள்ளவாறு காண்பதே மெய்யுணர்வாகும்.'},
    37: {'name_ta': 'அவாவறுத்தல்', 'name_en': 'Avaa Aruththal', 'key_kural': 361, 'meaning': 'எல்லா உயிர்களுக்கும் எக்காலத்திலும் தீராத துன்பங்களைத் தரும் மறுபிறவிக்கு வித்தாக அமைவது ஆசை என்னும் கொடுங்குணமே ஆகும்; அதை அறுப்பதே மெய்ஞ்ஞானம்.'},
    38: {'name_ta': 'ஊழ்', 'name_en': 'Oozh', 'key_kural': 371, 'meaning': 'முன்செய்த நல்வினைப் பயன் வந்து சேரும் போது பொருள் பெருகும்; தீவினைப் பயன் சூழும்போது விரும்பிச் செய்தாலும் அழியும்.'},
    39: {'name_ta': 'இறைமாட்சி', 'name_en': 'Irai Maatchi', 'key_kural': 381, 'meaning': 'வீரமிக்க படை, அறிவுள்ள குடிமக்கள், திரண்ட செல்வம், தேர்ந்த அமைச்சர், நல்ல நட்பு, வலிமையான அரண் ஆகிய ஆறும் உடைய ஆட்சியாளனே அரசர்களுள் சிங்கம் போன்றவனாவான்.'},
    40: {'name_ta': 'கல்வி', 'name_en': 'Kalvi', 'key_kural': 391, 'meaning': 'கற்கத் தகுந்த நன்னூல்களைக் குற்றமறக் கற்க வேண்டும்; அவ்வாறு கற்ற பிறகு, கற்ற நன்னெறியின் வழியே தன் வாழ்நாளில் வழுவாது வாழ வேண்டும்.'},
    41: {'name_ta': 'கல்லாமை', 'name_en': 'Kallaamai', 'key_kural': 401, 'meaning': 'அறிஞர்கள் கூடிய அவையில் கல்லாதவன் பேச முனைவது, சூதாட்டக் களம் அறியாது தாய உருட்ட நினைப்பது போன்றது.'},
    42: {'name_ta': 'கேள்வி', 'name_en': 'Kelvi Selvam', 'key_kural': 411, 'meaning': 'சான்றோர்களின் அருள்மொழிகளைக் கேட்டுப் பெறும் கேள்விச் செல்வமே எல்லாச் செல்வங்களிலும் மிகச் சிறந்த தலையாய செல்வமாகும்.'},
    43: {'name_ta': 'அறிவுடைமை', 'name_en': 'Arivudaimai', 'key_kural': 421, 'meaning': 'அறிவு என்பது அழிவு வராமல் காக்கும் கவசமாகும்; பகைவராலும் அழிக்க முடியாத உட்புக இயலாத அரணாகும்.'},
    44: {'name_ta': 'குற்றங்கடிதல்', 'name_en': 'Kuttrangadithal', 'key_kural': 431, 'meaning': 'பழிபாவங்களுக்கு அஞ்சும் சான்றோர்கள், தமக்குத் தினை அளவு மிகச் சிறிய குற்றம் நேர்ந்தாலும், அதனைப் பனை மரத்தைப் போலப் பெரிதாகக் கருதி உடனே திருத்திக் கொள்வர்.'},
    45: {'name_ta': 'பெரியாரைத் துணைக்கோடல்', 'name_en': 'Periyarai Thunaikodal', 'key_kural': 441, 'meaning': 'கிடைத்தற்கு அரிய பேறுகள் எல்லாவற்றிலும் மிகச் சிறந்த பேறு எதுவென்றால், தம்மிலும் முதிர்ந்த சான்றோர்களைப் போற்றி அவர்களுக்குத் துணையாகவும் நண்பராகவும் ஆக்கிக் கொள்வதேயாகும்.'},
    46: {'name_ta': 'சிற்றினம் சேராமை', 'name_en': 'Sitrinam Seraamai', 'key_kural': 451, 'meaning': 'சேர்ந்த நிலத்தின் தன்மையால் நீரானது தனது குணம் மாறுவது போல, மனிதர்களுக்குத் தாம் சேர்கின்ற சிற்றினத்தின் சகவாசத்தால் மனமும் அறிவும் மாறிவிடும்; எனவே நற்பண்பாளர்களைச் சேர்க.'},
    47: {'name_ta': 'தெரிந்து செயல்வகை', 'name_en': 'Therinthu Seyalvagai', 'key_kural': 461, 'meaning': 'வருவாய், செலவு, தனக்கு வரும் ஊதியம் ஆகியவற்றை நன்கு ஆராய்ந்த பிறகே ஒரு செயலில் இறங்க வேண்டும்.'},
    48: {'name_ta': 'வலியறிதல்', 'name_en': 'Valiyarithal', 'key_kural': 471, 'meaning': 'செயலின் வலிமை, தன் வலிமை, பகைவனின் வலிமை, துணையாளரின் வலிமை ஆகியவற்றை அறிந்து தொடங்க வேண்டும்.'},
    49: {'name_ta': 'காலமறிதல்', 'name_en': 'Kaalamarithal', 'key_kural': 481, 'meaning': 'பகலில் காக்கையை ஆந்தை வென்றுவிடும்; அதுபோல பகையை வெல்ல நினைப்பவர்க்குத் தக்க காலமறிந்து செயல்படுதல் இன்றியமையாதது.'},
    50: {'name_ta': 'இடனறிதல்', 'name_en': 'Idanarithal', 'key_kural': 491, 'meaning': 'தக்க இடத்தை அறிந்து அரண் அமைத்துத் தொடங்காவிட்டால், பெருமுயற்சி செய்தாலும் காரியம் கைகூடாது.'},
    51: {'name_ta': 'தெரிந்து தெளிதல்', 'name_en': 'Therinthu Thelithal', 'key_kural': 501, 'meaning': 'அறம், பொருள், இன்பம், உயிரச்சம் ஆகிய நான்கு வழிகளிலும் ஒருவனை நன்கு பரிசோதித்த பின்னரே நம்பிப் பொறுப்பு ஒப்படைக்க வேண்டும்.'},
    52: {'name_ta': 'தெரிந்து வினையாடல்', 'name_en': 'Therinthu Vinaiyaadal', 'key_kural': 511, 'meaning': 'இச்செயலை முடிக்கவல்லவன் இவன் என்பதை ஆராய்ந்து, செயலையும் ஆராய்ந்து, தக்க காலத்தோடு பொருந்துமாறு உணர்ந்து அவனிடம் அச்செயலை ஒப்படைக்க வேண்டும்.'},
    53: {'name_ta': 'சுற்றந்தழால்', 'name_en': 'Suttranthazhaal', 'key_kural': 521, 'meaning': 'பழைய உறவினர்களின் சுற்றத்தை அன்பு காட்டித் தழுவி அரவணைப்பதே ஒரு மனிதனின் சிறந்த பண்பாகும்.'},
    54: {'name_ta': 'பொச்சாவாமை', 'name_en': 'Pochchaavaamai', 'key_kural': 531, 'meaning': 'அளவுகடந்த சினத்தை விடவும், அளவுக்கு மீறிய மகிழ்ச்சியில் மெய்மறந்து விழிப்புணர்வை இழக்கும் கவனக்குறைவே (மறதி) ஒருவனுக்குப் பேராபத்தைத் தரும்.'},
    55: {'name_ta': 'செங்கோன்மை', 'name_en': 'Sengonmai', 'key_kural': 541, 'meaning': 'எல்லா உயிர்களிடத்தும் நடுவுநிலையாக நின்று முறைசெய்து காப்பதே அரசனுடைய அறநெறி செங்கோலாகும்.'},
    56: {'name_ta': 'கொடுங்கோன்மை', 'name_en': 'Kodungonmai', 'key_kural': 551, 'meaning': 'மக்களைக் கொடுமைப்படுத்தி நீதி தவறும் அரசனது கொடுங்கோல் ஆட்சி நாட்டின் அமைதியையும் வளத்தையும் அழித்துவிடும்.'},
    57: {'name_ta': 'வெருவந்த செய்யாமை', 'name_en': 'Veruvandha Seyyaamai', 'key_kural': 561, 'meaning': 'குற்றத்தை நடுநிலையோடு ஆராய்ந்து, மீண்டும் அக்குற்றம் செய்யாதவாறு தக்க தண்டனை விதித்து நாட்டு மக்களைக் காப்பவனே சிறந்த அரசனாவான்.'},
    58: {'name_ta': 'கண்ணோட்டம்', 'name_en': 'Kannottam', 'key_kural': 571, 'meaning': 'கண்ணோட்டம் எனப்படும் இரக்கமும் தாட்சணியமும் உடைமையே கண்களுக்கு அழகு தரும் தலையாய பண்பாகும்.'},
    59: {'name_ta': 'ஒற்றாடல்', 'name_en': 'Ottraadal', 'key_kural': 581, 'meaning': 'நாட்டினுள் நடப்பவற்றையும் புறத்தே பகைவரிடம் நடப்பவற்றையும் ஒற்றரைக் கொண்டு ஆராய்ந்து அறிதல் வேண்டும்.'},
    60: {'name_ta': 'ஊக்கமுடைமை', 'name_en': 'Ookkamudaimai', 'key_kural': 591, 'meaning': 'மனதில் தளராத ஊக்கம் கொண்டிருத்தலே ஒரு மனிதனின் உண்மையான உடைமையாகும்; பொருள் உடைமைகள் நிலையற்றவை.'},
    61: {'name_ta': 'மடியின்மை', 'name_en': 'Madiyinmai', 'key_kural': 601, 'meaning': 'தன் குலப்பெருமை என்னும் அணையாத ஒளிவிளக்கானது, சோம்பல் என்னும் இருள் அல்லது அழுக்கு வந்து படிந்தால் ஒளியிழந்து அழிந்து போகும்.'},
    62: {'name_ta': 'ஆள்வினையுடைமை', 'name_en': 'Aalvinaiyudaimai', 'key_kural': 611, 'meaning': 'முயற்சி செய்வதை ஒருபோதும் கைவிடலாகாது; இடைவிடாத முயற்சியே ஒருவனுக்கு வெற்றியை ஈட்டித் தரும்.'},
    63: {'name_ta': 'இடுக்கண் அழியாமை', 'name_en': 'Idukkan Azhiyaamai', 'key_kural': 621, 'meaning': 'துன்பம் வரும்போது கலங்கி வாடாமல் மனஉறுதியுடன் புன்னகைத்து எதிர்கொள்ள வேண்டும்; அதுவே துன்பத்தை வெல்லும் வழி.'},
    64: {'name_ta': 'அமைச்சு', 'name_en': 'Amaichu', 'key_kural': 631, 'meaning': 'காரியங்களை முடிக்கும் கருவி, காலம், செய்யும் முறை, அருஞ்செயல் ஆகியவற்றைத் தெளிவாக உணர்ந்து செயல்படுபவனே சிறந்த அமைச்சர்.'},
    65: {'name_ta': 'சொல்வன்மை', 'name_en': 'Solvanmai', 'key_kural': 641, 'meaning': 'கேட்போரைப் பிணிக்கும் தன்மையும், கேளாதவரையும் விரும்பிக் கேட்கச் செய்யும் சொல்லாற்றலுமே சொல்வன்மையாகும்.'},
    66: {'name_ta': 'வினைத்தூய்மை', 'name_en': 'Vinai Thooymai', 'key_kural': 651, 'meaning': 'துணையாளரின் உதவி நலம் தரும் எனினும், தன் செயலின் தூய்மையே எல்லா நலன்களையும் ஒருவனுக்குப் பெற்றுத் தரும்.'},
    67: {'name_ta': 'வினைத்திட்பம்', 'name_en': 'Vinai Thitpam', 'key_kural': 661, 'meaning': 'வினைத்திட்பம் என்பது ஒரு செயலைத் தொடங்கிய பிறகு மனம் தளராது இறுதிவரை உறுதியோடு செய்து முடிக்கும் மன வலிமையாகும்.'},
    68: {'name_ta': 'வினைசெயல்வகை', 'name_en': 'Vinai Seyalvagai', 'key_kural': 671, 'meaning': 'ஆராய்ந்து முடிவு செய்த செயலைத் தடையின்றி காலந்தாழ்த்தாது நிறைவேற்றுவதே காரிய வெற்றியின் இரகசியமாகும்.'},
    69: {'name_ta': 'தூது', 'name_en': 'Thoothu', 'key_kural': 681, 'meaning': 'அன்பு, நற்குடிப்பிறப்பு, அரசன் விரும்பும் நற்குணங்கள் ஆகிய மூன்றும் ஒருங்கே அமையப்பெற்றவனே தூதுவனாவான்.'},
    70: {'name_ta': 'மன்னரைச் சேர்ந்தொழுதல்', 'name_en': 'Mannaraich Cherndhozhudhal', 'key_kural': 691, 'meaning': 'தீக்காய்பவர் மிக அருகில் செல்லாமலும் நெடுந்தொலைவில் விலகாமலும் இருப்பதைப் போல மன்னரைச் சார்ந்திருப்பவர் அடக்கத்தோடு பழக வேண்டும்.'},
    71: {'name_ta': 'குறிப்பறிதல்', 'name_en': 'Kuripparithal', 'key_kural': 701, 'meaning': 'முகக்குறிப்பையும் கண் பார்வையையும் கண்டே ஒருவர் மனக்கருத்தை உணரும் ஆற்றல் கொண்டவன் உலகில் தெய்வ நிகரானவன்.'},
    72: {'name_ta': 'அவையறிதல்', 'name_en': 'Avaiyarithal', 'key_kural': 711, 'meaning': 'அவையின் தன்மையையும் சான்றோர்களின் தகுதியையும் அறிந்து தகுந்தவாறு உரையாற்றுவதே கற்றறிந்தாரின் கடமை.'},
    73: {'name_ta': 'அவையஞ்சாமை', 'name_en': 'Avai Anjaamai', 'key_kural': 721, 'meaning': 'சொற்களின் ஆற்றலையும் வகையையும் அறிந்த தூய அறிவாளிகள், பல்துறை வல்லுநர்கள் கூடிய அவையினைக் கண்டும் மனம் கலங்கி வாய் சோர்ந்து பிழைபடப் பேசமாட்டார்கள்.'},
    74: {'name_ta': 'நாடு', 'name_en': 'Naadu', 'key_kural': 731, 'meaning': 'குன்றாத விளச்சலும், தக்க சான்றோர்களும், கெடாத பெருஞ்செல்வமும் ஒருங்கே அமைந்திருப்பதே சிறந்த நாடாகும்.'},
    75: {'name_ta': 'அரண்', 'name_en': 'Aran', 'key_kural': 741, 'meaning': 'பகைவரால் எளிதில் அணுக முடியாத நீரரண், நிலவரண், மலையரண், காட்டரண் ஆகிய நால்வகை அரண்களும் நாட்டிற்குப் பாதுகாப்பாகும்.'},
    76: {'name_ta': 'பொருள் செயல்வகை', 'name_en': 'Porul Seyalvagai', 'key_kural': 751, 'meaning': 'பொருளற்ற எளியவரையும் ஒரு பொருட்டாக மதிக்கச் செய்யும் ஆற்றல் செல்வம் ஒன்றுக்கே உண்டு.'},
    78: {'name_ta': 'படைச்செருக்கு', 'name_en': 'Padaicherukku', 'key_kural': 771, 'meaning': 'போர்க்களத்தில் பகைவரின் கூரிய வாள் தன் மீது பாய்ந்தாலும் அஞ்சாது முன்னேறும் வீரமே படையின் செருக்காகும்.'},
    79: {'name_ta': 'நட்பு', 'name_en': 'Natpu', 'key_kural': 781, 'meaning': 'செய்தற்கு அரிய பேறு நல்ல நட்பைப் போன்றது வேறில்லை; பகைவரால் அழிக்க முடியாத அரணும் நல்நட்பே.'},
    80: {'name_ta': 'நட்பாராய்தல்', 'name_en': 'Natpaaraaythal', 'key_kural': 791, 'meaning': 'ஒருவனது குணநலன்களை நன்கு ஆராயாமல் நட்புக் கொள்வது துன்பத்தை உண்டாக்கும்.'},
    81: {'name_ta': 'பழைமை', 'name_en': 'Pazhaimai', 'key_kural': 801, 'meaning': 'நெடுங்கால நட்பின் உரிமையால் நண்பர்கள் செய்யும் பிழைகளையும் அன்போடு பொறுத்துக் கொள்வதே பழைமையின் சிறப்பாகும்.'},
    82: {'name_ta': 'தீ நட்பு', 'name_en': 'Thee Natpu', 'key_kural': 811, 'meaning': 'மனதில் அன்பின்றி உதட்டளவில் பழகும் கீழ்மக்களின் நட்பு நாளுக்கு நாள் குறைந்து மறைவதே நல்லது.'},
    83: {'name_ta': 'கூடா நட்பு', 'name_en': 'Kooda Natpu', 'key_kural': 821, 'meaning': 'உள்ளத்தில் பகையை மறைத்துக்கொண்டு புறத்தே நண்பர் போலப் பழகும் வஞ்சகர்களின் நட்பைத் தவிர்க்க வேண்டும்.'},
    84: {'name_ta': 'பேதைமை', 'name_en': 'Pethaimai', 'key_kural': 831, 'meaning': 'தனக்கு நலம் தரும் நற்செயல்களை விட்டுவிட்டுத் தனக்கே கேடு விளைவிக்கும் தீயவற்றைச் செய்வதே பேதைமை ஆகும்.'},
    125: {'name_ta': 'நெஞ்சறிவுறுத்தல்', 'name_en': 'Nenjari Vuruthal', 'key_kural': 1241, 'meaning': 'காதலின் தூய தத்துவ விளக்கம்; பிரிவுத் துயரில் வாடும் ஆன்மா, பரம்பொருளையே எப்போதும் நினைத்து ஏங்கும் ஆழ்ந்த பக்தியின் ஞானக் குறியீடாகும்.'}
}

def load_kurals_data():
    if os.path.exists(KURALS_ALL_PATH):
        try:
            data = json.load(open(KURALS_ALL_PATH, encoding='utf-8'))
            kurals = data['kural'] if isinstance(data, dict) and 'kural' in data else data
            return {k['Number']: k for k in kurals}
        except Exception as e:
            print(f"Warning: could not load {KURALS_ALL_PATH}: {e}")
    return {}

def fetch_live_channel_videos():
    """
    Fetches videos using yt-dlp flat playlist extraction (0 quota).
    Falls back to channel RSS feed if yt-dlp is unavailable.
    """
    videos = []
    print("[Sync] Checking YouTube channel uploads via yt-dlp...")
    try:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--flat-playlist",
            "--dump-single-json",
            "--no-warnings",
            CHANNEL_URL
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=60)
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout)
            entries = data.get('entries', [])
            print(f"[Sync] yt-dlp returned {len(entries)} live channel items.")
            for e in entries:
                if e and e.get('id'):
                    videos.append({
                        'id': e.get('id'),
                        'title': e.get('title', ''),
                        'duration': e.get('duration'),
                        'upload_date': e.get('upload_date'),
                        'url': f"https://www.youtube.com/watch?v={e.get('id')}"
                    })
            return videos
    except Exception as e:
        print(f"[Sync] yt-dlp fetch failed or timed out: {e}")

    # Fallback to public RSS feed
    print("[Sync] Trying YouTube RSS feed fallback...")
    try:
        req = urllib.request.Request(
            CHANNEL_RSS_URL,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'yt': 'http://www.youtube.com/xml/schemas/2015'
            }
            for entry in root.findall('atom:entry', ns):
                vid_el = entry.find('yt:videoId', ns)
                title_el = entry.find('atom:title', ns)
                if vid_el is not None and vid_el.text:
                    videos.append({
                        'id': vid_el.text,
                        'title': title_el.text if title_el is not None else '',
                        'url': f"https://www.youtube.com/watch?v={vid_el.text}"
                    })
            print(f"[Sync] RSS feed returned {len(videos)} recent items.")
    except Exception as e:
        print(f"[Sync] RSS feed fetch failed: {e}")

    return videos

def identify_category_and_metadata(video, k_map):
    """
    Analyzes video title and metadata to infer category, lyrics, meaning, and playlists.
    """
    title = video.get('title', '')
    vid = video.get('id', '')
    
    # 1. Check Thirukkural
    ch_m = re.search(r'அதிகாரம்\s*(\d+)', title)
    if ch_m or 'thirukkural' in title.lower() or 'திருக்குறள்' in title:
        ch_num = int(ch_m.group(1)) if ch_m else None
        if not ch_num:
            for ch, info in CHAPTERS_DATA.items():
                if info['name_ta'] in title or info['name_en'].lower() in title.lower():
                    ch_num = ch
                    break
        
        cdata = CHAPTERS_DATA.get(ch_num, {})
        ta_name = cdata.get('name_ta', f'அதிகாரம் {ch_num}')
        en_name = cdata.get('name_en', f'Chapter {ch_num}')
        
        lyrics = ""
        meaning = cdata.get('meaning', 'திருவள்ளுவர் அருளிய உலகப் பொதுமறை திருக்குறள் நன்னெறிப் பாடல்.')
        
        if cdata.get('key_kural') and cdata['key_kural'] in k_map:
            k = k_map[cdata['key_kural']]
            lyrics = f"{k['Line1']}\n{k['Line2']}"
            if not meaning and k.get('mv'):
                meaning = k['mv']
        elif ch_num and (ch_num - 1) * 10 + 1 in k_map:
            k = k_map[(ch_num - 1) * 10 + 1]
            lyrics = f"{k['Line1']}\n{k['Line2']}"
            if not meaning and k.get('mv'):
                meaning = k['mv']
                
        is_film = 'Film' in title or 'Guru Kula Desam' in title or 'திரைப்படம்' in title
        track_type = "film" if is_film else "audio"
        canonical_title = f"திருக்குறள்: அதிகாரம் {ch_num} - {ta_name} | Thirukkural: {en_name} [{'Film' if is_film else 'Audio'}]" if ch_num else title

        return 'thirukkural', {
            "id": vid,
            "title": canonical_title,
            "type": track_type,
            "playlists": ["Discography", "திருக்குறள் | Thirukkural — Master Collection"],
            "category": "thirukkural",
            "description": f"திருக்குறள் - அதிகாரம் {ch_num}: {ta_name} | {en_name}\n\nOfficial YouTube: https://www.youtube.com/watch?v={vid}\n\n#Thirukkural #{en_name} #GuruKulaDesam",
            "author": "திருவள்ளுவர் (Thiruvalluvar)",
            "source": f"திருக்குறள் — அதிகாரம்: {ta_name}",
            "lyrics": lyrics,
            "meaning": meaning
        }
    
    # 2. Check Deity Categories
    if any(k in title for k in ['சிவன்', 'சிவ', 'நடராஜர்', 'தேவாரம்', 'திருவாசகம்', 'போற்றி திருவகவல்']):
        cat_key = 'shiva'
        author = 'மாணிக்கவாசகர் / சமயக் குரவர் நால்வர்'
        source = 'திருமுறை பன்னிரு திருமுறை'
        playlists = ['சிவ பக்தி | Shiva Songs', 'Discography']
    elif any(k in title for k in ['முருகன்', 'கந்தர்', 'சஷ்டி', 'சரவண', 'திருமுருகாற்றுப்படை']):
        cat_key = 'murugan'
        author = 'அருணகிரிநாதர் / ஸ்ரீ பாலதேவராய சுவாமிகள்'
        source = 'திருப்புகழ் / கந்த சஷ்டி கவசம்'
        playlists = ['முருகன் பக்தி | Murugan Songs', 'Discography']
    elif any(k in title for k in ['விஷ்ணு', 'கிருஷ்ணர்', 'பெருமாள்', 'கோவிந்தா', 'நாராயண', 'வெங்கடேச']):
        cat_key = 'vishnu_krishna'
        author = 'ஆழ்வார்கள்'
        source = 'நாலாயிர திவ்வியப் பிரபந்தம்'
        playlists = ['விஷ்ணு & கிருஷ்ணர் | Vishnu & Krishna Songs', 'Discography']
    elif any(k in title for k in ['விநாயகர்', 'கணபதி', 'பிள்ளையார்']):
        cat_key = 'vinayagar'
        author = 'ஔவையார் / பாரம்பரிய சான்றோர்'
        source = 'விநாயகர் அகவல் / திருமுறை'
        playlists = ['விநாயகர் பக்தி | Vinayagar Songs', 'Discography']
    elif any(k in title for k in ['அம்மன்', 'துர்க்கை', 'காளி', 'லலிதா', 'அபிராமி']):
        cat_key = 'amman'
        author = 'அபிராமி பட்டர் / தேவி உபாசகர்கள்'
        source = 'அபிராமி அந்தாதி / லலிதா சகஸ்ரநாமம்'
        playlists = ['அம்மன் & தேவி பக்தி | Amman Songs', 'Discography']
    elif any(k in title for k in ['வள்ளலார்', 'திருவருட்பா', 'பாரதியார்']):
        cat_key = 'vallalar_cultural'
        author = 'வள்ளலார் இராமலிங்க அடிகளார்'
        source = 'திருவருட்பா'
        playlists = ['வள்ளலார் & கலாச்சாரம் | Cultural', 'Discography']
    else:
        cat_key = 'thirukkural'
        author = 'குரு குல தேசம்'
        source = 'இறை இசை விருந்து'
        playlists = ['Discography']

    entry = {
        "id": vid,
        "title": title,
        "type": "film" if "Film" in title or "Guru Kula Desam" in title else "audio",
        "playlists": playlists,
        "category": cat_key,
        "description": f"{title}\n\nOfficial YouTube: https://www.youtube.com/watch?v={vid}\n#GuruKulaDesam",
        "author": author,
        "source": source,
        "lyrics": "இறை நெறியை விளக்கும் தெய்வீகப் பண்ணிசை வரிகள்.",
        "meaning": "ஆன்ம நேய ஒருமைப்பாட்டையும் இறைப் பேரருளையும் உணர்த்தும் புனித விளக்கம்."
    }
    return cat_key, entry

def run_sync():
    print("=" * 60)
    print("   Guru Kula Desam — Near-Live YouTube Sync Automation")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.path.exists(CATALOG_JSON_PATH):
        print(f"[Error] Catalog JSON not found at: {CATALOG_JSON_PATH}")
        return False

    catalog = json.load(open(CATALOG_JSON_PATH, encoding='utf-8'))
    existing_ids = {it['id'] for items in catalog.values() for it in items}
    print(f"[Sync] Existing site catalog holds {len(existing_ids)} unique video IDs.")

    live_videos = fetch_live_channel_videos()
    if not live_videos:
        print("[Sync] No live videos returned or network unavailable. Exiting gracefully.")
        return True

    missing_live = [v for v in live_videos if v['id'] not in existing_ids]
    print(f"[Sync] Detected {len(missing_live)} newly published videos on channel.")

    if not missing_live:
        print("[Sync] Site catalog is already 100% up to date with live YouTube channel!")
        return True

    k_map = load_kurals_data()

    # Ingest new videos
    new_thirukkural_items = []
    for vid_obj in missing_live:
        cat_key, entry = identify_category_and_metadata(vid_obj, k_map)
        if cat_key not in catalog:
            catalog[cat_key] = []
        catalog[cat_key].append(entry)
        existing_ids.add(entry['id'])
        print(f"  [+] Ingested [{cat_key}]: {entry['title']} ({entry['id']})")
        if cat_key == 'thirukkural':
            new_thirukkural_items.append(entry)

    # Save docs/assets/data/catalog.json
    with open(CATALOG_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"[Sync] Updated {CATALOG_JSON_PATH}")

    # Save docs/assets/data/catalog.js
    with open(CATALOG_JS_PATH, 'w', encoding='utf-8') as f:
        f.write("// Complete Curated Web Catalog (Sacred Musical Productions & Films)\n")
        f.write("window.GKD_SITE_CATALOG = ")
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        f.write(";\n\n// Dual-binding for main.js search integration\nwindow.GURUKULA_CATALOG = window.GKD_SITE_CATALOG;\n")
    print(f"[Sync] Updated {CATALOG_JS_PATH}")

    # Update docs/thirukkural.html if needed
    if new_thirukkural_items and os.path.exists(THIRUKKURAL_HTML_PATH):
        with open(THIRUKKURAL_HTML_PATH, 'r', encoding='utf-8') as f:
            html = f.read()
        m = re.search(r'const PAGE_ITEMS = (\[.*?\]);', html)
        if m:
            page_items = json.loads(m.group(1))
            p_ids = {it['id'] for it in page_items}
            for tk in new_thirukkural_items:
                if tk['id'] not in p_ids:
                    page_items.append({
                        "id": tk["id"],
                        "title": tk["title"],
                        "type": tk["type"],
                        "playlists": tk["playlists"]
                    })
                    p_ids.add(tk['id'])
            new_page_str = f"const PAGE_ITEMS = {json.dumps(page_items, ensure_ascii=False)};"
            html = html[:m.start()] + new_page_str + html[m.end():]
            with open(THIRUKKURAL_HTML_PATH, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[Sync] Updated PAGE_ITEMS in {THIRUKKURAL_HTML_PATH}")

    # Update master catalogs
    for mpath in MASTER_CATALOG_PATHS:
        if os.path.exists(mpath):
            try:
                master = json.load(open(mpath, encoding='utf-8'))
                m_ids = {m.get('video_id') for m in master}
                for v in missing_live:
                    if v['id'] not in m_ids:
                        master.append({
                            "video_id": v['id'],
                            "canonical_title": v.get('title'),
                            "tamil_title": v.get('title'),
                            "english_title": v.get('title'),
                            "descriptor": "Film" if "Film" in v.get('title', '') else "Audio",
                            "length": len(v.get('title', '')),
                            "genre": "இறை இசை விருந்து",
                            "track_type": "Cinematic Film / Video",
                            "author": "Guru Kula Desam",
                            "source": "YouTube Channel Live Sync",
                            "playlists": ["Discography"],
                            "youtube_url": v.get('url'),
                            "duration": "PT4M00S",
                            "published_at": datetime.now().isoformat(),
                            "scripture_source": "YouTube Live"
                        })
                        m_ids.add(v['id'])
                with open(mpath, 'w', encoding='utf-8') as f:
                    json.dump(master, f, ensure_ascii=False, indent=2)
                print(f"[Sync] Updated master catalog: {mpath}")
            except Exception as e:
                print(f"[Sync] Could not update {mpath}: {e}")

    # Trigger Tri-Folder Sync
    sync_tool = os.path.join(ROOT_DIR, 'tools', 'sync', 'sync_trifolder.py')
    if os.path.exists(sync_tool):
        print("[Sync] Invoking tools/sync/sync_trifolder.py --source docs...")
        subprocess.run([sys.executable, sync_tool, '--source', 'docs'], check=True)

    print("[Sync] Near-live sync successfully finished!")
    return True

if __name__ == '__main__':
    run_sync()

