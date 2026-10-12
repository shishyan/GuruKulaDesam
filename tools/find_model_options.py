import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

js_find_elements = """
(() => {
    const all = Array.from(document.querySelectorAll('*'));
    const matched = all.filter(el => el.children.length === 0 && (el.innerText.includes('Veo') || el.innerText.includes('Lite')));
    return matched.map(el => ({
        tag: el.tagName,
        text: el.innerText,
        parentTag: el.parentElement ? el.parentElement.tagName : null,
        parentClass: el.parentElement ? el.parentElement.className : null
    }));
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_find_elements, 'returnByValue': True}}))
print(json.dumps(json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'), indent=2))
ws.close()
