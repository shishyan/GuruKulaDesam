import json, sys, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
VID = 'Mata6vtnrjQ'

# Load canonical kurals
tk_data = json.load(open(ROOT / 'production/thirukkural_all.json', encoding='utf-8'))
kurals_by_num = {item['Number']: item for item in tk_data['kural']}

# Build complete 10 kurals lyrics and meanings
ch_num = 61
start_kural = 601
end_kural = 610

kural_sections = []
for kn in range(start_kural, end_kural + 1):
    kd = kurals_by_num[kn]
    mean = kd.get('mv') or kd.get('mk') or kd.get('sp') or kd.get('explanation')
    kural_sections.append(f"குறள் {kn}:\n{kd['Line1']}\n{kd['Line2']}\nஉரை: {mean}")

full_kurals_text = "\n\n".join(kural_sections)

desc = f"""அதிகாரம் 61 - மடியின்மை | Madiyinmai - Overcoming Indolence & Diligence | Guru Kula Desam

அதிகாரம் 61: மடியின்மை (Madiyinmai) — சோம்பலை அறவே ஒழித்து, சுறுசுறுப்பும் இடைவிடாத உழைப்பும் கொண்டு வாழ்க்கையை உயர்த்தும் மாபெரும் ஊக்க அதிகாரம். காலம் பொன் போன்றது; விடியலின் ஆற்றலை உணர்ந்து சுறுசுறுப்புடன் உழைப்பவனே உலகை ஆள்வான் என்ற அசைக்க முடியாத உழைப்பின் தத்துவத்தை வள்ளுவம் பறைசாற்றுகிறது.

Chapter 61: Madiyinmai (Overcoming Indolence & Cultivating Diligence) from Thirukkural by Thiruvalluvar. Sloth is condemned as the silent poison that destroys noble families and brings ruin, while relentless industrious effort conquers even adversity.

⏱️ Timestamps / Chapters:
00:00 - அதிகாலை உழைப்பின் உத்வேகம் (Dawn Energy & Prelude)
00:12 - குறள் 601: குடியென்னும் குன்றா விளக்கம்
00:35 - குறள் 602: மடியை மடியா தொழுகல்
00:58 - குறள் 603: மடிமடிக் கொண்டொழுகும் பேதை
01:21 - குறள் 604: குடிமடிந்து குற்றம் பெருகும்
01:44 - குறள் 605: நெடுநீர் மறவி மடிதுயில்
02:08 - குறள் 606: படியுடையார் பற்றமைந்தக் கண்ணும்
02:31 - குறள் 607: இடிபுரிந்து எள்ளுஞ்சொல் கேட்பர்
02:54 - குறள் 608: மடிமை குடிமைக்கண் பட்டால்
03:17 - குறள் 609: குடியாண்மை யுள்வந்த குற்றம்
03:40 - குறள் 610: மடியிலா மன்னவன் எய்தும்
04:03 - உழைப்பின் வெற்றிப் பேரொளி (Outro & Grand Cadence)

═════════════════════════════════════════════════════════════════
📜 அதிகாரம் 61: மடியின்மை — முழுப் பாடல் வரிகளும் உரையும் (Kurals 601-610)
═════════════════════════════════════════════════════════════════
{full_kurals_text}

═════════════════════════════════════════════════════════════════
🎵 Credits & Release Info:
• Track: அதிகாரம் 61 - மடியின்மை (Original Master)
• Channel: Guru Kula Desam (@guru-kula-desam)
• Production & Vocals: Nagarajan Balasubramanian
• Audio Master: https://www.youtube.com/watch?v=GfGlO3RQuik
• Thirukkural Master Collection: https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro

#திருக்குறள் #மடியின்மை #Thirukkural #Madiyinmai #HardWork #Diligence #OvercomingLaziness #TamilHeritage #GuruKulaDesam #Motivation #SuccessMindset

— குரு குல தேசம் | Guru Kula Desam
https://gurukuladesam.com
"""

print(f"Constructed description length: {len(desc)} characters (Limit: 5000)")

# Connect to YouTube API
token_path = ROOT / 'data/credentials/token_backup_guru-kula-desam.json'
creds = Credentials.from_authorized_user_file(str(token_path))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# 1. Update Video Description
print(f"Updating video description on YouTube for {VID}...")
v_obj = yt.videos().list(part='snippet', id=VID).execute()['items'][0]
v_snippet = v_obj['snippet']
v_snippet['description'] = desc

yt.videos().update(
    part='snippet',
    body={
        'id': VID,
        'snippet': v_snippet
    }
).execute()
print("SUCCESS: Live video description updated on YouTube!")

# 2. Update/Replace Caption Track
srt_file = ROOT / 'production/subtitles/Mata6vtnrjQ.srt'
print(f"Updating subtitle track using {srt_file}...")

caps = yt.captions().list(part='snippet', videoId=VID).execute()
for c in caps.get('items', []):
    cid = c['id']
    clang = c['snippet']['language']
    cname = c['snippet']['name']
    print(f"Deleting old caption track: {cid} ({clang} - {cname})...")
    yt.captions().delete(id=cid).execute()
    print("Old track deleted.")

print("Uploading new 10-Kural caption track...")
media = MediaFileUpload(str(srt_file), mimetype='application/x-subrip', resumable=True)
new_cap = yt.captions().insert(
    part='snippet',
    body={
        'snippet': {
            'videoId': VID,
            'language': 'ta',
            'name': 'தமிழ் பாடல் வரிகள் (Tamil Lyrics)',
            'isDraft': False
        }
    },
    media_body=media
).execute()
print(f"SUCCESS: Uploaded new caption track {new_cap.get('id')}!")

# 3. Verification download
print("Verifying uploaded caption by downloading directly from YouTube...")
downloaded = yt.captions().download(id=new_cap['id']).execute().decode('utf-8')
print("--- Downloaded Caption from YouTube ---")
print(downloaded)
print(f"Total downloaded length: {len(downloaded)} chars")
