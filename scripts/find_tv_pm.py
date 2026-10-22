import urllib.request
import re
import sys

url = 'https://www.projectmadurai.org/pmworks.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')

rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.I | re.S)
for r in rows:
    if 'திருவிளையாடல்' in r or 'திருவிளையாடற்' in r:
        clean = re.sub(r'<[^>]+>', ' | ', r)
        clean = re.sub(r'\s+', ' ', clean).strip()
        sys.stdout.buffer.write((clean + '\n').encode('utf-8'))
