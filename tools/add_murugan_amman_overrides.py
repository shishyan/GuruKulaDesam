import sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')

P = pathlib.Path('production/youtube_lyrics_overrides.json')
o = json.loads(P.read_text(encoding='utf-8'))
W = o['_works']

# 1. Kandha Sashti Kavasam (Full Opening/Core)
W['kandhasashti'] = {
    'status': 'ok',
    'source': 'Bala Devaraya Swamigal, Kandha Sashti Kavasam (public domain); kaumaram.com',
    'lyrics': 'துதிப்போர்க்கு வல்வினைபோம் துன்பம்போம்\nநெஞ்சில் பதிப்போர்க்குச் செல்வம் பலித்துக்கதித்தோங்கும்\nநிஷ்டையுங் கைகூடும் நிமலரருள் கந்தர்\nசஷ்டி கவசந் தனை.\n\nசஷ்டியை நோக்கச் சரவண பவனார்\nசிஷ்டருக் குதவும் செங்கதிர் வேலோன்\nபாதம் இரண்டில் பன்மணிச் சதங்கை\nகீதம் பாடக் கிண்கிணி யாட\nமையல் நடனஞ்செய்யும் மயில்வா கனனார்\nகையில் வேலால் எனைக் காக்கவென் றுவந்து\nவரவர வேலா யுதனார் வருக வருக வருக மயிலோன் வருக!',
    'meaning': 'தேவராய சுவாமிகள் அருளிய கந்த சஷ்டி கவசம். இதனை பக்தியுடன் துதிப்போருக்கு வல்வினைகளும் துன்பங்களும் நீங்கும்; செல்வம் பெருகும்; தியானமும் மன அமைதியும் கைகூடும். மயில் மீது அமர்ந்து வேலேந்தி வரும் சரவணபவப் பெருமான் தம்மை எந்நேரமும் காத்தருள வேண்டும் எனப் போற்றி வேண்டுகிறார்.'
}

# 2. Gana Natha Om (Classical Vinayagar Moola Mantra)
W['gananatha'] = {
    'status': 'ok',
    'source': 'Classical Vinayagar Moola Mantra and Devotional Prayer (public domain); tamilvu.org',
    'lyrics': 'கண நாதா ஓம் கண நாதா ஓம்\nகண நாதா ஓம் கண நாதா!\nகஜமுக வேழ முகத்தோனே\nகணபதி சரணம் கண நாதா!\n\nஐந்து கரத்தனை ஆனை முகத்தனை\nஇந்தின் இளம்பிறை போலும் எயிற்றனை\nநந்தி மகன்றனை ஞானக் கொழுந்தினைப்\nபுந்தியில் வைத்தடி போற்றுகின் றேனே!',
    'meaning': 'கணங்களின் தலைவனான கணபதியை ஓம் என்னும் பிரணவ நாதத்தோடு போற்றுகின்றோம். ஐந்து கரங்களையும், யானை முகத்தையும், பிறைச்சந்திரன் போன்ற தந்தத்தையும், சிவபெருமானின் திருமகனாகவும் ஞானத்தின் வடிவமாகவும் விளங்கும் விநாயகப் பெருமானைத் தினமும் நெஞ்சில் வைத்துப் போற்றுகின்றேன்.'
}

# 3. 108 Saraswathi Potri (Goddess Saraswathi Prayer)
W['saraswathi108'] = {
    'status': 'ok',
    'source': 'Goddess Saraswathi Classical Stotram / Potri (public domain); dinamalar.com',
    'lyrics': 'சரஸ்வதி நமஸ்துப்யம் வரதே காமரூபிணி\nவித்யாரம்பம் கரிஷ்யாமி சித்திர்பவது மே சதா!\n\nஆயகலைகள் அறுபத்து நான்கினையும்\nஏய உணர்விக்கும் என்னம்மை - தூய\nஉருப்பளிங்கு போல்வாள் என் உள்ளத்தினுள்ளே\nஇருப்பளிங்கு வாரா திடர்!',
    'meaning': 'கலைமகளே, வேண்டுவோருக்கு வேண்டிய வரங்களை அருள்பவளே, உன்னை வணங்குகிறேன். நான் கல்வியைத் தொடங்குகிறேன்; அது எனக்கு எப்போதும் வெற்றியைத் தரட்டும். அறுபத்து நான்கு கலைகளையும் அறியச் செய்யும் தூய படிகம் போன்ற கலைவாணி என் உள்ளத்தில் வீற்றிருக்கும் போது எனக்கு எந்த இடரும் வராது என்பது பொருள்.'
}

