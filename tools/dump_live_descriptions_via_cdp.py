import urllib.request, json, time, websocket, os, sys
sys.stdout.reconfigure(encoding='utf-8')

res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
tabs = json.loads(res.decode('utf-8'))
page = [t for t in tabs if t.get('type') == 'page'][0]
ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=25)

msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    i = msg_id
    ws.send(json.dumps({'id': i, 'method': method, 'params': params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get('id') == i:
            return m.get('result', {})

vids = [
    "Mata6vtnrjQ", "mQpQEuXiEZ4", "31xVgvxoiUA",
    "AW4cljBWy2w", "QH-xL37NmGM", "hm7_qUlTUiU"
]

for vid in vids:
    out_p = f"production/descriptions/{vid}.txt"
    if os.path.exists(out_p) and os.path.getsize(out_p) > 500:
        print(f"Skipping {vid}, already exists ({os.path.getsize(out_p)} bytes)")
        continue
    url = f"https://studio.youtube.com/video/{vid}/edit"
    print(f"Reading {vid} from {url}...")
    call("Page.navigate", {"url": url})
    time.sleep(5)
    get_desc = """(() => {
        const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
        return descBox ? descBox.innerText : '';
    })()"""
    desc = call("Runtime.evaluate", {"expression": get_desc, "returnByValue": True}).get("result", {}).get("value", "")
    if desc:
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(desc)
        print(f"  -> Saved {out_p} ({len(desc)} chars)")
    else:
        print(f"  -> Warning: empty desc for {vid}")

ws.close()
print("Done dumping live descriptions!")
