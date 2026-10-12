import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = await context.new_page()
        print("Navigating to YouTube API quota form...")
        await page.goto('https://support.google.com/youtube/contact/yt_api_form', wait_until='networkidle')
        await asyncio.sleep(3)
        title = await page.title()
        print(f"Page Title: {title}")
        
        # Take a screenshot to inspect
        await page.screenshot(path='production/quota_form_step1.png')
        print("Saved screenshot to production/quota_form_step1.png")

        # Check visible text
        content = await page.content()
        with open('production/quota_form_dom.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Dumped DOM to production/quota_form_dom.html")

asyncio.run(main())

