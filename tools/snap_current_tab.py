import urllib.request, json, websocket, base64

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json').read())
page = [t for t in tabs if t.get('type') == 'page' and 'studio.youtube.com' in t.get('url', '')][0]
print(f"Connecting to {page['id']} ({page['url']})...")

ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=10)
req = {'id': 1, 'method': 'Page.captureScreenshot'}
ws.send(json.dumps(req))
m = json.loads(ws.recv())
with open('scratch/po4_current_tab.png', 'wb') as f:
    f.write(base64.b64decode(m['result']['data']))
print("Screenshot saved to scratch/po4_current_tab.png")
ws.close()
