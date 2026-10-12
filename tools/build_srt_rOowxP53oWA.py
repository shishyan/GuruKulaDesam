# -*- coding: utf-8 -*-
"""
tools/build_srt_rOowxP53oWA.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 65 - சொல்வன்மை
YouTube ID: rOowxP53oWA
Suno Track: 958fdd10-c89e-4a90-9dd9-05da79cdfac5 (சொல்வன்மை 1R Golden)
Duration: 335.9s (5m 36s)
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
        "text": "திருக்குறள் — அதிகாரம் 65: சொல்வன்மை (Solvanmai / Eloquence of Speech)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 29.0,
        "end": 52.0,
        "text": "[பல்லவி / Chorus]\nநாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    {
        "start": 52.5,
        "end": 68.5,
        "text": "நாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    # [Verse 1]
    {
        "start": 69.0,
        "end": 85.0,
        "text": "[சரணம் 1 / Verse 1]\nதிறனறிந்து சொல்லுக சொல்லை (அறனும்)\nபொருளும் அதனினூஉங்கு இல் (குறள் 644)"
    },
    {
        "start": 85.5,
        "end": 101.5,
        "text": "திறனறிந்து சொல்லுக சொல்லை (அறனும்)\nபொருளும் அதனினூஉங்கு இல் (குறள் 644)"
    },
    {
        "start": 102.0,
        "end": 116.0,
        "text": "ஆக்கமுங் கேடும் அதனால் வருதலால் (காத்தோம்பல்)\nசொல்லின்கட் சோர்வு (குறள் 642)"
    },
    {
        "start": 116.5,
        "end": 130.0,
        "text": "ஆக்கமுங் கேடும் அதனால் வருதலால் (காத்தோம்பல்)\nசொல்லின்கட் சோர்வு (குறள் 642)"
    },
    # [Chorus Reprise 1]
    {
        "start": 131.0,
        "end": 143.0,
        "text": "[பல்லவி / Chorus Reprise]\nநாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    {
        "start": 143.5,
        "end": 160.0,
        "text": "நாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    # [Verse 2]
    {
        "start": 177.0,
        "end": 188.0,
        "text": "[சரணம் 2 / Verse 2]\nசொல்லுக சொல்லைப் பிறிதோர்சொல் (அச்சொல்லை)\nவெல்லுஞ்சொல் இன்மை அறிந்து (குறள் 645)"
    },
    {
        "start": 188.5,
        "end": 201.0,
        "text": "சொல்லுக சொல்லைப் பிறிதோர்சொல் (அச்சொல்லை)\nவெல்லுஞ்சொல் இன்மை அறிந்து (குறள் 645)"
    },
    {
        "start": 201.5,
        "end": 213.0,
        "text": "சொலல்வல்லன் சோர்விலன் அஞ்சான் (அவனை)\nஇகல்வெல்லல் யார்க்கும் அரிது (குறள் 647)"
    },
    {
        "start": 213.5,
        "end": 224.0,
        "text": "பலசொல்லக் காமுறுவர் மன்றமா (சற்ற)\nசிலசொல்லல் தேற்றா தவர் (குறள் 649)"
    },
    # [Chorus Reprise 2]
    {
        "start": 224.5,
        "end": 238.5,
        "text": "[பல்லவி / Chorus Reprise]\nநாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    {
        "start": 239.0,
        "end": 255.0,
        "text": "நாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    # [Bridge]
    {
        "start": 255.5,
        "end": 266.5,
        "text": "[சரணம் 3 / Bridge]\nகேட்டார்ப் பிணிக்கும் தகையவாய்க் (கேளாரும்)\nவேட்ப மொழிவதாம் சொல் (குறள் 643)"
    },
    {
        "start": 267.0,
        "end": 278.5,
        "text": "வேட்பத்தாஞ் சொல்லிப் பிறர்சொல் (பயன்கோடல்)\nமாட்சியின் மாசற்றார் கோள் (குறள் 646)"
    },
    {
        "start": 279.0,
        "end": 291.5,
        "text": "விரைந்து தொழில்கேட்கும் ஞாலம் (நிரந்தினிது)\nசொல்லுதல் வல்லார்ப் பெறின் (குறள் 648)"
    },
    {
        "start": 292.0,
        "end": 303.0,
        "text": "இணர்ஊழ்த்தும் நாறா மலரனையர் (கற்றது)\nஉணர விரித்துரையா தார் (குறள் 650)"
    },
    # [Grand Chorus Finale]
    {
        "start": 303.5,
        "end": 317.5,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nநாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    {
        "start": 318.0,
        "end": 334.0,
        "text": "நாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/rOowxP53oWA.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "rOowxP53oWA"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
