import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

pub = urllib.parse.quote('Category:வித்தியாநூபாலனயந்திரசாலை')
url = f'http://noolaham.org/wiki/api.php?action=query&list=categorymembers&cmtitle={pub}&cmlimit=100&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    members = data.get('query', {}).get('categorymembers', [])
    print(f"Total Vidyanupalana Yantrasala editions: {len(members)}")
    for m in members:
        print("  - " + m["title"])
except Exception as e:
    print("Error:", e)
