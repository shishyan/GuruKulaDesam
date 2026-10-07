# -*- coding: utf-8 -*-
"""
Encode Web-Optimized Videos & Micro-Clips for Guru Kula Desam
Converts release films into fast streaming 720p web videos (<35MB)
and generates 30-45s micro-clips (<5MB) for instant interactive learning.
"""
import os
import subprocess

videos = [
    ("renders/releases/adhikaram_27_thavam_cinematic.mp4", "assets/videos/adhikaram_27_thavam.mp4", "assets/videos/short_27_thavam.mp4", 40),
    ("renders/releases/adhikaram_52_therinthu_vinaiyaadal_cinematic.mp4", "assets/videos/adhikaram_52_therinthu_vinaiyaadal.mp4", "assets/videos/short_52_vinai.mp4", 45),
    ("renders/releases/adhikaram_54_pochchaavaamai_cinematic.mp4", "assets/videos/adhikaram_54_pochchaavaamai.mp4", "assets/videos/short_54_vigilance.mp4", 40),
    ("renders/releases/adhikaram_57_veruvantha_seyyaamai_cinematic.mp4", "assets/videos/adhikaram_57_veruvantha_seyyaamai.mp4", "assets/videos/short_57_justice.mp4", 42),
    ("renders/releases/adhikaram_61_madiyinmai_cinematic.mp4", "assets/videos/adhikaram_61_madiyinmai.mp4", "assets/videos/short_61_industry.mp4", 38),
]

# Also generate short for chapter 26
if os.path.exists("renders/releases/adhikaram_26_pulaal_unnaamai_cinematic.mp4"):
    short_26 = "assets/videos/short_26_ahimsa.mp4"
    if not os.path.exists(short_26):
        cmd = [
            "ffmpeg", "-y", "-ss", "00:00:15", "-i", "renders/releases/adhikaram_26_pulaal_unnaamai_cinematic.mp4",
            "-t", "42", "-vf", "scale=1280:720", "-c:v", "libx264", "-crf", "26", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", short_26
        ]
        subprocess.run(cmd, check=True)
        print("Generated short_26_ahimsa.mp4")

for src, web_out, short_out, short_dur in videos:
    if os.path.exists(src):
        # 1. Full web video
        if not os.path.exists(web_out):
            cmd_full = [
                "ffmpeg", "-y", "-i", src,
                "-vf", "scale=1280:720", "-c:v", "libx264", "-crf", "26", "-preset", "fast",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", web_out
            ]
            print(f"Encoding full web: {web_out}...")
            subprocess.run(cmd_full, check=True)
        
        # 2. Micro-clip (Short)
        if not os.path.exists(short_out):
            cmd_short = [
                "ffmpeg", "-y", "-ss", "00:00:20", "-i", src,
                "-t", str(short_dur), "-vf", "scale=1280:720", "-c:v", "libx264", "-crf", "26", "-preset", "fast",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", short_out
            ]
            print(f"Generating micro-clip: {short_out}...")
            subprocess.run(cmd_short, check=True)

print("All web videos and micro-clips ready!")
