import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    const dls = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
    return dls.map((b, idx) => ({
        idx,
        text: (b.innerText || '').trim(),
        aria: b.getAttribute('aria-label') || '',
        visible: b.offsetParent !== null,
        cls: b.className
    }));
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', []), indent=2))
ws.close()
