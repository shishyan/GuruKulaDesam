import urllib.request
import json
import websocket
import base64

def snap():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    ws.send(json.dumps({'id': 1, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
    res = json.loads(ws.recv())
    img_b64 = res.get('result', {}).get('data', '')

    artifact_path = 'C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_live_progress.png'
    with open(artifact_path, 'wb') as f:
        f.write(base64.b64decode(img_b64))

    ws.send(json.dumps({
        'id': 2,
        'method': 'Runtime.evaluate',
        'params': {
            'expression': '(() => ({ text: document.body.innerText.slice(0, 1000) }))()',
            'returnByValue': True
        }
    }))
    res2 = json.loads(ws.recv())
    print("Live text:")
    print(res2.get('result', {}).get('result', {}).get('value', {}).get('text', ''))
    ws.close()

if __name__ == '__main__':
    snap()
