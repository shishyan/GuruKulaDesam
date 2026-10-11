import asyncio
import json
import urllib.request
import base64
import websockets

async def cdp_eval_and_click():
    # 1. Get page WS URL
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json').read())
    page_tab = next(t for t in tabs if t.get('type') == 'page')
    ws_url = page_tab['webSocketDebuggerUrl']
    print(f"Connecting directly to CDP: {ws_url}")
    
    async with websockets.connect(ws_url) as ws:
        # 2. Click Save button via JS
        click_script = """(() => {
            let elms = Array.from(document.querySelectorAll('*'));
            for (let el of elms) {
                let t = (el.innerText || '').trim();
                if (t === 'Save' && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                    let r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0 && !el.hasAttribute('disabled')) {
                        el.click();
                        return { clicked: true, tag: el.tagName, id: el.id, x: r.x + r.width/2, y: r.y + r.height/2 };
                    }
                }
            }
            return { clicked: false };
        })()"""
        
        req = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": click_script,
                "returnByValue": True
            }
        }
        await ws.send(json.dumps(req))
        resp = json.loads(await ws.recv())
        print("Click response:", resp.get('result', {}).get('result', {}).get('value'))
        
        # Wait 4s
        await asyncio.sleep(4)
        
        # 3. Capture screenshot
        shot_req = {
            "id": 2,
            "method": "Page.captureScreenshot",
            "params": {"format": "png"}
        }
        await ws.send(json.dumps(shot_req))
        shot_resp = json.loads(await ws.recv())
        img_b64 = shot_resp.get('result', {}).get('data')
        if img_b64:
            with open("scratch/studio_save_confirmed.png", "wb") as f:
                f.write(base64.b64decode(img_b64))
            print("SUCCESS! Saved screenshot to scratch/studio_save_confirmed.png")

if __name__ == "__main__":
    asyncio.run(cdp_eval_and_click())
