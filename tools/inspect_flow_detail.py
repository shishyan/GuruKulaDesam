import urllib.request
import json
import websocket

def get_page_info():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json').read())
    flow_tab = next(t for t in tabs if 'flow.google.com/project' in t.get('url', ''))
    ws = websocket.create_connection(flow_tab['webSocketDebuggerUrl'], suppress_origin=True)
    
    js = """
    (() => {
        const bodyText = document.body.innerText;
        const hasStop = bodyText.includes('Stop');
        const hasFailed = bodyText.includes('failed to generate') || bodyText.includes('Failed to generate');
        const editor = document.querySelector('div.ProseMirror');
        const editorText = editor ? editor.innerText : '';
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: (b.innerText || '').trim(),
            aria: b.getAttribute('aria-label') || '',
            disabled: b.disabled
        })).filter(b => b.text || b.aria);
        
        return {
            hasStop,
            hasFailed,
            editorText: editorText.slice(0, 100),
            buttonsCount: buttons.length,
            submitButtons: buttons.filter(b => /start|generate|arrow_forward|stop/i.test(b.text) || /start|generate|stop/i.test(b.aria))
        };
    })()
    """
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
    res = json.loads(ws.recv())
    ws.close()
    return res.get('result', {}).get('value')

if __name__ == '__main__':
    print(json.dumps(get_page_info(), indent=2))
