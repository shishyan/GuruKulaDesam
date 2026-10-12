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

# Click language input trigger
click_lang = """(() => {
    let lang = document.querySelector('ytcp-form-language-input, ytcp-language-selector');
    if (!lang) return { found: false };
    let trigger = lang.querySelector('#trigger, .select-container, ytcp-dropdown-trigger');
    if (trigger) {
        trigger.click();
        return { found: true, clickedTrigger: true };
    }
    lang.click();
    return { found: true, clickedLang: true };
})()"""
r = call('Runtime.evaluate', {'expression': click_lang, 'returnByValue': True}).get('result', {}).get('value', {})
print('Click lang result:', r)
time.sleep(1.5)

# Find options in opened dropdown
find_tamil = """(() => {
    let items = Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu-item, [role="option"]'));
    let tamil = items.find(i => (i.innerText || '').trim() === 'Tamil');
    return {
        totalItems: items.length,
        foundTamil: !!tamil,
        sample: items.slice(0, 5).map(i => i.innerText.trim())
    };
})()"""
t_info = call('Runtime.evaluate', {'expression': find_tamil, 'returnByValue': True}).get('result', {}).get('value', {})
print('Tamil option info:', t_info)

if t_info.get('foundTamil'):
    call('Runtime.evaluate', {'expression': """(() => {
        let items = Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu-item, [role="option"]'));
        let tamil = items.find(i => (i.innerText || '').trim() === 'Tamil');
        if (tamil) {
            tamil.click();
            return true;
        }
        return false;
    })()"""})
    time.sleep(1)
    print("Clicked Tamil option!")

ws.close()
