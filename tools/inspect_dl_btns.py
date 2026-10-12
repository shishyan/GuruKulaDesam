import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
    return btns.map((b, idx) => ({
        idx: idx,
        text: (b.innerText || '').trim(),
        aria: b.getAttribute('aria-label'),
        top: b.getBoundingClientRect().top
    })).filter(b => b.text.toLowerCase().includes('download') || (b.aria && b.aria.toLowerCase().includes('download')));
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print('Buttons:', json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
