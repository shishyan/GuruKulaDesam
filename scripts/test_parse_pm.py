import urllib.request
import re
import sys

def parse_padalams(html):
    # Splits by headings like 1.1, 1.2, etc.
    sections = re.split(r'<h[34][^>]*>(.*?)</h[34]>', html, flags=re.I | re.S)
    padalams = []
    for i in range(1, len(sections), 2):
        title = re.sub(r'<[^>]+>', '', sections[i]).strip()
        body_html = sections[i+1]
        # Clean text
        text = re.sub(r'<br\s*/?>', '\n', body_html, flags=re.I)
        text = re.sub(r'<p[^>]*>', '\n\n', text, flags=re.I)
        text = re.sub(r'</p>', '', text, flags=re.I)
        text = re.sub(r'<[^>]+>', '', text)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        clean_text = '\n'.join(lines)
        if len(clean_text) > 200:
            padalams.append((title, clean_text))
    return padalams

url = 'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0414_01.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')

pads = parse_padalams(html)
sys.stdout.buffer.write((f'Parsed {len(pads)} padalams from PM 0414_01\n').encode('utf-8'))
for t, b in pads:
    sys.stdout.buffer.write((f"- {t} ({len(b)} chars, {len(b.splitlines())} lines)\n").encode('utf-8'))
