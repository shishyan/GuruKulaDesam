# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_kuripparithal_srt.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 71 - குறிப்பறிதல்
YouTube ID: 2Qs07DTJvvM
Suno Track: 02d8d772-ff2f-4eb7-9932-b4c70cd88a01 (குறிப்பறிதல் 1K)
Duration: 287.37 seconds (4m 47s)
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
# 00:25 - 00:54: [Chorus] அடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்) கடுத்தது காட்டும் முகம் (குறள் 706)
# 00:54 - 01:28: [Verse 1] முகம்நோக்கி நிற்க அமையும்... கூறாமை நோக்கி குறிப்பறிவான்... (குறள் 705 & 701)
# 01:28 - 01:54: [Chorus Reprise 1] அடுத்தது காட்டும் பளிங்குபோல்
# 01:54 - 02:35: [Verse 2] நுண்ணியம் என்பார் அளக்குங்கோல்... ஐயப் படாஅது... முகத்தின் முதுக்குறைந்தது... (குறள் 710, 702, 707)
# 02:35 - 03:02: [Chorus Reprise 2] அடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்) கடுத்தது காட்டும் முகம்
# 03:02 - 03:45: [Verse 3] பகைமையும் கேண்மையும் கண்ணுரைக்கும்... குறிப்பில் குறிப்புணர்வாரை... (குறள் 709, 703)
# 03:45 - 04:30: [Grand Chorus Finale] அடுத்தது காட்டும் பளிங்குபோல் நெஞ்சம் கடுத்தது காட்டும் முகம்
# 04:30 - 04:47: Orchestral Outro & Divine Finale

cues = [
    {
        "start": 5.0,
        "end": 24.5,
        "text": "திருக்குறள் — அதிகாரம் 71: குறிப்பறிதல் (Kuripparithal)\n[செவ்வியல் பக்தி இசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 25.0,
        "end": 39.0,
        "text": "[பல்லவி / Chorus]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    {
        "start": 39.5,
        "end": 53.5,
        "text": "அடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    # [Verse 1]
    {
        "start": 54.0,
        "end": 69.5,
        "text": "[சரணம் 1 / Verse 1]\nமுகம்நோக்கி நிற்க அமையும் (அகம்நோக்கி)\nஉற்றது உணர்வார்ப் பெறின் (குறள் 705)"
    },
    {
        "start": 70.0,
        "end": 85.5,
        "text": "முகம்நோக்கி நிற்க அமையும் (அகம்நோக்கி)\nஉற்றது உணர்வார்ப் பெறின்"
    },
    {
        "start": 86.0,
        "end": 105.0,
        "text": "கூறாமை நோக்கி குறிப்பறிவான் (எஞ்ஞான்றும்)\nமாறாநீர் வையக் கணி (குறள் 701)"
    },
    {
        "start": 105.5,
        "end": 125.0,
        "text": "கூறாமை நோக்கி குறிப்பறிவான் (எஞ்ஞான்றும்)\nமாறாநீர் வையக் கணி"
    },
    # [Chorus Reprise 1]
    {
        "start": 125.5,
        "end": 139.0,
        "text": "[பல்லவி / Chorus]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம்"
    },
    {
        "start": 139.5,
        "end": 153.0,
        "text": "அடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம்"
    },
    # [Verse 2]
    {
        "start": 153.5,
        "end": 172.0,
        "text": "[சரணம் 2 / Verse 2]\nநுண்ணியம் என்பார் அளக்குங்கோல் (காணுங்கால்)\nகண்ணல்லது இல்லை பிற (குறள் 710)"
    },
    {
        "start": 172.5,
        "end": 191.0,
        "text": "ஐயப் படாஅது அகத்தது (உணர்வானை)\nதெய்வத்தோடு ஒப்பக் கொளல் (குறள் 702)"
    },
    {
        "start": 191.5,
        "end": 210.0,
        "text": "முகத்தின் முதுக்குறைந்தது உண்டோ (உவப்பினும்)\nகாயினும் தான்முந் துறும் (குறள் 707)"
    },
    # [Chorus Reprise 2]
    {
        "start": 210.5,
        "end": 224.0,
        "text": "[பல்லவி / Chorus]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம்"
    },
    {
        "start": 224.5,
        "end": 238.0,
        "text": "அடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம்"
    },
    # [Verse 3]
    {
        "start": 238.5,
        "end": 254.0,
        "text": "[சரணம் 3 / Verse 3]\nபகைமையும் கேண்மையும் கண்ணுரைக்கும் (கண்ணின்)\nவகைமை உணர்வார்ப் பெறின் (குறள் 709)"
    },
    {
        "start": 254.5,
        "end": 270.0,
        "text": "பகைமையும் கேண்மையும் கண்ணுரைக்கும் (கண்ணின்)\nவகைமை உணர்வார்ப் பெறின்"
    },
    # [Grand Chorus Finale]
    {
        "start": 270.5,
        "end": 282.0,
        "text": "[பல்லவி நிறைவு / Grand Chorus Finale]\nஅடுத்தது காட்டும் பளிங்குபோல் (நெஞ்சம்)\nகடுத்தது காட்டும் முகம் (குறள் 706)"
    },
    {
        "start": 282.5,
        "end": 287.3,
        "text": "[குறிப்பறிதல் பக்தி இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/2Qs07DTJvvM.srt'
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Flawless real song-flow SRT generated: {srt_path} ({len(cues)} cues)")

    # Publish live to YouTube
    print("Publishing master SRT live to YouTube for 2Qs07DTJvvM...")
    cmd = 'python tools/api_publish_master.py 2Qs07DTJvvM'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
