import urllib.request
import json
import websocket

def inspect_flow():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    js_expr = """
    (() => {
        const body = document.body ? document.body.innerText : '';
        const buttons = Array.from(document.querySelectorAll('button, [role="button"]')).map(b => b.innerText.trim()).filter(Boolean);
        const textNodes = body.split('\\n').map(s => s.trim()).filter(Boolean);
        return {
            url: window.location.href,
            title: document.title,
            buttons: buttons.slice(0, 30),
            creditLines: textNodes.filter(s => s.toLowerCase().includes('credit') || s.toLowerCase().includes('point') || s.includes('2351') || s.includes('2,351')),
            recentLines: textNodes.slice(0, 40)
        };
    })()
    """

    cmd = {
        'id': 1,
        'method': 'Runtime.evaluate',
        'params': {
            'expression': js_expr,
            'returnByValue': True
        }
    }
    ws.send(json.dumps(cmd))
    res = json.loads(ws.recv())
    val = res.get('result', {}).get('result', {}).get('value', {})
    print(json.dumps(val, indent=2, ensure_ascii=False))
    ws.close()

if __name__ == '__main__':
    inspect_flow()
