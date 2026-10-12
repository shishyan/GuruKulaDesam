import urllib.request
import json
import time
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# Inspect tune button (model settings) and prompt options
js_tune = """
(() => {
    // Click tune button to see model selections (Veo 3.1, Veo 3.1 Lite, etc.)
    const tuneBtn = document.querySelector('button[aria-label*="tune" i], button:has-text("tune")') || Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('tune'));
    if (tuneBtn) {
        tuneBtn.click();
        return 'Clicked tune button';
    }
    return 'Tune button not found';
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_tune, 'returnByValue': True}}))
print("Tune click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

time.sleep(1)

# Check what popped up
js_inspect_menu = """
(() => {
    const textNodes = document.body.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
    const options = Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], [role="radiogroup"], [role="tab"], select option')).map(o => o.innerText.trim());
    return {
        options,
        snippet: textNodes.slice(-30)
    };
})()
"""

ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_inspect_menu, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
