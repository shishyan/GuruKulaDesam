import urllib.request, json, websocket, time, base64

res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
tabs = json.loads(res.decode('utf-8'))
page = [t for t in tabs if t.get('type') == 'page'][0]
ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=10)

def call(method, params={}):
    req = {'id': 1, 'method': method, 'params': params}
    ws.send(json.dumps(req))
    m = json.loads(ws.recv())
    return m.get('result', {})

ss = call('Page.captureScreenshot')
with open('scratch/kls_current_check.png', 'wb') as f:
    f.write(base64.b64decode(ss['data']))

js = """(() => {
    let items = Array.from(document.querySelectorAll('#text-input, ytcp-form-textarea, .line-text, .cue-text, [role="textbox"], .timing-row'));
    return items.slice(0, 10).map(l => l.innerText || l.value);
})()"""
info = call('Runtime.evaluate', {'expression': js, 'returnByValue': True}).get('result', {}).get('value', {})
print("Editor info:", info)
ws.close()
