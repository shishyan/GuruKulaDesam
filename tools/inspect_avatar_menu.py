import urllib.request, json, time, websocket, sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [t for t in tabs if 'studio.youtube.com' in t.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# First go to studio dashboard
ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://studio.youtube.com'}}))
ws.recv()
time.sleep(3)

# Click avatar
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.querySelector("#avatar-btn").click()'}}))
ws.recv()
time.sleep(1)

# Dump menu structure
expr = """
(() => {
    let items = Array.from(document.querySelectorAll('ytd-compact-link-renderer, ytd-menu-service-item-renderer, tp-yt-paper-item, yt-formatted-string'));
    return items.map(el => ({tag: el.tagName, id: el.id, text: el.innerText.trim()})).filter(x => x.text.length > 0);
})()
"""
ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
res = json.loads(ws.recv())
data = res.get('result', {}).get('result', {}).get('value', [])
print("Menu Items Count:", len(data))
for item in data[:15]:
    print(" ", item)

ws.close()

