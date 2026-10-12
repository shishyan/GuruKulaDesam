import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    time.sleep(3)
    print('Current Page URL:', page.url)
    print('Current Page Title:', page.title())
    
    script = """() => {
        const rows = document.querySelectorAll('ytcp-video-translations-row, ytcp-table-row, [role="row"]');
        return Array.from(rows).map(r => r.innerText.replace(/\\s+/g, ' ').trim()).filter(Boolean);
    }"""
    rows = page.evaluate(script)
    print(f'Rows count: {len(rows)}')
    for i, r in enumerate(rows):
        clean_text = r.encode('ascii', 'ignore').decode('ascii')
        print(f'  [{i}] {clean_text}')
