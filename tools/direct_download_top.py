import urllib.request
import json
import websocket
import time
import os
import glob
from pathlib import Path

DOWNLOAD_DIR = Path.home() / "Downloads"

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

# Set download behavior
ws.send(json.dumps({'id': 1, 'method': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': str(DOWNLOAD_DIR)}}))
ws.recv()

before_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip")))

js = """(() => {
    const dls = Array.from(document.querySelectorAll('button, [role="button"]'))
        .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
    if (dls.length > 0) {
        dls[0].scrollIntoView();
        dls[0].click();
        return { clicked: true, text: dls[0].innerText, aria: dls[0].getAttribute('aria-label') };
    }
    return { clicked: false };
})()"""

ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Click download result:", res.get('result', {}).get('result', {}).get('value'))
ws.close()

for i in range(15):
    time.sleep(1)
    new_zips = set(glob.glob(str(DOWNLOAD_DIR / "*.zip"))) - before_zips
    if new_zips:
        print("Success! Downloaded:", new_zips)
        break
else:
    print("Download timeout.")
