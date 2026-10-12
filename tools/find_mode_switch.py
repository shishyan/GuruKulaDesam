import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    const els = Array.from(document.querySelectorAll('button, [role="button"], [role="tab"], mat-button-toggle, span, div.button, .mat-mdc-menu-item'));
    return els.map((el, i) => ({
        i,
        tag: el.tagName,
        cls: el.className,
        text: (el.innerText || '').trim().replace(/\\n/g, ' '),
        aria: el.getAttribute('aria-label') || ''
    })).filter(x => /agent|manual|switch|standard|chat|prompt/i.test(x.text) || /agent|manual|switch|standard|chat|prompt/i.test(x.aria));
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', []), indent=2))
ws.close()
