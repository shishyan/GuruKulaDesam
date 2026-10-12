import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        
        # Click "View quotas & system limits" link
        link = page.locator("text='View quotas & system limits'").first
        await link.click()
        await asyncio.sleep(3)
        await page.screenshot(path='production/cloud_console_quotas_limits.png')
        print("Clicked link and saved screenshot")

asyncio.run(main())

