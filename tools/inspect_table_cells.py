import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    time.sleep(2)
    
    script = """() => {
        const rows = document.querySelectorAll('ytcp-video-translations-row, tr, [role="row"]');
        return Array.from(rows).map(row => {
            const cells = row.querySelectorAll('ytcp-table-cell, td, [role="cell"]');
            return Array.from(cells).map(c => ({
                text: c.innerText.trim().replace(/\\s+/g, ' '),
                innerHTML: c.innerHTML.slice(0, 200)
            }));
        });
    }"""
    data = page.evaluate(script)
    print(f'Rows: {len(data)}')
    for i, r in enumerate(data):
        print(f'Row {i}: {len(r)} cells')
        for j, c in enumerate(r):
            print(f'  Cell {j}: text="{c["text"]}"')
            print(f'    HTML: {c["innerHTML"][:100]}')
