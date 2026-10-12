import urllib.request
import json
import websocket
from pathlib import Path

dl_dir = str(Path.home() / "Downloads")
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(f_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

ws.send(json.dumps({'id': 1, 'method': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': dl_dir}}))
ws.recv()

js_card2 = """
(() => {
    const btns = Array.from(document.querySelectorAll('button, [role="button"]'))
        .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
    if (btns.length > 2) {
        btns[2].scrollIntoView();
        btns[2].click();
        return { clicked: true, index: 2, total: btns.length };
    }
    return { clicked: false, total: btns.length };
})()
"""

ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_card2, 'returnByValue': True}}))
print("Download card 2 click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
