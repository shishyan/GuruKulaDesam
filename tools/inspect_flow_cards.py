import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
f = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')][0]
ws = websocket.create_connection(f['webSocketDebuggerUrl'], suppress_origin=True)

js = """(() => {
    // Look for all video cards / items in the main workspace
    const items = Array.from(document.querySelectorAll('*')).filter(el => {
        const cls = el.className || '';
        return typeof cls === 'string' && (cls.includes('card') || cls.includes('media-item') || cls.includes('result-item') || cls.includes('tile'));
    });
    
    // Find all elements with download icon or download text
    const downloadIcons = Array.from(document.querySelectorAll('i, mat-icon, span'))
        .filter(el => (el.innerText || '').trim() === 'download');
        
    return {
        downloadIconsCount: downloadIcons.length,
        downloadIconsParents: downloadIcons.map(el => {
            const p = el.parentElement;
            return {
                tag: p.tagName,
                cls: p.className,
                aria: p.getAttribute('aria-label'),
                rect: p.getBoundingClientRect()
            };
        }),
        allCards: items.slice(0, 10).map(el => ({ tag: el.tagName, cls: el.className }))
    };
})()"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
