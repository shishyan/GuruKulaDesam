import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        
        # Click on Section 2 checkbox / label
        sec2 = page.locator("text='Section 2: Organization and Contact Information'")
        await sec2.click()
        await asyncio.sleep(1)
        await page.screenshot(path='production/quota_form_section2.png')
        print("Clicked Section 2 and saved screenshot")

asyncio.run(main())

