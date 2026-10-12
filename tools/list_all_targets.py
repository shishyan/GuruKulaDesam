import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

# Check raw CDP targets directly from Chrome endpoint http://127.0.0.1:9225/json
req = urllib.request.urlopen("http://127.0.0.1:9225/json")
targets = json.loads(req.read().decode('utf-8'))

print(f"Total targets on port 9225: {len(targets)}")
for t in targets:
    print(f"  Type: {t.get('type'):<10} | URL: {t.get('url')} | Title: {t.get('title')}")
