import sys, urllib.request, json, time, websocket, os, base64

vid = "HPP3IG7DWRc"
srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
assert os.path.exists(srt_file), f"SRT not found: {srt_file}"
print(f"Uploading and publishing {srt_file} for {vid}...")

res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
tabs = json.loads(res.decode('utf-8'))
page = [t for t in tabs if t.get('type') == 'page'][0]
ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=30)

events = []
msg_id = 0

def call(method, params=None):
    global msg_id, events
    msg_id += 1
    i = msg_id
    ws.send(json.dumps({'id': i, 'method': method, 'params': params or {}}))
    while True:
        m = json.loads(ws.recv())
        if 'id' in m:
            if m['id'] == i:
                return m.get('result', {})
        else:
            events.append(m)

def click(x, y):
    call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    time.sleep(0.1)
    call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

def screenshot(path):
    ss = call("Page.captureScreenshot")
    if "data" in ss:
        with open(path, "wb") as f:
            f.write(base64.b64decode(ss["data"]))
        print(f"Saved screenshot: {path}")

call('Page.enable')
call('DOM.enable')
call('Page.setInterceptFileChooserDialog', {'enabled': True})

# Step A: Check if "Upload file" option is present in the initial modal
find_upload_file_option = """(() => {
    let all = Array.from(document.querySelectorAll('*'));
    let el = all.find(e => {
        let t = (e.innerText || '').trim();
        return t === 'Upload file' && e.children.length === 0;
    });
    if (el) {
        let parent = el.closest('button, ytcp-button, [role="button"], tr, div[class*="item"], div[class*="row"]') || el;
        let r = parent.getBoundingClientRect();
        return { found: true, x: r.x + r.width/2, y: r.y + r.height/2, tag: parent.tagName };
    }
    return { found: false };
})()"""
opt_info = call("Runtime.evaluate", {"expression": find_upload_file_option, "returnByValue": True}).get("result", {}).get("value", {})
print("Upload file option info:", opt_info)

if opt_info.get("found"):
    print(f"Clicking Upload file option at ({opt_info['x']}, {opt_info['y']})...")
    click(opt_info['x'], opt_info['y'])
    time.sleep(2)

# Step B: Check for Continue button
find_continue = """(() => {
    let btns = Array.from(document.querySelectorAll('ytcp-button, button'));
    let b = btns.find(e => (e.innerText || '').trim() === 'Continue' || (e.innerText || '').trim() === 'CONTINUE');
    if (b) {
        let r = b.getBoundingClientRect();
        return { found: true, x: r.x + r.width/2, y: r.y + r.height/2 };
    }
    return { found: false };
})()"""

c_info = {}
for _ in range(5):
    c_info = call("Runtime.evaluate", {"expression": find_continue, "returnByValue": True}).get("result", {}).get("value", {})
    print("Continue button info:", c_info)
    if c_info.get("found"):
        break
    time.sleep(1)

if c_info.get("found"):
    cx, cy = c_info["x"], c_info["y"]
    print(f"Dispatching mouse click at Continue ({cx}, {cy})...")
    click(cx, cy)
else:
    print("Continue not found, taking debug screenshot...")
    screenshot("scratch/hpp_upload_debug.png")

# Step C: Intercept file chooser
print("Waiting for Page.fileChooserOpened...")
backend_node_id = None
for ev in events:
    if ev.get('method') == 'Page.fileChooserOpened':
        backend_node_id = ev.get('params', {}).get('backendNodeId')
        print("Found in earlier events! backendNodeId:", backend_node_id)
        break

if not backend_node_id:
    t_end = time.time() + 10
    while time.time() < t_end:
        try:
            m = json.loads(ws.recv())
            if m.get('method') == 'Page.fileChooserOpened':
                backend_node_id = m.get('params', {}).get('backendNodeId')
                print("Captured Page.fileChooserOpened! backendNodeId:", backend_node_id)
                break
        except Exception as e:
            pass

assert backend_node_id, "Failed to intercept file chooser"
print(f"Setting SRT file: {srt_file}...")
call("DOM.setFileInputFiles", {
    "files": [srt_file],
    "backendNodeId": backend_node_id
})

node_obj = call("DOM.resolveNode", {"backendNodeId": backend_node_id})
obj_id = node_obj.get("object", {}).get("objectId")
if obj_id:
    call("Runtime.callFunctionOn", {
        "objectId": obj_id,
        "functionDeclaration": """function() {
            this.dispatchEvent(new Event('input', { bubbles: true }));
            this.dispatchEvent(new Event('change', { bubbles: true }));
        }"""
    })

print("Waiting 8s for subtitle editor to parse...")
time.sleep(8)

# Step D: Click Publish
find_pub = """(() => {
    let pub = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Publish' || (b.innerText || '').trim() === 'PUBLISH');
    if (pub) {
        let r = pub.getBoundingClientRect();
        return {found: true, disabled: pub.hasAttribute('disabled'), x: r.x + r.width/2, y: r.y + r.height/2};
    }
    return {found: false};
})()"""
pub_info = call('Runtime.evaluate', {'expression': find_pub, 'returnByValue': True}).get('result', {}).get('value', {})
print(f"Publish button status: {pub_info}")

if pub_info.get("found") and not pub_info.get("disabled"):
    px, py = pub_info["x"], pub_info["y"]
    print(f"Clicking Publish at ({px}, {py})...")
    click(px, py)
else:
    print("Clicking fallback publish coordinate (1496.6, 80)...")
    click(1496.6, 80)
    
time.sleep(6)
screenshot(f"scratch/{vid}_published_toast.png")
print(f"COMPLETED SUBTITLE PUBLISH FOR {vid}!")

ws.close()
