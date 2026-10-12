# -*- coding: utf-8 -*-
"""
tools/build_srt_wyDIU74Rs7Y.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 73 - அவையஞ்சாமை (Female Version)
YouTube ID: wyDIU74Rs7Y
Audio Duration: 227.97s (3m 48s)
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
        "end": 28.0,
        "text": "திருக்குறள் — அதிகாரம் 73: அவையஞ்சாமை (Not Dreading the Council / Female Devotional Rendition)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 29.0,
        "end": 42.0,
        "text": "[பல்லவி / Chorus]\nகல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    {
        "start": 42.5,
        "end": 56.0,
        "text": "கல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    # [Verse 1]
    {
        "start": 56.5,
        "end": 68.0,
        "text": "[சரணம் 1 / Verse 1]\nபகையகத்துப் பேடிகை வாளொக்கும் நற்றேர்\nஅவையகத்து அஞ்சு பவன் (குறள் 727)"
    },
    {
        "start": 68.5,
        "end": 78.0,
        "text": "பகையகத்துச் சாவார் எளியர் அரியர்\nஅவையகத்து அஞ்சா தவர் (குறள் 723)"
    },
    # [Chorus Reprise 1]
    {
        "start": 78.5,
        "end": 105.0,
        "text": "[பல்லவி / Chorus Reprise]\nகல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    # [Verse 2]
    {
        "start": 123.0,
        "end": 145.0,
        "text": "[சரணம் 2 / Verse 2]\nஆற்றின் அளவறிந்து கற்க அவையஞ்சா\nமாற்றங் கொடுத்தற் பொருட்டு (குறள் 725)"
    },
    {
        "start": 145.5,
        "end": 158.0,
        "text": "பல்லவை கற்றும் பயமிலரே நல்லவையுள்\nநன்கு செலச்சொல்லா தார் (குறள் 728)"
    },
    {
        "start": 158.5,
        "end": 174.0,
        "text": "கற்றார்முன் கற்ற செலச்சொல்லித் தாம்கற்ற\nமிக்காருள் மிக்க கொளல் (குறள் 724)\nகற்றாருள் கற்றார் எனப்படுவர் கற்றார்முன் கற்ற செலச்சொல்லு வார் (குறள் 722)"
    },
    # [Verse 3]
    {
        "start": 174.5,
        "end": 184.0,
        "text": "[சரணம் 3 / Verse 3]\nவாளொடென் வன்கண்ணர் அல்லார்க்கு நூலொடென்\nநுண்ணவை அஞ்சு பவர்க்கு (குறள் 726)"
    },
    {
        "start": 184.5,
        "end": 194.5,
        "text": "உளரெனினும் இல்லாரோடு ஒப்பர் களனஞ்சிக்\nகற்ற செலச்சொல்லா தார் (குறள் 729)"
    },
    # [Grand Finale Chorus]
    {
        "start": 195.0,
        "end": 209.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nகல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    {
        "start": 209.5,
        "end": 226.0,
        "text": "கல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/wyDIU74Rs7Y.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "wyDIU74Rs7Y"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
