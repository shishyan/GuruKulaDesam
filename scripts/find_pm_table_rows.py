import urllib.request
import re
import sys

url = 'https://www.projectmadurai.org/pmworks.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')

rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.I | re.S)
sys.stdout.buffer.write((f'Total table rows: {len(rows)}\n').encode('utf-8'))

for r in rows:
    if any(k in r for k in ['கம்பராமாயணம்', 'ராமாயணம்', 'பாரதம்', 'மகாபாரதம்', 'கந்தபுராணம்']):
        clean_row = re.sub(r'<[^>]+>', ' | ', r)
        clean_row = re.sub(r'\s+', ' ', clean_row).strip()
        sys.stdout.buffer.write((clean_row[:150] + '\n').encode('utf-8'))
