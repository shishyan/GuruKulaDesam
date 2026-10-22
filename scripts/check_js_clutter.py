import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\GitHub\Gurukuladesam\assets\js\purana-reader.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
keywords = ['verse', 'பாடல்', 'மூலப் பாடல்', 'சுலோகம்', 'ஸ்லோகம்', 'அருளியவர்', 'உரை', 'Verbatim']
for kw in keywords:
    matches = [line.strip() for line in text.split('\n') if kw in line]
    if matches:
        print(f"Keyword '{kw}': {len(matches)} matches")
        for m in matches[:3]:
            print("  ", m[:100])
