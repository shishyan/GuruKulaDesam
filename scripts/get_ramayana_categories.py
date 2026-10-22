import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

q = urllib.parse.quote('இராமாயண')
url = f'http://noolaham.org/wiki/api.php?action=query&list=allcategories&acprefix={q}&aclimit=50&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    cats = data.get('query', {}).get('allcategories', [])
    print(f"Categories starting with இராமாயண: {len(cats)}")
    for c in cats:
        print("  - " + c["*"])
except Exception as e:
    print("Error:", e)
