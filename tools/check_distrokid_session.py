import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    try:
        print("Navigating to https://distrokid.com ...")
        # Use commit or domcontentloaded with a 15s timeout
        page.goto('https://distrokid.com', wait_until='commit', timeout=15000)
        time.sleep(5)
        print("Page URL:", page.url)
        print("Page Title:", page.title())
        page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\distrokid_landing.png')
        
        # Check if logged in (look for sign in button or user avatar/dashboard)
        body = page.evaluate('() => document.body.innerText.slice(0, 1000)')
        print("Body snippet:", repr(body[:300]))
    except Exception as e:
        print("Navigation error:", e)
    finally:
        page.close()
