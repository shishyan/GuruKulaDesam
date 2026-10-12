# -*- coding: utf-8 -*-
import sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

creds = Credentials.from_authorized_user_file('data/credentials/tokens/token_942198183044.json')
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

r = yt.videos().list(part='snippet', id='dpx7C3wuyio').execute()
snip = r['items'][0]['snippet']
print('Current title:', snip['title'])

# Build pristine authentic description for திருவாசகம் — யாத்திரைப் பத்து
correct_desc = """மாணிக்கவாசகர் அருளிச்செய்த எட்டாம் திருமுறை திருவாசகம் — யாத்திரைப் பத்து: பூவார் சென்னி மன்னன் (தில்லையில் அருளியது).

Original song: https://youtu.be/iKIsoxTz5-k
Music: Guru Kula Desam

#GuruKulaDesam #LordShiva #Thiruvasagam #Manikkavasagar #TamilDevotional #SivaPeruman

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 திருவாசகம்: யாத்திரைப் பத்து — பாடல் வரிகள் (Lyrics):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[பல்லவி / தொடக்கம்]
பூவார் சென்னி மன்னன்எம் புயங்கப் பெருமான் சிறியோமை
ஓவா துள்ளங் கலந்துணர்வாய் உருக்கும் வெள்ளக் கருணையினால்
ஆவா என்னப் பட்டன்பாய் ஆட்பட் டீர்வந் தொருப்படுமின்
போவோம் காலம் வந்ததுகாண் பொய்விட் டுடையான் கழல்புகவே!

[சரணம் 1]
புகவே வேண்டாம் புலன்களில்நீர் புயங்கப் பெருமான் பூங்கழல்கள்
மிகவே நினைமின் மிக்கவெல்லாம் வேண்டா போக விடுமின்கள்
நகவே ஞாலத் துள்புகுந்து நாயே அனைய நமையாண்ட
தகவே உடையான் தனைச்சாரத் தளரா திருப்பார் தாம்தாமே!

[சரணம் 2]
தாமே தமக்குச் சுற்றமும் தாமே தமக்கு விதிவகையும்
யாமார் எமதார் பாசமார் என்ன மாய மிவைபோகக்
கோமான் பண்டைத் தொண்டரொடும் அவன்றன் குறிப்பே குறிக்கொண்டு
போமாறு அமைமின் பொய்நீக்கிப் புயங்கன் ஆள்வான் பொன்னடிக்கே!

[சரணம் 3]
அடியார் ஆனீர் எல்லீரும் அகல விடுமின் விளையாட்டைப்
படியே வந்து பாதம்பணிந்து கடைக்கொண் டிருமின் திருக்குறிப்பை
செடிசேர் உடலைச் செலநீக்கிச் சிவலோகத்தே நமைவைப்பான்
பொடிசேர் மேனிப் புயங்கன்றன் பூவார் கழற்கே புகவிடுமே!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 ஆன்மீகப் பொருள் விளக்கம் (Spiritual Meaning):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
மலர் நிறைந்த சடைமுடியை உடைய அரசனும், பாம்பினை ஆபரணமாக அணிந்த எம்பெருமானாகிய சிவபெருமான், சிறியவர்களாகிய நம் உள்ளத்தில் இடையறாது கலந்து நம்மை உருகச் செய்யும் அளப்பரிய கருணையினால் நம்மை ஆட்கொண்டருளினான்.

அன்புமிக்க அடியார்களே! நிலையில்லாத இவ்வுலகப் பொய்களைத் துறந்து, நம்மை ஆட்கொண்ட இறைவனின் திருவடிகளை அடைவதற்கான பேரின்ப காலம் வந்துவிட்டது; சிவலோக யாத்திரைக்கு உடனே புறப்படுங்கள்!

— குரு குல தேசம் | Guru Kula Desam
https://gurukuladesam.com"""

snip['description'] = correct_desc
up = yt.videos().update(part='snippet', body={'id': 'dpx7C3wuyio', 'snippet': snip}).execute()
print('SUCCESS! Updated dpx7C3wuyio description live on YouTube!')
