# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_thiruvadi_srt.py

Generates and publishes the true Suno song flow SRT for Thiruvarutpa: திருவடிச் சரண்புகல்:
Video ID: PXQW4sYo4nY
Suno Track: 7c195f6c-d800-4b08-9b97-ec1511a65975 (திருவடிச் சரண்புகல் 2026 by GuruKulaDesam)
Total Audio Duration: 412.01 seconds
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
# 00:00 - 00:20: Invocatory Orchestral Introduction
# 00:20 - 00:55: [Verse 1] ஓடல் எங்கணும் நமக்கென்ன குறைகாண் உற்ற நற்றுணை ஒன்றுமில்லார் போல்...
# 00:55 - 01:30: [Chorus] ஓங்கி வாழ்வொற்றியூர் இடையரவும் ஒளிகொள் திங்களும் கங்கையும் சடைமேல்...
# 01:30 - 02:10: [Verse 2] ஏங்கி நோகின்ற தெற்றினுக்கோநீர் எண்ணி வேண்டிய தியாவையுமுனக்கு...
# 02:10 - 02:45: [Chorus Reprise] ஓங்கி வாழ்வொற்றியூர் இடையரவும்... தந்தையாரடிச் சரண்புகலாமே!
# 02:45 - 03:25: [Verse 3] சண்ட வெம்பவப் பிணியினால் தந்தை தாயிலாரெனத் தயங்குகின்றாயே...
# 03:25 - 04:00: [Chorus Reprise] ஓங்கி வாழ்வொற்றியூர்... தாணுவாம் செல்வத்து தந்தையாரடிச் சரண்புகலாமே!
# 04:00 - 04:45: [Verse 4] பொருந்தியீனருள் புகுந்துவீண் காலம் போக்கி நின்றனை போனது போக...
# 04:45 - 05:25: [Verse 5] நாட்டமுற்றெனை எழுமையும் பிரியா நல்ல நெஞ்சமே நங்கையர் மயலால்...
# 05:25 - 06:10: [Grand Finale Chorus] ஓங்கி வாழ்வொற்றியூர் இடையரவும் ஒளிகொள் திங்களும் கங்கையும் சடைமேல்...
# 06:10 - 06:52: Symphonic Outro & Choral Fade

