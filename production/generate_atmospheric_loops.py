# -*- coding: utf-8 -*-
"""
Atmospheric Loop Generator
Generates seamless 10-second 1280x720 24fps video loops for:
1. Drizzle (delicate, slow, fine mist droplets)
2. Snow (gently floating and swaying white snowflakes)
3. Flowers (fluttering, rotating jasmine and lotus petals)
Default is rain (rain_composite_loop.mp4).
"""

import math
import random
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"

W, H = 1280, 720
FPS = 24
DURATION_SEC = 10
TOTAL_FRAMES = FPS * DURATION_SEC

def create_video_pipe(out_path):
    cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(out_path)
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

def generate_drizzle_loop():
    out_path = ROOT / "drizzle_composite_loop.mp4"
    print(f"Generating {out_path.name}...")
    rng = random.Random(101)
    
    # 500 fine, delicate droplets with slow, steady drift
    drops = []
    for _ in range(500):
        x = rng.uniform(-40, W + 40)
        cycles = rng.randint(2, 6) # slower than rain
        speed = cycles * (H + 30) / DURATION_SEC
        length = rng.uniform(4, 10)
        opacity = rng.uniform(0.15, 0.45)
        initial_y = rng.uniform(0, H)
        slant = rng.uniform(-0.8, -0.2)
        drops.append((x, initial_y, speed, length, opacity, slant))

    proc = create_video_pipe(out_path)
    try:
        for f in range(TOTAL_FRAMES):
            t = f / FPS
            img = Image.new("L", (W, H), 0)
            draw = ImageDraw.Draw(img)
            
            for x, initial_y, speed, length, opacity, slant in drops:
                cur_y = (initial_y + speed * t) % (H + 30) - 15
                cur_x = x + slant * (cur_y / H * 15)
                val = int(255 * opacity)
                draw.line([(cur_x, cur_y), (cur_x + slant, cur_y + length)], fill=val, width=1)
                
            blurred = img.filter(ImageFilter.GaussianBlur(0.3))
            arr = np.asarray(blurred, dtype=np.uint8)
            rgb = np.repeat(arr[:, :, None], 3, axis=2)
            proc.stdin.write(rgb.tobytes())
    finally:
        proc.stdin.close()
        proc.wait()
    print(f"✅ Generated {out_path.name} ({out_path.stat().st_size / (1024*1024):.2f} MB)")

def generate_snow_loop():
    out_path = ROOT / "snow_composite_loop.mp4"
    print(f"Generating {out_path.name}...")
    rng = random.Random(202)
    
    # 280 soft snowflakes swaying sinusoidally
    flakes = []
    for _ in range(280):
        base_x = rng.uniform(0, W)
        cycles = rng.randint(1, 3) # very slow float
        speed = cycles * (H + 40) / DURATION_SEC
        radius = rng.uniform(1.5, 4.0)
        opacity = rng.uniform(0.25, 0.70)
        initial_y = rng.uniform(0, H)
        sway_amp = rng.uniform(15, 45)
        sway_freq = rng.randint(1, 3) # cycles in 10s
        phase = rng.uniform(0, 2 * math.pi)
        flakes.append((base_x, initial_y, speed, radius, opacity, sway_amp, sway_freq, phase))

    proc = create_video_pipe(out_path)
    try:
        for f in range(TOTAL_FRAMES):
            t = f / FPS
            img = Image.new("L", (W, H), 0)
            draw = ImageDraw.Draw(img)
            
            for base_x, initial_y, speed, radius, opacity, sway_amp, sway_freq, phase in flakes:
                cur_y = (initial_y + speed * t) % (H + 40) - 20
                cur_x = base_x + sway_amp * math.sin(2 * math.pi * sway_freq * (t / DURATION_SEC) + phase)
                val = int(255 * opacity)
                draw.ellipse(
                    [(cur_x - radius, cur_y - radius), (cur_x + radius, cur_y + radius)],
                    fill=val
                )
                
            blurred = img.filter(ImageFilter.GaussianBlur(0.8))
            arr = np.asarray(blurred, dtype=np.uint8)
            rgb = np.repeat(arr[:, :, None], 3, axis=2)
            proc.stdin.write(rgb.tobytes())
    finally:
        proc.stdin.close()
        proc.wait()
    print(f"✅ Generated {out_path.name} ({out_path.stat().st_size / (1024*1024):.2f} MB)")

