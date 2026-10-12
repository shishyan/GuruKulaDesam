import urllib.request, json, time, websocket, sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [t for t in tabs if 'studio.youtube.com' in t.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

expr = """
(() => {
    function findAll(root, selector) {
        let results = Array.from(root.querySelectorAll(selector));
        let all = Array.from(root.querySelectorAll('*'));
        for (let el of all) {
            if (el.shadowRoot) {
                results = results.concat(findAll(el.shadowRoot, selector));
            }
        }
        return results;
    }
    let buttons = findAll(document, 'button, a, tp-yt-paper-button, ytcp-button');
    return buttons.map(b => ({tag: b.tagName, text: b.innerText.trim(), href: b.href || null}));
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
res = json.loads(ws.recv())
data = res.get('result', {}).get('result', {}).get('value', [])
print("Shadow DOM Buttons Count:", len(data))
for b in data:
    print(" ", b)

ws.close()

