import sys, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://www.tamilvu.org/library/libindex.htm'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
links = re.findall(r'<a\s+href=[\'"](.*?)[\'"][^>]*>(.*?)</a>', html, re.DOTALL)
for h, text in links:
    cleaned = re.sub(r'<[^>]*>', '', text).strip()
    if any(k in cleaned for k in ['புராணம்', 'காவியம்', 'இலக்கியம்', 'சமயம்', 'நூலகம்', 'இராமாயணம்', 'பாரதம்']):
        print(f'{cleaned:40} -> {h}')
