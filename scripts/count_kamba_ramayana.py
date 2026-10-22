import urllib.request
import re
import sys

# Project Madurai Kamba Ramayanam files:
# pmuni0414_01, pmuni0414_02 (Bala Kandam - 22 padalams)
# pmuni0422_01, pmuni0422_02 (Ayodhya Kandam - 12 padalams)
# pmuni0430, pmuni0455 (Aranya Kandam - 11 padalams)
# pmuni0478, pmuni0539 (Kishkindha Kandam - 16 padalams)
# pmuni0541_01, pmuni0541_02 (Sundara Kandam - 15 padalams)
# pmuni0545_01, pmuni0545_02, pmuni0558_01, pmuni0558_02, pmuni0561_01, pmuni0561_02 (Yuddha Kandam - 39 padalams)

pm_ramayana_files = [
    'pmuni0414_01', 'pmuni0414_02',
    'pmuni0422_01', 'pmuni0422_02',
    'pmuni0430', 'pmuni0455',
    'pmuni0478', 'pmuni0539',
    'pmuni0541_01', 'pmuni0541_02',
    'pmuni0545_01', 'pmuni0545_02',
    'pmuni0558_01', 'pmuni0558_02',
    'pmuni0561_01', 'pmuni0561_02'
]

total_ramayana_padalams = []

for fname in pm_ramayana_files:
    url = f'https://www.projectmadurai.org/pm_etexts/utf8/{fname}.html'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'<h[34][^>]*>(.*?)</h[34]>', html, re.I | re.S)
            for m in matches:
                clean = re.sub(r'<[^>]+>', '', m).strip()
                clean = re.sub(r'\s+', ' ', clean)
                if 'படலம்' in clean:
                    total_ramayana_padalams.append((fname, clean))
    except Exception as e:
        print(f"Error {fname}: {e}")

sys.stdout.buffer.write((f"Total distinct Kamba Ramayanam Padalams: {len(total_ramayana_padalams)}\n").encode('utf-8'))
for i, (fn, p) in enumerate(total_ramayana_padalams[:25]):
    sys.stdout.buffer.write((f"{i+1}: [{fn}] {p}\n").encode('utf-8'))
