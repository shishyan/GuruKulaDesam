import urllib.request, json

for port in [9222, 9223, 9224, 9225]:
    try:
        tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list', timeout=1).read())
        print(f"Port {port} connected! Total tabs: {len(tabs)}")
        for t in tabs:
            if t.get('type') == 'page':
                print(f"  [{port}] {t.get('title')} | {t.get('url')}")
    except Exception as e:
        pass
