# -*- coding: utf-8 -*-
"""
tools/build_srt_hCHBPd8BH8A.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 6 - வாழ்க்கைத் துணைநலம்
YouTube ID: hCHBPd8BH8A
Suno Track: 785ebb2a-d7c6-4b01-bd72-02cda092ff65 (வாழ்க்கைத் துணைநலம் 1A)
Duration: 302.74s (5m 02s)
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

# Suno Song Architecture for வாழ்க்கைத் துணைநலம் 1A:
# 00:00 - 00:15: Invocatory Orchestral Introduction
# 00:15 - 00:46: [Verse 1 & Chorus] மனைமாட்சி இல்லாள்கண் இல்லாயின் வாழ்க்கை எனைமாட்சித் தாயினும் இல் (குறள் 52)
# 00:46 - 01:25: [Verse 2] மங்கலம் என்ப மனைமாட்சி மற்றுஅதன் நன்கலம் நன்மக்கட் பேறு (குறள் 60)
# 01:25 - 02:00: [Verse 3] மனைத்தக்க மாண்புடையள்ஆகித் தற்கொண்டான் வளத்தக்காள் வாழ்க்கைத் துணை (குறள் 51)
# 02:00 - 02:40: [Verse 4] பெண்ணின் பெருந்தக்க யாவுள கற்பென்னும் திண்மைஉண் டாகப் பெறின் (குறள் 54)
# 02:40 - 03:30: [Verse 5] தெய்வம் தொழாஅள் கொழுநன் தொழுதெழுவாள் பெய்யெனப் பெய்யும் மழை (குறள் 55)
# 03:30 - 04:45: [Grand Chorus Finale & Reprise] மனைமாட்சி இல்லாள்கண் இல்லாயின் வாழ்க்கை எனைமாட்சித் தாயினும் இல்
# 04:45 - 05:02: Orchestral Outro & Finale

cues = [
    {
        "start": 3.0,
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 6: வாழ்க்கைத் துணைநலம் (Vaazhkkaith Thunainalam)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Verse 1 & Chorus]
    {
        "start": 15.0,
        "end": 30.0,
        "text": "[சரணம் 1 / Verse 1]\nமனைமாட்சி இல்லாள்கண் இல்லாயின் (வாழ்க்கை)\nஎனைமாட்சித் தாயினும் இல் (குறள் 52)"
    },
    {
        "start": 30.5,
        "end": 46.0,
        "text": "[பல்லவி / Chorus]\nமனைமாட்சி இல்லாள்கண் இல்லாயின் (வாழ்க்கை)\nஎனைமாட்சித் தாயினும் இல் (குறள் 52)"
    },
    # [Verse 2]
    {
        "start": 46.5,
        "end": 66.0,
        "text": "[சரணம் 2 / Verse 2]\nமங்கலம் என்ப மனைமாட்சி (மற்றுஅதன்)\nநன்கலம் நன்மக்கட் பேறு (குறள் 60)"
    },
    {
        "start": 66.5,
        "end": 86.0,
        "text": "மங்கலம் என்ப மனைமாட்சி (மற்றுஅதன்)\nநன்கலம் நன்மக்கட் பேறு (குறள் 60)"
    },
    {
        "start": 86.5,
        "end": 106.0,
        "text": "மங்கலம் என்பதாகிய மனைமாட்சியே!\nஅதன் நன்கலம் நன்மக்கட் பேறு!"
    },
    {
        "start": 106.5,
        "end": 125.0,
        "text": "மங்கலம் என்பதாகிய மனைமாட்சியே!\nஅதன் நன்கலம் நன்மக்கட் பேறு!"
    },
    # [Verse 3]
    {
        "start": 125.5,
        "end": 145.0,
        "text": "[சரணம் 3 / Verse 3]\nமனைத்தக்க மாண்புடையள்ஆகித் (தற்கொண்டான்)\nவளத்தக்காள் வாழ்க்கைத் துணை (குறள் 51)"
    },
    {
        "start": 145.5,
        "end": 165.0,
        "text": "மாண்பு உடையவளாகியே தன் கொண்டான்\nவளத்தக்காள் வாழ்க்கைத் துணையானாள்!"
    },
    {
        "start": 165.5,
        "end": 185.0,
        "text": "மனைத்தக்க மாண்புடையள்ஆகித் (தற்கொண்டான்)\nவளத்தக்காள் வாழ்க்கைத் துணை (குறள் 51)"
    },
    # [Verse 4]
    {
        "start": 185.5,
        "end": 208.0,
        "text": "[சரணம் 4 / Verse 4]\nபெண்ணின் பெருந்தக்க யாவுள (கற்பென்னும்)\nதிண்மைஉண் டாகப் பெறின் (குறள் 54)"
    },
    {
        "start": 208.5,
        "end": 230.0,
        "text": "கற்பு என்னும் திண்மையைப் பெற்றிடின்!\nபெண்ணின் பெருந்தக்கது யாதும் உளதோ?"
    },
    {
        "start": 230.5,
        "end": 255.0,
        "text": "பெண்ணின் பெருந்தக்க யாவுள (கற்பென்னும்)\nதிண்மைஉண் டாகப் பெறின் (குறள் 54)"
    },
    # [Verse 5]
    {
        "start": 255.5,
        "end": 280.0,
        "text": "[சரணம் 5 / Verse 5]\nதெய்வம் தொழாஅள் கொழுநன் தொழுதெழுவாள்\nபெய்யெனப் பெய்யும் மழை (குறள் 55)"
    },
    {
        "start": 280.5,
        "end": 305.0,
        "text": "அவள் கொழுநன் தொழுதெழுவாள்! ஒரு தெய்வமும் தொழாஅள்!\nஎனினும் அவள் \"பெய்\" என்றிட, பெய்யும் மழை!"
    },
    {
        "start": 305.5,
        "end": 330.0,
        "text": "தெய்வம் தொழாஅள் கொழுநன் தொழுதெழுவாள்\nபெய்யெனப் பெய்யும் மழை (குறள் 55)"
    },
    # [Grand Chorus Finale]
    {
        "start": 330.5,
        "end": 390.0,
        "text": "[நிறைவு / Finale]\nமனைமாட்சி இல்லாள்கண் இல்லாயின் (வாழ்க்கை)\nஎனைமாட்சித் தாயினும் இல் (குறள் 52)"
    },
    {
        "start": 390.5,
        "end": 490.0,
        "text": "மனைமாட்சி இல்லாள்கண் இல்லாயின் (வாழ்க்கை)\nஎனைமாட்சித் தாயினும் இல் (குறள் 52)"
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
    vid = "hCHBPd8BH8A"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
