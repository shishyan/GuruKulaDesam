"""
Automated YouTube Studio Video Publisher Pipeline.
Handles Description Update and Acoustic SRT Upload & Publish via Chrome port 9225.
"""

import os, sys, time, json, base64, urllib.request
import websocket

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

def get_page_ws():
    res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
    tabs = json.loads(res.decode('utf-8'))
    for t in tabs:
        if t.get('type') == 'page':
            return t.get('webSocketDebuggerUrl'), t.get('url')
    return None, None

class CDPClient:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=15)
        
    def call(self, method, params={}):
        msg_id = int(time.time() * 1000) % 1000000
        req = {"id": msg_id, "method": method, "params": params}
        self.ws.send(json.dumps(req))
        while True:
            raw = self.ws.recv()
            data = json.loads(raw)
            if data.get("id") == msg_id:
                return data.get("result", {})
                
    def click(self, x, y):
        self.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        time.sleep(0.1)
        self.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})
        
    def screenshot(self, path):
        ss = self.call("Page.captureScreenshot")
        if "data" in ss:
            with open(path, "wb") as f:
                f.write(base64.b64decode(ss["data"]))
            print(f"Saved screenshot: {path}")
            
    def close(self):
        try:
            self.ws.close()
        except:
            pass

def update_description_in_studio(vid, new_description):
    ws_url, _ = get_page_ws()
    client = CDPClient(ws_url)
    
    target_url = f"https://studio.youtube.com/video/{vid}/edit"
    print(f"[Studio] Navigating to {target_url}...")
    client.call("Page.navigate", {"url": target_url})
    time.sleep(6)
    
    # Inject text into description box
    inject_js = f"""(() => {{
        const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
        if (!descBox) return {{ success: false, error: 'no desc box found' }};
        descBox.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('insertText', false, {json.dumps(new_description)});
        descBox.dispatchEvent(new Event('input', {{ bubbles: true }}));
        descBox.dispatchEvent(new Event('change', {{ bubbles: true }}));
        
        const saveBtn = document.querySelector('#save-button, ytcp-button#save-button');
        return {{
            success: true,
            len: descBox.innerText.length
        }};
    }})()"""
    res = client.call("Runtime.evaluate", {"expression": inject_js, "returnByValue": True})
    print("[Studio] Description injected:", res.get("result", {}).get("value"))
    time.sleep(2)
    
    # Click Save button at (1272.8, 99)
    print("[Studio] Clicking Save button...")
    client.click(1272.8, 99)
    time.sleep(5)
    
    client.screenshot(f"scratch/{vid}_desc_saved.png")
    client.close()
    print(f"[Studio] Description updated and saved for {vid}!")

def upload_subtitles_in_studio(vid, srt_file):
    assert os.path.exists(srt_file), f"SRT not found: {srt_file}"
    ws_url, _ = get_page_ws()
    client = CDPClient(ws_url)
    
    target_url = f"https://studio.youtube.com/video/{vid}/translations"
    print(f"[Studio] Navigating to {target_url}...")
    client.call("Page.navigate", {"url": target_url})
    time.sleep(6)
    
    client.call("Page.enable")
    client.call("DOM.enable")
    client.call("Page.setInterceptFileChooserDialog", {"enabled": True})
    
    # Check if 'Edit subtitles' exists or 'Upload manual'
    check_js = """(() => {
        let editBtn = document.querySelector('#m2-editor-button, ytcp-button#m2-editor-button');
        let uploadBtn = document.querySelector('#upload-default-language-button, ytcp-button#upload-default-language-button');
        return {
            hasEdit: !!editBtn,
            hasUpload: !!uploadBtn
        };
    })()"""
    chk = client.call("Runtime.evaluate", {"expression": check_js, "returnByValue": True}).get("result", {}).get("value", {})
    print("[Studio] Track check:", chk)
    
    if chk.get("hasEdit"):
        print("[Studio] Opening existing track via 'Edit subtitles'...")
        client.click(336.7, 245.0)
        time.sleep(4)
        
        print("[Studio] Clicking 3-dots Options menu...")
        client.click(919.5, 142.0)
        time.sleep(1.5)
        
        print("[Studio] Clicking 'Upload file' in menu...")
        client.click(995.6, 226.0)
        time.sleep(2)
        
        print("[Studio] Clicking 'Continue'...")
        client.click(1083.9, 544.0)
    else:
        print("[Studio] Clicking 'Upload manual'...")
        client.click(466.4, 245.0)
        time.sleep(2)
        
        print("[Studio] Clicking 'Continue'...")
        client.click(1083.9, 544.0)
        
    # Intercept file chooser
    print("[Studio] Waiting for Page.fileChooserOpened...")
    client.ws.settimeout(10)
    backend_node_id = None
    t_end = time.time() + 10
    while time.time() < t_end:
        try:
            raw = client.ws.recv()
            data = json.loads(raw)
            if data.get("method") == "Page.fileChooserOpened":
                backend_node_id = data.get("params", {}).get("backendNodeId")
                print("[Studio] Intercepted file chooser! backendNodeId:", backend_node_id)
                break
        except:
            break
            
    assert backend_node_id, "Failed to intercept file chooser"
    
    client.call("DOM.setFileInputFiles", {
        "files": [srt_file],
        "backendNodeId": backend_node_id
    })
    print("[Studio] Set files via DOM.setFileInputFiles!")
    
    node_obj = client.call("DOM.resolveNode", {"backendNodeId": backend_node_id})
    obj_id = node_obj.get("object", {}).get("objectId")
    if obj_id:
        client.call("Runtime.callFunctionOn", {
            "objectId": obj_id,
            "functionDeclaration": """function() {
                this.dispatchEvent(new Event('input', { bubbles: true }));
                this.dispatchEvent(new Event('change', { bubbles: true }));
            }"""
        })
        
    print("[Studio] Waiting 8s for Subtitle Editor to process...")
    time.sleep(8)
    
    client.screenshot(f"scratch/{vid}_in_editor_ready.png")
    
    print("[Studio] Clicking Publish at (1496.6, 80)...")
    client.click(1496.6, 80)
    time.sleep(6)
    
    client.screenshot(f"scratch/{vid}_published_toast.png")
    client.close()
    print(f"[Studio] SUCCESS: Subtitles published for {vid}!")

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "mQpQEuXiEZ4"
    srt = os.path.abspath(f"production/subtitles/{vid}.srt")
    upload_subtitles_in_studio(vid, srt)
