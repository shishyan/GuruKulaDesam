import urllib.request
import json
import websocket
import time

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

# 1. Allow download
import os
from pathlib import Path
dl_dir = str(Path.home() / "Downloads")
ws.send(json.dumps({'id': 1, 'method': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': dl_dir}}))
ws.recv()

# 2. Click topmost download button
js_click = """
(() => {
    // Topmost download button
    const dls = Array.from(document.querySelectorAll('button, [role="button"]'))
        .filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
    if (dls.length > 0) {
        dls[0].scrollIntoView();
        dls[0].click();
        return { clicked: true, text: dls[0].innerText, aria: dls[0].getAttribute('aria-label') };
    }
    return { clicked: false };
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_click, 'returnByValue': True}}))
print("Download click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

time.sleep(2)

# 3. Check for popup menu options
js_menu = """
(() => {
    const items = Array.from(document.querySelectorAll('button, [role="menuitem"], div[role="menuitem"]'));
    const matches = items.filter(el => {
        const t = (el.innerText || '').toLowerCase();
        return t.includes('original') || t.includes('720p') || t.includes('1080p');
    });
    if (matches.length > 0) {
        matches[0].click();
        return { clicked: true, text: matches[0].innerText };
    }
    return { clicked: false, itemsFound: items.map(el => el.innerText).filter(Boolean).slice(0, 10) };
})()
"""
ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': js_menu, 'returnByValue': True}}))
print("Menu option click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

ws.close()
