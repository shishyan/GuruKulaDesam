import urllib.request
import json
import time
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# Click "New project"
js_new_proj = """
(() => {
    const btn = Array.from(document.querySelectorAll('button, [role="button"], a')).find(b => b.innerText.includes('New project'));
    if (btn) {
        btn.click();
        return 'Clicked New project';
    }
    return 'New project button not found';
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_new_proj, 'returnByValue': True}}))
print(json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
