import urllib.request
import json
import websocket
import base64
import time

def inspect_canvas_card():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Find the video card on the canvas or in the chat
    js = """
    (() => {
        // Look for cards or images on canvas
        const all = Array.from(document.querySelectorAll('*'));
        const candidates = all.filter(el => {
            const r = el.getBoundingClientRect();
            return r.left > 100 && r.left < 400 && r.top > 60 && r.top < 200 && r.width > 150 && r.height > 100;
        });
        
        return candidates.map(el => {
            const r = el.getBoundingClientRect();
            return {
                tag: el.tagName,
                className: el.className,
                left: r.left,
                top: r.top,
                width: r.width,
                height: r.height
            };
        });
    })()
    """
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}}))
    res = json.loads(ws.recv())
    cards = res.get('result', {}).get('result', {}).get('value', [])
    print("Found canvas cards:", len(cards))
    if cards:
        print("First candidate:", json.dumps(cards[0], indent=2))
        
        # Click on the card center
        r = cards[0]
        cx = r['left'] + r['width'] / 2
        cy = r['top'] + r['height'] / 2
        print(f"Clicking at ({cx}, {cy})...")
        
        # Dispatch mouse click at cx, cy
        ws.send(json.dumps({
            'id': 2,
            'method': 'Input.dispatchMouseEvent',
            'params': {'type': 'mousePressed', 'x': cx, 'y': cy, 'button': 'left', 'clickCount': 1}
        }))
        json.loads(ws.recv())
        ws.send(json.dumps({
            'id': 3,
            'method': 'Input.dispatchMouseEvent',
            'params': {'type': 'mouseReleased', 'x': cx, 'y': cy, 'button': 'left', 'clickCount': 1}
        }))
        json.loads(ws.recv())
        
        time.sleep(3)
        
        # Check screenshot after click
        ws.send(json.dumps({'id': 4, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
        res_shot = json.loads(ws.recv())
        shot_path = 'C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_card_clicked.png'
        with open(shot_path, 'wb') as f:
            f.write(base64.b64decode(res_shot.get('result', {}).get('data', '')))
        print("Saved screenshot to", shot_path)

        # Check for any new buttons (like download, play, extend, etc.)
        ws.send(json.dumps({
            'id': 5,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': 'Array.from(document.querySelectorAll("button, [role=\'button\']")).map(b => b.getAttribute("aria-label") || b.innerText).filter(Boolean)',
                'returnByValue': True
            }
        }))
        res_btn = json.loads(ws.recv())
        print("Buttons after card click:", res_btn.get('result', {}).get('result', {}).get('value', [])[:30])

    ws.close()

if __name__ == '__main__':
    inspect_canvas_card()
