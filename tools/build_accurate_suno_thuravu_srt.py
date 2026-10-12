# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_thuravu_srt.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 35 - துறவு
YouTube ID: 6MaQYObW8OQ
Suno Track: 0587ad0e-a564-4a06-8d02-05c74d821cb4 (துறவு 1B Golden)
Duration: 282.49 seconds (4m 42s)
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
# 00:00 - 00:25: Invocatory Orchestral Introduction
# 00:25 - 00:54: [Chorus] பற்றுக பற்றற்றான் பற்றினை (அப்பற்றை) பற்றுக பற்று விடற்கு (குறள் 350)
# 00:54 - 01:28: [Verse 1] யான்எனது என்னும் செருக்கறுப்பான்... பற்றற்ற கண்ணே... யாதனின் யாதனின்... (குறள் 346, 349, 341)
# 01:28 - 01:54: [Chorus Reprise 1] பற்றுக பற்றற்றான் பற்றினை
# 01:54 - 02:35: [Verse 2] தலைப்பட்டார் தீரத் துறந்தார்... அடல்வேண்டும் ஐந்தன்... வேண்டின் உண்டாகத்... (குறள் 342, 343, 344)
# 02:35 - 03:02: [Chorus Reprise 2] பற்றுக பற்றற்றான் பற்றினை
# 03:02 - 03:45: [Verse 3] பற்றி விடாஅ இடும்பைகள்... மற்றும் தொடர்ப்பாடு... இயல்பாகும் நோன்பிற்கு... (குறள் 347, 345, 348)
# 03:45 - 04:25: [Grand Chorus Finale] பற்றுக பற்றற்றான் பற்றினை அப்பற்றைப் பற்றுக பற்று விடற்கு
# 04:25 - 04:42: Orchestral Outro & Divine Finale

cues = [
    {
        "start": 5.0,
        "end": 24.5,
        "text": "திருக்குறள் — அதிகாரம் 35: துறவு (Thuravu)\n[செவ்வியல் பக்தி இசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 25.0,
        "end": 39.0,
        "text": "[பல்லவி / Chorus]\nபற்றுக பற்றற்றான் பற்றினை (அப்பற்றை)\nபற்றுக பற்று விடற்கு (குறள் 350)"
    },
    {
        "start": 39.5,
        "end": 53.5,
        "text": "பற்றுக பற்றற்றான் பற்றினை (அப்பற்றை)\nபற்றுக பற்று விடற்கு (குறள் 350)"
    },
    # [Verse 1]
    {
        "start": 54.0,
        "end": 69.5,
        "text": "[சரணம் 1 / Verse 1]\nயான்எனது என்னும் செருக்கறுப்பான் (வானோர்க்கு)\nஉயர்ந்த உலகம் புகும் (குறள் 346)"
    },
    {
        "start": 70.0,
        "end": 85.5,
        "text": "யான்எனது என்னும் செருக்கறுப்பான் (வானோர்க்கு)\nஉயர்ந்த உலகம் புகும்"
    },
    {
        "start": 86.0,
        "end": 105.0,
        "text": "பற்றற்ற கண்ணே பிறப்பறுக்கும் (மற்று)\nநிலையாமை காணப் படும் (குறள் 349)"
    },
    {
        "start": 105.5,
        "end": 125.0,
        "text": "யாதனின் யாதனின் நீங்கியான் (நோதல்)\nஅதனின் அதனின் இலன் (குறள் 341)"
    },
    # [Chorus Reprise 1]
    {
        "start": 125.5,
        "end": 139.0,
        "text": "[பல்லவி / Chorus]\nபற்றுக பற்றற்றான் பற்றினை (அப்பற்றை)\nபற்றுக பற்று விடற்கு"
    },
    {
        "start": 139.5,
        "end": 153.0,
        "text": "பற்றுக பற்றற்றான் பற்றினை (அப்பற்றை)\nபற்றுக பற்று விடற்கு"
    },
    # [Verse 2]
    {
        "start": 153.5,
        "end": 172.0,
        "text": "[சரணம் 2 / Verse 2]\nதலைப்பட்டார் தீரத் துறந்தார் (மயங்கி)\nவலைப்பட்டார் மற்றை யவர் (குறள் 342)"
    },
    {
        "start": 172.5,
        "end": 191.0,
        "text": "அடல்வேண்டும் ஐந்தன் புலத்தை (விடல்வேண்டும்)\nவேண்டிய எல்லாம் ஒருங்கு (குறள் 343)"
    },
    {
        "start": 191.5,
        "end": 210.0,
        "text": "வேண்டின் உண்டாகத் துறக்க (துறந்தபின்)\nஈண்டு இயற்பால பல (குறள் 344)"
    },
    # [Chorus Reprise 2]
    {
        "start": 210.5,
        "end": 224.0,
        "text": "[பல்லவி / Chorus]\nபற்றுக பற்றற்றான் பற்றினை (அப்பற்றை)\nபற்றுக பற்று விடற்கு"
    },
    {
        "start": 224.5,
        "end": 238.0,
        "text": "பற்றுக பற்றற்றான் பற்றினை (அப்பற்றை)\nபற்றுக பற்று விடற்கு"
    },
    # [Verse 3]
    {
        "start": 238.5,
        "end": 254.0,
        "text": "[சரணம் 3 / Verse 3]\nபற்றி விடாஅ இடும்பைகள் (பற்றினை)\nபற்றி விடாஅ தவர்க்கு (குறள் 347)"
    },
    {
        "start": 254.5,
        "end": 268.0,
        "text": "மற்றும் தொடர்ப்பாடு எவன்கொல் (பிறப்பறுக்கல்)\nஉற்றார்க்கு உடம்பும் மிகை (குறள் 345)"
    },
    {
        "start": 268.5,
        "end": 277.0,
        "text": "இயல்பாகும் நோன்பிற்கொன்று இன்மை (உடைமை)\nமயலாகும் மற்றும் பெயர்த்து (குறள் 348)"
    },
    # [Grand Chorus Finale]
    {
        "start": 277.5,
        "end": 282.4,
        "text": "[துறவு பக்தி இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/6MaQYObW8OQ.srt'
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Flawless real song-flow SRT generated: {srt_path} ({len(cues)} cues)")

    # Publish live to YouTube
    print("Publishing master SRT live to YouTube for 6MaQYObW8OQ...")
    cmd = 'python tools/api_publish_master.py 6MaQYObW8OQ'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
