# -*- coding: utf-8 -*-
"""
tools/build_srt_mCwNR1Bytj4.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 39 - இறைமாட்சி
YouTube ID: mCwNR1Bytj4
Suno Track: 103fafbd-15df-449d-be9e-b5cc3dbf4262 (இறைமாட்சி 1M Golden Remastered)
Duration: 227.79s (3m 47s)
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
        "text": "திருக்குறள் — அதிகாரம் 39: இறைமாட்சி (Iraimaatchi / The Greatness of a King)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 29.0,
        "end": 45.0,
        "text": "[பல்லவி / Chorus]\nமுறைசெய்து காப்பாற்றும் மன்னவன் (மக்கட்கு)\nஇறையென்று வைக்கப் படும் (குறள் 388)"
    },
    # [Verse 1]
    {
        "start": 46.0,
        "end": 60.0,
        "text": "[சரணம் 1 / Verse 1]\nஅஞ்சாமை ஈகை அறிவூக்கம் (இந்நான்கும்)\nஎஞ்சாமை வேந்தர்க்கு இயல்பு (குறள் 382)"
    },
    {
        "start": 60.5,
        "end": 78.0,
        "text": "படைகுடி கூழ் அமைச்சு நட்பரண் (ஆறும்)\nஉடையான் அரசருள் ஏறு (குறள் 381)"
    },
    {
        "start": 78.5,
        "end": 89.5,
        "text": "அறனிழுக்காது அல்லவை நீக்கி (மறனிழுக்கா)\nமானம் உடையது அரசு (குறள் 384)"
    },
    {
        "start": 90.0,
        "end": 99.0,
        "text": "இயற்றலும் ஈட்டலும் காத்தலும் (காத்த)\nவகுத்தலும் வல்லது அரசு (குறள் 385)"
    },
    # [Chorus Reprise 1]
    {
        "start": 99.5,
        "end": 112.5,
        "text": "[பல்லவி / Chorus Reprise]\nமுறைசெய்து காப்பாற்றும் மன்னவன் (மக்கட்கு)\nஇறையென்று வைக்கப் படும் (குறள் 388)"
    },
    {
        "start": 113.0,
        "end": 128.0,
        "text": "அஞ்சாமை ஈகை அறிவூக்கம் (இந்நான்கும்)\nஎஞ்சாமை வேந்தர்க்கு இயல்பு (குறள் 382)"
    },
    # [Verse 2]
    {
        "start": 149.0,
        "end": 156.0,
        "text": "[சரணம் 2 / Verse 2]\nதூங்காமை கல்வி துணிவுடைமை (இம்மூன்றும்)\nநீங்கா நிலனாள் பவர்க்கு (குறள் 383)"
    },
    {
        "start": 156.5,
        "end": 165.5,
        "text": "காட்சிக்கு எளியன் கடுஞ்சொல்லன் (அல்லனேல்)\nமீக்கூறும் மன்னன் நிலம் (குறள் 386)"
    },
    {
        "start": 166.0,
        "end": 178.0,
        "text": "இன்சொலால் ஈத்தளிக்க வல்லார்க்குத் (தன்சொலால்)\nதான்கண்ட அனைத்து இவ்வுலகு (குறள் 387)"
    },
    {
        "start": 178.5,
        "end": 190.0,
        "text": "செவிகைப்பச் சொற்பொறுக்கும் பண்புடை (வேந்தன்)\nகவிகைக்கீழ்த் தங்கும் உலகு (குறள் 389)"
    },
    {
        "start": 190.5,
        "end": 204.0,
        "text": "கொடையளி செங்கோல் குடியோம்பல் (நான்கும்)\nஉடையானாம் வேந்தர்க்கு ஒளி (குறள் 390)"
    },
    # [Grand Finale Chorus]
    {
        "start": 205.0,
        "end": 215.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nமுறைசெய்து காப்பாற்றும் மன்னவன் (மக்கட்கு)\nஇறையென்று வைக்கப் படும் (குறள் 388)"
    },
    {
        "start": 215.5,
        "end": 226.0,
        "text": "அஞ்சாமை ஈகை அறிவூக்கம் (இந்நான்கும்)\nஎஞ்சாமை வேந்தர்க்கு இயல்பு (குறள் 382)\nமுறைசெய்து காப்பாற்றும் மன்னவன் மக்கட்கு இறையென்று வைக்கப் படும்"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/mCwNR1Bytj4.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "mCwNR1Bytj4"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
