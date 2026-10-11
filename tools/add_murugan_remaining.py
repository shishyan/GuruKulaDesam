import sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')

P = pathlib.Path('production/youtube_lyrics_overrides.json')
o = json.loads(P.read_text(encoding='utf-8'))
W = o['_works']

# Arunagirinathar Thiruppugazh: Arumugam Arumugam
W['arumugam'] = {
    'status': 'ok',
    'source': 'Arunagirinathar, Thiruppugazh "Arumugam Arumugam" (public domain); kaumaram.com',
    'lyrics': 'ஆறுமுகம் ஆறுமுகம் ஆறுமுகம் ஆறுமுகம்\nஆறுமுகம் ஆறுமுகம் என்றுபூதி\nஆகமவி தப்படிய ணிந்துதொழு மவர்களெதிர்\nஅடிமையென நிற்பரம னம்பொற்கழலே!',
    'meaning': 'ஆறுமுகம் ஆறுமுகம் ஆறுமுகம் ஆறுமுகம் என்று பக்தியோடு கூறி, ஆகம முறைப்படி திருநீறு அணிந்து வணங்குபவர்களின் முன்னே, சிவபெருமானின் திருவடிகள் தமக்கே அடிமை போல வந்து நிற்கும் என்று அருணகிரிநாதர் அருளுகிறார்.'
}

# Ramalinga Swamigal (Vallalar) - Siva Subramaniyar Thiruvirutham
W['sivasubramaniyar'] = {
    'status': 'ok',
    'source': 'Ramalinga Swamigal (Vallalar), Siva Subramaniyar Thiruvirutham (public domain); shaivam.org',
    'lyrics': 'காரும் தணியா வெப்பகற்றும் கதிரே மணியே கந்தரசே\nசீரும் திகழும் சிவஞானச் செல்வப் பொருளே சீராளா\nவாரும் வாரும் எனையீன்ற வள்ளல் மணியே வடிவேலா\nபாரும் விழிப்பார் என்னாவிப் பற்றே சரணம் சரணாமே!',
    'meaning': 'அறியாமை என்னும் வெப்பத்தைப் போக்கும் சிவஞானச் சுடரே, கந்தவேளே, எம்பெருமானே, என்னை ஆட்கொள்ள வாராய்! உன்னுடைய கருணை விழிகளால் என்னை நோக்கி அருள் புரிய வேண்டும் என்று வள்ளலார் உருகி வேண்டுகிறார்.'
}

# Skanda Mantram / Koumaram Stuthi
W['skandamantram'] = {
    'status': 'ok',
    'source': 'Skanda Gayatri & Moola Mantra Classical Hymn (public domain); kaumaram.com',
    'lyrics': 'சரவணபவ ஓம் சரவணபவ ஓம்\nசரவணபவ ஓம் சண்முகா சரணம்!\nகார்த்திகேயா கருணாகரா\nகந்தா முருகா குகனே சரணம்!\n\nஓம் தத்புருஷாய வித்மஹே மஹாஸேனாய தீமஹி\nதந்நோ ஷண்முக: ப்ரசோதயாத்!',
    'meaning': 'சரவணபவ என்னும் ஆறு எழுத்து மந்திரத்தையும், கந்தனின் காயத்ரி மந்திரத்தையும் போற்றுகிறோம். ஞானத்தையும் ஆற்றலையும் அளிக்கும் சண்முகப் பெருமானின் திருவடிகளைப் போற்றிச் சரணடைகிறோம்.'
}

murugan_extra = {
    'B6yVe6HM8Ok': 'arumugam',
    'W2peLbC20sA': 'sivasubramaniyar',
    'yPfkP_EjTyc': 'skandamantram',
    'iJ-3SHR2MKw': 'skandamantram',
    'QRSRyYEacMs': 'skandamantram',
    'FFXImcs5Ehw': 'skandamantram',
    '-L3VXkM2MTY': 'skandamantram',
    'XErAOEtZdAU': 'skandamantram',
    'VMqFjcQtebw': 'skandamantram',
    'eEYBleNgRGU': 'alankaram38',
    'meXI3QsNHhE': 'seerulaaviya',
    'FTAB7OBVPPY': 'seerulaaviya',
    'l3E27q5r-nk': 'kaithala',
}

for vid, ref in murugan_extra.items():
    o[vid] = {'ref': ref}

P.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Added Murugan remaining overrides. Total video overrides now: {len([k for k in o if not k.startswith('_')])}")
