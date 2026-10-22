import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Check continuation of Category:ஆறுமுக நாவலர் or check palm-leaf manuscripts category
palm_category = urllib.parse.quote('Category:சுவடிகள்')
url = f'http://noolaham.org/wiki/api.php?action=query&list=categorymembers&cmtitle={palm_category}&cmlimit=100&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    members = data.get('query', {}).get('categorymembers', [])
    print(f"Total Category:சுவடிகள் members: {len(members)}")
    for m in members[:40]:
        print("  - " + m["title"])
except Exception as e:
    print("Error:", e)
