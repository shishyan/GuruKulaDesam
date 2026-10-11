import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
    targets = json.loads(r.read().decode())

page = next(t for t in targets if t.get('type') == 'page')
target_id = page['id']
print("Activating page target:", target_id)

url = f"http://127.0.0.1:9225/json/activate/{target_id}"
req = urllib.request.Request(url, method='GET')
with urllib.request.urlopen(req) as resp:
    print("Activate response:", resp.read().decode())
