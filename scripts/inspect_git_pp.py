import subprocess
import json
import sys

out = subprocess.check_output(['git', 'show', 'e0938dd1:data/puranas/periyapuranam.json'], encoding='utf-8')
d = json.loads(out)
sys.stdout.buffer.write((f"Total Periyapuranam entries in git: {len(d.get('chapters', []))}\n").encode('utf-8'))
for i in range(15):
    ch = d['chapters'][i]
    sys.stdout.buffer.write((f"{i+1}: {ch['title'][:70]}\n").encode('utf-8'))
