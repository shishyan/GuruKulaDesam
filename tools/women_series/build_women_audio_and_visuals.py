#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools/women_series/build_women_audio_and_visuals.py
================================================================================================
Stage 2 (Audio + Studio Cues + 30fps RTA Spectrum) & Stage 3 (Zero-Video-Credit nano-pro 16:9
Storyboards + v2 Movie-Poster Thumbnails + Visual QA Contact Sheets) for the 3 Women's Series Pilots.

Voice: ElevenLabs `GuruKulaDesam` (`Mu63hpI1uigjGMdYVTDr`) @ 0.86x rubberband formant-preserved
       using key provided by user (`ELEVENLABS_KEY` env or explicit arg).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import threading
import time
import urllib.request
import wave
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter1d

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from women_3pillars_catalog import EPISODES, SCENE_STYLE_PREFIX, validate_catalog  # noqa: E402

VOICE_ID = "Mu63hpI1uigjGMdYVTDr"  # GuruKulaDesam custom Tamil voice
TEMPO = 0.86

ASSETS_TDL = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life")
OUT_ROOT = ASSETS_TDL / "women_series_pilots"
STUDIO_PUB = Path("/home/shishyan/GitHub/tamil-lyric-studio/public")

INTRO_CUE = ASSETS_TDL / "Intro.wav"
INTER_CUE = ASSETS_TDL / "Interlude.wav"
OUTRO_CUE = ASSETS_TDL / "Outro.wav"
BG_CUE = ASSETS_TDL / "Background.wav"


def dur_of(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(path),
            ],
            text=True,
        ).strip()
    )


