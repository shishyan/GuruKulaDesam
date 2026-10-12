# -*- coding: utf-8 -*-
"""
tools/build_srt_irx33IVWrPY.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 75 - அரண்
YouTube ID: irx33IVWrPY
Suno Track: 84f3f779-4f2d-4f06-8a92-aae3b2e319c9 (அரண் 1V Golden)
Duration: 225.56s (3m 45s)
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
        "end": 14.5,
        "text": "திருக்குறள் — அதிகாரம் 75: அரண் (Aran / The Fortress)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 15.0,
        "end": 28.5,
        "text": "[பல்லவி / Chorus]\nஎல்லாப் பொருளும் உடைத்தாய் (இடத்துதவும்)\nநல்லாள் உடையது அரண் (குறள் 744)"
    },
    # [Verse 1]
    {
        "start": 29.0,
        "end": 42.5,
        "text": "[சரணம் 1 / Verse 1]\nமணிநீரும் மண்ணும் மலையும் (அணிநிழற்)\nகாடும் உடையது அரண் (குறள் 742)"
    },
    {
        "start": 43.0,
        "end": 52.0,
        "text": "எனைமாட்சித் தாகியக் கண்ணும் (வினைமாட்சி)\nஇல்லார்கண் இல்லதரண் (குறள் 750)"
    },
    {
        "start": 52.5,
        "end": 64.0,
        "text": "எனைமாட்சித் தாகியக் கண்ணும் (வினைமாட்சி)\nஇல்லார்கண் இல்லதரண் (குறள் 750)"
    },
    # [Chorus Reprise 1]
    {
        "start": 65.0,
        "end": 80.0,
        "text": "[பல்லவி / Chorus Reprise]\nஎல்லாப் பொருளும் உடைத்தாய் (இடத்துதவும்)\nநல்லாள் உடையது அரண் (குறள் 744)"
    },
    # Interlude
    # [Verse 2]
    {
        "start": 103.0,
        "end": 130.0,
        "text": "[சரணம் 2 / Verse 2]\nஆற்று பவர்க்கும் அரண் பொருள் (அஞ்சித்தற்)\nபோற்று பவர்க்கும் பொருள் (குறள் 741)"
    },
    {
        "start": 130.5,
        "end": 141.0,
        "text": "உயர்வகலம் திண்மை அருமை (இந் நான்கின்)\nஅமைவரண் என்றுரைக்கும் நூல் (குறள் 743)"
    },
    {
        "start": 141.5,
        "end": 148.5,
        "text": "கொளற்கரிதாய்க் கொண்டகூழ்த் தாகி (அகத்தார்)\nநிலைக்கெளிதாம் நீரது அரண் (குறள் 745)"
    },
    {
        "start": 149.0,
        "end": 156.5,
        "text": "சிறுகாப்பிற் பேரிடத்த தாகி (உறுபகை)\nஊக்கம் அழிப்பது அரண் (குறள் 746)"
    },
    # [Bridge]
    {
        "start": 157.0,
        "end": 164.5,
        "text": "[சரணம் 3 / Bridge]\nமுனைமுகத்து மாற்றலர் சாய (வினைமுகத்து)\nவீறெய்தி மாண்டது அரண் (குறள் 747)"
    },
    {
        "start": 165.0,
        "end": 173.0,
        "text": "முற்றியும் முற்றா தெறிந்தும் (அறைப்படுத்தும்)\nபற்றற் கரியது அரண் (குறள் 748)"
    },
    # [Grand Finale Chorus]
    {
        "start": 173.5,
        "end": 190.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nஎல்லாப் பொருளும் உடைத்தாய் (இடத்துதவும்)\nநல்லாள் உடையது அரண் (குறள் 744)"
    },
    {
        "start": 190.5,
        "end": 215.0,
        "text": "முற்றாற்றி முற்றி யவரையும் (பற்றாற்றிப்)\nபற்றியார் வெல்வது அரண் (குறள் 749)\nஎல்லாப் பொருளும் உடைத்தாய் இடத்துதவும் நல்லாள் உடையது அரண்"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/irx33IVWrPY.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "irx33IVWrPY"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
