import urllib.request
import json
import websocket
import time

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
    const tune = btns.find(b => (b.innerText || '').includes('tune') || (b.getAttribute('aria-label') || '').toLowerCase().includes('settings'));
    if (tune) {
        tune.click();
        return { clicked: true, text: tune.innerText };
    }
    return { clicked: false };
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print('Tune click:', json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
