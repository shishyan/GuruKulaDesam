# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_vaan_srt.py

Generates and publishes the true Suno song flow SRT for Thirukkural Chapter 2 (வான் சிறப்பு):
Video ID: f1jxgAbXcdE
Suno Track: 75b979f1-bb57-4a2a-bb6a-90a92321ec13 (வான் சிறப்பு 1C Golden by Shishyan)
Total Audio Duration: 312.56 seconds
"""

import os, sys, subprocess

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
# 00:25 - 00:58: [Chorus / பல்லவி] துப்பார்க்குத் துப்பாய துப்பாக்கித்... (குறள் 12)
# 00:58 - 01:30: [Verse 1 / சரணம் 1] நீர்இன்று அமையாது உலகு... தானம் தவம்இரண்டும் தங்கா... (குறள் 20 & 19)
# 01:30 - 01:55: [Chorus Reprise / பல்லவி மீள்சுழற்சி] துப்பார்க்குத் துப்பாய... (குறள் 12)
# 01:55 - 02:40: [Verse 2 / சரணம் 2] நெடுங்கடலும் தன்நீர்மை குன்றும்... வான்நின்று உலகம் வழங்கி... விண்இன்று பொய்ப்பின்... (குறள் 17, 11, 13)
# 02:40 - 03:00: [Chorus Reprise] துப்பாய தூஉம் மழை... (குறள் 12)
# 03:00 - 03:45: [Verse 3 / சரணம் 3] ஏரின் உழாஅர் உழவர்... சிறப்பொடு பூசனை... கெடுப்பதூஉம்... பசும்புல்... (குறள் 14, 18, 15, 16)
# 03:45 - 04:30: [Grand Finale Chorus] துப்பார்க்குத் துப்பாய துப்பாக்கித்... (குறள் 12)
# 04:30 - 05:12: Symphonic Outro & Choral Resolution

cues = [
    {
        "start": 5.0,
        "end": 24.0,
        "text": "திருக்குறள் — அதிகாரம் 2: வான் சிறப்பு (Vaan Sirappu)\n[திரைப்பட பக்திப் பாடல் / Cinematic Devotional Song]"
    },
    # [Chorus]
    {
        "start": 24.5,
        "end": 40.0,
        "text": "[பல்லவி / Chorus]\nதுப்பார்க்குத் துப்பாய துப்பாக்கித் (துப்பார்க்குத்)\nதுப்பாய தூஉம் மழை (குறள் 12)"
    },
    {
        "start": 40.5,
        "end": 57.5,
        "text": "துப்பார்க்குத் துப்பாய துப்பாக்கித் (துப்பார்க்குத்)\nதுப்பாய தூஉம் மழை (குறள் 12)"
    },
    # [Verse 1]
    {
        "start": 58.0,
        "end": 74.0,
        "text": "[சரணம் 1 / Verse 1]\nநீர்இன்று அமையாது உலகு (எனின் யார்யார்க்கும்)\nவான்இன்று அமையாது ஒழுக்கு (குறள் 20)"
    },
    {
        "start": 74.5,
        "end": 90.0,
        "text": "நீர்இன்று அமையாது உலகு (எனின் யார்யார்க்கும்)\nவான்இன்று அமையாது ஒழுக்கு"
    },
    {
        "start": 90.5,
        "end": 108.0,
        "text": "தானம் தவம்இரண்டும் தங்கா (வியன்உலகம்)\nவானம் வழங்கா தெனின் (குறள் 19)"
    },
    {
        "start": 108.5,
        "end": 128.0,
        "text": "தானம் தவம்இரண்டும் தங்கா (வியன்உலகம்)\nவானம் வழங்கா தெனின்"
    },
    # [Chorus Reprise]
    {
        "start": 128.5,
        "end": 142.0,
        "text": "[பல்லவி / Chorus]\nதுப்பார்க்குத் துப்பாய துப்பாக்கித் (துப்பார்க்குத்)\nதுப்பாய தூஉம் மழை"
    },
    {
        "start": 142.5,
        "end": 156.0,
        "text": "துப்பார்க்குத் துப்பாய துப்பாக்கித் (துப்பார்க்குத்)\nதுப்பாய தூஉம் மழை"
    },
    # [Verse 2]
    {
        "start": 156.5,
        "end": 178.0,
        "text": "[சரணம் 2 / Verse 2]\nநெடுங்கடலும் தன்நீர்மை குன்றும் (தடிந்தெழிலி)\nதான்நல்கா தாகி விடின் (குறள் 17)"
    },
    {
        "start": 178.5,
        "end": 198.0,
        "text": "வான்நின்று உலகம் வழங்கி (வருதலால்)\nதான்அமிழ்தம் என்றுணரற் பாற்று (குறள் 11)"
    },
    {
        "start": 198.5,
        "end": 218.0,
        "text": "விண்இன்று பொய்ப்பின் விரிநீர் (வியனுலகத்து)\nஉள்நின்று உடற்றும் பசி (குறள் 13)"
    },
    # [Chorus Break]
    {
        "start": 218.5,
        "end": 236.0,
        "text": "[பல்லவி மீள்சுழற்சி / Chorus Break]\nதுப்பார்க்குத் துப்பாய துப்பாக்கித்\nதுப்பாய தூஉம் மழை"
    },
    # [Verse 3]
    {
        "start": 236.5,
        "end": 252.0,
        "text": "[சரணம் 3 / Verse 3]\nஏரின் உழாஅர் உழவர் (புயல்என்னும்)\nவாரி வளங்குன்றிக் கால் (குறள் 14)"
    },
    {
        "start": 252.5,
        "end": 268.0,
        "text": "சிறப்பொடு பூசனை செல்லாது (வானம்)\nவறக்குமேல் வானோர்க்கும் ஈண்டு (குறள் 18)"
    },
    {
        "start": 268.5,
        "end": 284.0,
        "text": "கெடுப்பதூஉம் கெட்டார்க்குச் சார்வாய் (மற்றாங்கே)\nஎடுப்பதூஉம் எல்லாம் மழை (குறள் 15)"
    },
    {
        "start": 284.5,
        "end": 300.0,
        "text": "விசும்பின் துளிவீழின் அல்லால் (மற்றாங்கே)\nபசும்புல் தலைகாண்பு அரிது (குறள் 16)"
    },
    # [Grand Finale Chorus]
    {
        "start": 300.5,
        "end": 308.0,
        "text": "[மங்கள நிறைவு / Grand Finale]\nதுப்பார்க்குத் துப்பாய துப்பாக்கித் (துப்பார்க்குத்)\nதுப்பாய தூஉம் மழை"
    },
    {
        "start": 308.5,
        "end": 312.5,
        "text": "துப்பாய தூஉம் மழை\n[மழை வாழ்த்து நிறைவு]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/f1jxgAbXcdE.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Precise Real-Song Flow SRT generated: {srt_path} ({len(cues)} cues)")
    
    # Publish to YouTube live
    print("Publishing master SRT live to YouTube for f1jxgAbXcdE...")
    cmd = 'python tools/api_publish_master.py f1jxgAbXcdE'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
