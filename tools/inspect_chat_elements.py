import urllib.request
import json
import websocket

def inspect_chat():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    js = """
    (() => {
        const chatView = document.querySelector('flow-chat-view') || document.querySelector('.messages-list');
        if (!chatView) return [];
        const bubbles = Array.from(chatView.querySelectorAll('.agent-row, .message-row, flow-chat-bubble'));
        return bubbles.map((b, i) => {
            const r = b.getBoundingClientRect();
            const text = (b.innerText || '').slice(0, 80).replace(/\\n/g, ' ');
            const buttons = Array.from(b.querySelectorAll('button, [role="button"]')).map(btn => {
                const r = btn.getBoundingClientRect();
                return {
                    label: btn.getAttribute('aria-label') || btn.innerText,
                    left: r.left,
                    top: r.top,
                    width: r.width,
                    height: r.height
                };
            });
            const media = Array.from(b.querySelectorAll('img, video, canvas, .media-container, [role="img"]')).map(m => {
                const r = m.getBoundingClientRect();
                return {
                    tag: m.tagName,
                    class: m.className,
                    left: r.left,
                    top: r.top,
                    width: r.width,
                    height: r.height
                };
            });
            return {
                index: i,
                text,
                top: r.top,
                height: r.height,
                buttons,
                media
            };
        });
    })()
    """
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
    res = json.loads(ws.recv())
    bubbles = res.get('result', {}).get('result', {}).get('value', [])
    print(f"Found {len(bubbles)} chat bubbles:")
    for b in bubbles:
        print(f"[{b['index']}] {b['text']}")
        for btn in b.get('buttons', []):
            print(f"    Button: '{btn['label']}' at ({btn['left']:.1f}, {btn['top']:.1f})")
        for m in b.get('media', []):
            print(f"    Media: {m['tag']}.{m['class']} at ({m['left']:.1f}, {m['top']:.1f}) size ({m['width']:.1f}x{m['height']:.1f})")
    ws.close()

if __name__ == '__main__':
    inspect_chat()
