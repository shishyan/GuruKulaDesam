import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
page = browser.contexts[0].pages[0]

title_locators = [
    '#title-textarea #textbox',
    '#textbox[aria-label*="Title"]',
    'ytcp-video-title #textbox',
    'ytcp-social-suggestions-textbox[aria-label*="Title"] #textbox',
    '#textbox[aria-label*="title"]'
]

for loc in title_locators:
    l = page.locator(loc)
    count = l.count()
    print(f"Locator {loc}: count={count}")
    if count > 0:
        print("  Visible:", l.first.is_visible())
        print("  Text:", repr(l.first.inner_text()))

save_btn = page.locator('#save, ytcp-button#save-button, ytcp-button:has-text("Save")')
print("Save button count:", save_btn.count(), "enabled:", save_btn.first.is_enabled() if save_btn.count() > 0 else False)

browser.close()
p.stop()
