# -*- coding: utf-8 -*-
"""
tools/build_srt_pazhaimai_1H_pop.py

Generates accurate song-flow SRT for:
'பழைமை 1H Golden Pop (1).wav' (Duration: 317.6s / 5m 17s)
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

# Total Duration: 317.60s (5m 17s)
cues = [
    {
        "start": 3.0,
        "end": 20.0,
        "text": "திருக்குறள் — அதிகாரம் 81: பழைமை (Pazhaimai / Ancient Friendship)\n[செவ்வியல் துள்ளலிசைப் பாடல் / Classical Golden Pop 2026]"
    },
    # [Chorus 1]
    {
        "start": 21.0,
        "end": 40.0,
        "text": "[பல்லவி / Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    {
        "start": 40.5,
        "end": 58.0,
        "text": "பழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    # [Verse 1]
    {
        "start": 58.5,
        "end": 76.0,
        "text": "[சரணம் 1 / Verse 1]\nபழகிய நட்பெவன் செய்யுங் (கெழுதகைமை)\nசெய்து ஆங்கு அமையாக் கடை (குறள் 803)"
    },
    {
        "start": 76.5,
        "end": 94.0,
        "text": "பழகிய நட்பெவன் செய்யுங் (கெழுதகைமை)\nசெய்து ஆங்கு அமையாக் கடை (குறள் 803)"
    },
    {
        "start": 94.5,
        "end": 112.0,
        "text": "பேதைமை ஒன்றோ பெருங்கிழமை (என்றுணர்க)\nநோதக்க நட்டார் செயின் (குறள் 805)"
    },
    {
        "start": 112.5,
        "end": 130.0,
        "text": "பேதைமை ஒன்றோ பெருங்கிழமை (என்றுணர்க)\nநோதக்க நட்டார் செயின் (குறள் 805)"
    },
    # [Chorus Reprise 1]
    {
        "start": 130.5,
        "end": 144.0,
        "text": "[பல்லவி / Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    {
        "start": 144.5,
        "end": 158.0,
        "text": "பழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    # [Verse 2]
    {
        "start": 158.5,
        "end": 176.0,
        "text": "[சரணம் 2 / Verse 2]\nஅழிவந்த செய்யினும் அன்பறார் (அன்பின்)\nவழிவந்த கேண்மை யவர் (குறள் 807)"
    },
    {
        "start": 176.5,
        "end": 194.0,
        "text": "அழிவந்த செய்யினும் அன்பறார் (அன்பின்)\nவழிவந்த கேண்மை யவர் (குறள் 807)"
    },
    {
        "start": 194.5,
        "end": 212.0,
        "text": "கேளிழுக்கம் கேளாக் கெழுதகைமை (வல்லார்க்கு)\nநாளிழுக்கம் நட்டார் செயின் (குறள் 808)"
    },
    {
        "start": 212.5,
        "end": 230.0,
        "text": "விழைதகையான் வேண்டி இருப்பர் (கெழுதகையாற்)\nகேளாது நட்டார் செயின் (குறள் 804)"
    },
    # [Chorus Reprise 2]
    {
        "start": 230.5,
        "end": 243.0,
        "text": "[பல்லவி / Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    # [Verse 3]
    {
        "start": 243.5,
        "end": 260.0,
        "text": "[சரணம் 3 / Verse 3]\nஎல்லைக்கண் நின்றார் துறவார் (தொலைவிடத்தும்)\nதொல்லைக்கண் நின்றார் தொடர்பு (குறள் 806)"
    },
    {
        "start": 260.5,
        "end": 276.0,
        "text": "நட்பிற் குறுப்புக் கெழுதகைமை (மற்றதற்கு)\nஉப்பாதல் சான்றோர் கடன் (குறள் 802)"
    },
    {
        "start": 276.5,
        "end": 292.0,
        "text": "கெடாஅ வழிவந்த கேண்மையார் (கேண்மை)\nவிடாஅர் விழையும் உலகு (குறள் 809)"
    },
    {
        "start": 292.5,
        "end": 304.0,
        "text": "விழையார் விழையப் படுப (பழையார்கண்)\nபண்பின் தலைப்பிரியாதார் (குறள் 810)"
    },
    # [Grand Chorus Finale]
    {
        "start": 304.5,
        "end": 312.0,
        "text": "[முழு நிறைவுப் பல்லவி / Grand Finale Chorus]\nபழைமை எனப்படுவது யாது எனின் (யாதும்)\nகிழமையைக் கீழ்ந்திடா நட்பு (குறள் 801)"
    },
    {
        "start": 312.5,
        "end": 317.0,
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
    out_p = "production/subtitles/pazhaimai_1H_golden_pop.srt"
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Master song-flow SRT saved to: {out_p} ({len(cues)} cues)")
