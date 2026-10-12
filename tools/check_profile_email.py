import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        await page.bring_to_front()
        
        # Check what contact email might already be present
        email_val = await page.evaluate('''() => {
            const emailInput = document.querySelector('#organization_contact_email_address');
            return emailInput ? emailInput.value : '';
        }''')
        print(f"Current email value in form: '{email_val}'")

        # Let's see what email addresses appear in the top-right account menu
        profile_info = await page.evaluate('''() => {
            const avatar = document.querySelector('img[alt*="@"], button[aria-label*="@"], div[aria-label*="@"]');
            return avatar ? (avatar.getAttribute('aria-label') || avatar.getAttribute('alt')) : '';
        }''')
        print(f"Profile info from header: '{profile_info}'")

asyncio.run(main())

