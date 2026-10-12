import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
if not f_tabs:
    print("No flow tab found!")
    exit(1)

ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)
js = """
(() => {
    const buttons = Array.from(document.querySelectorAll('button, [role="button"]'))
        .map(b => (b.innerText || b.getAttribute('aria-label') || '').trim())
        .filter(Boolean);
    const textSnippet = document.body.innerText.slice(0, 500);
    const dialogs = Array.from(document.querySelectorAll('[role="dialog"], [aria-modal="true"]'))
        .map(d => d.innerText.slice(0, 200));
    return {
        url: window.location.href,
        buttonsCount: buttons.length,
        buttons: buttons.slice(0, 20),
        dialogs: dialogs,
        textSnippet: textSnippet
    };
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('value', {}), indent=2))
ws.close()
