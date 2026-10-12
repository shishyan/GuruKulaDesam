import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    const chip = document.querySelector('button.agent-mode-chip');
    if (chip) {
        chip.click();
        return { clicked: true, prevClass: chip.className };
    }
    return { clicked: false };
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Click agent chip result:", res.get('result', {}).get('result', {}).get('value'))
ws.close()
