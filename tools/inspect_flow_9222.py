import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [tab for tab in tabs if 'flow.google.com/project' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const text = document.body ? document.body.innerText : '';
    const avatar = document.querySelector('[aria-label*="Google Account" i], [aria-label*="Account details" i]');
    const editor = document.querySelector('div.ProseMirror');
    return {
        url: window.location.href,
        title: document.title,
        avatarLabel: avatar ? avatar.getAttribute('aria-label') : 'Not found',
        hasEditor: !!editor,
        textSnippet: text.slice(0, 300)
    };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
