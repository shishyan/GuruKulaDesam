# -*- coding: utf-8 -*-
"""
tools/build_srt_fRNAsDZr3QA.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 32 - இன்னா செய்யாமை
YouTube ID: fRNAsDZr3QA
Duration: 479.58s (7m 59s)
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
        "text": "திருக்குறள் — அதிகாரம் 32: இன்னா செய்யாமை (Not Doing Evil / Kindness Story)\n[செவ்வியல் திரை இசை / Classical Devotional Story Film]"
    },
    # [Chorus 1]
    {
        "start": 29.0,
        "end": 45.0,
        "text": "[பல்லவி / Chorus]\nஇன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    {
        "start": 45.5,
        "end": 75.0,
        "text": "இன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    # [Verse 1]
    {
        "start": 76.0,
        "end": 104.0,
        "text": "[சரணம் 1 / Verse 1]\nஅறிவினான் ஆகுவ துண்டோ பிறிதின்நோய்\nதந்நோய்போல் போற்றாக் கடை (குறள் 315)"
    },
    {
        "start": 104.5,
        "end": 118.0,
        "text": "அறிவினான் ஆகுவ துண்டோ பிறிதின்நோய்\nதந்நோய்போல் போற்றாக் கடை (குறள் 315)"
    },
    # [Chorus Reprise 1]
    {
        "start": 118.5,
        "end": 131.0,
        "text": "[பல்லவி / Chorus Reprise]\nஇன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    {
        "start": 131.5,
        "end": 150.0,
        "text": "இன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    # [Verse 2]
    {
        "start": 156.0,
        "end": 169.0,
        "text": "[சரணம் 2 / Verse 2]\nசெய்யாமல் செற்றார்க்கும் இன்னாத செய்தபின்\nஉய்யா விழுமந் தரும் (குறள் 313)"
    },
    {
        "start": 169.5,
        "end": 180.0,
        "text": "செய்யாமல் செற்றார்க்கும் இன்னாத செய்தபின்\nஉய்யா விழுமந் தரும் (குறள் 313)"
    },
    {
        "start": 180.5,
        "end": 207.0,
        "text": "சிறப்பீனும் செல்வம் பெறினும் பிறர்க்குஇன்னா\nசெய்யாமை மாசற்றார் கோள் (குறள் 311)"
    },
    # [Chorus Reprise 2]
    {
        "start": 207.5,
        "end": 225.0,
        "text": "[பல்லவி / Chorus Reprise]\nஇன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    # [Verse 3]
    {
        "start": 250.0,
        "end": 263.0,
        "text": "[சரணம் 3 / Verse 3]\nஇன்னா எனத்தான் உணர்ந்தவை துன்னாமை\nவேண்டும் பிறன்கண் செயல் (குறள் 316)"
    },
    {
        "start": 263.5,
        "end": 275.0,
        "text": "கறுத்துஇன்னா செய்தவக் கண்ணும் மறுத்தின்னா\nசெய்யாமை மாசற்றார் கோள் (குறள் 312)"
    },
    {
        "start": 275.5,
        "end": 288.0,
        "text": "பிறர்க்கின்னா முற்பகல் செய்யின் தமக்குஇன்னா\nபிற்பகல் தாமே வரும் (குறள் 319)"
    },
    {
        "start": 288.5,
        "end": 300.0,
        "text": "நோயெல்லாம் நோய்செய்தார் மேலவாம் நோய்செய்யார்\nநோயின்மை வேண்டு பவர் (குறள் 320)"
    },
    # [Chorus Reprise 3]
    {
        "start": 300.5,
        "end": 326.0,
        "text": "[பல்லவி / Chorus Reprise]\nஇன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    # [Verse 4]
    {
        "start": 359.0,
        "end": 376.0,
        "text": "[சரணம் 4 / Verse 4]\nதன்னுயிர்க்கு இன்னாமை தானறிவான் என்கொலோ\nமன்னுயிர்க்கு இன்னா செயல் (குறள் 318)"
    },
    {
        "start": 377.0,
        "end": 402.0,
        "text": "எனைத்தானும் எஞ்ஞான்றும் யார்க்கும் மனத்தானாம்\nமாணாசெய் யாமை தலை (குறள் 317)"
    },
    # [Grand Finale Chorus]
    {
        "start": 403.0,
        "end": 421.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nஇன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    {
        "start": 421.5,
        "end": 441.0,
        "text": "இன்னாசெய்தாரை ஒறுத்தல் அவர்நாண\nநன்னயஞ் செய்து விடல் (குறள் 314)"
    },
    {
        "start": 442.0,
        "end": 479.0,
        "text": "அறிவினான் ஆகுவ துண்டோ பிறிதின்நோய் தந்நோய்போல் போற்றாக் கடை (குறள் 315)\nஇன்னாசெய்தாரை ஒறுத்தல் அவர்நாண நன்னயஞ் செய்து விடல் (குறள் 314)\n[நிறைவு / Grand Musical Outro]"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/fRNAsDZr3QA.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "fRNAsDZr3QA"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
