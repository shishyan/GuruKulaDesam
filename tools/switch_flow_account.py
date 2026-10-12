import urllib.request
import json
import time
import websocket

def run():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Click account profile avatar
    click_code = """
    (() => {
        const btn = document.querySelector('[aria-label*="Google Account" i], [aria-label*="Account details" i]');
        if (btn) {
            btn.click();
            return 'Clicked account button';
        }
        return 'Not found';
    })()
    """
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': click_code, 'returnByValue': True}}))
    print("Click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

    time.sleep(2)

    # Find accounts listed in popup or iframes
    find_code = """
    (() => {
        const iframes = Array.from(document.querySelectorAll('iframe')).map(f => f.src);
        const text = document.body.innerText;
        return {
            iframes,
            hasNagaraj: text.toLowerCase().includes('nagaraj957'),
            textSnippet: text.slice(0, 300)
        };
    })()
    """
    ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': find_code, 'returnByValue': True}}))
    print("Popup status:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
    ws.close()

if __name__ == '__main__':
    run()
