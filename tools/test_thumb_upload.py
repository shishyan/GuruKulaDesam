import urllib.request, json, time, websocket, os, base64

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

call('DOM.enable')
doc = call('DOM.getDocument', {'depth': -1})
root_id = doc.get('root', {}).get('nodeId')

# Find #file-loader
loader = call('DOM.querySelector', {'nodeId': root_id, 'selector': '#file-loader'})
node_id = loader.get('nodeId')
print('Loader nodeId:', node_id)

thumb_path = os.path.abspath('production/thumbnails/mG9IzlD9vmI.png')
print(f'Thumbnail path: {thumb_path} (exists: {os.path.exists(thumb_path)})')

if node_id:
    call('DOM.setFileInputFiles', {'files': [thumb_path], 'nodeId': node_id})
    print('Called DOM.setFileInputFiles for thumbnail!')
    
    # Dispatch change
    node_obj = call('DOM.resolveNode', {'nodeId': node_id})
    obj_id = node_obj.get('object', {}).get('objectId')
    if obj_id:
        call('Runtime.callFunctionOn', {
            'objectId': obj_id,
            'functionDeclaration': """function() {
                this.dispatchEvent(new Event('change', { bubbles: true }));
            }"""
        })
        print('Dispatched change event on thumbnail input!')

time.sleep(3)
ss = call('Page.captureScreenshot')
with open('scratch/thumb_uploaded_test.png', 'wb') as f:
    f.write(base64.b64decode(ss['data']))
print('Saved scratch/thumb_uploaded_test.png')
ws.close()
