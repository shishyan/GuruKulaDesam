import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

fp = r"C:\GitHub\Gurukuladesam\data\puranas\ramayanam.json"
with open(fp, 'r', encoding='utf-8') as f:
    d = json.load(f)

for ch in d['chapters']:
    print(ch['chapterNumber'], ch['title'])
    print(ch['exposition'][:200])
    print('-'*40)
