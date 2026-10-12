import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

url = "https://www.youtube.com/watch?v=qPjurMK6xpI"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

m = re.search(r'"shortDescription":"(.*?)"', html)
if m:
    desc = m.group(1).encode('utf-8').decode('unicode_escape')
    print("Description length:", len(desc))
    print("Has முதாகராத்த:", "முதாகராத்த" in desc)
    print("Has நிதாந்த:", "நிதாந்த" in desc)
    print("--- Desc ---")
    print(desc[:600])
    print("...")
    print(desc[-600:])
else:
    print("Not found in HTML")
