import time, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print('Current URL:', page.url)
    print('Current Title:', page.title())
    
    page.screenshot(path='scratch/kft_rendered.png')
    print('Saved scratch/kft_rendered.png')
