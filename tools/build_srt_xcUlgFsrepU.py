# -*- coding: utf-8 -*-
"""
tools/build_srt_xcUlgFsrepU.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 31 - வெகுளாமை
YouTube ID: xcUlgFsrepU
Suno Track: c6c3096d-fa6a-48fb-a9a1-603133162a8c (திருக்குறள் - வெகுளாமை 2026)
Duration: 324.94s (5m 25s)
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
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 31: வெகுளாமை (Vegulaamai / Not Harboring Anger)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 15.0,
        "end": 29.0,
        "text": "[பல்லவி / Chorus]\nதன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    },
    {
        "start": 29.5,
        "end": 47.0,
        "text": "தன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    },
    # [Verse 1]
    {
        "start": 48.0,
        "end": 63.5,
        "text": "[சரணம் 1 / Verse 1]\nசெல்லா இடத்துச் சினந்தீது (செல்லிடத்தும்)\nஇல்அதனின் தீய பிற (குறள் 301)"
    },
    {
        "start": 64.0,
        "end": 77.5,
        "text": "செல்லிடத்துக் காப்பான் சினங்காப்பான் (அல்லிடத்துக்)\nகாக்கினென் காவாக்கால் என் (குறள் 302)"
    },
    {
        "start": 78.0,
        "end": 92.5,
        "text": "செல்லா இடத்துச் சினந்தீது (செல்லிடத்தும்)\nஇல்அதனின் தீய பிற (குறள் 301)"
    },
    {
        "start": 93.0,
        "end": 108.0,
        "text": "செல்லிடத்துக் காப்பான் சினங்காப்பான் (அல்லிடத்துக்)\nகாக்கினென் காவாக்கால் என் (குறள் 302)"
    },
    # [Chorus Reprise 1]
    {
        "start": 115.0,
        "end": 125.0,
        "text": "[பல்லவி / Chorus Reprise]\nதன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    },
    {
        "start": 125.5,
        "end": 140.0,
        "text": "தன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    },
    # [Verse 2]
    {
        "start": 141.5,
        "end": 156.0,
        "text": "[சரணம் 2 / Verse 2]\nநகையும் உவகையும் கொல்லும் (சினத்தின்)\nபகையும் உளவோ பிற (குறள் 304)"
    },
    {
        "start": 156.5,
        "end": 173.0,
        "text": "நகையும் உவகையும் கொல்லும் (சினத்தின்)\nபகையும் உளவோ பிற (குறள் 304)"
    },
    {
        "start": 173.5,
        "end": 189.0,
        "text": "சினத்தைப் பொருளென்று கொண்டவன் (கேடு)\nநிலத்தறைந்தான் கைபிழையா தற்று (குறள் 307)"
    },
    {
        "start": 189.5,
        "end": 203.0,
        "text": "மறத்தல் வெகுளியை யார்மாட்டும் (தீய)\nபிறத்தல் அதனான் வரும் (குறள் 303)"
    },
    # [Chorus Reprise 2]
    {
        "start": 203.5,
        "end": 221.0,
        "text": "[பல்லவி / Chorus Reprise]\nதன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    },
    {
        "start": 221.5,
        "end": 237.0,
        "text": "தன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    },
    # [Verse 3]
    {
        "start": 238.0,
        "end": 252.5,
        "text": "[சரணம் 3 / Verse 3]\nசினமென்னும் சேர்ந்தாரைக் கொல்லி (இனமென்னும்)\nஏமப் புணையைச் சுடும் (குறள் 306)"
    },
    {
        "start": 253.0,
        "end": 268.0,
        "text": "உள்ளிய தெல்லாம் உடனெய்தும் (உள்ளத்தால்)\nஉள்ளான் வெகுளி எனின் (குறள் 309)"
    },
    {
        "start": 268.5,
        "end": 283.5,
        "text": "இணர்எரி தோய்வன்ன இன்னா (செயினும்)\nபுணரின் வெகுளாமை நன்று (குறள் 308)"
    },
    {
        "start": 284.0,
        "end": 294.0,
        "text": "இறந்தார் இறந்தார் அனையர் (சினத்தைத்)\nதுறந்தார் துறந்தார் துணை (குறள் 310)"
    },
    # [Grand Chorus Finale]
    {
        "start": 294.5,
        "end": 308.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nதன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    },
    {
        "start": 308.5,
        "end": 324.0,
        "text": "தன்னைத்தான் காக்கின் சினங்காக்க (காவாக்கால்)\nதன்னையே கொல்லுஞ் சினம் (குறள் 305)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/xcUlgFsrepU.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "xcUlgFsrepU"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
