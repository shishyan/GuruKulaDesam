import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    const cards = Array.from(document.querySelectorAll('.media-card, .video-card, .tile, [class*="card"]'));
    const playIcons = Array.from(document.querySelectorAll('mat-icon, i, span')).filter(el => (el.innerText || '').trim() === 'play_circle');
    const dls = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => (b.innerText || '').toLowerCase().includes('download') || (b.getAttribute('aria-label') || '').toLowerCase().includes('download'));
    return {
        cardsCount: cards.length,
        playIconsCount: playIcons.length,
        downloadButtonsCount: dls.length,
        hasStop: document.body.innerText.includes('Stop')
    };
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
