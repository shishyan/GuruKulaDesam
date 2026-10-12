import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/whisper_f1jxgAbXcdE.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total segments: {len(d['segments'])}")
for idx, s in enumerate(d['segments']):
    print(f"[{idx+1:02d}] {s['start']:6.2f}s -> {s['end']:6.2f}s: {s['text'].strip()}")
