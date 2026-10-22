import urllib.request
import re
import sys

url = 'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0414_01.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        sys.stdout.buffer.write((f'PM 0414_01 length: {len(html)} bytes\n').encode('utf-8'))
        # find headings
        headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html, re.I | re.S)
        sys.stdout.buffer.write((f'Headings count: {len(headings)}\n').encode('utf-8'))
        for h in headings[:15]:
            clean_h = re.sub(r'<[^>]+>', '', h).strip()
            sys.stdout.buffer.write((f'- {clean_h}\n').encode('utf-8'))
except Exception as e:
    sys.stdout.buffer.write((str(e) + '\n').encode('utf-8'))
