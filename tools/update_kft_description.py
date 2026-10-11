import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

vid = 'KFtS403RfbY'

new_description = """நெஞ்சறிவுறுத்தல் – பகுதி 1 | Nenjari Vuruthal Part 1
ஆன்ம விழிப்புணர்வு மற்றும் மெய்யறிவுப் பெருங்கடல் | A Divine Cinematic Journey of Reflection, Inner Light and Spiritual Liberation.

═════════════════════════════════════════════════════════════════
🕉️ SCRIPTURE & PHILOSOPHICAL OVERVIEW
═════════════════════════════════════════════════════════════════
Deity / Subject: நெஞ்சறிவுறுத்தல் (Awakening the Soul / Mind Contemplation)
Scripture Source: சித்தர் மரபு & தமிழ் மெய்யியல் (Tamil Siddha Philosophy & Wisdom)
Core Essence: மாயையை நீக்கி, ஆன்மாவை நடுநிலைப்படுத்தி, இறையருளோடு கலக்கும் உன்னத ஞான அனுபவம்.

═════════════════════════════════════════════════════════════════
📜 பாடல் வரிகள் (FULL SACRED TAMIL LYRICS)
═════════════════════════════════════════════════════════════════
[பல்லவி / முகப்பு]
ஒன்றாய் பலவாய் உயிராய் நன்றாய்
நவமாய் நடுநிலையாய் நின்ற பேரொளியே!

[அனுபல்லவி & திருப்பாடல்கள்]
இப்பிறவி நோய் தீர்க்கும் மாமருந்தே
என்றும் நிலைபெற்ற தத்துவப் பரம்பொருளே!
பொறிவாயில் ஐந்தவித்த மெய்ந்நெறியே
பவக்கடல் கடத்திடும் ஞானப் பெருந்துறையே!

சத்துவமாய் சாந்தமாய் விளங்கும் உள்ளொளியே
ஒன்றாய் பலவாய் நிறைந்த அருள்வடிவே!
காலமாய் காலத்தைக் கடந்த நிலையாய்
சுதியாய் சுதியினில் லயிக்கும் பேரமைதியே!

சித்தமாகிச் சித்துக்கெல்லாம் வித்தாகிய நிலையே
சுத்த சிவ சாந்தமயானந்த பெருவெளியே!
அருட்பெருஞ்ஜோதி அனந்தப் பெருங்கடலே
அசைவற்ற ஆனந்தக் கரும்பே ஆரமுதமே!

பரமாய் பார்த்த பொருளாய் சுவையாய்
பரப்பிரம்மமாய் விளங்கும் தனிப்பெரும் கதியே!
எல்லார்க்கும் ஒன்றாய் பலவாய் நிறைந்த பேரொளியே
உயிராய் நின்றொளிரும் ஆதிப் பரம்பொருளே!

நல்வினையாய் தீவினையாய் கடந்த ஞானமே
அரிதினும் அரிதாய் விளங்கும் சிவவடிவே!
உன்னுடன் இருப்பதாய் உய்வதாய் உள்ளொளியே
நிலையான பேரின்ப முக்திப் பெருவாழ்வே!

[நிறைவுப் பாடல்]
பட்டுருவாய் பட்டால் படாஅ வருவின் மொழி விளங்கும்
சித்துருவாய் உள்ளிக்கும் சித்தனே - வையாது
வைத்துக்களை மாவேந்திர சாலம் செய்யாது
சேவிக்கும் சித்தனே போற்றி!

═════════════════════════════════════════════════════════════════
📖 ENGLISH TRANSLATION & MEANING
═════════════════════════════════════════════════════════════════
• Nenjari Vuruthal is a supreme spiritual contemplation addressing one's inner soul to transcend the illusions of the senses and find everlasting peace in divine oneness.
• "O Supreme Divine Light, One and Many, the Primal Life and Truth, You stand in absolute stillness as the remedy for the afflictions of this worldly birth."
• "Beyond all duality of past deeds, You shine as the nectar of silence and pure bliss in the lotus of the meditator's heart."

═════════════════════════════════════════════════════════════════
⏱ Timestamps / Musical Chapters (அமைப்பும் நேரமும்):
═════════════════════════════════════════════════════════════════
00:00 - சங்க கால முகப்பு & தோற்றுவாய் (Sangam Invocation & Soul Prelude)
01:30 - இப்பிறவி நோய் தீர்க்கும் மாமருந்து (Sacred Remedy of Being)
02:11 - பொறிவாயில் ஐந்தவித்த மெய்ந்நெறி (Mastery of the Five Senses)
03:26 - சத்துவமாய் சாந்தமாய் விளங்கும் உள்ளொளி (Luminous Inner Peace)
04:21 - காலத்தைக் கடந்த பேரமைதி (Timeless Contemplation)
04:59 - வேதத்தின் மெய்ப்பொருள் (Universal Divine Light)
06:05 - சித்தமாகிச் சித்துக்கெல்லாம் வித்து (The Root of Liberation)
06:40 - அருட்பெருஞ்ஜோதி அனந்தப் பெருங்கடல் (Infinite Grace & Bliss)
08:11 - பரப்பிரம்மமாய் விளங்கும் தனிப்பெரும் கதி (Supreme Divine Soliloquy)
08:48 - எல்லார்க்கும் ஒன்றாய் பலவாய் நிறைந்த பேரொளி (Omnipresent Grace)
09:39 - இருவினைகளைக் கடந்த ஞானம் (Beyond Karma: Pure Awakening)
10:18 - அலவாய் நின்ற பேரருளமுதம் (Divine Flow of Silence)
11:32 - பேரின்ப முக்திப் பெருவாழ்வு (Sacred Communion with Mind)
12:48 - நடுநிலையாய் நின்ற தனிமுதல்வன் (Centered Cosmic Stillness)
13:35 - சித்துருவாய் உள்ளிக்கும் சித்தனே போற்றி (Final Benediction & Siddha Outro)

═════════════════════════════════════════════════════════════════
🎵 PRODUCTION CREDITS
═════════════════════════════════════════════════════════════════
• Concept, Production & Curation: Guru Kula Desam (@guru-kula-desam)
• Sound Engineering: Guru Kula Desam Sacred Audio Lab
• Visuals: 24 Sacred Devotional Scenes & Divine Meditation Imagery

#GuruKulaDesam #NenjariVuruthal #TamilDevotional #SiddhaWisdom #MeditationMusic #SpiritualAwakening #TamilWisdom"""

try:
    token_path = 'data/credentials/token_backup_guru-kula-desam.json'
    creds = Credentials.from_authorized_user_file(token_path)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    yt = build('youtube', 'v3', credentials=creds)
    v_res = yt.videos().list(part='snippet', id=vid).execute()
    snip = v_res['items'][0]['snippet']
    snip['description'] = new_description
    upd = yt.videos().update(part='snippet', body={'id': vid, 'snippet': snip}).execute()
    print("SUCCESS via API! Updated description on YouTube live!")
except Exception as e:
    print("API update failed or quota exceeded:", e)
    # Save description locally for browser update
    with open('scratch/kft_new_desc.txt', 'w', encoding='utf-8') as f:
        f.write(new_description)
    print("Saved scratch/kft_new_desc.txt for browser CDP injection!")
