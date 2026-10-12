# -*- coding: utf-8 -*-
"""
tools/build_srt_dD_cXqU_XVQ.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 38 - ஊழ்
YouTube ID: dD_cXqU_XVQ
Suno Track: 9eb32aff-7079-4c68-a2b1-2919e45daab0 (ஊழ் 1 A)
Duration: 234.24s (3m 54s)
"""

import sys, json, os, subprocess

sys.stdout.reconfigure(encoding='utf-8')

def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# Suno Song Architecture for ஊழ் 1 A:
# 00:00 - 00:15: Invocatory Orchestral Introduction
# 00:15 - 00:46: [Chorus] நல்லவை எல்லாம் தீயவாம் (தீயவும்) நல்லவாம் செல்வம் செயற்கு (குறள் 375)
# 00:46 - 01:25: [Verse 1] வகுத்தான் வகுத்த வகையல்லால் (கோடி) தொகுத்தார்க்கு துய்த்தல் அரிது (குறள் 377)
#                நுண்ணிய நூல்பல கற்பினும்... ஆகூழால் தோன்றும் அசைவின்மை... பேதைப்படுக்கும் இழவூழ்... (குறள் 373, 371, 372)
# 01:25 - 01:48: [Chorus Reprise 1] நல்லவை எல்லாம் தீயவாம்... வகுத்தான் வகுத்த வகையல்லால்...
# 01:48 - 02:45: [Verse 2] இருவேறு உலகத்து இயற்கை... பரியினும் ஆகாவாம் பாலல்ல... (குறள் 374 & 376)
#                துறப்பார்மன் துப்புரவு இல்லார்... நன்றாங்கால் நல்லவாக் காண்பவர்... ஊழிற் பெருவலி யாவுள... (குறள் 378, 379, 380)
# 02:45 - 03:45: [Grand Chorus Finale & Reprise] நல்லவை எல்லாம் தீயவாம் நல்லவாம் செல்வம் செயற்கு
# 03:45 - 03:54: Orchestral Outro & Finale

cues = [
    {
        "start": 3.0,
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 38: ஊழ் (Oozh / Destiny)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 15.0,
        "end": 30.0,
        "text": "[பல்லவி / Chorus]\nநல்லவை எல்லாம் தீயவாம் (தீயவும்)\nநல்லவாம் செல்வம் செயற்கு (குறள் 375)"
    },
    {
        "start": 30.5,
        "end": 46.0,
        "text": "நல்லவை எல்லாம் தீயவாம் (தீயவும்)\nநல்லவாம் செல்வம் செயற்கு (குறள் 375)"
    },
    # [Verse 1]
    {
        "start": 46.5,
        "end": 64.0,
        "text": "[சரணம் 1 / Verse 1]\nவகுத்தான் வகுத்த வகையல்லால் (கோடி)\nதொகுத்தார்க்கு துய்த்தல் அரிது (குறள் 377)"
    },
    {
        "start": 64.5,
        "end": 84.0,
        "text": "நுண்ணிய நூல்பல கற்பினும் (மற்றும் தன்)\nஉண்மை அறிவே மிகும் (குறள் 373)"
    },
    {
        "start": 84.5,
        "end": 104.0,
        "text": "ஆகூழால் தோன்றும் அசைவின்மை (கைப்பொருள்)\nபோகூழால் தோன்றும் மடி (குறள் 371)"
    },
    {
        "start": 104.5,
        "end": 125.0,
        "text": "பேதைப் படுக்கும் இழவூழ் அறிவு (அகற்றும்)\nஆகலூழ் உற்றக் கடை (குறள் 372)"
    },
    # [Chorus Reprise 1]
    {
        "start": 125.5,
        "end": 136.0,
        "text": "[பல்லவி / Chorus]\nநல்லவை எல்லாம் தீயவாம் (தீயவும்)\nநல்லவாம் செல்வம் செயற்கு (குறள் 375)"
    },
    {
        "start": 136.5,
        "end": 148.0,
        "text": "வகுத்தான் வகுத்த வகையல்லால் (கோடி)\nதொகுத்தார்க்கு துய்த்தல் அரிது (குறள் 377)"
    },
    # [Verse 2]
    {
        "start": 148.5,
        "end": 170.0,
        "text": "[சரணம் 2 / Verse 2]\nஇருவேறு உலகத்து இயற்கை (திருவேறு)\nதெள்ளியர் ஆதலும் வேறு (குறள் 374)"
    },
    {
        "start": 170.5,
        "end": 192.0,
        "text": "பரியினும் ஆகாவாம் பாலல்ல (உய்த்து)\nசொரியினும் போகா தம (குறள் 376)"
    },
    {
        "start": 192.5,
        "end": 214.0,
        "text": "துறப்பார்மன் துப்புரவு இல்லார் (உறற்பால)\nஊட்டா கழியும் எனின் (குறள் 378)"
    },
    {
        "start": 214.5,
        "end": 236.0,
        "text": "நன்றாங்கால் நல்லவாக் காண்பவர் (அன்றாங்கால்)\nஅல்லற்படுவது எவன் (குறள் 379)"
    },
    {
        "start": 236.5,
        "end": 258.0,
        "text": "ஊழிற் பெருவலி யாவுள (மற்றொன்று)\nசூழினும் தான் முந்துறும் (குறள் 380)"
    },
    # [Grand Chorus Finale]
    {
        "start": 258.5,
        "end": 298.0,
        "text": "[நிறைவு / Finale]\nநல்லவை எல்லாம் தீயவாம் (தீயவும்)\nநல்லவாம் செல்வம் செயற்கு (குறள் 375)"
    },
    {
        "start": 298.5,
        "end": 348.0,
        "text": "வகுத்தான் வகுத்த வகையல்லால் (கோடி)\nதொகுத்தார்க்கு துய்த்தல் அரிது (குறள் 377)"
    }
]

def generate_srt(cues):
    lines = []
    for idx, cue in enumerate(cues, 1):
        s = to_srt_time(cue["start"])
        e = to_srt_time(cue["end"])
        lines.append(f"{idx}\n{s} --> {e}\n{cue['text']}\n")
    return "\n".join(lines)

if __name__ == "__main__":
    vid = "dD_cXqU_XVQ"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
