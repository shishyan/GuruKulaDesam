import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        # find the tab that is at yt_api_form
        page = None
        for p_tab in context.pages:
            if 'yt_api_form' in p_tab.url:
                page = p_tab
                break
        
        if not page:
            print("Could not find yt_api_form tab, creating new one...")
            page = await context.new_page()
            await page.goto('https://support.google.com/youtube/contact/yt_api_form')
        
        await page.bring_to_front()
        # Scroll down
        await page.evaluate("window.scrollBy(0, 800)")
        await asyncio.sleep(1)
        await page.screenshot(path='production/quota_form_step1_scrolled.png')
        print("Saved scrolled screenshot")

asyncio.run(main())

