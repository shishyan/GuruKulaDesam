import urllib.request, json, time, websocket, sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [t for t in tabs if 'studio.youtube.com' in t.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

expr = """
(() => {
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        text: document.body.innerText.slice(0, 1000)
    });
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
res = json.loads(ws.recv())
data = json.loads(res.get('result', {}).get('result', {}).get('value', '{}'))
print("=== STUDIO CONTENT ===")
print("URL:", data.get('url'))
print("Title:", data.get('title'))
print("Body:\n", data.get('text'))
ws.close()

