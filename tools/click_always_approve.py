import urllib.request
import json
import websocket
import base64
import time

def click_approve():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Click 'Always approve' or 'Approve'
    js_code = """
    (() => {
        const buttons = Array.from(document.querySelectorAll('button, [role="button"]'));
        const alwaysBtn = buttons.find(b => b.innerText.includes('Always approve'));
        if (alwaysBtn) {
            alwaysBtn.click();
            return 'CLICKED_ALWAYS_APPROVE';
        }
        const appBtn = buttons.find(b => b.innerText.trim() === 'Approve' || b.innerText.includes('Approve'));
        if (appBtn) {
            appBtn.click();
            return 'CLICKED_APPROVE';
        }
        return 'BUTTON_NOT_FOUND';
    })()
    """

    ws.send(json.dumps({
        'id': 1,
        'method': 'Runtime.evaluate',
        'params': {'expression': js_code, 'returnByValue': True}
    }))
    res = json.loads(ws.recv())
    action_taken = res.get('result', {}).get('result', {}).get('value')
    print("Action taken:", action_taken)

    time.sleep(3)

    # Take screenshot
    ws.send(json.dumps({'id': 2, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
    res2 = json.loads(ws.recv())
    img_b64 = res2.get('result', {}).get('data', '')
    shot_path = 'C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_after_always_approve.png'
    with open(shot_path, 'wb') as f:
        f.write(base64.b64decode(img_b64))
    print("Saved screenshot to", shot_path)

    # Get body text
    ws.send(json.dumps({
        'id': 3,
        'method': 'Runtime.evaluate',
        'params': {'expression': 'document.body ? document.body.innerText.slice(0, 1000) : ""', 'returnByValue': True}
    }))
    res3 = json.loads(ws.recv())
    print("Page text snippet after click:")
    print(res3.get('result', {}).get('result', {}).get('value', ''))
    ws.close()

if __name__ == '__main__':
    click_approve()
