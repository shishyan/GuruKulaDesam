import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# Navigate to YouTube Studio home or check active channel/email on YouTube Studio tab
ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://flow.google.com/u/0/'}}))
print("Navigated to /u/0/:", ws.recv())
ws.close()
