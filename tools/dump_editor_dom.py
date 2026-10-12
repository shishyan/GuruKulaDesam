import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    # Evaluate inside the editor
    res = page.evaluate('''() => {
        let editor = document.querySelector('ytcp-subtitles-editor') || document.querySelector('ytcp-dialog');
        if (!editor) return "No editor found";
        
        function getTree(el, depth=0) {
            if (depth > 6) return "";
            let s = "  ".repeat(depth) + el.tagName.toLowerCase();
            if (el.id) s += "#" + el.id;
            if (el.className) s += "." + (typeof el.className === 'string' ? el.className.split(' ').join('.') : '');
            let txt = (el.innerText || "").trim().slice(0, 30);
            if (txt) s += ` [${txt}]`;
            s += "\\n";
            
            let children = Array.from(el.children);
            if (el.shadowRoot) {
                s += "  ".repeat(depth+1) + "#shadow-root\\n";
                children = children.concat(Array.from(el.shadowRoot.children));
            }
            for (let c of children) {
                s += getTree(c, depth + 1);
            }
            return s;
        }
        return getTree(editor);
    }''')
    
    print(res[:3000])
