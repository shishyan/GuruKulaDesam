import urllib.request, json, time, websocket, sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [t for t in tabs if 'studio.youtube.com' in t.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q'}}))
ws.recv()
time.sleep(3)

expr = """
(() => {
    let clickable = Array.from(document.querySelectorAll('a, button, [role="button"]'));
    return clickable.map(el => ({tag: el.tagName, text: el.innerText.trim(), href: el.href || null}));
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
res = json.loads(ws.recv())
data = res.get('result', {}).get('result', {}).get('value', [])
print("Clickable elements on error page:")
for item in data:
    print(" ", item)

ws.close()

