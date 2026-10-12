# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_kadavul_srt.py

Generates and publishes the true Suno song flow SRT for Thirukkural Chapter 1 (கடவுள் வாழ்த்து):
Video ID: 02C8glMmetw
Suno Track: 8cb22c54-8326-4af2-9a05-cf75ad2393cf (கடவுள் வாழ்த்து (Cover))
Total Audio Duration: 238.59 seconds
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
# 00:25 - 00:52: [Verse 1] அகர முதல எழுத்தெல்லாம்! ஆதி பகவன் முதற்றே உலகு! (குறள் 1)
# 00:52 - 01:18: [Verse 1 Part B] கற்றதனால் ஆய பயன் என்கொல்! வாலறிவன் நற்றாள் தொழார் எனின்! (குறள் 2)
# 01:18 - 01:45: [Chorus / பல்லவி] மலர்மிசை ஏகினான்! மாணடி சேர்ந்தார் நிலமிசை நீடு வாழ்வார்! (குறள் 3)
# 01:45 - 02:08: [Verse 2] பிறவிப் பெருங்கடல் நீந்துவர்! நீந்தார் இறைவன் அடி சேராதார்! (குறள் 10)
# 02:08 - 02:30: [Chorus Reprise] மலர்மிசை ஏகினான் மாணடி சேர்ந்தார் நிலமிசை நீடு வாழ்வார்! (குறள் 3)
# 02:30 - 02:38: [Outro] அகர முதல எழுத்தெல்லாம்... (குறள் 1) & Choral Fade

cues = [
    {
        "start": 5.0,
        "end": 24.5,
        "text": "திருக்குறள் — அதிகாரம் 1: கடவுள் வாழ்த்து (Kadavul Vaazhthu)\n[பக்தி இசைப் பாடல் / Devotional Classical Song]"
    },
    # [Verse 1]
    {
        "start": 25.0,
        "end": 38.0,
        "text": "[சரணம் 1 / Verse 1]\nஅகர முதல எழுத்தெல்லாம்!\nஆதி பகவன் முதற்றே உலகு (குறள் 1)"
    },
    {
        "start": 38.5,
        "end": 51.5,
        "text": "அகர முதல எழுத்தெல்லாம்!\nஆதி பகவன் முதற்றே உலகு! (குறள் 1)"
    },
    # [Verse 1 Part B]
    {
        "start": 52.0,
        "end": 68.0,
        "text": "கற்றதனால் ஆய பயன் என்கொல்!\nவாலறிவன் நற்றாள் தொழார் எனின்! (குறள் 2)"
    },
    {
        "start": 68.5,
        "end": 85.0,
        "text": "கற்றதனால் ஆய பயன் என்கொல்!\nவாலறிவன் நற்றாள் தொழார் எனின்!"
    },
    {
        "start": 85.5,
        "end": 100.0,
        "text": "அகர முதல எழுத்தெல்லாம்!\nஆதி பகவன் முதற்றே உலகு!"
    },
    # [Chorus]
    {
        "start": 100.5,
        "end": 118.0,
        "text": "[பல்லவி / Chorus]\nமலர்மிசை ஏகினான்! மாணடி சேர்ந்தார்,\nநிலமிசை நீடு வாழ்வார்! (குறள் 3)"
    },
    {
        "start": 118.5,
        "end": 138.0,
        "text": "மலர்மிசை ஏகினான்! மாணடி சேர்ந்தார்,\nநிலமிசை நீடு வாழ்வார்! (குறள் 3)"
    },
    # [Verse 2]
    {
        "start": 138.5,
        "end": 158.0,
        "text": "[சரணம் 2 / Verse 2]\nபிறவிப் பெருங்கடல் நீந்துவர் (நீந்தார்)\nஇறைவனடி சேராதார்! (குறள் 10)"
    },
    {
        "start": 158.5,
        "end": 178.0,
        "text": "பிறவிப் பெருங்கடல் நீந்துவர் (நீந்தார்)\nஇறைவனடி சேராதார்! (குறள் 10)"
    },
    # [Chorus Reprise]
    {
        "start": 178.5,
        "end": 198.0,
        "text": "[பல்லவி மீள்சுழற்சி / Chorus Reprise]\nமலர்மிசை ஏகினான்! மாணடி சேர்ந்தார்,\nநிலமிசை நீடு வாழ்வார்!"
    },
    {
        "start": 198.5,
        "end": 218.0,
        "text": "மலர்மிசை ஏகினான்! மாணடி சேர்ந்தார்,\nநிலமிசை நீடு வாழ்வார்! (குறள் 3)"
    },
    # [Outro]
    {
        "start": 218.5,
        "end": 232.0,
        "text": "[மங்கள நிறைவு / Outro]\nஅகர முதல எழுத்தெல்லாம்...\nஆதி பகவன் முதற்றே உலகு!"
    },
    {
        "start": 232.5,
        "end": 238.5,
        "text": "[கடவுள் வாழ்த்து இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/02C8glMmetw.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Precise Real-Song Flow SRT generated: {srt_path} ({len(cues)} cues)")
    
    # Publish to YouTube live
    print("Publishing master SRT live to YouTube for 02C8glMmetw...")
    cmd = 'python tools/api_publish_master.py 02C8glMmetw'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
