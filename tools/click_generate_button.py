import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    const btn = document.querySelector('button.generate-icon-button');
    if (!btn) return { error: 'No generate-icon-button found' };
    
    // Dispatch full pointer down, mousedown, up, click sequence
    const opts = { bubbles: true, cancelable: true, view: window };
    btn.dispatchEvent(new MouseEvent('mousedown', opts));
    btn.dispatchEvent(new MouseEvent('mouseup', opts));
    btn.click();
    return {
        clicked: true,
        disabled: btn.disabled,
        cls: btn.className,
        aria: btn.getAttribute('aria-label')
    };
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Full click result:", json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
