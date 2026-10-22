import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\GitHub\Gurukuladesam\puranas.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<aside[^>]*class="purana-sticky-sidebar".*?</aside>', text, re.DOTALL)
if matches:
    print(matches[0])
