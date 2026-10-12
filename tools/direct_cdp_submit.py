import urllib.request
import json
import websocket
import base64

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/list').read())
t = [tab for tab in tabs if 'flow.google.com/project' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# 1. Clear ProseMirror and insert prompt
prompt = "Close atmospheric pan over bronze Kuthuvilakku oil lamps. Create a single continuous 16:9 cinematic slow crane rise at 24 fps. Looking across a serene temple lotus tank reflecting the rising sun and distant Dravidian temple gopuram in soft mist. Profound inner peace, ethical clarity, timeless wisdom. *Exclusions:* No rapid motion, no modern artifacts, no text, no audio."

js_code = f"""
(() => {{
    const ed = document.querySelector('div.ProseMirror');
    if (!ed) return 'no_editor';
    ed.focus();
    document.execCommand('selectAll', false, null);
    document.execCommand('delete', false, null);
    document.execCommand('insertText', false, {json.dumps(prompt)});
    
    // Find generate button
    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('arrow_forward') || (b.getAttribute('aria-label') || '').includes('Start generation'));
    if (btn) {{
        btn.click();
        return 'clicked_button';
    }} else {{
        return 'no_btn';
    }}
}})()
"""

ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js_code, 'returnByValue': True}}))
res = json.loads(ws.recv())
print("Submit result:", res.get('result', {}).get('result', {}).get('value'))
ws.close()
