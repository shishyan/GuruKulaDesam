import urllib.request, json, websocket, time, base64

res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
tabs = json.loads(res.decode('utf-8'))
page = [t for t in tabs if t.get('type') == 'page'][0]
ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=15)

msg_id = 1
def call(method, params={}):
    global msg_id
    msg_id += 1
    req = {'id': msg_id, 'method': method, 'params': params}
    ws.send(json.dumps(req))
    while True:
        m = json.loads(ws.recv())
        if m.get('id') == msg_id:
            return m.get('result', {})

def click(x, y):
    call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    time.sleep(0.1)
    call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

js = """(() => {
    let btns = Array.from(document.querySelectorAll('ytcp-button, button'));
    let pub = btns.find(b => (b.innerText || '').trim() === 'Publish' || (b.innerText || '').trim() === 'PUBLISH');
    if (pub) {
        let r = pub.getBoundingClientRect();
        return { found: true, x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height };
    }
    return { found: false };
})()"""
r = call('Runtime.evaluate', {'expression': js, 'returnByValue': True}).get('result', {}).get('value', {})
print("Publish button info:", r)

if r.get('found'):
    px, py = r['x'], r['y']
    print(f"Clicking Publish at ({px}, {py})...")
    click(px, py)
    time.sleep(5)
    ss = call('Page.captureScreenshot')
    with open('scratch/PO4_publish_confirmed.png', 'wb') as f:
        f.write(base64.b64decode(ss['data']))
    print("Saved scratch/PO4_publish_confirmed.png!")

ws.close()
