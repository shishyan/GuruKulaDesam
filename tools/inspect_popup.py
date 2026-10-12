import urllib.request, json, time, websocket, sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [t for t in tabs if 'studio.youtube.com' in t.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# Navigate to channel dashboard
ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://studio.youtube.com'}}))
ws.recv()
time.sleep(4)

# Click avatar
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.querySelector("#avatar-btn").click()'}}))
ws.recv()
time.sleep(1)

# Find all elements inside ytd-multi-page-menu-renderer
expr = """
(() => {
    let menu = document.querySelector('yt-multi-page-menu-section-renderer') || document.querySelector('ytd-multi-page-menu-renderer') || document.querySelector('#sections');
    let popup = document.querySelector('tp-yt-iron-dropdown') || document.querySelector('#menu');
    return {
        hasMenu: !!menu,
        hasPopup: !!popup,
        popupHTML: popup ? popup.innerHTML.slice(0, 1000) : 'no popup'
    };
})()
"""
ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(res.get('result', {}).get('result', {}).get('value'))
ws.close()
