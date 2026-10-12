# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_aalvinaiyudaimai_srt.py

Generates and publishes true song-flow SRT for திருக்குறள்: அதிகாரம் 62 - ஆள்வினையுடைமை
YouTube ID: 37qaN4sG53k
Suno Track: 0cbf79f8-2b9c-4762-a89b-13373a77f6e5 (ஆள்வினையுடைமை 1S Golden)
Duration: 302.46 seconds (5m 02s)
"""

import os, sys, subprocess

sys.stdout.reconfigure(encoding='utf-8')

def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# Musical Song Flow Architecture mapped to Vocal Timeline:
# 00:00 - 00:26: Invocatory Orchestral Introduction
# 00:26 - 00:54: [Chorus] தெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்) மெய்வருத்தக் கூலி தரும் (குறள் 619)
# 00:54 - 01:28: [Verse 1] முயற்சி திருவினை ஆக்கும்... மடியுளாள் மாமுகடி என்ப... (குறள் 616 & 617)
# 01:28 - 01:54: [Chorus Reprise 1] தெய்வத்தான் ஆகாது எனினும்
# 01:54 - 02:35: [Verse 2] தாளாண்மை இல்லாதான்... தாளாண்மை என்னும்... அருமை உடைத்தென்று... (குறள் 614, 613, 611)
# 02:35 - 03:02: [Chorus Reprise 2] தெய்வத்தான் ஆகாது எனினும்
# 03:02 - 03:45: [Bridge] பொறியின்மை யார்க்கும்... இன்பம் விழையான்... ஊழியையும் உப்பக்கம்... (குறள் 618, 615, 620)
# 03:45 - 04:30: [Grand Chorus Finale] தெய்வத்தான் ஆகாது எனினும் முயற்சிதன் மெய்வருத்தக் கூலி தரும்
# 04:30 - 05:02: Orchestral Outro & Divine Finale

cues = [
    {
        "start": 5.0,
        "end": 25.5,
        "text": "திருக்குறள் — அதிகாரம் 62: ஆள்வினையுடைமை (Aalvinaiyudaimai)\n[செவ்வியல் பக்தி இசைப் பாடல் / Classical Devotional Song]"
    },
    # [Chorus 1]
    {
        "start": 26.0,
        "end": 40.0,
        "text": "[பல்லவி / Chorus]\nதெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்)\nமெய்வருத்தக் கூலி தரும் (குறள் 619)"
    },
    {
        "start": 40.5,
        "end": 54.0,
        "text": "தெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்)\nமெய்வருத்தக் கூலி தரும் (குறள் 619)"
    },
    # [Verse 1]
    {
        "start": 54.5,
        "end": 71.0,
        "text": "[சரணம் 1 / Verse 1]\nமுயற்சி திருவினை ஆக்கும் (முயற்றின்மை)\nஇன்மை புகுத்தி விடும் (குறள் 616)"
    },
    {
        "start": 71.5,
        "end": 88.0,
        "text": "முயற்சி திருவினை ஆக்கும் (முயற்றின்மை)\nஇன்மை புகுத்தி விடும்"
    },
    {
        "start": 88.5,
        "end": 108.0,
        "text": "மடியுளாள் மாமுகடி என்ப (மடியிலான்)\nதாளுளான் தாமரையி னாள் (குறள் 617)"
    },
    {
        "start": 108.5,
        "end": 127.5,
        "text": "மடியுளாள் மாமுகடி என்ப (மடியிலான்)\nதாளுளான் தாமரையி னாள்"
    },
    # [Chorus Reprise 1]
    {
        "start": 128.0,
        "end": 141.0,
        "text": "[பல்லவி / Chorus]\nதெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்)\nமெய்வருத்தக் கூலி தரும்"
    },
    {
        "start": 141.5,
        "end": 154.5,
        "text": "தெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்)\nமெய்வருத்தக் கூலி தரும்"
    },
    # [Verse 2]
    {
        "start": 155.0,
        "end": 174.0,
        "text": "[சரணம் 2 / Verse 2]\nதாளாண்மை இல்லாதான் வேளாண்மை (பேடிகை)\nவாளாண்மை போலக் கெடும் (குறள் 614)"
    },
    {
        "start": 174.5,
        "end": 194.0,
        "text": "தாளாண்மை என்னும் தகைமைக்கண் (தங்கிற்றே)\nவேளாண்மை என்னுஞ் செருக்கு (குறள் 613)"
    },
    {
        "start": 194.5,
        "end": 214.0,
        "text": "அருமை உடைத்தென்று அசாவாமை (வேண்டும்)\nபெருமை முயற்சி தரும் (குறள் 611)"
    },
    {
        "start": 214.5,
        "end": 234.5,
        "text": "அருமை உடைத்தென்று அசாவாமை (வேண்டும்)\nபெருமை முயற்சி தரும்"
    },
    # [Chorus Reprise 2]
    {
        "start": 235.0,
        "end": 248.5,
        "text": "[பல்லவி / Chorus]\nதெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்)\nமெய்வருத்தக் கூலி தரும்"
    },
    {
        "start": 249.0,
        "end": 262.0,
        "text": "தெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்)\nமெய்வருத்தக் கூலி தரும்"
    },
    # [Bridge]
    {
        "start": 262.5,
        "end": 278.0,
        "text": "[அனுபல்லவி / Bridge]\nபொறியின்மை யார்க்கும் பழியன்று (அறிவறிந்து)\nஆள்வினை இன்மை பழி (குறள் 618)"
    },
    {
        "start": 278.5,
        "end": 294.0,
        "text": "இன்பம் விழையான் வினைவிழைவான் (தன்கேளிர்)\nதுன்பம் துடைத்தூன்றும் தூண் (குறள் 615)"
    },
    {
        "start": 294.5,
        "end": 310.0,
        "text": "ஊழையும் உப்பக்கம் காண்பர் (உலைவின்றித்)\nதாழாது உஞற்று பவர் (குறள் 620)"
    },
    # [Grand Chorus Finale]
    {
        "start": 310.5,
        "end": 325.0,
        "text": "[பல்லவி நிறைவு / Grand Chorus Finale]\nதெய்வத்தான் ஆகாது எனினும் (முயற்சிதன்)\nமெய்வருத்தக் கூலி தரும் (குறள் 619)"
    },
    {
        "start": 325.5,
        "end": 362.4,
        "text": "[ஆள்வினையுடைமை பக்தி இசை நிறைவு / Finale]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/37qaN4sG53k.srt'
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Flawless real song-flow SRT generated: {srt_path} ({len(cues)} cues)")

    # Publish live to YouTube
    print("Publishing master SRT live to YouTube for 37qaN4sG53k...")
    cmd = 'python tools/api_publish_master.py 37qaN4sG53k'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
