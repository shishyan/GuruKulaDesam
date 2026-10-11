import sys
import json
import urllib.request
import asyncio
import websockets

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

async def do_connect():
    with urllib.request.urlopen("http://127.0.0.1:9225/json") as r:
        targets = json.loads(r.read().decode())
    page = next(t for t in targets if t.get('type') == 'page')
    ws_url = page['webSocketDebuggerUrl']
    print("Testing connection to:", ws_url)
    async with websockets.connect(ws_url) as ws:
        print("Connected successfully!")
        await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": "document.title"}}))
        res = await ws.recv()
        print("Result:", res)

async def test():
    try:
        await asyncio.wait_for(do_connect(), timeout=3.0)
    except Exception as e:
        print("Exception:", type(e), e)

asyncio.run(test())
