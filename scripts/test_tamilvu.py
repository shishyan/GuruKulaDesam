import sys, urllib.request, re
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://www.tamilvu.org/library/libindex.htm'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
    links = re.findall(r'<a\s+href=[\'"](.*?)[\'"][^>]*>(.*?)</a>', html, re.DOTALL)
    print(f'TamilVU Library Links count: {len(links)}')
    for h, text in links[:30]:
        cleaned = re.sub(r'<[^>]*>', '', text).strip()
        if cleaned:
            print(f'  {cleaned[:40]:40} -> {h}')
except Exception as e:
    print('TamilVU error:', e)