def synth_gurukuladesam_voice(text: str, out_wav: Path, api_key: str) -> None:
    raw_mp3 = out_wav.with_suffix(".raw.mp3")
    payload = json.dumps(
        {
            "text": text.strip(),
            "model_id": "eleven_v4",
            "voice_settings": {
                "stability": 0.52,
                "similarity_boost": 0.86,
                "style": 0.20,
                "use_speaker_boost": True,
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_192",
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                raw_mp3.write_bytes(resp.read())
            break
        except Exception as exc:
            if attempt == 3:
                raise
            print(f"  [ElevenLabs retry {attempt+1}] {exc}")
            time.sleep(3)

    subprocess.run(
        [
            "ffmpeg", "-nostdin", "-y", "-i", str(raw_mp3),
            "-af", (
                f"rubberband=tempo={TEMPO}:formant=preserved,"
                "highpass=f=85,equalizer=f=240:t=q:w=1.2:g=-2.0,"
                "equalizer=f=2800:t=q:w=1.1:g=2.4,equalizer=f=4200:t=q:w=1.0:g=3.4,"
                "treble=g=2.5:f=7200,acompressor=threshold=-21dB:ratio=3.0:attack=6:release=110:makeup=4.2dB,"
                "aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=8"
            ),
            "-c:a", "pcm_s16le", str(out_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    raw_mp3.unlink(missing_ok=True)


def extract_spectrum_bin(wav_path: Path, out_bin: Path) -> int:
    FPS, N_BINS, WAVE_PTS, VOC_WAVE_PTS = 30, 64, 96, 16
    data, sr = sf.read(str(wav_path), dtype="float32", always_2d=True)
    mono = librosa.resample(data.mean(axis=1), orig_sr=sr, target_sr=22050)
    n_frames = int(np.floor(len(mono) / 22050 * FPS))
    hop = int(round(22050 / FPS))

    inst_mel = librosa.feature.melspectrogram(y=mono, sr=22050, n_fft=2048, hop_length=hop, n_mels=N_BINS, fmin=28, fmax=11000, power=1.5)
    voc_mel = librosa.feature.melspectrogram(y=mono, sr=22050, n_fft=2048, hop_length=hop, n_mels=N_BINS, fmin=120, fmax=8500, power=1.5)
    inst_norm = np.clip((librosa.power_to_db(inst_mel, ref=np.max, top_db=65.0)[:, :n_frames] + 65.0) / 65.0, 0, 1)
    voc_norm = np.clip((librosa.power_to_db(voc_mel, ref=np.max, top_db=60.0)[:, :n_frames] + 60.0) / 60.0, 0, 1)
    inst_uint8 = (gaussian_filter1d(inst_norm, sigma=0.65, axis=1) * 255.0).astype(np.uint8)
    voc_uint8 = (gaussian_filter1d(voc_norm, sigma=0.65, axis=1) * 255.0).astype(np.uint8)

    out_bin.parent.mkdir(parents=True, exist_ok=True)
    with open(out_bin, "wb") as bf:
        bf.write(struct.pack("<4sIII", b"SPEC", n_frames, N_BINS, WAVE_PTS))
        for f in range(n_frames):
            s_start, s_end = f * hop, min(len(mono), (f + 1) * hop)
            frame_mix = mono[s_start:s_end]
            if len(frame_mix) > 0:
                mix_wave = (np.clip(np.interp(np.linspace(0, len(frame_mix) - 1, WAVE_PTS), np.arange(len(frame_mix)), frame_mix) * 1.45, -1, 1) * 127).astype(np.int8)
                voc_wave = (np.clip(np.interp(np.linspace(0, len(frame_mix) - 1, VOC_WAVE_PTS), np.arange(len(frame_mix)), frame_mix) * 1.55, -1, 1) * 127).astype(np.int8)
            else:
                mix_wave = np.zeros(WAVE_PTS, dtype=np.int8)
                voc_wave = np.zeros(VOC_WAVE_PTS, dtype=np.int8)
            bass = int(np.clip(inst_norm[:8, f].mean() * 1.25, 0, 1) * 255)
            voc_env = int(np.clip(voc_norm[8:36, f].mean() * 1.35, 0, 1) * 255)
            high = int(np.clip(inst_norm[40:, f].mean() * 1.2, 0, 1) * 255)
            beat = int(np.clip(bass * 0.65 + high * 0.35, 0, 255))
            bf.write(inst_uint8[:, f].tobytes())
            bf.write(voc_uint8[:, f].tobytes())
            bf.write(mix_wave.tobytes())
            bf.write(voc_wave.tobytes())
            bf.write(struct.pack("<BBBB", beat, bass, voc_env, high))
    return n_frames


def split_clauses_two_lines(sentence: str) -> tuple[str, str]:
    words = sentence.strip().split()
    if len(words) <= 5:
        return sentence.strip(), ""
    mid = len(words) // 2
    best_i = mid
    for delta in range(0, max(3, len(words) // 3)):
        for cand in [mid - delta, mid + delta]:
            if 2 <= cand < len(words) - 1 and words[cand - 1].endswith((",", ";", "—")):
                best_i = cand
                break
        else:
            continue
        break
    return " ".join(words[:best_i]), " ".join(words[best_i:])


def map_sentences_rms_fallback(stem_wav: Path, master_offset: float, paras: list[str], badge: str, is_story: bool) -> list[dict]:
    with wave.open(str(stem_wav), "rb") as w:
        sr = w.getframerate()
        nch = w.getnchannels()
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32).reshape(-1, nch).mean(axis=1) / 32768.0
    dur = len(x) / sr
    hop, win = int(0.02 * sr), int(0.06 * sr)
    rms = np.array([np.sqrt(np.mean(x[i : i + win] ** 2)) for i in range(0, max(1, len(x) - win), hop)])

    sents = []
    for p in paras:
        for s in re.split(r"(?<=[.!?])\s+", p.strip()):
            if s.strip():
                sents.append(s.strip())

    merged = []
    idx = 0
    while idx < len(sents):
        if len(sents[idx]) < 18 and idx + 1 < len(sents):
            merged.append(sents[idx] + " " + sents[idx + 1])
            idx += 2
        elif len(sents[idx]) < 15 and merged:
            merged[-1] = merged[-1] + " " + sents[idx]
            idx += 1
        else:
            merged.append(sents[idx])
            idx += 1
    sents = merged

    total_chars = max(1, sum(len(s) for s in sents))
    boundaries = [0.08]
    cum = 0
    for s in sents[:-1]:
        cum += len(s)
        est_t = (cum / total_chars) * dur
        lo = max(boundaries[-1] + 1.2, est_t - 1.4)
        hi = min(dur - 1.2, est_t + 1.4)
        if hi > lo:
            i_lo, i_hi = int(lo / 0.02), min(len(rms), int(hi / 0.02))
            best_t = (i_lo + int(np.argmin(rms[i_lo:i_hi]))) * 0.02 if i_hi > i_lo else est_t
        else:
            best_t = est_t
        boundaries.append(round(best_t, 2))
    boundaries.append(round(dur - 0.08, 2))

    out = []
    for i, s in enumerate(sents):
        l1, l2 = split_clauses_two_lines(s)
        out.append(
            {
                "startSec": round(master_offset + boundaries[i], 2),
                "endSec": round(master_offset + boundaries[i + 1] - 0.06, 2),
                "badge": badge,
                "isDialogue": bool(is_story and (i % 2 == 1 or "!" in s)),
                "line1": l1,
                "line2": l2,
                "writtenSentence": s,
            }
        )
    return out


def build_audio_all(api_key: str) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    shared_work = Path("/tmp/women_series_cues")
    shared_work.mkdir(parents=True, exist_ok=True)

    intro_6s = shared_work / "cue_intro.wav"
    inter_a = shared_work / "cue_inter_a.wav"
    inter_b = shared_work / "cue_inter_b.wav"
    outro_12s = shared_work / "cue_outro.wav"
    bg_unit = shared_work / "bg_unit.wav"

    subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(INTRO_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=0:6.2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.4,afade=t=out:st=4.6:d=1.6,loudnorm=I=-20:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(intro_6s)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(INTER_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=0:5.2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.5,afade=t=out:st=3.8:d=1.4,loudnorm=I=-21:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(inter_a)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(INTER_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=2.0:7.2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.6,afade=t=out:st=3.8:d=1.4,loudnorm=I=-21:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(inter_b)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(OUTRO_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=90.0:103.5,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.2,afade=t=out:st=10.0:d=3.5,loudnorm=I=-19:TP=-2.0:LRA=9", "-c:a", "pcm_s16le", str(outro_12s)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(BG_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-18:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(bg_unit)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    for ep in EPISODES:
        slug = ep["slug"]
        ep_id = ep["id"]
        ep_dir = OUT_ROOT / slug
        ep_dir.mkdir(parents=True, exist_ok=True)
        work = Path(f"/tmp/women_series_{ep_id}")
        work.mkdir(parents=True, exist_ok=True)

        # Save canonical markdown script
        md_lines = [f"# {ep['title_pill']}\n", f"> {ep['pillar']}\n"]
        for sec in ep["sections"]:
            md_lines.append(f"\n## {sec['badge']}\n")
            for p in sec["paragraphs"]:
                md_lines.append(p + "\n")
        (ep_dir / f"{slug}_Script.md").write_text("\n".join(md_lines), encoding="utf-8")
        (ep_dir / f"{slug}_Description.txt").write_text(ep["yt_description"], encoding="utf-8")

        print(f"\n=== Synthesizing GuruKulaDesam Voice for {slug} ===")
        vo_paths = []
        voiced_with_bg = []
        bg_offsets = [0.0, 12.0, 24.0, 6.0, 18.0]

        for idx, sec in enumerate(ep["sections"]):
            vp = work / f"{sec['id']}.wav"
            if not vp.exists() or vp.stat().st_size < 10_000:
                synth_gurukuladesam_voice("\n\n".join(sec["paragraphs"]), vp, api_key)
            vdur = dur_of(vp)
            print(f"  [{ep_id}] {sec['id']}: {vdur:.2f}s")
            vo_paths.append(vp)

            v_out = work / f"vo_bedded_{idx+1}.wav"
            off = bg_offsets[idx]
            fc_v = (
                f"[0:a]apad=pad_dur=0.25,atrim=0:{vdur+0.25:.3f},asetpts=PTS-STARTPTS[v];"
                f"[1:a]aloop=loop=-1:size=2e+09,atrim={off}:{off+vdur+0.25:.3f},asetpts=PTS-STARTPTS,"
                f"volume=0.075,afade=t=in:st=0:d=0.4,afade=t=out:st={max(0.1, vdur-0.2):.3f}:d=0.45[b];"
                f"[v][b]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[out]"
            )
            subprocess.run(
                ["ffmpeg", "-nostdin", "-y", "-i", str(vp), "-i", str(bg_unit), "-filter_complex", fc_v, "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(v_out)],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            )
            voiced_with_bg.append(v_out)

        sequence = [
            (intro_6s, 0.90),
            (voiced_with_bg[0], 0.45),
            (inter_a, 0.45),
            (voiced_with_bg[1], 0.45),
            (inter_b, 0.45),
            (voiced_with_bg[2], 0.45),
            (inter_a, 0.45),
            (voiced_with_bg[3], 0.45),
            (inter_b, 0.45),
            (voiced_with_bg[4], 1.10),
            (outro_12s, 0.0),
        ]

        cur_t = 0.0
        sec_starts = []
        for seq_i, (p, xf) in enumerate(sequence):
            if seq_i in (1, 3, 5, 7, 9):
                sec_starts.append(round(cur_t, 3))
            cur_t += dur_of(p) - xf

        inputs = []
        for p, _ in sequence:
            inputs.extend(["-i", str(p)])
        fc_chain = []
        prev = "[0:a]"
        for i in range(1, len(sequence)):
            xf_dur = sequence[i - 1][1]
            out_lbl = f"[m{i}]" if i < len(sequence) - 1 else "[pre_master]"
            fc_chain.append(f"{prev}[{i}:a]acrossfade=d={xf_dur}:c1=tri:c2=tri{out_lbl};")
            prev = out_lbl
        fc_chain.append("[pre_master]loudnorm=I=-14:TP=-1.5:LRA=9[out]")

        master_wav = ep_dir / f"{slug}.wav"
        subprocess.run(
            ["ffmpeg", "-nostdin", "-y", *inputs, "-filter_complex", "".join(fc_chain), "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(master_wav)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        total_dur = dur_of(master_wav)

        opus_rel = f"audio/women_{ep_id}.opus"
        opus_path = STUDIO_PUB / opus_rel
        opus_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(master_wav), "-c:a", "libopus", "-b:a", "192k", str(opus_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        spec_name = f"women_{ep_id}_spectrum.bin"
        n_frames = extract_spectrum_bin(master_wav, STUDIO_PUB / spec_name)

        # Build initial RMS-snapped sentence timeline (will be refined with Colab faster-whisper GPU forced alignment!)
        captions = [
            {
                "startSec": 0.4,
                "endSec": round(sec_starts[0] - 0.15, 2),
                "badge": "குரு குல தேசம் • மகளிர் சிறப்புத் தொடர்",
                "isDialogue": False,
                "line1": "சிவாயநம! • அன்பான தாய்மார்களே, சகோதரிகளே!",
                "line2": ep["title_pill"],
            }
        ]
        stem_manifest = []
        for idx, sec in enumerate(ep["sections"]):
            sec_caps = map_sentences_rms_fallback(vo_paths[idx], sec_starts[idx], sec["paragraphs"], sec["badge"], sec["isDialogue"] if "isDialogue" in sec else sec["is_story"])
            captions.extend(sec_caps)
            stem_manifest.append(
                {
                    "sec_idx": idx,
                    "sec_id": sec["id"],
                    "badge": sec["badge"],
                    "is_story": sec["is_story"],
                    "stem_wav": f"{ep_id}_{sec['id']}.wav",
                    "master_offset": sec_starts[idx],
                    "stem_dur": round(dur_of(vo_paths[idx]), 3),
                    "sentences": [c["writtenSentence"] for c in sec_caps],
                }
            )

        captions.append(
            {
                "startSec": round(total_dur - 11.8, 2),
                "endSec": round(total_dur - 1.4, 2),
                "badge": "குரு குல தேசம் • ஆசீர்வாதம்",
                "isDialogue": False,
                "line1": "நல்லதே நினைப்போம் • நல்லதே நடக்கும்",
                "line2": "சிவாயநம!",
            }
        )

        # Section-aware 16-shot mapping so shots align cleanly with the 5 narrative sections!
        # Shots allocation across 5 sections: [3, 3, 4, 4, 2] for ep01 & ep03; [3, 4, 3, 4, 2] for ep02
        alloc = [3, 4, 3, 4, 2] if ep_id == "ep02" else [3, 3, 4, 4, 2]
        sec_spans = [
            (0.0, round(sec_starts[1] - 2.2, 2)),
            (round(sec_starts[1] - 2.2, 2), round(sec_starts[2] - 2.2, 2)),
            (round(sec_starts[2] - 2.2, 2), round(sec_starts[3] - 2.2, 2)),
            (round(sec_starts[3] - 2.2, 2), round(sec_starts[4] - 2.2, 2)),
            (round(sec_starts[4] - 2.2, 2), round(total_dur, 2)),
        ]
        shots = []
        shot_num = 1
        for (sp0, sp1), k in zip(sec_spans, alloc):
            for j in range(k):
                s0 = round(sp0 + (j / k) * (sp1 - sp0), 2)
                s1 = round(sp0 + ((j + 1) / k) * (sp1 - sp0), 2)
                shots.append({"shotNum": shot_num, "startSec": s0, "endSec": s1, "camPreset": ((shot_num - 1) * 3) % 8})
                shot_num += 1

        tl_data = {
            "ep_id": ep_id,
            "slug": slug,
            "titlePillText": ep["title_pill"],
            "durationSec": round(total_dur, 2),
            "durationInFrames": n_frames,
            "audioFile": opus_rel,
            "spectrumFile": spec_name,
            "shotsFolder": f"women_{ep_id}",
            "shots": shots,
            "captions": [{k: v for k, v in c.items() if k != "writtenSentence"} for c in captions],
            "stem_manifest": stem_manifest,
        }
        (work / "episode_timeline.json").write_text(json.dumps(tl_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  => {slug}: {total_dur:.2f}s ({n_frames} frames, 16 section-locked shots, {len(captions)} kinetic captions)")


def _gen_single_gflow(prompt: str, out_jpg: Path, profile: str, env: dict, prefer_model: str = "nano-pro") -> None:
    if out_jpg.exists() and out_jpg.stat().st_size > 45_000:
        return
    models = [prefer_model, "nano2"] if prefer_model == "nano-pro" else ["nano2"]
    for model_name in models:
        for att in range(2):
            res = subprocess.run(
                [
                    "gflow-headless", "image", "t2i",
                    "--profile", profile,
                    prompt,
                    "--aspect", "16:9",
                    "--model", model_name,
                    "--out-file", str(out_jpg),
                ],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if res.returncode == 0 and out_jpg.exists() and out_jpg.stat().st_size > 45_000:
                # Ensure < 1.92 MB JPEG for YouTube compatibility & fast Remotion decoding
                im = Image.open(out_jpg).convert("RGB")
                if out_jpg.stat().st_size > 1_900_000:
                    im.save(out_jpg, format="JPEG", quality=88, optimize=True)
                print(f"  [{profile}/{model_name}] Saved {out_jpg.name} ({out_jpg.stat().st_size // 1024} KB)")
                return
            print(f"  [{profile}/{model_name} retry {att+1}] {out_jpg.name}: {res.stdout[-200:].strip()}")
            time.sleep(2)
    raise RuntimeError(f"Failed to generate {out_jpg} on profile {profile}")


def _gen_batch_or_single(tasks: list[tuple[str, Path, str]], profile: str) -> None:
    """
    Runs strictly sequentially on `profile` (1 process per profile lock).
    Uses `gflow-headless image batch` (4 shots per project) for scene shots, and `t2i --model nano-pro` for thumbnails.
    """
    env = os.environ.copy()
    env["GFLOW_CLI_UPDATE_CHECK"] = "0"
    env["GFLOW_CLI_LEASE_WAIT_SECONDS"] = "180"

    thumb_tasks = [t for t in tasks if t[2] == "thumb"]
    shot_tasks = [t for t in tasks if t[2] == "shot"]

    # 1. Generate Movie-Poster Thumbnails first with strict nano-pro!
    for prompt, dst, _ in thumb_tasks:
        dst.parent.mkdir(parents=True, exist_ok=True)
        _gen_single_gflow(prompt, dst, profile, env, prefer_model="nano-pro")

    # 2. Generate 16:9 story shots sequentially via t2i --model nano-pro (skips batch multi-prompt WAF rejections)
    pending_shots = [(p, d) for p, d, _ in shot_tasks if not (d.exists() and d.stat().st_size > 45_000)]
    for p_txt, dst in pending_shots:
        dst.parent.mkdir(parents=True, exist_ok=True)
        _gen_single_gflow(p_txt, dst, profile, env, prefer_model="nano-pro")
        time.sleep(2.5)


def build_qa_sheets() -> None:
    qa_dir = Path("/tmp/women_series_qa")
    qa_dir.mkdir(parents=True, exist_ok=True)

    # 1. Storyboard 4x4 contact sheets per episode + duplicate hash assertion
    for ep in EPISODES:
        ep_id = ep["id"]
        slug = ep["slug"]
        shot_dir = STUDIO_PUB / f"women_{ep_id}"
        hashes = set()
        sheet = Image.new("RGB", (1920, 1080), (12, 16, 28))
        draw = ImageDraw.Draw(sheet)
        for idx in range(16):
            sp = shot_dir / f"shot_{idx+1:02d}.jpg"
            assert sp.exists() and sp.stat().st_size > 40_000, f"Missing shot {sp}"
            h = hashlib.sha256(sp.read_bytes()).hexdigest()
            hashes.add(h)
            im = Image.open(sp).convert("RGB").resize((468, 256), Image.Resampling.LANCZOS)
            cx = (idx % 4) * 480 + 6
            cy = (idx // 4) * 270 + 7
            sheet.paste(im, (cx, cy))
            draw.rectangle([cx + 6, cy + 6, cx + 96, cy + 32], fill=(0, 0, 0))
            draw.text((cx + 12, cy + 10), f"{ep_id} #{idx+1:02d}", fill=(255, 225, 120))
        assert len(hashes) == 16, f"{slug}: duplicate shots detected ({len(hashes)}/16 unique)!"
        # Also mirror shots into episode asset folder
        ep_shots_backup = OUT_ROOT / slug / "shots"
        ep_shots_backup.mkdir(parents=True, exist_ok=True)
        for idx in range(16):
            shutil.copy2(shot_dir / f"shot_{idx+1:02d}.jpg", ep_shots_backup / f"shot_{idx+1:02d}.jpg")
        out_q = qa_dir / f"qa_storyboard_{ep_id}.jpg"
        sheet.save(out_q, format="JPEG", quality=88)
        print(f"QA Storyboard saved: {out_q} (16/16 unique SHA-256 verified)")


def build_visuals_all() -> None:
    all_items: list[tuple[str, Path, str]] = []

    for ep in EPISODES:
        ep_id = ep["id"]
        slug = ep["slug"]
        thumb_dst = OUT_ROOT / slug / f"{slug}_Thumbnail.jpg"
        shot_dir = STUDIO_PUB / f"women_{ep_id}"
        shot_dir.mkdir(parents=True, exist_ok=True)

        if not (thumb_dst.exists() and thumb_dst.stat().st_size > 45_000):
            all_items.append((ep["thumbnail_prompt"], thumb_dst, "thumb"))

        for s_idx, s_prompt in enumerate(ep["shot_prompts"]):
            full_p = SCENE_STYLE_PREFIX + s_prompt
            dst = shot_dir / f"shot_{s_idx+1:02d}.jpg"
            if not (dst.exists() and dst.stat().st_size > 45_000):
                all_items.append((full_p, dst, "shot"))

    print(f"Running fast 5-shot stay-mounted nano-pro batch on profile nagaraj957: {len(all_items)} remaining items")
    if all_items:
        _gen_batch_or_single(all_items, "nagaraj957")

    build_qa_sheets()


def main():
    validate_catalog()
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", default=os.environ.get("ELEVENLABS_KEY", ""))
    ap.add_argument("--audio-only", action="store_true")
    ap.add_argument("--visuals-only", action="store_true")
    args = ap.parse_args()

    if not args.visuals_only:
        assert args.api_key, "Pass --api-key or ELEVENLABS_KEY"
        build_audio_all(args.api_key)
    if not args.audio_only:
        build_visuals_all()


if __name__ == "__main__":
    main()
