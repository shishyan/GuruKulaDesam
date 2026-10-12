import urllib.request
import json
import websocket
import time
import os
import glob
import zipfile
import shutil
from pathlib import Path

DOWNLOAD_DIR = Path.home() / "Downloads"

def inspect_page():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
    flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
    if not flow_tabs:
        print("No Flow tab found")
        return
    ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)
    
    js = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const dls = btns.filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
        const isStop = !!btns.find(b => (b.innerText || '').toLowerCase().includes('stop') || (b.getAttribute('aria-label') || '').toLowerCase().includes('stop'));
        const pcts = Array.from(document.querySelectorAll('*'))
            .filter(el => el.children.length === 0 && /^\\d{1,2}%$/.test((el.innerText || '').trim()))
            .map(el => el.innerText.trim());
        return {
            dlCount: dls.length,
            isStop,
            pcts
        };
    })()
    """
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
    res = json.loads(ws.recv())
    print("Page status:", res.get('result', {}).get('result', {}).get('value'))
    ws.close()

if __name__ == '__main__':
    inspect_page()
