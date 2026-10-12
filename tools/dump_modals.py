from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    cdp = ctx.new_cdp_session(page)
    
    expr = '''
    (() => {
        function getVisibleText(node) {
            let res = [];
            if (node.shadowRoot) res = res.concat(getVisibleText(node.shadowRoot));
            for (let c of node.children || []) {
                let tag = c.tagName.toLowerCase();
                if (tag.includes('dialog') || tag.includes('modal') || c.getAttribute('role') === 'dialog' || tag.includes('overlay')) {
                    res.push({tag: tag, id: c.id, text: c.innerText.trim().replace(/\\s+/g, ' ')});
                }
                res = res.concat(getVisibleText(c));
            }
            return res;
        }
        return JSON.stringify(getVisibleText(document.body).filter(x => x.text));
    })()
    '''
    res = cdp.send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
    items = json.loads(res['result']['value'])
    print(f'Modals with text: {len(items)}')
    for it in items:
        print('  *', it['tag'], 'id=' + it['id'], '-->', it['text'][:150])
