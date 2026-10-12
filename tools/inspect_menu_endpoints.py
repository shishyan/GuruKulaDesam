import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Click 3-dot menu on first row
    first_row = page.locator('ytd-playlist-video-renderer').first
    btn = first_row.locator('ytd-menu-renderer yt-icon-button#button')
    btn.click()
    time.sleep(1)
    
    # Inspect serviceEndpoints of all menu items
    menu_data = page.evaluate('''() => {
        const items = document.querySelectorAll('ytd-menu-service-item-renderer');
        const results = [];
        for (const item of items) {
            const text = item.innerText.trim();
            const data = item.__data || item.data || {};
            results.push({
                text,
                endpoint: data.data?.serviceEndpoint || data.serviceEndpoint
            });
        }
        return results;
    }''')
    
    print('Menu items and service endpoints:')
    print(json.dumps(menu_data, indent=2))
    
    # Press Escape to close menu
    page.keyboard.press('Escape')
