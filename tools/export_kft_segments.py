import json, sys

with open("scratch/whisper_KFtS403RfbY.json", "r", encoding="utf-8") as f:
    data = json.load(f)

segments = data.get("segments", [])
out_lines = [f"Total acoustic segments detected: {len(segments)}"]

for idx, seg in enumerate(segments):
    start = seg["start"]
    end = seg["end"]
    text = seg["text"].strip()
    m_s = f"{int(start//60):02d}:{int(start%60):02d}"
    m_e = f"{int(end//60):02d}:{int(end%60):02d}"
    out_lines.append(f"[{idx+1:03d}] {m_s} -> {m_e} ({end-start:5.2f}s): {text}")

with open("scratch/kft_segments.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print(f"Wrote {len(segments)} segments to scratch/kft_segments.txt")
