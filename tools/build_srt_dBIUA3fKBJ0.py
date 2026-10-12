# -*- coding: utf-8 -*-
"""
tools/build_srt_dBIUA3fKBJ0.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 71 - குறிப்பறிதல்
YouTube ID: dBIUA3fKBJ0
Suno Track: 54b95b60-ffc2-4bb9-84f7-a4b204997d3d (குறிப்பறிதல் 1J Golden)
Duration: 274.32s (4m 34s)
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
        "end": 21.0,
        "text": "திருக்குறள் — அதிகாரம் 71: குறிப்பறிதல் (Kuripparithal / Reading the Signs)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 22.0,
        "end": 33.5,
        "text": "[பல்லவி / Chorus]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    # [Verse 1]
    {
        "start": 34.0,
        "end": 45.5,
        "text": "[சரணம் 1 / Verse 1]\nமுகம்நோக்கி நிற்க அமையும் (அகம்நோக்கி)\nஉற்றது உணர்வார்ப் பெறின் (குறள் 702)"
    },
    {
        "start": 46.0,
        "end": 67.0,
        "text": "கூறாமை நோக்கி குறிப்பறிவான் (எஞ்ஞான்றும்)\nமாறாநீர் வையக் கணி (குறள் 701)"
    },
    # [Chorus Reprise 1]
    {
        "start": 68.0,
        "end": 89.0,
        "text": "[பல்லவி / Chorus Reprise]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    {
        "start": 89.5,
        "end": 102.0,
        "text": "அடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    # [Verse 2]
    {
        "start": 103.0,
        "end": 118.0,
        "text": "[சரணம் 2 / Verse 2]\nநுண்ணியம் என்பார் அளக்குங்கோல் (காணுங்கால்)\nகண்ணல்லது இல்லை பிற (குறள் 710)"
    },
    {
        "start": 118.5,
        "end": 132.0,
        "text": "ஐயப் படாஅது அகத்தது (உணர்வானை)\nதெய்வத்தோடு ஒப்பக் கொளல் (குறள் 703)"
    },
    {
        "start": 132.5,
        "end": 149.0,
        "text": "முகத்தின் முதுக்குறைந்தது உண்டோ (உவப்பினும்)\nகாயினும் தான்முந் துறும் (குறள் 707)"
    },
    # [Chorus Reprise 2]
    {
        "start": 150.0,
        "end": 166.0,
        "text": "[பல்லவி / Chorus Reprise]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    # [Verse 3]
    {
        "start": 196.0,
        "end": 203.0,
        "text": "[சரணம் 3 / Verse 3]\nபகைமையும் கேண்மையும் கண்ணுரைக்கும் (கண்ணின்)\nவகைமை உணர்வார்ப் பெறின் (குறள் 709)"
    },
    {
        "start": 203.5,
        "end": 214.0,
        "text": "பகைமையும் கேண்மையும் கண்ணுரைக்கும் (கண்ணின்)\nவகைமை உணர்வார்ப் பெறின் (குறள் 709)"
    },
    {
        "start": 214.5,
        "end": 226.0,
        "text": "குறிப்பிற் குறிப்புணரா வாயின் (உறுப்பினுள்)\nஎன்ன பயத்தவோ கண் (குறள் 705)"
    },
    {
        "start": 226.5,
        "end": 242.0,
        "text": "குறித்தது கூறாமைக் கொள்வாரோடு (ஏனை)\nஉறுப்போ ரனையரால் வேறு (குறள் 704)"
    },
    # [Grand Finale Chorus]
    {
        "start": 242.5,
        "end": 258.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    {
        "start": 258.5,
        "end": 274.0,
        "text": "அடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/dBIUA3fKBJ0.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "dBIUA3fKBJ0"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
