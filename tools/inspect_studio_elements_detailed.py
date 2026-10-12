import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
page = browser.contexts[0].pages[0]

print('Current URL:', page.url)
print('Current title:', page.title())

textboxes = page.locator('#textbox').all()
print('Total #textbox elements:', len(textboxes))
for i, tb in enumerate(textboxes):
    aria = tb.get_attribute('aria-label') or ''
    txt = tb.inner_text()[:60].replace('\n', ' ')
    print(f"[{i}] aria-label='{aria}' text={repr(txt)}")

# Also look for contenteditable or textarea
inputs = page.locator('div[contenteditable="true"]').all()
print('Total contenteditable elements:', len(inputs))
for i, el in enumerate(inputs):
    aria = el.get_attribute('aria-label') or ''
    txt = el.inner_text()[:60].replace('\n', ' ')
    print(f"[{i}] contenteditable aria-label='{aria}' text={repr(txt)}")

browser.close()
p.stop()
