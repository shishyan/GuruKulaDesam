import urllib.request
import json
import time
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# Find iframe or popup window for Google Account switcher
js_click = """
(() => {
    const avatar = document.querySelector('[aria-label*="Google Account" i], [aria-label*="Account details" i]');
    if (avatar) {
        avatar.click();
        return 'Clicked avatar';
    }
    return 'Not found';
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_click, 'returnByValue': True}}))
print("Click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
time.sleep(2)

# Check all iframes on page
js_iframes = """
(() => {
    const iframes = Array.from(document.querySelectorAll('iframe')).map(f => ({
        src: f.src,
        id: f.id,
        name: f.name,
        visible: f.offsetWidth > 0 && f.offsetHeight > 0
    }));
    return iframes;
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_iframes, 'returnByValue': True}}))
print("Iframes:", json.dumps(json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'), indent=2))
ws.close()
