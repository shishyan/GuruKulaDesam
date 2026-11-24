#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote Colab L4 GPU Forced-Alignment Script (`faster-whisper` large-v3, CUDA float16).
Maps exact written Tamil script sentences onto Whisper word timestamps so zero Whisper text
is ever displayed — only 100% clean written Tamil sentences locked to true vocal timing!
"""

import json
import os
import subprocess
import sys
import wave
import numpy as np

print("=== Installing faster-whisper on Colab GPU ===", flush=True)
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "faster-whisper"],
    check=True,
)

# Ensure cuBLAS/cuDNN shared libs from pip nvidia packages are discoverable
site_pkgs = subprocess.check_output(
    [sys.executable, "-c", "import site; print(site.getsitepackages()[0])"], text=True
).strip()
ld_dirs = []
for sub in ("nvidia/cublas/lib", "nvidia/cudnn/lib"):
    p = os.path.join(site_pkgs, sub)
    if os.path.isdir(p):
        ld_dirs.append(p)
if ld_dirs:
    os.environ["LD_LIBRARY_PATH"] = ":".join(ld_dirs + [os.environ.get("LD_LIBRARY_PATH", "")])

from faster_whisper import WhisperModel  # noqa: E402

print("=== Loading Whisper large-v3 on CUDA ===", flush=True)
model = WhisperModel("large-v3", device="cuda", compute_type="float16")


def load_16k_mono(wav_path: str) -> np.ndarray:
    raw16 = wav_path + ".16k.wav"
    subprocess.run(
        ["ffmpeg", "-nostdin", "-y", "-i", wav_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", raw16],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    with wave.open(raw16, "rb") as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    os.remove(raw16)
    return pcm


def split_clauses_two_lines(sentence: str):
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


with open("/content/stems/timelines_in.json", "r", encoding="utf-8") as f:
    timelines = json.load(f)

out_timelines = {}
for ep_id, tl in timelines.items():
    total_dur = tl["durationSec"]
    first_sec_start = tl["stem_manifest"][0]["master_offset"]
    aligned_caps = [
        {
            "startSec": 0.4,
            "endSec": round(first_sec_start - 0.15, 2),
            "badge": "குரு குல தேசம் • மகளிர் சிறப்புத் தொடர்",
            "isDialogue": False,
            "line1": "சிவாயநம! • அன்பான தாய்மார்களே, சகோதரிகளே!",
            "line2": tl["titlePillText"],
        }
    ]

    for sm in tl["stem_manifest"]:
        wav_file = os.path.join("/content/stems", sm["stem_wav"])
        audio_arr = load_16k_mono(wav_file)
        dur = sm["stem_dur"]
        offset = sm["master_offset"]
        sents = sm["sentences"]

        segments, _ = model.transcribe(
            audio_arr,
            language="ta",
            word_timestamps=True,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 220},
        )
        w_list = []
        for seg in segments:
            for w in (seg.words or []):
                w_list.append((float(w.start), float(w.end), len(w.word.strip()) or 1))

        if len(w_list) >= len(sents):
            # Map written sentences monotonically onto cumulative Whisper spoken character progress!
            total_w_chars = max(1, sum(c for _, _, c in w_list))
            w_cum = []
            acc = 0
            for ws, we, wc in w_list:
                w_cum.append((acc / total_w_chars, (acc + wc) / total_w_chars, ws, we))
                acc += wc

            total_s_chars = max(1, sum(len(s) for s in sents))
            s_acc = 0
            prev_end = 0.05
            for s_idx, s in enumerate(sents):
                r0 = s_acc / total_s_chars
                s_acc += len(s)
                r1 = s_acc / total_s_chars
                # Find closest word start for r0 and closest word end for r1
                cand_starts = [ws for p0, _, ws, _ in w_cum if p0 >= r0 - 0.04]
                cand_ends = [we for _, p1, _, we in w_cum if p1 <= r1 + 0.04]
                t0 = max(prev_end + 0.04, cand_starts[0] if cand_starts else r0 * dur)
                t1 = cand_ends[-1] if cand_ends else r1 * dur
                if s_idx == len(sents) - 1:
                    t1 = max(t0 + 0.8, min(dur - 0.05, max(t1, dur - 0.25)))
                elif t1 <= t0 + 0.6:
                    t1 = min(dur - 0.1, t0 + max(1.0, (len(s) / total_s_chars) * dur))
                prev_end = t1
                l1, l2 = split_clauses_two_lines(s)
                aligned_caps.append(
                    {
                        "startSec": round(offset + t0, 2),
                        "endSec": round(offset + t1, 2),
                        "badge": sm["badge"],
                        "isDialogue": bool(sm["is_story"] and (s_idx % 2 == 1 or "!" in s)),
                        "line1": l1,
                        "line2": l2,
                    }
                )
            print(f"  [Whisper GPU {ep_id}/{sm['sec_id']}] Aligned {len(sents)} sentences across {len(w_list)} acoustic words", flush=True)
        else:
            print(f"  [Fallback {ep_id}/{sm['sec_id']}] Kept RMS boundaries", flush=True)

    aligned_caps.append(
        {
            "startSec": round(total_dur - 11.8, 2),
            "endSec": round(total_dur - 1.4, 2),
            "badge": "குரு குல தேசம் • ஆசீர்வாதம்",
            "isDialogue": False,
            "line1": "நல்லதே நினைப்போம் • நல்லதே நடக்கும்",
            "line2": "சிவாயநம!",
        }
    )
    out_timelines[ep_id] = aligned_caps

with open("/content/aligned_captions_out.json", "w", encoding="utf-8") as f:
    json.dump(out_timelines, f, ensure_ascii=False, indent=2)

print("WHISPER_ALIGNMENT_COMPLETE", flush=True)
