import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        
        # Type into the New value input
        input_field = page.locator("input[placeholder*='New value'], input[aria-label*='New value'], input[type='text']").last
        await input_field.click()
        await input_field.fill("50000")
        await asyncio.sleep(1)
        await page.screenshot(path='production/cloud_console_typed_50k.png')
        print("Typed 50000 into input and saved screenshot")

asyncio.run(main())

