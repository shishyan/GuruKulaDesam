import os
import time
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    cdp = ctx.new_cdp_session(page)
    
    vid = "31xVgvxoiUA"
    srt_file = os.path.abspath(f"production/subtitles/{vid}.srt")
    print(f"Target srt file: {srt_file} (exists: {os.path.exists(srt_file)})")
    
    # 1. Find captions-file-loader
    res_obj = cdp.send('Runtime.evaluate', {
        'expression': '''(() => {
            function findInput(node) {
                if (node.id === 'captions-file-loader') return node;
                if (node.shadowRoot) {
                    let f = findInput(node.shadowRoot);
                    if (f) return f;
                }
                for (let c of node.children || []) {
                    let f = findInput(c);
                    if (f) return f;
                }
                return null;
            }
            return findInput(document.body);
        })()''',
        'returnByValue': False
    })
    
    obj_id = res_obj['result']['objectId']
    node_res = cdp.send('DOM.describeNode', {'objectId': obj_id})
    backend_id = node_res['node']['backendNodeId']
    print(f"Found input element. backendNodeId: {backend_id}")
    
    # 2. Set file
    cdp.send('DOM.setFileInputFiles', {
        'files': [srt_file],
        'backendNodeId': backend_id
    })
    print("Files set via DOM.setFileInputFiles!")
    
    # 3. Dispatch change and input events
    cdp.send('Runtime.callFunctionOn', {
        'objectId': obj_id,
        'functionDeclaration': '''function() {
            this.dispatchEvent(new Event('input', { bubbles: true }));
            this.dispatchEvent(new Event('change', { bubbles: true }));
        }'''
    })
    print("Dispatched input and change events!")
    time.sleep(3)
    
    # 4. Check what appeared on the page (buttons, texts)
    expr = '''
    (() => {
        function getButtons(node) {
            let res = [];
            if (node.shadowRoot) res = res.concat(getButtons(node.shadowRoot));
            for (let c of node.children || []) {
                let tag = c.tagName.toLowerCase();
                let txt = (c.innerText || '').trim();
                let id = c.id || '';
                let aria = c.getAttribute('aria-label') || '';
                if (tag.includes('button') || tag === 'a' || c.getAttribute('role') === 'button') {
                    if (txt || aria) res.push({tag: tag, id: id, text: txt.replace(/\\s+/g, ' ').slice(0, 40), aria: aria});
                }
                res = res.concat(getButtons(c));
            }
            return res;
        }
        return JSON.stringify(getButtons(document.body));
    })()
    '''
    res = cdp.send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
    buttons = json.loads(res['result']['value'])
    print(f"Active buttons after file upload ({len(buttons)}):")
    for b in buttons:
        t = b['text'].lower()
        if any(w in t for w in ['publish', 'save', 'done', 'upload', 'confirm', 'continue', 'replace', 'draft']):
            print("  ->", b)
