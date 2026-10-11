import sys, requests, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

# Open fresh tab via CDP HTTP
target_url = "https://studio.youtube.com/video/QXhT9uoA7_w/edit"
new_tab = requests.put(f"http://127.0.0.1:9225/json/new?{target_url}").json()
tab_id = new_tab['id']

time.sleep(10)

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
target_page = None
for page in browser.contexts[0].pages:
    if "QXhT9uoA7_w" in page.url:
        target_page = page
        break

if target_page:
    target_page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/studio_page_debug.png")
    html = target_page.content()
    print("HTML length:", len(html))
    print("Page title:", target_page.title())
    print("Body text snippet:", target_page.locator("body").inner_text()[:300])

requests.put(f"http://127.0.0.1:9225/json/close/{tab_id}")
browser.close()
p.stop()
