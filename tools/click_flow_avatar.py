import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com/project' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# 1. Click top right profile avatar button to open Google Account switcher
js_click_avatar = """
(() => {
    // The top-right circular avatar button with initial 'G' or profile image
    const btns = Array.from(document.querySelectorAll('button, [role="button"], a'));
    const avatar = btns.find(b => {
        const aria = (b.getAttribute('aria-label') || '').toLowerCase();
        return aria.includes('google account') || aria.includes('account details') || b.innerText.trim() === 'G';
    });
    if (avatar) {
        avatar.click();
        return 'Clicked avatar';
    }
    return 'Avatar button not found';
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_click_avatar, 'returnByValue': True}}))
print("Avatar click:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))
ws.close()
