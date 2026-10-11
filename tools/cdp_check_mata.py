import websocket, json, time, base64

ws = websocket.create_connection('ws://127.0.0.1:9225/devtools/page/080D45A1127A8B9C759EB2B714DBB3D7', timeout=10)

print("Querying current Mata6vtnrjQ translations page...")
time.sleep(2)

# Screenshot
ws.send(json.dumps({'id': 2, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
res = json.loads(ws.recv())
b64 = res.get('result', {}).get('data')
if b64:
    with open('scratch/mata_translations_check.png', 'wb') as f:
        f.write(base64.b64decode(b64))
    print("Saved scratch/mata_translations_check.png")

# Query buttons
expr = '''(() => {
    let elms = Array.from(document.querySelectorAll('*'));
    let res = [];
    for (let el of elms) {
        let t = (el.innerText || '').trim();
        if (t === 'Edit subtitles' || t === 'Upload manual' || t === 'Add language') {
            let r = el.getBoundingClientRect();
            res.push({ tag: el.tagName, id: el.id, text: t, x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2), w: Math.round(r.width), h: Math.round(r.height), disabled: el.hasAttribute('disabled') || el.getAttribute('aria-disabled') === 'true' });
        }
    }
    return res;
})()'''
ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
btns = json.loads(ws.recv()).get('result', {}).get('result', {}).get('value')
print("Buttons found:")
for b in btns:
    print(" ", b)

ws.close()
