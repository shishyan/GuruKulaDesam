import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const avatar = document.querySelector('button[aria-label*="Google Account" i], button[aria-label*="Account details" i]');
    return avatar ? avatar.getAttribute('aria-label') : 'No avatar found';
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print("Current Flow Account:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
