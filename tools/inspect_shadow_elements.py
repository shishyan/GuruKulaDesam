from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    script = """() => {
        function getAllElements(root) {
            let res = [];
            let walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, null, false);
            let n;
            while(n = walker.nextNode()) {
                res.push(n);
                if (n.shadowRoot) {
                    res = res.concat(getAllElements(n.shadowRoot));
                }
            }
            return res;
        }
        
        let all = getAllElements(document.body);
        let interactives = all.filter(el => {
            let tag = el.tagName.toLowerCase();
            return tag.includes('button') || tag.includes('link') || el.getAttribute('role') === 'button' || el.hasAttribute('aria-label');
        });
        
        return interactives.map(el => {
            return {
                tag: el.tagName.toLowerCase(),
                id: el.id,
                text: el.innerText ? el.innerText.trim().replace(/\\s+/g, ' ').slice(0, 50) : '',
                aria: el.getAttribute('aria-label') || ''
            };
        }).filter(e => e.text || e.aria || e.id).slice(0, 30);
    }"""
    
    items = page.evaluate(script)
    print(f'Found {len(items)} interactive elements:')
    for it in items:
        print(' ', it)
