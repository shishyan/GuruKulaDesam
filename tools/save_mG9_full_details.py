import urllib.request, json, time, websocket, os, base64

vid = "mG9IzlD9vmI"
desc_path = os.path.abspath(f"production/descriptions/{vid}.txt")
thumb_path = os.path.abspath(f"production/thumbnails/{vid}.png")

with open(desc_path, "r", encoding="utf-8") as f:
    description_text = f.read()

res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
tabs = json.loads(res.decode('utf-8'))
page = [t for t in tabs if t.get('type') == 'page'][0]
ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=20)

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

print("Injecting description into #description-textarea #textbox...")
inject_js = f"""(() => {{
    const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
    if (!descBox) return {{ success: false, error: 'no desc box found' }};
    descBox.focus();
    document.execCommand('selectAll', false, null);
    document.execCommand('insertText', false, {json.dumps(description_text)});
    descBox.dispatchEvent(new Event('input', {{ bubbles: true }}));
    descBox.dispatchEvent(new Event('change', {{ bubbles: true }}));
    return {{ success: true, length: descBox.innerText.length }};
}})()"""
res = call('Runtime.evaluate', {'expression': inject_js, 'returnByValue': True}).get('result', {}).get('value', {})
print("Description injected:", res)
time.sleep(2)

# Ensure thumbnail uploaded
call('DOM.enable')
doc = call('DOM.getDocument', {'depth': -1})
root_id = doc.get('root', {}).get('nodeId')
loader = call('DOM.querySelector', {'nodeId': root_id, 'selector': '#file-loader'})
node_id = loader.get('nodeId')
if node_id and os.path.exists(thumb_path):
    call('DOM.setFileInputFiles', {'files': [thumb_path], 'nodeId': node_id})
    node_obj = call('DOM.resolveNode', {'nodeId': node_id})
    obj_id = node_obj.get('object', {}).get('objectId')
    if obj_id:
        call('Runtime.callFunctionOn', {
            'objectId': obj_id,
            'functionDeclaration': """function() {
                this.dispatchEvent(new Event('change', { bubbles: true }));
            }"""
        })
    print("Thumbnail file set and event dispatched!")

time.sleep(2)

# Click Save button
print("Clicking Save button...")
click_save = """(() => {
    let btn = document.querySelector('#save, [id="save"], ytcp-button#save-button, ytcp-button#save');
    if (btn && !btn.hasAttribute('disabled')) {
        let r = btn.getBoundingClientRect();
        btn.click();
        return { clicked: true, x: r.x + r.width/2, y: r.y + r.height/2 };
    }
    return { clicked: false, found: !!btn, disabled: btn ? btn.hasAttribute('disabled') : null };
})()"""
s_info = call('Runtime.evaluate', {'expression': click_save, 'returnByValue': True}).get('result', {}).get('value', {})
print("Save button click result:", s_info)

time.sleep(6)

ss = call('Page.captureScreenshot')
with open(f'scratch/{vid}_details_saved.png', 'wb') as f:
    f.write(base64.b64decode(ss['data']))
print(f"Saved scratch/{vid}_details_saved.png")

ws.close()
