import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const text = document.body ? document.body.innerText : '';
    const progressBars = document.querySelectorAll('[role="progressbar"], .mat-mdc-progress-bar, mat-progress-bar');
    const pcts = Array.from(document.querySelectorAll('*'))
        .filter(el => el.children.length === 0 && /^\\d{1,2}%$/.test((el.innerText || '').trim()))
        .map(el => el.innerText.trim());
    return {
        textSnippet: text.slice(-600),
        progressBarsCount: progressBars.length,
        pcts
    };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
