import urllib.request
import json
import websocket
import base64
import time

def click_option():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
    t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
    ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

    # Click the option-row containing 'Always approve' or 'Approve'
    js_click = """
    (() => {
        const optionRows = Array.from(document.querySelectorAll('.choice-container .option-row, flow-permission-message .option-row, .option-row'));
        const target = optionRows.find(el => el.textContent.includes('Always approve')) || optionRows.find(el => el.textContent.includes('Approve'));
        if (target) {
            target.scrollIntoView();
            target.click();
            // Also try clicking the child span or label if present
            const span = target.querySelector('.option-label, span');
            if (span) span.click();
            return { success: true, text: target.textContent.trim() };
        }
        return { success: false, foundRows: optionRows.map(r => r.textContent.trim()) };
    })()
    """

    ws.send(json.dumps({
        'id': 1,
        'method': 'Runtime.evaluate',
        'params': {'expression': js_click, 'returnByValue': True}
    }))
    res = json.loads(ws.recv())
    val = res.get('result', {}).get('result', {}).get('value', {})
    print("Click result:", json.dumps(val, indent=2))

    time.sleep(3)

    # Capture screenshot
    ws.send(json.dumps({'id': 2, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
    res2 = json.loads(ws.recv())
    img_b64 = res2.get('result', {}).get('data', '')
    shot_path = 'C:/Users/Shishyan/.gemini/antigravity/brain/3487bd75-58a3-46ff-b8c8-f0b8c719cf46/flow_clicked_always_approve.png'
    with open(shot_path, 'wb') as f:
        f.write(base64.b64decode(img_b64))
    print("Screenshot saved to", shot_path)

    # Get updated text
    ws.send(json.dumps({
        'id': 3,
        'method': 'Runtime.evaluate',
        'params': {'expression': '(() => ({ text: document.body.innerText.slice(0, 1000) }))()', 'returnByValue': True}
    }))
    res3 = json.loads(ws.recv())
    print("Updated text:")
    print(res3.get('result', {}).get('result', {}).get('value', {}).get('text', ''))
    ws.close()

if __name__ == '__main__':
    click_option()
