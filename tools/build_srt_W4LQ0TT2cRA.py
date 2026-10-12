# -*- coding: utf-8 -*-
"""
tools/build_srt_W4LQ0TT2cRA.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 73 - அவையஞ்சாமை
YouTube ID: W4LQ0TT2cRA
Audio Duration: 238.52s (3m 58s)
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
        "text": "திருக்குறள் — அதிகாரம் 73: அவையஞ்சாமை (Not Dreading the Council / Fearlessness in Assembly)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 21.0,
        "end": 33.0,
        "text": "[பல்லவி / Chorus]\nகல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    {
        "start": 33.5,
        "end": 48.0,
        "text": "கல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    # [Verse 1]
    {
        "start": 81.0,
        "end": 90.5,
        "text": "[சரணம் 1 / Verse 1]\nவகையறிந்து வல்லவை வாய்சோரார் சொல்லின்\nதொகையறிந்த தூய்மை யவர் (குறள் 721)"
    },
    {
        "start": 91.0,
        "end": 100.5,
        "text": "வகையறிந்து வல்லவை வாய்சோரார் சொல்லின்\nதொகையறிந்த தூய்மை யவர் (குறள் 721)"
    },
    # [Chorus Reprise 1]
    {
        "start": 101.0,
        "end": 113.0,
        "text": "[பல்லவி / Chorus Reprise]\nகல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    {
        "start": 113.5,
        "end": 126.5,
        "text": "கல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    # [Verse 2]
    {
        "start": 137.0,
        "end": 154.0,
        "text": "[சரணம் 2 / Verse 2]\nகற்றாருள் கற்றார் எனப்படுவர் கற்றார்முன்\nகற்ற செலச்சொல்லு வார் (குறள் 722)\nபகையகத்துச் சாவார் எளியர் அரியர் அவையகத்து அஞ்சா தவர் (குறள் 723)"
    },
    {
        "start": 154.5,
        "end": 164.5,
        "text": "கற்றார்முன் கற்ற செலச்சொல்லித் தாம்கற்ற\nமிக்காருள் மிக்க கொளல் (குறள் 724)\nஆற்றின் அளவறிந்து கற்க அவையஞ்சா மாற்றங் கொடுத்தற் பொருட்டு (குறள் 725)"
    },
    # [Verse 3]
    {
        "start": 165.0,
        "end": 178.5,
        "text": "[சரணம் 3 / Verse 3]\nவாளொடென் வன்கண்ணர் அல்லார்க்கு நூலொடென்\nநுண்ணவை அஞ்சு பவர்க்கு (குறள் 726)"
    },
    {
        "start": 179.0,
        "end": 188.5,
        "text": "பகையகத்துப் பேடிகை வாளொக்கும் நற்றேர்\nஅவையகத்து அஞ்சு பவன் (குறள் 727)"
    },
    {
        "start": 189.0,
        "end": 203.0,
        "text": "பல்லவை கற்றும் பயமிலரே நல்லவையுள்\nநன்கு செலச்சொல்லா தார் (குறள் 728)\nஉளரெனினும் இல்லாரோடு ஒப்பர் களனஞ்சிக் கற்ற செலச்சொல்லா தார் (குறள் 729)"
    },
    # [Grand Finale Chorus]
    {
        "start": 203.5,
        "end": 216.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nகல்லாதவரின் கடைஎன்ப கற்றறிந்து\nநல்லார் அவையஞ்சு வார் (குறள் 730)"
    },
    {
        "start": 216.5,
        "end": 235.0,
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
out_srt = "production/subtitles/W4LQ0TT2cRA.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "W4LQ0TT2cRA"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
