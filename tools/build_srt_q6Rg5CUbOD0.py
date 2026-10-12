# -*- coding: utf-8 -*-
"""
tools/build_srt_q6Rg5CUbOD0.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 65 - சொல்வன்மை
YouTube ID: q6Rg5CUbOD0
Duration: 338.8s (5m 38s)
"""

import sys, os, subprocess

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
        "end": 69.0,
        "text": "நாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    # [Verse 1]
    {
        "start": 69.5,
        "end": 86.0,
        "text": "[சரணம் 1 / Verse 1]\nதிறனறிந்து சொல்லுக சொல்லை (அறனும்)\nபொருளும் அதனினூஉங்கு இல் (குறள் 644)"
    },
    {
        "start": 86.5,
        "end": 102.0,
        "text": "திறனறிந்து சொல்லுக சொல்லை (அறனும்)\nபொருளும் அதனினூஉங்கு இல் (குறள் 644)"
    },
    {
        "start": 102.5,
        "end": 117.0,
        "text": "ஆக்கமுங் கேடும் அதனால் வருதலால் (காத்தோம்பல்)\nசொல்லின்கட் சோர்வு (குறள் 642)"
    },
    {
        "start": 117.5,
        "end": 132.0,
        "text": "ஆக்கமுங் கேடும் அதனால் வருதலால் (காத்தோம்பல்)\nசொல்லின்கட் சோர்வு (குறள் 642)"
    },
    # [Chorus Reprise 1]
    {
        "start": 132.5,
        "end": 149.0,
        "text": "[பல்லவி / Chorus]\nநாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    {
        "start": 149.5,
        "end": 166.0,
        "text": "நாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    # [Verse 2]
    {
        "start": 166.5,
        "end": 184.0,
        "text": "[சரணம் 2 / Verse 2]\nசொல்லுக சொல்லைப் பிறிதோர்சொல் (அச்சொல்லை)\nவெல்லுஞ்சொல் இன்மை அறிந்து (குறள் 645)"
    },
    {
        "start": 184.5,
        "end": 202.0,
        "text": "சொலல்வல்லன் சோர்விலன் அஞ்சான் (அவனை)\nஇகல்வெல்லல் யார்க்கும் அரிது (குறள் 647)"
    },
    {
        "start": 202.5,
        "end": 220.0,
        "text": "இணர்ஊழ்த்தும் நாறா மலரனையர் (கற்றது)\nஉணர விரித்துரையா தார் (குறள் 650)"
    },
    # [Bridge]
    {
        "start": 220.5,
        "end": 238.0,
        "text": "[இடைப்பகுதி / Bridge]\nகேட்டார்ப் பிணிக்கும் தகையவாய்க் (கேளாரும்)\nவேட்ப மொழிவதாம் சொல் (குறள் 643)"
    },
    {
        "start": 238.5,
        "end": 256.0,
        "text": "வேட்பத்தாம் சொல்லிப் பிறர்சொல் (பயன்கோடல்)\nமாட்சியின் மாண்டார் கோள் (குறள் 646)"
    },
    {
        "start": 256.5,
        "end": 274.0,
        "text": "விரைந்து தொழில்கேட்கும் ஞாலம் (நிரந்தினிது)\nசொல்லுதல் வல்லார்ப் பெறின் (குறள் 648)"
    },
    {
        "start": 274.5,
        "end": 292.0,
        "text": "பலசொல்லக் காமுறுவர் மன்ற (மாசற்ற)\nசிலசொல்லல் தேற்றா தவர் (குறள் 649)"
    },
    # [Grand Chorus Finale]
    {
        "start": 292.5,
        "end": 315.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nநாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    },
    {
        "start": 315.5,
        "end": 336.0,
        "text": "நாநலம் என்னும் நலனுடைமை (அந்நலம்)\nயாநலத்து உள்ளதூஉம் அன்று (குறள் 641)"
    }
]

def generate_srt(cues):
    lines = []
    for idx, cue in enumerate(cues, 1):
        s = to_srt_time(cue["start"])
        e = to_srt_time(cue["end"])
        lines.append(f"{idx}\n{s} --> {e}\n{cue['text']}\n")
    return "\n".join(lines)

if __name__ == "__main__":
    vid = "q6Rg5CUbOD0"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
