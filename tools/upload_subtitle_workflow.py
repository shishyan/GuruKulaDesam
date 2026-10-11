import time
import os
import json
import base64
from playwright.sync_api import sync_playwright

def upload_subtitle_for_video(vid):
    srt_path = os.path.abspath(f"production/subtitles/{vid}.srt")
    if not os.path.exists(srt_path):
        print(f"Error: {srt_path} does not exist!")
        return False
        
    print(f"\n==========================================")
    print(f"Starting browser subtitle upload for {vid}...")
    print(f"File: {srt_path}")
    print(f"==========================================")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        cdp = ctx.new_cdp_session(page)
        
        # 1. Enable Page domain and file chooser interceptor
        cdp.send('Page.enable')
        cdp.send('Page.setInterceptFileChooserDialog', {'enabled': True})
        
        file_chooser_opened = []
        def on_file_chooser(params):
            print(">>> FILE CHOOSER OPENED! Intercepted! <<<")
            file_chooser_opened.append(params)
            # Accept file
            cdp.send('Page.handleFileChooser', {
                'action': 'accept',
                'files': [srt_path]
            })
            print(">>> Handled file chooser with srt file! <<<")
            
        cdp.on('Page.fileChooserOpened', on_file_chooser)
        
        # 2. Navigate to translations
        print(f"Navigating to https://studio.youtube.com/video/{vid}/translations...")
        cdp.send('Page.navigate', {'url': f'https://studio.youtube.com/video/{vid}/translations'})
        time.sleep(5)
        
        # 3. Find and click 'upload-default-language-button'
        print("Finding Upload manual button...")
        find_btn_expr = '''
        (() => {
            function findInShadow(node, id) {
                if (node.id === id) return node;
                if (node.shadowRoot) {
                    let f = findInShadow(node.shadowRoot, id);
                    if (f) return f;
                }
                for (let c of node.children || []) {
                    let f = findInShadow(c, id);
                    if (f) return f;
                }
                return null;
            }
            let btn = findInShadow(document.body, 'upload-default-language-button');
            if (btn) {
                let rect = btn.getBoundingClientRect();
                return JSON.stringify({x: rect.x + rect.width / 2, y: rect.y + rect.height / 2});
            }
            return null;
        })()
        '''
        res = cdp.send('Runtime.evaluate', {'expression': find_btn_expr, 'returnByValue': True})
        coords = json.loads(res['result']['value'])
        if not coords:
            print("Upload manual button not found!")
            return False
            
        print(f"Clicking Upload manual at {coords}...")
        cdp.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': coords['x'], 'y': coords['y']})
        cdp.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
        cdp.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
        time.sleep(2)
        
        # 4. Now find the Continue button inside the newly opened modal!
        find_continue_expr = '''
        (() => {
            function findButtons(node) {
                let res = [];
                if (node.shadowRoot) res = res.concat(findButtons(node.shadowRoot));
                for (let c of node.children || []) {
                    let txt = (c.innerText || '').trim();
                    let tag = c.tagName.toLowerCase();
                    if (txt === 'Continue' || txt === 'CONTINUE') {
                        let r = c.getBoundingClientRect();
                        if (r.width > 0 && r.height > 0) {
                            res.push({tag: tag, text: txt, x: r.x + r.width / 2, y: r.y + r.height / 2});
                        }
                    }
                    res = res.concat(findButtons(c));
                }
                return res;
            }
            return JSON.stringify(findButtons(document.body));
        })()
        '''
        res2 = cdp.send('Runtime.evaluate', {'expression': find_continue_expr, 'returnByValue': True})
        continue_btns = json.loads(res2['result']['value'])
        print(f"Found {len(continue_btns)} Continue buttons: {continue_btns}")
        
        if continue_btns:
            cb = continue_btns[0]
            print(f"Clicking Continue at ({cb['x']}, {cb['y']})...")
            cdp.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': cb['x'], 'y': cb['y']})
            cdp.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': cb['x'], 'y': cb['y'], 'button': 'left', 'clickCount': 1})
            cdp.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': cb['x'], 'y': cb['y'], 'button': 'left', 'clickCount': 1})
            time.sleep(4)
        else:
            print("Continue button not found in modal!")
            
        print(f"File chooser opened count: {len(file_chooser_opened)}")
        
        # Take screenshot of result
        shot = cdp.send('Page.captureScreenshot', {'format': 'png', 'fromSurface': False})
        out_shot = f'C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/upload_result_{vid}.png'
        with open(out_shot, 'wb') as f:
            f.write(base64.b64decode(shot['data']))
        print(f"Result screenshot saved to: {out_shot}")
        return True

if __name__ == '__main__':
    upload_subtitle_for_video('31xVgvxoiUA')
