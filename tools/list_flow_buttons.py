import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    return Array.from(document.querySelectorAll('button, [role="button"]')).map(b => ({
        tag: b.tagName,
        text: (b.innerText || '').trim().replace(/\\n/g, ' '),
        aria: b.getAttribute('aria-label') || '',
        cls: b.className
    })).filter(b => b.text || b.aria);
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
btns = res.get('result', {}).get('result', {}).get('value', [])
print(f"Total buttons found: {len(btns)}")
for i, b in enumerate(btns):
    txt = b['text'].lower()
    aria = b['aria'].lower()
    if any(k in txt or k in aria for k in ['start', 'gen', 'arrow', 'submit', 'download', 'stop', 'play', 'keyboard_return']):
        print(f"[{i}] text='{b['text']}', aria='{b['aria']}', cls='{b['cls']}'")
ws.close()
