import sys, requests, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

# 1. Open fresh tab via CDP HTTP
target_url = "https://studio.youtube.com/video/QXhT9uoA7_w/edit"
new_tab = requests.put(f"http://127.0.0.1:9225/json/new?{target_url}").json()
tab_id = new_tab['id']
print(f"Opened new tab: {tab_id}")

# 2. Wait 8s for Studio SPA to mount components
time.sleep(8)

# 3. Connect via Playwright and find the tab
p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
target_page = None
for page in browser.contexts[0].pages:
    if "QXhT9uoA7_w" in page.url:
        target_page = page
        break

if not target_page:
    target_page = browser.contexts[0].pages[-1]

print("Target page URL:", target_page.url)
print("Target page title:", target_page.title())

textboxes = target_page.locator('#textbox').all()
print("Total #textbox elements:", len(textboxes))
for i, tb in enumerate(textboxes):
    aria = tb.get_attribute('aria-label') or ''
    txt = tb.inner_text()[:60].replace('\n', ' ')
    print(f"[{i}] aria-label='{aria}' text={repr(txt)}")

# Close the tab via CDP HTTP
requests.put(f"http://127.0.0.1:9225/json/close/{tab_id}")
browser.close()
p.stop()
