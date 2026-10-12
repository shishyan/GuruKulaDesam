import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const closeBtns = Array.from(document.querySelectorAll('button, [role="button"]'))
        .filter(b => (b.innerText || '').trim() === 'close' || (b.getAttribute('aria-label') || '').toLowerCase().includes('close'));
    if (closeBtns.length > 0) {
        closeBtns[0].click();
        return { closed: true };
    }
    return { closed: false };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print('Close sidebar:', json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
