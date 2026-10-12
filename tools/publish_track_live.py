"""
Unified Live Track Publisher for YouTube Studio via Chrome Port 9225.
Updates:
1. Video Description (Full scripture lyrics, devotional meaning, acoustic musical chapters)
2. Video Language (Enforces Tamil as default language)
3. Modern 16:9 Thumbnail (1920x1080)
4. Subtitles (Acoustic voice timestamps from Whisper STT published live)
"""

import os, sys, time, json, base64, urllib.request
import websocket

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

class StudioPublisher:
    def __init__(self):
        res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
        tabs = json.loads(res.decode('utf-8'))
        page = [t for t in tabs if t.get('type') == 'page'][0]
        self.ws_url = page['webSocketDebuggerUrl']
        self.ws = websocket.create_connection(self.ws_url, timeout=25)
        self.msg_id = 0
        self.events = []
        
    def call(self, method, params=None):
        self.msg_id += 1
        i = self.msg_id
        self.ws.send(json.dumps({'id': i, 'method': method, 'params': params or {}}))
        while True:
            m = json.loads(self.ws.recv())
            if 'id' in m:
                if m['id'] == i:
                    return m.get('result', {})
            else:
                self.events.append(m)

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

    def update_video_details(self, vid):
        desc_path = os.path.abspath(f"production/descriptions/{vid}.txt")
        thumb_path = os.path.abspath(f"production/thumbnails/{vid}.png")
        assert os.path.exists(desc_path), f"Missing desc: {desc_path}"
        with open(desc_path, "r", encoding="utf-8") as f:
            desc_text = f.read()

        url = f"https://studio.youtube.com/video/{vid}/edit"
        print(f"\n[Step 1] Navigating to {url}...")
        self.call("Page.navigate", {"url": url})
        time.sleep(6)

        # Inject description
        print("[Step 1] Injecting description...")
        inject_js = f"""(() => {{
            const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
            if (!descBox) return {{ success: false, error: 'no desc box found' }};
            descBox.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, {json.dumps(desc_text)});
            descBox.dispatchEvent(new Event('input', {{ bubbles: true }}));
            descBox.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return {{ success: true, length: descBox.innerText.length }};
        }})()"""
        r = self.call("Runtime.evaluate", {"expression": inject_js, "returnByValue": True}).get("result", {}).get("value", {})
        print(f"[Step 1] Description injected: {r}")
        time.sleep(1.5)

        # Upload thumbnail if available
        if os.path.exists(thumb_path):
            print(f"[Step 1] Uploading thumbnail: {thumb_path}...")
            self.call('DOM.enable')
            doc = self.call('DOM.getDocument', {'depth': -1})
            root_id = doc.get('root', {}).get('nodeId')
            loader = self.call('DOM.querySelector', {'nodeId': root_id, 'selector': '#file-loader'})
            node_id = loader.get('nodeId')
            if node_id:
                self.call('DOM.setFileInputFiles', {'files': [thumb_path], 'nodeId': node_id})
                node_obj = self.call('DOM.resolveNode', {'nodeId': node_id})
                obj_id = node_obj.get('object', {}).get('objectId')
                if obj_id:
                    self.call('Runtime.callFunctionOn', {
                        'objectId': obj_id,
                        'functionDeclaration': "function() { this.dispatchEvent(new Event('change', { bubbles: true })); }"
                    })
                print("[Step 1] Thumbnail loaded successfully!")
                time.sleep(1.5)

        # Check and expand Show More for language
        print("[Step 1] Checking Video Language...")
        self.call("Runtime.evaluate", {"expression": """(() => {
            let b = Array.from(document.querySelectorAll('ytcp-button, button')).find(e => (e.innerText || '').includes('SHOW MORE') || (e.innerText || '').includes('Show more'));
            if (b) b.click();
        })()"""})
        time.sleep(1.5)

        lang_js = """(() => {
            let lang = document.querySelector('ytcp-form-language-input#language-input, ytcp-form-language-input, [label="Video language"]');
            return lang ? lang.innerText.trim() : '';
        })()"""
        current_lang = self.call("Runtime.evaluate", {"expression": lang_js, "returnByValue": True}).get("result", {}).get("value", "")
        print(f"[Step 1] Current language text: {repr(current_lang)}")

        if "Tamil" not in current_lang:
            print("[Step 1] Setting language to Tamil...")
            self.call("Runtime.evaluate", {"expression": """(() => {
                let lang = document.querySelector('ytcp-form-language-input, ytcp-language-selector');
                if (lang) {
                    let trig = lang.querySelector('#trigger, .select-container, ytcp-dropdown-trigger');
                    if (trig) trig.click(); else lang.click();
                }
            })()"""})
            time.sleep(1.5)

            # Select Tamil from dropdown
            self.call("Runtime.evaluate", {"expression": """(() => {
                let items = Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu-item, [role="option"]'));
                let tamil = items.find(i => (i.innerText || '').trim() === 'Tamil');
                if (tamil) tamil.click();
            })()"""})
            time.sleep(1.5)
            print("[Step 1] Selected Tamil!")

        # Click Save
        print("[Step 1] Clicking Save button...")
        click_save = """(() => {
            let btn = document.querySelector('#save, [id="save"], ytcp-button#save-button, ytcp-button#save');
            if (btn && !btn.hasAttribute('disabled')) {
                btn.click();
                return { clicked: true };
            }
            return { clicked: false, disabled: btn ? btn.hasAttribute('disabled') : null };
        })()"""
        s_res = self.call("Runtime.evaluate", {"expression": click_save, "returnByValue": True}).get("result", {}).get("value", {})
        print(f"[Step 1] Save result: {s_res}")
        time.sleep(6)
        self.screenshot(f"scratch/{vid}_edit_saved.png")

    def publish_subtitles(self, vid):
        srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
        assert os.path.exists(srt_file), f"Missing SRT: {srt_file}"

        url = f"https://studio.youtube.com/video/{vid}/translations"
        print(f"\n[Step 2] Navigating to {url}...")
        self.call("Page.navigate", {"url": url})
        time.sleep(6)

        self.call('Page.enable')
        self.call('DOM.enable')
        self.call('Page.setInterceptFileChooserDialog', {'enabled': True})

        # Check track state
        check_js = """(() => {
            let editBtn = document.querySelector('#m2-editor-button, ytcp-button#m2-editor-button');
            let uploadBtn = document.querySelector('#upload-default-language-button, ytcp-button#upload-default-language-button');
            return {
                hasEdit: !!editBtn,
                hasUpload: !!uploadBtn
            };
        })()"""
        chk = {}
        for attempt in range(10):
            chk = self.call("Runtime.evaluate", {"expression": check_js, "returnByValue": True}).get("result", {}).get("value", {})
            print(f"[Step 2] Check attempt {attempt+1}: {chk}")
            if chk.get("hasEdit") or chk.get("hasUpload"):
                break
            time.sleep(2)

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
        m_info = self.call("Runtime.evaluate", {"expression": check_modal, "returnByValue": True}).get("result", {}).get("value", {})
        print(f"[Step 2] Initial page state: {m_info}")

        if not m_info.get("hasEditor") and not m_info.get("hasContinue"):
            find_btn = """(() => {
                let editBtn = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Edit subtitles');
                let upBtn = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').trim() === 'Upload manual');
                let target = editBtn || upBtn;
                if (target) {
                    let r = target.getBoundingClientRect();
                    return { found: true, x: r.x + r.width/2, y: r.y + r.height/2, text: target.innerText.trim() };
                }
                return { found: false };
            })()"""
            b_info = self.call("Runtime.evaluate", {"expression": find_btn, "returnByValue": True}).get("result", {}).get("value", {})
            if b_info.get("found"):
                print(f"[Step 2] Clicking {b_info['text']} at ({b_info['x']}, {b_info['y']})...")
                self.click(b_info['x'], b_info['y'])
                time.sleep(5)

        # Check for initial modal "Upload file" row
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
        opt_info = self.call("Runtime.evaluate", {"expression": find_upload_file_option, "returnByValue": True}).get("result", {}).get("value", {})
        print(f"[Step 2] Upload file option check: {opt_info}")
        if opt_info.get("found"):
            print(f"[Step 2] Clicking initial modal Upload file option at ({opt_info['x']}, {opt_info['y']})...")
            self.click(opt_info['x'], opt_info['y'])
            time.sleep(2)
        else:
            # Check state again
            m_info = self.call("Runtime.evaluate", {"expression": check_modal, "returnByValue": True}).get("result", {}).get("value", {})
            print(f"[Step 2] Post-click state: {m_info}")

            if not m_info.get("hasContinue"):
                print("[Step 2] Clicking Options menu at (919.5, 142.0)...")
                self.click(919.5, 142.0)
                time.sleep(1.5)

                print("[Step 2] Clicking 'Upload file' menu item...")
                self.call("Runtime.evaluate", {
                    "expression": """(() => {
                        let items = Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-menu-service-item, .ytcp-menu-service-item'));
                        let target = items.find(e => e.innerText.includes('Upload file'));
                        if (target) target.click();
                    })()"""
                })
                time.sleep(2)

        # Click Continue on file type dialog
        print("[Step 2] Finding Continue button...")
        find_continue = """(() => {
            let btns = Array.from(document.querySelectorAll('ytcp-button, button'));
            let b = btns.find(e => e.innerText.trim() === 'Continue' || e.innerText.trim() === 'CONTINUE');
            if (b) {
                let r = b.getBoundingClientRect();
                return { found: true, x: r.x + r.width/2, y: r.y + r.height/2 };
            }
            return { found: false };
        })()"""
        c_info = self.call("Runtime.evaluate", {"expression": find_continue, "returnByValue": True}).get("result", {}).get("value", {})
        print(f"[Step 2] Continue info: {c_info}")
        if c_info.get("found"):
            self.click(c_info["x"], c_info["y"])
        else:
            self.click(1083.8, 544.0)

        # Intercept file chooser
        print("[Step 2] Waiting for Page.fileChooserOpened...")
        backend_node_id = None
        for ev in self.events:
            if ev.get('method') == 'Page.fileChooserOpened':
                backend_node_id = ev.get('params', {}).get('backendNodeId')
                break

        if not backend_node_id:
            t_end = time.time() + 10
            while time.time() < t_end:
                try:
                    m = json.loads(self.ws.recv())
                    if m.get('method') == 'Page.fileChooserOpened':
                        backend_node_id = m.get('params', {}).get('backendNodeId')
                        break
                except:
                    break

        assert backend_node_id, "Failed to intercept file chooser"
        print(f"[Step 2] Setting SRT file: {srt_file}...")
        self.call("DOM.setFileInputFiles", {
            "files": [srt_file],
            "backendNodeId": backend_node_id
        })

        node_obj = self.call("DOM.resolveNode", {"backendNodeId": backend_node_id})
        obj_id = node_obj.get("object", {}).get("objectId")
        if obj_id:
            self.call("Runtime.callFunctionOn", {
                "objectId": obj_id,
                "functionDeclaration": """function() {
                    this.dispatchEvent(new Event('input', { bubbles: true }));
                    this.dispatchEvent(new Event('change', { bubbles: true }));
                }"""
            })

        print("[Step 2] Waiting 8s for subtitle editor to parse...")
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
        pub_info = self.call('Runtime.evaluate', {'expression': find_pub, 'returnByValue': True}).get('result', {}).get('value', {})
        print(f"[Step 2] Publish button status: {pub_info}")

        if pub_info.get("found") and not pub_info.get("disabled"):
            px, py = pub_info["x"], pub_info["y"]
            print(f"[Step 2] Clicking Publish at ({px}, {py})...")
            self.click(px, py)
        else:
            self.click(1496.6, 80)
            
        time.sleep(6)
        self.screenshot(f"scratch/{vid}_published_toast.png")
        print(f"[Step 2] LIVE PUBLISH COMPLETED FOR {vid}!")

    def close(self):
        try:
            self.ws.close()
        except:
            pass

def publish_track(vid):
    pub = StudioPublisher()
    try:
        pub.update_video_details(vid)
        pub.publish_subtitles(vid)
    finally:
        pub.close()

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "TUwlsvN7v1w"
    publish_track(vid)
