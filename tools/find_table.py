import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        
        # Find all table headers or text
        res = await page.evaluate('''() => {
            const table = document.querySelector('table');
            if (!table) return 'No table found';
            table.scrollIntoView();
            return table.innerText.substring(0, 500);
        }''')
        print("Table info:", res)
        await asyncio.sleep(2)
        await page.screenshot(path='production/cloud_console_table_view.png')

asyncio.run(main())

