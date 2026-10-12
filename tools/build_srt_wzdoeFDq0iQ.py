# -*- coding: utf-8 -*-
"""
tools/build_srt_wzdoeFDq0iQ.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 56 - கொடுங்கோன்மை
YouTube ID: wzdoeFDq0iQ
Suno Track: 34fad2d1-6083-48a5-b4ce-6986b8f4ca68 (கொடுங்கோன்மை 1C Golden)
Duration: 275.3s (4m 35s)
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
        "start": 3.0,
        "end": 20.0,
        "text": "திருக்குறள் — அதிகாரம் 56: கொடுங்கோன்மை (Kodungonmai / Cruel Tyranny)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 21.0,
        "end": 39.5,
        "text": "[பல்லவி / Chorus]\nமுறைகோடி மன்னவன் செய்யின் (உறைகோடி)\nஒல்லாது வானம் பெயல் (குறள் 559)"
    },
    {
        "start": 40.0,
        "end": 58.0,
        "text": "முறைகோடி மன்னவன் செய்யின் (உறைகோடி)\nஒல்லாது வானம் பெயல் (குறள் 559)"
    },
    # [Verse 1]
    {
        "start": 58.5,
        "end": 74.0,
        "text": "[சரணம் 1 / Verse 1]\nமன்னர்க்கு மன்னுதல் செங்கோன்மை (அஃதின்றேல்)\nமன்னாவாம் மன்னர்க் கொளி (குறள் 556)"
    },
    {
        "start": 74.5,
        "end": 88.0,
        "text": "மன்னர்க்கு மன்னுதல் செங்கோன்மை (அஃதின்றேல்)\nமன்னாவாம் மன்னர்க் கொளி (குறள் 556)"
    },
    {
        "start": 88.5,
        "end": 96.0,
        "text": "இன்மையின் இன்னாது உடைமை (முறைசெய்யா)\nமன்னவன் கோற்கீழ்ப் படின் (குறள் 558)"
    },
    {
        "start": 96.5,
        "end": 105.0,
        "text": "இன்மையின் இன்னாது உடைமை (முறைசெய்யா)\nமன்னவன் கோற்கீழ்ப் படின் (குறள் 558)"
    },
    # [Chorus Reprise 1]
    {
        "start": 105.5,
        "end": 117.0,
        "text": "[பல்லவி / Chorus Reprise]\nமுறைகோடி மன்னவன் செய்யின் (உறைகோடி)\nஒல்லாது வானம் பெயல் (குறள் 559)"
    },
    {
        "start": 117.5,
        "end": 130.0,
        "text": "முறைகோடி மன்னவன் செய்யின் (உறைகோடி)\nஒல்லாது வானம் பெயல் (குறள் 559)"
    },
    # [Bridge]
    {
        "start": 140.0,
        "end": 150.5,
        "text": "[சரணம் 2 / Bridge]\nஆபயன் குன்றும் அறுதொழிலோர் (நூல்மறப்பர்)\nகாவலன் காவான் எனின் (குறள் 560)"
    },
    {
        "start": 151.0,
        "end": 165.5,
        "text": "துளியின்மை ஞாலத்திற்கு எற்றற்றே (வேந்தன்)\nஅளியின்மை வாழும் உயிர்க்கு (குறள் 557)"
    },
    {
        "start": 166.0,
        "end": 175.5,
        "text": "அல்லற்பட்டு ஆற்றாது அழுதகண் (நீரன்றே)\nசெல்வத்தைத் தேய்க்கும் படை (குறள் 555)"
    },
    # [Chorus Reprise 2]
    {
        "start": 176.0,
        "end": 192.0,
        "text": "[பல்லவி / Chorus Reprise]\nமுறைகோடி மன்னவன் செய்யின் (உறைகோடி)\nஒல்லாது வானம் பெயல் (குறள் 559)"
    },
    # [Verse 2]
    {
        "start": 193.0,
        "end": 208.0,
        "text": "[சரணம் 3 / Verse 3]\nகூழுங் குடியும் ஒருங்கிழக்கும் (கோல்கோடிச்)\nசூழாது செய்யும் அரசு (குறள் 554)"
    },
    {
        "start": 208.5,
        "end": 219.0,
        "text": "வேலொடு நின்றான் இடுவென் (றதுபோலும்)\nகோலொடு நின்றான் இரவு (குறள் 552)"
    },
    {
        "start": 219.5,
        "end": 232.0,
        "text": "கொலைமேற்கொண் டாரிற் கொடிதே (அலைமேற்கொண்டு)\nஅல்லவை செய்தொழுகும் வேந்து (குறள் 551)"
    },
    {
        "start": 232.5,
        "end": 248.0,
        "text": "நாடொறும் நாடி முறைசெய்யா (மன்னவன்)\nநாடொறும் நாடு கெடும் (குறள் 553)"
    },
    # [Grand Chorus Finale]
    {
        "start": 248.5,
        "end": 260.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nமுறைகோடி மன்னவன் செய்யின் (உறைகோடி)\nஒல்லாது வானம் பெயல் (குறள் 559)"
    },
    {
        "start": 260.5,
        "end": 274.0,
        "text": "முறைகோடி மன்னவன் செய்யின் (உறைகோடி)\nஒல்லாது வானம் பெயல் (குறள் 559)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/wzdoeFDq0iQ.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "wzdoeFDq0iQ"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
