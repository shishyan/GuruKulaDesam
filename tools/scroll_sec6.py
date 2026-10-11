import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        
        await page.evaluate('''() => {
            const el = document.querySelector('#upload_1_1') || document.querySelector("input[name='upload_1_1']");
            if (el) {
                el.closest('.field').scrollIntoView();
            }
        }''')
        await asyncio.sleep(1)
        await page.screenshot(path='production/compliance/section6_view.png')
        print("Captured Section 6 screenshot")

asyncio.run(main())

