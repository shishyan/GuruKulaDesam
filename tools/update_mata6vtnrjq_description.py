import os, sys, json
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('data/credentials/token_backup_guru-kula-desam.json')
yt = build('youtube', 'v3', credentials=creds)

vid = 'Mata6vtnrjQ'
res = yt.videos().list(part='snippet', id=vid).execute()
item = res['items'][0]
snip = item['snippet']
desc = snip['description']

old_chapter_block_start = "⏱ Timestamps / Chapters:"
old_chapter_block_end = "======================================================================"

new_chapter_block = """⏱ Timestamps / Musical Chapters (அமைப்பும் நேரமும்):
00:00 - குறள் 610: மடியிலா மன்னவன் எய்தும் (தொடக்கப் பல்லவி)
00:30 - குறள் 601: குடியென்னும் குன்றா விளக்கம்
01:00 - குறள் 610: அடியளந்தான் தாஅய தெல்லாம் (பல்லவி)
01:31 - குறள் 609: குடியாண்மை யுள்வந்த குற்றம்
02:01 - குறள் 602: மடியை மடியா ஒழுகல்
02:16 - குறள் 604: குடிமடிந்து குற்றம் பெருகும்
02:31 - குறள் 610: மடியிலா மன்னவன் எய்தும் (இடைக்காலப் பல்லவி)
03:01 - குறள் 605: நெடுநீர் மறவி மடிதுயில் நான்கும்
03:12 - குறள் 607: இடிபுரிந்து எள்ளுஞ்சொல் கேட்பர் & குறள் 603: மடிமடிக் கொண்டொழுகும்
03:24 - குறள் 608: மடிமை குடிமைக்கண் தங்கின்தன்
03:36 - குறள் 606: படியுடையார் பற்றமைந்தக் கண்ணும்
03:44 - குறள் 610: அடியளந்தான் தாஅய தெல்லாம் ஒருங்கு (நிறைவுப் பல்லவி)"""

if old_chapter_block_start in desc and old_chapter_block_end in desc:
    p1 = desc.split(old_chapter_block_start)[0]
    p2 = desc.split(old_chapter_block_end, 1)[1]
    new_desc = p1 + new_chapter_block + "\n\n" + old_chapter_block_end + p2
else:
    print("Could not find delimiters. Replacing chapters by lines...")
    lines = desc.splitlines()
    new_lines = []
    skip = False
    for line in lines:
        if "⏱ Timestamps" in line:
            new_lines.append(new_chapter_block)
            skip = True
        elif skip and ("====" in line or "குறள் 601:" in line):
            skip = False
            new_lines.append(line)
        elif not skip:
            new_lines.append(line)
    new_desc = "\n".join(new_lines)

snip['description'] = new_desc

update_res = yt.videos().update(
    part='snippet',
    body={
        'id': vid,
        'snippet': snip
    }
).execute()

print("SUCCESS! Updated description on YouTube with acoustically verified timestamps!")
print("New Description length:", len(update_res['snippet']['description']))
