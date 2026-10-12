import sys, json

sys.stdout.reconfigure(encoding='utf-8')
fn = sys.argv[1]
with open(fn, 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"File: {fn} | Total Segments: {len(d['segments'])}")
for i, s in enumerate(d['segments']):
    st = s['start']
    en = s['end']
    tx = s['text'].strip()
    print(f"{i+1:02d} [{st:6.2f} - {en:6.2f}] {tx}")
