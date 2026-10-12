import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
page = browser.contexts[0].pages[0]

print("Page URL:", page.url)
print("Page Title:", page.title())

# Let's search inside frames or root
title_box = page.locator('#title-textarea #textbox, [aria-label*="Add a title"], [aria-label*="Title"]').first
print("Title box count:", title_box.count())
if title_box.count() > 0:
    print("Title box visible:", title_box.is_visible())
    print("Title text:", repr(title_box.inner_text()))

desc_box = page.locator('#description-textarea #textbox, [aria-label*="Description"]').first
print("Desc box count:", desc_box.count())
if desc_box.count() > 0:
    print("Desc box visible:", desc_box.is_visible())
    print("Desc text preview:", repr(desc_box.inner_text()[:100]))

browser.close()
p.stop()
