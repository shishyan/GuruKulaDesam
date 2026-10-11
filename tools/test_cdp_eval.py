import sys
import json
import urllib.request
import asyncio
import websockets

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

async def test_eval():
    with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
        targets = json.loads(r.read().decode())
    
    page_target = next(t for t in targets if t.get('type') == 'page')
    ws_url = page_target['webSocketDebuggerUrl']
    print(f"Connecting to {ws_url}...")
    
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        # Evaluate document.title
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.title",
                "returnByValue": True
            }
        }
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        print("Title response:", json.loads(resp))
        
        # Check what the Save button is
        msg = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """(() => {
                    const saveBtn = document.querySelector('#save-button, ytcp-button#save-button, [test-id="save-button"]');
                    if (!saveBtn) {
                        // find all buttons
                        const btns = Array.from(document.querySelectorAll('ytcp-button, button'));
                        return {
                            found: false,
                            buttons: btns.map(b => ({
                                id: b.id,
                                text: (b.innerText || '').trim(),
                                disabled: b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true'
                            }))
                        };
                    }
                    return {
                        found: true,
                        id: saveBtn.id,
                        tagName: saveBtn.tagName,
                        text: saveBtn.innerText.trim(),
                        disabled: saveBtn.hasAttribute('disabled') || saveBtn.getAttribute('aria-disabled') === 'true'
                    };
                })()""",
                "returnByValue": True
            }
        }
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        print("Save button check:", json.dumps(json.loads(resp), indent=2, ensure_ascii=False))

asyncio.run(test_eval())
