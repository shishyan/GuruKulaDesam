"""Merge web-sourced Thiruppavai 1-3 and Abirami Anthadhi 1 into production/youtube_lyrics_overrides.json (idempotent).

Texts: public-domain (Andal; Abirami Bhattar) as found on dinamalar.com / prapatti.com / epintamilnanban.com via web search.
Meanings are original short summaries.
"""
import json, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'production' / 'youtube_lyrics_overrides.json'
o = json.loads(P.read_text(encoding='utf-8'))
W = o['_works']

W['thiruppavai1'] = dict(status='ok', source='Andal, Thiruppavai 1 (public domain); dinamalar.com, prapatti.com',
 lyrics='மார்கழித் திங்கள் மதிநிறைந்த நன்னாளால்\nநீராடப் போதுவீர் போதுமினோ நேரிழையீர்!\nசீர்மல்கும் ஆய்ப்பாடிச் செல்வச் சிறுமீர்காள்!\nகூர்வேல் கொடுந்தொழிலன் நந்தகோபன் குமரன்,\nஏரார்ந்த கண்ணி யசோதை இளஞ்சிங்கம்,\nகார்மேனிச் செங்கண் கதிர்மதியம் போல் முகத்தான்\nநாராயணனே, நமக்கே பறை தருவான்,\nபாரோர் புகழப் படிந்தேலோர் எம்பாவாய்!',
 meaning='மார்கழி மாதத்தின் நிறைமதி நாளில், ஆய்ப்பாடிச் சிறுமியரை நீராடி நோன்பு நோற்க ஆண்டாள் அழைக்கிறாள். நந்தகோபன், யசோதையின் இளஞ்சிங்கமான கண்ணனே நாராயணன்; அவனே நமக்கு நோன்பின் பயனை அருள்வான், உலகம் புகழும்படி நாம் நீராடுவோம் என்று திருப்பாவையைத் தொடங்குகிறாள்.')

W['thiruppavai2'] = dict(status='ok', source='Andal, Thiruppavai 2 (public domain); dinamalar.com, prapatti.com',
 lyrics='வையத்து வாழ்வீர்காள்! நாமும் நம் பாவைக்குச்\nசெய்யும் கிரிசைகள் கேளீரோ! பாற்கடலுள்\nபையத் துயின்ற பரமன் அடிபாடி\nநெய்யுண்ணோம் பாலுண்ணோம் நாட்காலே நீராடி\nமையிட்டெழுதோம் மலரிட்டு நாம் முடியோம்\nசெய்யாதன செய்யோம் தீக்குறளைச் சென்றோதோம்\nஐயமும் பிச்சையும் ஆந்தனையும் கைகாட்டி\nஉய்யுமா றெண்ணி உகந்தேலோர் எம்பாவாய்!',
 meaning='பாற்கடலில் அறிதுயில் கொள்ளும் பரமனின் திருவடிகளைப் பாடி நோன்பு நோற்போம். நெய், பால் உண்ணோம்; கண்ணுக்கு மை இடோம்; மலர் சூடோம்; செய்யத் தகாதன செய்யோம்; கோள் சொல்லோம்; தானம் செய்து உய்யும் வழியை எண்ணி மகிழ்வோம் என்று நோன்பின் நியமங்களை ஆண்டாள் கூறுகிறாள்.')

W['thiruppavai3'] = dict(status='ok', source='Andal, Thiruppavai 3 (public domain); dinamalar.com, vedics.org',
 lyrics='ஓங்கி உலகளந்த உத்தமன் பேர்பாடி\nநாங்கள் நம் பாவைக்குச் சாற்றி நீராடினால்\nதீங்கின்றி நாடெல்லாம் திங்கள் மும்மாரி பெய்து\nஓங்கு பெருஞ்செந்நெல் ஊடு கயலுகள\nபூங்குவளைப் போதில் பொறிவண்டு கண்படுப்ப\nதேங்காதே புக்கிருந்து சீர்த்த முலைபற்றி\nவாங்கக் குடம்நிறைக்கும் வள்ளல் பெரும்பசுக்கள்\nநீங்காத செல்வம் நிறைந்தேலோர் எம்பாவாய்!',
 meaning='உலகை அளந்த உத்தமனான திருமாலின் திருநாமத்தைப் பாடி நோன்பு நோற்றால், நாட்டில் தீங்கின்றி மாதம் மூன்று முறை மழை பெய்யும்; செந்நெல் வளரும், மீன்கள் துள்ளும், வண்டுகள் மலரில் உறங்கும், பசுக்கள் குடம் குடமாகப் பால் தரும்; நீங்காத செல்வம் நிறையும் என்று பாடுகிறாள்.')

W['abirami1'] = dict(status='needs_audio_check', source='Abirami Bhattar, Abirami Anthadhi verse 1 (public domain); epintamilnanban.com',
 lyrics='உதிக்கின்ற செங்கதிர், உச்சித் திலகம், உணர்வுடையோர்\nமதிக்கின்ற மாணிக்கம், மாதுளம்போது, மலர்க்கமலை\nதுதிக்கின்ற மின்கொடி, மென்கடிக் குங்குமத் தோயமென்ன\nவிதிக்கின்ற மேனி அபிராமி, என்றன் விழுத்துணையே!',
 meaning='உதிக்கும் செங்கதிர், நெற்றித் திலகம், அறிந்தோர் போற்றும் மாணிக்கம், மாதுளம்பூ, குங்குமக் குழம்பு போன்ற செந்நிறத் திருமேனியுடைய அபிராமி அன்னையே என் உறுதுணை என்று அபிராமிபட்டர் அந்தாதியைத் தொடங்குகிறார்.')

for vid, ref in {'RDcw0Bol-cE': 'thiruppavai1', 'QH-xL37NmGM': 'thiruppavai1',
                 'Lzkbhp_ehA8': 'thiruppavai2', 'hm7_qUlTUiU': 'thiruppavai2',
                 '31xVgvxoiUA': 'thiruppavai3', '2tL-bKjkL18': 'abirami1'}.items():
    o[vid] = {'ref': ref}
P.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding='utf-8')
print('overrides now:', len([k for k in o if not k.startswith('_')]), 'videos,', len(W), 'works')
