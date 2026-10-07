# -*- coding: utf-8 -*-
"""
Generate a seamless 10-second looping 1280x720 video of photorealistic falling rain/drizzle.
"""
import math
import random
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent
FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"
OUT_MP4 = ROOT / "rain_composite_loop.mp4"

w, h = 1280, 720
fps = 24
duration_sec = 10
total_frames = fps * duration_sec
rng = random.Random(42)

# Generate 600 distinct raindrops with varied speeds and lengths
# To make it loop seamlessly, speed must cycle integer times through the screen
drops = []
for _ in range(650):
    x = rng.uniform(-50, w + 50)
    base_speed = rng.choice([360, 480, 600, 720, 840]) # pixels per second
    # ensure it completes an integer number of screen cycles in 10s:
    # cycles * 720 / 10s
    cycles = rng.randint(4, 12)
    speed = cycles * (h + 40) / duration_sec
    length = rng.uniform(8, 22)
    opacity = rng.uniform(0.20, 0.65)
    width = 1 if length < 15 else 2
    initial_y = rng.uniform(0, h)
    slant = rng.uniform(-1.5, -0.5)
    drops.append((x, initial_y, speed, length, opacity, width, slant))

cmd = [
    FFMPEG, "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps),
    "-i", "pipe:0",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-pix_fmt", "yuv420p",
    str(OUT_MP4)
]

print(f"Generating {OUT_MP4.name} ({total_frames} frames)...", flush=True)
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

try:
    for f in range(total_frames):
        t = f / fps
        img = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(img)
        
        for x, initial_y, speed, length, opacity, width, slant in drops:
            # seamlessly looped vertical position
            cur_y = (initial_y + speed * t) % (h + 40) - 20
            cur_x = x + slant * (cur_y / h * 20)
            
            val = int(255 * opacity)
            draw.line([(cur_x, cur_y), (cur_x + slant * 2, cur_y + length)], fill=val, width=width)
            
        # Subtle blur for realistic motion trail
        blurred = img.filter(ImageFilter.GaussianBlur(0.35))
        arr = np.asarray(blurred, dtype=np.uint8)
        rgb = np.repeat(arr[:, :, None], 3, axis=2)
        proc.stdin.write(rgb.tobytes())
        
        if f % 48 == 0:
            print(f"  Frame {f}/{total_frames} ({int(f/total_frames*100)}%)", flush=True)
finally:
    proc.stdin.close()
    proc.wait()

print(f"SUCCESS: Created {OUT_MP4} ({OUT_MP4.stat().st_size / (1024*1024):.2f} MB)", flush=True)

