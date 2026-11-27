#!/usr/bin/env python3
"""
Autonomous Cloud Daily Interactive News Video & 16:9 Poster Builder for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`)

Designed strictly for **GitHub Actions Cloud Execution** (`.github/workflows/intelligentian-daily-auto.yml`)
so `@intelligentian` autonomously fetches breaking AI news, synthesizes expressive **Interactive NotebookLM
Male/Female Co-Host (`Maya=Aoede`, `Alex=Puck`) + Simulated Live Audience Call-In (`Leda` / `Fenrir` / `Charon` / `Callirrhoe`)**
speech via **`gemini-3.8-flash-tts`** (`POST https://generativelanguage.googleapis.com/v1beta/interactions`),
renders kinetic 1080p architecture & live viewer Q&A slides + custom `< 2MB` 16:9 thumbnail, and publishes live!

Resilience & Guardrails:
  - Primary TTS: `gemini-3.8-flash-tts` -> automatic HTTP 429 fallback to `gemini-3.8-flash-lite-tts` ->
    automatic fallback to `edge-tts` / `gTTS` if `GEMINI_API_KEY` is missing.
  - Prepends a crisp incoming broadcast call-in chime on `AUDIENCE_Q` beats.
  - Visual Compositor displays **"MAYA & ALEX · AI BRIEFING DESK"** on `COHOST_DUO` beats and a glassmorphic
    **"LIVE VIEWER CALL-IN · <Name> (<Role>)"** question card on `AUDIENCE_Q` beats.
  - Refuses to run full FFmpeg video encoding on the local workstation unless `GITHUB_ACTIONS=true` or
    `--cloud-runner` is explicitly passed (per Global Core Rule 1.4: zero local master renders).
  - Enforces strict `assert_zero_cta` across all rendered text, narration, and poster typography.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import math
import os
import re
import subprocess
import sys
import textwrap
import time
import urllib.error
import urllib.request
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCjVbL7GE3cHLOWRYAxZH65A"

GEMINI_INTERACTIONS_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
GEMINI_TTS_PRIMARY = "gemini-3.8-flash-tts"
GEMINI_TTS_FALLBACK = "gemini-3.8-flash-lite-tts"

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


def resolve_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    repo_env = Path(__file__).resolve().parent.parent / ".env"
    if repo_env.exists():
        for ln in repo_env.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = ln.strip()
            if s.startswith("GEMINI_API_KEY="):
                return s.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def assert_zero_cta(text: str, ctx: str) -> None:
    low = (text or "").lower()
    for w in BANNED_CTA_WORDS:
        if w in low:
            raise ValueError(f"STRICT ZERO-CTA VIOLATION in {ctx}: found '{w}'")


def strip_inline_tts_tags(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", " ", text or "")
    cleaned = re.sub(r"\|[^|]+\|", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


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


def _call_gemini_tts_interaction(
    api_key: str,
    model_name: str,
    content_parts: list[dict],
    speech_config: dict | list,
) -> tuple[bytes | None, int]:
    """
    Calls `POST https://generativelanguage.googleapis.com/v1beta/interactions` with `x-goog-api-key`
    and returns `(decoded_wav_bytes, http_status)`.
    """
    payload = {
        "model": model_name,
        "store": False,
        "input": [
            {
                "type": "user_input",
                "content": content_parts,
            }
        ],
        "response_format": {
            "type": "audio",
        },
        "generation_config": {
            "speech_config": speech_config,
        },
    }
    req = urllib.request.Request(
        GEMINI_INTERACTIONS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
            "Api-Revision": "2026-05-20",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as hexc:
        err_preview = hexc.read().decode("utf-8", errors="ignore")[:240]
        print(f"[Gemini TTS {model_name}] HTTP {hexc.code}: {err_preview}")
        return None, hexc.code
    except Exception as exc:
        print(f"[Gemini TTS {model_name}] Network/parse error: {exc}")
        return None, 0

    audio_b64 = ""
    for step in body.get("steps", []):
        if step.get("type") == "model_output":
            for part in step.get("content", []):
                if part.get("type") == "audio" and part.get("data"):
                    audio_b64 = part["data"]
    if not audio_b64 and isinstance(body.get("output_audio"), dict):
        audio_b64 = body["output_audio"].get("data", "")

    if not audio_b64:
        return None, 200
    return base64.b64decode(audio_b64), 200


def _synthesize_gemini_beat_raw_wav(api_key: str, beat: dict, raw_wav: Path) -> bool:
    speaker_role = beat.get("speakerRole", "COHOST_DUO")
    turns = beat.get("dialogueTurns") or []

    if speaker_role == "AUDIENCE_Q":
        caller = beat.get("audienceCaller") or {}
        voice_name = str(
            (turns[0].get("voice") if turns else None)
            or caller.get("voice")
            or "Fenrir"
        )
        style_hint = str(
            (turns[0].get("style") if turns else None)
            or "curious, engaged tech viewer calling in live"
        )
        txt = str((turns[0].get("text") if turns else None) or beat.get("narration", "")).strip()
        assert_zero_cta(txt, f"tts_audience:{raw_wav.name}")
        content_parts = [
            {
                "type": "text",
                "text": txt,
                "annotations": [
                    {
                        "type": "speech_metadata",
                        "style": style_hint,
                    }
                ],
            }
        ]
        speech_cfg: dict | list = [{"voice": voice_name}]
    else:
        if not turns:
            txt = beat.get("narration", "")
            turns = [
                {
                    "speaker": "Maya",
                    "voice": "Aoede",
                    "style": "curious, energetic co-host",
                    "text": txt,
                }
            ]
        # Multi-speaker (`Maya=Aoede`, `Alex=Puck`) when >=2 distinct speakers; single-speaker if 1
        unique_speakers: list[tuple[str, str]] = []
        seen_sp: set[str] = set()
        content_parts = []
        for t in turns:
            sp = "Maya" if str(t.get("speaker", "Maya")).lower().startswith("maya") else "Alex"
            vc = "Aoede" if sp == "Maya" else "Puck"
            st = str(t.get("style") or ("curious, energetic co-host" if sp == "Maya" else "sharp AI systems architect"))
            tx = str(t.get("text") or "").strip()
            if not tx:
                continue
            assert_zero_cta(tx, f"tts_duo:{raw_wav.name}:{sp}")
            if sp not in seen_sp:
                seen_sp.add(sp)
                unique_speakers.append((sp, vc))
            meta_ann: dict = {"type": "speech_metadata", "style": st}
            if len(turns) >= 2:
                meta_ann["speaker"] = sp
            content_parts.append(
                {
                    "type": "text",
                    "text": tx,
                    "annotations": [meta_ann],
                }
            )

        if len(unique_speakers) >= 2:
            speech_cfg = {
                "speakers": [{"speaker": sp, "voice": vc} for sp, vc in unique_speakers[:2]]
            }
        else:
            only_sp, only_vc = unique_speakers[0] if unique_speakers else ("Maya", "Aoede")
            # Remove `speaker` annotation on single-speaker call
            for cp in content_parts:
                for ann in cp.get("annotations", []):
                    ann.pop("speaker", None)
            speech_cfg = [{"voice": only_vc}]

    models_to_try = [GEMINI_TTS_PRIMARY, GEMINI_TTS_FALLBACK]
    for m_idx, model_id in enumerate(models_to_try):
        wav_bytes, status_code = _call_gemini_tts_interaction(api_key, model_id, content_parts, speech_cfg)
        if wav_bytes and len(wav_bytes) > 512:
            raw_wav.write_bytes(wav_bytes)
            return True
        if status_code == 429 and m_idx == 0:
            print(f"[Gemini TTS Quota/429] Switching {raw_wav.name} -> {GEMINI_TTS_FALLBACK}")
            time.sleep(1.2)
            continue
        if status_code not in (429, 500, 503) and m_idx == 0:
            # Also try lite fallback once on unexpected transient errors
            continue
    return False


def _prepend_call_in_chime(voice_wav: Path, out_wav: Path) -> None:
    """
    Prepends a crisp two-note studio broadcast call-in chime (587Hz D5 -> 880Hz A5, ~0.34s)
    before a `LIVE VIEWER CALL-IN` (`AUDIENCE_Q`) voice clip, normalized to 48kHz stereo WAV.
    """
    chime_wav = out_wav.with_suffix(".chime.wav")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=587.33:duration=0.14",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=880.0:duration=0.22",
            "-filter_complex",
            "[0:a]volume=0.14,afade=t=in:st=0:d=0.02,afade=t=out:st=0.10:d=0.04[c1];"
            "[1:a]volume=0.16,afade=t=in:st=0:d=0.02,afade=t=out:st=0.12:d=0.10,apad=pad_dur=0.12[c2];"
            "[c1][c2]concat=n=2:v=0:a=1,aformat=sample_rates=48000:channel_layouts=stereo[ch]",
            "-map",
            "[ch]",
            str(chime_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    norm_vox = out_wav.with_suffix(".vox48.wav")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(voice_wav),
            "-af",
            "apad=pad_dur=0.42",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(norm_vox),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    concat_list = out_wav.with_suffix(".chime_concat.txt")
    concat_list.write_text(
        f"file '{chime_wav.resolve()}'\nfile '{norm_vox.resolve()}'\n",
        encoding="utf-8",
    )
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(out_wav)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    chime_wav.unlink(missing_ok=True)
    norm_vox.unlink(missing_ok=True)
    concat_list.unlink(missing_ok=True)


def synthesize_beat_audio(
    beat: dict,
    fallback_male_edge: str,
    fallback_female_edge: str,
    out_wav: Path,
    api_key: str = "",
) -> float:
    """
    Synthesizes beat speech via:
      1. `gemini-3.8-flash-tts` (multi-speaker `Maya=Aoede, Alex=Puck` on `COHOST_DUO`,
         single-speaker `Leda/Fenrir/Charon/Callirrhoe` + incoming call-in chime on `AUDIENCE_Q`)
      2. Automatic 429 fallback to `gemini-3.8-flash-lite-tts`
      3. Automatic fallback to `edge-tts` / `gTTS` when `GEMINI_API_KEY` is unavailable.
    Normalizes to 48kHz stereo WAV and returns exact duration in seconds.
    """
    plain_text = strip_inline_tts_tags(beat.get("narration", ""))
    assert_zero_cta(plain_text, f"tts:{out_wav.name}")
    is_audience = beat.get("speakerRole") == "AUDIENCE_Q"

    raw_gemini_wav = out_wav.with_suffix(".gemini.wav")
    synthesized_raw: Path | None = None

    if api_key and _synthesize_gemini_beat_raw_wav(api_key, beat, raw_gemini_wav):
        synthesized_raw = raw_gemini_wav

    if synthesized_raw is None:
        raw_mp3 = out_wav.with_suffix(".raw.mp3")
        turns = beat.get("dialogueTurns") or []
        try:
            if not is_audience and len(turns) >= 2:
                # Multi-turn edge-tts fallback alternating female (Maya) & male (Alex) neural voices
                turn_mp3s: list[Path] = []
                for t_idx, t in enumerate(turns):
                    t_clean = strip_inline_tts_tags(t.get("text", ""))
                    if not t_clean:
                        continue
                    sp_is_maya = str(t.get("speaker", "")).lower().startswith("maya")
                    ev = fallback_female_edge if sp_is_maya else fallback_male_edge
                    t_mp3 = out_wav.with_suffix(f".t{t_idx}.mp3")
                    asyncio.run(_synthesize_edge_tts(t_clean, ev, t_mp3))
                    if t_mp3.exists() and t_mp3.stat().st_size > 256:
                        turn_mp3s.append(t_mp3)
                if turn_mp3s:
                    t_list = out_wav.with_suffix(".turns.txt")
                    t_list.write_text("\n".join(f"file '{p.resolve()}'" for p in turn_mp3s) + "\n", encoding="utf-8")
                    subprocess.run(
                        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(t_list), "-c", "copy", str(raw_mp3)],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    t_list.unlink(missing_ok=True)
                    for p in turn_mp3s:
                        p.unlink(missing_ok=True)
                    synthesized_raw = raw_mp3
            else:
                caller_voice = str((beat.get("audienceCaller") or {}).get("voice", ""))
                ev = fallback_female_edge if caller_voice in ("Leda", "Callirrhoe") else fallback_male_edge
                asyncio.run(_synthesize_edge_tts(plain_text, ev, raw_mp3))
                if raw_mp3.exists() and raw_mp3.stat().st_size > 512:
                    synthesized_raw = raw_mp3
        except Exception as exc:
            print(f"[TTS Fallback Notice] edge-tts retry/fallback on {out_wav.name}: {exc}")

        if synthesized_raw is None:
            try:
                from gtts import gTTS

                gTTS(text=plain_text, lang="en", slow=False).save(str(raw_mp3))
                if raw_mp3.exists() and raw_mp3.stat().st_size > 512:
                    synthesized_raw = raw_mp3
            except Exception as g_exc:
                print(f"[TTS Fallback] gTTS unavailable ({g_exc}); generating clean studio tone-paced WAV")

    if synthesized_raw is not None:
        if is_audience:
            _prepend_call_in_chime(synthesized_raw, out_wav)
        else:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(synthesized_raw),
                    "-af",
                    "apad=pad_dur=0.42",
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
        synthesized_raw.unlink(missing_ok=True)
    else:
        est_sec = max(7.0, len(plain_text.split()) / 2.5)
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
    Renders a crisp 1920x1080 interactive podcast & architectural briefing slide:
      - `COHOST_DUO` beats feature the **"MAYA & ALEX · AI BRIEFING DESK"** studio header, dual host speaker pills,
        architecture flow diagram nodes, and key engineering bullets.
      - `AUDIENCE_Q` beats feature a vibrant glassmorphic **"LIVE VIEWER CALL-IN · <Name> (<Role>)"** question card,
        waveform pulse bars, and the exact viewer question in cinema-clarity typography!
    """
    from PIL import Image, ImageDraw, ImageEnhance

    W, H = 1920, 1080
    is_audience = beat.get("speakerRole") == "AUDIENCE_Q"
    accent = hex_to_rgb(beat.get("accentHex", "#34D399" if is_audience else "#38BDF8"))
    comp_name = manifest.get("companyDisplayName") or manifest.get("company", "AI")

    base = Image.new("RGB", (W, H), (10, 16, 30))

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

    # Ambient studio glow
    glow_cx = 960 if is_audience else W - 360
    glow_cy = 440 if is_audience else 180
    for r in range(460, 40, -30):
        alpha = int(22 * (1.0 - r / 460.0))
        draw.ellipse((glow_cx - r, glow_cy - r, glow_cx + r, glow_cy + r), fill=(accent[0], accent[1], accent[2], alpha))

    f_badge = load_font(25, bold=True)
    f_stamp = load_font(26, bold=True)
    f_title = load_font(52, bold=True)
    f_node = load_font(25, bold=True)
    f_bullet = load_font(31, bold=False)
    f_quote = load_font(42, bold=True)
    f_caller = load_font(32, bold=True)
    f_caption = load_font(27, bold=False)

    if is_audience:
        caller = beat.get("audienceCaller") or {}
        c_name = caller.get("name", "Viewer")
        c_role = caller.get("roleTitle", "AI Builder")
        banner_label = f"LIVE VIEWER CALL-IN · {c_name} ({c_role})"
        assert_zero_cta(banner_label, "slide.audience_banner")

        # Top Left Live Call-In Pill
        b_bbox = draw.textbbox((0, 0), banner_label[:54], font=f_badge)
        pill_w = min(1160, max(620, (b_bbox[2] - b_bbox[0]) + 96))
        draw.rounded_rectangle((84, 58, 84 + pill_w, 118), radius=30, fill=(accent[0], accent[1], accent[2], 58), outline=(*accent, 235), width=3)
        draw.ellipse((110, 77, 132, 99), fill=(52, 211, 153, 255))
        draw.text((148, 73), banner_label[:54], font=f_badge, fill=(248, 250, 252, 255))

        # Top Right Company Stamp
        punch = f"{comp_name.upper()} · Q&A"[:22]
        draw.rounded_rectangle((W - 460, 58, W - 84, 118), radius=30, fill=(15, 23, 42, 225), outline=(*accent, 200), width=2)
        draw.text((W - 432, 73), punch, font=f_stamp, fill=(*accent, 255))

        # Chapter Title
        ch_title = beat.get("chapterTitle", f"Viewer Question from {c_name}")
        draw.text((88, 148), ch_title[:52], font=f_title, fill=(248, 250, 252, 255))

        # Centerpiece Glassmorphic Live Question Card
        card_x1, card_y1, card_x2, card_y2 = 84, 244, W - 84, 720
        draw.rounded_rectangle(
            (card_x1, card_y1, card_x2, card_y2),
            radius=34,
            fill=(19, 30, 52, 224),
            outline=(*accent, 225),
            width=3,
        )
        # Inner frosted highlight strip
        draw.rounded_rectangle(
            (card_x1 + 28, card_y1 + 26, card_x2 - 28, card_y1 + 104),
            radius=22,
            fill=(accent[0], accent[1], accent[2], 38),
            outline=(*accent, 140),
            width=1,
        )
        draw.text(
            (card_x1 + 56, card_y1 + 46),
            f"INCOMING VOICE QUESTION  ·  {c_name.upper()}  ({c_role})",
            font=f_caller,
            fill=(*accent, 255),
        )

        # Acoustic Call-In Waveform Bars on Right of Header Strip
        bar_heights = [18, 36, 24, 46, 30, 42, 20, 34, 26, 16]
        wx = card_x2 - 260
        for bh in bar_heights:
            wy1 = card_y1 + 65 - bh // 2
            wy2 = card_y1 + 65 + bh // 2
            draw.rounded_rectangle((wx, wy1, wx + 10, wy2), radius=4, fill=(*accent, 235))
            wx += 18

        # Spoken Question Transcript inside Glassmorphic Card
        turns = beat.get("dialogueTurns") or []
        q_raw = strip_inline_tts_tags(turns[0].get("text", "") if turns else caller.get("questionSummary", beat.get("narration", "")))
        q_wrapped = textwrap.wrap(f'"{q_raw}"', width=52)[:4]
        qy = card_y1 + 148
        for ln in q_wrapped:
            draw.text((card_x1 + 60, qy), ln, font=f_quote, fill=(248, 250, 252, 255))
            qy += 64

        # Bottom Context Flow Strip (3 nodes)
        nodes = beat.get("diagramNodes", [])[:4]
        if nodes:
            n_count = len(nodes)
            box_w = min(360, (W - 220 - (n_count - 1) * 40) // max(1, n_count))
            box_h = 92
            total_row_w = n_count * box_w + (n_count - 1) * 40
            sx = (W - total_row_w) // 2
            ry = 758
            for i, nd in enumerate(nodes):
                bx = sx + i * (box_w + 40)
                draw.rounded_rectangle((bx, ry, bx + box_w, ry + box_h), radius=18, fill=(30, 41, 59, 215), outline=(*accent, 175), width=2)
                lbl = str(nd.get("label", ""))[:22]
                bbox = draw.textbbox((0, 0), lbl, font=f_node)
                lw = bbox[2] - bbox[0]
                draw.text((bx + (box_w - lw) // 2, ry + 30), lbl, font=f_node, fill=(241, 245, 249, 255))
                if i < n_count - 1:
                    ax1, ax2, ay = bx + box_w + 6, bx + box_w + 34, ry + box_h // 2
                    draw.line([(ax1, ay), (ax2, ay)], fill=(*accent, 220), width=3)

        cit_text = f"Maya & Alex Respond Next  ·  Live Viewer Call-In ({c_name} · {c_role})  ·  Beat {beat_idx} of {total_beats}"
        draw.rounded_rectangle((84, 885, W - 84, 965), radius=22, fill=(30, 41, 59, 225), outline=(*accent, 150), width=2)
        draw.text((120, 908), cit_text[:98], font=f_caption, fill=(226, 232, 240, 255))

    else:
        # COHOST_DUO: "MAYA & ALEX · AI BRIEFING DESK"
        desk_banner = f"MAYA & ALEX · AI BRIEFING DESK  |  {comp_name.upper()}"
        b_bbox = draw.textbbox((0, 0), desk_banner[:54], font=f_badge)
        pill_w = min(1140, max(660, (b_bbox[2] - b_bbox[0]) + 84))
        draw.rounded_rectangle((84, 58, 84 + pill_w, 118), radius=30, fill=(accent[0], accent[1], accent[2], 46), outline=(*accent, 220), width=2)
        draw.text((116, 73), desk_banner[:54], font=f_badge, fill=(248, 250, 252, 255))

        # Top-right punch metric badge
        punch = str(beat.get("punchMetric") or beat.get("yearStamp") or f"0{beat_idx}/0{total_beats}")
        draw.rounded_rectangle((W - 470, 58, W - 84, 118), radius=30, fill=(15, 23, 42, 225), outline=(*accent, 195), width=2)
        draw.text((W - 442, 72), punch[:22], font=f_stamp, fill=(*accent, 255))

        # Chapter Headline
        ch_title = beat.get("chapterTitle", "Technical Architecture")
        wrapped_title = textwrap.wrap(ch_title, width=42)[:2]
        ty = 144
        for line in wrapped_title:
            draw.text((88, ty), line, font=f_title, fill=(248, 250, 252, 255))
            ty += 62

        # Co-Host Studio Avatar Badges (Maya · Host + Alex · Systems Architect) on Top-Right below punch pill
        draw.rounded_rectangle((W - 610, 144, W - 355, 198), radius=24, fill=(236, 72, 153, 48), outline=(244, 114, 182, 210), width=2)
        draw.text((W - 584, 157), "MAYA · CO-HOST", font=load_font(21, bold=True), fill=(253, 242, 248, 255))
        draw.rounded_rectangle((W - 340, 144, W - 84, 198), radius=24, fill=(56, 189, 248, 48), outline=(56, 189, 248, 210), width=2)
        draw.text((W - 316, 157), "ALEX · ARCHITECT", font=load_font(21, bold=True), fill=(240, 249, 255, 255))

        # Architecture Flow Diagram Nodes Row (Center Canvas)
        nodes = beat.get("diagramNodes", [])[:5]
        if nodes:
            n_count = len(nodes)
            box_w = min(300, (W - 220 - (n_count - 1) * 44) // max(1, n_count))
            box_h = 118
            total_row_w = n_count * box_w + (n_count - 1) * 44
            start_x = (W - total_row_w) // 2
            row_y = 320

            for i, nd in enumerate(nodes):
                bx = start_x + i * (box_w + 44)
                is_core = nd.get("role") == "core"
                fill_c = (accent[0], accent[1], accent[2], 62) if is_core else (30, 41, 59, 215)
                border_c = (*accent, 255) if is_core else (148, 163, 184, 155)
                draw.rounded_rectangle((bx, row_y, bx + box_w, row_y + box_h), radius=20, fill=fill_c, outline=border_c, width=3)

                lbl_lines = textwrap.wrap(str(nd.get("label", "")), width=16)[:2]
                ly = row_y + (38 if len(lbl_lines) == 1 else 24)
                for ln in lbl_lines:
                    bbox = draw.textbbox((0, 0), ln, font=f_node)
                    lw = bbox[2] - bbox[0]
                    draw.text((bx + (box_w - lw) // 2, ly), ln, font=f_node, fill=(248, 250, 252, 255))
                    ly += 34

                if i < n_count - 1:
                    ax1 = bx + box_w + 6
                    ax2 = bx + box_w + 38
                    ay = row_y + box_h // 2
                    draw.line([(ax1, ay), (ax2, ay)], fill=(*accent, 235), width=4)
                    draw.polygon([(ax2, ay), (ax2 - 12, ay - 8), (ax2 - 12, ay + 8)], fill=(*accent, 235))

        # Key Engineering Bullets + Dialogue Highlights Card
        bullets = beat.get("keyBullets", [])[:3]
        card_y = 492
        draw.rounded_rectangle((84, card_y, W - 84, card_y + 345), radius=26, fill=(15, 23, 42, 214), outline=(71, 85, 105, 165), width=2)
        by = card_y + 38
        for btxt in bullets:
            clean_b = textwrap.shorten(str(btxt), width=92, placeholder="...")
            draw.ellipse((118, by + 10, 136, by + 28), fill=(*accent, 255))
            draw.text((158, by), clean_b, font=f_bullet, fill=(226, 232, 240, 255))
            by += 96

        cit = beat.get("citation", {})
        cit_text = f"Maya & Alex · AI Briefing Desk  |  Source: {cit.get('sourceName', comp_name)}  ·  Beat {beat_idx} of {total_beats}"
        draw.rounded_rectangle((84, 885, W - 84, 965), radius=22, fill=(30, 41, 59, 225), outline=(*accent, 135), width=2)
        draw.text((120, 908), cit_text[:98], font=f_caption, fill=(203, 213, 225, 255))

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

    for r in range(620, 60, -35):
        alpha = int(28 * (1.0 - r / 620.0))
        draw.ellipse((1380 - r, 480 - r, 1380 + r, 480 + r), fill=(accent[0], accent[1], accent[2], alpha))

    f_pill = load_font(40, bold=True)
    f_hero = load_font(76, bold=True)
    f_sub = load_font(36, bold=True)
    f_node = load_font(32, bold=True)

    pill_text = f"{comp}  ·  BREAKING AI"[:28]
    p_bbox = draw.textbbox((0, 0), pill_text, font=f_pill)
    pill_w = max(520, (p_bbox[2] - p_bbox[0]) + 88)
    draw.rounded_rectangle((84, 84, 84 + pill_w, 172), radius=44, fill=(*accent, 245))
    draw.text((128, 104), pill_text, font=f_pill, fill=(9, 14, 26, 255))

    lines = textwrap.wrap(headline, width=20)[:4]
    hy = 224
    for i, ln in enumerate(lines):
        col = (255, 255, 255, 255) if i < 2 else (*accent, 255)
        draw.text((88, hy), ln, font=f_hero, fill=col)
        hy += 100

    draw.text((92, 910), "MAYA & ALEX  ·  AI BRIEFING + LIVE Q&A", font=f_sub, fill=(203, 213, 225, 245))

    # Right 40%: Clean 3-Tier Visual Stack Card (leaving bottom-right corner 100% clear for YT timestamp!)
    rx1, rx2 = 1190, 1830
    tiers = ["MAYA & ALEX DESK", "STACK TOPOLOGY", "2 LIVE CALLER Q&As"]
    ty = 170
    for idx, tlabel in enumerate(tiers):
        fill_c = (accent[0], accent[1], accent[2], 68 if idx == 0 else 34)
        draw.rounded_rectangle((rx1, ty, rx2, ty + 160), radius=28, fill=fill_c, outline=(*accent, 230), width=4)
        bbox = draw.textbbox((0, 0), tlabel, font=f_node)
        tw = bbox[2] - bbox[0]
        draw.text((rx1 + (rx2 - rx1 - tw) // 2, ty + 62), tlabel, font=f_node, fill=(248, 250, 252, 255))
        if idx < 2:
            mid_x = (rx1 + rx2) // 2
            draw.line([(mid_x, ty + 164), (mid_x, ty + 216)], fill=(*accent, 240), width=6)
        ty += 220

    img.save(out_jpg, format="JPEG", quality=91, optimize=True)
    if out_jpg.stat().st_size >= 2 * 1024 * 1024:
        img.save(out_jpg, format="JPEG", quality=82, optimize=True)


def add_subtle_ambient_bed(voice_wav: Path, total_dur: float, mixed_wav: Path) -> None:
    """Mixes an ultra-clean, subtle -28 dB warm harmonic pad underneath the podcast voices so audio is broadcast-grade."""
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
            "[1:a]lowpass=f=220,volume=0.016,afade=t=in:st=0:d=1.2,afade=t=out:st="
            + f"{max(0.5, total_dur - 1.8):.2f}:d=1.8[bed];"
            + "[0:a]highpass=f=75,acompressor=threshold=-18dB:ratio=2.4[vox];"
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

    vc_cfg = manifest.get("voiceConfig", {})
    male_edge = vc_cfg.get("edgeVoice", "en-US-AndrewMultilingualNeural")
    female_edge = vc_cfg.get("femaleEdgeVoice", "en-US-AvaMultilingualNeural")
    api_key = resolve_gemini_api_key()

    work_dir = ep_dir / "_build"
    work_dir.mkdir(parents=True, exist_ok=True)

    seg_mp4s: list[Path] = []
    seg_wavs: list[Path] = []
    cursor_sec = 0.0

    tts_label = f"{GEMINI_TTS_PRIMARY} (Maya=Aoede, Alex=Puck + Live Callers)" if api_key else f"edge-tts fallback ({female_edge}/{male_edge})"
    print(f"[Cloud Builder] Rendering {len(beats)} interactive 1080p segments for {ep_id} [{tts_label}]...")

    for idx, beat in enumerate(beats, 1):
        beat["startSec"] = round(cursor_sec, 3)
        wav_path = work_dir / f"beat_{idx:02d}.wav"
        dur = synthesize_beat_audio(beat, male_edge, female_edge, wav_path, api_key=api_key)
        beat["durationSec"] = round(dur, 3)
        cursor_sec += dur
        seg_wavs.append(wav_path)

        slide_png = work_dir / f"slide_{idx:02d}.png"
        render_beat_slide_1080p(manifest, beat, idx, len(beats), slide_png)

        seg_mp4 = work_dir / f"seg_{idx:02d}.mp4"
        frames = max(30, int(math.ceil(dur * 30.0)))
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
    ap = argparse.ArgumentParser(description="GitHub Actions Cloud Builder for @intelligentian Interactive Daily AI News Show")
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
    ap.add_argument("--poster-only", action="store_true", help="Render only thumbnail_16x9.jpg + slide previews without FFmpeg video encode")
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
        preview_dir = ep_dir / "_slide_previews"
        preview_dir.mkdir(parents=True, exist_ok=True)
        beats = mf.get("beats", [])
        for idx, beat in enumerate(beats, 1):
            render_beat_slide_1080p(mf, beat, idx, len(beats), preview_dir / f"slide_{idx:02d}.png")
        print(f"[Poster & Slide Previews] Generated {out_jpg} ({out_jpg.stat().st_size // 1024} KB) + {len(beats)} slides in {preview_dir}")
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
