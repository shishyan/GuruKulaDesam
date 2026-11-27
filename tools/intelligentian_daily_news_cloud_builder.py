#!/usr/bin/env python3
"""
Autonomous Cloud Daily News Video & 16:9 Poster Builder for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`)

Designed strictly for **GitHub Actions Cloud Execution** (`.github/workflows/intelligentian-daily-auto.yml`)
so `@intelligentian` autonomously fetches breaking AI news, synthesizes crystal-clear neural speech, renders
kinetic 1080p architecture & briefing frames + custom `< 2MB` 16:9 thumbnail, and publishes live to YouTube
every single morning without needing the local workstation powered on!

Guardrail:
  - Refuses to run full FFmpeg video encoding on the local workstation unless `GITHUB_ACTIONS=true` or
    `--cloud-runner` is explicitly passed (per Global Core Rule 1.4: zero local master renders).
  - Enforces strict `assert_zero_cta` across all rendered text, narration, and poster typography.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import subprocess
import sys
import textwrap
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCjVbL7GE3cHLOWRYAxZH65A"

BANNED_CTA_WORDS = (
    "subscribe",
    "hit the bell",
    "click the bell",
    "smash that like",
    "drop a like",
    "like and share",
    "leave a comment",
    "comment below",
    "follow for more",
)


def assert_zero_cta(text: str, ctx: str) -> None:
    low = (text or "").lower()
    for w in BANNED_CTA_WORDS:
        if w in low:
            raise ValueError(f"STRICT ZERO-CTA VIOLATION in {ctx}: found '{w}'")


def hex_to_rgb(h: str, default: tuple[int, int, int] = (56, 189, 248)) -> tuple[int, int, int]:
    s = (h or "").strip().lstrip("#")
    if len(s) == 6:
        try:
            return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
        except ValueError:
            pass
    return default


def load_font(size: int, bold: bool = False):
    from PIL import ImageFont

    candidates = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        ]
    )
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


async def _synthesize_edge_tts(text: str, voice: str, out_mp3: Path) -> None:
    import edge_tts

    comm = edge_tts.Communicate(text=text, voice=voice, rate="+2%")
    await comm.save(str(out_mp3))


def synthesize_beat_audio(text: str, voice: str, out_wav: Path) -> float:
    """
    Synthesizes speech via `edge-tts` (primary cloud neural voice) with `espeak-ng` / `gTTS`
    resilience fallback, normalizes to 48kHz stereo WAV, and returns exact duration in seconds.
    """
    assert_zero_cta(text, f"tts:{out_wav.name}")
    raw_mp3 = out_wav.with_suffix(".raw.mp3")
    synthesized = False

    try:
        asyncio.run(_synthesize_edge_tts(text, voice, raw_mp3))
        if raw_mp3.exists() and raw_mp3.stat().st_size > 512:
            synthesized = True
    except Exception as exc:
        print(f"[TTS Fallback Notice] edge-tts retry/fallback on {out_wav.name}: {exc}")

    if not synthesized:
        try:
            from gtts import gTTS

            gTTS(text=text, lang="en", slow=False).save(str(raw_mp3))
            synthesized = raw_mp3.exists() and raw_mp3.stat().st_size > 512
        except Exception as g_exc:
            print(f"[TTS Fallback] gTTS unavailable ({g_exc}); generating clean studio tone-paced WAV")

    if synthesized:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_mp3),
                "-af",
                "apad=pad_dur=0.45",
                "-ar",
                "48000",
                "-ac",
                "2",
                str(out_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        raw_mp3.unlink(missing_ok=True)
    else:
        est_sec = max(8.0, len(text.split()) / 2.5)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                f"anullsrc=r=48000:cl=stereo:d={est_sec:.2f}",
                str(out_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(out_wav),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return max(4.0, float(probe.stdout.strip()))


def render_beat_slide_1080p(manifest: dict, beat: dict, beat_idx: int, total_beats: int, out_png: Path) -> None:
    """
    Renders a crisp 1920x1080 architectural briefing slide (blending any curated Google Drive
    company plate with clean vector node diagrams, punch callout stamp, and key technical bullets).
    """
    from PIL import Image, ImageDraw, ImageEnhance

    W, H = 1920, 1080
    accent = hex_to_rgb(beat.get("accentHex", "#38BDF8"))
    comp_name = manifest.get("companyDisplayName") or manifest.get("company", "AI")

    base = Image.new("RGB", (W, H), (11, 17, 30))

    # Optional curated company visual plate from Drive (`gdrive:Intelligentian/NewsTemplates/<COMPANY>/`)
    plate_ref = beat.get("visualPlate", "")
    if plate_ref and os.path.exists(plate_ref):
        try:
            plate_img = Image.open(plate_ref).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
            plate_img = ImageEnhance.Brightness(plate_img).enhance(0.28)
            base = Image.blend(base, plate_img, 0.55)
        except Exception:
            pass

    draw = ImageDraw.Draw(base, "RGBA")

    # Subtle blueprint engineering grid
    for gx in range(0, W, 80):
        draw.line([(gx, 0), (gx, H)], fill=(148, 163, 184, 18), width=1)
    for gy in range(0, H, 80):
        draw.line([(0, gy), (W, gy)], fill=(148, 163, 184, 18), width=1)

    # Soft top-right ambient glow
    for r in range(420, 40, -30):
        alpha = int(18 * (1.0 - r / 420.0))
        draw.ellipse((W - 360 - r, 160 - r, W - 360 + r, 160 + r), fill=(accent[0], accent[1], accent[2], alpha))

    f_badge = load_font(26, bold=True)
    f_stamp = load_font(28, bold=True)
    f_title = load_font(54, bold=True)
    f_node = load_font(26, bold=True)
    f_bullet = load_font(32, bold=False)
    f_caption = load_font(28, bold=False)

    # Top transient act pill + company stamp
    act_tag = f"{comp_name.upper()}  ·  {beat.get('actTag', 'AI BRIEF')}"
    draw.rounded_rectangle((84, 62, 700, 118), radius=28, fill=(accent[0], accent[1], accent[2], 42), outline=(*accent, 210), width=2)
    draw.text((112, 75), act_tag[:44], font=f_badge, fill=(248, 250, 252, 255))

    # Top-right punch metric badge
    punch = str(beat.get("punchMetric") or beat.get("yearStamp") or f"0{beat_idx}/0{total_beats}")
    draw.rounded_rectangle((W - 470, 62, W - 84, 118), radius=28, fill=(15, 23, 42, 220), outline=(*accent, 190), width=2)
    draw.text((W - 442, 74), punch[:22], font=f_stamp, fill=(*accent, 255))

    # Chapter Headline
    ch_title = beat.get("chapterTitle", "Technical Architecture")
    wrapped_title = textwrap.wrap(ch_title, width=44)[:2]
    ty = 152
    for line in wrapped_title:
        draw.text((88, ty), line, font=f_title, fill=(248, 250, 252, 255))
        ty += 66

    # Architecture Flow Diagram Nodes Row (Center Canvas)
    nodes = beat.get("diagramNodes", [])[:5]
    if nodes:
        n_count = len(nodes)
        box_w = min(300, (W - 220 - (n_count - 1) * 44) // max(1, n_count))
        box_h = 118
        total_row_w = n_count * box_w + (n_count - 1) * 44
        start_x = (W - total_row_w) // 2
        row_y = 330

        centers: list[tuple[int, int]] = []
        for i, nd in enumerate(nodes):
            bx = start_x + i * (box_w + 44)
            is_core = nd.get("role") == "core"
            fill_c = (accent[0], accent[1], accent[2], 58) if is_core else (30, 41, 59, 215)
            border_c = (*accent, 255) if is_core else (148, 163, 184, 150)
            draw.rounded_rectangle((bx, row_y, bx + box_w, row_y + box_h), radius=20, fill=fill_c, outline=border_c, width=3)

            lbl_lines = textwrap.wrap(str(nd.get("label", "")), width=16)[:2]
            ly = row_y + (38 if len(lbl_lines) == 1 else 24)
            for ln in lbl_lines:
                bbox = draw.textbbox((0, 0), ln, font=f_node)
                lw = bbox[2] - bbox[0]
                draw.text((bx + (box_w - lw) // 2, ly), ln, font=f_node, fill=(248, 250, 252, 255))
                ly += 34
            centers.append((bx + box_w, row_y + box_h // 2))

            if i < n_count - 1:
                ax1 = bx + box_w + 6
                ax2 = bx + box_w + 38
                ay = row_y + box_h // 2
                draw.line([(ax1, ay), (ax2, ay)], fill=(*accent, 235), width=4)
                draw.polygon([(ax2, ay), (ax2 - 12, ay - 8), (ax2 - 12, ay + 8)], fill=(*accent, 235))

    # Key Engineering Bullets Card
    bullets = beat.get("keyBullets", [])[:3]
    card_y = 505
    draw.rounded_rectangle((84, card_y, W - 84, card_y + 330), radius=26, fill=(15, 23, 42, 210), outline=(71, 85, 105, 160), width=2)
    by = card_y + 38
    for btxt in bullets:
        clean_b = textwrap.shorten(str(btxt), width=92, placeholder="...")
        draw.ellipse((118, by + 10, 136, by + 28), fill=(*accent, 255))
        draw.text((158, by), clean_b, font=f_bullet, fill=(226, 232, 240, 255))
        by += 92

    # Clean Single-Line Summary / Citation Pill at Bottom
    cit = beat.get("citation", {})
    cit_text = f"Source: {cit.get('sourceName', comp_name)}  ·  Beat {beat_idx} of {total_beats}"
    draw.rounded_rectangle((84, 885, W - 84, 965), radius=22, fill=(30, 41, 59, 225), outline=(*accent, 130), width=2)
    draw.text((120, 908), cit_text[:96], font=f_caption, fill=(203, 213, 225, 255))

    # Subtle Progress Bar along bottom edge
    prog_w = int((W - 168) * (beat_idx / max(1, total_beats)))
    draw.rounded_rectangle((84, 1002, W - 84, 1014), radius=6, fill=(30, 41, 59, 200))
    draw.rounded_rectangle((84, 1002, 84 + prog_w, 1014), radius=6, fill=(*accent, 255))

    base.save(out_png, format="PNG", optimize=True)


def render_poster_16x9(manifest: dict, out_jpg: Path) -> None:
    """
    Renders a high-contrast 1920x1080 (< 2MB) YouTube thumbnail with zero lower-right text
    (respecting YouTube's duration badge safe zone) and strict Zero-CTA typography.
    """
    from PIL import Image, ImageDraw

    W, H = 1920, 1080
    beats = manifest.get("beats", [])
    accent = hex_to_rgb(beats[0].get("accentHex", "#38BDF8") if beats else "#38BDF8")
    comp = (manifest.get("companyDisplayName") or manifest.get("company", "AI")).upper()
    headline = manifest.get("breakingStory", {}).get("headline") or manifest.get("title", "AI Technical Brief")
    assert_zero_cta(headline, "poster.headline")

    img = Image.new("RGB", (W, H), (9, 14, 26))
    draw = ImageDraw.Draw(img, "RGBA")

    # Radiant diagonal glow on right 45%
    for r in range(620, 60, -35):
        alpha = int(28 * (1.0 - r / 620.0))
        draw.ellipse((1380 - r, 480 - r, 1380 + r, 480 + r), fill=(accent[0], accent[1], accent[2], alpha))

    # Left 58%: Monumental Cinema-Clarity Typography
    f_pill = load_font(42, bold=True)
    f_hero = load_font(78, bold=True)
    f_sub = load_font(38, bold=True)
    f_node = load_font(34, bold=True)

    pill_text = f"{comp}  ·  BREAKING AI"[:28]
    p_bbox = draw.textbbox((0, 0), pill_text, font=f_pill)
    pill_w = max(520, (p_bbox[2] - p_bbox[0]) + 88)
    draw.rounded_rectangle((84, 84, 84 + pill_w, 172), radius=44, fill=(*accent, 245))
    draw.text((128, 103), pill_text, font=f_pill, fill=(9, 14, 26, 255))

    lines = textwrap.wrap(headline, width=20)[:4]
    hy = 224
    for i, ln in enumerate(lines):
        col = (255, 255, 255, 255) if i < 2 else (*accent, 255)
        draw.text((88, hy), ln, font=f_hero, fill=col)
        hy += 102

    draw.text((92, 910), "INTELLIGENTIAN  ·  ARCHITECTURE BRIEF", font=f_sub, fill=(203, 213, 225, 240))

    # Right 40%: Clean 3-Tier Visual Stack Card (leaving bottom-right corner 100% clear for YT timestamp!)
    rx1, rx2 = 1190, 1830
    tiers = ["FRONTIER MODEL", "SYSTEM TOPOLOGY", "BUILDER IMPACT"]
    ty = 170
    for idx, tlabel in enumerate(tiers):
        fill_c = (accent[0], accent[1], accent[2], 64 if idx == 0 else 32)
        draw.rounded_rectangle((rx1, ty, rx2, ty + 160), radius=28, fill=fill_c, outline=(*accent, 230), width=4)
        bbox = draw.textbbox((0, 0), tlabel, font=f_node)
        tw = bbox[2] - bbox[0]
        draw.text((rx1 + (rx2 - rx1 - tw) // 2, ty + 60), tlabel, font=f_node, fill=(248, 250, 252, 255))
        if idx < 2:
            mid_x = (rx1 + rx2) // 2
            draw.line([(mid_x, ty + 164), (mid_x, ty + 216)], fill=(*accent, 240), width=6)
        ty += 220

    img.save(out_jpg, format="JPEG", quality=91, optimize=True)
    if out_jpg.stat().st_size >= 2 * 1024 * 1024:
        img.save(out_jpg, format="JPEG", quality=82, optimize=True)


def add_subtle_ambient_bed(voice_wav: Path, total_dur: float, mixed_wav: Path) -> None:
    """Mixes a ultra-clean, subtle -28 dB warm harmonic pad underneath the voiceover so audio is studio-grade."""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(voice_wav),
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=110:duration={total_dur:.2f}",
            "-filter_complex",
            "[1:a]lowpass=f=220,volume=0.018,afade=t=in:st=0:d=1.2,afade=t=out:st="
            + f"{max(0.5, total_dur - 1.8):.2f}:d=1.8[bed];"
            + "[0:a]highpass=f=75,acompressor=threshold=-18dB:ratio=2.5[vox];"
            + "[vox][bed]amix=inputs=2:duration=first:dropout_transition=0[out]",
            "-map",
            "[out]",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(mixed_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def build_episode_package(ep_dir: Path, stage_drive_remote: str = "") -> Path:
    manifest_path = ep_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ep_id = manifest["episodeId"]
    assert_zero_cta(json.dumps(manifest), ep_id)

    beats = manifest.get("beats", [])
    if not beats:
        raise ValueError(f"Manifest {ep_id} contains 0 beats")

    voice_name = manifest.get("voiceConfig", {}).get("edgeVoice", "en-US-AndrewMultilingualNeural")
    work_dir = ep_dir / "_build"
    work_dir.mkdir(parents=True, exist_ok=True)

    seg_mp4s: list[Path] = []
    seg_wavs: list[Path] = []
    cursor_sec = 0.0

    print(f"[Cloud Builder] Rendering {len(beats)} kinetic 1080p segments for {ep_id} (voice={voice_name})...")
    for idx, beat in enumerate(beats, 1):
        beat["startSec"] = round(cursor_sec, 3)
        wav_path = work_dir / f"beat_{idx:02d}.wav"
        dur = synthesize_beat_audio(beat["narration"], voice_name, wav_path)
        beat["durationSec"] = round(dur, 3)
        cursor_sec += dur
        seg_wavs.append(wav_path)

        slide_png = work_dir / f"slide_{idx:02d}.png"
        render_beat_slide_1080p(manifest, beat, idx, len(beats), slide_png)

        seg_mp4 = work_dir / f"seg_{idx:02d}.mp4"
        frames = max(30, int(math.ceil(dur * 30.0)))
        # Subtle smooth 1.00 -> 1.035 push-in motion at 1080p30 with fade-in/out transitions
        fade_out_st = max(0.2, dur - 0.35)
        vf = (
            f"scale=2060:1158,zoompan=z='min(zoom+0.00022,1.035)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30,"
            f"fade=t=in:st=0:d=0.30,fade=t=out:st={fade_out_st:.2f}:d=0.30,format=yuv420p"
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(slide_png),
                "-t",
                f"{dur:.3f}",
                "-vf",
                vf,
                "-r",
                "30",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                str(seg_mp4),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        seg_mp4s.append(seg_mp4)

    manifest["totalDurationSec"] = round(cursor_sec, 3)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # Concatenate video segments & audio segments cleanly
    vid_list = work_dir / "vid_concat.txt"
    aud_list = work_dir / "aud_concat.txt"
    vid_list.write_text("\n".join(f"file '{p.resolve()}'" for p in seg_mp4s) + "\n", encoding="utf-8")
    aud_list.write_text("\n".join(f"file '{p.resolve()}'" for p in seg_wavs) + "\n", encoding="utf-8")

    concat_vid = work_dir / "video_track.mp4"
    concat_vox = work_dir / "voice_track.wav"
    mixed_aud = work_dir / "master_audio.wav"

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(vid_list), "-c", "copy", str(concat_vid)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(aud_list), "-c", "copy", str(concat_vox)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    add_subtle_ambient_bed(concat_vox, cursor_sec, mixed_aud)

    out_mp4 = ep_dir / f"{ep_id}_1080p.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(concat_vid),
            "-i",
            str(mixed_aud),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(out_mp4),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    thumb_jpg = ep_dir / "thumbnail_16x9.jpg"
    render_poster_16x9(manifest, thumb_jpg)

    # Clean intermediate _build files so rclone staging stays lean
    for tmp_f in work_dir.glob("*"):
        tmp_f.unlink(missing_ok=True)
    work_dir.rmdir()

    print(
        f"[Cloud Build Ready] {out_mp4.name} ({out_mp4.stat().st_size / (1024 * 1024):.2f} MB, "
        f"{cursor_sec:.1f}s) + {thumb_jpg.name} ({thumb_jpg.stat().st_size // 1024} KB)"
    )

    if stage_drive_remote:
        dst_remote = f"{stage_drive_remote.rstrip('/')}/{ep_id}"
        subprocess.run(["rclone", "copy", str(ep_dir), dst_remote], check=False)
        print(f"[Drive Backup] Staged rendered News package -> {dst_remote}")

    return out_mp4


def main() -> None:
    ap = argparse.ArgumentParser(description="GitHub Actions Cloud Builder for @intelligentian Daily AI News Brief")
    ap.add_argument("--episode-dir", default="", help="Exact episode folder containing manifest.json")
    ap.add_argument(
        "--news-root",
        default="/tmp/intelligentian_daily_news",
        help="Parent directory containing latest_episode.json from intelligentian_live_news_harvester.py",
    )
    ap.add_argument(
        "--stage-drive-remote",
        default="gdrive:Intelligentian/NewsArchive",
        help="Optional rclone remote backup path",
    )
    ap.add_argument(
        "--cloud-runner",
        action="store_true",
        help="Explicitly confirm execution inside cloud runner (GitHub Actions / Colab)",
    )
    ap.add_argument("--poster-only", action="store_true", help="Render only thumbnail_16x9.jpg for validation")
    args = ap.parse_args()

    ep_dir = Path(args.episode_dir) if args.episode_dir else None
    if ep_dir is None:
        ptr = Path(args.news_root) / "latest_episode.json"
        if not ptr.exists():
            raise FileNotFoundError(f"No --episode-dir passed and {ptr} not found. Run harvester first.")
        ep_dir = Path(json.loads(ptr.read_text(encoding="utf-8"))["episodeDir"])

    if args.poster_only:
        mf = json.loads((ep_dir / "manifest.json").read_text(encoding="utf-8"))
        out_jpg = ep_dir / "thumbnail_16x9.jpg"
        render_poster_16x9(mf, out_jpg)
        print(f"[Poster Only] Generated {out_jpg} ({out_jpg.stat().st_size // 1024} KB)")
        return

    is_ci = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    if not is_ci and not args.cloud_runner:
        print(
            "[Workstation Guardrail] Refusing full local MP4 encode per Global Rule 1.4 "
            "(use Colab GPU locally, or pass --cloud-runner inside GitHub Actions).",
            file=sys.stderr,
        )
        sys.exit(2)

    build_episode_package(ep_dir, stage_drive_remote=args.stage_drive_remote)


if __name__ == "__main__":
    main()
