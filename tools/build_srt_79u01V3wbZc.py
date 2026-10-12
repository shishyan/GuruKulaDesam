# -*- coding: utf-8 -*-
"""
tools/build_srt_79u01V3wbZc.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 78 - படைச்செருக்கு
YouTube ID: 79u01V3wbZc
Suno Track: 4d36e243-8bfd-4f31-8648-fd0caeb8ad59 (படைச்செருக்கு 1J Golden)
Duration: 228.39s (3m 48s)
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

# Suno Song Architecture for படைச்செருக்கு 1J Golden:
# 00:00 - 00:15: Invocatory Orchestral Introduction
# 00:15 - 00:44: [Chorus] பேராண்மை என்பது தறுகண் ஒன்று (உற்றக்கால்) ஊராண்மை மற்றதன் எஃகு (குறள் 773)
# 00:44 - 01:24: [Verse 1] என்னை முன்நில்லன்மின் தெவ்விர் பலர் என்னை முன்நின்று கல்நின்றவர் (குறள் 771)
#                கான முயல் எய்த அம்பினில் யானை பிழைத்த வேல் ஏந்தல் இனிது (குறள் 772)
#                கைவேல் களிற்றொடு போக்கி வருபவன்... சுழலும் இசைவேண்டி வேண்டா உயிரார்... (குறள் 774 & 778)
# 01:24 - 01:48: [Chorus Reprise 1] பேராண்மை என்பது தறுகண் ஒன்று ஊராண்மை மற்றதன் எஃகு
# 01:48 - 02:40: [Verse 2 / 3] விழித்தகண் வேல்கொண் டெறிய... புரந்தார்கண் நீர்மல்கச் சாகிற்... (குறள் 775, 776)
#                விழுப்புண் படாதநாள் எல்லாம்... உறின்உயிர் அஞ்சா மறவர்... இழைத்தது இகவாமைச்... (குறள் 777, 779, 780)
# 02:40 - 03:35: [Grand Chorus Finale & Reprise] பேராண்மை என்பது தறுகண் ஒன்று ஊராண்மை மற்றதன் எஃகு
# 03:35 - 03:48: Orchestral Outro & Finale

cues = [
    {
        "start": 3.0,
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 78: படைச்செருக்கு (Padaicherukku)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 15.0,
        "end": 29.5,
        "text": "[பல்லவி / Chorus]\nபேராண்மை என்பது தறுகண் ஒன்று (உற்றக்கால்)\nஊராண்மை மற்றதன் எஃகு (குறள் 773)"
    },
    {
        "start": 30.0,
        "end": 44.0,
        "text": "பேராண்மை என்பது தறுகண் ஒன்று (உற்றக்கால்)\nஊராண்மை மற்றதன் எஃகு (குறள் 773)"
    },
    # [Verse 1]
    {
        "start": 44.5,
        "end": 64.0,
        "text": "[சரணம் 1 / Verse 1]\nஎன்னை முன்நில்லன்மின் தெவ்விர் (பலர்)\nஎன்னை முன்நின்று கல்நின்றவர் (குறள் 771)"
    },
    {
        "start": 64.5,
        "end": 84.0,
        "text": "கான முயல் எய்த அம்பினில் (யானை)\nபிழைத்த வேல் ஏந்தல் இனிது (குறள் 772)"
    },
    {
        "start": 84.5,
        "end": 104.0,
        "text": "கைவேல் களிற்றொடு போக்கி (வருபவன்)\nமெய்வேல் பறியா நகும் (குறள் 774)"
    },
    {
        "start": 104.5,
        "end": 124.0,
        "text": "சுழலும் இசைவேண்டி வேண்டா (உயிரார்)\nகழல்யாப்புக் காரிகை நீர்த்து (குறள் 778)"
    },
    # [Chorus Reprise 1]
    {
        "start": 124.5,
        "end": 136.0,
        "text": "[பல்லவி / Chorus]\nபேராண்மை என்பது தறுகண் ஒன்று (உற்றக்கால்)\nஊராண்மை மற்றதன் எஃகு (குறள் 773)"
    },
    {
        "start": 136.5,
        "end": 148.0,
        "text": "பேராண்மை என்பது தறுகண் ஒன்று (உற்றக்கால்)\nஊராண்மை மற்றதன் எஃகு (குறள் 773)"
    },
    # [Verse 2 / 3]
    {
        "start": 148.5,
        "end": 168.0,
        "text": "[சரணம் 2 / Verse 2]\nவிழித்தகண் வேல்கொண் டெறிய (அழித்திமைப்பின்)\nஒட்டன்றோ வன்க ணவர்க்கே (குறள் 775)"
    },
    {
        "start": 168.5,
        "end": 188.0,
        "text": "புரந்தார்கண் நீர்மல்கச் சாகிற் (பின்தாக்காடு)\nஇரந்துகோள் தகுதியுடைத்து (குறள் 776)"
    },
    {
        "start": 188.5,
        "end": 208.0,
        "text": "விழுப்புண் படாதநாள் எல்லாம் (வழுக்கினுள்)\nவைக்கும்தன் நாளை எடுத்து (குறள் 777)"
    },
    {
        "start": 208.5,
        "end": 228.0,
        "text": "உறின்உயிர் அஞ்சா மறவர் (இறைவன்)\nசெறினும் சீர்குன்றல் இலர் (குறள் 779)"
    },
    {
        "start": 228.5,
        "end": 248.0,
        "text": "இழைத்தது இகவாமைச் சாவாரை (யாரே)\nபிழைத்தது ஒறுக்கிற் பவர் (குறள் 780)"
    },
    # [Grand Chorus Finale]
    {
        "start": 248.5,
        "end": 285.0,
        "text": "[நிறைவு / Finale]\nபேராண்மை என்பது தறுகண் ஒன்று (உற்றக்கால்)\nஊராண்மை மற்றதன் எஃகு (குறள் 773)"
    },
    {
        "start": 285.5,
        "end": 335.0,
        "text": "பேராண்மை என்பது தறுகண் ஒன்று (உற்றக்கால்)\nஊராண்மை மற்றதன் எஃகு (குறள் 773)"
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
    vid = "79u01V3wbZc"
    srt_content = generate_srt(cues)
    srt_path = f"production/subtitles/{vid}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Wrote master song-flow SRT to {srt_path} ({len(cues)} cues)")

    # Publish to YouTube
    print(f"Publishing master SRT live to YouTube for {vid}...")
    subprocess.run(f'python tools/api_publish_master.py "{vid}"', shell=True)
