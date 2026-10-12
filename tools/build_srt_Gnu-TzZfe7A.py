# -*- coding: utf-8 -*-
"""
tools/build_srt_Gnu-TzZfe7A.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 41 - கல்லாமை
YouTube ID: Gnu-TzZfe7A
Suno Track: 75d7c5d2-3577-4f60-8dd6-f94a889dcd89 (கல்லாமை Golden 2026)
Duration: 395.99s (6m 36s)
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
        "text": "திருக்குறள் — அதிகாரம் 41: கல்லாமை (Kallaamai / Ignorance)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 29.0,
        "end": 50.0,
        "text": "[பல்லவி / Chorus]\nநல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    {
        "start": 50.5,
        "end": 71.0,
        "text": "நல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    # [Verse 1]
    {
        "start": 72.0,
        "end": 88.0,
        "text": "[சரணம் 1 / Verse 1]\nமேற்பிறந்தா ராயினும் கல்லாதார் (கீழ்ப்பிறந்தும்)\nகற்றார் அனைத்திலர் பாடு (குறள் 409)"
    },
    {
        "start": 88.5,
        "end": 108.0,
        "text": "கல்லாதவரும் நனிநல்லர் (கற்றார்முன்)\nசொல்லாது இருக்கப் பெறின் (குறள் 403)"
    },
    # [Chorus Reprise 1]
    {
        "start": 133.0,
        "end": 146.0,
        "text": "[பல்லவி / Chorus Reprise]\nநல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    {
        "start": 146.5,
        "end": 165.0,
        "text": "நல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    # [Verse 2]
    {
        "start": 166.0,
        "end": 188.5,
        "text": "[சரணம் 2 / Verse 2]\nஉளரென்னும் மாத்திரையர் அல்லால் (பயவா)\nகளரனையர் கல்லா தவர் (குறள் 406)"
    },
    {
        "start": 189.0,
        "end": 203.5,
        "text": "கல்லாதான் ஒட்பம் கழியநன்று (ஆயினும்)\nகொள்ளார் அறிவுடை யார் (குறள் 404)"
    },
    {
        "start": 204.0,
        "end": 218.0,
        "text": "கல்லா ஒருவன் தகைமை (தலைப்பெய்து)\nசொல்லாட சோர்வு படும் (குறள் 405)"
    },
    {
        "start": 218.5,
        "end": 232.0,
        "text": "அரங்கின்றி வட்டு ஆடி அற்றே (நிரம்பிய)\nநூலின்றி கோட்டி கொளல் (குறள் 401)"
    },
    # [Chorus Reprise 2]
    {
        "start": 232.5,
        "end": 246.0,
        "text": "[பல்லவி / Chorus Reprise]\nநல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    {
        "start": 246.5,
        "end": 265.0,
        "text": "நல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    # [Verse 3]
    {
        "start": 276.0,
        "end": 306.0,
        "text": "[சரணம் 3 / Verse 3]\nவிலங்கொடு மக்கள் அனையர் (இலங்குநூல்)\nகற்றாரோடு ஏனை யவர் (குறள் 410)"
    },
    {
        "start": 307.0,
        "end": 322.5,
        "text": "நுண்மாண் நுழைபுலம் இல்லான் (எழில்நலம்)\nமண்மாண் புனைபாவை அற்று (குறள் 407)"
    },
    {
        "start": 323.0,
        "end": 330.5,
        "text": "கல்லாதான் சொற் காமுறுதல் (முலையிரண்டும்)\nஇல்லாதாள் பெண்காமுற் றற்று (குறள் 402)"
    },
    # [Grand Finale Chorus]
    {
        "start": 331.0,
        "end": 351.5,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nநல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    {
        "start": 352.0,
        "end": 375.0,
        "text": "நல்லார்கண் பட்ட வறுமையின் (இன்னாதே)\nகல்லார்கண் பட்ட திரு (குறள் 408)"
    },
    {
        "start": 375.5,
        "end": 395.0,
        "text": "நல்லார்கண் பட்ட வறுமையின் இன்னாதே கல்லார்கண் பட்ட திரு (குறள் 408)\n[இசை நிறைவு / Grand Musical Outro]"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/Gnu-TzZfe7A.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "Gnu-TzZfe7A"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
