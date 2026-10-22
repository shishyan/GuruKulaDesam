import urllib.request
import re
import sys

url = 'https://www.projectmadurai.org/pmworks.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'<a[^>]*href=[\'"](.*?)[\'"][^>]*>(.*?)</a>', html, re.I | re.S)
        sys.stdout.buffer.write((f'Total links in pmworks: {len(matches)}\n').encode('utf-8'))
        for href, text in matches:
            clean_text = re.sub(r'\s+', ' ', text).strip()
            if any(k in clean_text or k in href.lower() for k in ['ராமாயண', 'பாரத', 'கந்த', 'புராண', 'ramayan', 'kambar', 'villiputhur']):
                sys.stdout.buffer.write((f"{href} => {clean_text}\n").encode('utf-8'))
except Exception as e:
    sys.stdout.buffer.write((str(e) + '\n').encode('utf-8'))
