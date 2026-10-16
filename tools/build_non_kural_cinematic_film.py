#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_non_kural_cinematic_film.py
Unified Broadcast-Quality Cinematic 720p Film Assembler for Non-Thirukkural Songs:
- Supports arbitrary audio files (WAV/MP3/M4A).
- Supports dedicated scene image folders with 16:9 images.
- 4-way cinematic camera moves (Pan L->R, Pan R->L, Slow Push, Slow Pull, and 3D cosine-eased parabolic panzoom).
- 1.0s smooth cross-dissolve (xfade) transitions.
- Upward divine drizzle screen blend (0.45 opacity).
- Procedural / self-healing sacred lamp dhoopa overlay.
- Untouched master audio or 256k AAC stereo 48kHz remux with gentle 2.0s fadeout.
- High-efficiency NVENC or CPU libx264 encoding.
"""
import sys, os, json, argparse, subprocess, shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = shutil.which("ffmpeg") or "C:/ffmpeg/bin/ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or "C:/ffmpeg/bin/ffprobe.exe"
OVERLAY = ROOT / "production" / "sacred_lamp_dhoopa_overlay_1280x720.png"
DRIZZLE = ROOT / "production" / "upward_divine_drizzle_loop.mp4"

# Validate or auto-generate valid PNG overlay if corrupt/missing
try:
    if not OVERLAY.exists() or OVERLAY.stat().st_size < 1000 or not OVERLAY.read_bytes().startswith(b'\x89PNG'):
        from tools.sacred_overlay_data import SACRED_OVERLAY_PNG_B64
        import base64
        OVERLAY.parent.mkdir(parents=True, exist_ok=True)
        OVERLAY.write_bytes(base64.b64decode(SACRED_OVERLAY_PNG_B64))
        print("Restored valid sacred_lamp_dhoopa_overlay_1280x720.png from embedded asset.")
except Exception:
    pass

FPS = 24
SHOT_DURATION = 6.5
FADE_DURATION = 1.0

def run(cmd):
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)

def dur(p):
    return float(subprocess.check_output([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", str(p)]).decode().strip())

def is_valid_image(p):
    try:
        if not p.is_file() or p.stat().st_size < 1000:
            return False
        header = p.read_bytes()[:16]
        if header.startswith(b'\xff\xd8\xff') or header.startswith(b'\x89PNG\r\n\x1a\n') or (header.startswith(b'RIFF') and b'WEBP' in header):
            return True
        return False
    except Exception:
        return False

def collect_images_from_dir(image_dir):
    p = Path(image_dir)
    if not p.exists():
        raise FileNotFoundError(f"Image directory not found: {image_dir}")
    imgs = [f for f in sorted(p.glob("*.*")) if is_valid_image(f)]
    if not imgs:
        raise ValueError(f"No valid images found in {image_dir}")
    return imgs

def build_film(audio_path, image_dir, output_path, title="Cinematic Master Film", gpu="none", allow_drizzle=True):
    audio = Path(audio_path)
    if not audio.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    imgs = collect_images_from_dir(image_dir)
    adur = dur(audio)
    use_nvenc = (gpu == "nvenc")
    vcodec = "h264_nvenc" if use_nvenc else "libx264"
    enc_opts = ["-preset", "fast", "-cq", "19"] if use_nvenc else ["-preset", "veryfast", "-crf", "17"]

    print("=" * 60)
    print(f"🎬 BUILDING CINEMATIC 720p FILM: {title}")
    print(f"🎵 Audio: {audio.name} ({adur:.2f}s / {adur/60:.2f} min)")
    print(f"🖼️ Images: {len(imgs)} curated scenes from {Path(image_dir).name}")
    print(f"⚙️ Video Codec: {vcodec} (GPU: {gpu})")
    print("=" * 60)

    stem = Path(output_path).stem
    tmp = ROOT / "production" / "temp_build" / stem
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True, exist_ok=True)

    effective_per_shot = SHOT_DURATION - FADE_DURATION  # 5.5s
    needed_shots = int((adur + 1.0) / effective_per_shot) + 1

    selected_imgs = []
    for i in range(needed_shots):
        selected_imgs.append(imgs[i % len(imgs)])

    print(f"Rendering {len(selected_imgs)} cinematic camera moves across parallel threads...")
    from concurrent.futures import ThreadPoolExecutor

    def render_single_clip(item):
        i, im = item
        out_clip = tmp / f"clip_{i:03d}.mp4"
        move_type = i % 5

        if move_type == 0:
            vf = (f"scale=1536:864:flags=bicubic,"
                  f"crop=1280:720:(in_w-out_w)*t/{SHOT_DURATION}:(in_h-out_h)/2,"
                  f"fps={FPS},setsar=1")
        elif move_type == 1:
            vf = (f"scale=1536:864:flags=bicubic,"
                  f"crop=1280:720:(in_w-out_w)*(1-t/{SHOT_DURATION}):(in_h-out_h)/2,"
                  f"fps={FPS},setsar=1")
        elif move_type == 2:
            vf = (f"scale=1536:864:flags=bicubic,"
                  f"crop=1280:720:(in_w-out_w)/2:(in_h-out_h)*(1-t/{SHOT_DURATION}),"
                  f"fps={FPS},setsar=1")
        elif move_type == 3:
            vf = (f"scale=1536:864:flags=bicubic,"
                  f"crop=1280:720:(in_w-out_w)/2:(in_h-out_h)*t/{SHOT_DURATION},"
                  f"fps={FPS},setsar=1")
        else:
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
        return i, out_clip

    workers = 24 if use_nvenc else 6
    clip_files = [None] * len(selected_imgs)
    done_count = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for idx, path in executor.map(render_single_clip, enumerate(selected_imgs)):
            clip_files[idx] = path
            done_count += 1
            if done_count % 15 == 0 or done_count == len(selected_imgs):
                print(f"  Camera moves rendered: {done_count}/{len(selected_imgs)}...", flush=True)

    print("Assembling seamless cross-dissolve transitions (xfade 1.0s)...")
    chunk_size = 8
    chunks = [clip_files[c_idx:c_idx + chunk_size] for c_idx in range(0, len(clip_files), chunk_size)]

    def render_stage_chunk(item):
        s_idx, chunk = item
        if len(chunk) == 1:
            return s_idx, chunk[0]

        stage_out = tmp / f"stage_{s_idx:02d}.mp4"
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
        return s_idx, stage_out

    stage_clips = [None] * len(chunks)
    with ThreadPoolExecutor(max_workers=min(workers, len(chunks))) as executor:
        for s_idx, s_path in executor.map(render_stage_chunk, enumerate(chunks)):
            stage_clips[s_idx] = s_path
            print(f"  Dissolve chunk {s_idx + 1}/{len(chunks)} complete...", flush=True)

    # Join stage clips
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

    print("Compositing final 720p master with upward drizzle & sacred lamp overlays...")
    ins = ["-i", str(base_video), "-i", str(audio)]
    fc, cur_v, in_idx = ["[0:v]format=rgba[b]"], "[b]", 2

    if allow_drizzle and DRIZZLE.exists():
        ins += ["-stream_loop", "-1", "-t", f"{adur:.2f}", "-i", str(DRIZZLE)]
        fc.append(f"[{in_idx}:v]scale=1280:720,fps={FPS},setsar=1,format=gbrp[d]")
        fc.append(f"{cur_v}format=gbrp[bg];[bg][d]blend=all_mode=screen:all_opacity=0.45:shortest=1,format=rgba[bd]")
        cur_v, in_idx = "[bd]", in_idx + 1

    overlay_valid = False
    try:
        if OVERLAY.exists() and OVERLAY.stat().st_size > 1000 and OVERLAY.read_bytes().startswith(b'\x89PNG'):
            overlay_valid = True
    except Exception:
        overlay_valid = False

    if overlay_valid:
        ins += ["-loop", "1", "-t", f"{adur:.2f}", "-i", str(OVERLAY)]
        fc.append(f"[{in_idx}:v]scale=1280:720,format=rgba[o]")
        fc.append(f"{cur_v}[o]overlay=0:0:shortest=1:format=auto,format=yuv420p[vf]")
        cur_v = "[vf]"
    else:
        fc.append(f"{cur_v}format=yuv420p[vf]")
        cur_v = "[vf]"

    fc.append(f"[1:a]afade=t=out:st={max(0, adur-2):.2f}:d=2[ao]")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    final_enc = ["-c:v", vcodec] + (["-preset", "fast", "-cq", "18"] if use_nvenc else ["-preset", "veryfast", "-crf", "18"])
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
    print("\n==========================================")
    print(f"✔ MASTER FILM COMPLETED: {out.name}")
    print(f"Duration: {final_dur:.1f}s | Size: {final_sz:.1f} MB | Resolution: 1280x720")
    print("==========================================")
    shutil.rmtree(tmp, ignore_errors=True)
    return str(out)

def main():
    ap = argparse.ArgumentParser(description="Build Cinematic Devotional Film for Non-Kural Songs")
    ap.add_argument("--audio", required=True, help="Path to audio file (WAV)")
    ap.add_argument("--images-dir", required=True, help="Directory containing 16:9 scene images")
    ap.add_argument("--output", required=True, help="Output MP4 file path")
    ap.add_argument("--title", default="Cinematic Master Film", help="Display title")
    ap.add_argument("--gpu", choices=["none", "nvenc"], default="none", help="GPU encoder")
    ap.add_argument("--no-drizzle", action="store_true", help="Omit upward drizzle effect")
    a = ap.parse_args()

    build_film(
        audio_path=a.audio,
        image_dir=a.images_dir,
        output_path=a.output,
        title=a.title,
        gpu=a.gpu,
        allow_drizzle=not a.no_drizzle
    )

if __name__ == "__main__":
    main()
