import urllib.request
import json
import websocket
import time

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

# Dispatch Enter key event directly to ProseMirror
press_enter = """
(() => {
    const ed = document.querySelector('div.ProseMirror');
    if (!ed) return 'no_ed';
    ed.focus();
    const event = new KeyboardEvent('keydown', {
        key: 'Enter',
        code: 'Enter',
        keyCode: 13,
        which: 13,
        bubbles: true,
        cancelable: true
    });
    ed.dispatchEvent(event);
    return 'dispatched_enter';
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': press_enter, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Dispatch result:", res.get('result', {}).get('result', {}).get('value'))

time.sleep(3)

ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '(() => ({ hasStop: document.body.innerText.includes("Stop"), snippet: document.body.innerText.slice(-250) }))()', 'returnByValue': True}}))
res2 = json.loads(ws.recv())
print("Status:", res2.get('result', {}).get('result', {}).get('value'))
ws.close()