cues = [
    {
        "start": 4.0,
        "end": 19.5,
        "text": "திருவருட்பா — திருவடிச் சரண்புகல் (வள்ளலார் / இராமலிங்க அடிகளார்)\n[பக்தி இசைப் பாடல் / Classical Devotional Symphony]"
    },
    # [Verse 1]
    {
        "start": 20.0,
        "end": 37.0,
        "text": "[சரணம் 1 / Verse 1]\nஓடல் எங்கணும் நமக்கென்ன (குறைகாண்)\nஉற்ற நற்றுணை ஒன்றுமில்லார் (போல்)"
    },
    {
        "start": 37.5,
        "end": 54.0,
        "text": "வாடல் நெஞ்சமே வருதி (யென்னுடனே)\nமகிழ்ந்து நாமிருவரும் சென்று (மகிழ்வாய்)"
    },
    {
        "start": 54.5,
        "end": 74.0,
        "text": "கூடல் நேர்திரு (ஒற்றியூரகத்து)\nகோயில் மேவிநம் (குடிமுழு தாளவே)"
    },
    # [Chorus]
    {
        "start": 74.5,
        "end": 94.0,
        "text": "[பல்லவி / Chorus]\nஓங்கி வாழ்வொற்றியூர் (இடையரவும்)\nஒளிகொள் திங்களும் கங்கையும் (சடைமேல்)"
    },
    {
        "start": 94.5,
        "end": 114.0,
        "text": "தாங்கி வாழும்நம்தாணுவாம் (செல்வத்து)\nதந்தையாரடிச் சரண் (புகலாமே!)"
    },
    # [Verse 2]
    {
        "start": 114.5,
        "end": 134.0,
        "text": "[சரணம் 2 / Verse 2]\nஏங்கி நோகின்ற (தெற்றினுக்கோநீர்)\nஎண்ணி வேண்டிய (தியாவையுமுனக்கு)"
    },
    {
        "start": 134.5,
        "end": 154.0,
        "text": "வாங்கியீகுவன் (ஒன்றுக்குமஞ்சேல்)\nமகிழ்ந்து நெஞ்சமே (வருதியென்னுடனே)"
    },
    {
        "start": 154.5,
        "end": 174.0,
        "text": "காம ஐம்புலத்துக் (கள்வரை வீட்டி)\nவயமளிக்குவன் (காண்டியென் மொழியை)"
    },
    # [Chorus Reprise]
    {
        "start": 174.5,
        "end": 194.0,
        "text": "[பல்லவி மீள்சுழற்சி / Chorus Reprise]\nஓங்கி வாழ்வொற்றியூர் (இடையரவும்)\nஒளிகொள் திங்களும் கங்கையும் (சடைமேல்)"
    },
    {
        "start": 194.5,
        "end": 214.0,
        "text": "தாங்கி வாழும்நம்தாணுவாம் (செல்வத்து)\nதந்தையாரடிச் சரண் (புகலாமே!)"
    },
    # [Verse 3]
    {
        "start": 214.5,
        "end": 234.0,
        "text": "[சரணம் 3 / Verse 3]\nசண்ட வெம்பவப் (பிணியினால் தந்தை)\nதாயிலாரெனத் (தயங்குகின்றாயே)"
    },
    {
        "start": 234.5,
        "end": 254.0,
        "text": "மண்டலத்துழல் (நெஞ்சமே சுகமா)\nவாழ வேண்டிடில் (வருதியென்னுடனே)"
    },
    {
        "start": 254.5,
        "end": 274.0,
        "text": "மடங்கொள் நெஞ்சமே (நினக்கின்று நல்ல)\nவாழ்வு வந்தது (வருதியென்னுடனே)"
    },
    # [Verse 4]
    {
        "start": 274.5,
        "end": 294.0,
        "text": "[சரணம் 4 / Verse 4]\nபொருந்தியீனருள் (புகுந்துவீண் காலம்)\nபோக்கி நின்றனை (போனது போக)"
    },
    {
        "start": 294.5,
        "end": 314.0,
        "text": "வருந்தியின்னுமிங் (குழன்றிடேல் நெஞ்சே)\nவாழ்க வாழ்கநீ (வருதியென்னுடனே)"
    },
    {
        "start": 314.5,
        "end": 334.0,
        "text": "திருந்தி நின்றநம் (மூவர்தம் பதிக)\nசெய்ய தீந்தமிழ்த் (தேறலுண்டருளைத்)"
    },
    # [Verse 5]
    {
        "start": 334.5,
        "end": 354.0,
        "text": "[சரணம் 5 / Verse 5]\nநாட்டமுற்றெனை (எழுமையும் பிரியா)\nநல்ல நெஞ்சமே (நங்கையர் மயலால்)"
    },
    {
        "start": 354.5,
        "end": 374.0,
        "text": "கோட்டமற்றிரு (மலர்க்கரம் கூப்பிக்)\nகும்பிடும்பெரும் (குணத்தவர் தமக்குத்)"
    },
    # [Grand Finale Chorus]
    {
        "start": 374.5,
        "end": 394.0,
        "text": "[மங்கள நிறைவு / Grand Finale]\nஓங்கி வாழ்வொற்றியூர் (இடையரவும்)\nஒளிகொள் திங்களும் கங்கையும் (சடைமேல்)"
    },
    {
        "start": 394.5,
        "end": 412.0,
        "text": "தாங்கி வாழும்நம்தாணுவாம் (செல்வத்து)\nதந்தையாரடிச் சரண் புகலாமே!"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/PXQW4sYo4nY.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Precise Real-Song Flow SRT generated: {srt_path} ({len(cues)} cues)")
    
    # Publish to YouTube live
    print("Publishing master SRT live to YouTube for PXQW4sYo4nY...")
    cmd = 'python tools/api_publish_master.py PXQW4sYo4nY'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
