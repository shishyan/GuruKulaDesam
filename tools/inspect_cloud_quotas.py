import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = await context.new_page()
        print("Navigating to Cloud Console Quotas page...")
        await page.goto('https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas?project=guru-kula-desam', wait_until='domcontentloaded')
        await asyncio.sleep(5)
        print("Page title:", await page.title())
        await page.screenshot(path='production/cloud_console_quotas.png')
        print("Saved screenshot to production/cloud_console_quotas.png")

asyncio.run(main())

