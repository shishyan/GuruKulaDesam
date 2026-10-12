import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'console.cloud.google.com' in t.url][0]
        
        # Click "Edit quota" in the open popup menu
        edit_quota_btn = page.locator("text='Edit quota'")
        await edit_quota_btn.click()
        await asyncio.sleep(2)
        await page.screenshot(path='production/cloud_console_edit_quota_dialog.png')
        print("Clicked Edit quota and captured screenshot")

asyncio.run(main())

