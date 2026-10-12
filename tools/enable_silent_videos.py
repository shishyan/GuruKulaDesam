import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    // Find all switches or role="switch"
    const switches = Array.from(document.querySelectorAll('button[role="switch"], [role="switch"]'));
    if (switches.length >= 2) {
        // Switch 0: Sound on hover, Switch 1: Return silent videos
        switches[1].click();
        return { clicked: true, checked: switches[1].getAttribute('aria-checked') };
    }
    return { clicked: false, switchesFound: switches.length };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print('Toggle switch 1:', json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

# Press Escape to close the settings panel
js_esc = """
(() => {
    document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', code: 'Escape', bubbles: true}));
    return true;
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_esc, 'returnByValue': True}}))
ws.recv()

ws.close()
