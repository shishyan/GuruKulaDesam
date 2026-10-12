import urllib.request
import json
import websocket
import base64
import time

def snap():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    ws.send(json.dumps({'id': 1, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
    res = json.loads(ws.recv())
    img_b64 = res.get('result', {}).get('data', '')

    artifact_path = 'production/flow_live_state.png'
    with open(artifact_path, 'wb') as f:
        f.write(base64.b64decode(img_b64))

    ws.send(json.dumps({
        'id': 2,
        'method': 'Runtime.evaluate',
        'params': {
            'expression': '(() => ({ text: document.body.innerText.slice(0, 500), hasStop: document.body.innerText.includes("Stop"), hasDialog: !!document.querySelector(".cdk-overlay-backdrop") }))()',
            'returnByValue': True
        }
    }))
    res2 = json.loads(ws.recv())
    val = res2.get('result', {}).get('result', {}).get('value', {})
    print("Has Stop:", val.get('hasStop'), "Has Backdrop Dialog:", val.get('hasDialog'))
    ws.close()

if __name__ == '__main__':
    snap()
