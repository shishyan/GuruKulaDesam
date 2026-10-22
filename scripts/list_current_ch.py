import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open(r'C:\GitHub\Gurukuladesam\data\puranas\children-purana-stories.json', encoding='utf-8'))
for ch in data['chapters']:
    print(ch['chapterNumber'], ch['title'])
