import subprocess
import json
import sys

out = subprocess.check_output(['git', 'show', 'e0938dd1:data/puranas/thiruvilaiyadal.json'], encoding='utf-8')
d = json.loads(out)
sys.stdout.buffer.write((f'Total chapters in e0938dd1: {len(d.get("chapters", []))}\n').encode('utf-8'))
for i in range(min(10, len(d.get('chapters', [])))):
    sys.stdout.buffer.write((f"Ch {i+1}: {d['chapters'][i]['title']}\n").encode('utf-8'))
