import urllib.request
import json
import websocket
import base64

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

ws.send(json.dumps({'id': 1, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
res = json.loads(ws.recv())
img_b64 = res.get('result', {}).get('data', '')
with open("production/flow_current_state.png", "wb") as f:
    f.write(base64.b64decode(img_b64))

js = """
(() => {
    const text = document.body ? document.body.innerText : '';
    const cards = Array.from(document.querySelectorAll('video, img')).length;
    return {
        hasStop: text.includes('Stop'),
        textSnippet: text.slice(-400)
    };
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print("State:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
