# -*- coding: utf-8 -*-
"""
tools/build_srt_SWAjAbur-TQ.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 1 - கடவுள் வாழ்த்து
YouTube ID: SWAjAbur-TQ
Suno Track: 96a10819-3be3-46b9-849e-9c88bbf75cb0 (கடவுள் வாழ்த்து 2026)
Duration: 328.42s (5m 28s)
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

cues = [
    {
        "start": 3.0,
        "end": 28.0,
        "text": "திருக்குறள் — அதிகாரம் 1: கடவுள் வாழ்த்து (Kadavul Vaazhthu / Praise of God)\n[செவ்வியல் திரை இசை / Classical Devotional Film Song]"
    },
    # [Verse 1]
    {
        "start": 29.0,
        "end": 55.0,
        "text": "[சரணம் 1 / Verse 1]\nஅகர முதல எழுத்தெல்லாம்!\nஆதி பகவன் முதற்றே உலகு! (குறள் 1)"
    },
    {
        "start": 55.5,
        "end": 80.0,
        "text": "அகர முதல எழுத்தெல்லாம்!\nஆதி பகவன் முதற்றே உலகு! (குறள் 1)"
    },
    {
        "start": 80.5,
        "end": 105.0,
        "text": "கற்றதனால் ஆய பயன் என்கொல்!\nவாலறிவன் நற்றாள் தொழார் எனின்! (குறள் 2)"
    },
    # [Chorus 1]
    {
        "start": 106.0,
        "end": 125.0,
        "text": "[பல்லவி / Chorus]\nமலர்மிசை ஏகினான் மாணடி சேர்ந்தார்\nநிலமிசை நீடுவாழ் வார் (குறள் 3)"
    },
    {
        "start": 125.5,
        "end": 144.0,
        "text": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார்\nநிலமிசை நீடுவாழ் வார் (குறள் 3)"
    },
    # [Verse 2]
    {
        "start": 145.0,
        "end": 160.0,
        "text": "[சரணம் 2 / Verse 2]\nஅறவாழி அந்தணன் தாள்சேர்ந்தார்க் கல்லால்\nபிறவாழி நீந்தல் அரிது (குறள் 8)"
    },
    {
        "start": 160.5,
        "end": 168.5,
        "text": "பொறிவாயில் ஐந்தவித்தான் பொய்தீர் ஒழுக்க\nநெறிநின்றார் நீடுவாழ் வார் (குறள் 6)"
    },
    {
        "start": 169.0,
        "end": 174.5,
        "text": "இருள்சேர் இருவினையும் சேரா இறைவன்\nபொருள்சேர் புகழ்புரிந்தார் மாட்டு (குறள் 5)"
    },
    {
        "start": 175.0,
        "end": 184.0,
        "text": "வேண்டுதல் வேண்டாமை இலானடி சேர்ந்தார்க்கு\nயாண்டும் இடும்பை இல (குறள் 4)"
    },
    # [Chorus Reprise 1]
    {
        "start": 184.5,
        "end": 204.0,
        "text": "[பல்லவி / Chorus Reprise]\nமலர்மிசை ஏகினான் மாணடி சேர்ந்தார்\nநிலமிசை நீடுவாழ் வார் (குறள் 3)"
    },
    {
        "start": 204.5,
        "end": 220.0,
        "text": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார்\nநிலமிசை நீடுவாழ் வார் (குறள் 3)"
    },
    # [Verse 3]
    {
        "start": 238.0,
        "end": 249.5,
        "text": "[சரணம் 3 / Verse 3]\nகோளில் பொறியின் குணமிலவே எண்குணத்தான்\nதாளை வணங்காத் தலை (குறள் 9)"
    },
    {
        "start": 250.0,
        "end": 262.5,
        "text": "தனக்குவமை இல்லாதான் தாள்சேர்ந்தார்க் கல்லால்\nமனக்கவலை மாற்றல் அரிது (குறள் 7)"
    },
    {
        "start": 263.0,
        "end": 275.5,
        "text": "பிறவிப் பெருங்கடல் நீந்துவர் நீந்தார்\nஇறைவன் அடிசேரா தார் (குறள் 10)"
    },
    # [Grand Finale Chorus]
    {
        "start": 276.0,
        "end": 296.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nமலர்மிசை ஏகினான் மாணடி சேர்ந்தார்\nநிலமிசை நீடுவாழ் வார் (குறள் 3)"
    },
    {
        "start": 296.5,
        "end": 328.0,
        "text": "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார் நிலமிசை நீடுவாழ் வார் (குறள் 3)\n[இசை நிறைவு / Grand Musical Outro]"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/SWAjAbur-TQ.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "SWAjAbur-TQ"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
