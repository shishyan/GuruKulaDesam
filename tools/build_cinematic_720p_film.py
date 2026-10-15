#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_cinematic_720p_film.py
Official 720p Broadcast Film Assembler with Refined Cinematic Elements:
1. Pure 720p native resolution (1280x720 24fps) - sharp, clean, no grain, light file size (~130 MB).
2. 4-way cinematic camera moves (Pan L->R, Pan R->L, Slow Push, Slow Pull).
3. 1.0s smooth cross-dissolve (xfade) transitions.
4. Realistic Drizzle Effect:
   - Very slow, fine raindrops falling top to bottom
   - Gentle rising mist droplets in random locations
   - Lens edge rain condensation droplets (after-rain glass beads)
5. Song Mood / Emotion Check:
   - Skips rain for songs with negative or austere themes.
6. Sacred Dhoopa & Agarbatti flame overlays.
"""
import sys, os, json, argparse, subprocess, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
ROOT = Path(__file__).resolve().parents[1]
FFMPEG = shutil.which("ffmpeg") or "C:/ffmpeg/bin/ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or "C:/ffmpeg/bin/ffprobe.exe"
OVERLAY = ROOT / "production" / "sacred_lamp_dhoopa_overlay_1280x720.png"
DRIZZLE = ROOT / "production" / "upward_divine_drizzle_loop.mp4"
FPS = 24
SHOT_DURATION = 6.5
FADE_DURATION = 1.0

# Chapters with negative or intense conflict themes where rain should be omitted:
NEGATIVE_EMOTION_CHAPTERS = {
    86,  # இகல் (Hostility / Grudge)
    87,  # பகைமாட்சி (Enmity)
    88,  # பகைத்திறந்தெரிதல் (Appraising Enmity)
    89,  # உட்பகை (Internal Treachery)
    93,  # கள்ளுண்ணாமை (Drunkenness)
    94,  # சூது (Gambling)
}

def run(cmd):
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)

def dur(p):
    return float(subprocess.check_output([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", str(p)]).decode().strip())

def collect_images_ordered(chapter_num):
    ch_dir = ROOT / "production" / "scene_images" / f"ch{chapter_num:03d}"
    base_imgs = sorted(ch_dir.glob("scene_*.jpg"))
    extra_imgs = sorted((ch_dir / "extra").glob("*.jpg"))

    closeups = [img for img in extra_imgs if "closeup" in img.name]
    virtues = [img for img in extra_imgs if "virtue" in img.name or "google" in img.name or "imagen" in img.name]
    others = [img for img in extra_imgs if img not in closeups and img not in virtues]

    ordered = []
    # Opening 3 base images (crowd/temple entrance)
    ordered.extend(base_imgs[:3])
    if closeups:
        ordered.append(closeups[0])
    
    b_idx, v_idx, c_idx = 3, 0, 1
    while b_idx < len(base_imgs) or v_idx < len(virtues) or c_idx < len(closeups):
        if v_idx < len(virtues):
            ordered.append(virtues[v_idx])
            v_idx += 1
        if b_idx < len(base_imgs):
            ordered.append(base_imgs[b_idx])
            b_idx += 1
        if c_idx < len(closeups):
            ordered.append(closeups[c_idx])
            c_idx += 1

    for o in others:
        if o not in ordered: ordered.append(o)
    for c in closeups:
        if c not in ordered: ordered.append(c)
    for v in virtues:
        if v not in ordered: ordered.append(v)
    return ordered

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--gpu", choices=["none", "nvenc"], default="none", help="Enable NVIDIA GPU NVENC acceleration")
    a = ap.parse_args()
    ch = a.chapter
    use_nvenc = (a.gpu == "nvenc")
    vcodec = "h264_nvenc" if use_nvenc else "libx264"
    enc_opts = ["-preset", "fast", "-cq", "19"] if use_nvenc else ["-preset", "veryfast", "-crf", "17"]

    cur = {c["chapter"]: c for c in json.loads((ROOT / "production/curated_37_waiting_adhigarams.json").read_text(encoding="utf-8"))}
    raw_audio_path = cur[ch]["file_path"]
    
    # Cross-platform audio path resolution
    candidates = [
        Path(raw_audio_path),
        Path("/content/audio") / f"audio_ch{ch:03d}.wav",
        Path("/content/audio") / Path(raw_audio_path).name,
        ROOT / "production" / "audio_staging" / f"audio_ch{ch:03d}.wav",
    ]
    audio = None
    for cand in candidates:
        if cand.exists():
            audio = cand
            break
            
    if audio is None:
        raise FileNotFoundError(f"Audio file not found for Chapter {ch}. Tried: {[str(c) for c in candidates]}")

    adur = dur(audio)
    
    imgs = collect_images_ordered(ch)
    print(f"Chapter {ch}: {len(imgs)} curated unique images | Audio: {adur:.2f}s ({audio.name}) | Encoder: {vcodec}")

    tmp = ROOT / "production" / "temp_build" / f"cinematic_720p_ch{ch:03d}"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)

    effective_per_shot = SHOT_DURATION - FADE_DURATION  # 5.5s
    needed_shots = int((adur + 1.0) / effective_per_shot) + 1
    
    selected_imgs = []
    for i in range(needed_shots):
        selected_imgs.append(imgs[i % len(imgs)])

    print(f"Rendering {len(selected_imgs)} cinematic 720p camera moves (Pan L->R, R->L, Zoom In, Zoom Out, 3D Curved Arc Pan)...")
    clip_files = []
    
    for i, im in enumerate(selected_imgs):
        out_clip = tmp / f"clip_{i:03d}.mp4"
        move_type = i % 5
        
        # Native 720p scaling (1536x864 source crop down to 1280x720) for sharp clean grain-free edges
        if move_type == 0:
            # Cinematic Pan Left-to-Right
            vf = (f"scale=1536:864:flags=lanczos,"
                  f"crop=1280:720:(in_w-out_w)*t/{SHOT_DURATION}:(in_h-out_h)/2,"
                  f"fps={FPS},setsar=1")
        elif move_type == 1:
            # Cinematic Pan Right-to-Left
            vf = (f"scale=1536:864:flags=lanczos,"
                  f"crop=1280:720:(in_w-out_w)*(1-t/{SHOT_DURATION}):(in_h-out_h)/2,"
                  f"fps={FPS},setsar=1")
        elif move_type == 2:
            # Slow push-in with gentle upward drift
            vf = (f"scale=1536:864:flags=lanczos,"
                  f"crop=1280:720:(in_w-out_w)/2:(in_h-out_h)*(1-t/{SHOT_DURATION}),"
                  f"fps={FPS},setsar=1")
        elif move_type == 3:
            # Slow pull-out with gentle center focus
            vf = (f"scale=1536:864:flags=lanczos,"
                  f"crop=1280:720:(in_w-out_w)/2:(in_h-out_h)*t/{SHOT_DURATION},"
                  f"fps={FPS},setsar=1")
        else:
            # 3D Parabolic Curved Arc Pan (crane/dolly parallax curve)
            total_frames = int(SHOT_DURATION * FPS)
            vf = (f"zoompan=z='1.0+0.12*(0.5-0.5*cos(PI*on/{total_frames}))':"
                  f"x='(iw-iw/zoom)*(0.5+0.4*cos(PI*on/{total_frames}))':"
                  f"y='(ih-ih/zoom)*(0.5+0.35*sin(PI*on/{total_frames}))':"
                  f"d={total_frames}:s=1280x720:fps={FPS},setsar=1")
            
        run([
            FFMPEG, "-y", "-loglevel", "error",
            "-loop", "1", "-t", str(SHOT_DURATION), "-i", str(im),
            "-vf", vf,
            "-c:v", vcodec, *enc_opts,
            "-pix_fmt", "yuv420p", "-an", str(out_clip)
        ])
        clip_files.append(out_clip)
        if (i + 1) % 5 == 0 or (i + 1) == len(selected_imgs):
            print(f"  Rendered camera moves: {i+1}/{len(selected_imgs)}...", flush=True)

    print("Assembling seamless cross-dissolve transitions (xfade 1.0s)...")
    stage_clips = []
    chunk_size = 8
    
    for c_idx in range(0, len(clip_files), chunk_size):
        chunk = clip_files[c_idx:c_idx + chunk_size]
        if len(chunk) == 1:
            stage_clips.append(chunk[0])
            continue
            
        stage_out = tmp / f"stage_{c_idx // chunk_size:02d}.mp4"
        inputs = []
        for cf in chunk:
            inputs.extend(["-i", str(cf)])
            
        fc = []
        prev = "[0:v]"
        curr_offset = SHOT_DURATION - FADE_DURATION
        for j in range(1, len(chunk)):
            next_in = f"[{j}:v]"
            out_label = f"[v{j}]" if j < len(chunk) - 1 else "[outv]"
            fc.append(f"{prev}{next_in}xfade=transition=fade:duration={FADE_DURATION}:offset={curr_offset:.2f}{out_label}")
            prev = out_label
            curr_offset += (SHOT_DURATION - FADE_DURATION)
            
        run([
            FFMPEG, "-y", "-loglevel", "error", *inputs,
            "-filter_complex", ";".join(fc),
            "-map", "[outv]",
            "-c:v", vcodec, *enc_opts,
            "-pix_fmt", "yuv420p", str(stage_out)
        ])
        stage_clips.append(stage_out)
        print(f"  Completed dissolve chunk {len(stage_clips)}...", flush=True)

    # Join stage clips with xfade
    if len(stage_clips) == 1:
        base_video = stage_clips[0]
    else:
        base_video = tmp / "base_video.mp4"
        inputs = []
        for sc in stage_clips:
            inputs.extend(["-i", str(sc)])
        fc = []
        prev = "[0:v]"
        curr_offset = dur(stage_clips[0]) - FADE_DURATION
        for j in range(1, len(stage_clips)):
            next_in = f"[{j}:v]"
            out_label = f"[sv{j}]" if j < len(stage_clips) - 1 else "[basev]"
            fc.append(f"{prev}{next_in}xfade=transition=fade:duration={FADE_DURATION}:offset={curr_offset:.2f}{out_label}")
            prev = out_label
            curr_offset += (dur(stage_clips[j]) - FADE_DURATION)
            
        run([
            FFMPEG, "-y", "-loglevel", "error", *inputs,
            "-filter_complex", ";".join(fc),
            "-map", "[basev]",
            "-c:v", vcodec, *enc_opts,
            "-pix_fmt", "yuv420p", str(base_video)
        ])

    print("Compositing final 720p master with realistic drizzle & sacred overlays...")
    ins = ["-i", str(base_video), "-i", str(audio)]
    fc, cur_v, in_idx = ["[0:v]format=rgba[b]"], "[b]", 2

    # Check if this chapter allows drizzle (omitted for negative emotion chapters)
    allow_drizzle = ch not in NEGATIVE_EMOTION_CHAPTERS
    if allow_drizzle and DRIZZLE.exists():
        ins += ["-stream_loop", "-1", "-t", f"{adur:.2f}", "-i", str(DRIZZLE)]
        fc.append(f"[{in_idx}:v]scale=1280:720,fps={FPS},setsar=1,format=gbrp[d]")
        # 0.45 opacity screen blend for realistic subtle droplets
        fc.append(f"{cur_v}format=gbrp[bg];[bg][d]blend=all_mode=screen:all_opacity=0.45:shortest=1,format=rgba[bd]")
        cur_v, in_idx = "[bd]", in_idx + 1
    else:
        print(f"  Note: Drizzle omitted for Chapter {ch} (theme mood / setting)")

    if OVERLAY.exists():
        ins += ["-loop", "1", "-t", f"{adur:.2f}", "-i", str(OVERLAY)]
        fc.append(f"[{in_idx}:v]scale=1280:720,format=rgba[o]")
        fc.append(f"{cur_v}[o]overlay=0:0:shortest=1:format=auto,format=yuv420p[vf]")
        cur_v = "[vf]"
    else:
        fc.append(f"{cur_v}format=yuv420p[vf]")
        cur_v = "[vf]"

    fc.append(f"[1:a]afade=t=out:st={max(0, adur-2):.2f}:d=2[ao]")

    out = ROOT / "renders" / "releases" / f"thirukkural_ch{ch:03d}_cinematic_720p_master.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)

    final_enc = ["-c:v", vcodec] + (["-preset", "fast", "-cq", "18"] if use_nvenc else ["-preset", "medium", "-crf", "17"])
    run([
        FFMPEG, "-y", "-loglevel", "error", *ins,
        "-filter_complex", ";".join(fc),
        "-map", cur_v, "-map", "[ao]",
        "-t", f"{adur:.2f}",
        *final_enc,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        str(out)
    ])

    final_dur = dur(out)
    final_sz = out.stat().st_size / (1024 * 1024)
    print(f"\n==========================================")
    print(f"CINEMATIC 720p MASTER COMPLETED: {out.name}")
    print(f"Duration: {final_dur:.1f}s | File Size: {final_sz:.1f} MB | Resolution: 1280x720")
    print(f"==========================================")
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
