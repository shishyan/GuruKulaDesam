import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    // 1. Look for submit / arrow button
    const btns = Array.from(document.querySelectorAll('button')).filter(b => {
        const aria = (b.getAttribute('aria-label') || '').toLowerCase();
        const text = (b.innerText || '').toLowerCase();
        const cls = b.className || '';
        return aria.includes('start') || aria.includes('generate') || cls.includes('generate') || text.includes('arrow_forward');
    });
    
    // Check if there's any active disabled state or if clicking works
    if (btns.length > 0) {
        const btn = btns[btns.length - 1];
        const rect = btn.getBoundingClientRect();
        btn.click();
        return { clicked: true, aria: btn.getAttribute('aria-label'), disabled: btn.disabled, rect };
    }
    
    // If not found, try pressing Enter inside ProseMirror
    const pm = document.querySelector('div.ProseMirror');
    if (pm) {
        pm.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
        return { dispatchedEnter: true };
    }
    return { error: 'Nothing found' };
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Submit trigger result:", json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
