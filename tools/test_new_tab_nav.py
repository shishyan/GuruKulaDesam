import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
    targets = json.loads(r.read().decode())
old_page = next(t for t in targets if t.get('type') == 'page')
old_id = old_page['id']
print("Old page ID:", old_id, old_page['url'])

vid = "rRoJfeRQiaM"
new_url = f"https://studio.youtube.com/video/{vid}/edit"
print(f"Opening new tab for {new_url}...")

req = urllib.request.Request(f"http://127.0.0.1:9225/json/new?{new_url}", method='PUT')
with urllib.request.urlopen(req) as resp:
    new_page_data = json.loads(resp.read().decode())
    print("New page ID:", new_page_data['id'], new_page_data['url'])

time.sleep(2)
print("Closing old tab...")
req_close = urllib.request.Request(f"http://127.0.0.1:9225/json/close/{old_id}", method='PUT')
with urllib.request.urlopen(req_close) as resp:
    print("Closed old tab:", resp.read().decode())
