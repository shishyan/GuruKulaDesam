# -*- coding: utf-8 -*-
"""
tools/build_srt_wPT_1jgn2Ys.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 28 - கூடா ஒழுக்கம்
YouTube ID: wPT_1jgn2Ys
Suno Track: 20ef6d30-07bd-4d2b-a870-010569134db8 (திருக்குறள் கூடா ஒழுக்கம் 1L Golden)
Duration: 282.17s (4m 42s)
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
        "start": 2.0,
        "end": 20.0,
        "text": "திருக்குறள் — அதிகாரம் 28: கூடா ஒழுக்கம் (Kooda Ozhukkam / False Conduct)\n[செவ்வியல் திரை இசை / Classical Devotional Film Song]"
    },
    # [Verse 1]
    {
        "start": 21.0,
        "end": 48.0,
        "text": "[சரணம் 1 / Verse 1]\nவலியில் நிலைமையான் வல்லுருவம் (பெற்றம்)\nபுலியின்தோல் போர்த்து மேய்ந்தற்று (குறள் 273)"
    },
    {
        "start": 48.5,
        "end": 64.0,
        "text": "பற்று அற்றேம் என்பார் படிற்று ஒழுக்கம் (எற்று எற்று)\nஎன்று ஏதம் பலவும் தரும் (குறள் 275)"
    },
    {
        "start": 64.5,
        "end": 80.0,
        "text": "புறம் குன்றி கண்டனையர் ஏனும் (அகம் குன்றி)\nமூக்கின் கரியார் உடைத்து (குறள் 277)"
    },
    # [Chorus 1]
    {
        "start": 81.0,
        "end": 96.0,
        "text": "[பல்லவி / Chorus]\nநெஞ்சில் துறவார் துறந்தார்போல் (வஞ்சித்து)\nவாழ்வாரின் வன்கணார் இல் (குறள் 276)"
    },
    {
        "start": 96.5,
        "end": 115.0,
        "text": "நெஞ்சில் துறவார் துறந்தார்போல் (வஞ்சித்து)\nவாழ்வாரின் வன்கணார் இல் (குறள் 276)"
    },
    # [Verse 2]
    {
        "start": 121.0,
        "end": 131.0,
        "text": "[சரணம் 2 / Verse 2]\nமனத்தது மாசாக மாண்டார் நீராடி (மறைந்து)\nஒழுகும் மாந்தர் பலர் (குறள் 278)"
    },
    {
        "start": 131.5,
        "end": 141.5,
        "text": "தவம் மறைந்து அல்லவை செய்தல் (புதல் மறைந்து)\nவேட்டுவன் புள் சிமிழ்த்தற்று (குறள் 274)"
    },
    {
        "start": 142.0,
        "end": 156.0,
        "text": "வஞ்ச மனத்தான் படிற்று ஒழுக்கம் (பூதங்கள்)\nஐந்தும் அகத்தே நகும் (குறள் 271)"
    },
    # [Chorus Reprise 1]
    {
        "start": 156.5,
        "end": 174.0,
        "text": "[பல்லவி / Chorus Reprise]\nநெஞ்சில் துறவார் துறந்தார்போல் (வஞ்சித்து)\nவாழ்வாரின் வன்கணார் இல் (குறள் 276)"
    },
    {
        "start": 174.5,
        "end": 195.0,
        "text": "நெஞ்சில் துறவார் துறந்தார்போல் (வஞ்சித்து)\nவாழ்வாரின் வன்கணார் இல் (குறள் 276)"
    },
    # [Verse 3]
    {
        "start": 199.0,
        "end": 209.0,
        "text": "[சரணம் 3 / Verse 3]\nகணை கொடிது யாழ்கோடு செவ்விது (ஆங்கு அன்ன)\nவினைபடு பாலால் கொளல் (குறள் 279)"
    },
    {
        "start": 209.5,
        "end": 218.0,
        "text": "மழித்தலும் நீட்டலும் வேண்டா (உலகம்)\nபழித்தது ஒழித்து விடின் (குறள் 280)"
    },
    {
        "start": 218.5,
        "end": 235.0,
        "text": "வானுயர் தோற்றம் எவன்செய்யும் (தன்னெஞ்சம்)\nதான்அறி குற்றப் படின் (குறள் 272)"
    },
    # [Grand Finale Chorus]
    {
        "start": 235.5,
        "end": 255.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nநெஞ்சில் துறவார் துறந்தார்போல் (வஞ்சித்து)\nவாழ்வாரின் வன்கணார் இல் (குறள் 276)"
    },
    {
        "start": 255.5,
        "end": 282.0,
        "text": "நெஞ்சில் துறவார் துறந்தார்போல் (வஞ்சித்து)\nவாழ்வாரின் வன்கணார் இல் (குறள் 276)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/wPT_1jgn2Ys.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "wPT_1jgn2Ys"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
