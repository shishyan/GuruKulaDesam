# -*- coding: utf-8 -*-
"""
tools/build_srt_djYooU1LmGk.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 30 - வாய்மை
YouTube ID: djYooU1LmGk
Suno Track: 4d2a17ee-02bb-410c-8c6a-3dc850c88586 (வாய்மை 1J Golden)
Duration: 236.89s (3m 56s)
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

# Suno Song Architecture for வாய்மை 1J Golden:
# 00:00 - 00:15: Invocatory Orchestral Introduction
# 00:15 - 00:46: [Verse 1] வாய்மை எனப்படுவது யாதெனின்... பொய்யாமை பொய்யாமை ஆற்றின்... பொய்யாமை அன்ன புகழில்லை... (குறள் 291, 297, 296)
# 00:46 - 01:10: [Chorus 1] தன்நெஞ்சு அறிவது பொய்யற்க (பொய்த்தபின்) தன்நெஞ்சே தன்னை சுடும் (குறள் 293)
# 01:10 - 01:50: [Verse 2] பொய்மையும் வாய்மை இடத்த... உள்ளத்தால் பொய்யாது ஒழுகின்... மனத்தொடு வாய்மை மொழியின்... (குறள் 292, 294, 295)
# 01:50 - 02:12: [Chorus Reprise 1] பொய்யாமை பொய்யாமை ஆற்றின் அறம்பிற செய்யாமை செய்யாமை நன்று
# 02:12 - 02:56: [Verse 3] புறந்தூய்மை நீரான் அமையும்... எல்லா விளக்கும் விளக்கல்ல... யாமெய்யாக் கண்டவற்றுள் இல்லை... (குறள் 298, 299, 300)
# 02:56 - 03:50: [Grand Chorus Finale & Reprise] தன்நெஞ்சு அறிவது பொய்யற்க பொய்த்தபின் தன்நெஞ்சே தன்னை சுடும்
# 03:50 - 03:56: Orchestral Outro & Finale

cues = [
    {
        "start": 3.0,
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 30: வாய்மை (Vaaimai / Truthfulness)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Verse 1]
    {
        "start": 15.0,
        "end": 30.0,
        "text": "[சரணம் 1 / Verse 1]\nவாய்மை எனப்படுவது யாதெனின் (யாதொன்றும்)\nதீமை இலாத சொலல் (குறள் 291)"
    },
    {
        "start": 30.5,
        "end": 46.0,
        "text": "பொய்யாமை பொய்யாமை ஆற்றின் (அறம்பிற)\nசெய்யாமை செய்யாமை நன்று (குறள் 297)"
    },
    # [Chorus 1]
    {
        "start": 46.5,
        "end": 58.0,
        "text": "[பல்லவி / Chorus]\nதன்நெஞ்சு அறிவது பொய்யற்க (பொய்த்தபின்)\nதன்நெஞ்சே தன்னை சுடும் (குறள் 293)"
    },
    {
        "start": 58.5,
        "end": 70.0,
        "text": "தன்நெஞ்சு அறிவது பொய்யற்க (பொய்த்தபின்)\nதன்நெஞ்சே தன்னை சுடும் (குறள் 293)"
    },
    # [Verse 2]
    {
        "start": 70.5,
        "end": 90.0,
        "text": "[சரணம் 2 / Verse 2]\nபொய்மையும் வாய்மை இடத்த (புரைதீர்ந்த)\nநன்மை பயக்கும் எனின் (குறள் 292)"
    },
    {
        "start": 90.5,
        "end": 110.0,
        "text": "உள்ளத்தால் பொய்யாது ஒழுகின் (உலகத்தார்)\nஉள்ளத்துள் எல்லாம் உளன் (குறள் 294)"
    },
    {
        "start": 110.5,
        "end": 130.0,
        "text": "மனத்தொடு வாய்மை மொழியின் (தவத்தொடு)\nதானம் செய்வாரின் தலை (குறள் 295)"
    },
    # [Chorus Reprise 1]
    {
        "start": 130.5,
        "end": 145.0,
        "text": "[பல்லவி / Chorus]\nபொய்யாமை பொய்யாமை ஆற்றின் (அறம்பிற)\nசெய்யாமை செய்யாமை நன்று (குறள் 297)"
    },
    {
        "start": 145.5,
        "end": 160.0,
        "text": "பொய்யாமை அன்ன புகழில்லை (எய்யாமை)\nஎல்லா அறமும் தரும் (குறள் 296)"
    },
    # [Verse 3]
    {
        "start": 160.5,
        "end": 180.0,
        "text": "[சரணம் 3 / Verse 3]\nபுறந்தூய்மை நீரான் அமையும் (அகந்தூய்மை)\nவாய்மையால் காணப் படும் (குறள் 298)"
    },
    {
        "start": 180.5,
        "end": 200.0,
        "text": "எல்லா விளக்கும் விளக்கல்ல (சான்றோர்க்கு)\nபொய்யா விளக்கே விளக்கு (குறள் 299)"
    },
    {
        "start": 200.5,
        "end": 220.0,
        "text": "யாமெய்யாக் கண்டவற்றுள் இல்லை (எனைத்தொன்றும்)\nவாய்மையின் நல்ல பிற (குறள் 300)"
    },
    # [Grand Chorus Finale]
    {
        "start": 220.5,
        "end": 236.0,
        "text": "[நிறைவு / Finale]\nதன்நெஞ்சு அறிவது பொய்யற்க (பொய்த்தபின்)\nதன்நெஞ்சே தன்னை சுடும் (குறள் 293)"
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
    vid = "djYooU1LmGk"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
