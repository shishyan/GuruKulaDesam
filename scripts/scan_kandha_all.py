import subprocess
import json
import sys

out = subprocess.check_output(['git', 'show', 'e0938dd1:data/puranas/kandha-puranam.json'], encoding='utf-8')
d = json.loads(out)
sys.stdout.buffer.write((f'Total chapters in Kandha: {len(d.get("chapters", []))}\n').encode('utf-8'))

for i in range(len(d.get('chapters', []))):
    ch = d['chapters'][i]
    t = ch['title']
    s = ch['synopsis'][:80].replace('\n', ' ')
    sys.stdout.buffer.write((f"{i+1}: {t} => {s}\n").encode('utf-8'))
