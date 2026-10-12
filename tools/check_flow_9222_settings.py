import urllib.request
import json
import time
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [tab for tab in tabs if 'flow.google.com/project' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# 1. Click settings_2 to check model & confirmation settings
js_check_settings = """
(() => {
    const settingsBtn = document.querySelector('button[aria-label*="settings" i], [aria-label*="settings_2" i]') || 
                        Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('settings_2') || b.innerText.includes('settings'));
    if (settingsBtn) {
        settingsBtn.click();
        return 'Clicked settings';
    }
    return 'Settings button not found';
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_check_settings, 'returnByValue': True}}))
print("Settings click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
time.sleep(1)

js_read_settings = """
(() => {
    const text = document.body ? document.body.innerText : '';
    return {
        hasVeo: text.includes('Veo'),
        hasLite: text.includes('Lite'),
        hasNever: text.includes('Never'),
        snippet: text.slice(text.indexOf('Agent settings') > -1 ? text.indexOf('Agent settings') : 0, 800)
    };
})()
"""
ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': js_read_settings, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Settings detail:", json.dumps(res.get('result', {}).get('result', {}).get('value'), indent=2))
ws.close()
