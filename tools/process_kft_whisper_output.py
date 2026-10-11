import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

whisper_file = "scratch/whisper_KFtS403RfbY.json"
if not os.path.exists(whisper_file):
    print(f"Waiting for {whisper_file}...")
    sys.exit(0)

with open(whisper_file, "r", encoding="utf-8") as f:
    data = json.load(f)

segments = data.get("segments", [])
print(f"Total acoustic segments detected: {len(segments)}")

for idx, seg in enumerate(segments):
    start = seg["start"]
    end = seg["end"]
    text = seg["text"].strip()
    m_s = f"{int(start//60):02d}:{int(start%60):02d}"
    m_e = f"{int(end//60):02d}:{int(end%60):02d}"
    print(f"[{idx+1:02d}] {m_s} -> {m_e} ({end-start:5.2f}s): {text}")
