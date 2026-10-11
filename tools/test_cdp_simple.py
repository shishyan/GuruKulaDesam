import asyncio, json, urllib.request, websockets, sys
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

async def test():
    print("1. Fetching tabs...", flush=True)
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json').read())
    pages = [t for t in tabs if t.get('type') == 'page']
    for p in pages:
        print("  Page:", p['title'], p['url'], p['webSocketDebuggerUrl'], flush=True)
        
    target = pages[0]
    ws_url = target['webSocketDebuggerUrl']
    print(f"2. Connecting to {ws_url}...", flush=True)
    async with websockets.connect(ws_url, ping_interval=None) as ws:
        print("3. Connected! Sending Runtime.evaluate to click #save...", flush=True)
        script = """(() => {
            let btn = document.querySelector('#save, [id="save"], ytcp-button#save');
            if (btn) {
                let r = btn.getBoundingClientRect();
                btn.click();
                return { clicked: true, disabled: btn.hasAttribute('disabled'), text: btn.innerText };
            }
            return { clicked: false, all_buttons: Array.from(document.querySelectorAll('ytcp-button, button')).map(b => b.innerText) };
        })()"""
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": script, "returnByValue": True}
        }))
        resp = json.loads(await ws.recv())
        print("4. Response:", resp.get('result', {}).get('result', {}).get('value'), flush=True)

asyncio.run(test())
