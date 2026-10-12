import json, sys
sys.stdout.reconfigure(encoding='utf-8')

fn = sys.argv[1] if len(sys.argv) > 1 else 'scratch/whisper_TUwlsvN7v1w.json'
with open(fn, 'r', encoding='utf-8') as f:
    data = json.load(f)

for s in data.get('segments', []):
    print(f"{s['start']:6.2f} -> {s['end']:6.2f}: {s['text']}")
