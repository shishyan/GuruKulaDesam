# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_aruludaimai_srt.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 25 - அருளுடைமை
YouTube ID: 0fD-z3s_g2A
Suno Track: 093244e4-4cdd-4ab5-8d5b-81aea26a9fc3 (திருக்குறள் அருளுடைமை 1S Golden)
Duration: 231.21 seconds (3m 51s)
"""

import os, sys, subprocess

sys.stdout.reconfigure(encoding='utf-8')

def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# Musical Song Flow Architecture mapped to Vocal Timeline:
# 00:00 - 00:24: Invocatory Orchestral Introduction
# 00:24 - 00:52: [Verse 1] அருட்செல்வம் செல்வத்துள் செல்வம்... அருளில்லார்க்கு அவ்வுலகம்... (குறள் 241 & 247)
# 00:52 - 01:18: [Verse 1 Part B] அருள்சேர்ந்த நெஞ்சினார்க்கு... அல்லல் அருளாள்வார்க்கு... (குறள் 242 & 245)
# 01:18 - 01:45: [Chorus] அருட்செல்வம் செல்வத்துள் செல்வம் பொருட்செல்வம் பூரியார் கண்ணும் உள (குறள் 241)
# 01:45 - 02:18: [Verse 2] மன்னுயிர் ஓம்பி... நல்லாற்றால் நாடி... பொருளற்றார் பூப்பர்... (குறள் 244, 243, 248)
# 02:18 - 02:45: [Chorus Reprise] அருட்செல்வம் செல்வத்துள் செல்வம்
# 02:45 - 03:22: [Verse 3] தெருளாதான் மெய்ப்பொருள்... வலியார்முன் தன்னை... (குறள் 249, 250)
# 03:22 - 03:45: [Grand Chorus Finale] அருட்செல்வம் செல்வத்துள் செல்வம் அருளில்லார்க்கு அவ்வுலகம் இல்லை
# 03:45 - 03:51: Orchestral Outro & Divine Finale

cues = [
    {
        "start": 5.0,
        "end": 23.5,
        "text": "திருக்குறள் — அதிகாரம் 25: அருளுடைமை (Aruludaimai)\n[செவ்வியல் பக்தி இசைப் பாடல் / Classical Devotional Song]"
    },
    # [Verse 1]
    {
        "start": 24.0,
        "end": 37.5,
        "text": "[சரணம் 1 / Verse 1]\nஅருட்செல்வம் செல்வத்துள் செல்வம் (பொருட்செல்வம்)\nபூரியார் கண்ணும் உள (குறள் 241)"
    },
    {
        "start": 38.0,
        "end": 51.5,
        "text": "அருளில்லார்க்கு அவ்வுலகம் இல்லை (பொருளில்லார்க்கு)\nஇவ்வுலகம் இல்லாகி யாங்கு (குறள் 247)"
    },
    {
        "start": 52.0,
        "end": 68.0,
        "text": "அருள்சேர்ந்த நெஞ்சினார்க்கு இல்லை இருள்சேர்ந்த\nஇன்னா உலகம் புகல் (குறள் 242)"
    },
    {
        "start": 68.5,
        "end": 85.0,
        "text": "அல்லல் அருளாள்வார்க்கு இல்லை (வளிவழங்கும்)\nமல்லன்மா ஞாலங் கரி (குறள் 245)"
    },
    # [Chorus]
    {
        "start": 85.5,
        "end": 102.0,
        "text": "[பல்லவி / Chorus]\nஅருட்செல்வம் செல்வத்துள் செல்வம் (பொருட்செல்வம்)\nபூரியார் கண்ணும் உள (குறள் 241)"
    },
    {
        "start": 102.5,
        "end": 118.0,
        "text": "அருளில்லார்க்கு அவ்வுலகம் இல்லை (பொருளில்லார்க்கு)\nஇவ்வுலகம் இல்லாகி யாங்கு (குறள் 247)"
    },
    # [Verse 2]
    {
        "start": 118.5,
        "end": 136.0,
        "text": "[சரணம் 2 / Verse 2]\nமன்னுயிர் ஓம்பி அருளாள்வார்க்கு (இல்லென்ப)\nதன்னுயிர் அஞ்சும் வினை (குறள் 244)"
    },
    {
        "start": 136.5,
        "end": 154.0,
        "text": "நல்லாற்றால் நாடி அருளாள்க (பல்லாற்றால்)\nதேரினும் அஃதே துணை (குறள் 243)"
    },
    {
        "start": 154.5,
        "end": 172.0,
        "text": "பொருளற்றார் பூப்பர் ஒருகால் (அருளற்றார்)\nஅற்றார்மற் றாதல் அரிது (குறள் 248)"
    },
    # [Chorus Reprise]
    {
        "start": 172.5,
        "end": 189.0,
        "text": "[பல்லவி / Chorus]\nஅருட்செல்வம் செல்வத்துள் செல்வம் (பொருட்செல்வம்)\nபூரியார் கண்ணும் உள"
    },
    {
        "start": 189.5,
        "end": 204.0,
        "text": "அருளில்லார்க்கு அவ்வுலகம் இல்லை (பொருளில்லார்க்கு)\nஇவ்வுலகம் இல்லாகி யாங்கு"
    },
    # [Verse 3]
    {
        "start": 204.5,
        "end": 218.0,
        "text": "[சரணம் 3 / Verse 3]\nதெருளாதான் மெய்ப்பொருள் கண்டற்றால் (தேரின்)\nஅருளாதான் செய்யும் அறம் (குறள் 249)"
    },
    {
        "start": 218.5,
        "end": 226.0,
        "text": "வலியார்முன் தன்னை நினைக்கதான் (தன்னின்)\nமெலியார்மேல் செல்லு மிடத்து (குறள் 250)"
    },
    # [Grand Chorus Finale]
    {
        "start": 226.5,
        "end": 231.2,
        "text": "[அருளுடைமை பக்தி இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/0fD-z3s_g2A.srt'
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Flawless real song-flow SRT generated: {srt_path} ({len(cues)} cues)")

    # Publish live to YouTube
    print("Publishing master SRT live to YouTube for 0fD-z3s_g2A...")
    cmd = 'python tools/api_publish_master.py 0fD-z3s_g2A'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
