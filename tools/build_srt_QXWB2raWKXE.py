# -*- coding: utf-8 -*-
"""
tools/build_srt_QXWB2raWKXE.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 63 - இடுக்கண் அழியாமை
YouTube ID: QXWB2raWKXE
Suno Track: 0a96e734-2d36-4b0a-93f3-0b0f156e0cdd (இடுக்கணழியாமை 1S Golden Pop)
Duration: 329.77s (5m 30s)
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
        "text": "திருக்குறள் — அதிகாரம் 63: இடுக்கண் அழியாமை (Not Grieving at Calamities)\n[செவ்வியல் திரை இசை / Classical Devotional Remix]"
    },
    # [Chorus 1]
    {
        "start": 21.0,
        "end": 46.0,
        "text": "[பல்லவி / Chorus]\nஇடுக்கண் வருங்கால் நகுக (அதனை)\nஅடுத்தூர்வது அஃதொப்பது இல் (குறள் 621)"
    },
    {
        "start": 46.5,
        "end": 64.0,
        "text": "இடுக்கண் வருங்கால் நகுக (அதனை)\nஅடுத்தூர்வது அஃதொப்பது இல் (குறள் 621)"
    },
    # [Verse 1]
    {
        "start": 65.0,
        "end": 80.5,
        "text": "[சரணம் 1 / Verse 1]\nஅடுக்கி வரினும் அழிவிலான் (உற்ற)\nஇடுக்கண் இடுக்கட் படும் (குறள் 625)"
    },
    {
        "start": 81.0,
        "end": 96.0,
        "text": "இன்பம் விழையான் இடும்பை (இயல்பென்பான்)\nதுன்பம் உறுதல் இலன் (குறள் 628)"
    },
    {
        "start": 96.5,
        "end": 115.0,
        "text": "இன்பம் விழையான் இடும்பை (இயல்பென்பான்)\nதுன்பம் உறுதல் இலன் (குறள் 628)"
    },
    # [Chorus Reprise 1]
    {
        "start": 115.5,
        "end": 145.0,
        "text": "[பல்லவி / Chorus Reprise]\nஇடுக்கண் வருங்கால் நகுக (அதனை)\nஅடுத்தூர்வது அஃதொப்பது இல் (குறள் 621)"
    },
    # [Verse 2]
    {
        "start": 161.0,
        "end": 172.0,
        "text": "[சரணம் 2 / Verse 2]\nவெள்ளத் தனைய இடும்பை (அறிவுடையான்)\nஉள்ளத்தின் உள்ளக் கெடும் (குறள் 622)"
    },
    {
        "start": 172.5,
        "end": 188.0,
        "text": "இடும்பைக்கு இடும்பை படுப்பர் (இடும்பைக்கு)\nஇடும்பை படாஅ தவர் (குறள் 623)"
    },
    {
        "start": 188.5,
        "end": 204.0,
        "text": "அற்றேம் என்று அல்லற் படுபவோ (பெற்றேம் என்று)\nஓம்புதல் தேற்றா தவர் (குறள் 626)"
    },
    {
        "start": 204.5,
        "end": 215.0,
        "text": "அற்றேம் என்று அல்லற் படுபவோ (பெற்றேம் என்று)\nஓம்புதல் தேற்றா தவர் (குறள் 626)"
    },
    # [Chorus Reprise 2]
    {
        "start": 215.5,
        "end": 228.0,
        "text": "[பல்லவி / Chorus Reprise]\nஇடுக்கண் வருங்கால் நகுக (அதனை)\nஅடுத்தூர்வது அஃதொப்பது இல் (குறள் 621)"
    },
    {
        "start": 228.5,
        "end": 242.0,
        "text": "இடுக்கண் வருங்கால் நகுக (அதனை)\nஅடுத்தூர்வது அஃதொப்பது இல் (குறள் 621)"
    },
    # [Verse 3 / Bridge]
    {
        "start": 242.5,
        "end": 255.0,
        "text": "[சரணம் 3 / Bridge]\nஇலக்கம் உடம்பிடும்பைக் கென்று (கலக்கத்தைக்)\nகையாறாக் கொள்ளாதாம் மேல் (குறள் 627)"
    },
    {
        "start": 255.5,
        "end": 270.0,
        "text": "மடுத்தவா யெல்லாம் பகடன்னான் (உற்ற)\nஇடுக்கண் இடர்ப்பாடு உடைத்து (குறள் 624)"
    },
    {
        "start": 270.5,
        "end": 283.0,
        "text": "இன்பத்துள் இன்பம் விழையாதான் (துன்பத்துள்)\nதுன்பம் உறுதல் இலன் (குறள் 629)"
    },
    {
        "start": 283.5,
        "end": 296.0,
        "text": "இன்னாமை இன்பம் எனக்கொளின் (ஆகுந்தன்)\nஒன்னார் விழையுஞ் சிறப்பு (குறள் 630)"
    },
    # [Grand Finale Chorus]
    {
        "start": 296.5,
        "end": 312.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nஇடுக்கண் வருங்கால் நகுக (அதனை)\nஅடுத்தூர்வது அஃதொப்பது இல் (குறள் 621)"
    },
    {
        "start": 312.5,
        "end": 329.0,
        "text": "இடுக்கண் வருங்கால் நகுக (அதனை)\nஅடுத்தூர்வது அஃதொப்பது இல் (குறள் 621)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/QXWB2raWKXE.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "QXWB2raWKXE"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
