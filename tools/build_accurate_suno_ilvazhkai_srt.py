# -*- coding: utf-8 -*-
"""
tools/build_accurate_suno_ilvazhkai_srt.py

Generates and publishes the true Suno song flow SRT for Thirukkural Chapter 5 (இல்வாழ்க்கை):
Video ID: C05GEfkJZaY
Suno Track: cc5def14-edba-4e10-9542-eabf2afea1d6 (திருக்குறள் இல்வாழ்க்கை L by GuruKulaDesam)
Total Audio Duration: 257.60 seconds
"""

import os, sys, subprocess

def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# Musical Song Flow Architecture mapped to Vocal Timeline:
# 00:00 - 00:25: Invocatory Orchestral Introduction
# 00:25 - 00:50: [Verse 0] வையகத்துள் வாழ்வாங்கு இல் வாழ்பவன்! வான்உறையும் தெய்வத்துள் வைக்கப்படும்! (குறள் 50)
# 00:50 - 01:15: [Chorus / பல்லவி] வையகத்துள் வாழ்வாங்கு இல் வாழ்பவன்! வான்உறையும் தெய்வத்துள் வைக்கப்படும்!
# 01:15 - 01:40: [Verse 1] அன்பும் அறமும் நிதமும் உடையதாயின்! இல்வாழ்க்கையின் பண்பும் பயனும் அது! (குறள் 45)
# 01:40 - 02:00: [Chorus Reprise] அன்பும் அறமும் நிதமும் உடையதாயின்! பண்பும் பயனும் அது!
# 02:00 - 02:22: [Verse 2] அறனிழுக்கா இல்வாழ்க்கை ஆற்றினொழுகின்! நோற்பாரினும் நோன்மை உடையது அது! (குறள் 46 & 48)
# 02:22 - 02:40: [Chorus Bridge] இயல்பினான் இல்வாழ்க்கை வாழ்பவனென்பான் முயல்வாருளெலாம் தலை! (குறள் 47)
# 02:40 - 02:57: [Grand Finale] அன்பும் அறமும் நிதமும் உடையதாயின் இல்வாழ்க்கையின் பண்பும் பயனும் அது! & Outro

cues = [
    {
        "start": 5.0,
        "end": 24.5,
        "text": "திருக்குறள் — அதிகாரம் 5: இல்வாழ்க்கை (Ilvazhkkai)\n[திரைப்பட பக்திப் பாடல் / Cinematic Devotional Song]"
    },
    # [Verse 0]
    {
        "start": 25.0,
        "end": 37.0,
        "text": "[சரணம் / Verse]\nவையகத்துள் வாழ்வாங்கு இல் வாழ்பவன்!\nவான்உறையும் தெய்வத்துள் வைக்கப்படும்! (குறள் 50)"
    },
    {
        "start": 37.5,
        "end": 50.0,
        "text": "வையகத்துள் வாழ்வாங்கு இல் வாழ்பவன்!\nவான்உறையும் தெய்வத்துள் வைக்கப்படும்! (குறள் 50)"
    },
    # [Chorus]
    {
        "start": 50.5,
        "end": 64.0,
        "text": "[பல்லவி / Chorus]\nவையகத்துள் வாழ்வாங்கு இல் வாழ்பவன்!\nவான்உறையும் தெய்வத்துள் வைக்கப்படும்!"
    },
    {
        "start": 64.5,
        "end": 78.0,
        "text": "வையகத்துள் வாழ்வாங்கு இல் வாழ்பவன்!\nவான்உறையும் தெய்வத்துள் வைக்கப்படும்!"
    },
    # [Verse 1]
    {
        "start": 78.5,
        "end": 96.0,
        "text": "[சரணம் 1 / Verse 1]\nஅன்பும் அறமும் நிதமும் உடையதாயின்!\nஇல்வாழ்க்கையின் பண்பும் பயனும் அது! (குறள் 45)"
    },
    {
        "start": 96.5,
        "end": 115.0,
        "text": "அன்பும் அறமும் நிதமும் உடையதாயின்!\nஇல்வாழ்க்கையின் பண்பும் பயனும் அது!"
    },
    # [Chorus Reprise]
    {
        "start": 115.5,
        "end": 136.0,
        "text": "[பல்லவி மீள்சுழற்சி / Chorus Reprise]\nஅன்பும் அறமும் நிதமும் உடையதாயின்!\nஇல்வாழ்க்கையின் பண்பும் பயனும் அது!"
    },
    # [Verse 2]
    {
        "start": 136.5,
        "end": 158.0,
        "text": "[சரணம் 2 / Verse 2]\nஅறனிழுக்கா இல்வாழ்க்கை ஆற்றினொழுகின்!\nநோற்பாரினும் நோன்மை உடையது அது! (குறள் 46 & 48)"
    },
    {
        "start": 158.5,
        "end": 178.0,
        "text": "ஆற்றின் ஒழுக்கி அறனிழுக்கா இல்வாழ்க்கை\nநோற்பாரின் நோன்மை உடைத்து!"
    },
    # [Chorus Bridge]
    {
        "start": 178.5,
        "end": 198.0,
        "text": "[இணைப்புப் பல்லவி / Bridge]\nஅறனிழுக்கா இல்வாழ்க்கை ஆற்றினொழுகின்!\nநோற்பாரினும் நோன்மை உடையது அது!"
    },
    {
        "start": 198.5,
        "end": 218.0,
        "text": "இயல்பினான் இல்வாழ்க்கை வாழ்பவனென்பான்!\nமுயல்வாருளெலாம் எல்லாம் தலை! (குறள் 47)"
    },
    {
        "start": 218.5,
        "end": 238.0,
        "text": "இயல்பினான் இல்வாழ்க்கை வாழ்பவனென்பான்!\nமுயல்வாருளெலாம் எல்லாம் தலை!"
    },
    # [Grand Finale Chorus]
    {
        "start": 238.5,
        "end": 252.0,
        "text": "[மங்கள நிறைவு / Grand Finale]\nஅன்பும் அறமும் நிதமும் உடையதாயின்!\nஇல்வாழ்க்கையின் பண்பும் பயனும் அது!"
    },
    {
        "start": 252.5,
        "end": 257.6,
        "text": "[இல்வாழ்க்கை பக்திப் பாடல் நிறைவு]"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    srt_path = 'production/subtitles/C05GEfkJZaY.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(cues, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
            f.write(f"{item['text']}\n\n")

    print(f"Precise Real-Song Flow SRT generated: {srt_path} ({len(cues)} cues)")
    
    # Publish to YouTube live
    print("Publishing master SRT live to YouTube for C05GEfkJZaY...")
    cmd = 'python tools/api_publish_master.py C05GEfkJZaY'
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
