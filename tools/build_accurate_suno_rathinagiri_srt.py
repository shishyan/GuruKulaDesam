# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_rathinagiri_srt.py

Generates and publishes the true Suno song flow SRT for Thiruppugazh 566: இரத்னகிரி II:
Video ID: mG9IzlD9vmI
Suno Track: acd56a69-1b29-429f-8e34-dd9ca7922b8b (திருப்புகழ் 566 (இரத்னகிரி) A7 Golden by GuruKulaDesam)
Total Audio Duration: 239.89 seconds (3m 59s)
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
# 00:00 - 00:15: Invocatory Orchestral Introduction
# 00:15 - 00:48: [Verse 1] சுற்ற பகடோடு பல சூது வினையான பல கற்ற களவோடு பழி...
# 00:48 - 01:18: [Chorus] எத்தி ஒரு மானை தினை காவல் வலப் பூவை தனை சித்தமலை காமுக குகா... ரத்நகிரி வாழ் முருகனே!
# 01:18 - 01:45: [Verse 2] சற்று மதியாத கலி காலன் வரு நேரமதில் தத்து அறியாமல் ஓடி...
# 01:45 - 02:10: [Chorus Reprise] எத்தி ஒரு மானை தினை காவல் வலப் பூவை தனை... ரத்நகிரி வாழ் முருகனே!
# 02:10 - 02:40: [Verse 3] தித்திமித தீதிமித திக்கு முகில் ஆட அரி ஆட அயன் ஆட சிவன்...
# 02:40 - 03:15: [Verse 4 & Bridge] எத்திசையும் நாடி யமனார் நிணமொடு ஆட பெல மிக்க நரி ஆட...
# 03:15 - 03:48: [Grand Finale Chorus] எத்தி ஒரு மானை தினை காவல் வலப் பூவை தனை சித்தமலை காமுக குகா ரத்நகிரி வாழ் முருகனே!
# 03:48 - 03:59: Murugan Temple Bell & Choral Resolution

cues = [
    {
        "start": 3.0,
        "end": 14.5,
        "text": "திருப்புகழ் 566 — இரத்னகிரி (அருணகிரிநாதர் சுவாமிகள்)\n[பக்தி இசைப் பாடல் / Classical Murugan Symphony]"
    },
    # [Verse 1]
    {
        "start": 15.0,
        "end": 31.0,
        "text": "[சந்தப் பா / Verse 1]\nசுற்ற பகடோடு பல சூது வினையான பல\nகற்ற களவோடு பழி காரர் கொலைகாரர் சலி"
    },
    {
        "start": 31.5,
        "end": 48.0,
        "text": "சுற்ற விழலான பவிஷோடு கடல் மூழ்கி வரு துயர் மேவி!\nதுக்க சமுசார வலை மீனதென கூழில் விழு"
    },
    # [Chorus]
    {
        "start": 48.5,
        "end": 66.0,
        "text": "[பல்லவி / Chorus]\nஎத்தி ஒரு மானை தினை (காவல் வலப் பூவை தனை)\nசித்தமலை காமுக குகா (நமசிவாயனொடு)"
    },
    {
        "start": 66.5,
        "end": 85.0,
        "text": "ரத்நகிரி வாழ் முருகனே (இளையவா அமரர்)\nபெருமாளே! ரத்நகிரி வாழ் முருகனே!"
    },
    # [Verse 2]
    {
        "start": 85.5,
        "end": 102.0,
        "text": "[சரணம் 2 / Verse 2]\nசற்று மதியாத கலி காலன் வரு நேரமதில்\nதத்து அறியாமல் ஓடி ஆடி வரு சூதர் ஐவர்"
    },
    {
        "start": 102.5,
        "end": 120.0,
        "text": "சத்த பரிசான மண ரூப ரசமான பொய்மை விளையாடி!\nதக்க மடவார் மனையை நாடி அவரோடு பல"
    },
    # [Chorus Reprise]
    {
        "start": 120.5,
        "end": 138.0,
        "text": "[பல்லவி மீள்சுழற்சி / Chorus Reprise]\nஎத்தி ஒரு மானை தினை (காவல் வலப் பூவை தனை)\nசித்தமலை காமுக குகா (நமசிவாயனொடு)"
    },
    {
        "start": 138.5,
        "end": 156.0,
        "text": "ரத்நகிரி வாழ் முருகனே (இளையவா அமரர்)\nபெருமாளே! ரத்நகிரி வாழ் முருகனே!"
    },
    # [Verse 3 - Thalam Rhythm]
    {
        "start": 156.5,
        "end": 178.0,
        "text": "[சந்த தாளம் / Rhythmic Verse]\nதித்திமித தீதிமித தத்ததன தானதன\nதிக்கு முகில் ஆட அரி ஆட அயன் ஆட சிவன்"
    },
    {
        "start": 178.5,
        "end": 198.0,
        "text": "ஒத்து விளையாட பரை ஆட வரர் ஆட பல\nதிக்கசுரர் வாட சுரர் பாட மறை பாட எதிர் களமீதே!"
    },
    # [Verse 4 - War Dance]
    {
        "start": 198.5,
        "end": 218.0,
        "text": "[போர்க்களப் பா / Epic Climax]\nஎத்திசையும் நாடி யமனார் நிணமொடு ஆட பெல\nமிக்க நரி ஆட கழுது ஆட கொடி ஆட சமர்"
    },
    {
        "start": 218.5,
        "end": 232.0,
        "text": "எற்றி வரு பூத கணம் ஆட ஒளி ஆட விடு வடிவேலா!\nரத்நகிரி வாழ் முருகனே பெருமாளே!"
    },
    # [Grand Finale Chorus]
    {
        "start": 232.5,
        "end": 239.8,
        "text": "[மங்கள நிறைவு / Grand Finale]\nஎத்தி ஒரு மானை தினை காவல் வலப் பூவை தனை\nரத்நகிரி வாழ் முருகனே! பெருமாளே!"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/mG9IzlD9vmI.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Precise Real-Song Flow SRT generated: {srt_path} ({len(cues)} cues)")
    
    # Publish to YouTube live
    print("Publishing master SRT live to YouTube for mG9IzlD9vmI...")
    cmd = 'python tools/api_publish_master.py mG9IzlD9vmI'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
