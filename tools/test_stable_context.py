from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Wait for the table or app element to be attached and stable
    print('Waiting for stable container...')
    page.wait_for_selector('ytcp-video-section', state='attached', timeout=10000)
    print('Container ready! Title:', page.title())
    
    # Now query text safely
    text = page.inner_text('body')
    print('Page text preview:')
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for l in lines[:15]:
        print('  *', l.encode('ascii', 'ignore').decode('ascii'))
