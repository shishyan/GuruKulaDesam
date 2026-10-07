# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Professional Cinematic Multi-Scene Film Builder
Builds authentic multi-shot film releases:
- Changes scenes every 5 to 6 seconds matching verses & meaning
- Dynamic sub-pixel zoompan (smooth push-in camera motion per shot)
- Subtle atmospheric incense/haze composite overlay
- Synced to exact master audio track duration
- Progressive 1280x720 24fps H.264 + 48kHz AAC with +faststart
"""

import sys
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = Path("C:/ffmpeg/bin/ffmpeg.exe")
FFPROBE = Path("C:/ffmpeg/bin/ffprobe.exe")
SMOKE_LOOP = ROOT / "production" / "smoke_composite_loop.mp4"
RENDERS_DIR = ROOT / "renders" / "releases"
RENDERS_DIR.mkdir(parents=True, exist_ok=True)

def render_chapter_film(chapter_num, audio_id, visual_dir, output_path, shot_duration=6.0):
    images = sorted(list(visual_dir.glob("*.jpg")) + list(visual_dir.glob("*.png")))
    if not images:
        raise FileNotFoundError(f"No visual images found in {visual_dir}")
        
    audio_path = ROOT / "source" / "youtube" / f"{audio_id}.m4a"
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
    # Get audio duration
    probe_cmd = [
        str(FFPROBE), "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    duration = float(subprocess.check_output(probe_cmd).decode('utf-8').strip())
    print(f"Chapter {chapter_num}: Master Audio Duration = {duration:.3f}s, Visuals = {len(images)} scenes", flush=True)
    
    # Build sequence of shots
    num_shots = math.ceil(duration / shot_duration)
    sequence = [images[i % len(images)] for i in range(num_shots)]
    
    concat_file = ROOT / "renders" / f"chapter_{chapter_num}_concat.txt"
    lines = []
    for img in sequence:
        p = img.as_posix().replace("'", "'\\''")
        lines.append(f"file '{p}'\nduration {shot_duration}")
    last_p = sequence[-1].as_posix().replace("'", "'\\''")
    lines.append(f"file '{last_p}'")
    
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    frames_per_shot = int(shot_duration * 24)
    
    print(f"Rendering {output_path.name} ({num_shots} shot transitions @ {shot_duration}s per cut)...", flush=True)
    
    cmd = [
        str(FFMPEG), "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-stream_loop", "-1", "-i", str(SMOKE_LOOP),
        "-i", str(audio_path),
        "-t", str(duration),
        "-filter_complex",
        f"[0:v]scale=1344:756:force_original_aspect_ratio=increase,crop=1280:720,"
        f"zoompan=z='min(zoom+0.0003,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_per_shot}:s=1280x720:fps=24,"
        f"format=yuv420p[base];"
        f"[1:v]scale=1280:720,format=yuv420p[smoke];"
        f"[base][smoke]blend=all_mode=screen:all_opacity=0.10,format=yuv420p[v]",
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        "-shortest", str(output_path)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"SUCCESS: Rendered {output_path.name} ({output_path.stat().st_size / (1024*1024):.2f} MB)", flush=True)
    return output_path

AUDIO_MAP = {
    26: ("h2q-ADrbBc4", ROOT / "production" / "visuals" / "thirukkural" / "26-pulaal-unnaamai", RENDERS_DIR / "adhikaram_26_pulaal_unnaamai_cinematic.mp4"),
    27: ("IEk-wwY3rC8", ROOT / "production" / "visuals" / "thirukkural" / "27-thavam", RENDERS_DIR / "adhikaram_27_thavam_cinematic.mp4"),
    52: ("5uRYFxhT32k", ROOT / "production" / "visuals" / "thirukkural" / "52-therinthu-vinaiyaadal", RENDERS_DIR / "adhikaram_52_therinthu_vinaiyaadal_cinematic.mp4"),
    54: ("O0hASl4BS2c", ROOT / "production" / "visuals" / "thirukkural" / "54-pochchaavaamai", RENDERS_DIR / "adhikaram_54_pochchaavaamai_cinematic.mp4"),
    57: ("hjcH8zbEleE", ROOT / "production" / "visuals" / "thirukkural" / "57-veruvantha-seyyaamai", RENDERS_DIR / "adhikaram_57_veruvantha_seyyaamai_cinematic.mp4"),
    61: ("GfGlO3RQuik", ROOT / "production" / "visuals" / "thirukkural" / "61-madiyinmai", RENDERS_DIR / "adhikaram_61_madiyinmai_cinematic.mp4"),
}

if __name__ == "__main__":
    ch = 26
    if len(sys.argv) > 1:
        ch = int(sys.argv[1])
        
    if ch in AUDIO_MAP:
        aid, vdir, out = AUDIO_MAP[ch]
        render_chapter_film(ch, aid, vdir, out, shot_duration=6.0)
    elif ch == 0:
        for c, (aid, vdir, out) in AUDIO_MAP.items():
            print(f"\n{'='*60}\nSTARTING RENDER: Chapter {c}\n{'='*60}", flush=True)
            render_chapter_film(c, aid, vdir, out, shot_duration=6.0)
    else:
        print(f"Unknown chapter {ch}")