def generate_flowers_loop():
    out_path = ROOT / "flowers_composite_loop.mp4"
    print(f"Generating {out_path.name}...")
    rng = random.Random(303)
    
    # 160 drifting, rotating flower petals
    petals = []
    for _ in range(160):
        base_x = rng.uniform(0, W)
        cycles = rng.randint(1, 3)
        speed = cycles * (H + 50) / DURATION_SEC
        rx = rng.uniform(3.5, 7.5) # petal width
        ry = rng.uniform(6.5, 14.0) # petal length
        opacity = rng.uniform(0.30, 0.75)
        initial_y = rng.uniform(0, H)
        sway_amp = rng.uniform(20, 60)
        sway_freq = rng.randint(1, 3)
        rot_cycles = rng.choice([-2, -1, 1, 2])
        phase = rng.uniform(0, 2 * math.pi)
        petals.append((base_x, initial_y, speed, rx, ry, opacity, sway_amp, sway_freq, rot_cycles, phase))

    proc = create_video_pipe(out_path)
    try:
        for f in range(TOTAL_FRAMES):
            t = f / FPS
            img = Image.new("L", (W, H), 0)
            
            for base_x, initial_y, speed, rx, ry, opacity, sway_amp, sway_freq, rot_cycles, phase in petals:
                cur_y = (initial_y + speed * t) % (H + 50) - 25
                cur_x = base_x + sway_amp * math.sin(2 * math.pi * sway_freq * (t / DURATION_SEC) + phase)
                angle_deg = (rot_cycles * 360 * (t / DURATION_SEC) + math.degrees(phase)) % 360
                
                # Draw single petal on a small patch then paste with rotation
                pw, ph = int(ry * 2 + 10), int(ry * 2 + 10)
                p_img = Image.new("L", (pw, ph), 0)
                p_draw = ImageDraw.Draw(p_img)
                val = int(255 * opacity)
                p_draw.ellipse(
                    [(pw/2 - rx, ph/2 - ry), (pw/2 + rx, ph/2 + ry)],
                    fill=val
                )
                rotated = p_img.rotate(angle_deg, resample=Image.BICUBIC)
                
                paste_x = int(cur_x - pw/2)
                paste_y = int(cur_y - ph/2)
                
                # Paste with max blend
                patch = np.asarray(rotated)
                # bounding box clamp
                x0 = max(0, paste_x)
                y0 = max(0, paste_y)
                x1 = min(W, paste_x + pw)
                y1 = min(H, paste_y + ph)
                
                if x1 > x0 and y1 > y0:
                    px0 = x0 - paste_x
                    py0 = y0 - paste_y
                    px1 = px0 + (x1 - x0)
                    py1 = py0 + (y1 - y0)
                    
                    sub_patch = patch[py0:py1, px0:px1]
                    cur_arr = np.asarray(img)
                    cur_slice = cur_arr[y0:y1, x0:x1]
                    blended = np.maximum(cur_slice, sub_patch)
                    # write back
                    p_view = Image.fromarray(blended)
                    img.paste(p_view, (x0, y0))

            blurred = img.filter(ImageFilter.GaussianBlur(0.5))
            arr = np.asarray(blurred, dtype=np.uint8)
            rgb = np.repeat(arr[:, :, None], 3, axis=2)
            proc.stdin.write(rgb.tobytes())
    finally:
        proc.stdin.close()
        proc.wait()
    print(f"✅ Generated {out_path.name} ({out_path.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    generate_drizzle_loop()
    generate_snow_loop()
    generate_flowers_loop()
