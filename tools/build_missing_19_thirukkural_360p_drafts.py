#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam (@guru-kula-desam)
Batch Builder for the 19 Missing Thirukkural Adhigarams (360p Review Drafts & 1080p Masters)
Supports:
  --resolution 360p  (640x360 @ 24fps, fast review-ready drafts)
  --resolution 1080p (1920x1080 @ 24fps, full HD masters after user approval)
  --chapter <num>    (Optional: render a single chapter, e.g. --chapter 97)
"""

import argparse
import glob
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from PIL import Image, ImageDraw

ROOT_REPO = Path("/home/shishyan/GitHub/GuruKulaDesam")
ASSETS_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets")
LOCAL_ASSETS = Path("/home/shishyan/GuruKulaDesam_Local/assets")
AUDIT_JSON = ROOT_REPO / "production" / "missing_19_thirukkural_adhigarams_audit.json"
DEFAULT_OUT_360P = ROOT_REPO / "production" / "thirukkural_missing_19_drafts_360p"
DEFAULT_OUT_1080P = ROOT_REPO / "production" / "thirukkural_missing_19_masters_1080p"

CHAPTER_METADATA = {
    97: {
        "slug": "Maanam",
        "ta": "மானம்",
        "en": "Honor",
        "kural_range": "961–970",
        "suno_id": "e225af93-d4fd-4f05-98d3-4fac80540018",
        "preferred_wav": "மானம் 1H Golden.wav",
    },
    99: {
        "slug": "Saandraanmai",
        "ta": "சான்றாண்மை",
        "en": "Perfect Goodness",
        "kural_range": "981–990",
        "suno_id": "e38e23bf-d78b-4f6a-bb50-44225131a88b",
        "preferred_wav": "சான்றாண்மை 1Q Golden.wav",
    },
    100: {
        "slug": "Panbudaimai",
        "ta": "பண்புடைமை",
        "en": "Courteous Demeanour",
        "kural_range": "991–1000",
        "suno_id": "8587d5c2-5357-4cc9-b706-642d2212eda9",
        "preferred_wav": "பண்புடைமை 1H Golden.wav",
    },
    101: {
        "slug": "Nandriyil_Selvam",
        "ta": "நன்றியில் செல்வம்",
        "en": "Wealth without Beneficence",
        "kural_range": "1001–1010",
        "suno_id": "711491bf-c18d-4617-9bc8-8d8afd7a3681",
        "preferred_wav": "நன்றியில் செல்வம் 1D Golden.wav",
    },
    102: {
        "slug": "Naanudaimai",
        "ta": "நாணுடைமை",
        "en": "Sensibility to Shame",
        "kural_range": "1011–1020",
        "suno_id": "4aa0e6d3-27b1-4bb4-99fb-529531789c6b",
        "preferred_wav": "நாணுடைமை 1E Golden.wav",
    },
    105: {
        "slug": "Nalkuravu",
        "ta": "நல்குரவு",
        "en": "Poverty",
        "kural_range": "1041–1050",
        "suno_id": "4c61d602-4891-49e6-8778-0d836c9f6bc5",
        "preferred_wav": "நல்குரவு 1I Golden 2026.wav",
    },
    109: {
        "slug": "Thagaiyananguruthal",
        "ta": "தகையணங்குறுத்தல்",
        "en": "Mental Agony Caused by Beauty",
        "kural_range": "1081–1090",
        "suno_id": "2236b3a5-d644-41db-a063-d2c9bdf3fcba",
        "preferred_wav": "தகையணங்குறுத்தல் 1A  Golden Symphony.wav",
    },
    110: {
        "slug": "Kuripparithal",
        "ta": "குறிப்பறிதல்",
        "en": "Recognition of the Signs",
        "kural_range": "1091–1100",
        "suno_id": "cec3ef06-1657-4cdd-813e-83d1e0e29bbf",
        "preferred_wav": "குறிப்பறிதல்_Ch110_Suno_Shishyan_1091_1100.wav",
    },
    111: {
        "slug": "Punarchi_Magizhthal",
        "ta": "புணர்ச்சி மகிழ்தல்",
        "en": "Rejoicing in the Embrace",
        "kural_range": "1101–1110",
        "suno_id": "43ee183b-abf1-4fb2-bb26-62c0f21ce78d",
        "preferred_wav": "புணர்ச்சிமகிழ்தல் 1F Symphony.wav",
    },
    112: {
        "slug": "Nalam_Punaindhuraithal",
        "ta": "நலம் புனைந்துரைத்தல்",
        "en": "Praise of Her Beauty",
        "kural_range": "1111–1120",
        "suno_id": "011769e2-6cf6-47b9-a68b-b5b7e66e9ab3",
        "preferred_wav": "நலம்புனைந்துரைத்தல் 1D Golden.wav",
    },
    114: {
        "slug": "Naanuthuravuraithal",
        "ta": "நாணுத்துறவுரைத்தல்",
        "en": "Declaration of Loss of Reserve",
        "kural_range": "1131–1140",
        "suno_id": "fa9d2038-0fa9-495c-a0f7-da4b282b2d0e",
        "preferred_wav": "நாணுத்துறவுரைத்தல் 1C Golden Symphony.wav",
    },
    116: {
        "slug": "Pirivaatraamai",
        "ta": "பிரிவாற்றாமை",
        "en": "Separation Unendurable",
        "kural_range": "1151–1160",
        "suno_id": "4e1d09cb-ffc1-47a3-a2d3-333120c8351c",
        "preferred_wav": "பிரிவாற்றாமை Golden 2026.wav",
    },
    117: {
        "slug": "Padarmelindhirangal",
        "ta": "படர்மெலிந்திரங்கல்",
        "en": "Pining Desire",
        "kural_range": "1161–1170",
        "suno_id": "f5ab3b96-98b5-407e-b5c1-820561019a14",
        "preferred_wav": "படர்மெலிந்திரங்கல் Golden 2026.wav",
    },
    119: {
        "slug": "Pasappuru_Paruvaral",
        "ta": "பசப்புறு பருவரல்",
        "en": "Pallid Hue of Longing",
        "kural_range": "1181–1190",
        "suno_id": "0f9b1df1-8c3c-4995-8385-764c97b89371",
        "preferred_wav": "பசப்புறுபருவரல் Golden.wav",
    },
    120: {
        "slug": "Thanippadar_Miguthi",
        "ta": "தனிப்படர் மிகுதி",
        "en": "Solitary Anguish",
        "kural_range": "1191–1200",
        "suno_id": "c09c99fa-0fce-425a-aa24-a22cbbbc62e5",
        "preferred_wav": "தனிப்படர்மிகுதி (Symphony).wav",
    },
    121: {
        "slug": "Ninaindhavar_Pulambal",
        "ta": "நினைந்தவர் புலம்பல்",
        "en": "Sad Memories",
        "kural_range": "1201–1210",
        "suno_id": "b8e90c50-8def-401a-a5ab-10250e80aaee",
        "preferred_wav": "நினைந்தவர்புலம்பல் (Original).wav",
    },
    123: {
        "slug": "Pozhuthukandu_Irangal",
        "ta": "பொழுதுகண்டு இரங்கல்",
        "en": "Lamentations at Eventide",
        "kural_range": "1221–1230",
        "suno_id": "4fc54f95-5c00-4989-99b8-72a302e828da",
        "preferred_wav": "பொழுதுகண்டிரங்கல் (Original).wav",
    },
    126: {
        "slug": "Niraiyazhithal",
        "ta": "நிறையழிதல்",
        "en": "Reserve Overcome",
        "kural_range": "1251–1260",
        "suno_id": "51fb0632-d97d-4c68-b3e0-212cd36838cb",
        "preferred_wav": "நிறையழிதல் (Original).wav",
    },
    129: {
        "slug": "Punarchi_Vithumbal",
        "ta": "புணர்ச்சி விதும்பல்",
        "en": "Longing for Reunion",
        "kural_range": "1281–1290",
        "suno_id": "a8014812-5aa4-48a9-a67a-40ff0adb8373",
        "preferred_wav": "புணர்ச்சிவிதும்பல் 1 A Golden.wav",
    },
}


def build_static_sacred_overlay(w: int, h: int, out_png: Path):
    """Builds the sacred side lamps, bottom brass thoopam burners, and channel avatar overlay."""
    scale_x = w / 1920.0
    scale_y = h / 1080.0
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    diya_path = LOCAL_ASSETS / "diya_master_perfect_final.png"
    if diya_path.exists():
        dw = max(12, int(round(42 * scale_x)))
        dh = max(14, int(round(48 * scale_y)))
        diya_master = Image.open(diya_path).convert("RGBA")
        diya_small = diya_master.resize((dw, dh), Image.Resampling.LANCZOS)
        diya_alpha = diya_small.split()[3].point(lambda p: int(p * 0.75))
        diya_small.putalpha(diya_alpha)
        pad_x = max(4, int(round(12 * scale_x)))
        top_y = int(round(50 * scale_y))
        span_y = h - int(round(130 * scale_y))
        for i in range(9):
            y = int(top_y + i * span_y / 8.0)
            canvas.alpha_composite(diya_small, (pad_x, y))
            diya_flipped = diya_small.transpose(Image.FLIP_LEFT_RIGHT)
            canvas.alpha_composite(diya_flipped, (w - pad_x - dw, y))

    thoopam_path = LOCAL_ASSETS / "dheepam-thoopam-corners.png"
    if thoopam_path.exists():
        corners_img = Image.open(thoopam_path).convert("RGBA")
        thoopam_crop = corners_img.crop((20, 715, 160, 935))
        tw = max(28, int(round(96 * scale_x)))
        th = max(44, int(round(150 * scale_y)))
        thoopam_scaled = thoopam_crop.resize((tw, th), Image.Resampling.LANCZOS)
        tx = max(16, int(round(52 * scale_x)))
        ty = h - th - max(5, int(round(15 * scale_y)))
        canvas.alpha_composite(thoopam_scaled, (tx, ty))
        canvas.alpha_composite(
            thoopam_scaled.transpose(Image.FLIP_LEFT_RIGHT), (w - tw - tx, ty)
        )

    avatar_path = LOCAL_ASSETS / "channel-avatar-reference.jpg"
    if avatar_path.exists():
        logo_size = max(28, int(round(84 * scale_x)))
        avatar = (
            Image.open(avatar_path)
            .convert("RGB")
            .resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        )
        mask = Image.new("L", (logo_size, logo_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, logo_size - 1, logo_size - 1), fill=255)
        logo_rgba = Image.new("RGBA", (logo_size, logo_size), (0, 0, 0, 0))
        logo_rgba.paste(avatar, (0, 0), mask)
        ImageDraw.Draw(logo_rgba).ellipse(
            (0, 0, logo_size - 1, logo_size - 1),
            outline=(218, 165, 32, 220),
            width=1,
        )
        logo_rgba.putalpha(mask.point(lambda p: int(p * 0.85)))
        ax = int(round(1740 * scale_x)) - logo_size // 2
        ay = int(round(908 * scale_y)) - logo_size // 2
        canvas.alpha_composite(logo_rgba, (ax, ay))

    canvas.save(out_png)


def write_title_ass(ch_num: int, ta_name: str, duration: float, w: int, h: int, ass_path: Path):
    """Writes top-center Tamil title header ASS file."""
    font_size = 24 if w >= 1920 else 11
    outline = 3.0 if w >= 1920 else 1.5
    shadow = 4.0 if w >= 1920 else 2.0
    margin_v = 12 if w >= 1920 else 6

    def to_tc(s: float) -> str:
        hrs = int(s // 3600)
        mins = int((s % 3600) // 60)
        secs = s % 60
        return f"{hrs}:{mins:02d}:{secs:05.2f}"

    title_str = f"அதிகாரம் {ch_num} : {ta_name}"
    content = f"""[Script Info]
