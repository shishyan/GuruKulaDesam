# -*- coding: utf-8 -*-
"""
Guru Kula Desam - True Atmospheric Motion Film Production Engine
1. Zero Shaking: Locked camera plates (100% stability, no integer-pan jitter)
2. True Physical Atmospheric Motion:
   - Continuous falling raindrops / drizzling with motion trails
   - Continuous sacred incense smoke / morning mist
3. Zero Image Duplication:
   - Each unique couplet artwork is shown exactly once for its full verse duration
4. Flawless 1280x720 24fps progressive sync with master studio audio
"""

import sys
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe"
RAIN_LOOP = ROOT / "production" / "rain_composite_loop.mp4"
SMOKE_LOOP = ROOT / "production" / "smoke_composite_loop.mp4"
RENDERS_DIR = ROOT / "renders" / "releases"
TEMP_DIR = ROOT / "renders" / "temp_shots"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
RENDERS_DIR.mkdir(parents=True, exist_ok=True)

def render_stable_film(chapter_num, audio_id, visual_dir, output_path, rain_opacity=0.30, smoke_opacity=0.10):
    images = sorted(list(visual_dir.glob("*.jpg")) + list(visual_dir.glob("*.png")))
    if not images:
        raise FileNotFoundError(f"No images found in {visual_dir}")
        
    audio_path = ROOT / "source" / "youtube" / f"{audio_id}.m4a"
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
    # Get exact audio duration
    probe_cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    duration = float(subprocess.check_output(probe_cmd).decode('utf-8').strip())
    
    n_images = len(images)
    shot_duration = duration / n_images
    print(f"\n==================================================================", flush=True)
    print(f"PRODUCING CHAPTER {chapter_num} TRUE MOTION FILM", flush=True)
    print(f"Total Duration: {duration:.2f}s | Unique Artworks: {n_images}", flush=True)
    print(f"Duration per Unique Shot: {shot_duration:.2f}s (ZERO DUPLICATION)", flush=True)
    print(f"Effects: Locked Stable Camera + Falling Rain + Rising Dhoopam Smoke", flush=True)
    print(f"==================================================================", flush=True)
    
    shot_mp4s = []
    ch_temp = TEMP_DIR / f"ch_{chapter_num}"
    ch_temp.mkdir(parents=True, exist_ok=True)
    
    # 1. Render each unique image into a solid 24fps clip
    for idx, img in enumerate(images):
        shot_out = ch_temp / f"shot_{idx:02d}.mp4"
        shot_mp4s.append(shot_out)
        
        # Calculate precise duration for each shot so total matches audio exactly
        # Last shot takes any fractional remainder
        this_dur = duration - (shot_duration * (n_images - 1)) if idx == n_images - 1 else shot_duration
        
        cmd_shot = [
            FFMPEG, "-y",
            "-loop", "1", "-framerate", "24", "-t", f"{this_dur:.4f}",
            "-i", str(img),
            "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,format=yuv420p",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "17",
            "-pix_fmt", "yuv420p",
            str(shot_out)
        ]
        subprocess.run(cmd_shot, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  [Plate {idx+1}/{n_images}] {img.name} -> {this_dur:.2f}s clip ready", flush=True)
        
    # 2. Concat the solid clips into a seamless base video
    concat_txt = ch_temp / "shots.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for s in shot_mp4s:
            p = s.as_posix().replace("'", "'\\''")
            f.write(f"file '{p}'\n")
            
    base_combined = ch_temp / "all_shots_base.mp4"
    cmd_cat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy",
        str(base_combined)
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Base multi-scene assembly complete. Now compositing atmospheric rain & dhoopam...", flush=True)
    
    # 3. Composite atmospheric motion layers + master audio
    cmd_final = [
        FFMPEG, "-y",
        "-i", str(base_combined),
        "-stream_loop", "-1", "-i", str(RAIN_LOOP),
        "-stream_loop", "-1", "-i", str(SMOKE_LOOP),
        "-i", str(audio_path),
        "-t", str(duration),
        "-filter_complex",
        f"[0:v][2:v]blend=all_mode=screen:all_opacity={smoke_opacity}[with_smoke];"
        f"[with_smoke][1:v]blend=all_mode=screen:all_opacity={rain_opacity},format=yuv420p[v]",
        "-map", "[v]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        "-shortest", str(output_path)
    ]
    subprocess.run(cmd_final, check=True)
    print(f"SUCCESS: Master Film Rendered: {output_path.name} ({output_path.stat().st_size / (1024*1024):.2f} MB)", flush=True)
    return output_path

CHAPTERS = {
    26: ("h2q-ADrbBc4", ROOT / "production" / "visuals" / "thirukkural" / "26-pulaal-unnaamai", RENDERS_DIR / "adhikaram_26_pulaal_unnaamai_cinematic.mp4"),
    27: ("IEk-wwY3rC8", ROOT / "production" / "visuals" / "thirukkural" / "27-thavam", RENDERS_DIR / "adhikaram_27_thavam_cinematic.mp4"),
    52: ("5uRYFxhT32k", ROOT / "production" / "visuals" / "thirukkural" / "52-therinthu-vinaiyaadal", RENDERS_DIR / "adhikaram_52_therinthu_vinaiyaadal_cinematic.mp4"),
    54: ("O0hASl4BS2c", ROOT / "production" / "visuals" / "thirukkural" / "54-pochchaavaamai", RENDERS_DIR / "adhikaram_54_pochchaavaamai_cinematic.mp4"),
    57: ("hjcH8zbEleE", ROOT / "production" / "visuals" / "thirukkural" / "57-veruvantha-seyyaamai", RENDERS_DIR / "adhikaram_57_veruvantha_seyyaamai_cinematic.mp4"),
    61: ("GfGlO3RQuik", ROOT / "production" / "visuals" / "thirukkural" / "61-madiyinmai", RENDERS_DIR / "adhikaram_61_madiyinmai_cinematic.mp4"),
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = int(sys.argv[1])
        if target in CHAPTERS:
            aid, vdir, out = CHAPTERS[target]
            render_stable_film(target, aid, vdir, out)
        elif target == 0:
            for ch, (aid, vdir, out) in CHAPTERS.items():
                render_stable_film(ch, aid, vdir, out)
    else:
        print("Usage: python build_true_motion_film.py <chapter_number | 0 for all>")

