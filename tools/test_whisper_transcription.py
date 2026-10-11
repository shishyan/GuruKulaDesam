import whisper
import json, sys

sys.stdout.reconfigure(encoding='utf-8')

print("Loading Whisper model 'base'...")
model = whisper.load_model("base")

print("Transcribing scratch/Mata6vtnrjQ.wav with language='ta'...")
result = model.transcribe("scratch/Mata6vtnrjQ.wav", language="ta", verbose=False)

print(f"\nDetected {len(result['segments'])} segments:")
for s in result['segments']:
    print(f"[{s['start']:.2f}s -> {s['end']:.2f}s] {s['text'].strip()}")

out_file = "scratch/whisper_Mata6vtnrjQ.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(f"\nSaved full transcription to {out_file}")
