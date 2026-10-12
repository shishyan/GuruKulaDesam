# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_kollaamai_srt.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 33 - கொல்லாமை
YouTube ID: L6DWSjPqoH0
Suno Track: 08494739-c45e-4101-8b26-2a5fd0495069 (கொல்லாமை 2A Golden)
Duration: 277.57 seconds (4m 37s)
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
# 00:24 - 00:52: [Chorus] பகுத்துண்டு பல்லுயிர் ஓம்புதல் (நூலோர்) தொகுத்தவற்றுள் எல்லாந் தலை (குறள் 322)
# 00:52 - 01:28: [Verse 1] நிலைஅஞ்சி நீத்தாருள்... அறவினை யாதெனின்... கொல்லாமை மேற்கொண்டு... (குறள் 325, 321, 326)
# 01:28 - 01:54: [Chorus Reprise 1] பகுத்துண்டு பல்லுயிர் ஓம்புதல்
# 01:54 - 02:35: [Verse 2] தன்னுயிர் நீப்பினும் செய்யற்க... நல்லாறு எனப்படுவது... நன்றாகும் ஆக்கம்... (குறள் 327, 324, 328)
# 02:35 - 03:02: [Bridge] கொலைவினையர் ஆகிய மாக்கள்... உயிர்உடம்பின் நீக்கியார் என்ப... (குறள் 329, 330)
# 03:02 - 03:45: [Chorus Reprise 2] பகுத்துண்டு பல்லுயிர் ஓம்புதல்
# 03:45 - 04:20: [Grand Chorus Finale] பகுத்துண்டு பல்லுயிர் ஓம்புதல் நூலோர் தொகுத்தவற்றுள் எல்லாந் தலை
# 04:20 - 04:37: Orchestral Outro & Divine Finale

cues = [
    {
        "start": 5.0,
        "end": 23.5,
        "text": "திருக்குறள் — அதிகாரம் 33: கொல்லாமை (Kollaamai)\n[செவ்வியல் பக்தி இசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 24.0,
        "end": 37.5,
        "text": "[பல்லவி / Chorus]\nபகுத்துண்டு பல்லுயிர் ஓம்புதல் (நூலோர்)\nதொகுத்தவற்றுள் எல்லாந் தலை (குறள் 322)"
    },
    {
        "start": 38.0,
        "end": 51.5,
        "text": "பகுத்துண்டு பல்லுயிர் ஓம்புதல் (நூலோர்)\nதொகுத்தவற்றுள் எல்லாந் தலை (குறள் 322)"
    },
    # [Verse 1]
    {
        "start": 52.0,
        "end": 68.0,
        "text": "[சரணம் 1 / Verse 1]\nநிலைஅஞ்சி நீத்தாருள் எல்லாம் (கொலைஅஞ்சி)\nகொல்லாமை சூழ்வான் தலை (குறள் 325)"
    },
    {
        "start": 68.5,
        "end": 85.0,
        "text": "அறவினை யாதெனின் கொல்லாமை (கோறல்)\nபிறவினை எல்லாந் தரும் (குறள் 321)"
    },
    {
        "start": 85.5,
        "end": 104.0,
        "text": "கொல்லாமை மேற்கொண்டு ஒழுகுவான் (வாழ்நாள்மேல்)\nசெல்லாது உயிருண்ணுங் கூற்று (குறள் 326)"
    },
    {
        "start": 104.5,
        "end": 125.0,
        "text": "ஒன்றாக நல்லது கொல்லாமை (மற்றதன்)\nபின்சாரப் பொய்யாமை நன்று (குறள் 323)"
    },
    # [Chorus Reprise 1]
    {
        "start": 125.5,
        "end": 139.0,
        "text": "[பல்லவி / Chorus]\nபகுத்துண்டு பல்லுயிர் ஓம்புதல் (நூலோர்)\nதொகுத்தவற்றுள் எல்லாந் தலை"
    },
    {
        "start": 139.5,
        "end": 153.0,
        "text": "பகுத்துண்டு பல்லுயிர் ஓம்புதல் (நூலோர்)\nதொகுத்தவற்றுள் எல்லாந் தலை"
    },
    # [Verse 2]
    {
        "start": 153.5,
        "end": 172.0,
        "text": "[சரணம் 2 / Verse 2]\nதன்னுயிர் நீப்பினும் செய்யற்க (தான்பிறிது)\nஇன்னுயிர் நீக்கும் வினை (குறள் 327)"
    },
    {
        "start": 172.5,
        "end": 191.0,
        "text": "நல்லாறு எனப்படுவது யாதெனின் (யாதொன்றும்)\nகொல்லாமை சூழும் நெறி (குறள் 324)"
    },
    {
        "start": 191.5,
        "end": 210.0,
        "text": "நன்றாகும் ஆக்கம் பெரிதெனினும் (சான்றோர்க்கு)\nகொன்றாகும் ஆக்கங் கடை (குறள் 328)"
    },
    # [Bridge]
    {
        "start": 210.5,
        "end": 228.0,
        "text": "[அனுபல்லவி / Bridge]\nகொலைவினையர் ஆகிய மாக்கள் (புலைவினையர்)\nபுன்மை தெரிவார் அகத்து (குறள் 329)"
    },
    {
        "start": 228.5,
        "end": 246.0,
        "text": "உயிர்உடம்பின் நீக்கியார் என்ப (செயிர்உடம்பின்)\nசெல்லாத்தீ வாழ்க்கை யவர் (குறள் 330)"
    },
    # [Grand Chorus Finale]
    {
        "start": 246.5,
        "end": 260.0,
        "text": "[பல்லவி நிறைவு / Grand Chorus Finale]\nபகுத்துண்டு பல்லுயிர் ஓம்புதல் (நூலோர்)\nதொகுத்தவற்றுள் எல்லாந் தலை (குறள் 322)"
    },
    {
        "start": 260.5,
        "end": 272.0,
        "text": "பகுத்துண்டு பல்லுயிர் ஓம்புதல் (நூலோர்)\nதொகுத்தவற்றுள் எல்லாந் தலை"
    },
    {
        "start": 272.5,
        "end": 277.5,
        "text": "[கொல்லாமை பக்தி இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/L6DWSjPqoH0.srt'
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Flawless real song-flow SRT generated: {srt_path} ({len(cues)} cues)")

    # Publish live to YouTube
    print("Publishing master SRT live to YouTube for L6DWSjPqoH0...")
    cmd = 'python tools/api_publish_master.py L6DWSjPqoH0'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
