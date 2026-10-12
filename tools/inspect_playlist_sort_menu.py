import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    page.goto('https://www.youtube.com/playlist?list=PLP-GdNkY_qyo', wait_until='domcontentloaded')
    time.sleep(4)

    # Click the sort button
    clicked = page.evaluate('''() => {
        const allBtns = Array.from(document.querySelectorAll('button, tp-yt-paper-button'));
        const sortBtn = allBtns.find(b => b.innerText && b.innerText.includes('Date published'));
        if (sortBtn) {
            sortBtn.click();
            return { clicked: true, text: sortBtn.innerText };
        }
        return { clicked: false };
    }''')
    print("Clicked sort button:", clicked)
    time.sleep(2)

    menu_items = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('ytd-menu-service-item-renderer, tp-yt-paper-item, [role="menuitem"]')).map(el => el.innerText.trim()).filter(Boolean);
    }''')
    print("Sort menu options:", menu_items)

    # If Manual option exists, click it!
    manual_clicked = page.evaluate('''() => {
        const items = Array.from(document.querySelectorAll('ytd-menu-service-item-renderer, tp-yt-paper-item, [role="menuitem"]'));
        const manual = items.find(el => el.innerText && (el.innerText.includes('Manual') || el.innerText.includes('Date added (oldest)')));
        if (manual) {
            manual.click();
            return { clicked: true, text: manual.innerText };
        }
        return { clicked: false };
    }''')
    print("Clicked manual/order:", manual_clicked)
    time.sleep(3)

    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\after_sort_change.png')
    page.close()
