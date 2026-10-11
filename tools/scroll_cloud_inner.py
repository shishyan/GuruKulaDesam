import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        
        # Scroll the element or click on the table
        await page.evaluate('''() => {
            const el = document.querySelector('.cfc-main-pane, [role="main"], mat-drawer-content') || document.scrollingElement || document.body;
            el.scrollTop = 1200;
            window.scrollBy(0, 1200);
        }''')
        await asyncio.sleep(2)
        await page.screenshot(path='production/cloud_console_scrolled_inner.png')
        print("Scrolled inner and saved screenshot")

asyncio.run(main())

