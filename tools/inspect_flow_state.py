import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
if not flow_tabs:
    print("No Flow project tab found!")
    exit(1)

ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const textareas = Array.from(document.querySelectorAll('textarea, div.ProseMirror, [contenteditable="true"]'));
    const buttons = Array.from(document.querySelectorAll('button, [role="button"]')).map(b => (b.innerText || b.getAttribute('aria-label') || '').trim()).filter(Boolean);
    const videos = Array.from(document.querySelectorAll('video')).map(v => ({ src: v.src, currentSrc: v.currentSrc }));
    return {
        inputs: textareas.map(el => ({ tag: el.tagName, class: el.className, text: el.innerText })),
        buttonsSnippet: buttons.slice(0, 25),
        videosCount: videos.length
    };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
