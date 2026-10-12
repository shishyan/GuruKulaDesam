from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    print('Page URL:', page.url)
    
    # Query all buttons and action links
    elements = page.locator('button, [role="button"], a[href*="subtitles"], #upload-subtitles, [aria-label*="subtitle"], [aria-label*="Edit"]').all()
    print(f'Total action elements: {len(elements)}')
    for i, el in enumerate(elements[:25]):
        try:
            txt = el.inner_text().strip().replace('\n', ' ')
            aria = el.get_attribute('aria-label') or ''
            el_id = el.get_attribute('id') or ''
            if txt or aria or el_id:
                print(f'  [{i}] tag={el.evaluate("e => e.tagName")} id={el_id} aria={aria[:40]} text={txt[:40]}')
        except Exception:
            pass
