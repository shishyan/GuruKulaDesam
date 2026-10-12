import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const all = Array.from(document.querySelectorAll('*'));
    const label = all.find(el => (el.innerText || '').trim() === 'Return silent videos');
    if (label) {
        // Find adjacent switch
        const row = label.closest('div, tr, li') || label.parentElement;
        const clickable = row.querySelector('button, [role="switch"], input, span.switch') || row;
        clickable.click();
        return { clicked: true, outerHTML: clickable.outerHTML.slice(0, 150) };
    }
    return { clicked: false };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
print('Toggle result:', json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
