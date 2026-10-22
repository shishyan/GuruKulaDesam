import subprocess
import json
import sys

out = subprocess.check_output(['git', 'show', 'e0938dd1:data/puranas/thiruvilaiyadal.json'], encoding='utf-8')
d = json.loads(out)
sys.stdout.buffer.write((f'Total chapters in Thiruvilaiyadal: {len(d.get("chapters", []))}\n').encode('utf-8'))
for i, ch in enumerate(d.get('chapters', [])):
    sys.stdout.buffer.write((f"{i+1}: {ch['title'][:70]}\n").encode('utf-8'))
