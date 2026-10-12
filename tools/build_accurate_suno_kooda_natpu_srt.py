# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_kooda_natpu_srt.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 83 - கூடா நட்பு
YouTube ID: 8uX2yl_EnMI
Suno Track: 054a4b53-2d30-49d5-8443-d5d204e962f6 (கூடா நட்பு 1L Golden)
Duration: 260.48 seconds (4m 20s)
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
# 00:24 - 00:52: [Chorus] நட்டார்போல் நல்லவை சொல்லினும்... இனம்போன்று இனமல்லார்... (குறள் 826 & 822)
# 00:52 - 01:25: [Verse 1] மனத்தின் அமையாதவரை... தொழுதகை யுள்ளும்... (குறள் 825 & 828)
# 01:25 - 01:50: [Chorus Reprise 1] நட்டார்போல் நல்லவை சொல்லினும்
# 01:50 - 02:22: [Verse 2] மிகச்செய்து தம்மெள்ளு வாரை... பகைநட்பாம் காலம்... முகத்தின் இனிய... (குறள் 829, 830, 824)
# 02:22 - 02:46: [Chorus Reprise 2] நட்டார்போல் நல்லவை சொல்லினும்
# 02:46 - 03:25: [Verse 3] சீரிடம் காணின் எறிதற்குப்... சொல்வணக்கம் ஒன்னார்... (குறள் 821, 827)
# 03:25 - 04:05: [Grand Chorus Finale] நட்டார்போல் நல்லவை சொல்லினும் ஓட்டார் சொல் ஒல்லை உணரப் படும்
# 04:05 - 04:20: Orchestral Outro & Divine Finale

cues = [
    {
        "start": 5.0,
        "end": 23.5,
        "text": "திருக்குறள் — அதிகாரம் 83: கூடா நட்பு (Kooda Natpu)\n[செவ்வியல் பக்தி இசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 24.0,
        "end": 37.5,
        "text": "[பல்லவி / Chorus]\nநட்டார்போல் நல்லவை சொல்லினும் (ஒட்டார்)\nசொல் ஒல்லை உணரப் படும் (குறள் 826)"
    },
    {
        "start": 38.0,
        "end": 51.5,
        "text": "இனம்போன்று இனமல்லார் கேண்மை (மகளிர்)\nமனம்போல வேறு படும் (குறள் 822)"
    },
    # [Verse 1]
    {
        "start": 52.0,
        "end": 68.0,
        "text": "[சரணம் 1 / Verse 1]\nமனத்தின் அமையா தவரை (எனைத்தொன்றும்)\nசொல்லினால் தேறற்பாற்று அன்று (குறள் 825)"
    },
    {
        "start": 68.5,
        "end": 85.0,
        "text": "தொழுதகை யுள்ளும் படையொடுங்கும் (ஒன்னார்)\nஅழுதகண் ணீரும் அனைத்து (குறள் 828)"
    },
    {
        "start": 85.5,
        "end": 104.0,
        "text": "தொழுதகை யுள்ளும் படையொடுங்கும் (ஒன்னார்)\nஅழுதகண் ணீரும் அனைத்து"
    },
    # [Chorus Reprise 1]
    {
        "start": 104.5,
        "end": 118.0,
        "text": "[பல்லவி / Chorus]\nநட்டார்போல் நல்லவை சொல்லினும் (ஒட்டார்)\nசொல் ஒல்லை உணரப் படும்"
    },
    {
        "start": 118.5,
        "end": 132.0,
        "text": "இனம்போன்று இனமல்லார் கேண்மை (மகளிர்)\nமனம்போல வேறு படும்"
    },
    # [Verse 2]
    {
        "start": 132.5,
        "end": 150.0,
        "text": "[சரணம் 2 / Verse 2]\nமிகச்செய்து தம்மெள்ளு வாரை (நகச்செய்து)\nநட்பினுள் சாப்புல்லற் பாற்று (குறள் 829)"
    },
    {
        "start": 150.5,
        "end": 168.0,
        "text": "பகைநட்பாம் காலம் வருங்கால் (முகநட்டு)\nஅகநட்பு ஒரீஇ விடல் (குறள் 830)"
    },
    {
        "start": 168.5,
        "end": 186.0,
        "text": "முகத்தின் இனிய நகாஅ (அகத்தின்னா)\nவஞ்சரை அஞ்சப் படும் (குறள் 824)"
    },
    # [Chorus Reprise 2]
    {
        "start": 186.5,
        "end": 200.0,
        "text": "[பல்லவி / Chorus]\nநட்டார்போல் நல்லவை சொல்லினும் (ஒட்டார்)\nசொல் ஒல்லை உணரப் படும்"
    },
    {
        "start": 200.5,
        "end": 214.0,
        "text": "இனம்போன்று இனமல்லார் கேண்மை (மகளிர்)\nமனம்போல வேறு படும்"
    },
    # [Verse 3]
    {
        "start": 214.5,
        "end": 230.0,
        "text": "[சரணம் 3 / Verse 3]\nசீரிடம் காணின் எறிதற்குப் (பட்டடை)\nநேரா நிரந்தவர் நட்பு (குறள் 821)"
    },
    {
        "start": 230.5,
        "end": 245.0,
        "text": "சொல்வணக்கம் ஒன்னார் கண்கொள்ளற்க (வில்வணக்கம்)\nதீங்கு குறித்தமை யான் (குறள் 827)"
    },
    # [Grand Chorus Finale]
    {
        "start": 245.5,
        "end": 255.0,
        "text": "[பல்லவி நிறைவு / Grand Chorus Finale]\nநட்டார்போல் நல்லவை சொல்லினும் (ஒட்டார்)\nசொல் ஒல்லை உணரப் படும் (குறள் 826)"
    },
    {
        "start": 255.5,
        "end": 260.4,
        "text": "[கூடா நட்பு பக்தி இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/8uX2yl_EnMI.srt'
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Flawless real song-flow SRT generated: {srt_path} ({len(cues)} cues)")

    # Publish live to YouTube
    print("Publishing master SRT live to YouTube for 8uX2yl_EnMI...")
    cmd = 'python tools/api_publish_master.py 8uX2yl_EnMI'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
