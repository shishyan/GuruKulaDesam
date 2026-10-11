import urllib.request, json, sys
import websocket

sys.stdout.reconfigure(encoding='utf-8')

# 1. Find tab
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
target = None
for t in tabs:
    if 'studio.youtube.com' in t.get('url', ''):
        target = t
        break

if not target:
    print("No studio.youtube.com tab found!")
    sys.exit(1)

print(f"Target found: {target['title']} | {target['url']}")
ws_url = target['webSocketDebuggerUrl']

# 2. Connect via websocket
ws = websocket.create_connection(ws_url, timeout=5, suppress_origin=True)

# 3. Evaluate expression
msg = {
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "JSON.stringify({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 500)})"
    }
}
ws.send(json.dumps(msg))
res = json.loads(ws.recv())
data = json.loads(res.get('result', {}).get('result', {}).get('value', '{}'))
print("=== TAB EVALUATION ===")
print("URL:", data.get('url'))
print("Title:", data.get('title'))
print("Body Text Preview:\n", data.get('text'))

ws.close()
