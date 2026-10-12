# -*- coding: utf-8 -*-
"""
tools/build_srt_HRN77i6Kio8.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 45 - பெரியாரைத் துணைக்கோடல்
YouTube ID: HRN77i6Kio8
Suno Track: 4575ad0d-1fc2-47a2-b962-179ea5c54918 (பெரியாரைத் துணைக்கோடல் 1O Golden Pop)
Duration: 262.94s (4m 23s)
"""

import sys, json, os, subprocess

sys.stdout.reconfigure(encoding='utf-8')

def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

cues = [
    {
        "start": 2.0,
        "end": 20.0,
        "text": "திருக்குறள் — அதிகாரம் 45: பெரியாரைத் துணைக்கோடல் (Seeking the Aid of Great Men)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 21.0,
        "end": 35.5,
        "text": "[பல்லவி / Chorus]\nஅரியவற்றுள் எல்லாம் அரிதே (பெரியாரை)\nபேணித் தமராக் கொளல் (குறள் 443)"
    },
    # [Verse 1]
    {
        "start": 36.0,
        "end": 50.5,
        "text": "[சரணம் 1 / Verse 1]\nமுதலிலார்க்கு ஊதியம் இல்லை (மதலையாம்)\nசார்பிலார்க்கு இல்லை நிலை (குறள் 449)"
    },
    {
        "start": 51.0,
        "end": 68.0,
        "text": "அறனறிந்து மூத்த அறிவுடையார் (கேண்மை)\nதிறனறிந்து தேர்ந்து கொளல் (குறள் 441)"
    },
    {
        "start": 68.5,
        "end": 80.0,
        "text": "முதலிலார்க்கு ஊதியம் இல்லை (மதலையாம்)\nசார்பிலார்க்கு இல்லை நிலை (குறள் 449)"
    },
    # [Chorus Reprise 1]
    {
        "start": 81.0,
        "end": 109.0,
        "text": "[பல்லவி / Chorus Reprise]\nஅரியவற்றுள் எல்லாம் அரிதே (பெரியாரை)\nபேணித் தமராக் கொளல் (குறள் 443)"
    },
    {
        "start": 109.5,
        "end": 123.5,
        "text": "அரியவற்றுள் எல்லாம் அரிதே (பெரியாரை)\nபேணித் தமராக் கொளல் (குறள் 443)"
    },
    # [Verse 2]
    {
        "start": 124.0,
        "end": 141.5,
        "text": "[சரணம் 2 / Verse 2]\nதம்மின் பெரியார் தமரா (ஒழுகுதல்)\nவன்மையுள் எல்லாம் தலை (குறள் 444)"
    },
    {
        "start": 142.0,
        "end": 153.0,
        "text": "இடிக்கும் துணையாரை ஆள்வாரை (யாரே)\nகெடுக்கும் தகைமை அவர் (குறள் 447)"
    },
    {
        "start": 153.5,
        "end": 167.0,
        "text": "இடிப்பாரை இல்லாத ஏமரா (மன்னன்)\nகெடுப்பார் இலானும் கெடும் (குறள் 448)"
    },
    # [Chorus Reprise 2]
    {
        "start": 168.0,
        "end": 196.0,
        "text": "[பல்லவி / Chorus Reprise]\nஅரியவற்றுள் எல்லாம் அரிதே (பெரியாரை)\nபேணித் தமராக் கொளல் (குறள் 443)"
    },
    # [Verse 3 / Bridge]
    {
        "start": 198.0,
        "end": 204.0,
        "text": "[சரணம் 3 / Verse 3]\nசூழ்வார் கண்ணாக ஒழுகலான் (மன்னவன்)\nசூழ்வாரைச் சூழ்ந்து கொளல் (குறள் 445)"
    },
    {
        "start": 204.5,
        "end": 211.5,
        "text": "உற்றநோய் நீக்கி உறாஅமை (முற்காக்கும்)\nபெற்றியார் பேணிக் கொளல் (குறள் 442)"
    },
    {
        "start": 212.0,
        "end": 220.0,
        "text": "தக்கார் இனத்தனாய் தானொழுக (வல்லானை)\nசெற்றார் செயக்கிடந்தது இல் (குறள் 446)"
    },
    {
        "start": 220.5,
        "end": 232.0,
        "text": "பல்லார் பகைகொளலின் பத்தடுத்த (தீமைத்தே)\nநல்லார் தொடர்கை விடல் (குறள் 450)"
    },
    # [Grand Finale Chorus]
    {
        "start": 233.0,
        "end": 262.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nஅரியவற்றுள் எல்லாம் அரிதே (பெரியாரை)\nபேணித் தமராக் கொளல் (குறள் 443)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/HRN77i6Kio8.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "HRN77i6Kio8"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
