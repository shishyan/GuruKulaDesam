import sys
import json
import urllib.request
import websocket

sys.stdout.reconfigure(encoding='utf-8')

def get_page_ws(pattern='youtube.com'):
    res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
    tabs = json.loads(res.decode('utf-8'))
    for t in tabs:
        if t.get('type') == 'page' and pattern in t.get('url', ''):
            return t.get('webSocketDebuggerUrl'), t.get('url')
    for t in tabs:
        if t.get('type') == 'page':
            return t.get('webSocketDebuggerUrl'), t.get('url')
    return None, None

def evaluate(js, ws_url):
    ws = websocket.create_connection(ws_url, timeout=10)
    req = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js,
            "awaitPromise": True,
            "returnByValue": True
        }
    }
    ws.send(json.dumps(req))
    raw = ws.recv()
    ws.close()
    res = json.loads(raw)
    return res.get('result', {}).get('result', {}).get('value')

if __name__ == '__main__':
    ws_url, current_url = get_page_ws('PLP-GdNkY_qyo')
    print("Connecting to:", current_url)
    res = evaluate("document.title", ws_url)
    print("Page Title:", res)
