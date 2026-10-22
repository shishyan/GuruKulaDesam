import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

q = urllib.parse.quote('Manuscript')
url = f'http://noolaham.org/wiki/api.php?action=query&list=search&srsearch={q}&srlimit=20&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    items = data.get('query', {}).get('search', [])
    print(f"Manuscript search results: {len(items)}")
    for it in items:
        print("  - " + it["title"])
except Exception as e:
    print("Error:", e)
