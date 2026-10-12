# -*- coding: utf-8 -*-
"""
tools/build_srt_9NIv50lV4-M.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 36 - மெய்யுணர்தல்
YouTube ID: 9NIv50lV4-M
Suno Track: 2b85c899-8f95-4ea0-b081-a8ac88fd3e87 (மெய்யுணர்தல் 1E)
Duration: 207.42s (3m 27s)
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

# Suno Song Architecture for மெய்யுணர்தல் 1E:
# 00:00 - 00:15: Invocatory Orchestral Introduction
# 00:15 - 00:44: [Chorus] எப்பொருள் எத்தன்மையது ஆயினும் (அப்பொருள்) மெய்ப்பொருள் காண்பது அறிவு (குறள் 355)
#                பிறப்பென்னும் பேதைமை நீங்கச் (சிறப்பென்னும்) செம்பொருள் காண்பது அறிவு (குறள் 358)
# 00:44 - 01:24: [Verse 1] ஐயத்தின் நீங்கித் தெளிந்தார்க்கு... ஐயுணர்வு எய்தியக் கண்ணும்... (குறள் 353 & 354)
#                பொருளல்ல வற்றைப் பொருளென்று... இருள்நீங்கி இன்பம் பயக்கும்... (குறள் 351 & 352)
# 01:24 - 01:52: [Chorus Reprise] எப்பொருள் எத்தன்மையது ஆயினும்... பிறப்பென்னும் பேதைமை நீங்கச்...
# 01:52 - 02:35: [Verse 2] கற்றீண்டு மெய்ப்பொருள் கண்டார்... ஓர்த்துள்ளம் உள்ளது உணரின்... (குறள் 356 & 357)
#                சார்புணர்ந்து சார்பு கெடஒழுகின்... காமம் வெகுளி மயக்கம்... (குறள் 359 & 360)
# 02:35 - 03:15: [Grand Chorus Finale & Reprise] எப்பொருள் எத்தன்மையது ஆயினும் மெய்ப்பொருள் காண்பது அறிவு
# 03:15 - 03:27: Orchestral Outro & Finale

cues = [
    {
        "start": 3.0,
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 36: மெய்யுணர்தல் (Meiyunarthal)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 15.0,
        "end": 29.0,
        "text": "[பல்லவி / Chorus]\nஎப்பொருள் எத்தன்மையது ஆயினும் (அப்பொருள்)\nமெய்ப்பொருள் காண்பது அறிவு (குறள் 355)"
    },
    {
        "start": 29.5,
        "end": 44.0,
        "text": "பிறப்பென்னும் பேதைமை நீங்கச் (சிறப்பென்னும்)\nசெம்பொருள் காண்பது அறிவு (குறள் 358)"
    },
    # [Verse 1]
    {
        "start": 44.5,
        "end": 64.0,
        "text": "[சரணம் 1 / Verse 1]\nஐயத்தின் நீங்கித் தெளிந்தார்க்கு (வையத்தின்)\nவானம் நணியது உடைத்து (குறள் 353)"
    },
    {
        "start": 64.5,
        "end": 84.0,
        "text": "ஐயுணர்வு எய்தியக் கண்ணும் (பயமின்றே)\nமெய்யுணர்வு இல்லாத அவர்க்கு (குறள் 354)"
    },
    {
        "start": 84.5,
        "end": 104.0,
        "text": "பொருளல்ல வற்றைப் பொருளென்று (உணரும்)\nமருளானாம் மாணாப் பிறப்பு (குறள் 351)"
    },
    {
        "start": 104.5,
        "end": 124.0,
        "text": "இருள்நீங்கி இன்பம் பயக்கும் (மருள்நீங்கி)\nமாசறு காட்சி யவர்க்கு (குறள் 352)"
    },
    # [Chorus Reprise]
    {
        "start": 124.5,
        "end": 138.0,
        "text": "[பல்லவி / Chorus]\nஎப்பொருள் எத்தன்மையது ஆயினும் (அப்பொருள்)\nமெய்ப்பொருள் காண்பது அறிவு (குறள் 355)"
    },
    {
        "start": 138.5,
        "end": 152.0,
        "text": "பிறப்பென்னும் பேதைமை நீங்கச் (சிறப்பென்னும்)\nசெம்பொருள் காண்பது அறிவு (குறள் 358)"
    },
    # [Verse 2]
    {
        "start": 152.5,
        "end": 172.0,
        "text": "[சரணம் 2 / Verse 2]\nகற்றீண்டு மெய்ப்பொருள் கண்டார் (தலைப்படுவர்)\nமற்றீண்டு வாரா நெறி (குறள் 356)"
    },
    {
        "start": 172.5,
        "end": 192.0,
        "text": "ஓர்த்துள்ளம் உள்ளது உணரின் (ஒருதலையா)\nபேர்த்துள்ள வேண்டா பிறப்பு (குறள் 357)"
    },
    {
        "start": 192.5,
        "end": 213.0,
        "text": "சார்புணர்ந்து சார்பு கெடஒழுகின் (மற்றழித்து)\nசார்தரா சார்தரு நோய் (குறள் 359)"
    },
    {
        "start": 213.5,
        "end": 235.0,
        "text": "காமம் வெகுளி மயக்கம் (இவைமூன்றன்)\nநாமம் கெடக்கெடும் நோய் (குறள் 360)"
    },
    # [Grand Chorus Finale]
    {
        "start": 235.5,
        "end": 265.0,
        "text": "[நிறைவு / Finale]\nஎப்பொருள் எத்தன்மையது ஆயினும் (அப்பொருள்)\nமெய்ப்பொருள் காண்பது அறிவு (குறள் 355)"
    },
    {
        "start": 265.5,
        "end": 305.0,
        "text": "பிறப்பென்னும் பேதைமை நீங்கச் (சிறப்பென்னும்)\nசெம்பொருள் காண்பது அறிவு (குறள் 358)"
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
    vid = "9NIv50lV4-M"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
