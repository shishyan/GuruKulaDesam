import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    page = b.new_page()
    messages = []
    page.on('console', lambda msg: messages.append(f'[{msg.type}] {msg.text}'))
    page.on('pageerror', lambda exc: messages.append(f'[PAGE_ERROR] {exc}'))
    
    # Listen to navigation
    navs = []
    page.on('framenavigated', lambda frame: navs.append(frame.url) if frame == page.main_frame else None)
    
    page.goto('http://localhost:8000/index.html', wait_until='domcontentloaded')
    page.wait_for_timeout(4000) # wait 4 seconds to observe if any reload is triggered
    
    print('Total main frame navigations:', len(navs), flush=True)
    print('Navigations list:', navs, flush=True)
    print('Console messages count:', len(messages), flush=True)
    for m in messages[:10]:
        print(' ', m, flush=True)
    b.close()
