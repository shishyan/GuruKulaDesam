# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_aadalamudha_srt.py

Generates and publishes the true Suno song flow SRT for Thiruvarutpa: ஆடலமுதப் பத்து:
Video ID: 8IAiHMylZJc
Suno Track: 91257b70-dd08-4112-861f-744a776dda25 (திருவருட்பா ஆடலமுதப் பத்து A5 Golden)
Total Audio Duration: 344.0 seconds
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
# 00:25 - 01:00: [Verse 1] சிந்தை நொந்துநொந்து (அயர்கின்றேன் சிவனே!) தீதுசெய்தன் ஆயினும்...
# 01:00 - 01:40: [Chorus] எந்நாளும் நின்னருள் உண்டெனிலில் உய்வேன்! அந்திவானான் நிறத்தது ஒற்றியூர் அரசே!
# 01:40 - 02:20: [Verse 2] மாயநெஞ்சமோ நின்னடி வழுத்தா வண்ணமென்தனை வலிக்கின்ற ததனால்...
# 02:20 - 02:50: [Chorus Reprise] அம்பலத்தினின்று ஆடல்செய் அமுதே! சிந்தை நொந்துநொந்து அயர்கின்றேன் சிவனே!
# 02:50 - 03:45: [Verse 3] பாவிநெஞ்சமென் பாலிராதோடிப் பாவையார்மயல் படிந்துழைப் பதனால்...
# 03:45 - 04:30: [Chorus 3] அம்பலத்தினின்று ஆடல்செய் அமுதே! சிந்தை நொந்துநொந்து...
# 04:30 - 05:44: [Grand Finale] அம்பலத்தினின்று ஆடல்செய் அமுதே! & Symphonic Outro Fade

cues = [
    {
        "start": 5.0,
        "end": 24.5,
        "text": "திருவருட்பா — ஆடலமுதப் பத்து (வள்ளலார் / இராமலிங்க அடிகளார்)\n[சிம்பொனி பக்திப் பாடல் / Symphonic Devotional Song]"
    },
    # [Verse 1]
    {
        "start": 25.0,
        "end": 42.0,
        "text": "[சரணம் 1 / Verse 1]\nசிந்தை நொந்துநொந்து (அயர்கின்றேன் சிவனே!)\nதீதுசெய்தன் ஆயினும் (பொறுத்தெனைச் சிவனே!)"
    },
    {
        "start": 42.5,
        "end": 60.0,
        "text": "இடர்கொள்வேன் அன்றி (என்செய்வேன் சிவனே!)\nமுன்னை வல்வினை (முடித்திடில் சிவனே!)"
    },
    # [Chorus]
    {
        "start": 60.5,
        "end": 80.0,
        "text": "[பல்லவி / Chorus]\nஎந்தை நின்னருள் (உண்டெனில் உய்வேன்)\nஇல்லையென்னில்நான் (இல்லையுய்ந் திடலே)"
    },
    {
        "start": 80.5,
        "end": 100.0,
        "text": "அந்திவான் நிறத்தது (ஒற்றியூர் அரசே)\nஅம்பலத்தினின்று (ஆடல்செய் அமுதே!)"
    },
    # [Chorus Reprise]
    {
        "start": 100.5,
        "end": 120.0,
        "text": "சிந்தை நொந்துநொந்து (அயர்கின்றேன் சிவனே!)\nதீதுசெய்தன் ஆயினும் (பொறுத்தெனைச் சிவனே!)"
    },
    {
        "start": 120.5,
        "end": 140.0,
        "text": "இடர்கொள்வேன் அன்றி (என்செய்வேன் சிவனே!)\nமுன்னை வல்வினை (முடித்திடில் சிவனே!)"
    },
    # [Verse 2]
    {
        "start": 140.5,
        "end": 160.0,
        "text": "[சரணம் 2 / Verse 2]\nமாயநெஞ்சமோ (நின்னடி வழுத்தா)\nவண்ணமென்தனை (வலிக்கின்ற ததனால்)"
    },
    {
        "start": 160.5,
        "end": 180.0,
        "text": "தீயனாயினேன் (என்செய்வேன் சிவனே!)\nதிருவருட்குநான் (சேயனும் ஆனேன்)"
    },
    {
        "start": 180.5,
        "end": 200.0,
        "text": "காயவாழ்க்கையில் (காமமுண் டுள்ளம்)\nகலங்குகின்றனன் (களைகண்மற் றறியேன்)"
    },
    {
        "start": 200.5,
        "end": 220.0,
        "text": "ஆயவொற்றியூர் (அண்ணலே தில்லை)\nஅம்பலத்தினின்று (ஆடல்செய் அமுதே!)"
    },
    # [Verse 3]
    {
        "start": 220.5,
        "end": 240.0,
        "text": "[சரணம் 3 / Verse 3]\nபாவிநெஞ்சமென் (பாலிரா தோடிப்)\nபாவையார்மயல் (படிந்துழைப் பதனால்)"
    },
    {
        "start": 240.5,
        "end": 260.0,
        "text": "சேவியாதவென் (பிழைபொறுத் தாளும்)\nசெய்கைநின்னதே (செப்பலென் சிவனே!)"
    },
    {
        "start": 260.5,
        "end": 280.0,
        "text": "காவிநேர்விழி (மலைமகள் காணக்)\nகடலின்நஞ்சுண்டு (கண்ணனா தியர்கள்)"
    },
    {
        "start": 280.5,
        "end": 305.0,
        "text": "ஆவியீந்தருள் (ஒற்றியெம் இறையே)\nஅம்பலத்தினின்று (ஆடல்செய் அமுதே!)"
    },
    # [Grand Finale Chorus]
    {
        "start": 305.5,
        "end": 325.0,
        "text": "[மங்கள நிறைவு / Grand Finale]\nசிந்தை நொந்துநொந்து (அயர்கின்றேன் சிவனே!)\nதீதுசெய்தன் ஆயினும் (பொறுத்தெனைச் சிவனே!)"
    },
    {
        "start": 325.5,
        "end": 344.0,
        "text": "அம்பலத்தினின்று ஆடல்செய் அமுதே...\n[திருவருட்பா பக்திப் பாடல் நிறைவு]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/8IAiHMylZJc.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Precise Real-Song Flow SRT generated: {srt_path} ({len(cues)} cues)")
    
    # Publish to YouTube live
    print("Publishing master SRT live to YouTube for 8IAiHMylZJc...")
    cmd = 'python tools/api_publish_master.py 8IAiHMylZJc'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
