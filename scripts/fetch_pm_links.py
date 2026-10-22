import urllib.request
import re
import sys

url = 'https://www.projectmadurai.org/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        links = re.findall(r'href=[\'"](.*?)[\'"]', html)
        for l in links[:40]:
            sys.stdout.buffer.write((l + '\n').encode('utf-8'))
except Exception as e:
    sys.stdout.buffer.write((str(e) + '\n').encode('utf-8'))
