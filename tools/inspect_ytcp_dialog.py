from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    cdp = ctx.new_cdp_session(page)
    
    expr = '''
    (() => {
        let dlgs = document.querySelectorAll('ytcp-dialog');
        let res = [];
        for (let d of dlgs) {
            function scan(node) {
                let out = [];
                if (node.shadowRoot) out = out.concat(scan(node.shadowRoot));
                for (let c of node.children || []) {
                    out.push({tag: c.tagName, id: c.id, text: (c.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 60)});
                    out = out.concat(scan(c));
                }
                return out;
            }
            res.push({dialogId: d.id, items: scan(d)});
        }
        return JSON.stringify(res);
    })()
    '''
    res = cdp.send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
    data = json.loads(res['result']['value'])
    for d in data:
        print(f"Dialog {d['dialogId']}: {len(d['items'])} items")
        for it in d['items']:
            if it['text']:
                print('  *', it)
