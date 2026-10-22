import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

q = urllib.parse.quote('உரைநடை OR வசனம்')
url = f'http://noolaham.org/wiki/api.php?action=query&list=search&srsearch={q}&srlimit=50&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    results = data.get('query', {}).get('search', [])
    print(f"Results for உரைநடை OR வசனம்: {len(results)}")
    for r in results:
        t = r["title"]
        if any(k in t for k in ['புராண', 'பாரத', 'இராமாயண', 'கதை', 'காவிய']):
            print("  - " + t)
except Exception as e:
    print("Error:", e)
