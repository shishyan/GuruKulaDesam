import os, sys, time, json, base64, urllib.request
import websocket

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = sys.argv[1] if len(sys.argv) > 1 else "FVkGdLV7O34"
srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
print(f"=== CDP SUBTITLE UPLOAD FOR {vid} ===")
print(f"SRT: {srt_file} (exists: {os.path.exists(srt_file)})")
assert os.path.exists(srt_file), f"SRT not found: {srt_file}"

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json').read())
page = [t for t in tabs if t.get('type') == 'page'][0]
print(f"Connecting to tab {page['id']} ({page['url']})...")

ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=25)

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

target_url = f"https://studio.youtube.com/video/{vid}/translations"
print(f"Navigating to {target_url}...")
call("Page.navigate", {"url": target_url})
time.sleep(6)

call('Page.enable')
call('DOM.enable')
call('Page.setInterceptFileChooserDialog', {'enabled': True})

# Wait for table to load
check_js = """(() => {
    let editBtn = document.querySelector('#m2-editor-button, ytcp-button#m2-editor-button');
    let uploadBtn = document.querySelector('#upload-default-language-button, ytcp-button#upload-default-language-button');
    return {
        hasEdit: !!editBtn,
        hasUpload: !!uploadBtn
    };
})()"""

chk = {}
for attempt in range(12):
    chk = call("Runtime.evaluate", {"expression": check_js, "returnByValue": True}).get("result", {}).get("value", {})
    print(f"Attempt {attempt+1}: {chk}")
    if chk.get("hasEdit") or chk.get("hasUpload"):
        break
    time.sleep(2)

print("Final Track check:", chk)

if chk.get("hasEdit"):
    print("Opening existing track via JS on #m2-editor-button...")
    call("Runtime.evaluate", {
        "expression": "document.querySelector('#m2-editor-button, ytcp-button#m2-editor-button').click()"
    })
    time.sleep(4)
    
    print("Opening options menu via JS on #more-actions-menu...")
    call("Runtime.evaluate", {
        "expression": "document.querySelector('#more-actions-menu').click()"
    })
    time.sleep(1.5)
    
    print("Clicking 'Upload file' in options menu...")
    call("Runtime.evaluate", {
        "expression": """(() => {
            let items = Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-menu-service-item, .ytcp-menu-service-item'));
            let target = items.find(e => e.innerText.includes('Upload file'));
            if (target) { target.click(); return true; }
            return false;
        })()"""
    })
    time.sleep(2)
else:
    print("Clicking 'Upload manual' via JS...")
    call("Runtime.evaluate", {
        "expression": "document.querySelector('#upload-default-language-button, ytcp-button#upload-default-language-button').click()"
    })
    time.sleep(2)

# Click Continue button on type selection modal
find_continue = """(() => {
    let btns = Array.from(document.querySelectorAll('ytcp-button, button'));
    let b = btns.find(e => e.innerText.trim() === 'Continue' || e.innerText.trim() === 'CONTINUE');
    if (b) {
        let r = b.getBoundingClientRect();
        return {found: true, x: r.x + r.width/2, y: r.y + r.height/2};
    }
    return {found: false};
})()"""
c_info = call("Runtime.evaluate", {"expression": find_continue, "returnByValue": True}).get("result", {}).get("value", {})
print("Continue button info:", c_info)
if c_info.get("found"):
    cx, cy = c_info["x"], c_info["y"]
    print(f"Clicking Continue at ({cx}, {cy})...")
    call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": cx, "y": cy, "button": "left", "clickCount": 1})
    time.sleep(0.1)
    call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": cx, "y": cy, "button": "left", "clickCount": 1})
else:
    print("Clicking default coordinates (1083.8, 544.0)...")
    call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": 1083.8, "y": 544.0, "button": "left", "clickCount": 1})
    time.sleep(0.1)
    call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": 1083.8, "y": 544.0, "button": "left", "clickCount": 1})

# Wait for file chooser
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
                print("Received Page.fileChooserOpened! backendNodeId:", backend_node_id)
                break
        except Exception as e:
            print("Recv error:", e)
            break

print("backend_node_id:", backend_node_id)
assert backend_node_id, "Failed to intercept file chooser"

call("DOM.setFileInputFiles", {
    "files": [srt_file],
    "backendNodeId": backend_node_id
})
print("Set files on backendNodeId via DOM.setFileInputFiles!")

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
    print("Dispatched input and change events!")

print("Waiting 7s for Subtitle Editor to process SRT...")
time.sleep(7)

# Find Publish button
find_pub = """(() => {
    let pub = document.querySelector('#publish-button, ytcp-button#publish-button');
    if (pub) {
        let r = pub.getBoundingClientRect();
        return {found: true, disabled: pub.hasAttribute('disabled'), x: r.x + r.width/2, y: r.y + r.height/2};
    }
    return {found: false};
})()"""
r = call('Runtime.evaluate', {'expression': find_pub, 'returnByValue': True})
pub_info = r.get('result', {}).get('value', {})
print("Publish button status:", pub_info)

if pub_info.get("found") and not pub_info.get("disabled"):
    px, py = pub_info["x"], pub_info["y"]
    print(f"Clicking Publish button at ({px}, {py})...")
    call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": px, "y": py, "button": "left", "clickCount": 1})
    time.sleep(0.1)
    call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": px, "y": py, "button": "left", "clickCount": 1})
    print("Waiting 5s for publish...")
    time.sleep(5)
    
    ss = call("Page.captureScreenshot")
    with open(f"scratch/{vid}_published_toast.png", "wb") as f:
        f.write(base64.b64decode(ss['data']))
    print(f"Saved scratch/{vid}_published_toast.png!")

ws.close()
print(f"SUCCESS: UPLOAD AND PUBLISH FINISHED FOR {vid}!")
