import urllib.request, json

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json').read())
for i, t in enumerate(tabs):
    print(f"{i}: type={t.get('type')}, id={t.get('id')}, url={t.get('url')}")
