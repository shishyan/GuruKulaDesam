# -*- coding: utf-8 -*-
"""
tools/build_srt_x3CyxNH5bpQ.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 69 - தூது
YouTube ID: x3CyxNH5bpQ
Suno Track: 1aee551b-b608-4409-abb0-2d0ab8f67078 (தூது 1I Golden)
Duration: 251.05s (4m 11s)
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
        "end": 28.0,
        "text": "திருக்குறள் — அதிகாரம் 69: தூது (Thoothu / The Envoy)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 29.0,
        "end": 44.5,
        "text": "[பல்லவி / Chorus]\nகற்றுக்கண் அஞ்சான் செலச்சொல்லிக் (காலத்தால்)\nதக்கது அறிவதாம் தூது (குறள் 684)"
    },
    {
        "start": 45.0,
        "end": 60.0,
        "text": "கற்றுக்கண் அஞ்சான் செலச்சொல்லிக் (காலத்தால்)\nதக்கது அறிவதாம் தூது (குறள் 684)"
    },
    # [Verse 1]
    {
        "start": 60.5,
        "end": 74.0,
        "text": "[சரணம் 1 / Verse 1]\nதொகச்சொல்லித் தூவாத நீக்கி (நகச்சொல்லி)\nநன்றி பயப்பதாந் தூது (குறள் 685)"
    },
    {
        "start": 74.5,
        "end": 85.0,
        "text": "தொகச்சொல்லித் தூவாத நீக்கி (நகச்சொல்லி)\nநன்றி பயப்பதாந் தூது (குறள் 685)"
    },
    {
        "start": 85.5,
        "end": 100.0,
        "text": "அன்புடைமை ஆன்ற குடிப்பிறத்தல் (வேந்தவாம்)\nபண்புடைமை தூதுரைப்பான் பண்பு (குறள் 681)"
    },
    {
        "start": 100.5,
        "end": 115.0,
        "text": "நூலாருள் நூல்வல்லன் ஆகுதல் (வேலாருள்)\nவென்றி வினையுரைப்பான் பண்பு (குறள் 683)"
    },
    # [Chorus Reprise 1]
    {
        "start": 115.5,
        "end": 127.0,
        "text": "[பல்லவி / Chorus Reprise]\nகற்றுக்கண் அஞ்சான் செலச்சொல்லிக் (காலத்தால்)\nதக்கது அறிவதாம் தூது (குறள் 684)"
    },
    {
        "start": 127.5,
        "end": 142.0,
        "text": "கற்றுக்கண் அஞ்சான் செலச்சொல்லிக் (காலத்தால்)\nதக்கது அறிவதாம் தூது (குறள் 684)"
    },
    # [Verse 2 / Bridge]
    {
        "start": 160.0,
        "end": 170.0,
        "text": "[சரணம் 2 / Verse 2]\nதூய்மை துணைமை துணிவுஉடைமை (இம்மூன்றின்)\nவாய்மை வழியுரைப்பான் பண்பு (குறள் 688)"
    },
    {
        "start": 170.5,
        "end": 176.5,
        "text": "கடனறிந்து காலங் கருதி (இடனறிந்து)\nஎண்ணி உரைப்பான் தலை (குறள் 687)"
    },
    {
        "start": 177.0,
        "end": 188.0,
        "text": "அன்பறிவு ஆராய்ந்த சொல்வன்மை (தூதுரைப்பார்க்கு)\nஇன்றி யமையாத மூன்று (குறள் 682)"
    },
    {
        "start": 188.5,
        "end": 201.0,
        "text": "அறிவுரு வாராய்ந்த கல்விஇம் (மூன்றன்)\nசெறிவுடையான் செல்க வினைக்கு (குறள் 689)"
    },
    {
        "start": 201.5,
        "end": 214.0,
        "text": "விடுமாற்றம் வேந்தர்க்கு உரைப்பான் (வடுமாற்றம்)\nவாய்சேரா வன்க ணவன் (குறள் 686)"
    },
    {
        "start": 214.5,
        "end": 226.0,
        "text": "இறுதி பயப்பினும் எஞ்சாது (இறைவற்கு)\nஉறுதி பயப்பதாம் தூது (குறள் 690)"
    },
    # [Grand Finale Chorus]
    {
        "start": 227.0,
        "end": 238.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nகற்றுக்கண் அஞ்சான் செலச்சொல்லிக் (காலத்தால்)\nதக்கது அறிவதாம் தூது (குறள் 684)"
    },
    {
        "start": 238.5,
        "end": 250.0,
        "text": "கற்றுக்கண் அஞ்சான் செலச்சொல்லிக் (காலத்தால்)\nதக்கது அறிவதாம் தூது (குறள் 684)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/x3CyxNH5bpQ.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

# Duplicate also to nR7R0TWyZHk (same track)
with open("production/subtitles/nR7R0TWyZHk.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "x3CyxNH5bpQ"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
