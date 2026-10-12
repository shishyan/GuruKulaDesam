import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    // Find element with text "Return silent videos"
    const elements = Array.from(document.querySelectorAll('*'));
    const target = elements.find(el => el.innerText && el.innerText.trim() === 'Return silent videos');
    if (target) {
        // Find clickable parent or switch/checkbox
        let clickable = target.closest('button, [role="switch"], [role="checkbox"], label, div[role="button"]') || target;
        clickable.click();
        return { clicked: true, text: target.innerText };
    }
    return { clicked: false };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print('Toggle silent videos:', json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
