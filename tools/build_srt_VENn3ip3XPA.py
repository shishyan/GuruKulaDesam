# -*- coding: utf-8 -*-
"""
tools/build_srt_VENn3ip3XPA.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 64 - அமைச்சு
YouTube ID: VENn3ip3XPA
Duration: 307.5s (5m 07s)
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
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 64: அமைச்சு (Amaichu / The Minister)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 15.0,
        "end": 30.0,
        "text": "[பல்லவி / Chorus]\nகருவியும் காலமும் செய்கையும் (செய்யும்)\nஅருவினையும் மாண்டது அமைச்சு (குறள் 631)"
    },
    {
        "start": 30.5,
        "end": 46.0,
        "text": "கருவியும் காலமும் செய்கையும் (செய்யும்)\nஅருவினையும் மாண்டது அமைச்சு (குறள் 631)"
    },
    # [Verse 1]
    {
        "start": 46.5,
        "end": 64.0,
        "text": "[சரணம் 1 / Verse 1]\nதெரிதலும் தேர்ந்து செயலும் (ஒருதலையாச்)\nசொல்லலும் வல்லது அமைச்சு (குறள் 634)"
    },
    {
        "start": 64.5,
        "end": 84.0,
        "text": "பிரித்தலும் பேணிக் கொளலும் (பிரிந்தார்ப்)\nபொருத்தலும் வல்ல தமைச்சு (குறள் 633)"
    },
    # [Chorus Reprise 1]
    {
        "start": 84.5,
        "end": 96.0,
        "text": "[பல்லவி / Chorus]\nகருவியும் காலமும் செய்கையும் (செய்யும்)\nஅருவினையும் மாண்டது அமைச்சு (குறள் 631)"
    },
    {
        "start": 96.5,
        "end": 108.0,
        "text": "கருவியும் காலமும் செய்கையும் (செய்யும்)\nஅருவினையும் மாண்டது அமைச்சு (குறள் 631)"
    },
    # [Verse 2]
    {
        "start": 108.5,
        "end": 128.0,
        "text": "[சரணம் 2 / Verse 2]\nஅறனறிந்து ஆன்றமைந்த சொல்லான் (எஞ்ஞான்றுந்)\nதிறனறிந்தான் தேர்ச்சித் துணை (குறள் 635)"
    },
    {
        "start": 128.5,
        "end": 148.0,
        "text": "வன் கண் குடிகாத்தல் கற்றறிதல் (ஆள்வினையோடு)\nஐந்துடன் மாண்டது அமைச்சு (குறள் 632)"
    },
    {
        "start": 148.5,
        "end": 168.0,
        "text": "அரிகொன்று அறியான் எனினும் (உறுதி)\nஉழையிருந்தான் கூறல் கடன் (குறள் 638)"
    },
    # [Chorus Reprise 2]
    {
        "start": 168.5,
        "end": 182.0,
        "text": "[பல்லவி / Chorus]\nகருவியும் காலமும் செய்கையும் (செய்யும்)\nஅருவினையும் மாண்டது அமைச்சு (குறள் 631)"
    },
    # [Bridge]
    {
        "start": 182.5,
        "end": 204.0,
        "text": "[இடைப்பகுதி / Bridge]\nமதிநுட்பம் நூலோடு உடையார்க்கு (அதிநுட்பம்)\nயாவுள முன்னிற் பவை (குறள் 636)"
    },
    {
        "start": 204.5,
        "end": 226.0,
        "text": "செயற்கை அறிந்தக் கடைத்தும் (உலகத்து)\nஇயற்கை அறிந்து செயல் (குறள் 637)"
    },
    {
        "start": 226.5,
        "end": 248.0,
        "text": "பழுதெண்ணும் மந்திரியின் பக்கத்துள் (தெவ்வோர்)\nஎழுபது கோடி உறும் (குறள் 639)"
    },
    {
        "start": 248.5,
        "end": 270.0,
        "text": "முறைப்படச் சூழ்ந்தும் முடிவெய்தா (நீர)\nதொகைப்படச் சூழா தவரின் (குறள் 640)"
    },
    # [Grand Chorus Finale]
    {
        "start": 270.5,
        "end": 290.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nகருவியும் காலமும் செய்கையும் (செய்யும்)\nஅருவினையும் மாண்டது அமைச்சு (குறள் 631)"
    },
    {
        "start": 290.5,
        "end": 305.0,
        "text": "கருவியும் காலமும் செய்கையும் (செய்யும்)\nஅருவினையும் மாண்டது அமைச்சு (குறள் 631)"
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
    vid = "VENn3ip3XPA"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
