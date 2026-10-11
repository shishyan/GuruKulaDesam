import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
page = browser.contexts[0].pages[0]

url = "https://studio.youtube.com/video/IHMZsM7LJf8/edit"
print(f"Navigating page to {url}...")
page.goto(url, wait_until="domcontentloaded")
time.sleep(6)

print("Page URL:", page.url)
print("Page Title:", page.title())

desc_elem = page.locator('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox').first
if desc_elem.is_visible():
    print("Description element visible!")
    print("Current description preview:\n", repr(desc_elem.inner_text()[:200]))
else:
    print("Description element NOT visible. Checking all textboxes...")
    for i, el in enumerate(page.locator('#textbox').all()):
        print(f"[{i}] aria={el.get_attribute('aria-label')} text={repr(el.inner_text()[:50])}")

browser.close()
p.stop()
