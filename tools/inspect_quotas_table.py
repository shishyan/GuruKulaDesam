import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        await page.bring_to_front()
        await page.evaluate("window.scrollBy(0, 600)")
        await asyncio.sleep(2)
        await page.screenshot(path='production/cloud_console_quotas_table.png')
        print("Captured quotas table screenshot")

asyncio.run(main())

