import urllib.request, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json/list').read())
    print("SUCCESS: Edge connected on port 9223!")
    for t in tabs:
        print(f"Tab: {t.get('title')} | URL: {t.get('url')}")
except Exception as e:
    print("Edge port 9223 error:", e)

