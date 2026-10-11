import sys
import json
import urllib.request
import asyncio
import websockets

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

async def test():
    with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
        targets = json.loads(r.read().decode())
    page = next(t for t in targets if t.get('type') == 'page')
    ws_url = page['webSocketDebuggerUrl']
    
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        await ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": "document.title", "returnByValue": True}}))
        
        for _ in range(5):
            msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=3.0))
            print("Received:", msg.get('id'), msg.get('method'), msg.get('result'))
            if msg.get('id') == 2:
                break

asyncio.run(test())
