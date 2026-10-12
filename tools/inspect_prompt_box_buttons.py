import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    // Look at all buttons inside the prompt box container
    const promptBox = document.querySelector('flow-base-prompt-box, flow-prompt-box, .prompt-box-container');
    if (!promptBox) return { error: 'No prompt box container' };
    
    const btns = Array.from(promptBox.querySelectorAll('button')).map(b => ({
        text: (b.innerText || '').trim(),
        aria: b.getAttribute('aria-label') || '',
        cls: b.className,
        disabled: b.disabled,
        rect: b.getBoundingClientRect()
    }));
    return { promptBoxClass: promptBox.className, btns };
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
