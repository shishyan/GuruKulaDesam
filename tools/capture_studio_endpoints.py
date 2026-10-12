import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page() # open fresh page so it has clean event listeners
    
    studio_endpoints = []
    
    def log_request(req):
        url = req.url
        if 'youtubei' in url or 'studio' in url or 'caption' in url:
            method = req.method
            endpoint = url.split('?')[0]
            studio_endpoints.append((method, endpoint))
            
    page.on('request', log_request)
    
    print('Navigating fresh tab to video translations...')
    page.goto('https://studio.youtube.com/video/NK2PqzKz3aI/translations', wait_until='domcontentloaded')
    time.sleep(5)
    
    print(f'Captured {len(studio_endpoints)} internal studio endpoints:')
    for method, ep in list(set(studio_endpoints))[:20]:
        print(f'  {method} {ep}')
        
    page.close()
