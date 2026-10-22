import glob
import json

pattern = 'data/puranas/*.json'
bp_target = 'மனிதனின் மனோநிலையை பிரதிபலிக்கின்றன'

for filepath in sorted(glob.glob(pattern)):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    if bp_target in text:
        data = json.loads(text)
        chapters = data.get('chapters', [])
        bp_indices = [
            i+1 for i, ch in enumerate(chapters)
            if bp_target in ch.get('exposition', '') or bp_target in ch.get('summary', '')
        ]
        print(f"{filepath} : {len(bp_indices)} / {len(chapters)} chapters have boilerplate -> {bp_indices}")
