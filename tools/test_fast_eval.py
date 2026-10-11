import json
import urllib.request
import websocket
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Get tabs
resp = urllib.request.urlopen('http://127.0.0.1:9225/json')
tabs = json.loads(resp.read().decode('utf-8'))

# Pick the YouTube tab
yt_tab = None
for t in tabs:
    if 'youtube.com' in t.get('url', '') and 'studio' not in t.get('url', ''):
        yt_tab = t
        break

if not yt_tab:
    print("No YouTube tab found among:", [t.get('url') for t in tabs])
    sys.exit(1)

print(f"Connecting to: {yt_tab.get('title')} ({yt_tab.get('url')})")
ws_url = yt_tab.get('webSocketDebuggerUrl')

ws = websocket.create_connection(ws_url, timeout=5)
# Evaluate document.title
req = {
    "id": 100,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.title",
        "returnByValue": True
    }
}
ws.send(json.dumps(req))

while True:
    msg = ws.recv()
    data = json.loads(msg)
    if data.get('id') == 100:
        val = data.get('result', {}).get('result', {}).get('value')
        print(f"SUCCESS! Document title is: {val}")
        break

ws.close()
