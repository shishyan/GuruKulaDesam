import sys
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import (
    FFMPEG, FFPROBE, OVERLAY_FILE, DRIZZLE_LOOP, RENDERS_DIR,
    get_media_duration, create_processed_clip
)

tid = "l3E27q5r-nk"
audio_path = ROOT / "source" / "youtube" / f"{tid}.m4a"
scene_dir = ROOT / "production" / "google_flow_renders" / tid
scene_clips = sorted(scene_dir.glob("scene_*.mp4"))

with open(ROOT / "production" / "exact_timed_lyrics_l3E27q5r-nk.json", "r", encoding="utf-8") as f:
    timed_lyrics = json.load(f)

print(f"Loaded {len(timed_lyrics)} exact timed cards for {tid}")

audio_dur = get_media_duration(audio_path)
print(f"Audio duration: {audio_dur:.2f}s | Available clips: {len(scene_clips)}")

temp_dir = ROOT / "renders" / f"temp_perfect_{tid}"
temp_dir.mkdir(parents=True, exist_ok=True)
concat_file = temp_dir / "concat_list.txt"

# 75% speed retiming
speed = 0.75
forward_clips = [create_processed_clip(c, temp_dir, speed=speed, reverse=False) for c in scene_clips]
reversed_clips = [create_processed_clip(c, temp_dir, speed=speed, reverse=True) for c in reversed(scene_clips)]

base_durs = [get_media_duration(c) for c in forward_clips]
one_pass_dur = sum(base_durs)

playlist = []
current_dur = 0.0
cycle = 1
while current_dur < audio_dur:
    if cycle % 2 == 1:
        playlist.extend(forward_clips)
    else:
        playlist.extend(reversed_clips)
    current_dur += one_pass_dur
    cycle += 1
    if cycle > 30:
        break

with open(concat_file, "w", encoding="utf-8") as f:
    for clip in playlist:
        clip_str = str(clip.resolve()).replace("\\", "/")
        f.write(f"file '{clip_str}'\n")

looped_video = temp_dir / "looped_video.mp4"
cmd_concat = [
    str(FFMPEG), "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(concat_file),
    "-c", "copy",
    str(looped_video)
]
subprocess.run(cmd_concat, check=True, capture_output=True)

# Build drawtext filters for each exact timed card
lyrics_dir = temp_dir / "lyrics_cards"
lyrics_dir.mkdir(parents=True, exist_ok=True)
font_path = "C\\:/Windows/Fonts/NirmalaB.ttf"

inputs = ["-i", str(looped_video), "-i", str(audio_path)]
filter_complex = []
curr_v = "[0:v]"

has_drizzle = DRIZZLE_LOOP.exists()
has_overlay = OVERLAY_FILE.exists()

curr_input_idx = 2
if has_drizzle:
    inputs.extend(["-stream_loop", "-1", "-i", str(DRIZZLE_LOOP)])
    filter_complex.append(f"[{curr_input_idx}:v]scale=1280:720,format=rgba,colorchannelmixer=aa=0.22[drizzle]")
    filter_complex.append(f"{curr_v}[drizzle]overlay=0:0:shortest=1[v_drizzle]")
    curr_v = "[v_drizzle]"
    curr_input_idx += 1

if has_overlay:
    inputs.extend(["-i", str(OVERLAY_FILE)])
    filter_complex.append(f"[{curr_input_idx}:v]scale=1280:720,format=rgba,colorchannelmixer=aa=0.88[ovl]")
    filter_complex.append(f"{curr_v}[ovl]overlay=0:0[v_sacred]")
    curr_v = "[v_sacred]"
    curr_input_idx += 1

for idx, card in enumerate(timed_lyrics):
    t_start = card["start_sec"]
    t_end = card["end_sec"]
    card_text = card["tamil_text"]

    txt_file = lyrics_dir / f"card_{idx:03d}.txt"
    txt_file.write_text(card_text, encoding="utf-8")
    txt_path_posix = txt_file.as_posix().replace(":", "\\:")

    out_label = f"v_lyric_{idx}"
    filter_elem = (
        f"{curr_v}drawtext=fontfile='{font_path}':"
        f"textfile='{txt_path_posix}':"
        f"fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-text_h-35:"
        f"box=1:boxcolor=black@0.65:boxborderw=10:"
        f"line_spacing=2:text_shaping=1:"
        f"enable='between(t,{t_start:.3f},{t_end:.3f})'[{out_label}]"
    )
    filter_complex.append(filter_elem)
    curr_v = f"[{out_label}]"

out_film = RENDERS_DIR / "shiva_l3E27q5r-nk_master_perfect_timed.mp4"

cmd_master = [
    str(FFMPEG), "-y",
    *inputs,
    "-filter_complex", ";".join(filter_complex),
    "-map", curr_v,
    "-map", "1:a",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "20",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(out_film)
]

print("Rendering master film with exact lyric timing...")
subprocess.run(cmd_master, check=True)
print(f"Master film completed: {out_film} ({out_film.stat().st_size / (1024*1024):.2f} MB)")
