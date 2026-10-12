import urllib.request, json, time, websocket, base64

res = urllib.request.urlopen('http://127.0.0.1:9225/json').read()
tabs = json.loads(res.decode('utf-8'))
page = [t for t in tabs if t.get('type') == 'page'][0]
ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=15)

msg_id = 1
def call(method, params={}):
    global msg_id
    msg_id += 1
    req = {'id': msg_id, 'method': method, 'params': params}
    ws.send(json.dumps(req))
    while True:
        m = json.loads(ws.recv())
        if m.get('id') == msg_id:
            return m.get('result', {})

print('Navigating to mG9IzlD9vmI edit page...')
call('Page.navigate', {'url': 'https://studio.youtube.com/video/mG9IzlD9vmI/edit'})
time.sleep(6)

js = """(() => {
    let title = document.querySelector('#textbox[aria-label*="Title"], ytcp-social-suggestions-textbox[aria-label*="Title"] #textbox');
    let desc = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox');
    let lang = document.querySelector('ytcp-form-language-input#language-input');
    let saveBtn = document.querySelector('#save-button, ytcp-button#save-button, #save');
    return {
        title: title ? title.innerText : null,
        descLen: desc ? desc.innerText.length : 0,
        descSnippet: desc ? desc.innerText.slice(0, 100) : null,
        langText: lang ? lang.innerText : null,
        saveBtnDisabled: saveBtn ? saveBtn.hasAttribute('disabled') : null
    };
})()"""
info = call('Runtime.evaluate', {'expression': js, 'returnByValue': True}).get('result', {}).get('value', {})
print('Edit page info:', info)

ss = call('Page.captureScreenshot')
with open('scratch/mG9_edit_page.png', 'wb') as f:
    f.write(base64.b64decode(ss['data']))
print('Saved screenshot scratch/mG9_edit_page.png')
ws.close()
