import urllib.request, json, time, websocket, sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [t for t in tabs if 'studio.youtube.com' in t.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

for auth in ['1', 'shishyan@gmail.com', '2', '0']:
    url = f'https://studio.youtube.com/video/NK2PqzKz3aI/translations?authuser={auth}'
    ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': url}}))
    ws.recv()
    time.sleep(3)
    ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': 'JSON.stringify({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 100)})'}}))
    res = json.loads(ws.recv())
    data = json.loads(res.get('result', {}).get('result', {}).get('value', '{}'))
    print(f'authuser={auth}: title="{data.get("title")}"')
    if 'Oops' not in data.get('title', '') and 'Oops' not in data.get('text', ''):
        print('  SUCCESS with authuser=' + auth)
        break

ws.close()