Title: Thirukkural Ch{ch_num:03d}
ScriptType: v4.00+
WrapStyle: 0
PlayResX: {w}
PlayResY: {h}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Noto Sans Tamil,{font_size},&H00FFFFFF,&H000000FF,&H00181890,&H00000000,1,0,0,0,100,100,0,0,1,{outline},{shadow},8,10,10,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{to_tc(duration)},Title,,0,0,{margin_v},,{{\\b1}}{title_str}{{\\b0}}
"""
    ass_path.write_text(content, encoding="utf-8")


def get_audio_duration(wav_path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(wav_path),
    ]
    out = subprocess.check_output(cmd).decode("utf-8").strip()
    return float(out)


def build_pendulum_sequence(scenes: list, total_duration: float, target_cut_sec: float = 6.0) -> list:
    """
    Orders all 37-38 scene images in forward-reverse pendulum sequence
    across the full audio duration (~6 seconds per scene cut).
    """
    n = len(scenes)
    if n == 0:
        raise RuntimeError("No valid scene images found!")
    total_cuts = max(n, int(round(total_duration / target_cut_sec)))
    if n == 1:
        return [scenes[0]] * total_cuts

    # Pendulum cycle: 0, 1, ..., n-1, n-2, ..., 1
    cycle = list(range(n)) + list(range(n - 2, 0, -1))
    seq = [scenes[cycle[i % len(cycle)]] for i in range(total_cuts)]
    return seq


def render_single_chapter(task: dict) -> dict:
    ch = task["chapter"]
    meta = CHAPTER_METADATA[ch]
    asset_dir = Path(task["asset_dir"])
    wav_path = Path(task["wav_path"])
    out_mp4 = Path(task["out_mp4"])
    res_mode = task["resolution"]
    w, h = (1920, 1080) if res_mode == "1080p" else (640, 360)
    fps = 24

    # Collect and validate Scene_01 .. Scene_38 images
    raw_scenes = sorted(asset_dir.glob("Scene_*.jpg"))
    valid_scenes = [p for p in raw_scenes if p.stat().st_size > 1000]
    if not valid_scenes:
        raise RuntimeError(f"Ch {ch:03d}: No valid Scene_*.jpg found in {asset_dir}")

    # Copy scenes and audio to local /tmp workspace to avoid slow FUSE reads during ffmpeg encoding
    tmp_dir = Path(tempfile.mkdtemp(prefix=f"gkd_ch{ch:03d}_{res_mode}_"))
    try:
        local_wav = tmp_dir / "audio.wav"
        shutil.copy2(wav_path, local_wav)
        duration = get_audio_duration(local_wav)

        local_scenes = []
        hash_to_local = {}
        for idx, s_path in enumerate(valid_scenes):
            st = s_path.stat()
            sig = (st.st_size,)
            if sig in hash_to_local:
                # Avoid redundant FUSE reads if identical size and header/tail match
                dst_img = hash_to_local[sig]
            else:
                dst_img = tmp_dir / f"scene_{idx:03d}.jpg"
                shutil.copy2(s_path, dst_img)
                hash_to_local[sig] = dst_img
            local_scenes.append(dst_img)

        pendulum_imgs = build_pendulum_sequence(local_scenes, duration, target_cut_sec=6.0)
        num_cuts = len(pendulum_imgs)
        cut_dur = duration / float(num_cuts)

        # Write ffmpeg concat file
        concat_txt = tmp_dir / "concat.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for img_p in pendulum_imgs:
                f.write(f"file '{img_p.as_posix()}'\n")
                f.write(f"duration {cut_dur:.6f}\n")
            # Repeat last image for concat demuxer termination
            f.write(f"file '{pendulum_imgs[-1].as_posix()}'\n")

        overlay_png = tmp_dir / "overlay.png"
        build_static_sacred_overlay(w, h, overlay_png)

        title_ass = tmp_dir / "title.ass"
        write_title_ass(ch, meta["ta"], duration, w, h, title_ass)

        # Gentle dynamic camera breathing + sacred overlay + Tamil title header
        overscan_w = int(round(w * 1.08))
        overscan_h = int(round(h * 1.08))
        ass_escaped = title_ass.as_posix().replace(":", "\\:")

        vf_chain = (
            f"[0:v]fps={fps},"
            f"scale={overscan_w}:{overscan_h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}:x='(iw-ow)/2+((iw-ow)/2)*0.75*sin(2*PI*t/12.0)':y='(ih-oh)/2+((ih-oh)/2)*0.75*cos(2*PI*t/16.0)',"
            f"setsar=1,format=rgba[bg];"
            f"[1:v]format=rgba[ov];"
            f"[bg][ov]overlay=0:0:format=auto,"
            f"ass=filename='{ass_escaped}',"
            f"format=yuv420p[vout]"
        )

        crf = "19" if res_mode == "1080p" else "21"
        preset = "fast" if res_mode == "1080p" else "veryfast"

        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_txt),
            "-i",
            str(overlay_png),
            "-i",
            str(local_wav),
            "-filter_complex",
            vf_chain,
            "-map",
            "[vout]",
            "-map",
            "2:a:0",
            "-r",
            str(fps),
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-crf",
            crf,
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-t",
            f"{duration:.3f}",
            "-movflags",
            "+faststart",
            "-loglevel",
            "error",
            str(out_mp4),
        ]
        subprocess.run(cmd, check=True)

        # Verify output via ffprobe
        probe_cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size",
            "-show_entries",
            "stream=codec_type,width,height",
            "-of",
            "json",
            str(out_mp4),
        ]
        probe_data = json.loads(subprocess.check_output(probe_cmd).decode("utf-8"))
        out_dur = float(probe_data["format"]["duration"])
        out_size = int(probe_data["format"]["size"])

        return {
            "chapter": ch,
            "adhigaram_ta": meta["ta"],
            "adhigaram_en": meta["en"],
            "kural_range": meta["kural_range"],
            "suno_id": meta["suno_id"],
            "title": f"திருக்குறள் - அதிகாரம் {ch}: {meta['ta']} | Thirukkural Chapter {ch}: {meta['en']}",
            "audio_source": str(wav_path),
            "audio_filename": wav_path.name,
            "audio_duration_sec": round(duration, 2),
            "video_duration_sec": round(out_dur, 2),
            "unique_scene_count": len(valid_scenes),
            "pendulum_cut_count": num_cuts,
            "seconds_per_cut": round(cut_dur, 2),
            "resolution": f"{w}x{h}",
            "fps": fps,
            "draft_360p_path": str(out_mp4) if res_mode == "360p" else str(DEFAULT_OUT_360P / f"Ch{ch:03d}_{meta['slug']}_360p_draft.mp4"),
            "output_path": str(out_mp4),
            "file_size_mb": round(out_size / (1024 * 1024), 2),
            "upscale_1080p_command": f"python3 /home/shishyan/GitHub/GuruKulaDesam/tools/build_missing_19_thirukkural_360p_drafts.py --resolution 1080p --chapter {ch}",
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Build Thirukkural 360p drafts or 1080p masters for the 19 missing Adhigarams.")
    parser.add_argument("--resolution", choices=["360p", "1080p"], default="360p", help="Target resolution (360p or 1080p)")
    parser.add_argument("--chapter", type=int, default=None, help="Optional single chapter number to build")
    parser.add_argument("--workers", type=int, default=4, help="Parallel chapter render workers")
    parser.add_argument("--output-dir", type=str, default=None, help="Custom output directory")
    args = parser.parse_args()

    with open(AUDIT_JSON, "r", encoding="utf-8") as f:
        audit_list = json.load(f)

    out_dir = Path(args.output_dir) if args.output_dir else (DEFAULT_OUT_1080P if args.resolution == "1080p" else DEFAULT_OUT_360P)
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks = []
    for item in audit_list:
        ch = item["chapter"]
        if args.chapter is not None and ch != args.chapter:
            continue
        meta = CHAPTER_METADATA[ch]
        asset_dir = ASSETS_ROOT / item["asset_folders"][0]
        wav_path = asset_dir / meta["preferred_wav"]
        if not wav_path.exists():
            raise FileNotFoundError(f"Ch {ch:03d} preferred WAV not found: {wav_path}")

        suffix = "360p_draft" if args.resolution == "360p" else "1080p_master"
        out_mp4 = out_dir / f"Ch{ch:03d}_{meta['slug']}_{suffix}.mp4"
        tasks.append(
            {
                "chapter": ch,
                "asset_dir": str(asset_dir),
                "wav_path": str(wav_path),
                "out_mp4": str(out_mp4),
                "resolution": args.resolution,
            }
        )

    print(f"Building {len(tasks)} Thirukkural chapter video(s) at {args.resolution} into {out_dir} ...")
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        future_map = {pool.submit(render_single_chapter, t): t["chapter"] for t in tasks}
        for fut in as_completed(future_map):
            ch_num = future_map[fut]
            res = fut.result()
            results.append(res)
            print(
                f"  [DONE] Ch{ch_num:03d} ({res['adhigaram_ta']} / {res['adhigaram_en']}): "
                f"{Path(res['output_path']).name} | {res['video_duration_sec']}s | {res['unique_scene_count']} scenes | {res['file_size_mb']} MB",
                flush=True,
            )

    results.sort(key=lambda x: x["chapter"])

    if args.chapter is None:
        manifest_name = "drafts_360p_manifest.json" if args.resolution == "360p" else "masters_1080p_manifest.json"
        manifest_path = out_dir / manifest_name
        manifest_payload = {
            "channel": "@guru-kula-desam",
            "resolution": args.resolution,
            "dimensions": "640x360" if args.resolution == "360p" else "1920x1080",
            "fps": 24,
            "total_chapters": len(results),
            "upscale_all_1080p_command": "python3 /home/shishyan/GitHub/GuruKulaDesam/tools/build_missing_19_thirukkural_360p_drafts.py --resolution 1080p",
            "chapters": results,
        }
        manifest_path.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nSaved manifest: {manifest_path}")


if __name__ == "__main__":
    main()
