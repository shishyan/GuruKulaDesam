import websocket, json, time, base64, sys

ws = websocket.create_connection('ws://127.0.0.1:9225/devtools/page/080D45A1127A8B9C759EB2B714DBB3D7', timeout=10)

# Click at 337, 245
ws.send(json.dumps({'id': 1, 'method': 'Input.dispatchMouseEvent', 'params': {'type': 'mousePressed', 'x': 337, 'y': 245, 'button': 'left', 'clickCount': 1}}))
ws.recv()
ws.send(json.dumps({'id': 2, 'method': 'Input.dispatchMouseEvent', 'params': {'type': 'mouseReleased', 'x': 337, 'y': 245, 'button': 'left', 'clickCount': 1}}))
ws.recv()

print('Clicked Edit subtitles! Waiting 4s...')
time.sleep(4)

# Take screenshot
ws.send(json.dumps({'id': 3, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
res = json.loads(ws.recv())
b64 = res.get('result', {}).get('data')
if b64:
    with open('scratch/after_cdp_edit_click.png', 'wb') as f:
        f.write(base64.b64decode(b64))
    print('Saved scratch/after_cdp_edit_click.png')

# Check title and URL
ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.title + " | " + window.location.href', 'returnByValue': True}}))
print('Page state:', json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
