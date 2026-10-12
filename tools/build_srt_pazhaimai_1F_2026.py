# -*- coding: utf-8 -*-
"""
tools/build_srt_pazhaimai_1F_2026.py

Generates accurate song-flow SRT for:
'பழைமை 1F Golden 2026.wav' (Duration: 318.5s / 5m 18s)
Matches authentic Suno vocal flow for Thirukkural Chapter 81: Pazhaimai (பழைமை).
"""

import sys, os

sys.stdout.reconfigure(encoding='utf-8')

def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# Total Duration: 318.50s (5m 18s)
cues = [
    {
        "start": 3.0,
        "end": 22.0,
        "text": "திருக்குறள் — அதிகாரம் 81: பழைமை (Pazhaimai / Ancient Friendship)\n[செவ்வியல் திரையிசைப் பாடல் / Classical Devotional Song 2026]"
    },
    # [Chorus 1]
    {
        "start": 23.0,
        "end": 42.0,
        "text": "[பல்லவி / Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    {
        "start": 42.5,
        "end": 60.0,
        "text": "பழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    # [Verse 1]
    {
        "start": 60.5,
        "end": 78.0,
        "text": "[சரணம் 1 / Verse 1]\nபழகிய நட்பெவன் செய்யுங் (கெழுதகைமை)\nசெய்தாங்கு அமையாக் கடை (குறள் 803)"
    },
    {
        "start": 78.5,
        "end": 96.0,
        "text": "பழகிய நட்பெவன் செய்யுங் (கெழுதகைமை)\nசெய்தாங்கு அமையாக் கடை (குறள் 803)"
    },
    {
        "start": 96.5,
        "end": 114.0,
        "text": "பேதைமை ஒன்றோ பெருங்கிழமை (என்றுணர்க)\nநோதக்க நட்டார் செயின் (குறள் 805)"
    },
    {
        "start": 114.5,
        "end": 132.0,
        "text": "பேதைமை ஒன்றோ பெருங்கிழமை (என்றுணர்க)\nநோதக்க நட்டார் செயின் (குறள் 805)"
    },
    # [Chorus Reprise 1]
    {
        "start": 132.5,
        "end": 146.0,
        "text": "[பல்லவி / Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    {
        "start": 146.5,
        "end": 160.0,
        "text": "பழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    # [Verse 2]
    {
        "start": 160.5,
        "end": 178.0,
        "text": "[சரணம் 2 / Verse 2]\nஅழிவந்த செய்யினும் அன்பறார் (அன்பின்)\nவழிவந்த கேண்மை யவர் (குறள் 807)"
    },
    {
        "start": 178.5,
        "end": 196.0,
        "text": "அழிவந்த செய்யினும் அன்பறார் (அன்பின்)\nவழிவந்த கேண்மை யவர் (குறள் 807)"
    },
    {
        "start": 196.5,
        "end": 214.0,
        "text": "கேளிழுக்கம் கேளாக் கெழுதகைமை (வல்லார்க்கு)\nநாளிழுக்கம் நட்டார் செயின் (குறள் 808)"
    },
    {
        "start": 214.5,
        "end": 232.0,
        "text": "விழைதகையான் வேண்டி இருப்பர் (கெழுதகையாற்)\nகேளாது நட்டார் செயின் (குறள் 804)"
    },
    # [Chorus Reprise 2]
    {
        "start": 232.5,
        "end": 245.0,
        "text": "[பல்லவி / Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    # [Verse 3]
    {
        "start": 245.5,
        "end": 262.0,
        "text": "[சரணம் 3 / Verse 3]\nஎல்லைக்கண் நின்றார் துறவார் (தொலைவிடத்தும்)\nதொல்லைக்கண் நின்றார் தொடர்பு (குறள் 806)"
    },
    {
        "start": 262.5,
        "end": 278.0,
        "text": "நட்பிற் குறுப்புக் கெழுதகைமை (மற்றதற்கு)\nஉப்பாதல் சான்றோர் கடன் (குறள் 802)"
    },
    {
        "start": 278.5,
        "end": 294.0,
        "text": "கெடாஅ வழிவந்த கேண்மையார் (கேண்மை)\nவிடாஅர் விழையும் உலகு (குறள் 809)"
    },
    {
        "start": 294.5,
        "end": 305.0,
        "text": "விழையார் விழையப் படுப (பழையார்கண்)\nபண்பின் தலைப்பிரியாதார் (குறள் 810)"
    },
    # [Grand Chorus Finale]
    {
        "start": 305.5,
        "end": 313.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    {
        "start": 313.5,
        "end": 318.0,
        "text": "பழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
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
    srt_content = generate_srt(cues)
    os.makedirs("production/subtitles", exist_ok=True)
    out_p = "production/subtitles/pazhaimai_1F_golden_2026.srt"
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Master song-flow SRT saved to: {out_p} ({len(cues)} cues)")
