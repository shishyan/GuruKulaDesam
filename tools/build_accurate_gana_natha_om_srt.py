# -*- coding: utf-8 -*-
"""
tools/build_accurate_gana_natha_om_srt.py

Generates and publishes true song-flow SRT for கண நாதா ஓம் (Symphony / Devotional Film)
YouTube IDs: YOYCCthqAEo, VtXBwlKV3qc, uqQlyCQjz-A, ljsORaldcqE
Suno Audio & Lyrics: 24c61c24-174e-43c8-9839-7e9922c78aff
Duration: 03:47.60 (227.6s)
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

# Vocal timeline from acoustic transcription:
cues = [
    {
        "start": 2.0,
        "end": 23.5,
        "text": "விநாயகர் பக்தி இசைப் பாடல்: கண நாதா ஓம்\n[Gana Natha Om — Symphonic Devotional Film]"
    },
    # [Verse 1]
    {
        "start": 24.0,
        "end": 35.0,
        "text": "[சரணம் 1 / Verse 1]\nகண நாதா ஓம் (கண நாதா)\nகங்கா தரசுத (கண நாதா)"
    },
    {
        "start": 35.5,
        "end": 47.0,
        "text": "கண நாதா ஓம் (கண நாதா)\nகங்கா தரசுத (கண நாதா)"
    },
    {
        "start": 47.5,
        "end": 59.0,
        "text": "மத்தள வயிறனே (கண நாதா)\nமாதவன் மருகனே (கண நாதா)"
    },
    {
        "start": 59.5,
        "end": 74.0,
        "text": "மத்தள வயிறனே (கண நாதா)\nமாதவன் மருகனே (கண நாதா)"
    },
    # [Interlude]
    {
        "start": 74.5,
        "end": 116.5,
        "text": "[சிம்பொனி இசை இடைவேளை / Symphonic Orchestral Interlude]"
    },
    # [Chorus]
    {
        "start": 117.0,
        "end": 128.5,
        "text": "[பல்லவி / Chorus]\nகண நாதா ஓம் (கண நாதா)\nகங்கா தரசுத (கண நாதா)"
    },
    {
        "start": 128.7,
        "end": 145.0,
        "text": "மத்தள வயிறனே (கண நாதா)\nமாதவன் மருகனே (கண நாதா)"
    },
    # [Verse 2]
    {
        "start": 145.3,
        "end": 152.9,
        "text": "[சரணம் 2 / Verse 2]\nமூஷிகவாஹன (கண நாதா)"
    },
    {
        "start": 153.0,
        "end": 161.0,
        "text": "மூலாதாரனே (கண நாதா)"
    },
    {
        "start": 161.1,
        "end": 169.0,
        "text": "மோதகப்ரியனே (கண நாதா)"
    },
    {
        "start": 169.1,
        "end": 177.0,
        "text": "சங்கடம் தீர்த்திடும் (கண நாதா)"
    },
    {
        "start": 177.2,
        "end": 184.8,
        "text": "சண்முக சோதர (கண நாதா)"
    },
    {
        "start": 184.9,
        "end": 192.8,
        "text": "இக்கணம் எனையாள் (கண நாதா)"
    },
    # [Grand Chorus Finale]
    {
        "start": 193.0,
        "end": 208.5,
        "text": "[பல்லவி நிறைவு / Grand Chorus Finale]\nகண நாதா ஓம் (கண நாதா)\nகங்காதரசுத (கண நாதா)"
    },
    {
        "start": 208.8,
        "end": 227.4,
        "text": "மத்தள வயிறனே (கண நாதா)\nமாதவன் மருகனே (கண நாதா)"
    }
]

def main():
    os.makedirs('production/subtitles', exist_ok=True)
    targets = ['YOYCCthqAEo', 'VtXBwlKV3qc', 'uqQlyCQjz-A', 'ljsORaldcqE']
    
    for vid in targets:
        srt_path = f'production/subtitles/{vid}.srt'
        with open(srt_path, 'w', encoding='utf-8') as f:
            for idx, item in enumerate(cues, 1):
                f.write(f"{idx}\n")
                f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
                f.write(f"{item['text']}\n\n")
        print(f"Generated song-flow SRT: {srt_path} ({len(cues)} cues)")

        # Publish live
        print(f"Publishing master SRT live to YouTube for {vid}...")
        cmd = f'python tools/api_publish_master.py {vid}'
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
