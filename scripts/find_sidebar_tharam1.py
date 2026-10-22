import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('tharam-1.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<aside[^>]*id="([^"]+)"[^>]*>', text):
    print("Found <aside> in tharam-1.html:", m.group(0))

# Search for courseSidebar
idx = text.find('courseSidebar')
if idx != -1:
    print(text[idx-50:idx+800])
