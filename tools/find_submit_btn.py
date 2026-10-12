import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
flow_tabs = [t for t in tabs if 'flow.google.com/project' in t.get('url', '')]
ws = websocket.create_connection(flow_tabs[0]['webSocketDebuggerUrl'], suppress_origin=True)

js = """
(() => {
    const editor = document.querySelector('div.ProseMirror');
    const container = editor ? editor.closest('form, div[class*="input"], div[class*="prompt"], div[class*="bottom"]') : null;
    const buttons = Array.from(document.querySelectorAll('button, [role="button"]')).map((b, i) => ({
        index: i,
        tag: b.tagName,
        text: (b.innerText || '').trim(),
        aria: b.getAttribute('aria-label') || '',
        title: b.getAttribute('title') || '',
        disabled: b.disabled || b.getAttribute('aria-disabled') === 'true',
        classes: b.className
    }));
    return {
        hasEditor: !!editor,
        editorText: editor ? editor.innerText : '',
        nearbyButtons: buttons.filter(b => b.text.includes('arrow') || b.aria.includes('Submit') || b.aria.includes('Generate') || b.text.includes('send') || b.text.includes('return'))
    };
})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
res = json.loads(ws.recv())
print(json.dumps(res.get('result', {}).get('result', {}).get('value', {}), indent=2))
ws.close()
