import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

# Scroll to top
js_scroll_top = """
(() => {
    window.scrollTo(0, 0);
    const scrollables = Array.from(document.querySelectorAll('*')).filter(el => {
        const style = window.getComputedStyle(el);
        return (style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
    });
    scrollables.forEach(s => s.scrollTop = 0);
    return { scrollablesCount: scrollables.length };
})()
"""
ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_scroll_top, 'returnByValue': True}}))
print("Scroll result:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

# Capture screenshot of top
ws.send(json.dumps({'id': 2, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
import base64
res_shot = json.loads(ws.recv())
with open("production/flow_top_cards.png", "wb") as f:
    f.write(base64.b64decode(res_shot.get('result', {}).get('data', '')))

# Get list of cards text
js_cards = """
(() => {
    const cards = Array.from(document.querySelectorAll('div[class*="card"], div[class*="tile"], div[role="listitem"]'));
    const allP = Array.from(document.querySelectorAll('p, span')).map(el => (el.innerText || '').trim()).filter(t => t.startsWith('Create a single continuous'));
    return {
        cardsCount: cards.length,
        promptsFound: allP
    };
})()
"""
ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': js_cards, 'returnByValue': True}}))
print("Prompts found:", json.loads(ws.recv()).get('result', {}).get('result', {}).get('value'))

ws.close()
