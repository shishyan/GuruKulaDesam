import urllib.request, json
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
for t in tabs:
    print(f"Tab: {t.get('title')} | URL: {t.get('url')} | Type: {t.get('type')}")