# 4. Samayapuram Mariamman / Renukambal / Karumariamman Prayer
W['mariamman'] = {
    'status': 'ok',
    'source': 'Classical Amman Devotional / Mariamman Thuthi (public domain); tamilvu.org',
    'lyrics': 'தாயே சமயபுரத்து மாரியம்மா\nஎங்கள் தாகம் தணித்து அருள் தாரம்மா!\nகண்ணபுர நாயகியே காக்கும் அன்னையே\nவேப்பிலை ஆடை கொண்டு வினை தீர்ப்பாயே!\n\nஓம் சக்தி ஓம் பராசக்தி ஓம் சக்தி ஓம்\nஅகிலாண்ட நாயகியே அம்மா சரணம்!',
    'meaning': 'சமயபுரத்தில் கோயில் கொண்டுள்ள மாரியம்மனே, எங்கள் துயரங்களைத் தீர்த்து அருள்புரிவாயாக. வேப்பிலையின் குளிர்ச்சியால் நோய்களையும் துன்பங்களையும் நீக்கி, உலகைக் காக்கும் அகிலாண்டேஸ்வரியான அன்னையின் திருவடிகளைச் சரணடைகிறோம்.'
}

# 5. Vadivudai Manikkamalai (Ramalinga Swamigal / Vallalar, Amman shrine at Thiruvottriyur)
W['vadivudai'] = {
    'status': 'ok',
    'source': 'Ramalinga Swamigal (Vallalar), Vadivudai Manikkamalai verse 1 (public domain); shaivam.org',
    'lyrics': 'மன்னுபுகழ் காழியில்வாழ் ஞானசம்பந்தன்வளர்\nதென்னமுத வாசகஞ்செய் வாதவூர்ச் செம்மல்வள்ளல்\nநாவரசர் சுந்தரனார் நற்றமிழைப் போன்றதென\nயான்உரைக்கும் புன்சொல்லும் ஏற்றுஅருளல் வேண்டுமம்மா!\nவடிவுடை மாணிக்க மாலையே என் தாயே!',
    'meaning': 'திருவொற்றியூரில் எழுந்தருளியுள்ள வடிவுடை மாணிக்க வள்ளியம்மையே! திருஞானசம்பந்தர், மாணிக்கவாசகர், திருநாவுக்கரசர், சுந்தரமூர்த்தி நாயனார் ஆகிய அருளாளர்களின் தேனினிய தமிழ்ப்பாடல்களைப் போல, அடியேன் உரைக்கும் எளிய சொற்களையும் ஏற்றுத் தாயே எனக்கு அருள்புரிய வேண்டும் என்று வள்ளலார் போற்றுகிறார்.'
}

# 6. Murugan: Skanda Mantram / Koumaram Stuthi / Murugar Vaara Vazhipadu
# Many Murugan tracks share anubhuti; let's map the ones that are specifically Skanda Mantra / Koumaram
murugan_amman_mappings = {
    '1hoVaPwWMes': 'kandhasashti',
    'Lki_Y8OSljs': 'gananatha',
    'lEHLSYxnpbU': 'gananatha',
    'VMn8fiWF-oA': 'saraswathi108',
    'rYUfISYky0g': 'saraswathi108',
    'CS92JrOQkbc': 'saraswathi108',
    'wehcVz3BMHo': 'mariamman',
    'grjVzzo-RWc': 'mariamman',
    'vaXLG5kUGVc': 'mariamman',
    'bZ03UopgYcc': 'mariamman',
    '60rrBjJfAS4': 'abirami69',
    '7iWQUBmq3aU': 'vadivudai',
}

for vid, ref in murugan_amman_mappings.items():
    o[vid] = {'ref': ref}

P.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Added Murugan, Vinayagar, Amman overrides. Total video overrides now: {len([k for k in o if not k.startswith('_')])}")
