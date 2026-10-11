import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
page = browser.contexts[0].pages[0]

textboxes = page.locator('#textbox').all()
for i, el in enumerate(textboxes):
    aria = el.get_attribute('aria-label') or ''
    txt = el.inner_text().strip()
    print(f"[{i}] aria='{aria}' text='{txt[:80]}'")

browser.close()
p.stop()
