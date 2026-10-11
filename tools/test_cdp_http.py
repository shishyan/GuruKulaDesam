import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

try:
    with urllib.request.urlopen("http://127.0.0.1:9225/json", timeout=3) as resp:
        data = json.loads(resp.read().decode())
        print(f"Total targets: {len(data)}")
        for item in data:
            print(f"- Type: {item.get('type')}, Title: {item.get('title')}, URL: {item.get('url')}")
except Exception as e:
    print("Error:", e)
