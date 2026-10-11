import whisper
import json, sys, time

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

print("Loading Whisper model 'tiny'...", flush=True)
t0 = time.time()
model = whisper.load_model("tiny")
print(f"Model loaded in {time.time() - t0:.2f}s", flush=True)

print("Transcribing scratch/Mata6vtnrjQ.wav with temperature=0.0, condition_on_previous_text=False...", flush=True)
t1 = time.time()
result = model.transcribe(
    "scratch/Mata6vtnrjQ.wav",
    language="ta",
    temperature=0.0,
    best_of=1,
    beam_size=1,
    condition_on_previous_text=False,
    fp16=False,
    verbose=True
)
print(f"\nDecoding completed in {time.time() - t1:.2f}s!", flush=True)

out_file = "scratch/whisper_Mata6vtnrjQ.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(f"Saved full transcription to {out_file}", flush=True)
