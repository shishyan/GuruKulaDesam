import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        
        # Click "Done" button inside the card
        done_btn = page.locator("button:has-text('Done')")
        await done_btn.click()
        await asyncio.sleep(1)
        await page.screenshot(path='production/cloud_console_clicked_done.png')
        print("Clicked Done and saved screenshot")

asyncio.run(main())

