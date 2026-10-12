import urllib.request, json, time, websocket

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

# Find file inputs on current page
js = """(() => {
    let inputs = Array.from(document.querySelectorAll('input[type="file"]'));
    let showMore = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').includes('SHOW MORE') || (b.innerText || '').includes('Show more'));
    return {
        fileInputs: inputs.map(i => ({ id: i.id, accept: i.accept, className: i.className })),
        hasShowMore: !!showMore
    };
})()"""
info = call('Runtime.evaluate', {'expression': js, 'returnByValue': True}).get('result', {}).get('value', {})
print('Page inputs & showMore:', info)

# If showMore exists, click it and find language input
if info.get('hasShowMore'):
    call('Runtime.evaluate', {'expression': """(() => {
        let b = Array.from(document.querySelectorAll('ytcp-button, button')).find(b => (b.innerText || '').includes('SHOW MORE') || (b.innerText || '').includes('Show more'));
        if (b) b.click();
    })()"""})
    time.sleep(2)
    
lang_info = call('Runtime.evaluate', {'expression': """(() => {
    let lang = document.querySelector('ytcp-form-language-input, [label="Video language"]');
    return {
        found: !!lang,
        text: lang ? lang.innerText : null
    };
})()""", 'returnByValue': True}).get('result', {}).get('value', {})
print('Language element info:', lang_info)

ws.close()
