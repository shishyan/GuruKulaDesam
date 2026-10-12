# -*- coding: utf-8 -*-
"""
tools/build_srt_dVYI3ZgpDC8.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 49 - காலமறிதல் (Remix/Pop)
YouTube ID: dVYI3ZgpDC8
Suno Track: 55e307c1-b50b-4da3-8165-521a4765aa3b (காலமறிதல் 1M Golden Pop)
Duration: 236.98s (3m 57s)
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
        "end": 14.0,
        "text": "திருக்குறள் — அதிகாரம் 49: காலமறிதல் (Kaalamaridhal / Knowing the Fitting Time)\n[செவ்வியல் திரை இசை / Classical Devotional Remix]"
    },
    # [Chorus 1]
    {
        "start": 14.5,
        "end": 29.5,
        "text": "[பல்லவி / Chorus]\nஅருவினை என்ப உளவோ (கருவியான்)\nகாலம் அறிந்து செயின் (குறள் 483)"
    },
    {
        "start": 30.0,
        "end": 44.5,
        "text": "அருவினை என்ப உளவோ (கருவியான்)\nகாலம் அறிந்து செயின் (குறள் 483)"
    },
    # [Verse 1]
    {
        "start": 45.0,
        "end": 58.0,
        "text": "[சரணம் 1 / Verse 1]\nஞாலம் கருதினும் கைகூடும் (காலம்)\nகருதி இடத்தால் செயின் (குறள் 484)"
    },
    {
        "start": 58.5,
        "end": 72.0,
        "text": "ஞாலம் கருதினும் கைகூடும் (காலம்)\nகருதி இடத்தால் செயின் (குறள் 484)"
    },
    {
        "start": 72.5,
        "end": 84.0,
        "text": "காலம் கருதி இருப்பர் (கலங்காது)\nஞாலம் கருதுபவர் (குறள் 485)"
    },
    {
        "start": 84.5,
        "end": 96.0,
        "text": "காலம் கருதி இருப்பர் (கலங்காது)\nஞாலம் கருதுபவர் (குறள் 485)"
    },
    # [Chorus Reprise 1]
    {
        "start": 96.5,
        "end": 108.0,
        "text": "[பல்லவி / Chorus Reprise]\nஅருவினை என்ப உளவோ (கருவியான்)\nகாலம் அறிந்து செயின் (குறள் 483)"
    },
    # [Bridge]
    {
        "start": 108.5,
        "end": 121.0,
        "text": "[இடைப்பகுதி / Bridge]\nபொள்ளென ஆங்கே புறம்வேரார் (காலம்பார்த்து)\nஉள்வேர்ப்பர் ஒள்ளி யவர் (குறள் 487)"
    },
    {
        "start": 121.5,
        "end": 133.0,
        "text": "செறுநரைக் காணின் சுமக்க (இறுவரை)\nகாணின் கிழக்காம் தலை (குறள் 488)"
    },
    {
        "start": 133.5,
        "end": 143.0,
        "text": "எய்தற்கு அரியது இயைந்தக்கால் (அந்நிலையே)\nசெய்தற்கு அரிய செயல் (குறள் 489)"
    },
    # [Chorus Reprise 2]
    {
        "start": 143.5,
        "end": 151.0,
        "text": "[பல்லவி / Chorus Reprise]\nஅருவினை என்ப உளவோ (கருவியான்)\nகாலம் அறிந்து செயின் (குறள் 483)"
    },
    {
        "start": 151.5,
        "end": 162.0,
        "text": "அருவினை என்ப உளவோ (கருவியான்)\nகாலம் அறிந்து செயின் (குறள் 483)"
    },
    # [Verse 2]
    {
        "start": 173.0,
        "end": 185.0,
        "text": "[சரணம் 2 / Verse 2]\nஊக்கம் உடையான் ஒடுக்கம் (பொருதகர்)\nதாக்கற்குப் பேரும் தகைத்து (குறள் 486)"
    },
    {
        "start": 185.5,
        "end": 194.0,
        "text": "கொக்கொக்க கூம்பும் பருவத்து (மற்றதன்)\nகுத்தொக்க சீர்த்த இடத்து (குறள் 490)"
    },
    {
        "start": 194.5,
        "end": 204.0,
        "text": "பகல்வெல்லும் கூகையைக் காக்கை (இகல்வெல்லும்)\nவேந்தர்க்கு வேண்டும் பொழுது (குறள் 481)"
    },
    {
        "start": 204.5,
        "end": 218.0,
        "text": "பருவத்தோடு ஒட்ட ஒழுகல் (திருவினை)\nதீராமை ஆர்க்கும் கயிறு (குறள் 482)"
    },
    # [Grand Finale Chorus]
    {
        "start": 218.5,
        "end": 236.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nஅருவினை என்ப உளவோ (கருவியான்)\nகாலம் அறிந்து செயின் (குறள் 483)"
    }
]

srt_lines = []
for i, cue in enumerate(cues, 1):
    start_str = to_srt_time(cue["start"])
    end_str = to_srt_time(cue["end"])
    srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{cue['text']}\n")

srt_content = "\n".join(srt_lines)

os.makedirs("production/subtitles", exist_ok=True)
out_srt = "production/subtitles/dVYI3ZgpDC8.srt"
with open(out_srt, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"Generated song-flow master SRT: {out_srt} ({len(cues)} cues)")

# Automatically publish live
print("\nPublishing live to YouTube...")
res = subprocess.run([sys.executable, "tools/api_publish_master.py", "dVYI3ZgpDC8"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
