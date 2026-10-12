import sys, json

fn = sys.argv[1] if len(sys.argv) > 1 else 'scratch/whisper_6r6TpY-sgbw.json'
with open(fn, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total segments: {len(data['segments'])}")
for i, s in enumerate(data['segments']):
    t = s['text'].strip()
    # Print with utf-8 representation safe on windows console
    safe_t = t.encode('ascii', 'backslashreplace').decode('ascii')
    print(f"{i+1:02d} [{s['start']:6.2f} - {s['end']:6.2f}] {safe_t}")
