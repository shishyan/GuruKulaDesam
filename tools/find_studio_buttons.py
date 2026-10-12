from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    script = """() => {
        function findInShadow(node, predicate) {
            let results = [];
            if (predicate(node)) results.push(node);
            if (node.shadowRoot) {
                results = results.concat(findInShadow(node.shadowRoot, predicate));
            }
            for (let child of node.children || []) {
                results = results.concat(findInShadow(child, predicate));
            }
            return results;
        }
        
        let buttons = findInShadow(document.body, n => {
            let tag = (n.tagName || '').toLowerCase();
            return tag.includes('button') || tag === 'a' || n.getAttribute && n.getAttribute('role') === 'button';
        });
        
        return buttons.map(b => ({
            tag: b.tagName.toLowerCase(),
            text: (b.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 40),
            aria: b.getAttribute('aria-label') || '',
            id: b.id || ''
        })).filter(x => x.text || x.aria);
    }"""
    
    items = page.evaluate(script)
    print(f'Total interactive items in Shadow DOM: {len(items)}')
    for it in items[:35]:
        print('  ', it)
