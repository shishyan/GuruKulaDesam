import sys
import json
import urllib.request
import asyncio
import websockets

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

async def run():
    with urllib.request.urlopen("http://127.0.0.1:9225/json/version") as r:
        info = json.loads(r.read().decode())
    browser_ws = info['webSocketDebuggerUrl']
    
    async with websockets.connect(browser_ws, max_size=50*1024*1024) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Target.getTargets"}))
        resp = json.loads(await ws.recv())
        targets = resp['result']['targetInfos']
        studio_target = next(t for t in targets if 'studio.youtube.com' in t.get('url', ''))
        target_id = studio_target['targetId']
        
        await ws.send(json.dumps({
            "id": 2,
            "method": "Target.attachToTarget",
            "params": {"targetId": target_id, "flatten": True}
        }))
        
        session_id = None
        while True:
            msg = json.loads(await ws.recv())
            # print("MSG:", msg.get('id'), msg.get('method'))
            if msg.get('id') == 2:
                session_id = msg['result']['sessionId']
                break
            elif msg.get('method') == 'Target.attachedToTarget':
                session_id = msg['params']['sessionId']
                break
                
        print("Session ID:", session_id)
        
        # Enable Runtime on session
        await ws.send(json.dumps({
            "id": 3,
            "sessionId": session_id,
            "method": "Runtime.enable"
        }))
        
        await ws.send(json.dumps({
            "id": 10,
            "sessionId": session_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """(() => {
                    const saveBtn = document.querySelector('#save-button, ytcp-button#save-button, ytcp-button-shape#save-button, [test-id="save-button"]');
                    if (saveBtn) {
                        return { found: true, id: saveBtn.id, text: saveBtn.innerText };
                    }
                    const allBtns = Array.from(document.querySelectorAll('button, ytcp-button, ytcp-button-shape'));
                    return {
                        found: false,
                        buttons: allBtns.map(b => ({ id: b.id, text: (b.innerText || '').trim() })).filter(b => b.text.toLowerCase().includes('save') || b.id.toLowerCase().includes('save'))
                    };
                })()""",
                "returnByValue": True
            }
        }))
        
        for _ in range(10):
            msg = json.loads(await ws.recv())
            if msg.get('id') == 10:
                print("EVAL RESULT:", json.dumps(msg, indent=2, ensure_ascii=False))
                break

asyncio.run(run())
