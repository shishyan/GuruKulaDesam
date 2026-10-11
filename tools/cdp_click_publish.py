import websocket, json, time, base64

ws = websocket.create_connection('ws://127.0.0.1:9225/devtools/page/080D45A1127A8B9C759EB2B714DBB3D7', timeout=10)

print("Dispatching click to Publish button at (1497, 80)...")
ws.send(json.dumps({'id': 1, 'method': 'Input.dispatchMouseEvent', 'params': {'type': 'mousePressed', 'x': 1497, 'y': 80, 'button': 'left', 'clickCount': 1}}))
ws.recv()
ws.send(json.dumps({'id': 2, 'method': 'Input.dispatchMouseEvent', 'params': {'type': 'mouseReleased', 'x': 1497, 'y': 80, 'button': 'left', 'clickCount': 1}}))
ws.recv()

print("Clicked Publish! Waiting 5s...")
time.sleep(5)

# Take confirmation screenshot
ws.send(json.dumps({'id': 3, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
res = json.loads(ws.recv())
b64 = res.get('result', {}).get('data')
if b64:
    with open('scratch/kft_subtitles_published_live.png', 'wb') as f:
        f.write(base64.b64decode(b64))
    print("Saved scratch/kft_subtitles_published_live.png")

ws.close()
print("Done!")
