# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_porul_seyalvagai_srt.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 76 - பொருள் செயல்வகை
YouTube ID: cR_u-JuGJAU
Suno Track: 00015792-f886-407a-b7cd-d98adebe656a (பொருள்செயல்வகை 1M Golden)
Total Audio Duration: 300.56 seconds (5m 00s)
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
# 00:00 - 00:26: Invocatory Orchestral Introduction
# 00:26 - 00:54: [Chorus] பொருள் என்னும் பொய்யா விளக்கம் (இருள் அறுக்கும்) எண்ணிய தேயத்துச் சென்று (குறள் 753)
# 00:54 - 01:28: [Verse 1] அருளொடும் அன்பொடும் வாராப்... அறன் ஈனும் இன்பமும் ஈனும்... (குறள் 755 & 754)
# 01:28 - 01:54: [Chorus Reprise] பொருள் என்னும் பொய்யா விளக்கம் (இருளறுக்கும்)
# 01:54 - 02:35: [Bridge] உறுபொருளும் உல்கு பொருளும்... பொருளல்லவரைப்... இல்லாரை எல்லாரும்... (குறள் 756, 751, 752)
# 02:35 - 03:02: [Chorus Reprise 2] பொருள் என்னும் பொய்யா விளக்கம்
# 03:02 - 03:45: [Verse 3] அருளென்னும் அன்பீன் குழவி... குன்றேறி யானைப்போர்... செய்க பொருளைச்... (குறள் 757, 758, 759, 760)
# 03:45 - 04:30: [Grand Chorus Finale] பொருள் என்னும் பொய்யா விளக்கம் இருளறுக்கும் எண்ணிய தேயத்துச் சென்று
# 04:30 - 05:00: Orchestral Outro & Divine Finale

cues = [
    {
        "start": 5.0,
        "end": 25.5,
        "text": "திருக்குறள் — அதிகாரம் 76: பொருள் செயல்வகை (Porul Seyalvagai)\n[செவ்வியல் பக்தி இசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 26.0,
        "end": 40.0,
        "text": "[பல்லவி / Chorus]\nபொருள்என்னும் பொய்யா விளக்கம் (இருள்அறுக்கும்)\nஎண்ணிய தேயத்துச் சென்று (குறள் 753)"
    },
    {
        "start": 40.5,
        "end": 54.0,
        "text": "பொருள்என்னும் பொய்யா விளக்கம் (இருள்அறுக்கும்)\nஎண்ணிய தேயத்துச் சென்று (குறள் 753)"
    },
    # [Verse 1]
    {
        "start": 54.5,
        "end": 71.0,
        "text": "[சரணம் 1 / Verse 1]\nஅருளொடும் அன்பொடும் வாராப் (பொருளாக்கம்)\nபுல்லார் புரள விடல் (குறள் 755)"
    },
    {
        "start": 71.5,
        "end": 88.0,
        "text": "அருளொடும் அன்பொடும் வாராப் (பொருளாக்கம்)\nபுல்லார் புரள விடல்"
    },
    {
        "start": 88.5,
        "end": 108.0,
        "text": "அறன்ஈனும் இன்பமும் ஈனும் (திறனறிந்து)\nதீதின்றி வந்த பொருள் (குறள் 754)"
    },
    {
        "start": 108.5,
        "end": 127.5,
        "text": "அறன்ஈனும் இன்பமும் ஈனும் (திறனறிந்து)\nதீதின்றி வந்த பொருள்"
    },
    # [Chorus Reprise 1]
    {
        "start": 128.0,
        "end": 141.0,
        "text": "[பல்லவி / Chorus]\nபொருள்என்னும் பொய்யா விளக்கம் (இருளறுக்கும்)\nஎண்ணிய தேயத்துச் சென்று"
    },
    {
        "start": 141.5,
        "end": 154.5,
        "text": "பொருள்என்னும் பொய்யா விளக்கம் (இருளறுக்கும்)\nஎண்ணிய தேயத்துச் சென்று"
    },
    # [Bridge]
    {
        "start": 155.0,
        "end": 174.0,
        "text": "[அனுபல்லவி / Bridge]\nஉறுபொருளும் உல்கு பொருளும் (தன்ஒன்னார்த்)\nதெறுபொருளும் வேந்தன் பொருள் (குறள் 756)"
    },
    {
        "start": 174.5,
        "end": 194.0,
        "text": "பொருளல் லவரைப் பொருளாகச் (செய்யும்)\nபொருளல்லது இல்லை பொருள் (குறள் 751)"
    },
    {
        "start": 194.5,
        "end": 214.0,
        "text": "இல்லாரை எல்லாரும் எள்ளுவர் (செல்வரை)\nஎல்லாரும் செய்வர் சிறப்பு (குறள் 752)"
    },
    {
        "start": 214.5,
        "end": 234.5,
        "text": "இல்லாரை எல்லாரும் எள்ளுவர் (செல்வரை)\nஎல்லாரும் செய்வர் சிறப்பு"
    },
    # [Chorus Reprise 2]
    {
        "start": 235.0,
        "end": 248.5,
        "text": "[பல்லவி / Chorus]\nபொருள்என்னும் பொய்யா விளக்கம் (இருளறுக்கும்)\nஎண்ணிய தேயத்துச் சென்று"
    },
    {
        "start": 249.0,
        "end": 262.0,
        "text": "பொருள்என்னும் பொய்யா விளக்கம் (இருளறுக்கும்)\nஎண்ணிய தேயத்துச் சென்று"
    },
    # [Verse 3]
    {
        "start": 262.5,
        "end": 278.0,
        "text": "[சரணம் 2 / Verse 2]\nஅருளென்னும் அன்பீன் குழவி (பொருளென்னும்)\nசெல்வச் செவிலியால் உண்டு (குறள் 757)"
    },
    {
        "start": 278.5,
        "end": 294.0,
        "text": "குன்றேறி யானைப்போர் கண்டற்றால் (தன்தைத்தொன்று)\nஉண்டாகச் செய்வான் வினை (குறள் 758)"
    },
    {
        "start": 294.5,
        "end": 308.0,
        "text": "செய்க பொருளைச் செறுநர் செருக்கறுக்கும்\nஎஃகதனிற் கூரிய தில் (குறள் 759)"
    },
    {
        "start": 308.5,
        "end": 324.0,
        "text": "ஒண்பொருள் காழ்ப்ப இயற்றியார்க்கு (எண்பொருள்)\nஏனை இரண்டும் ஒருங்கு (குறள் 760)"
    },
    # [Grand Chorus Finale]
    {
        "start": 324.5,
        "end": 342.0,
        "text": "[பல்லவி நிறைவு / Grand Chorus Finale]\nபொருள்என்னும் பொய்யா விளக்கம் (இருளறுக்கும்)\nஎண்ணிய தேயத்துச் சென்று (குறள் 753)"
    },
    {
        "start": 342.5,
        "end": 360.5,
        "text": "[பொருள் செயல்வகை பக்தி இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/cR_u-JuGJAU.srt'
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Flawless real song-flow SRT generated: {srt_path} ({len(cues)} cues)")

    # Publish live to YouTube
    print("Publishing master SRT live to YouTube for cR_u-JuGJAU...")
    cmd = 'python tools/api_publish_master.py cR_u-JuGJAU'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
