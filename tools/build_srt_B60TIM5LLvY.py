# -*- coding: utf-8 -*-
"""
tools/build_srt_B60TIM5LLvY.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 44 - குற்றங்கடிதல்
YouTube ID: B60TIM5LLvY
Suno Track: 4994325b-7c8c-4381-8282-d555542dc829 (குற்றம் கடிதல் 1M Golden)
Duration: 233.73s (3m 53s)
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
        "text": "திருக்குறள் — அதிகாரம் 44: குற்றங்கடிதல் (Correction of Faults)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 21.0,
        "end": 45.0,
        "text": "[பல்லவி / Chorus]\nவருமுன்னர் காவாதான் வாழ்க்கை (எரிமுன்னர்)\nவைத்தூறு போலக் கெடும் (குறள் 435)"
    },
    # [Verse 1]
    {
        "start": 46.0,
        "end": 64.0,
        "text": "[சரணம் 1 / Verse 1]\nதன்குற்றம் நீக்கிப் பிறர்குற்றம் (காண்கிற் பின்)\nஎன்குற்றம் ஆகும் இறைக்கு (குறள் 436)"
    },
    {
        "start": 64.5,
        "end": 85.0,
        "text": "செயற்பால செய்யாது இவறியான் (செல்வம்)\nஉயற்பாலது அன்றிக் கெடும் (குறள் 437)"
    },
    # [Chorus Reprise 1]
    {
        "start": 85.5,
        "end": 105.0,
        "text": "[பல்லவி / Chorus Reprise]\nவருமுன்னர் காவாதான் வாழ்க்கை (எரிமுன்னர்)\nவைத்தூறு போலக் கெடும் (குறள் 435)"
    },
    # [Verse 2]
    {
        "start": 115.0,
        "end": 128.0,
        "text": "[சரணம் 2 / Verse 2]\nசெருக்கும் சினமும் சிறுமையும் (இல்லார்)\nபெருக்கம் பெருமித நீர்த்து (குறள் 431)"
    },
    {
        "start": 128.5,
        "end": 140.0,
        "text": "இவறலும் மாண்பிறந்த மானமும் (மாணா)\nஉவகையும் ஏதம் இறைக்கு (குறள் 432)"
    },
    {
        "start": 140.5,
        "end": 148.0,
        "text": "குற்றமே காக்க பொருளாக (குற்றமே)\nஅற்றம் தரூஉம் பகை (குறள் 434)"
    },
    {
        "start": 148.5,
        "end": 156.0,
        "text": "தினைத்துணையாம் குற்றம் வரினும் (பனைத்துணையாக)\nகொள்வர் பழி நாணுவார் (குறள் 433)"
    },
    # [Chorus Reprise 2]
    {
        "start": 156.5,
        "end": 178.0,
        "text": "[பல்லவி / Chorus Reprise]\nவருமுன்னர் காவாதான் வாழ்க்கை (எரிமுன்னர்)\nவைத்தூறு போலக் கெடும் (குறள் 435)"
    },
    # [Verse 3]
    {
        "start": 179.0,
        "end": 195.0,
        "text": "[சரணம் 3 / Verse 3]\nவியவற்க எஞ்ஞான்றும் தன்னை (நயவற்க)\nநன்றி பயவா வினை (குறள் 439)"
    },
    {
        "start": 195.5,
        "end": 204.0,
        "text": "பற்றுள்ளம் என்னும் இவறன்மை (எற்றுள்ளும்)\nஎண்ணப்படுவது ஒன்று அன்று (குறள் 438)"
    },
    {
        "start": 204.5,
        "end": 212.0,
        "text": "காதல காதல் அறியாமை (உய்க்கிற்பின்)\nஏதில ஏதிலார் நூல் (குறள் 440)"
    },
    # [Grand Finale Chorus]
    {
        "start": 212.5,
        "end": 222.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nவருமுன்னர் காவாதான் வாழ்க்கை (எரிமுன்னர்)\nவைத்தூறு போலக் கெடும் (குறள் 435)"
    },
    {
        "start": 222.5,
        "end": 233.0,
        "text": "வருமுன்னர் காவாதான் வாழ்க்கை (எரிமுன்னர்)\nவைத்தூறு போலக் கெடும் (குறள் 435)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/B60TIM5LLvY.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "B60TIM5LLvY"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
