import urllib.request
import json
import time
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# Find and click the button containing the 'tune' icon
js_find_tune = """
(() => {
    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
    const tune = btns.find(b => b.innerText.includes('tune') || b.innerHTML.includes('tune'));
    if (tune) {
        tune.click();
        return { clicked: true, innerText: tune.innerText, outerHTML: tune.outerHTML.slice(0, 100) };
    }
    return { clicked: false, available: btns.map(b => b.innerText).slice(0, 20) };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_find_tune, 'returnByValue': True}}))
print("Tune btn:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

time.sleep(1)

js_after_tune = """
(() => {
    const dialogs = Array.from(document.querySelectorAll('[role="dialog"], [role="menu"], [role="listbox"], .popup')).map(d => d.innerText);
    const body = document.body.innerText;
    return {
        dialogs,
        hasVeo: body.includes('Veo'),
        hasLite: body.includes('Lite'),
        hasOmni: body.includes('Omni')
    };
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_after_tune, 'returnByValue': True}}))
print("Settings popup:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
