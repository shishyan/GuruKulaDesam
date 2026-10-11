import sys, requests, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

target_url = 'https://studio.youtube.com/video/IHMZsM7LJf8/edit'
new_tab = requests.put(f'http://127.0.0.1:9225/json/new?{target_url}').json()
tab_id = new_tab['id']
print('Opened tab:', tab_id)
time.sleep(8)

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
target_page = None
for page in browser.contexts[0].pages:
    if 'IHMZsM7LJf8' in page.url:
        target_page = page
        break

if target_page:
    print('Page URL:', target_page.url)
    print('Page Title:', target_page.title())
    desc_elem = target_page.locator('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox').first
    if desc_elem.is_visible():
        print('Description element visible!')
        print('Current description preview:\n', repr(desc_elem.inner_text()[:200]))
    else:
        print('Description element NOT visible.')

requests.put(f'http://127.0.0.1:9225/json/close/{tab_id}')
browser.close()
p.stop()
