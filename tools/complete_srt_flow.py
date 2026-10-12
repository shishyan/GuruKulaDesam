import sys, urllib.request, json, time, websocket, os, base64

vid = sys.argv[1] if len(sys.argv) > 1 else "PO4U3nRv6o0"
srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
assert os.path.exists(srt_file), f"SRT not found: {srt_file}"
print(f"=== Complete SRT Publish Flow for {vid} ===")
print(f"Target SRT: {srt_file}")

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json').read())
page = [t for t in tabs if t.get('type') == 'page' and 'studio.youtube.com' in t.get('url', '')][0]
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

def click(x, y):
    call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    time.sleep(0.1)
    call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

call('Page.enable')
call('DOM.enable')
call('Page.setInterceptFileChooserDialog', {'enabled': True})

# Step 1: Open editor modal if not already open
check_modal = """(() => {
    let editor = document.querySelector('#more-actions-menu, [aria-label="Options"]');
    let continueBtn = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Continue');
    let editBtn = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Edit subtitles');
    let uploadBtn = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Upload manual');
    return {
        hasEditor: !!editor,
        hasContinue: !!continueBtn,
        hasEditBtn: !!editBtn,
        hasUploadBtn: !!uploadBtn
    };
})()"""
m_info = call("Runtime.evaluate", {"expression": check_modal, "returnByValue": True}).get("result", {}).get("value", {})
print("Initial page state:", m_info)

if not m_info.get("hasEditor") and not m_info.get("hasContinue"):
    if m_info.get("hasEditBtn"):
        print("Clicking 'Edit subtitles' button...")
        call("Runtime.evaluate", {"expression": """(() => {
            let b = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Edit subtitles');
            if (b) b.click();
        })()"""})
        time.sleep(4)
    elif m_info.get("hasUploadBtn"):
        print("Clicking 'Upload manual' button...")
        call("Runtime.evaluate", {"expression": """(() => {
            let b = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Upload manual');
            if (b) b.click();
        })()"""})
        time.sleep(3)

# Check again
m_info = call("Runtime.evaluate", {"expression": check_modal, "returnByValue": True}).get("result", {}).get("value", {})
print("Post-click state:", m_info)

if not m_info.get("hasContinue"):
    print("Clicking Options menu at (919.5, 142.0)...")
    click(919.5, 142.0)
    time.sleep(1.5)

    print("Clicking 'Upload file' menu item...")
    call("Runtime.evaluate", {
        "expression": """(() => {
            let items = Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-menu-service-item, .ytcp-menu-service-item'));
            let target = items.find(e => e.innerText.includes('Upload file'));
            if (target) target.click();
        })()"""
    })
    time.sleep(2)

# Click Continue
print("Finding Continue button...")
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
print("Continue info:", c_info)
if c_info.get("found"):
    cx, cy = c_info["x"], c_info["y"]
    print(f"Dispatching mouse click on Continue at ({cx}, {cy})...")
    click(cx, cy)
else:
    print("Clicking default coordinates (1083.8, 544.0)...")
    click(1083.8, 544.0)

# Intercept file chooser
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

print("Waiting 8s for Subtitle Editor to process SRT...")
time.sleep(8)

# Click Publish
find_pub = """(() => {
    let pub = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Publish' || (b.innerText || '').trim() === 'PUBLISH');
    if (pub) {
        let r = pub.getBoundingClientRect();
        return {found: true, disabled: pub.hasAttribute('disabled'), x: r.x + r.width/2, y: r.y + r.height/2};
    }
    return {found: false};
})()"""
pub_info = call('Runtime.evaluate', {'expression': find_pub, 'returnByValue': True}).get('result', {}).get('value', {})
print("Publish button status:", pub_info)

if pub_info.get("found") and not pub_info.get("disabled"):
    px, py = pub_info["x"], pub_info["y"]
    print(f"Clicking Publish button at ({px}, {py})...")
    click(px, py)
    print("Waiting 6s for publish confirmation...")
    time.sleep(6)
    
    ss = call("Page.captureScreenshot")
    with open(f"scratch/{vid}_published_toast.png", "wb") as f:
        f.write(base64.b64decode(ss['data']))
    print(f"Saved scratch/{vid}_published_toast.png!")

ws.close()
print(f"SUCCESS: SUBTITLES UPLOADED AND PUBLISHED FOR {vid}!")
