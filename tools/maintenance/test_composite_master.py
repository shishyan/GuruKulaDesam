# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

ROOT = Path('.').resolve()
FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"

test_img = ROOT / "production" / "visuals" / "thirukkural" / "26-pulaal-unnaamai" / "02-kural-251-ahimsa-creatures.jpg"
rain_loop = ROOT / "production" / "rain_composite_loop.mp4"
smoke_loop = ROOT / "production" / "smoke_composite_loop.mp4"
audio_file = ROOT / "source" / "youtube" / "h2q-ADrbBc4.m4a"
out_test = ROOT / "renders" / "tests" / "test_fluid_rain_dhoopam_stable.mp4"

cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-framerate", "24", "-t", "15", "-i", str(test_img),
    "-stream_loop", "-1", "-i", str(rain_loop),
    "-stream_loop", "-1", "-i", str(smoke_loop),
    "-i", str(audio_file),
    "-t", "15",
    "-filter_complex",
    "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,format=yuv420p[base];"
    "[1:v]scale=1280:720,format=yuv420p[rain];"
    "[2:v]scale=1280:720,format=yuv420p[smoke];"
    "[base][smoke]blend=all_mode=screen:all_opacity=0.10[with_smoke];"
    "[with_smoke][rain]blend=all_mode=screen:all_opacity=0.35,format=yuv420p[v]",
    "-map", "[v]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
    "-movflags", "+faststart",
    "-shortest", str(out_test)
]

print("Rendering test composite...", flush=True)
subprocess.run(cmd, check=True)
print(f"SUCCESS: Rendered {out_test} ({out_test.stat().st_size / (1024*1024):.2f} MB)")

