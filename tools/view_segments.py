import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/whisper_Mata6vtnrjQ.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total segments: {len(data['segments'])}\n")
for i, s in enumerate(data['segments'], 1):
    print(f"{i:2d}. [{s['start']:6.2f}s - {s['end']:6.2f}s] {s['text'].strip()}")
