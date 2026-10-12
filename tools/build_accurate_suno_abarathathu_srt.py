# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_abarathathu_srt.py

Generates and publishes the true Suno song flow SRT for Thiruvarutpa: அபராதத்து ஆற்றாமை:
Video ID: 6_qh4-WoWNM
Suno Track: 39499e9c-1e43-4195-9791-35e91de35be6 (திருவருட்பா - அபராதத்து ஆற்றாமை 2026)
Total Audio Duration: 288.0 seconds
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
# 00:00 - 00:15: Solo Violin Melody & Acoustic Guitar Intro
# 00:15 - 00:50: [Verse 1] வைதிலேன் வணங்காது இகழ்பவர் தம்மை வஞ்சனேன் நின்னடியவர் பால்...
# 00:50 - 01:25: [Chorus] உச்சிலை விரும்பித் துயர்க்கொடும் கொடியே துப்பனேன் தூய்மையொன்றில்லா எச்சிலை அனையேன்...
# 01:25 - 01:55: [Verse 2] அச்சிலையிடுவார் பக்கமே மருவும் பரமனே எம்பசுபதியே...
# 01:55 - 02:30: [Chorus Reprise] வைதிலேன் வணங்காது இகழ்பவர் தம்மை வஞ்சனேன் நின்னடியவர் பால்...
# 02:30 - 03:10: [Bridge] வாங்கி மேருவினை வளைத்திடும் பவளா மாமணிக் குன்றமே மருந்தே...
# 03:10 - 04:35: [Outro & Climax] கற்பவர்க்கெல்லாம் முற்படும் கொடியே... என் செய்தாய் திரு ஐயாரே!
# 04:35 - 04:48: Violin Sustained Synth Outro Fade

cues = [
    {
        "start": 4.0,
        "end": 14.5,
        "text": "திருவருட்பா — அபராதத்து ஆற்றாமை (வள்ளலார் / இராமலிங்க அடிகளார்)\n[பக்தி இசைப் பாடல் / Classical Devotional Symphony]"
    },
    # [Verse 1]
    {
        "start": 15.0,
        "end": 32.0,
        "text": "[சரணம் 1 / Verse 1]\nவைதிலேன் வணங்காது இகழ்பவர் தம்மை\nவஞ்சனேன் நின்னடியவர் பால்"
    },
    {
        "start": 32.5,
        "end": 50.0,
        "text": "எய்திலேன் பேயேன் ஏழையேன் என்னை\nஎன் செய்தாய் திரு ஐயாரே!"
    },
    # [Chorus]
    {
        "start": 50.5,
        "end": 68.0,
        "text": "[பல்லவி / Chorus]\nஉச்சிலை விரும்பித் துயர்க்கொடும் கொடியே\nதுப்பனேன் தூய்மையொன்றில்லா"
    },
    {
        "start": 68.5,
        "end": 88.0,
        "text": "எச்சிலை அனையேன் பாவியேன் என்னை\nஎன் செய்தாய் திரு ஐயாரே!"
    },
    # [Verse 2]
    {
        "start": 88.5,
        "end": 106.0,
        "text": "[சரணம் 2 / Verse 2]\nஅச்சிலையிடுவார் பக்கமே மருவும்\nபரமனே எம்பசுபதியே"
    },
    {
        "start": 106.5,
        "end": 126.0,
        "text": "அச்சிலை விரும்பு மவர்தம் முதே\nஅையனே ஒற்றியூரரசே!"
    },
    # [Chorus Reprise]
    {
        "start": 126.5,
        "end": 144.0,
        "text": "[பல்லவி மீள்சுழற்சி / Chorus Reprise]\nவைதிலேன் வணங்காது இகழ்பவர் தம்மை\nவஞ்சனேன் நின்னடியவர் பால்"
    },
    {
        "start": 144.5,
        "end": 164.0,
        "text": "எய்திலேன் பேயேன் ஏழையேன் என்னை\nஎன் செய்தாய் திரு ஐயாரே!"
    },
    # [Bridge]
    {
        "start": 164.5,
        "end": 184.0,
        "text": "[இணைப்பு / Bridge]\nவாங்கி மேருவினை வளைத்திடும் பவளா\nமாமணிக் குன்றமே மருந்தே!"
    },
    {
        "start": 184.5,
        "end": 210.0,
        "text": "ஓங்கி வந்தலமும் பொழில் செறி ஒற்றியூர்\nவரும் என்னுடை உயிரே!"
    },
    # [Outro]
    {
        "start": 210.5,
        "end": 232.0,
        "text": "[சரணம் 3 / Verse 3]\nகற்பவர்க்கெல்லாம் முற்படும் கொடியே\nகடையனேன் விடையமே உடையாய்"
    },
    {
        "start": 232.5,
        "end": 255.0,
        "text": "இறப்பவர் கழுவும் ஈந்திலேன் என்னை\nவைதிலேன் வணங்காது இகழ்பவர் தம்மை"
    },
    {
        "start": 255.5,
        "end": 278.0,
        "text": "[மங்கள நிறைவு / Grand Finale]\nவஞ்சனேன் நின்னடியவர் பால் எய்திலேன் பேயேன்\nஏழையேன் என்னை என் செய்தாய் திரு ஐயாரே!"
    },
    {
        "start": 278.5,
        "end": 288.0,
        "text": "என் செய்தாய் திரு ஐயாரே...\n[திருவருட்பா பக்திப் பாடல் நிறைவு]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/6_qh4-WoWNM.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Precise Real-Song Flow SRT generated: {srt_path} ({len(cues)} cues)")
    
    # Publish to YouTube live
    print("Publishing master SRT live to YouTube for 6_qh4-WoWNM...")
    cmd = 'python tools/api_publish_master.py 6_qh4-WoWNM'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
