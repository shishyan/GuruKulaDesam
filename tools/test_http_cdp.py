import urllib.request, json
try:
    with urllib.request.urlopen('http://127.0.0.1:9225/json', timeout=2) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"HTTP CDP responds OK! Total targets: {len(data)}")
except Exception as e:
    print("HTTP CDP error:", e)
