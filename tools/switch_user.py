import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# 1. Switch to nagaraj957@gmail.com
# Google account URLs often use /u/1 or /u/0 or authuser query param
js_switch = """
(() => {
    // Navigate directly with authuser parameter
    window.location.href = 'https://flow.google.com/?authuser=nagaraj957@gmail.com';
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_switch}}))
print("Navigated:", ws.recv())
ws.close()
