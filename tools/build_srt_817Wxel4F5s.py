# -*- coding: utf-8 -*-
"""
tools/build_srt_817Wxel4F5s.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 50 - இடனறிதல் (Film)
YouTube ID: 817Wxel4F5s
Matches master vocal timing: 270.3s (4m 30s)
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

# Cues matching exact musical flow & duration of 817Wxel4F5s (270.3s)
cues = [
    {
        "start": 3.0,
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 50: இடனறிதல் (Idanarithal)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 15.0,
        "end": 30.0,
        "text": "[பல்லவி / Chorus]\nதொடங்கற்க எவ்வினையும் எள்ளற்க (முற்றும்)\nஇடங்கண்டபின் அல்லது (குறள் 491)"
    },
    {
        "start": 30.5,
        "end": 45.0,
        "text": "தொடங்கற்க எவ்வினையும் எள்ளற்க (முற்றும்)\nஇடங்கண்டபின் அல்லது (குறள் 491)"
    },
    # [Verse 1]
    {
        "start": 45.5,
        "end": 63.0,
        "text": "[சரணம் 1 / Verse 1]\nகடலோடா கால்வல் நெடுந்தேர் (கடலோடும்)\nநாவாயும் ஓடா நிலத்து (குறள் 496)"
    },
    {
        "start": 63.5,
        "end": 81.0,
        "text": "கடலோடா கால்வல் நெடுந்தேர் (கடலோடும்)\nநாவாயும் ஓடா நிலத்து (குறள் 496)"
    },
    {
        "start": 81.5,
        "end": 101.0,
        "text": "ஆற்றாரும் ஆற்றி அடுப (இடனறிந்து)\nபோற்றார்கண் போற்றிச் செயின் (குறள் 492)"
    },
    {
        "start": 101.5,
        "end": 121.0,
        "text": "ஆற்றாரும் ஆற்றி அடுப (இடனறிந்து)\nபோற்றார்கண் போற்றிச் செயின் (குறள் 492)"
    },
    # [Chorus Reprise 1]
    {
        "start": 121.5,
        "end": 133.0,
        "text": "[பல்லவி / Chorus]\nதொடங்கற்க எவ்வினையும் எள்ளற்க (முற்றும்)\nஇடங்கண்டபின் அல்லது (குறள் 491)"
    },
    {
        "start": 133.5,
        "end": 145.0,
        "text": "தொடங்கற்க எவ்வினையும் எள்ளற்க (முற்றும்)\nஇடங்கண்டபின் அல்லது (குறள் 491)"
    },
    # [Bridge]
    {
        "start": 145.5,
        "end": 164.0,
        "text": "[இடைப்பகுதி / Bridge]\nஎண்ணியார் எண்ணம் இழப்பர் (இடனறிந்து)\nதுன்னியார் துன்னிச் செயின் (குறள் 494)"
    },
    {
        "start": 164.5,
        "end": 183.0,
        "text": "அஞ்சாமை அல்லால் துணைவேண்டா (எஞ்சாமை)\nஎண்ணி இடத்தால் செயின் (குறள் 497)"
    },
    {
        "start": 183.5,
        "end": 204.0,
        "text": "நெடும்புனலுள் வெல்லும் முதலை (அடும்புனலின்)\nநீங்கின் அதனைப் பிற (குறள் 495)"
    },
    {
        "start": 204.5,
        "end": 224.0,
        "text": "நெடும்புனலுள் வெல்லும் முதலை (அடும்புனலின்)\nநீங்கின் அதனைப் பிற (குறள் 495)"
    },
    # [Verse 2]
    {
        "start": 224.5,
        "end": 242.0,
        "text": "[சரணம் 2 / Verse 2]\nகாலாழ் களரில் நரியடும் (கண்ணஞ்சா)\nவேலாள் முகத்த களிறு (குறள் 500)"
    },
    {
        "start": 242.5,
        "end": 254.0,
        "text": "சிறைநலனும் சீரும் இலரெனினும் (மாந்தர்)\nஉறைநிலத்தோடு ஒட்டல் அரிது (குறள் 498)"
    },
    # [Grand Chorus Finale]
    {
        "start": 254.5,
        "end": 264.0,
        "text": "[நிறைவுப் பல்லவி / Grand Finale Chorus]\nதொடங்கற்க எவ்வினையும் எள்ளற்க (முற்றும்)\nஇடங்கண்டபின் அல்லது (குறள் 491)"
    },
    {
        "start": 264.5,
        "end": 269.5,
        "text": "தொடங்கற்க எவ்வினையும் எள்ளற்க (முற்றும்)\nஇடங்கண்டபின் அல்லது (குறள் 491)"
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
    vid = "817Wxel4F5s"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
