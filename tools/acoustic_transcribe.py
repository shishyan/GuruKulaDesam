"""
Acoustic Transcribe and Lyric Alignment Tool
Uses OpenAI Whisper ('tiny' model) with single-pass greedy decoding (no fallback loops)
to extract exact acoustic timestamps for sung vocal segments and align canonical lyrics.
"""

import os
import sys
import json
import time
import torch
import whisper

torch.set_num_threads(8)
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

def transcribe_audio_acoustically(wav_path, out_json_path):
    print(f"[Whisper] Loading model 'tiny'...", flush=True)
    t0 = time.time()
    model = whisper.load_model("tiny")
    print(f"[Whisper] Loaded in {time.time() - t0:.2f}s", flush=True)

    print(f"[Whisper] Transcribing {wav_path} with fast greedy decoding...", flush=True)
    t1 = time.time()
    result = model.transcribe(
        wav_path,
        language="ta",
        temperature=(0.0,),
        compression_ratio_threshold=None,
        logprob_threshold=None,
        no_speech_threshold=None,
        condition_on_previous_text=False,
        fp16=False,
        verbose=False
    )
    print(f"[Whisper] Completed in {time.time() - t1:.2f}s! Segments: {len(result.get('segments', []))}", flush=True)

    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[Whisper] Saved acoustic output to {out_json_path}", flush=True)
    return result

if __name__ == "__main__":
    if len(sys.argv) > 2:
        wav = sys.argv[1]
        out = sys.argv[2]
    else:
        wav = "scratch/Mata6vtnrjQ.wav"
        out = "scratch/whisper_Mata6vtnrjQ.json"
    transcribe_audio_acoustically(wav, out)
