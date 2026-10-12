import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/whisper_ETELjf0OTi4.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total segments: {len(d['segments'])}")
for idx, s in enumerate(d['segments']):
    print(f"[{idx+1}] {s['start']:.2f}s -> {s['end']:.2f}s: {s['text']}")
