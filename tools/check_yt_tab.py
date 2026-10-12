import urllib.request, json, websocket, sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
for t in tabs:
    if 'youtube.com' in t.get('url', '') and t.get('type') == 'page':
        ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)
        expr = """
        (() => {
            let avatar = document.querySelector('#avatar-btn') || document.querySelector('button#avatar-btn');
            return JSON.stringify({
                url: window.location.href,
                title: document.title,
                avatarLabel: avatar ? avatar.getAttribute('aria-label') : null,
                bodyText: document.body.innerText.slice(0, 150)
            });
        })()
        """
        ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
        res = json.loads(ws.recv())
        data = json.loads(res.get('result', {}).get('result', {}).get('value', '{}'))
        print(f"Tab [{t['id']}]:", data)
        ws.close()
sys.exit(0)

ws = websocket.create_connection(target['webSocketDebuggerUrl'], suppress_origin=True)
expr = """
(() => {
    let avatar = document.querySelector('#avatar-btn') || document.querySelector('button#avatar-btn');
    let label = avatar ? avatar.getAttribute('aria-label') : null;
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        avatarLabel: label
    });
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
res = json.loads(ws.recv())
data = json.loads(res.get('result', {}).get('result', {}).get('value', '{}'))
print("YouTube tab data:", data)
ws.close()
