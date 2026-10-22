import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

q = urllib.parse.quote('கம்பராமாயணம்')
url = f'http://noolaham.org/wiki/api.php?action=query&list=search&srsearch={q}&srlimit=15&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    results = data.get('query', {}).get('search', [])
    print(f"Kamba Ramayanam search on Noolaham: {len(results)}")
    for r in results:
        print("  - " + r["title"])
except Exception as e:
    print("Error:", e)
