import urllib.request
import json
import websocket
import time

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js_click = """
(() => {
    const btn = document.querySelector('button.generate-icon-button, button[aria-label*="Start generation" i]');
    if (btn) {
        btn.click();
        return { clicked: true, text: btn.innerText, aria: btn.getAttribute('aria-label') };
    }
    return { clicked: false };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_click, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Click response:", res.get('result', {}).get('result', {}).get('value'))

time.sleep(3)

js_check = """
(() => {
    const text = document.body ? document.body.innerText : '';
    const hasStop = text.includes('Stop');
    const pcts = Array.from(document.querySelectorAll('*'))
        .filter(el => el.children.length === 0 && /^\\d{1,2}%$/.test((el.innerText || '').trim()))
        .map(el => el.innerText.trim());
    return { hasStop, pcts, snippet: text.slice(-300) };
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_check, 'returnByValue': True}}))
res2 = json.loads(ws.recv())
print("Check response:", res2.get('result', {}).get('result', {}).get('value'))

ws.close()
