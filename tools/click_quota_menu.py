import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        
        # Click the 3 dots menu on the row
        menu_btn = page.locator("button[aria-label*='Action'], button:has-text('more_vert'), td button").last
        await menu_btn.click()
        await asyncio.sleep(1)
        await page.screenshot(path='production/cloud_console_menu_open.png')
        print("Clicked menu button and saved screenshot")

asyncio.run(main())

