# -*- coding: utf-8 -*-
"""
tools/build_srt_jdvz_yoK5eI.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 79 - நட்பு (Remix/Film)
YouTube ID: jdvz-yoK5eI
Suno Track: 9ec07734-49df-4176-89bd-dae9e51fbf22 (நட்பு 1A)
Duration: 269.72s (4m 30s)
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
        "text": "திருக்குறள் — அதிகாரம் 79: நட்பு (Natpu / Friendship)\n[செவ்வியல் திரை இசை / Classical Devotional Remix]"
    },
    # [Chorus 1]
    {
        "start": 21.0,
        "end": 44.5,
        "text": "[பல்லவி / Chorus]\nமுகநக நட்பது நட்பன்று (நெஞ்சத்து)\nஅகநக நட்பது நட்பு (குறள் 786)"
    },
    # [Verse 1]
    {
        "start": 45.0,
        "end": 68.0,
        "text": "[சரணம் 1 / Verse 1]\nஉடுக்கை இழந்தவன் கைபோல (ஆங்கே)\nஇடுக்கண் களைவதாம் நட்பு (குறள் 788)"
    },
    {
        "start": 68.5,
        "end": 92.0,
        "text": "நிறைநீர நீரவர் கேண்மை (பிறைமதி)\nபின்னீர பேதையார் நட்பு (குறள் 782)"
    },
    # [Chorus Reprise 1]
    {
        "start": 92.5,
        "end": 109.5,
        "text": "[பல்லவி / Chorus Reprise]\nமுகநக நட்பது நட்பன்று (நெஞ்சத்து)\nஅகநக நட்பது நட்பு (குறள் 786)"
    },
    # [Verse 2]
    {
        "start": 110.0,
        "end": 134.0,
        "text": "[சரணம் 2 / Verse 2]\nஇனையர் இவரெமக்கு இன்னம்யாம் (என்று)\nபுனையினும் புல்லென்னும் நட்பு (குறள் 790)"
    },
    {
        "start": 134.5,
        "end": 160.0,
        "text": "அழிவினவை நீக்கி ஆறுய்த்து (அழிவின்கண்)\nஅல்லல் உழப்பதாம் நட்பு (குறள் 787)"
    },
    # [Chorus Reprise 2]
    {
        "start": 160.5,
        "end": 182.0,
        "text": "[பல்லவி / Chorus Reprise]\nமுகநக நட்பது நட்பன்று (நெஞ்சத்து)\nஅகநக நட்பது நட்பு (குறள் 786)"
    },
    # [Verse 3 / Bridge]
    {
        "start": 182.5,
        "end": 204.0,
        "text": "[சரணம் 3 / Verse 3]\nசெயற்கரிய யாவுள நட்பின் (அதுபோல்)\nவினைக்கரிய யாவுள காப்பு (குறள் 781)"
    },
    {
        "start": 204.5,
        "end": 218.0,
        "text": "நவில்தொறும் நூல்நயம் போலும் (பயில்தொறும்)\nபண்புடை யாளர் தொடர்பு (குறள் 783)"
    },
    {
        "start": 218.5,
        "end": 230.5,
        "text": "நகுதற் பொருட்டன்று நட்டல் (மிகுதிக்கண்)\nமேற்சென்று இடித்தற் பொருட்டு (குறள் 784)"
    },
    {
        "start": 231.0,
        "end": 239.5,
        "text": "புணர்ச்சி பழகுதல் வேண்டா (உணர்ச்சிதான்)\nநட்பாங் கிழமை தரும் (குறள் 785)\nநட்பிற்கு வீற்றிருக்கை யாதெனின் ஒல்லும்வாய் ஊன்றும் நிலை (குறள் 789)"
    },
    # [Grand Finale Chorus]
    {
        "start": 240.0,
        "end": 269.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nமுகநக நட்பது நட்பன்று (நெஞ்சத்து)\nஅகநக நட்பது நட்பு (குறள் 786)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/jdvz-yoK5eI.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "jdvz-yoK5eI"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
